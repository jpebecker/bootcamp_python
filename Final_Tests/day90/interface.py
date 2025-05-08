import tkinter as tk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Vanish Text App")

        #top label
        self.label = tk.Label(root, text="Digite algo ou tudo desaparecerá...", font=("Arial", 12))
        self.label.pack(pady=(20, 0))

        #text entry
        self.text_widget = tk.Text(root, height=15, width=50, font=("Arial", 14))
        self.text_widget.pack(padx=20, pady=20)

        self.text_widget.bind("<KeyPress>", self.reset_timer)

        self.inactivity_delay = 5000  # milissegundos de inatividade
        self.delete_interval = 300    # milissegundos entre apagar caracteres

        self.inactivity_job = None
        self.deletion_job = None
        self.deleting = False

    def reset_timer(self, event=None):
        if self.deletion_job:
            self.root.after_cancel(self.deletion_job)
            self.deletion_job = None
            self.deleting = False

        if self.inactivity_job:
            self.root.after_cancel(self.inactivity_job)

        self.inactivity_job = self.root.after(self.inactivity_delay, self.start_deletion)

    def start_deletion(self):
        self.deleting = True
        self.delete_one_char()

    def delete_one_char(self):
        if not self.deleting:
            return

        #counter da remocao de linha
        content = self.text_widget.get("1.0", "end-1c")

        if len(content.strip()) > 0:
            new_content = content[1:]  # remove o primeiro caractere

            self.text_widget.delete("1.0", tk.END)
            self.text_widget.insert("1.0", new_content)

            #cursor ao final da linha
            self.text_widget.mark_set(tk.INSERT, tk.END)
            self.text_widget.see(tk.INSERT)

            self.deletion_job = self.root.after(self.delete_interval, self.delete_one_char)
        else:
            self.deleting = False
            self.deletion_job = None
