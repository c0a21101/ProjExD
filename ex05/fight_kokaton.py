import pygame as pg
import random
import sys
import copy


class Screen:
    def __init__(self, title, wh, img_path):
        pg.display.set_caption(title)  # 負けるな！こうかとん
        self.sfc = pg.display.set_mode(wh)  # (1600, 900)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(img_path)  # fig/pg_bg.jpg
        self.bgi_rct = self.bgi_sfc.get_rect()

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)


class Bird:
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
        self.lives = 3  # 残基
        self.power = 1  # パワー（2だと加速＆無敵，1だと通常通り）
        self.p_up_time = 0  # パワーが上がる残りフレーム数

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        key_dct = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_dct[key]:
                self.rct.centerx += delta[0] * self.power
                self.rct.centery += delta[1] * self.power
            if check_bound(self.rct, scr.rct) != (+1, +1):
                self.rct.centerx -= delta[0] * self.power
                self.rct.centery -= delta[1] * self.power
        if self.p_up_time > 0:
            self.power = 2
            self.p_up_time -= 1
        else:
            self.power = 1
        self.blit(scr)


class Bomb:
    def __init__(self, color, rad, vxy, scr:Screen):
        self.sfc = pg.Surface((2*rad, 2*rad)) # 正方形の空のSurface
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = 10
        self.vx, self.vy = vxy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        scr.sfc.blit(self.sfc, self.rct) 


class Item:
    drop_speed = 1

    def __init__(self, img_path, scr:Screen):
        self.sfc = pg.image.load(img_path)  # アイテムの見た目
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = 0

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(0, Item.drop_speed)
        scr.sfc.blit(self.sfc, self.rct) 

    # y座標の取得    
    def check_y(self):
        return self.rct.centery

    # アイテム取得時の処理（継承先で書く）
    def catch(self):
        pass


class Heart(Item):
    def __init__(self, img_path, scr:Screen):
        super().__init__(img_path, scr)

    # アイテム取得時の処理
    def catch(self, kkt:Bird):
        kkt.lives += 1

class Power(Item):
    def __init__(self, img_path, scr:Screen):
        super().__init__(img_path, scr)

    # アイテム取得時の処理
    def catch(self, kkt:Bird):
        kkt.p_up_time += 1500

class Text:
    def __init__(self, font):
        self.font = pg.font.Font(font, 40)
        self.sfc = self.font.render("", True, (0, 0, 0))
        self.rct = self.sfc.get_rect()
        self.rct.topleft = 30, 15

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

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
    clock =pg.time.Clock()

    scr = Screen("負けるな！こうかとん", (1600, 900), "fig/pg_bg.jpg")

    kkt = Bird("fig/6.png", 2.0, (900, 400))
    kkt.update(scr)

    txt = Text("/Windows/Fonts/meiryo.ttc")

    frame = 0
    items = []
    bombs = []

    while True:
        scr.blit()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        
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

        new_bombs = []
        for bomb in bombs:
            bomb.update(scr)
            if kkt.rct.colliderect(bomb.rct):
                if kkt.power != 2:
                    kkt.lives -= 1
                    if kkt.lives <= 0:
                        return
                continue
            new_bombs += [bomb]
        bombs = copy.copy(new_bombs)

        new_items = []
        for item in items:
            item.update(scr)
            if kkt.rct.colliderect(item.rct):
                item.catch(kkt)
                continue
            if item.check_y() < scr.rct.height:
                new_items += [item]
        items = copy.copy(new_items)
        

        pg.display.update()
        frame += 1
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()