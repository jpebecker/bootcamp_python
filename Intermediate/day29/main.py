from tkinter import *
from tkinter import messagebox
import os,random
FONT = ('Times New Roman', 12, 'bold')
#######################################################################FUNCTIONS
def save_values():
    adress = website_entrybox.get()
    user = user_entrybox.get()
    passw = pass_entrybox.get()

    if len(adress) == 0 or len(user) == 0 or len(passw) == 0:
        messagebox.showerror(title='Erro de Entrada',message='Dados Incompletos!')
        clear_all()
    else:
        confirmation = messagebox.askokcancel(title='Confirmação',message=f'Dados inseridos para {adress}:\n'
                                                 f'Usuário : {user}\n'
                                                 f'Senha : {passw}\n'
                                                 f'\nDeseja salvar?')

        if confirmation:
            messagebox.showinfo(title='Confirmação',message='Dados Salvos')
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            filepath = os.path.join(desktop_path, "passwords.txt")

            if os.path.isfile(filepath):  #se existir arquivo salvo na desktop
                with open(filepath, mode='a') as newFile:
                    newFile.write(f'\n>>> {adress} | {user} | {passw}')
                    clear_all()
            else:  #se nao existir arquivo salvo na desktop
                with open(filepath, mode='w') as newFile:
                    newFile.write(f'Plataforma | Login | Senha\n')
                    newFile.write('---------------------------')
                    newFile.write(f'\n>>> {adress} | {user} | {passw}')
                    clear_all()
        else:
            clear_all()

def clear_all():
    website_entrybox.delete(0,END)
    website_entrybox.focus()
    user_entrybox.delete(0,END)
    user_entrybox.insert(END,'@gmail.com')
    pass_entrybox.delete(0,END)

def create_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '*', '+']

    letters_pass = [random.choice(letters) for _ in range(random.randint(8, 10))]
    symbols_pass = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    num_pass = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = letters_pass + symbols_pass + num_pass
    random.shuffle(password_list)
    password = "".join(password_list)
    pass_entrybox.delete(0,END)
    pass_entrybox.insert(END,password)
#############################################################################USER INTERFACE
tela = Tk()
tela.config(padx=50, pady=50)
tela.title('Password Saver - KeyLogger')
canvas = Canvas(width=200, height=200, highlightthickness=0)
canvas.grid(column=1, row=0)
img = PhotoImage(file='icon.png')
canvas.create_image(100, 100, image=img)

website_text = Label(text='Website/Platform:', font=FONT)
website_text.grid(column=0, row=1)
website_entrybox = Entry(width=40)
website_entrybox.focus()
website_entrybox.grid(column=1, row=1, columnspan=2, sticky='w')

user_text = Label(text='Username/E-mail:', font=FONT)
user_text.grid(column=0, row=2)
user_entrybox = Entry(width=40)
user_entrybox.insert(END,'@gmail.com')
user_entrybox.grid(column=1, row=2, columnspan=2, sticky='w')

passw_text = Label(text='Password:', font=FONT)
passw_text.grid(column=0, row=3)

# Frame alinhado
pass_frame = Frame(tela)
pass_frame.grid(column=1, row=3, sticky='w')

pass_entrybox = Entry(pass_frame, width=21)
pass_entrybox.grid(column=0, row=0)

generatepassword_btn = Button(pass_frame, text='Generate Password',command=create_password)
generatepassword_btn.grid(column=1, row=0, padx=5)

add_tolist_btn = Button(text='Add to Local Desktop', width=34,command=save_values)
add_tolist_btn.grid(column=1, row=4, columnspan=2, sticky='w')
tela.mainloop()
