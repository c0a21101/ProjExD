import pygame as pg
import sys


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1600,900))  # ウィンドウ生成

    clock = pg.time.Clock()  # 時間計測用のオブジェクト
    clock.tick(1000)  # 1000fpsの時を刻む

    bg_sfc = pg.image.load("fig/pg_bg.jpg")
    bg_rct = bg_sfc.get_rect()
    bg_rct.center = 800, 450
    scrn_sfc.blit(bg_sfc, bg_rct)

    pg.display.update()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:  # 「×」ボタンが押されたらウィンドウを閉じる
                return


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()