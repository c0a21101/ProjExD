import tkinter as tk
import maze_maker


#リアルタイム処理関数
def main_proc():
    global cx, cy

    # 十字キーが押されていたらその方向にこうかとんを移動させる
    if key == "Up":
        cy -= 20
    elif key == "Down":
        cy += 20
    elif key == "Left":
        cx -= 20
    elif key == "Right":
        cx += 20

    # 座標の更新
    canvas.coords("player",cx,cy)
    root.after(20, main_proc)


def key_down(event):
    global key
    key = event.keysym


def key_up(event):
    global key
    key = ""


if __name__ == "__main__":
    # ウィンドウ生成
    root = tk.Tk()
    root.title("迷えるこうかとん")

    # 背景が黒色のCanvasを生成
    canvas = tk.Canvas(width=1500,height=900,bg="black")

    # 迷路の生成
    maze = maze_maker.make_maze(15, 9)
    maze_maker.show_maze(canvas, maze)

    # こうかとんの画像を表示
    cx = 300  # こうかとんの横軸の現在地
    cy = 400  # こうかとんの縦軸の現在地
    image = tk.PhotoImage(file="fig/0.png")
    canvas.create_image(cx,cy,image=image,tag="player")
    canvas.pack()

    key = ""  # 現在押されているキー

    main_proc()

    # key_down()
    root.bind("<KeyPress>", key_down)

    # key_up()
    root.bind("<KeyRelease>", key_up)

    root.mainloop()