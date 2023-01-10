import pygame as pg
import sys


# スクリーンクラス
class Screen:
    def __init__(self, title, wh, img_path):
        pg.display.set_caption(title)  # turnshot
        self.sfc = pg.display.set_mode(wh)  # (1500, 900)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(img_path)  # fig/pg_bg.jpg
        self.bgi_rct = self.bgi_sfc.get_rect()

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)


# 操作キャラクラス
class Ship:
    key_delta = [{
        pg.K_w: [0, -1],
        pg.K_s: [0, +1],
        pg.K_a: [-1, 0],
        pg.K_d: [+1, 0] },
        {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0]}]

    def __init__(self, img_path, xy, player):
        self.sfc = pg.image.load(img_path)  # fig_ts/ship_1
        self.sfc = pg.transform.rotate(self.sfc, -90+player*180)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.pl = player  # 0(左) or 1(右)
        self.bullet_lst = []  # 弾のリスト

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        # 移動の処理
        key_dct = pg.key.get_pressed()
        for key, delta in Ship.key_delta[self.pl].items():
            if key_dct[key]:
                self.rct.centerx += delta[0]
                self.rct.centery += delta[1]
            if check_bound(self.rct, scr.rct) != (+1, +1):
                self.rct.centerx -= delta[0]
                self.rct.centery -= delta[1]
        self.blit(scr)


# バレットクラス
class Bullet:
    def __init__(self, img_path, xy, player, bullet_type, vx, vy):
        self.sfc = pg.image.load(img_path)  
        self.sfc = pg.transform.rotate(self.sfc, -90+player*180)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.pl = player  # 0(左) or 1(右)
        self.bullet_type = bullet_type  # 0(通常) or 1(拡散前)
        self.vx = vx
        self.vy = vy
        self.bullet_lst = []

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    # 弾の位置の更新
    def update(self, scr:Screen, pl:Ship, turn, frame):
        if turn == 0:
            self.rct.move_ip(self.vx, self.vy)
        if frame % 1500 == 1100 and self.bullet_type == 1:
            for i in range(-1, 2):
                self.bullet_lst.append(Bullet("fig_ts/bullet_1.png", self.rct.center, 1, 0, 0, i))
                self.bullet_type = 0
        self.blit(scr) 
        return self.bullet_lst


def check_bound(obj_rct, scr_rct):
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate


def main():
    # 初期設定
    clock =pg.time.Clock()

    scr = Screen("turnshot", (1500, 900), "fig_ts/pg_bg.jpg")

    # 操作キャラ設定
    pl = []
    pl += [Ship("fig_ts/ship_1.png", (300, 450), 0)]
    pl += [Ship("fig_ts/ship_1.png", (1200, 450), 1)]
    for i in range(2):
        pl[i].update(scr)

    frame = 0  # 経過フレーム
    turn = 0  # 現在のターン(0=回避，1=設置)

    # ループ時の処理
    while True:
        scr.blit()

        # ボタンを押された時の処理
        for event in pg.event.get():
            # xボタンの処理
            if event.type == pg.QUIT:
                return
            # 設置ターン中の処理
            if event.type == pg.KEYDOWN and turn == 1:
                if event.key == pg.K_LCTRL:
                    bullet = Bullet("fig_ts/bullet_1.png", pl[0].rct.center, 0, 0, 2, 0)
                    pl[0].bullet_lst += [bullet]
                if event.key == pg.K_RCTRL:
                    bullet = Bullet("fig_ts/bullet_2.png", pl[1].rct.center, 1, 1, -2, 0)
                    pl[1].bullet_lst += [bullet]
                
        # プレイヤーの更新
        for i in range(2):
            pl[i].update(scr)

        # 弾の更新
        for i in range(2):
            for shot in pl[i].bullet_lst:
                bullet_lst = []
                bullet_lst = shot.update(scr, pl[i], turn, frame)
                if bullet_lst != []:
                    pl[i].bullet_lst += bullet_lst
                if pl[(i+1)%2].rct.colliderect(shot.rct):
                    return
                if shot.rct.right < scr.rct.left or shot.rct.right < scr.rct.left:
                    pl[i].bullet_lst.pop(pl[i].bullet_lst.index(shot))

        if frame % 750 == 0:
            turn = (turn+1)%2

        pg.display.update()  # ディスプレイの更新
        frame += 1  # フレームカウントを進める
        clock.tick(1000)  # 1000fpsで動かす


# メイン関数の実装
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()