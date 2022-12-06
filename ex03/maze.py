import tkinter as tk


def key_down(event):
    global key
    key = event.keysym


if __name__ == "__main__":
    # ウィンドウ生成
    root = tk.Tk()
    root.title("迷えるこうかとん")

    # 背景が黒色のCanvasを生成
    canvas = tk.Canvas(width=1500,height=900,bg="black")

    # こうかとんの画像を表示
    cx = 300  # こうかとんの横軸の現在地
    cy = 400  # こうかとんの縦軸の現在地
    image = tk.PhotoImage(file="fig/0.png")
    canvas.create_image(cx,cy,image=image)
    canvas.pack()

    key = ""  # 現在押されているキー

    # key_down()
    root.bind("<KeyPress>", key_down)

    root.mainloop()