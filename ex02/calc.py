import tkinter as tk
import tkinter.messagebox as tkm


def button_click(event):
    btn = event.widget
    txt = btn["text"]
    tkm.showinfo(txt, f"{txt}のボタンが押されました")

root = tk.Tk()
root.geometry("300x500")

button = [0] * 10
for i in range(10):
    button[i] = tk.Button(root,
                        text = str(i),
                        width = "4",
                        height = "2",
                        font = ("", 30))
    button[i].grid(row = 3 - (i+2)//3, column = 3 - (i-1)%3)
    button[i].bind("<1>", button_click)

root.mainloop()
