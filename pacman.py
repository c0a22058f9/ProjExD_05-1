#Pacman in Python with PyGame
#https://github.com/hbokmann/Pacman
  
import pygame
import random

  
black = (0,0,0) #黒
white = (255,255,255) #白
blue = (0,0,255) #青
green = (0,255,0) #緑
red = (255,0,0) #赤
purple = (255,0,255) #紫
yellow   = ( 255, 255,   0) #黄
kkk = 1

Trollicon=pygame.image.load('images/pacman.png') #pacmanの画像を読み込む
pygame.display.set_icon(Trollicon) #ウィンドウに表示されるシステムアイコンを変更します。

#Add music
pygame.mixer.init() #mixerモジュールを初期化します
pygame.mixer.music.load('pacman.mp3') #音楽ファイルの読み込み
pygame.mixer.music.play(-1, 0.0) #音楽の再生引数-1で永遠に繰り返される。pygame.mixer.music.play(loops=0, start=0.0): return None

# This class represents the bar at the bottom that the player controls
class Wall(pygame.sprite.Sprite): #定の画像をゲーム画面に表示するためのシンプルな基底クラス
    # Constructor function
    def __init__(self,x,y,width,height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self) #特定の画像をゲーム画面に表示するためのシンプルな基底クラス
  
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height]) #画像を描写するために使用するpygameのクラス
        self.image.fill(color) #color塗りつぶす
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect() #
        self.rect.top = y #左上y座標
        self.rect.left = x #左上x座標

# This creates all the walls in room 1
def setupRoomOne(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list=pygame.sprite.RenderPlain() #壁でマップを作成するリスト
     
    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = [ [-30,-30,36,630],  #左
              [-30,-30,630,36],  #上
              [-30,600,660,36],  #右
              [600,-30,36,660],  #下
              [300,0,6,66],
              [60,60,186,6],
              [360,60,186,6],
              [60,120,66,6],
              [60,120,6,126],
              [180,120,246,6],
              [300,120,6,66],
              [480,120,66,6],
              [540,120,6,126],
              [120,180,126,6],
              [120,180,6,126],
              [360,180,126,6],
              [480,180,6,126],
              [180,240,6,126],
              [180,360,246,6],
              [420,240,6,126],
              [240,240,42,6],
              [324,240,42,6],
              [240,240,6,66],
              [240,300,126,6],
              [360,240,6,66],
              [0,300,66,6],
              [540,300,66,6],
              [60,360,66,6],
              [60,360,6,186],
              [480,360,66,6],
              [540,360,6,186],
              [120,420,366,6],
              [120,420,6,66],
              [480,420,6,66],
              [180,480,246,6],
              [300,480,6,66],
              [120,540,126,6],
              [360,540,126,6],

              #[200,400,6,20],
              
              

            ]
     
    # Loop through the list. Create the wall, add it to the list
    #リストをループします。壁を作成し、リストに追加します
    for item in walls:
        wall=Wall(item[0],item[1],item[2],item[3],blue)
        #item[0]: x 座標,item[1]: y 座標,item[2]: 幅 (width),item[3]: 高さ (height),bule(0, 0, 255)を使用
        wall_list.add(wall) #wall_listにマップの情報を追加
        all_sprites_list.add(wall) #all_sprites_listにもマップの情報を追加
         
    # return our new list
    return wall_list

def setupGate(all_sprites_list):
      #ゴーストが出てくるゲートのセットアップ
      gate = pygame.sprite.RenderPlain()
      gate.add(Wall(282,242,42,2,white))
      all_sprites_list.add(gate)
      return gate

# This class represents the ball        
# It derives from the "Sprite" class in Pygame
# このクラスはボールを表します
# Pygame の「Sprite」クラスから派生します
class Block(pygame.sprite.Sprite):
     
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    # コンストラクター。ブロックの色を渡し、
    # とその x 位置と y 位置
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        # ブロックの画像を作成し、色で塗りつぶします。
        # これはディスクからロードされたイメージである可能性もあります。
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image,color,[0,0,width,height])
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect() #self.imageの短形領域を取得しますこれにより、ブロックの位置や衝突判定に使用される矩形情報を取得します。

# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
  
    # Set speed vector
    change_x=0
    change_y=0
  #change_x と change_y はプレイヤーの移動速度を表す変数です。初期値として 0 を設定しています。


    # Constructor function
    def __init__(self,x,y, filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
   
        # Set height, width
        self.image = pygame.image.load(filename).convert()
        # pygame.image.load(filename).convert() を使用して画像を読み込みます。convert() メソッドは画像のピクセルフォーマットを変換し、描画速度を向上させます。
        # Make our top-left corner the passed-in location.
        #左上隅を渡された場所にします。
        self.rect = self.image.get_rect() #self.rect には画像の矩形領域が格納されます。
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    # Clear the speed of the player
    # prevdirection メソッドは、プレイヤーの速度をクリアします。現在の速度を self.prev_x と self.prev_y に保存します。
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change the speed of the player
    # changespeed メソッドは、プレイヤーの速度を変更します。x と y を現在の速度に加算します。
    def changespeed(self,x,y):
        self.change_x+=x
        self.change_y+=y
          
    # Find a new position for the player
    def update(self,walls,gate):
        # Get the old position, in case we need to go back to it
        
        old_x=self.rect.left
        new_x=old_x+self.change_x
        prev_x=old_x+self.prev_x
        self.rect.left = new_x
        
        old_y=self.rect.top
        new_y=old_y+self.change_y
        prev_y=old_y+self.prev_y


        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.left=old_x
            # self.rect.top=prev_y
            # y_collide = pygame.sprite.spritecollide(self, walls, False)
            # if y_collide:
            #     # Whoops, hit a wall. Go back to the old position
            #     self.rect.top=old_y
            #     print('a')
        else:

            self.rect.top = new_y

            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top=old_y
                # self.rect.left=prev_x
                # x_collide = pygame.sprite.spritecollide(self, walls, False)
                # if x_collide:
                #     # Whoops, hit a wall. Go back to the old position
                #     self.rect.left=old_x
                #     print('b')

        if gate != False:
          gate_hit = pygame.sprite.spritecollide(self, gate, False)
          if gate_hit:
            self.rect.left=old_x
            self.rect.top=old_y
    def teleport(self, width, height):
      """
      テレポート機能に関するメソッド
      引数1:ランダムな位置の幅の範囲
      引数2:ランダムな位置の高さの範囲
      """
      while True:
        self.rect.x = random.randrange(18, width-30, 30)  #通路の真ん中にpacmanが来るように最低値を18に設定
        self.rect.y = random.randrange(18, height-30, 30)
        if not((self.rect.x >= 258 and self.rect.x <= 348)\
          and (self.rect.y == 258)):  #迷路の真ん中にある小部屋に入らないための条件分岐
          break

#Inheritime Player klassist
#class Ghost(Player):
    

#Inheritime Player klassist
class Ghost(Player):
    def update(self,walls,gate):
        # Get the old position, in case we need to go back to it
        if kkk > 0:
          old_x=self.rect.left
          new_x=old_x+self.change_x
          prev_x=old_x+self.prev_x
          self.rect.left = new_x
          
          old_y=self.rect.top
          new_y=old_y+self.change_y
          prev_y=old_y+self.prev_y
          

          # Did this update cause us to hit a wall?
          x_collide = pygame.sprite.spritecollide(self, walls, False)
          if x_collide:
              # Whoops, hit a wall. Go back to the old position
              self.rect.left=old_x
              # self.rect.top=prev_y
              # y_collide = pygame.sprite.spritecollide(self, walls, False)
              # if y_collide:
              #     # Whoops, hit a wall. Go back to the old position
              #     self.rect.top=old_y
              #     print('a')
          else:

              self.rect.top = new_y

              # Did this update cause us to hit a wall?
              y_collide = pygame.sprite.spritecollide(self, walls, False)
              if y_collide:
                  # Whoops, hit a wall. Go back to the old position
                  self.rect.top=old_y
                  # self.rect.left=prev_x
                  # x_collide = pygame.sprite.spritecollide(self, walls, False)
                  # if x_collide:
                  #     # Whoops, hit a wall. Go back to the old position
                  #     self.rect.left=old_x
                  #     print('b')

          if gate != False:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
              self.rect.left=old_x
              self.rect.top=old_y
       
    # Change the speed of the ghost
    

    #ここの下がどうなってるのかわからない

          # ゴーストの移動処理
          #ghost.changespeed(list, ghost, turn, steps, l, k)

    def changespeed(self,list,ghost,turn,steps,l):
      #print(f"list:{list}, ghost:{ghost}, turn:{turn}, step:{steps}, l:{l}")
      #list は移動のリスト、ghost はゴーストの種類、turn は現在の方向のインデックス、
      # steps は現在の方向のステップ数、l は移動リストの最後のインデックスです
      #ゴーストは同じ場所をループしてる
      try:
        z=list[turn][2] #リストの3つ目の値
        #turnは多分方向転換のためのおっきいほうのリスト
        
        if steps < z:
          if kkk > 0:          #kkkが1だったらkkkは（0or1）
             self.change_x=list[turn][0] #リストの0つ目の値 playerの速度をリストの0つ目にする
             self.change_y=list[turn][1] #リストの1つ目の値 playerの速度をリストの1つ目にする
             steps+=1
          

        
        else:
            if turn < l: #おっきいほうのリストがラストじゃなかったら
              turn+=kkk #リストのインデックスを１大きくする   ココが変わらなかったらゴーストは動かない
            elif ghost == "clyde":#茶色いゴーストだったら
              turn = 2 #２のインデックスにする
            else:
              turn = 0 #リストを最初からにして
            self.change_x=list[turn][0]
            self.change_y=list[turn][1]
            steps = 0
        
        return [turn,steps]
      except IndexError:
         return [0,0]
    
                  
         

Pinky_directions =[
[0,-30,4],    #下に4回進む
[15,0,9],     #右に9回進む
[0,15,11],    #上に11回進む
[-15,0,23],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,19],
[0,15,3],
[15,0,3],
[0,15,3],
[15,0,3],
[0,-15,15],
[-15,0,7],
[0,15,3],
[-15,0,19],
[0,-15,11],
[15,0,9]
]

