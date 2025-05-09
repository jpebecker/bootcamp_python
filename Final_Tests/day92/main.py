import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from colorthief import ColorThief
import os,threading

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def process_image(file_path):
    #loading status
    status_label.config(text="Carregando imagem...")
    tela.update_idletasks()

    #update filename
    filename = os.path.basename(file_path)
    file_label.config(text=filename)

    #load image to app
    img = Image.open(file_path)
    img.thumbnail((300, 300))
    tk_img = ImageTk.PhotoImage(img)
    image_label.config(image=tk_img)
    image_label.image = tk_img

    #update status
    status_label.config(text="Extraindo paleta de cores...")
    tela.update_idletasks()

    #extract palette
    color_thief = ColorThief(file_path)
    palette = color_thief.get_palette(color_count=6, quality=5)

    #clean colors saved
    for widget in color_frame.winfo_children():
        widget.destroy()

    #colors grid
    cols = 3
    for i, color in enumerate(palette):
        hex_color = rgb_to_hex(color)

        cell = tk.Frame(color_frame, bg="#f0f0f0", padx=10, pady=10)
        cell.grid(row=i//cols, column=i%cols, padx=5, pady=5)

        color_box = tk.Frame(cell, bg=hex_color, width=40, height=40)
        color_box.pack()

        hex_entry = tk.Entry(cell, width=10, font=('Arial', 10), justify='center')
        hex_entry.insert(0, hex_color)
        hex_entry.configure(state='readonly')
        hex_entry.pack(pady=5)

    #update interface
    tela.update_idletasks()

    #update status
    status_label.config(text="Paleta extraída com sucesso!")

def open_image():
    #get image from user pc
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    if not file_path:
        return

    #new thread process (did that way so the app wont get inactive)
    threading.Thread(target=process_image, args=(file_path,), daemon=True).start()

#interface
tela = tk.Tk()
tela.title("Extract Pallete App")
tela.minsize(400, 550)
tela.configure(bg="#f0f0f0")

#open image btn
btn = tk.Button(tela, text="Selecionar Imagem", command=open_image)
btn.pack(pady=10)

#app status label
status_label = tk.Label(tela, text="", bg="#f0f0f0", fg="gray", font=('Arial', 10))
status_label.pack()

#file name label
file_label = tk.Label(tela, text="Nenhum arquivo selecionado", bg="#f0f0f0")
file_label.pack()

#image
image_label = tk.Label(tela)
image_label.pack(pady=10)

#palettes area
color_frame = tk.Frame(tela, bg="#f0f0f0")
color_frame.pack(pady=20)

tela.mainloop()