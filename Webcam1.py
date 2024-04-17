# importar as Bibliotecas a usar---------------------------------------------------------------------
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk
#----------------------------------------------------------------------------------------------------
# Função para atualizar a imagem da webcam com brilho ajustado --------------------------------------
def update_webcam_with_brightness():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Ajustar o brilho
        brightness = SBrilho.get()
        frame = adjust_brightness(frame, brightness)
        
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        label_foto.imgtk = frame
        label_foto.configure(image=frame)
        label_foto.after(10, update_webcam_with_brightness)
#---------------------------------------------------------------------------------------------------
# Função para ajustar o brilho da imagem -----------------------------------------------------------
def adjust_brightness(frame, brightness):
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(hsv)
    
    # Aumentar o valor do canal V (brilho)
    v = cv2.add(v, brightness)
    
    # Garantir que os valores do canal V estejam no intervalo de 0 a 255
    v = np.clip(v, 0, 255)
    
    # Mesclar os canais novamente
    hsv = cv2.merge((h, s, v))
    
    # Converter de volta para RGB
    frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    return frame
#---------------------------------------------------------------------------------------------------
# Função para atualizar a imagem da webcam com aparência ajustada ----------------------------------
def update_webcam_with_appearance():
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Ajustar a aparência
        appearance = SAparencia.get()
        frame = adjust_appearance(frame, appearance)
        
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        label_foto.imgtk = frame
        label_foto.configure(image=frame)
        label_foto.after(10, update_webcam_with_appearance)
#--------------------------------------------------------------------------------------------------
# Função para ajustar a aparência da imagem -------------------------------------------------------
def adjust_appearance(frame, appearance):
    # Converter para HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    
    # Ajustar o brilho (canal V)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] + appearance, 0, 255)
    
    # Converter de volta para RGB
    frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    return frame
#--------------------------------------------------------------------------------------------------
# Função para capturar a imagem com brilho e aparência ajustados ----------------------------------
def capturar_imagem():
    global frame_retocado
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Ajustar o brilho
        brightness = SBrilho.get()
        frame = adjust_brightness(frame, brightness)
        
        # Ajustar a aparência
        appearance = SAparencia.get()
        frame = adjust_appearance(frame, appearance)
        
        # Ajustar o tamanho da imagem para corresponder ao tamanho do frame de cópia
        frame = cv2.resize(frame, (275, 290))
        
        # Exibir a imagem retocada na interface
        frame_retocado = frame
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)
        label_copia.imgtk = frame
        label_copia.configure(image=frame)
    else:
        print("Erro ao capturar imagem!")
#--------------------------------------------------------------------------------------------------
# Função para selecionar a webcam -----------------------------------------------------------------
def Selecionar(event):
    global cap
    if cmb_device.get() == 'Webcam':
        cap = cv2.VideoCapture(0)
        update_webcam_with_brightness()  # Agora atualiza com brilho ajustado
    else:
        cap.release()
#--------------------------------------------------------------------------------------------------
# Função para guardar a imagem capturada
def Guardar():
    global frame_retocado
    if frame_retocado is not None:
        # Abre o diálogo de salvamento de arquivo
        file_path = filedialog.asksaveasfilename(defaultextension=".bmp", filetypes=[("BMP files", "*.bmp"), ("All Files", "*.*")])
        if file_path:
            # Salva a imagem no formato especificado pelo usuário
            cv2.imwrite(file_path, cv2.cvtColor(frame_retocado, cv2.COLOR_RGB2BGR))
            messagebox.showinfo("Guardar", "Imagem salva com sucesso em: " + file_path)
    else:
        messagebox.showinfo("Erro", "Erro ao capturar imagem!")
#------------------------------------------------------------------------------------------------------
# Função para Limpar a cópia --------------------------------------------------------------------------
def Limpar():
    # Remove a imagem do label
    label_copia.imgtk = None
    label_copia.configure(image=None)
    
    # Redefinir o controle deslizante de aparência
    SAparencia.set(0)
    SBrilho.set(0)
    messagebox.showinfo('Limpeza','Sua Cópia Limpa com Sucesso !....')  
#-----------------------------------------------------------------------------------------------------
# Função para Sair -----------------------------------------------------------------------------------
def Sair():
    # Perguntar ao usuário se deseja sair
    resposta = messagebox.askyesno("Sair", "Deseja realmente sair? sim / nao")
    
    if resposta:  # Se o usuário escolher "Sim"
        Janela.destroy()  # Destruir a janela principal, encerrando o programa      
