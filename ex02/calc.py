import tkinter as tk
import tkinter.messagebox as tkm


def button_click(event):
    btn = event.widget
    txt = btn["text"]
    tkm.showinfo(txt, f"{txt}のボタンが押されました")

root = tk.Tk()
root.geometry("300x500")

button_num = [0] * 10
for i in range(len(button_num)):
    button_num[i] = tk.Button(root,
                              text = str(i),
                              width = "4",
                              height = "2",
                              font = ("", 30))
    button_num[i].grid(row = 4 - (i+2)//3, column = 2 - (i-1)%3)
    button_num[i].bind("<1>", button_click)

operators = ["+", "="]
button_ope = [0] * len(operators)
for i in range(len(operators)):
    button_ope[i] = tk.Button(root,
                              text = operators[i],
                              width = "4",
                              height = "2",
                              font = ("", 30))
    button_ope[i].grid(row = 4, column = 1 + i)

entry = tk.Entry(justify = "right",
                 width = 30,
                 font = 40)
entry.grid(row = 0, column = 0, columnspan = 3)

root.mainloop()
