from tkinter import Button, Label, Frame, Entry
from tkinter import filedialog as F_dial, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os, math

class WatermarkApp:
    def __init__(self, window):
        self.tela = window
        self.tela.title("Watermark - Marca d'Água")
        self.tela.geometry("500x600")

        #label com o nome da imagem/arquivo
        self.img_name_text_label = Label(self.tela, text="", font=("Arial", 10, "italic"))
        self.img_name_text_label.pack(pady=(10, 0))

        #label da imagem
        self.img_label = Label(self.tela)
        self.img_label.pack(pady=(0, 10))

        Label(self.tela, text="Bem-vindo ao Personal Watermarker").pack()
        Button(self.tela, text="Selecionar Imagem", command=self.select_img).pack(pady=10)

        #botoes principais
        self.button_frame = Frame(self.tela)
        self.button_frame.pack(pady=10)
        Button(self.button_frame, text="Adicionar Texto", command=self.show_text_entry).grid(row=0, column=0, padx=10)
        Button(self.button_frame, text="Adicionar Imagem (PNG)", command=self.add_image).grid(row=0, column=1, padx=10)
        Button(self.button_frame, text="Salvar Imagem", command=self.save_image).grid(row=0, column=2, padx=10)

        #vars de controle usadas depois
        self.img_path = None
        self.img_tk   = None
        self.text_entry       = None
        self.apply_text_button = None
        self.final_image = None

    def select_img(self):
        path = F_dial.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Image files", "*.jpg *.jpeg *.png")]
        )
        if not path:
            messagebox.showerror("Erro", "Nenhuma imagem foi selecionada.")
            return

        try:
            img = Image.open(path)
            img.thumbnail((400, 300))
            self.img_tk = ImageTk.PhotoImage(img)

            self.img_name_text_label.config(text=f"name: {os.path.basename(path)}")
            self.img_label.config(image=self.img_tk)
            self.img_path = path
        except Exception as e:
            messagebox.showerror("Erro ao Carregar", str(e))

    def show_text_entry(self):
        if not self.text_entry:
            self.text_entry = Entry(self.tela, width=30)
            self.text_entry.insert(0, "Digite a marca d'água")
            self.text_entry.bind("<FocusIn>", lambda e: self.text_entry.delete(0, 'end'))
            self.text_entry.pack(pady=5)

            self.apply_text_button = Button(self.tela, text="Aplicar Texto", command=self.add_text)
            self.apply_text_button.pack(pady=10)
        else:
            self.text_entry.pack(pady=5)
            self.apply_text_button.pack(pady=10)

    def add_text(self):
        if not self.img_path:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return

        try:
            text = self.text_entry.get().strip() or "Marca d'Água"
            base = Image.open(self.img_path).convert("RGBA")
            bw, bh = base.size

            #comprimento da diagonal
            diagonal = int(math.hypot(bw, bh))

            # camada quadrada do tamanho da diagonal mais bordas
            txt_layer = Image.new("RGBA", (diagonal+10, diagonal+10), (0, 0, 0, 0))
            draw = ImageDraw.Draw(txt_layer)

            #tamanho de fonte aproximado
            font_size = max(20, diagonal // max(len(text), 1))
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()

            #mede o texto
            x0, y0, x1, y1 = draw.textbbox((0, 0), text, font=font)
            tw, th = x1 - x0, y1 - y0

            #centraliza na camada
            pos = ((diagonal - tw) // 2, (diagonal - th) // 2)
            draw.text(pos, text, font=font, fill=(255, 255, 255, 128))

            #rotaciona somente o texto
            rotated = txt_layer.rotate(45, expand=True)

            #cola o texto rotacionado sobre a base/imagem
            rx, ry = rotated.size
            offset = ((bw - rx) // 2, (bh - ry) // 2)
            base.paste(rotated, offset, rotated)

            #converte e redimensiona para exibição
            final = base.convert("RGB")
            self.final_image = final.copy()
            final.thumbnail((400, 300))

            self.img_tk = ImageTk.PhotoImage(final)
            self.img_label.config(image=self.img_tk)

            messagebox.showinfo("Sucesso", "Marca d'água adicionada com sucesso!")
            self.text_entry.delete(0, 'end')
            self.text_entry.pack_forget()
            self.apply_text_button.pack_forget()
        except Exception as e:
            messagebox.showerror("Erro", f"{e}")

    def add_image(self):
        if not self.img_path:
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro.")
            return

        wm_path = F_dial.askopenfilename(
            title="Selecione o PNG da marca d'água",
            filetypes=[("PNG files", "*.png")]
        )
        if not wm_path:
            return  #operacao cancelada pelo user

        try:
            #abre imagem base e converte para RGBA
            base = Image.open(self.img_path).convert("RGBA")
            bw, bh = base.size

            #abre marca d'água (PNG) em RGBA
            wm = Image.open(wm_path).convert("RGBA")

            #Redimensiona a Watermark para 40% da largura da base
            scale = 0.4 #scale da imagem
            new_w = int(bw * scale)
            wm_ratio = wm.height / wm.width
            wm = wm.resize((new_w, int(new_w * wm_ratio)), Image.Resampling.LANCZOS)
            ww, wh = wm.size

            #Reduz a opacidade 60%
            alpha = wm.split()[3]
            alpha = alpha.point(lambda p: p * 0.6)#opacidade alpha
            wm.putalpha(alpha)

            #posição centralizada
            offset = ((bw - ww) // 2, (bh - wh) // 2)

            #cola a WaterMark sobre a base usando o canal alfa como máscara
            base.paste(wm, offset, wm)

            #converte de volta para RGB, redimensiona para preview e atualiza
            final = base.convert("RGB")
            self.final_image = final.copy()
            final.thumbnail((400, 300))
            self.img_tk = ImageTk.PhotoImage(final)
            self.img_label.config(image=self.img_tk)

            messagebox.showinfo("Sucesso", "Marca d'água em PNG adicionada com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    def save_image(self):
        if not hasattr(self, 'final_image'):
            messagebox.showwarning("Aviso", "Não há imagem para salvar.")
            return

        #caminho pra salvar
        save_path = F_dial.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg")],
            title="Salvar imagem com marca d'água"
        )
        if not save_path:
            return  # cancelou

        try:
            # salva usando o PIL.Image armazenado
            self.final_image.save(save_path)
            messagebox.showinfo("Salvo", f"Imagem salva em:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Erro ao Salvar", str(e))