#-----------------------------------------------------------------------------------------------------
# Definir as cores a usar ----------------------------------------------------------------------------
co0 = '#FFFFFF'  # cor branco
co1 = '#F4F2F4'  # cor Cinza Botões
co2 = '#F6FFFF'  # cor Azul Claro Para O estido Combobox
#------------------------------------------------------------------------------------------------------
# Configurar a Nossa janela----------------------------------------------------------------------------
Janela = Tk()
Janela.geometry('618x490+100+100')
Janela.resizable(0, 0)
Janela.title('Menu Webcam 1.0.0.1 dev Joel 2024 PT ©')
Janela.configure(bg=co0)
#Janela.iconbitmap('C:\\Users\\HP\\Desktop\\Python tkinter\\Menu Webcam1\\icon1.ico')  # Adicione o caminho correto do ícone
#--------------------------------------------------------------------------------------------------------
# Criar um estilo ---------------------------------------------------------------------------------------
style = ttk.Style()
#--------------------------------------------------------------------------------------------------------
# Frame para a foto -------------------------------------------------------------------------------------
frame_foto = Frame(Janela, width=300, height=300, bg='white')
frame_foto.place(x=10, y=35)
#-------------------------------------------------------------------------------------------------------
# Frame para a cópia da foto ---------------------------------------------------------------------------
frame_copia = Frame(Janela, width=300, height=300, bg='white')
frame_copia.place(x=320, y=35)
#-------------------------------------------------------------------------------------------------------
# Criar combobox ---------------------------------------------------------------------------------------
cmb_device = ttk.Combobox(Janela, width=40, style='Custom.TCombobox')
cmb_device.place(x=10, y=5)
cmb_device.set('Selecione a sua Webcam')
cmb_device.bind("<<ComboboxSelected>>", Selecionar)
cmb_device['values'] = ['Webcam']
#--------------------------------------------------------------------------------------------------------
# Label para a foto--------------------------------------------------------------------------------------
label_foto = Label(frame_foto, bg='white')
label_foto.pack(fill=BOTH, expand=YES)
label_foto.configure(width=295, height=290)  # Redimensiona o Label
#--------------------------------------------------------------------------------------------------------
# Label para a cópia da foto ----------------------------------------------------------------------------
label_copia = Label(frame_copia, bg='white')
label_copia.pack(fill=BOTH, expand=YES)
label_copia.configure(width=275, height=290)  # Redimensiona o Label
#--------------------------------------------------------------------------------------------------------
# Criar os botões ---------------------------------------------------------------------------------------
BtnCapturar = Button(Janela, text='Capturar Imagem', font=('Arial 12'), relief=RAISED, overrelief=RIDGE, bg=co1,command=capturar_imagem)
BtnCapturar.place(x=10, y=340)
BtnGuardar = Button(Janela, text='Guardar Imagem', font=('Arial 12'), relief=RAISED, overrelief=RIDGE, bg=co1,command=Guardar)
BtnGuardar.place(x=150, y=340)
BtnLimpar = Button(Janela, text='Limpar Imagem', font=('Arial 12'), relief=RAISED, overrelief=RIDGE, bg=co1,command=Limpar)
BtnLimpar.place(x=310, y=340)
BtnSair = Button(Janela, text='Sair Aplicação', font=('Arial 12'), relief=RAISED, overrelief=RIDGE, bg=co1,command=Sair)
BtnSair.place(x=440, y=340)
#---------------------------------------------------------------------------------------------------------
# Criar um slider para Aumentar Brilho -------------------------------------------------------------------
SBrilho = Scale(Janela, orient=HORIZONTAL, bg=co0, length=595, from_=0, to=255)
SBrilho.place(x=10, y=385)
#---------------------------------------------------------------------------------------------------------
# Criar um slider para Ajustar Aparência -----------------------------------------------------------------
SAparencia = Scale(Janela, orient=HORIZONTAL, bg=co0, length=595, from_=0, to=255)
SAparencia.place(x=10, y=440)
#---------------------------------------------------------------------------------------------------------
# Iniciar a Nossa Janela ---------------------------------------------------------------------------------
Janela.mainloop()
#----------------------------------------------------------------------------------------------------------