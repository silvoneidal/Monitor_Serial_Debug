 # pyinstaller --onefile -w seu_script.py

import winsound
import tkinter as tk
from tkinter import ttk
import tkinter.simpledialog as simpledialog
from tkinter import messagebox
import customtkinter as ctk
import serial
import threading
import serial.tools.list_ports
import time
import datetime

# Configurando o tema da janela
ctk.set_appearance_mode("dark")  # Pode ser "light", "dark", ou "system" (baseado no SO)
ctk.set_default_color_theme("dark-blue")  # Pode ajustar o tema de cor também, blue, dark-blue, green

# Variável global para controlar a conexão serial
ser = None
is_connected = False
new_fonte = ("Courier New", 12)
list_variable = ["V0:", "V1:", "V2:", "V3:", "V4:", "V5:", "V6:", "V7:", "V8:", "V9:"]
list_name = ["", "", "", "", "", "", "", "", "", "", ]

# Função para listar portas COM ativas
def listar_portas():
    return [port.device for port in serial.tools.list_ports.comports()]

# Função para atualizar a combobox com as portas disponíveis
def atualizar_com_port_combo():
    com_port_combo.set('')  # Limpa o texto selecionado da combobox
    portas = listar_portas()
    com_port_combo.configure(values=portas)  # Atualiza os valores da combobox
    if portas:
        com_port_combo.set(portas[0])  # Seleciona a primeira porta, se houver
                    
# Função para leitura da porta serial
def read_serial():
    global is_connected
    while ser and ser.is_open:
        try:
            data = ser.readline().decode('utf-8').strip()
            if data:
                if checkbox_var.get() == 1:
                    update_listbox_debug(data)
                    update_break_point(data)
                else:
                    text_area.insert("end", data + '\n')
                    text_area.yview("end")  # Scroll automático para o fim
        except Exception as e:
            if e.args[0] == f"GetOverlappedResult failed (PermissionError(13, 'Acesso negado.', None, 5))":
                ser.close()
                is_connected = False
                connect_button.configure(text="Conectar")  # Muda o botão de volta para "Conectar"
                scan_button.configure(state='normal')  # Habilita o botão
                com_port_combo.configure(state='normal')  # Habilita o combo
                baudrate_combo.configure(state='normal')  # Habilita o combo
                conectar_serial() # Somente para atualizar variáveis
                atualizar_com_port_combo() # Atualizar portas ativas
                print(f"Porta desconectada...")
            print(f"Erro ao ler da porta serial: {e}")
            

# Função para enviar dados
def send_data():
    data = entry.get()
    if send_button.cget("fg_color") == "yellow":
        send_button.configure(text="Enviar", fg_color="#00008B")
        ser.write(data.encode('utf-8') + b'\n')
    else:
        try:
            if ser and ser.is_open:
                if endline_combo.get() == "None":
                    ser.write(data.encode('utf-8'))
                elif endline_combo.get() == "New Line":
                    ser.write(data.encode('utf-8') + b'\n')
                elif endline_combo.get() == "Carriage Return":
                    ser.write(data.encode('utf-8') + b'\r')
                elif endline_combo.get() == "Both NL and CR":
                    ser.write(data.encode('utf-8') + b'\n\r')
                entry.delete(0, "end")
        except Exception as e:
            print(f"Erro ao enviar dados: {e}")

# Função para conectar/desconectar à porta serial
def conectar_serial():
    global ser, is_connected

    if not is_connected:
        try:
            com_port = com_port_combo.get()
            baudrate = baudrate_combo.get()
            ser = serial.Serial(com_port, baudrate=int(baudrate), timeout=1)
            is_connected = True
            connect_button.configure(text="Desconectar")
            scan_button.configure(state='disabled')
            com_port_combo.configure(state='disabled')
            baudrate_combo.configure(state='disabled')
            text_area.delete("1.0", "end")
            if checkbox_var.get() == 1:
                for index in range(10):
                    list_variable[index] = f"V{index}:"
                    text_area.insert("end", list_variable[index] + '\n')
            
            # Iniciar a leitura da porta serial em uma thread separada
            thread = threading.Thread(target=read_serial)
            thread.daemon = True
            thread.start()

        except serial.SerialException as e:
            print(f"Erro ao conectar à porta serial: {e}")
    else:
        try:
            if ser:
                ser.close()
                is_connected = False
                connect_button.configure(text="Conectar")
                scan_button.configure(state='normal')
                com_port_combo.configure(state='normal')
                baudrate_combo.configure(state='normal')
                send_button.configure(text="Enviar", fg_color="#00008B")
        except Exception as e:
            print(f"Erro ao desconectar: {e}")

def on_checkbox_toggle():
    # DEBUG
    if checkbox_var.get() == 1:
        text_area.delete("1.0", "end")
        for index in range(10):
            text_area.insert("end", list_variable[index] + '\n')
    else:
        text_area.delete("1.0", "end")    

def clique(event):
    index = text_area.index("@%s,%s" % (event.x, event.y))  # Obtém o índice do caractere clicado
    linha = int(index.split('.')[0])  # Extrai o número da linha

    if linha <= 10:
        # Abre um inputbox como uma msgbox
        nome = simpledialog.askstring(f"V{linha-1}", "Digite o nome para sua variável:")

        # Verifica se o usuário digitou um valor
        if nome is not None:
            list_name[linha-1] = list_name[linha-1] + " " + nome # Atribui o nome à linha clicada
            text_area.delete("1.0", "end")
            for index in range(10):
                text_area.insert("end", list_variable[index] + '\n')

