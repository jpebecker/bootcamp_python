import tkinter as tk
from tkinter import filedialog, messagebox
from convert import convertio  # Supondo que a função de conversão esteja em converter.py
# Variáveis globais para guardar os caminhos
selected_pdf_path = None
selected_output_directory = None
audio_file = None  # Caminho do arquivo de áudio final


def choose_pdf_file():
    global selected_pdf_path
    selected_pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if selected_pdf_path:
        pdf_label.config(text=f"Arquivo selecionado: {selected_pdf_path}")
        if selected_output_directory:
            convert_button.config(state=tk.NORMAL)  # Habilita conversão só se ambos forem escolhidos



def choose_output_directory():
    global selected_output_directory
    selected_output_directory = filedialog.askdirectory()
    if selected_output_directory:
        output_label.config(text=f"Diretório de saída: {selected_output_directory}")
        if selected_pdf_path:
            convert_button.config(state=tk.NORMAL)  # Habilita conversão só se ambos forem escolhidos

def start_conversion(pdf_path, output_directory, lang='pt'):
    if not pdf_path or not output_directory:
        messagebox.showerror("Erro", "Você precisa selecionar o arquivo PDF e o diretório de saída!")
        return False

    try:
        status_label.config(text="Conversão em andamento...", fg="blue")
        tela.update_idletasks()

        print("Chamando convertio...")
        # Tenta converter
        audio_path = convertio(pdf_path, lang=lang, output_directory=output_directory)
        print("convertio retornou:", audio_path)
        if audio_path:
            status_label.config(text="Conversão concluída com sucesso!", fg="green")
            messagebox.showinfo("Sucesso", f"Áudio salvo em: {audio_path}")
        else:
            raise ValueError("Falha ao converter o PDF para áudio.")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao converter PDF: {str(e)}")
        status_label.config(text="Erro na conversão.", fg="red")
        audio_path = False

    return bool(audio_path)

def choose_output_path():
    # Abrir a janela para escolher o local e nome do arquivo MP3
    file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
    if file_path:
        return file_path
    return None

def reset_interface():
    # Limpar variáveis e restaurar estado inicial
    pdf_label.config(text="Selecione um arquivo PDF para conversão")
    output_label.config(text="Salvar Áudio em:")
    convert_button.config(state=tk.DISABLED)


# Configuração do Tkinter
tela = tk.Tk()
tela.title("Conversão de PDF para Áudio")
selected_lang = tk.StringVar(value='pt')  # padrão: português
# Título
title_label = tk.Label(tela, text="Conversão de PDF para Áudio", font=("Arial", 18))
title_label.pack(pady=20)

# Label para exibir o diretório do arquivo PDF selecionado
pdf_label = tk.Label(tela, text="Selecione um diretório com o arquivo PDF para conversão", font=("Arial", 12))
pdf_label.pack(pady=10)

# Botão para selecionar o diretório PDF
select_pdf_button = tk.Button(tela, text="Selecionar Diretório PDF", command=lambda: choose_pdf_file(),
                              font=("Arial", 12))
select_pdf_button.pack(pady=5)

lang_label = tk.Label(tela, text="Idioma do áudio:", font=("Arial", 12))
lang_label.pack(pady=5)

lang_menu = tk.OptionMenu(tela, selected_lang, "pt", "en")
lang_menu.config(font=("Arial", 12), width=10)
lang_menu.pack(pady=5)

# Label para exibir o diretório de saída
output_label = tk.Label(tela, text="Selecione um diretório de saída para o áudio", font=("Arial", 12))
output_label.pack(pady=10)

# Botão para selecionar o diretório de saída
select_output_button = tk.Button(tela, text="Selecionar Diretório de Saída", command=lambda: choose_output_directory(),
                                 font=("Arial", 12))
select_output_button.pack(pady=5)

# Botão para começar a conversão
convert_button = tk.Button(tela, text="Iniciar Conversão", font=("Arial", 12), state=tk.DISABLED,
                            command=lambda: start_conversion(selected_pdf_path, selected_output_directory, selected_lang.get()))

convert_button.pack(pady=10)

# Label de status para feedback
status_label = tk.Label(tela, text="", font=("Arial", 12))
status_label.pack(pady=10)


tela.mainloop()