Blinky_directions = [
[0,-15,4],
[15,0,9],
[0,15,11],
[15,0,3],
[0,15,7],
[-15,0,11],
[0,15,3],
[15,0,15],
[0,-15,15],
[15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,11],
[-15,0,3],
[0,-15,3],
[-15,0,7],
[0,-15,3],
[15,0,15],
[0,15,15],
[-15,0,3],
[0,15,3],
[-15,0,3],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,11],
[0,-15,7],
[15,0,5]
]

Inky_directions = [
[30,0,2],
[0,-15,4],
[15,0,10],
[0,15,7],
[15,0,3],
[0,-15,3],
[15,0,3],
[0,-15,15],
[-15,0,15],
[0,15,3],
[15,0,15],
[0,15,11],
[-15,0,3],
[0,-15,7],
[-15,0,11],
[0,15,3],
[-15,0,11],
[0,15,7],
[-15,0,3],
[0,-15,3],
[-15,0,3],
[0,-15,15],
[15,0,15],
[0,15,3],
[-15,0,15],
[0,15,11],
[15,0,3],
[0,-15,11],
[15,0,11],
[0,15,3],
[15,0,1],
]

Clyde_directions = [
[-30,0,2],
[0,-15,4],
[15,0,5],
[0,15,7],
[-15,0,11],
[0,-15,7],
[-15,0,3],
[0,15,7],
[-15,0,7],
[0,15,15],
[15,0,15],
[0,-15,3],
[-15,0,11],
[0,-15,7],
[15,0,3],
[0,-15,11],
[15,0,9],
]

pl = len(Pinky_directions)-1 #17
bl = len(Blinky_directions)-1 #27
il = len(Inky_directions)-1 #30
cl = len(Clyde_directions)-1 #16

# Call this function so the Pygame library can initialize itself
pygame.init()
  
# Create an 606x606 sized screen
screen = pygame.display.set_mode([606, 606]) #display描写用のウィンドウやスクリーンを初期化します。

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'RenderPlain.'


# Set the title of the window
pygame.display.set_caption('Pacman') #ウィンドウのタイトルを設定します。

# Create a surface we can draw on
background = pygame.Surface(screen.get_size()) #画像のピクセル形式を変更する

# Used for converting color maps and such
background = background.convert()
  
# Fill the screen with a black background
background.fill(black)



clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

#default locations for Pacman and monstas
w = 303-16 #Width
p_h = (7*60)+19 #Pacman height
m_h = (4*60)+19 #Monster height
b_h = (3*60)+19 #Binky height
i_w = 303-16-32 #Inky width
c_w = 303+(32-16) #Clyde width

