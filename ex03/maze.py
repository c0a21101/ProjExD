import tkinter as tk
import maze_maker
import random
import copy



#リアルタイム処理関数
def main_proc():
    global mx, my, timer

    # 十字キーが押されていたらその方向にこうかとんを移動させる
    if key == "Up" and maze[mx][my-1] == 0:
        my -= 1
        timer = 0
    elif key == "Down" and maze[mx][my+1] == 0:
        my += 1
        timer = 0
    elif key == "Left" and maze[mx-1][my] == 0:
        mx -= 1
        timer = 0
    elif key == "Right" and maze[mx+1][my] == 0:
        mx += 1
        timer = 0
    else:
        timer += 1
    
    # 座標の更新
    cx = mx * 100 + 50
    cy = my * 100 + 50
    canvas.coords("player",cx,cy)

    # 画像の更新
    canvas.delete('player')	
    if timer <= 4:
        canvas.create_image(cx,cy,image=images[2],tag="player")
    elif timer <= 20:
        canvas.create_image(cx,cy,image=images[1],tag="player")
    else:
        canvas.create_image(cx,cy,image=images[0],tag="player")
    root.after(50, main_proc)


# ゴール生成アルゴリズム
def set_goal(x, y, id = 0):
    global far, queue, gx, gy
    if far[x][y-1] == 0:
        queue += [[x, y-1]]
        far[x][y-1] = 1
    if far[x][y+1] == 0:
        queue += [[x, y+1]]
        far[x][y+1] = 1
    if far[x-1][y] == 0:
        queue += [[x-1, y]]
        far[x-1][y] = 1
    if far[x+1][y] == 0:
        queue += [[x+1, y]]
        far[x+1][y] = 1
    if id < len(queue)-1:
        set_goal(queue[id+1][0], queue[id+1][1], id+1)
    else:
        gx = x
        gy = y



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

    # スタート地点の設定
    sx = random.randrange(1,15,2)
    sy = random.randrange(1,9,2)
    canvas.create_rectangle(sx*100, sy*100, sx*100+100, sy*100+100, fill="blue")

    # ゴール地点の設定
    far = copy.deepcopy(maze)
    far[sx][sy] = 1
    queue = [[sx, sy]]
    set_goal(queue[0][0], queue[0][1])
    canvas.create_rectangle(gx*100, gy*100, gx*100+100, gy*100+100, fill="green")

    # こうかとんの画像を表示
    mx = sx  # こうかとんの横軸のマス
    my = sy  # こうかとんの縦軸のマス
    cx = mx * 100 + 50  # こうかとんの横軸の座標
    cy = my * 100 + 50  # こうかとんの縦軸の座標
    images = [tk.PhotoImage(file="fig/0.png"),
              tk.PhotoImage(file="fig/2.png"),
              tk.PhotoImage(file="fig/3.png")]
    canvas.create_image(cx,cy,image=images[1],tag="player")
    canvas.pack()

    key = ""  # 現在押されているキー

    timer = 0  # こうかとんが動いてからの時間
    main_proc()

    # key_down()
    root.bind("<KeyPress>", key_down)

    # key_up()
    root.bind("<KeyRelease>", key_up)

    root.mainloop()