def update_listbox_debug(data):
    for index in range (9):
        if data.startswith(f"V{index}:"):
            list_variable[index] = data + " " + time.strftime("%H:%M:%S") + " " + list_name[index]
            text_area.delete("1.0", "end")
            for index in range(10):
                text_area.insert("end", list_variable[index] + '\n')

def update_break_point(data):
    # Verifica se a string começa com "B" e termina com ":"
    if data.startswith("B") and data.endswith(":"):
        # Pega o segundo caractere
        index = data[1]
        
        # Exibe o segundo caractere em uma msgbox
        root = tk.Tk()
        root.withdraw()  # Esconde a janela principal do tkinter
        send_button.configure(text=f"Break({index})", fg_color="yellow")
        #messagebox.showinfo("Break point", f"Break({index})")
        #ser.write(data.encode('utf-8') + b'\n') 
        beep(3)

def beep(beeps):
    # Frequência em Hertz (Hz) e duração em milissegundos (ms)
    frequency = 1000  # 1000 Hz
    duration = 100    # 100 ms
    for n in range(beeps):
        winsound.Beep(frequency, duration) # Gera um som
        time.sleep(0.1)  # em segundos
        
# Interface CustomTkinter
root = ctk.CTk()
root.title("Monitor Serial + Debug by DALÇÓQUIO AUTOMAÇÃO")
root.geometry("800x400")

# Frame para configurações
frame_config = ctk.CTkFrame(root, width=1000, height=50)
frame_config.grid(row=0, column=0, sticky="ew", padx=10, pady=10) # Usando grid 
frame_config.grid_propagate(False)

# Criação das checkbox
checkbox_var = ctk.IntVar(value=0)
checkbox = ctk.CTkCheckBox(frame_config, font=new_fonte, text="Debug", variable=checkbox_var, command=on_checkbox_toggle)
checkbox.pack(side=tk.LEFT, padx=0)

# ComboBox para portas COM
com_port_combo = ctk.CTkComboBox(frame_config, font=new_fonte, values=listar_portas(), width=150, state="readonly")
com_port_combo.pack(side=tk.LEFT, padx=0)

# Atualiza as portas COM no combo após criar a combobox
atualizar_com_port_combo()

# ComboBox para baudrate
baudrate_combo = ctk.CTkComboBox(frame_config, font=new_fonte, values=["1200", "2400", "4800", "9600",  "19200", "38400", "57600", "115200"], width=150, state="readonly")
baudrate_combo.pack(side=tk.LEFT, padx=10)
baudrate_combo.set("9600")  # Seleciona 9600 por padrão

# Botão para scanear portas
scan_button = ctk.CTkButton(frame_config, font=new_fonte, text="Scanear", command=atualizar_com_port_combo, width=170)
scan_button.pack(side=tk.LEFT, padx=0)

# Botão para conectar/desconectar
connect_button = ctk.CTkButton(frame_config, font=new_fonte, text="Conectar", command=conectar_serial, width=170)
connect_button.pack(side=tk.LEFT, padx=10)

# Frame para dados recebidos
frame_area = ctk.CTkFrame(root)
frame_area.grid(row=1, column=0, sticky="nsew", padx=0, pady=0) # Usando grid
root.columnconfigure(0, weight=1) # Faz a coluna se expandir para ocupar todo o espaço
root.rowconfigure(1, weight=1)    # Faz a linha se expandir para ocupar todo o espaço

# Área de texto para exibir dados recebidos
text_area = ctk.CTkTextbox(frame_area, font=new_fonte, width=1000, height=450)
text_area.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

# Função para exibir a tooltip
def show_tooltip(event):
    tooltip.place(x=event.x_root - root.winfo_rootx() + 20,
                  y=event.y_root - root.winfo_rooty() + 20)
    tooltip.lift()  # Garante que a tooltip fica em cima dos outros widgets

# Função para ocultar a tooltip
def hide_tooltip(event):
    tooltip.place_forget()

# Criando a tooltip (inicialmente invisível)
tooltip = ctk.CTkLabel(root, text="CTRL + A para selecionar, e DEL para deletar.")
tooltip.place_forget()

# Vinculando os eventos de mouse para mostrar e ocultar a tooltip
text_area.bind("<Enter>", show_tooltip)
text_area.bind("<Leave>", hide_tooltip)
text_area.bind("<Double-Button-1>", clique)

# Frame para entrada e envio de dados
frame_entry = ctk.CTkFrame(root, width=1000, height=50)
frame_entry.grid(row=2, column=0, sticky="nsew", padx=0, pady=10) # Usando grid

# Entrada de texto para enviar dados
entry = ctk.CTkEntry(frame_entry, font=new_fonte, width=430)
entry.pack(side=tk.LEFT, padx=10)

# Caracter para fim de linha
endline_combo = ctk.CTkComboBox(frame_entry, font=new_fonte, values=["None", "New Line", "Carriage Return", "Both NL and CR"], width=150, state="readonly")
endline_combo.pack(side=tk.LEFT, padx=0)
endline_combo.set("None")

# Botão para enviar dados
send_button = ctk.CTkButton(frame_entry, font=new_fonte, text="Enviar", command=send_data, width=170)
send_button.pack(side=tk.LEFT, padx=10)

# Enter para enviar dados
entry.bind('<Return>', lambda event: send_data())

root.mainloop()

# Fechar a porta serial ao encerrar o programa
if ser and ser.is_open:
    ser.close()