def startGame():
  global kkk 
  stop_life = -1

  all_sprites_list = pygame.sprite.RenderPlain()

  block_list = pygame.sprite.RenderPlain()

  monsta_list = pygame.sprite.RenderPlain()

  pacman_collide = pygame.sprite.RenderPlain()

  wall_list = setupRoomOne(all_sprites_list)

  gate = setupGate(all_sprites_list)


  p_turn = 0
  p_steps = 0

  b_turn = 0
  b_steps = 0

  i_turn = 0
  i_steps = 0

  c_turn = 0
  c_steps = 0


  # Create the player paddle object
  Pacman = Player( w, p_h, "images/pacman.png" )
  all_sprites_list.add(Pacman)
  pacman_collide.add(Pacman)
   
  Blinky=Ghost( w, b_h, "images/Blinky.png" )
  monsta_list.add(Blinky)
  all_sprites_list.add(Blinky)

  Pinky=Ghost( w, m_h, "images/Pinky.png" )
  monsta_list.add(Pinky)
  all_sprites_list.add(Pinky)
   
  Inky=Ghost( i_w, m_h, "images/Inky.png" )
  monsta_list.add(Inky)
  all_sprites_list.add(Inky)
   
  Clyde=Ghost( c_w, m_h, "images/Clyde.png" )
  monsta_list.add(Clyde)
  all_sprites_list.add(Clyde)

  # Draw the grid
  for row in range(19):
      for column in range(19):
          if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
              continue
          else:
            block = Block(yellow, 4, 4)

            # Set a random location for the block
            block.rect.x = (30*column+6)+26
            block.rect.y = (30*row+6)+26

            b_collide = pygame.sprite.spritecollide(block, wall_list, False)
            p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)
            if b_collide:
              continue
            elif p_collide:
              continue
            else:
              # Add the block to the list of objects
              block_list.add(block)
              all_sprites_list.add(block)

  bll = len(block_list)

  score = 0

  done = False

  i = 0

  t_flag = False   # トロールのフラグ

  while done == False:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              done=True

          if event.type == pygame.KEYDOWN:
              if event.key == pygame.K_LEFT:
                  if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                      Pacman.changespeed(-60, 0)  # LSHIFTキーを押しながら左キーでスピード増加
                  else:
                      Pacman.changespeed(-30, 0)
              elif event.key == pygame.K_RIGHT:
                  if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                      Pacman.changespeed(60, 0)  # LSHIFTキーを押しながら右キーでスピード増加
                  else:
                      Pacman.changespeed(30, 0)
              elif event.key == pygame.K_UP:
                  if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                      Pacman.changespeed(0, -60)  # LSHIFTキーを押しながら上キーでスピード増加
                  else:
                      Pacman.changespeed(0, -30)
              elif event.key == pygame.K_DOWN:
                  if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                      Pacman.changespeed(0, 60)  # LSHIFTキーを押しながら下キーでスピード増加
                  else:
                      Pacman.changespeed(0, 30)
              if event.key == pygame.K_j:
                  if t_flag == False:
                    for i in range(10):
                      Troll=Ghost( (i*60+19), (i*60+19) , "images/Trollman.png" )
                      monsta_list.add(Troll)
                      all_sprites_list.add(Troll)
                  
                      Troll=Ghost( 2*w-(i*60+19), (i*60+19) , "images/Trollman.png" )
                      monsta_list.add(Troll)
                      all_sprites_list.add(Troll)
                    t_flag = True
                  
                  else:
                    for i in range(20):
                      monsta_list.remove(monsta_list.sprites()[-1])
                      all_sprites_list.remove(all_sprites_list.sprites()[-1])
                    t_flag = False

          if event.type == pygame.KEYUP:
              if event.key == pygame.K_LEFT:
                  if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                      Pacman.changespeed(60, 0)  # LSHIFTキーを押しながら左キーを離すとスピード減少
                  else:
                      Pacman.changespeed(30, 0)  # 左キーを離すとY方向の速度をそのままにする
              elif event.key == pygame.K_RIGHT:
                  if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                      Pacman.changespeed(-60, 0)  # LSHIFTキーを押しながら右キーを離すとスピード減少
                  else:
                      Pacman.changespeed(-30, 0)  # 右キーを離すとY方向の速度をそのままにする
              elif event.key == pygame.K_UP:
                  if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                      Pacman.changespeed(0, 60)  # LSHIFTキーを押しながら上キーを離すとスピード減少
                  else:
                      Pacman.changespeed(0, 30)  # 上キーを離すとX方向の速度をそのままにする
              elif event.key == pygame.K_DOWN:
                  if pygame.key.get_mods() & pygame.KMOD_LSHIFT:
                      Pacman.changespeed(0, -60)  # LSHIFTキーを押しながら下キーを離すとスピード減少
                  else:
                      Pacman.changespeed(0, -30)  # 下キーを離すとX方向の速度をそのままにする

              if event.key == pygame.K_t:  #Tキーが押されたときの処理（テレポート）
                  while True:
                     Pacman.teleport(screen.get_width(), screen.get_height())  #テレポート位置を画面の幅と高さのランダムな位置に指定
                     pac_collide = pygame.sprite.spritecollide(Pacman, wall_list, False)  #pacmanと壁の衝突判定
                     pg_collide = pygame.sprite.spritecollide(Pacman, gate, False)  #pacmanと扉の衝突判定
                     if (not pac_collide) and (not pg_collide):  #壁と扉に当たっていなければbreak、そうでなければ繰り返す
                        break

              if event.key == pygame.K_SPACE:
                if score >= 40:             #もしスコアが40以上だったら              ##ゲーム中にキーボードを押したら
                    score -= 40             #スコアを40消費する
                    kkk = 0
                    stop_life = 50           #stop_lifeを50にする



      # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
   
      # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
      Pacman.update(wall_list,gate)
      if stop_life > 0:
        stop_life -= 1
      else:
         kkk = 1
      
      if score <= 200:
         type_ = False
      elif score > 200:
         type_ = True

