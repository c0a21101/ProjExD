import tkinter as tk


if __name__ == "__main__":
    #ウィンドウ生成
    root = tk.Tk()
    root.title("迷えるこうかとん")

    #背景が黒色のCanvasを生成
    canvas = tk.Canvas(width=1500,height=900,bg="black")
    canvas.pack()

    root.mainloop()