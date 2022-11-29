import tkinter as tk

root = tk.Tk()
root.geometry("300x500")

button = [0] * 10
for i in range(10):
    button[i] = tk.Button(root,
                        text = str(i),
                        width = "4",
                        height = "2",
                        font = ("", 30),)
    button[i].grid(row = 3 - (i+2)//3, column = 3 - (i-1)%3)

root.mainloop()