#clyde以外type_がFalseになってる

      returned = Pinky.changespeed(Pinky_directions,type_,p_turn,p_steps,pl)
      p_turn = returned[0]
      p_steps = returned[1]
      Pinky.changespeed(Pinky_directions,False,p_turn,p_steps,pl)
      Pinky.update(wall_list,False)

      returned = Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl)
      b_turn = returned[0]
      b_steps = returned[1]
      Blinky.changespeed(Blinky_directions,False,b_turn,b_steps,bl)
      Blinky.update(wall_list,False)

      returned = Inky.changespeed(Inky_directions,False,i_turn,i_steps,il)
      i_turn = returned[0]
      i_steps = returned[1]
      Inky.changespeed(Inky_directions,False,i_turn,i_steps,il)
      Inky.update(wall_list,False)

      returned = Clyde.changespeed(Clyde_directions,"clyde",c_turn,c_steps,cl)
      c_turn = returned[0]
      c_steps = returned[1]
      Clyde.changespeed(Clyde_directions,"clyde",c_turn,c_steps,cl)
      Clyde.update(wall_list,False)

      # See if the Pacman block has collided with anything.
      blocks_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)
       
      # Check the list of collisions.
      if len(blocks_hit_list) > 0:
          score +=len(blocks_hit_list)
      
      # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
   
      # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
      screen.fill(black)
        
      wall_list.draw(screen)
      gate.draw(screen)
      all_sprites_list.draw(screen)
      monsta_list.draw(screen)

      text=font.render("Score: "+str(score)+"/"+str(bll), True, red)
      screen.blit(text, [10, 10])

      nums = []       # 奇数×10の数が入る空リストを作成
      nums1 = []      # 奇数×10の数が入る空リストを作成
      for i in range(22): #偶数、奇数のリストにそれぞれ分類する
         if i%2 ==0:
            nums1.append(i*10)
         else:
            nums.append(i*10)
      # print(nums, nums1)
      for i in range(len(nums)):   
        if score > nums1[i] and score < nums[i]:  #関数draw_rectを呼び出す条件
          draw_rect(screen, score, i)



      if score == bll:
        doNext("Congratulations, you won!",145,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)

      monsta_hit_list = pygame.sprite.spritecollide(Pacman, monsta_list, False)

      if monsta_hit_list:
        doNext("Game Over",235,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate)

      # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
      
      pygame.display.flip()
    
      clock.tick(10)

#投下画像を呼び出す関数
def draw_rect(screen, score, i):
  if i < 5:
    pygame.draw.rect(screen, (0, 0, 0), (score*i, score/2, 100, 100*score))
  else:
    pygame.draw.rect(screen, (0, 0, 0), (score*(i*0.01), score, 100, 100*score))


def doNext(message,left,all_sprites_list,block_list,monsta_list,pacman_collide,wall_list,gate):
  while True:
      # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()


        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            pygame.quit()

        

          if event.key == pygame.K_RETURN:
            del all_sprites_list
            del block_list
            del monsta_list
            del pacman_collide
            del wall_list
            del gate
            startGame()

      #Grey background
      w = pygame.Surface((400,200))  # the size of your rect
      w.set_alpha(10)                # alpha level
      w.fill((128,128,128))           # this fills the entire surface
      screen.blit(w, (100,200))    # (0,0) are the top-left coordinates

      #Won or lost
      text1=font.render(message, True, white)
      screen.blit(text1, [left, 233])

      text2=font.render("To play again, press ENTER.", True, white)
      screen.blit(text2, [135, 303])
      text3=font.render("To quit, press ESCAPE.", True, white)
      screen.blit(text3, [165, 333])

      pygame.display.flip()

      clock.tick(10)

startGame()

pygame.quit()