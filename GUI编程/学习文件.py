import tkinter as tk

top = tk.Tk()
label = tk.Label(top, text='你猜')


def hello():
    label.config(text='hello')


top.title('hello')
top.geometry('500x500')

menu = tk.Menu(top)
menu.add_command(label='显示', command=hello)
menu.add_command(label='退出', command=top.quit)

frame = tk.Frame(top, width=500, height=500)


def popup(event):
    menu.post(event.x_root, event.y_root)


frame.bind('<Button-3>', popup)
top.config(menu=menu)
label.pack()
frame.pack()
top.mainloop()

