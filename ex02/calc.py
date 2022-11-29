import tkinter as tk
import tkinter.messagebox as tkm

#ボタンを押された時の挙動
def button_click(event):
    btn = event.widget
    txt = btn["text"]
    # = の時
    if txt == "=":
        formula = entry.get()
        entry.delete(0, tk.END)
        entry.insert(tk.END, eval(formula))
    else:
        #四則演算の時
        if txt in operators:
            if entry.get()[-1].isdecimal() == True:
                if txt == "×":
                    txt = "*"
                if txt == "÷":
                    txt = "/"
                entry.insert(tk.END, txt)
        #削除系の時
        elif txt in deletes:
            if txt == "←":
                entry.delete(len(entry.get())-1, tk.END)
            if txt == "AC":
                entry.delete(0, tk.END)
            if txt == "C":
                not_num = 0
                for i in range(len(entry.get())-1, 0, -1):
                    if entry.get()[i].isdecimal() == False:
                        if entry.get()[i].isdecimal() != ".":
                            not_num = i
                        break
                entry.delete(not_num, tk.END)
            entry.insert(0, 0)
        #小数点の時
        elif txt == ".":
            not_num = 0
            for i in range(len(entry.get())-1, 0, -1):
                if entry.get()[i].isdecimal() == False:
                    if entry.get()[i].isdecimal() != ".":
                        not_num = i
                        break
            if not "." in entry.get()[not_num:]:
                if len(entry.get()[not_num:]) > 0:
                    entry.insert(tk.END, txt)
        #その他（数字）の時
        else:
            entry.insert(tk.END, txt)
        #頭に余分な0があったら消す
        if len(entry.get()) > 1:
            if entry.get()[0] == "0":
                if entry.get()[1] != ".":
                    entry.delete(0, 1)

#初期設定
root = tk.Tk()
root.geometry("400x600")

#各種ボタンの作成
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

button_pt = tk.Button(root,
                      text = ".",
                      width = "4",
                      height = "2",
                      font = ("", 30))
button_pt.grid(row = 5, column = 2)
button_pt.bind("<1>", button_click)

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

deletes = ["←", "C", "AC"]
button_del = [0] * len(deletes)
for i in range(len(deletes)):
    button_del[i] = tk.Button(root,
                              text = deletes[i],
                              width = "4",
                              height = "2",
                              font = ("", 30))
    button_del[i].grid(row = 1, column = i)
    button_del[i].bind("<1>", button_click)

#出力部分
entry = tk.Entry(justify = "right",
                 width = 42,
                 font = 40)
entry.insert(tk.END, "0")
entry.grid(row = 0, column = 0, columnspan = 4)

root.mainloop()
