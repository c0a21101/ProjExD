import random
import pygame as pg
import sys


# 画面の端に到着したら跳ね返る関数
def check_bound(obj_rct, scr_rct):
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or obj_rct.right > scr_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or obj_rct.bottom > scr_rct.bottom:
        tate = -1
    return yoko, tate


def main():
    clock = pg.time.Clock()  # 時間計測用のオブジェクト

    # ウィンドウ生成
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1600,900))
    scrn_rct = scrn_sfc.get_rect()

    # 背景生成
    bg_sfc = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect()
    bg_rct.center = 800, 450

    # 操作キャラ（こうかとん）生成
    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 800, 450

    # 爆弾生成
    bomb_sfc = pg.Surface((20,20))
    bomb_sfc.set_colorkey((0, 0, 0))
    pg.draw.circle(bomb_sfc, (255, 0, 0), (10,10), 10)
    bomb_rct = bomb_sfc.get_rect()
    bomb_rct.center = random.randint(10,scrn_rct.width-10), random.randint(10,scrn_rct.height-10)
    vx, vy = +1, +1

    while True:
        # 背景の描画
        scrn_sfc.blit(bg_sfc, bg_rct)

        # イベントを繰り返しで処理
        for event in pg.event.get():
            if event.type == pg.QUIT:  # 「×」ボタンが押されたらウィンドウを閉じる
                return

        # こうかとんの描写
        key_dct = pg.key.get_pressed()
        if key_dct[pg.K_UP]:
            tori_rct.centery -= 1
        if key_dct[pg.K_DOWN]:
            tori_rct.centery += 1
        if key_dct[pg.K_LEFT]:
            tori_rct.centerx -= 1
        if key_dct[pg.K_RIGHT]:
            tori_rct.centerx += 1
        if check_bound(tori_rct, scrn_rct) != (1, 1):
            if key_dct[pg.K_UP]:
                tori_rct.centery += 1
            if key_dct[pg.K_DOWN]:
                tori_rct.centery -= 1
            if key_dct[pg.K_LEFT]:
                tori_rct.centerx += 1
            if key_dct[pg.K_RIGHT]:
                tori_rct.centerx -= 1

        scrn_sfc.blit(tori_sfc, tori_rct)

        # 爆弾の描写
        bomb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bomb_rct, scrn_rct)
        vx *= yoko
        vy *= tate
        scrn_sfc.blit(bomb_sfc, bomb_rct)

        if tori_rct.colliderect(bomb_rct):
            return
        pg.display.update()
        clock.tick(1000)  # 1000fpsの時を刻む


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()