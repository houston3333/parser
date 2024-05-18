from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from comment_app_for_dict import comment
from parser_for_dict import parser


def click_comment_btn():
    hotels_num = comment()
    answer = mb.showinfo(title='Отчёт по вопросам',
                         message=f"Было отправлено: {hotels_num}")



def click_parser_btn():
    sum_hotels, count = parser()
    answer = mb.showinfo(title='Отчёт по парсингу',
                         message=f"Спарсено: {sum_hotels} \nДобавлено в базу данных: {count}")


root = Tk()
root.configure(background='#003da6')
root.title("P&Q with UTEMPLA")
root.geometry("340x200")

style = ttk.Style()
style.configure('TButton', font =
               ('Futura Book BT', 14, 'bold'),
                foreground = '#003da6'
                # background = '#A2F400'
                )

label = ttk.Label(root, text="UTEMPLA", font=("Futura Book BT", 60), foreground="#ffffff", background='#003da6')
label.grid(column=0, row=0, columnspan=2, sticky='EWNS') 


parser_btn = ttk.Button(root, text="Parsing", style = 'TButton', command=click_parser_btn)
parser_btn.grid(column=0, row=1, columnspan=1, rowspan=1, sticky='EWNS')

comment_btn = ttk.Button(root, text="Send Questions", style = 'TButton', command=click_comment_btn)
comment_btn.grid(column=1, row=1, columnspan=1, rowspan=1, sticky='EWNS')


desc = ttk.Label(root, text="Description: This program is designed for parsing \nand automatically sending questions to hotels. \nAfter completing the program, wait for the report.", 
                 font=("Fira Sans Condensed", 12), foreground="#ffffff", background='#003da6')
desc.grid(column=0, row=2, columnspan=2, sticky='EWNS') 
root.mainloop()