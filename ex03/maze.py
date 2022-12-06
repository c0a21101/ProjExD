import tkinter as tk
import maze_maker


#リアルタイム処理関数
def main_proc():
    global mx, my

    # 十字キーが押されていたらその方向にこうかとんを移動させる
    if key == "Up":
        my -= 1
    elif key == "Down":
        my += 1
    elif key == "Left":
        mx -= 1
    elif key == "Right":
        mx += 1
    # 座標の更新
    cx = mx * 100 + 50
    cy = my * 100 + 50

    # 座標の更新
    canvas.coords("player",cx,cy)
    root.after(80, main_proc)


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
    mx = 1  # こうかとんの横軸のマス
    my = 1  # こうかとんの縦軸のマス
    cx = mx * 100 + 50  # こうかとんの横軸の座標
    cy = my * 100 + 50  # こうかとんの縦軸の座標
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