import pyttsx3 #bib to convert text into audio
from PyPDF2 import PdfReader #bib to convert pdf to text str
import os
def convertio(pdf_path, lang='pt', output_directory=None):
    try:
        ###############################OPEN PDF AND CONVERT IT
        reader = PdfReader(pdf_path)
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

        if not full_text.strip():
            raise ValueError("Nenhum texto encontrado no PDF.")

        #DEFAULT DESTINATION OF THE AUDIO IS THE CODE DIRECTORY
        if not output_directory:
            output_directory = os.getcwd()

        #audio archive config (name)
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        audio_filename = f"{pdf_name}_audio.mp3"
        output_path = os.path.join(output_directory, audio_filename)

        #init
        engine = pyttsx3.init()

        #config
        voices = engine.getProperty('voices')
        if lang == 'pt':
            engine.setProperty('voice', voices[0].id)
        elif lang == 'en':
            engine.setProperty('voice', voices[1].id)

        #save
        engine.save_to_file(full_text, output_path)
        engine.runAndWait()

        print(output_path)
        print('CONVERTED')
        return output_path  #return path

    except Exception as e:
        print(f"[Erro em convertio] {e}")
        return None