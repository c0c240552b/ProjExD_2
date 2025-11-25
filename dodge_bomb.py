import os
import sys
import pygame as pg
import random
import time #演習課題1　pg.time.wait を使うため

WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


#練習問題3: check_bound 関数の定義 (型ヒントとdocstring付き)
def check_bound(obj_rct: pg.Rect, obj_sum_mv: tuple) -> tuple[bool, bool]:
    
    yoko, tate = True, True
    
    if obj_rct.left + obj_sum_mv[0] < 0 or WIDTH < obj_rct.right + obj_sum_mv[0]:
        yoko = False
    
    if obj_rct.top + obj_sum_mv[1] < 0 or HEIGHT < obj_rct.bottom + obj_sum_mv[1]:
        tate = False
    
    return yoko, tate

#演習課題1: ゲームオーバー画面関数の定義
def game_over(screen: pg.Surface):
    
    # 1. 半透明のSurface作成
    over_surface = pg.Surface((WIDTH, HEIGHT))
    # 半透明の黒にするため、透過度を設定し黒で塗りつぶす
    over_surface.set_alpha(150)           
    over_surface.fill((0, 0, 0))          
    
    # 2. Game Overテキストの準備
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 255, 255))
    text_rct = text.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
    
    # 3. 泣いているこうかとん
    kk_img_cry = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    kk_rct_cry = kk_img_cry.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
    
    # 4. 画面への描画と更新
    screen.blit(over_surface, (0, 0))  
    screen.blit(text, text_rct)        
    screen.blit(kk_img_cry, kk_rct_cry) 
    pg.display.update()
    
    #5秒間停止
    pg.time.wait(5000)

#演習課題2: 爆弾 Surface リストの準備関数の定義 
def init_bb_imgs() -> list[tuple[pg.Surface, int]]:
    
    bb_imgs = []
    # (半径, 速度) のリスト
    params = [(10,5), (15,8), (20,11), (25,14), (30,17), (35,20),(40,23),(45,26),(50,29),(55,32)] 
    
    for r, v in params:
        bb_img = pg.Surface((2*r, 2*r))#爆弾作成
        pg.draw.circle(bb_img, (255, 0, 0), (r, r), r)#赤玉の描画
        bb_img.set_colorkey((0, 0, 0))#透過色設定
        bb_imgs.append((bb_img, v)) #リスト追加
    
    return bb_imgs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")     
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
   #演習課題2: 爆弾の初期設定を関数呼び出しに置き換え
    bb_img_params = init_bb_imgs()
    bb_img, speed = bb_img_params[0] 
    vx, vy = speed, speed

    bb_rct = bb_img.get_rect()#最初の爆弾
    bb_rct.centerx = random.randint(0, WIDTH)#画面の幅ランダム
    bb_rct.centery = random.randint(0, HEIGHT)#画面の高さランダム
    
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

        #演習課題2: 時間経過による爆弾の拡大と加速
        level = min(tmr // 500, len(bb_img_params) - 1)#tmr÷500の商をレベルとする
        bb_img_new, speed_new = bb_img_params[level]
        
        # 画像または速度が変更されたかチェックし、更新
        if bb_img_new is not bb_img or abs(vx) != speed_new or abs(vy) != speed_new:
            bb_img = bb_img_new
            speed = speed_new
            
            # 速度の更新（向きは変えない）
            vx = speed if vx > 0 else -speed
            vy = speed if vy > 0 else -vy
            
            # 画像の変更に伴いRectを更新（中央座標は維持）
            center = bb_rct.center
            bb_rct = bb_img.get_rect(center=center)
        
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
            #game overの表示
            game_over(screen)
            return 
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()