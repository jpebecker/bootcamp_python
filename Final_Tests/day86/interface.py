import tkinter as tk
from tkinter import ttk
import json,random,time

# ======== utils ========
def load_phrases(language):
    file = f"data/{language}_phrases.json"
    with open(file, "r", encoding="utf-8") as f:
        frases = json.load(f)
    return list(frases.values())

def choose_phrase(phrase_list):
    return random.choice(phrase_list)

#======== app class ========
class Interface:
    def __init__(self, tela):
        self.window = tela
        self.window.title("Type Tester")
        self.window.geometry("800x400")
        self.window.resizable(False, False)

        self.idioma = tk.StringVar(value="pt")
        self.frases = []
        self.actual_frase = ""
        self.inicio = None
        self.tempo_total = 60  # segundos
        self.cpm = tk.StringVar(value="CPM: 0")
        self.remaining_time = tk.StringVar(value="Tempo: 60s")
        self.total_matches = 0  # Para contar os caracteres corretos durante o tempo
        self.show_widgts()

    def show_widgts(self):
        #dropdown do idioma
        frame_top = tk.Frame(self.window)
        frame_top.pack(pady=10)
        ttk.Label(frame_top, text="Idioma:").pack(side=tk.LEFT, padx=5)
        ttk.OptionMenu(frame_top, self.idioma, "pt", "pt", "en").pack(side=tk.LEFT)

        #botao de iniciar
        ttk.Button(frame_top, text="Iniciar", command=self.start_time).pack(side=tk.LEFT, padx=10)

        # frase exibida (com destaque colorido)
        self.text_frase = tk.Text(self.window, width=80, height=4, font=("Courier", 14), wrap="word", bd=0)
        self.text_frase.pack(pady=20)
        self.text_frase.config(state="disabled")
        self.text_frase.tag_configure("correct", foreground="green", background="#d4fcd4")  # verde claro
        self.text_frase.tag_configure("incorrect", foreground="red", background="#ffd6d6")  # vermelho claro

        #entry da digitacao
        self.entry_texto = tk.Entry(self.window, font=("Courier", 14), width=60)
        self.entry_texto.pack(pady=10)
        self.entry_texto.bind("<KeyRelease>", self._check_char)

        #info de tempo e LPM
        info_frame = tk.Frame(self.window)
        info_frame.pack(pady=10)
        tk.Label(info_frame, textvariable=self.remaining_time, font=("Arial", 12)).pack(side=tk.LEFT, padx=20)
        tk.Label(info_frame, textvariable=self.cpm, font=("Arial", 12)).pack(side=tk.LEFT)

    def start_time(self):
        #config para o início do teste
        if not self.inicio:
            self.frases = load_phrases(self.idioma.get())
            self.actual_frase = choose_phrase(self.frases)
            self.text_frase.config(state="normal")
            self.text_frase.delete("1.0", tk.END)
            self.text_frase.insert("1.0", self.actual_frase)
            self.text_frase.config(state="disabled")
            self.entry_texto.delete(0, tk.END)
            self.entry_texto.focus()
            self.inicio = time.time()
            self.total_matches = 0  # Resetando a contagem de caracteres corretos
            self._update_timer()

    def _check_char(self, event=None):
        texto = self.entry_texto.get()
        frase = self.actual_frase

        if not self.inicio and texto:
            self.inicio = time.time()

        #atualiza o texto com as cores
        self.text_frase.config(state="normal")
        self.text_frase.delete("1.0", tk.END)
        for i, char in enumerate(frase):
            if i < len(texto):
                if texto[i] == char:
                    self.text_frase.insert(tk.END, char, "correct")
                    self.total_matches += 1  #acertos
                else:
                    self.text_frase.insert(tk.END, char, "incorrect")
            else:
                self.text_frase.insert(tk.END, char)
        self.text_frase.config(state="disabled")

        #Calculo da CPM
        tempo = max(time.time() - self.inicio, 1)  # não divida por zero
        cpm = int((self.total_matches / tempo))  # Caracteres por minuto (acertados / tempo decorrido)
        self.cpm.set(f"CPM: {cpm}")

        # Caso a frase esteja correta, troca para nova
        if texto == frase:
            self.actual_frase = choose_phrase(self.frases)
            self.text_frase.config(state="normal")
            self.text_frase.delete("1.0", tk.END)
            self.text_frase.insert("1.0", self.actual_frase)
            self.text_frase.config(state="disabled")

            self.entry_texto.delete(0, tk.END)

    def _update_timer(self):
        if not self.inicio:
            return

        remaining = int(self.tempo_total - (time.time() - self.inicio))
        if remaining <= 0:
            self.remaining_time.set("Tempo: 0s")
            self.entry_texto.config(state=tk.DISABLED)

            #Mensagem final
            final_cpm = self.cpm.get()
            self.label_resultado = tk.Label(self.window, text=f"Tempo esgotado!\n{final_cpm}",
                                            font=("Arial", 16, "bold"), fg="orange")
            self.label_resultado.pack(pady=15)

            #botao de reiniciar
            self.btn_restart = ttk.Button(self.window, text="Reiniciar", command=self._restart)
            self.btn_restart.pack()
        else:
            #tempo restante
            self.remaining_time.set(f"Tempo: {remaining}s")
            self.window.after(1000, self._update_timer)

    def _restart(self):
        if hasattr(self, 'label_resultado'):
            self.label_resultado.destroy()
        if hasattr(self, 'btn_restart'):
            self.btn_restart.destroy()

        self.entry_texto.config(state=tk.NORMAL)
        self.cpm.set("CPM: 0")
        self.remaining_time.set("Tempo: 60s")
        self.inicio = None  # tempo base
        self.total_matches = 0  # acertos acumulados
        self.start_time()