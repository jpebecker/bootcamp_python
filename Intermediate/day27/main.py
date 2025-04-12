from tkinter import *

def convert_miles():
    miles = miles_input.get()
    return result_label.config(text=float(miles) * 1.609)
    pass
tela = Tk()
tela.title('Milhas para Quilômetros')
tela.config(padx=10,pady=10) #borda de delimitacao entre componentes
#tela.minsize(width=200,height=100)

miles_input = Entry(width=10)
miles_input.grid(column=1,row=0)

miles_txt = Label(text='Milhas')
miles_txt.grid(column=2,row=0)

is_equal = Label(text='É igual a:')
is_equal.grid(column=0,row=1)

result_label = Label(text='0',font=('Arial',10,'bold'))
result_label.grid(column=1,row=1)

kilo_label = Label(text='km')
kilo_label.grid(column=2,row=1)

calculate_btn = Button(text='Calcular',command=convert_miles)
calculate_btn.grid(column=1,row=2)
tela.mainloop()