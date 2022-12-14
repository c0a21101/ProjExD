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
    bomb_rct = [bomb_sfc.get_rect()]
    bomb_rct[0].center = random.randint(10,scrn_rct.width-10), 10
    vx, vy = [1], [1]

    # テキスト生成
    font = pg.font.Font("/Windows/Fonts/meiryo.ttc", 40)
    text_sfc = font.render("", True, (0, 0, 0))
    text_rct = text_sfc.get_rect()
    text_rct.topleft = 30, 15

    frame = 0  # 経過したフレームの数
    score = 0  # 現在のスコア
    high_score = 0  # 起動してからの最高のスコア

    while True:
        # 背景の描画
        scrn_sfc.blit(bg_sfc, bg_rct)

        # イベントを繰り返しで処理
        for event in pg.event.get():
            if event.type == pg.QUIT:  # 「×」ボタンが押されたらウィンドウを閉じる
                return

        # こうかとんの描写
        key_dct = pg.key.get_pressed()
        def move(n):
            if key_dct[pg.K_UP]:
                tori_rct.centery -= n
            if key_dct[pg.K_DOWN]:
                tori_rct.centery += n
            if key_dct[pg.K_LEFT]:
                tori_rct.centerx -= n
            if key_dct[pg.K_RIGHT]:
                tori_rct.centerx += n

        move(1)
        if check_bound(tori_rct, scrn_rct) != (1, 1):
            move(-1)

        scrn_sfc.blit(tori_sfc, tori_rct)

        # 爆弾の描写
        for i in range(len(bomb_rct)):
            bomb_rct[i].move_ip(vx[i], vy[i])
            yoko, tate = check_bound(bomb_rct[i], scrn_rct)
            vx[i] *= yoko 
            vy[i] *= tate
            scrn_sfc.blit(bomb_sfc, bomb_rct[i])
            # こうかとんとの接触判定
            if bomb_rct[i].colliderect(tori_rct):
                # スコアを0にする
                score = 0
                # 接触時に爆弾を全部消す
                bomb_rct, vx, vy = [], [], []
                break
        
        # 1000フレームごとの処理
        if frame % 1000 == 999:
            # 現在の爆弾の数に応じてスコアを増やす
            score += len(bomb_rct) * 100
            high_score = max(score, high_score)

            # 爆弾を時間経過で増やす
            bomb_rct += [bomb_sfc.get_rect()]
            bomb_rct[-1].center = random.randint(10,scrn_rct.width-10), 10
            vx += [1]
            vy += [1]


        # テキストの描画
        scrn_sfc.blit(text_sfc, text_rct)
        text_sfc = font.render(f"スコア：{score} ハイスコア：{high_score}", True, (0, 0, 0))

        pg.display.update()
        frame += 1
        clock.tick(1000)  # 1000fpsの時を刻む


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()