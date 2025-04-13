from tkinter import *
from tkinter import messagebox
import random,json,os
FONT = ('Times New Roman', 12, 'bold')
################################################# Caminho para desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
file_path = os.path.join(desktop_path, "passwords.json")
#######################################################################FUNCTIONS
def save_values():
    adress = website_entrybox.get().lower()
    user = user_entrybox.get()
    passw = pass_entrybox.get()

    new_data = {adress: {
                'username' : user,
                'password' : passw,
        }
    }

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

            try: #tenta abrir o arquivo
                with open(file_path, "r") as data_file:
                    data = json.load(data_file)
                    data.update(new_data)
                    with open(file_path, "w") as data_fileA:
                        json.dump(data, data_fileA, indent=4)
            except FileNotFoundError: #se nao encontrar
                with open(file_path,"w") as newFile:############escreve um novo arquivo
                    json.dump(new_data,newFile,indent=4)
            finally:
                clear_all()
        else:
            clear_all()

def load_values():
    try:  # tenta abrir o arquivo
        with open(file_path, "r") as data_file:
            data = json.load(data_file)
            if website_entrybox.get().lower() in data.keys():
                messagebox.showinfo(title='Retorno de Consulta',message=f'Dados Recuperados:\n'
                                                                        f'Plataforma: {website_entrybox.get()}\n'
                                                                        f'Login: {data[website_entrybox.get()]['username']}\n'
                                                                        f'Senha: {data[website_entrybox.get()]['password']}\n')
            else:
                messagebox.showwarning(title='Erro de Consulta', message='Registro não encontrado no arquivo')
    except FileNotFoundError:  # se nao encontrar
        messagebox.showwarning(title='Erro de Consulta',message='Arquivo não encontrado na Desktop')
    finally:
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
###################################################################
website_text = Label(text='Website/Platform:', font=FONT)
website_text.grid(column=0, row=1)

website_frame = Frame(tela)
website_frame.grid(column=1, row=1, sticky='w')

website_entrybox = Entry(website_frame,width=25)
website_entrybox.focus()
website_entrybox.grid(column=1, row=1,padx=2)
website_seachbtn = Button(website_frame,text='Search',width=10,padx=5,command=load_values)
website_seachbtn.grid(column=2,row=1,sticky='w')
#######################################################################
user_text = Label(text='Username/E-mail:', font=FONT)
user_text.grid(column=0, row=2)
user_entrybox = Entry(width=40)
user_entrybox.insert(END,'@gmail.com')
user_entrybox.grid(column=1, row=2, columnspan=2, sticky='w')
#########################################################################
passw_text = Label(text='Password:', font=FONT)
passw_text.grid(column=0, row=3,sticky='w')

pass_frame = Frame(tela)
pass_frame.grid(column=1, row=3, sticky='w')

pass_entrybox = Entry(pass_frame, width=22)
pass_entrybox.grid(column=0, row=0)

generatepassword_btn = Button(pass_frame, text='Generate Password',command=create_password)
generatepassword_btn.grid(column=1, row=0, padx=1)

add_tolist_btn = Button(text='Add to Local Desktop', width=34,command=save_values)
add_tolist_btn.grid(column=1, row=4, columnspan=2, sticky='w',pady=5)
#####################################################################################################
tela.mainloop()
