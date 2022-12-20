import pygame as pg
import random
import sys
import copy


# スクリーンクラス
class Screen:
    def __init__(self, title, wh, img_path):
        pg.display.set_caption(title)  # 負けるな！こうかとん
        self.sfc = pg.display.set_mode(wh)  # (1600, 900)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(img_path)  # fig/pg_bg.jpg
        self.bgi_rct = self.bgi_sfc.get_rect()

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)

# こうかとん（操作キャラ）クラス
class Bird:
    # 入力された十字キーと移動方向の対応
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
    }

    def __init__(self, img_path, ratio, xy):
        self.sfc = pg.image.load(img_path)  # fig/6.png
        self.sfc = pg.transform.rotozoom(self.sfc, 0, ratio)  # 2.0
        self.rct = self.sfc.get_rect()
        self.rct.center = xy  # 900, 400
        self.lives = 3  # 残基を示す変数
        self.power = 1  # パワーを示す変数（2だと加速＆無敵，1だと通常通り）
        self.p_up_time = 0  # パワーが上がる残りフレーム数

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        # 移動の処理（パワーに応じて加速）
        key_dct = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_dct[key]:
                self.rct.centerx += delta[0] * self.power
                self.rct.centery += delta[1] * self.power
            if check_bound(self.rct, scr.rct) != (+1, +1):
                self.rct.centerx -= delta[0] * self.power
                self.rct.centery -= delta[1] * self.power
        # 現在のパワーの更新
        if self.p_up_time > 0:
            self.power = 2
            self.p_up_time -= 1
        else:
            self.power = 1
        self.blit(scr)


# 爆弾クラス
class Bomb:
    def __init__(self, color, rad, vxy, scr:Screen):
        self.sfc = pg.Surface((2*rad, 2*rad)) # 正方形の空のSurface
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)  # 出現位置 横はランダム
        self.rct.centery = 10  # 出現位置 縦はy=10で固定
        self.vx, self.vy = vxy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        # 爆弾の移動
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        scr.sfc.blit(self.sfc, self.rct) 


# アイテムクラス
class Item:
    drop_speed = 1  # アイテムの落下する速さ

    def __init__(self, img_path, scr:Screen):
        self.sfc = pg.image.load(img_path)  # アイテムの見た目
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = 0

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    # アイテムの位置の更新
    def update(self, scr:Screen):
        self.rct.move_ip(0, Item.drop_speed)
        scr.sfc.blit(self.sfc, self.rct) 

    # y座標の取得    
    def check_y(self):
        return self.rct.centery

    # アイテム取得時の処理（継承先で書く）
    def catch(self):
        pass


# ハートクラス（アイテムクラスを継承）
class Heart(Item):
    def __init__(self, img_path, scr:Screen):
        super().__init__(img_path, scr)

    # アイテム取得時の処理
    # 残基を1増やす
    def catch(self, kkt:Bird):
        kkt.lives += 1


# パワークラス（アイテムクラスを継承）
class Power(Item):
    def __init__(self, img_path, scr:Screen):
        super().__init__(img_path, scr)

    # アイテム取得時の処理
    # 無敵時間を1500フレーム延長する
    def catch(self, kkt:Bird):
        kkt.p_up_time += 1500


# テキストクラス
class Text:
    def __init__(self, font):
        self.font = pg.font.Font(font, 40)  # フォントの設定
        self.sfc = self.font.render("", True, (0, 0, 0))
        self.rct = self.sfc.get_rect()
        self.rct.topleft = 30, 15

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    # テキストを表示
    def update(self, txt, scr:Screen):
        self.sfc = self.font.render(txt, True, (0, 0, 0))
        scr.sfc.blit(self.sfc, self.rct) 


def check_bound(obj_rct, scr_rct):
    """
    第1引数：こうかとんrectまたは爆弾rect
    第2引数：スクリーンrect
    範囲内：+1／範囲外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate


def main():
    # 初期設定
    clock =pg.time.Clock()

    scr = Screen("負けるな！こうかとん", (1600, 900), "fig/pg_bg.jpg")

    kkt = Bird("fig/6.png", 2.0, (900, 400))
    kkt.update(scr)

    txt = Text("/Windows/Fonts/meiryo.ttc")

    frame = 0
    items = []
    bombs = []

    # ループ時の処理
    while True:
        scr.blit()

        # ×ボタンを押された時の処理
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        
        # こうかとんとテキストの更新
        kkt.update(scr)
        txt.update(f"残りライフ：{kkt.lives} パワーアップ残り時間：{kkt.p_up_time}", scr)

        # アイテムや爆弾を追加する
        if frame % 3000 == 0:  # 残基＋
            heart = Heart("fig/heart.png", scr)
            items += [heart]
        if frame % 10000 == 0:  # 無敵化
            power = Power("fig/power.png", scr)
            items += [power]
        if frame % 800 == 0:  # 爆弾
            bomb = Bomb((255, 0, 0), 10, (+1, +1), scr)
            bombs += [bomb]
        
        # 爆弾の処理
        new_bombs = []
        for bomb in bombs:
            bomb.update(scr)  # 爆弾の更新
            if kkt.rct.colliderect(bomb.rct):  # こうかとんが爆弾に触れたら
                if kkt.power != 2:  # もしこうかとんが無敵でないなら
                    kkt.lives -= 1  # 残基を1減らす
                    if kkt.lives <= 0:  # 残基が0以下なら
                        return  # ゲームを終了
                continue  # 爆弾に触れていたら以下の処理を飛ばす
            new_bombs += [bomb]  # 次のフレームでも爆弾を描写する
        bombs = copy.copy(new_bombs)  # 爆弾リストの更新

        # アイテムの処理
        new_items = []
        for item in items:
            item.update(scr)  # アイテムの更新
            if kkt.rct.colliderect(item.rct):  # こうかとんが爆弾に触れたら
                item.catch(kkt)  # アイテム取得時の処理を行う
                continue  # アイテムに触れていたら以下の処理を飛ばす
            if item.check_y() < scr.rct.height:  # もしアイテムが画面内にあるなら
                new_items += [item]  # 次のフレームでもアイテムを描写する
        items = copy.copy(new_items)  # アイテムリストの更新
        
        pg.display.update()  # ディスプレイの更新
        frame += 1  # フレームカウントを進める
        clock.tick(1000)  # 1000fpsで動かす


# メイン関数の実装
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()