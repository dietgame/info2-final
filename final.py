import pyxel#ライブラリ

ITEMS_OK = [2, 7, 8, 10, 11, 12, 13]

class Ball:
   
    def __init__(self, fs):
        self.field_size = fs
        self.restart()
        self.speed = 1.5
       
    def move(self):
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed
        if (self.x < 0) or (self.x >= self.field_size):#0以下の時は左側よりもさらに左に行く時（壁にぶつかった時）反対側に跳ね返る仕組みであることを示す
            self.vx = -self.vx##反対側に跳ね返る仕組み

    def restart(self):
        self.x = pyxel.rndi(0, self.field_size - 1)
        self.y = 0
        angle = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(angle)
        self.vy = pyxel.sin(angle)
        self.type = pyxel.rndi(0,15) #落ちてくる食べ物を決める
       
class Pad:
    def __init__(self, fs):
        self.field_size = fs#変数
        self.x = self.field_size / 2 #field_sizeは全体サイズ、半分に割ることで全体のちょうど真ん中に持ってこれる
        self.size = 23 #5は適当な数、パッドの大きさを定義付けている

    def catch(self, ball): #受け取れたらTrue, そうでなければFalseを返す
        if ball.y >= self.field_size-self.field_size/40 and (self.x-self.size/2 <= ball.x <= self.x+self.size/2):
            #self.sizeの割る２してself.xを引くと、全体の真ん中の位置を指定できる（逆に足すと端を指定できる）
#            return True
            if ball.type in ITEMS_OK: #small rice
                pyxel.play(0, 0) # 成功
                ball.restart()
                return True
            else: 
                pyxel.play(0, 1) # 失敗
                #ball.restart() 
                return False 
        else:
            return False
        
class App: #本体
    def __init__ (self): 
        self.field_size = 150
        pyxel.init(self.field_size,self.field_size)#initは初期化
        pyxel.load('my_resource.pyxres')
        pyxel.sound(0).set(notes='E4C4', tones='TT', volumes='33', effects='NN', speed=15)
        pyxel.sound(1).set(notes='G1', tones='N', volumes='3', effects='N', speed=20)
        self.game_start()
        pyxel.run(self.update, self.draw)

        
    def game_start(self):
        self.balls = [Ball(self.field_size)]
        self.pad = Pad(self.field_size)
        self.alive = True
        self.life = 10
        self.receive = 0
        self.score = 0

    def update(self):##ボールの動きを処理
        if not self.alive:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.game_start()
            return
        self.pad.x = pyxel.mouse_x
        for b in self.balls:
            b.move()
        
            if self.pad.catch(b): #受け取れたら（受け取れた時の処理）
                b.restart()
                b.speed += 0.1
                self.score += 1
                self.receive += 1
                if self.receive >= 10:
                    b.speed = 2
                    self.receive = 0
                    self.balls.append(Ball(self.field_size))
                if b.type == 14:
                    self.score -= 3 #焼き芋をキャッチすると３点引かれる

            elif b.y >= self.field_size: #落とした
                if b.type in ITEMS_OK: # 食べていいものだと失敗
                    pyxel.play(0, 1)
                    b.restart()
                    b.speed += 0.2
                    self.life -= 1
                    self.alive = (self.life > 0)
                else: # 落としてもいい食べ物の場合はok
                    pyxel.play(0, 0)
                    b.restart()
        

    def draw(self):
        if self.alive:
            pyxel.cls(0) #背景色
            pyxel.bltm(0, 0, 0, 0, 0, 150, 150)
            for b in self.balls:
                #pyxel.circ(b.x, b.y, self.field_size/20, 6)
                if b.type == 0: #pudding NG
                    pyxel.blt(b.x,b.y,0,0,0,16,16,0)     
                elif b.type == 1: #donut NG
                    pyxel.blt(b.x,b.y,0,16,0,16,16,0)
                elif b.type == 2: #small rice OK
                    pyxel.blt(b.x,b.y,0,32,0,16,16,0)
                elif b.type == 3: #large rice NG
                    pyxel.blt(b.x,b.y,0,48,0,16,16,0)
                elif b.type == 4: #aice NG
                    pyxel.blt(b.x,b.y,0,0,16,16,16,0)
                elif b.type == 5: #small danngo NG
                    pyxel.blt(b.x,b.y,0,16,16,16,16,0)
                elif b.type == 6: #danngo NG
                    pyxel.blt(b.x,b.y,0,32,16,16,16,0)
                elif b.type == 7: #grape OK
                    pyxel.blt(b.x,b.y,0,48,16,16,16,0)
                elif b.type == 8: #tea OK
                    pyxel.blt(b.x,b.y,0,0,32,16,16,0)
                elif b.type == 9: #cola NG
                    pyxel.blt(b.x,b.y,0,16,32,16,16,0)
                elif b.type == 10: #raddish OK
                    pyxel.blt(b.x,b.y,0,32,32,16,16,0)
                elif b.type == 11: #carrot OK
                    pyxel.blt(b.x,b.y,0,48,32,16,16,0)
                elif b.type == 12: #fish OK
                    pyxel.blt(b.x,b.y,0,0,48,16,16,0)
                elif b.type == 13: #cherry OK
                    pyxel.blt(b.x,b.y,0,16,48,16,16,0)
                elif b.type == 14: #sweet poteto NG
                    pyxel.blt(b.x,b.y,0,32,48,16,16,0)
                
                
                
            pyxel.blt(self.pad.x-self.pad.size/2,self.field_size-16,0,48,48,16,16, 10)
            #pyxel.rect(self.pad.x-self.pad.size/2, self.field_size-self.field_size/40, self.pad.size, 5, 14)
            pyxel.text(5, 5, "score: " + str(self.score) + "  remaining lives: " + str(self.life), 0)
        else:
            pyxel.text(self.field_size/2-20, self.field_size/2-20, "Game Over!!!\nSPACE TO RESTART", 7)

App()
