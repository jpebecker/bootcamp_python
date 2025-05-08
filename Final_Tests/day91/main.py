import tkinter as tk
from tkinter import filedialog, messagebox
from convert import convertio


selected_pdf_path = None
selected_output_directory = None
audio_file = None

########################################PROGRAM MAIN FUNCTIONS
def choose_pdf():
    global selected_pdf_path
    selected_pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if selected_pdf_path:
        pdf_label.config(text=f"Arquivo selecionado: {selected_pdf_path}")
        if selected_output_directory:
            convert_btn.config(state=tk.NORMAL)  #both have to be selected

def choose_destination():
    global selected_output_directory
    selected_output_directory = filedialog.askdirectory()
    if selected_output_directory:
        output_label.config(text=f"Diretório de saída: {selected_output_directory}")
        if selected_pdf_path:
            convert_btn.config(state=tk.NORMAL)  #both have to be selected

def run_conversion(pdf_path, output_directory, lang='pt'):

    if not pdf_path or not output_directory:
        messagebox.showerror("Erro", "Você precisa selecionar o arquivo PDF e o diretório de saída!")
        return False

    try:
        status_label.config(text="Conversão em andamento...", fg="blue")
        tela.update_idletasks()

        print("Initializing convertio...")
        audio_path = convertio(pdf_path, lang=lang, output_directory=output_directory)
        print("convertio returned:", audio_path)
        if audio_path:
            status_label.config(text="Conversão concluída com sucesso!", fg="green")
            messagebox.showinfo("Sucesso", f"Áudio salvo em: {audio_path}")
            reset_interface()
        else:
            raise ValueError("Falha ao converter o PDF para áudio.")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao converter PDF: {str(e)}")
        status_label.config(text="Erro na conversão.", fg="red")
        audio_path = False

    return bool(audio_path)

# def choose_output_path():
#     # Abrir a janela para escolher o local e nome do arquivo MP3
#     file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
#     if file_path:
#         return file_path
#     return None

#reset UI
def reset_interface():
    pdf_label.config(text="Selecione um arquivo PDF para conversão")
    output_label.config(text="Salvar Áudio em:")
    convert_btn.config(state=tk.DISABLED)
    status_label.forget()

#####################################################UI Tkinter
tela = tk.Tk()
tela.title("PDF to Audio Converter")
selected_lang = tk.StringVar(value='pt')#idiom variable

#main title
title_label = tk.Label(tela, text="Conversão de PDF para Áudio", font=("Arial", 20,'bold'))
title_label.pack(pady=20)

#pdf label
pdf_label = tk.Label(tela, text="Selecione o caminho do arquivo PDF para conversão", font=("Arial", 12,'bold'))
pdf_label.pack(pady=10)

#pdf btn
select_pdf_btn = tk.Button(tela, text="Selecionar Arquivo PDF", command=lambda: choose_pdf(),
                           font=("Arial", 12))
select_pdf_btn.pack(pady=5)

#language label
lang_label = tk.Label(tela, text="Idioma do arquivo > áudio:", font=("Arial", 12))
lang_label.pack(pady=5)
#language menu
lang_menu = tk.OptionMenu(tela, selected_lang, "pt", "en")
lang_menu.config(font=("Arial",14,'bold'), width=20)
lang_menu.pack(pady=5)

#destination label
output_label = tk.Label(tela, text="Selecione um diretório de saída para o áudio", font=("Arial", 12))
output_label.pack(pady=10)

#destionation btn
select_output_btn = tk.Button(tela, text="Selecionar Diretório de Saída", command=lambda: choose_destination(),
                              font=("Arial", 12))
select_output_btn.pack(pady=5)

#start convertio btn
convert_btn = tk.Button(tela, text="Iniciar Conversão", font=("Arial", 12), state=tk.DISABLED,
                        command=lambda: run_conversion(selected_pdf_path, selected_output_directory, selected_lang.get()))

convert_btn.pack(pady=10)

#status label
status_label = tk.Label(tela, text="", font=("Arial", 12))
status_label.pack(pady=10)

tela.mainloop() #keep runing