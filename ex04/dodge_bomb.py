import pygame as pg
import sys


def main():
    clock = pg.time.Clock()  # 時間計測用のオブジェクト

    # ウィンドウ生成
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1600,900))

    # 背景生成
    bg_sfc = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect()
    bg_rct.center = 800, 450
    scrn_sfc.blit(bg_sfc, bg_rct)

    # 操作キャラ（こうかとん）生成
    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 800, 450
    scrn_sfc.blit(tori_sfc, tori_rct)

    pg.display.update()
    clock.tick(1000)  # 1000fpsの時を刻む

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:  # 「×」ボタンが押されたらウィンドウを閉じる
                return


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()