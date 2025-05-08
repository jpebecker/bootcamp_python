import pyttsx3
from PyPDF2 import PdfReader
import os

def convertio(pdf_path, lang='pt', output_directory=None):
    try:
        # Abrir o PDF e extrair texto
        reader = PdfReader(pdf_path)
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

        if not full_text.strip():
            raise ValueError("Nenhum texto encontrado no PDF.")

        # Diretório de saída padrão
        if not output_directory:
            output_directory = os.getcwd()

        # Nome base do arquivo de áudio
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        audio_filename = f"{pdf_name}_audio.mp3"
        output_path = os.path.join(output_directory, audio_filename)

        # Inicializa o engine do pyttsx3
        engine = pyttsx3.init()

        # Configura a voz e o idioma (pode precisar ajustar a voz dependendo do sistema)
        voices = engine.getProperty('voices')
        if lang == 'pt':
            engine.setProperty('voice', voices[0].id)  # Por exemplo, pode ser a voz masculina em português
        elif lang == 'en':
            engine.setProperty('voice', voices[1].id)  # Supondo que a voz feminina em inglês esteja em voices[1]

        # Salva o áudio gerado
        engine.save_to_file(full_text, output_path)
        engine.runAndWait()

        print(output_path)
        print('CONVERTED')
        return output_path  # Retorna o caminho do áudio gerado

    except Exception as e:
        print(f"[Erro em convertio] {e}")
        return None