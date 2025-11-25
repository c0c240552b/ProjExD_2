import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


#練習問題3: check_bound 関数の定義 (型ヒントとdocstring付き)
def check_bound(obj_rct: pg.Rect, obj_sum_mv: tuple) -> tuple[bool, bool]:
    
    yoko, tate = True, True
    
    # 横方向 (X軸) の判定
    if obj_rct.left + obj_sum_mv[0] < 0 or WIDTH < obj_rct.right + obj_sum_mv[0]:
        yoko = False
    
    # 縦方向 (Y軸) の判定
    if obj_rct.top + obj_sum_mv[1] < 0 or HEIGHT < obj_rct.bottom + obj_sum_mv[1]:
        tate = False
    
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")     
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    # 爆弾の初期設定
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5
    
    DELTA = {
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0)
    }
    
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
                
        #練習問題3: こうかとんの画面外判定と処理
        avaiable_x, avaiable_y = check_bound(kk_rct, tuple(sum_mv))
        if not avaiable_x: # 横方向が画面外
            sum_mv[0] = 0
        if not avaiable_y: # 縦方向が画面外
            sum_mv[1] = 0

        kk_rct.move_ip(sum_mv)
        screen.blit(kk_img, kk_rct)
        
        #練習問題3: 爆弾の画面外判定と処理
        avaiable_x, avaiable_y = check_bound(bb_rct, (vx, vy))
        if not avaiable_x: # 横方向が画面外
            vx *= -1
        if not avaiable_y: # 縦方向が画面外
            vy *= -1
            
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)
        
        # 練習問題4: 衝突判定
        if kk_rct.colliderect(bb_rct):
            return 
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()