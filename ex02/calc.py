import tkinter as tk
import tkinter.messagebox as tkm


def button_click(event):
    btn = event.widget
    txt = btn["text"]
    if txt == "=":
        formula = entry.get()
        entry.delete(0, tk.END)
        entry.insert(tk.END, eval(formula))
    else:
        if txt == "×":
            txt = "*"
        if txt == "÷":
            txt = "/"
        entry.insert(tk.END, txt)

root = tk.Tk()
root.geometry("400x600")

button_num = [0] * 10
for i in range(len(button_num)):
    button_num[i] = tk.Button(root,
                              text = str(i),
                              width = "4",
                              height = "2",
                              font = ("", 30))
    if i != 0:
        button_num[i].grid(row = 5 - (i+2)//3, column = (i-1)%3)
    else:
        button_num[i].grid(row = 5, column = 1)
    button_num[i].bind("<1>", button_click)

operators = ["+", "-", "×", "÷", "="]
button_ope = [0] * len(operators)
for i in range(len(operators)):
    button_ope[i] = tk.Button(root,
                              text = operators[i],
                              width = "4",
                              height = "2",
                              font = ("", 30))
    button_ope[i].grid(row = i+1, column = 3)
    button_ope[i].bind("<1>", button_click)

entry = tk.Entry(justify = "right",
                 width = 42,
                 font = 40)
entry.grid(row = 0, column = 0, columnspan = 4)

root.mainloop()
