import random
import os, pygame, sys
from pygame.locals import *
import spritesheet
import sound
import time as time1
import math
from monster import Monster
from map import Level
waiting = True
running = True
icon = pygame.image.load("Game.bmp")
icon.set_colorkey((0,0,0))
pygame.display.set_icon(icon)
level = Level()
level.loadFile("level0000.map")
pygame.init()
screen = pygame.display.set_mode((800, 600))
# Add a title
iconRect = icon.get_rect()
iconRect.centerx = screen.get_rect().centerx+10
iconRect.y=0
screen.blit(icon, iconRect)
font1 = pygame.font.Font(None, 72)
text1 = font1.render('PixelBuild', True, (255, 255, 255))
textRect1 = text1.get_rect()
textRect1.centerx = screen.get_rect().centerx
textRect1.y = 100
screen.blit(text1, textRect1)

# Add "Press <Enter> To Play"
font2 = pygame.font.Font(None, 17)
text2 = font2.render('Press <Enter> To Play', True, (255, 255, 255))
textRect2 = text2.get_rect()
textRect2.centerx = screen.get_rect().centerx
textRect2.y = 150
screen.blit(text2, textRect2)
pygame.display.set_caption('PixelBuild')
# Update the screen
pygame.display.update()
# Wait for enter to be pressed
# The user can also quit
while waiting:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         pygame.quit()
         waiting=False
         running=False
      elif event.type == pygame.KEYDOWN:
         if event.key == pygame.K_RETURN:
            waiting = False
if running:
    background = level.render(spritesheet.spritesheet("spritesheet.bmp"))
    pygame.display.set_caption('PixelBuild')
    character=spritesheet.spritesheet("spritesheet.bmp").image_at(pygame.rect.Rect(96,64, 32, 32), colorkey = (255, 255, 255))
    #Create The Backgound
    background.blit(character, (400, 300))
    screen.blit(background, (-100, -100))
    clock = pygame.time.Clock()
    pygame.display.flip()
    #spritesheet.spritesheet("spritesheet.bmp").image_at(pygame.Rect(32, 96, 32, 32))
    monsters=[]
    monsternum=10
    if level.monsters=={}:
        for i in range(monsternum):
            monsters.append(Monster(spritesheet.spritesheet("spritesheet.bmp").image_at(pygame.rect.Rect(96, 288, 32, 32), colorkey = (255, 255, 255)), 5, [random.randint(10, 900), random.randint(10, 1270)], level))
    else:
        for mon in level.monsters:
            monsters.append(Monster(spritesheet.spritesheet("spritesheet.bmp").image_at(pygame.rect.Rect(96, 288, 32, 32), colorkey = (255, 255, 255)), 5, [int(level.monsters[mon]["x"]), int(level.monsters[mon]["y"])], level))
    defaultmap="""
[level]
map = '''777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    777777777777777777777777777777
    
    '''
tileset = abc

[1]
name = wall
tile = 1, 1

[2]
name = wall
tile = 2, 1

[3]
name = wall
tile = 3, 1

[4]
name = wall
tile = 4, 1

[q]
name = pool
tile = 4, 8

[5]
name = wall
tile = 1, 2

[6]
name = wall
tile = 2, 2

[7]
name = floor
tile = 3, 2

[8]
name = wall
tile = 4, 2

[9]
name = wall
tile = 1, 3

[0]
name = wall
tile = 2, 3
                        """

    xoffset=0
    yoffset=0
    selected=""
    monsterspeed=7
    monsterdirection=random.randint(0,4)
    inv=[]
    inv=['1', '2', '3', '4', '5', '6', '7', '8', '9','0', 'q']
    currentselected=1
    def trunc(f, n):
        slen = len('%.*f' % (n, f))
        try:
            return int(str(f)[:slen])
        except:
            return int(str(f)[:slen-1])
    playerx=400
    playery=300
    chunk=(0,0,0,0)
    pygame.key.set_repeat(1,25)
    background = level.render(spritesheet.spritesheet("spritesheet.bmp"))
    currentbox=pygame.Surface((48, 64))
    currentbox.fill((255,255,255))
    running=True
    dead=False
while running:
    if dead:
        break
    time = pygame.time.get_ticks() 
    pygame.display.update()
    screen.fill(0)
    screen.blit(background, (0+xoffset, 0+yoffset))
    selected = spritesheet.spritesheet("spritesheet.bmp").image_at(pygame.rect.Rect(((int(level.key[str(inv[currentselected-1])]['tile'].split(", ")[0])-1)*32, (int(level.key[str(inv[currentselected-1])]['tile'].split(", ")[1])-1)*32, 32, 32)))
    currentbox.blit(selected, (8,24))
    font = pygame.font.Font(None, 13)

    # Render the text
    text = font.render('Currently', True, (0,0, 0), (255, 255, 255))
    text1 = font.render('Selected', True, (0,0, 0), (255, 255, 255))
    currentbox.blit(text, (4,4))
    currentbox.blit(text1, (8,14))
    screen.blit(currentbox, (0, 536))
    screen.blit(character, (400, 300))
    pygame.display.flip()
    if not dead:
        background.fill(0)
    chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
    for mon in monsters:
        if mon.update(time, 150, playerx, playery)==0:
            dead=True
    background = level.render(spritesheet.spritesheet("spritesheet.bmp"))
    for mon in monsters:
        background.blit(mon.image, (mon.rect[0],mon.rect[1]))

    for event in pygame.event.get():
        if event.type==QUIT:
            chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
            level.writeConfig("level"+"".join(chunk1)+".map", monsters)
            pygame.quit()
            running=False
            break
        elif event.type == KEYDOWN:
            if event.key == K_w:
                try:
                    if level.getTile(trunc((playerx+16)/32,0), trunc((playery+4)/32,0))["name"]=="floor":
                        yoffset+=5
                        playery-=5
                    elif level.getTile(trunc((playerx+16)/32,0), trunc((playery+4)/32,0))["name"]=="pool":
                        yoffset+=3
                        playery-=3
                except KeyError:
                    
                    #1280, -980, 2
                    screen.fill(0)
                    playery=1280
                    yoffset=-980
                    chunkb=chunk
                    if chunk[2]==0:
                        chunk=[chunk[0]+1, chunk[1], chunk[2], chunk[3]]
                    else:
                        chunk=[chunk[0], chunk[1], chunk[2]-1, chunk[3]]  
                    chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                    if os.path.exists("level"+"".join(chunk1)+".map")!=True:
                        open("level"+"".join(chunk1)+".map","w").write(defaultmap)
                        background = level.render(spritesheet.spritesheet("spritesheet.bmp"))
                        screen.blit(background, (0+xoffset, 0+yoffset))
                        screen.blit(character, (400, 300))
                        pygame.display.flip()
                    else:
                        chunk=chunkb
                        chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                        level.writeConfig("level"+"".join(chunk1)+".map", [])
                        if chunk[2]==0:
                            chunk=[chunk[0]+1, chunk[1], chunk[2], chunk[3]]
                        else:
                            chunk=[chunk[0], chunk[1], chunk[2]-1, chunk[3]]
                        chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                        level.loadFile("level"+"".join(chunk1)+".map")
                        background = level.render(spritesheet.spritesheet("spritesheet.bmp"))
                        screen.blit(background, (0+xoffset, 0+yoffset))
                        screen.blit(character, (400, 300))
                        pygame.display.flip()
                        
            if event.key == K_s:
                try:
                    if level.getTile(trunc((playerx+16)/32,0), trunc((playery+25)/32,0))["name"]=="floor":
                        yoffset-=5
                        playery+=5
                    elif level.getTile(trunc((playerx+16)/32,0), trunc((playery+25)/32,0))["name"]=="pool":
                        yoffset-=3
                        playery+=3
                except KeyError:
                    screen.fill(0)
                    playery=0
                    yoffset=300
                    chunkb=chunk
                    if chunk[0]==0:
                        chunk=[chunk[0], chunk[1], chunk[2]+1, chunk[3]]
                    else:
                        chunk=[chunk[0]-1, chunk[1], chunk[2], chunk[3]]  
                    chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                    if os.path.exists("level"+"".join(chunk1)+".map")!=True:
                        open("level"+"".join(chunk1)+".map","w").write(defaultmap)
                        level.loadFile("level"+"".join(chunk1)+".map")
                        background = level.render(spritesheet.spritesheet("spritesheet.bmp"))
                        screen.blit(background, (0+xoffset, 0+yoffset))
                        screen.blit(character, (400, 300))
                        pygame.display.flip()
                    else:
                        chunk=chunkb
                        chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                        
                        level.writeConfig("level"+"".join(chunk1)+".map", [])
                        if chunk[0]==0:
                            chunk=[chunk[0], chunk[1], chunk[2]+1, chunk[3]]
                        else:
                            chunk=[chunk[0]-1, chunk[1], chunk[2], chunk[3]]
                        chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                        level.loadFile("level"+"".join(chunk1)+".map")
                        background = level.render(spritesheet.spritesheet("spritesheet.bmp"))
                        screen.blit(background, (0+xoffset, 0+yoffset))
                        screen.blit(character, (400, 300))
                        pygame.display.flip()
            if event.key == K_a:
                if level.getTile(trunc((playerx+12)/32,0), trunc((playery+16)/32,0))["name"]=="floor" and playerx>-5:
                    playerx-=5
                    xoffset+=5
                elif level.getTile(trunc((playerx+12)/32,0), trunc((playery+16)/32,0))["name"]=="pool":
                    xoffset+=3
                    playerx-=3
                if playerx<=-5:
                    screen.fill(0)
                    #Figure out xoffset
                    playerx=900
                    xoffset=-496
                    chunkb=chunk
                    if chunk[3]==0:
                        chunk=[chunk[0], chunk[1]+1, chunk[2], chunk[3]]
                    else:
                        chunk=[chunk[0], chunk[1], chunk[2], chunk[3]-1]  
                    chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                    if os.path.exists("level"+"".join(chunk1)+".map")!=True:
                        open("level"+"".join(chunk1)+".map","w").write(defaultmap)
                        level.loadFile("level"+"".join(chunk1)+".map")
                        background = level.render(spritesheet.spritesheet("spritesheet.bmp"))
                        screen.blit(background, (0+xoffset, 0+yoffset))
                        screen.blit(character, (400, 300))
                        pygame.display.flip()
                    else:
                        chunk=chunkb
                        chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                        level.writeConfig("level"+"".join(chunk1)+".map", [])
                        if chunk[3]==0:
                            chunk=[chunk[0], chunk[1]+1, chunk[2], chunk[3]]
                        else:
                            chunk=[chunk[0], chunk[1], chunk[2], chunk[3]-1]
                        chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                        level.loadFile("level"+"".join(chunk1)+".map")
                        background = level.render(spritesheet.spritesheet("spritesheet.bmp"))
                        screen.blit(background, (0+xoffset, 0+yoffset))
                        screen.blit(character, (400, 300))
                        pygame.display.flip()
            if event.key == K_d:
                try:
                    if level.getTile(trunc((playerx+25)/32,0), trunc((playery+16)/32,0))["name"]=="floor" and playerx<40*32:
                        xoffset-=5
                        playerx+=5
                    elif level.getTile(trunc((playerx+25)/32,0), trunc((playery+16)/32,0))["name"]=="pool":
                        xoffset-=3
                        playerx+=3
                except KeyError:
                    screen.fill(0)
                    #Figure out xoffset
                    playerx=0
                    xoffset=400
                    chunkb=chunk
                    if chunk[1]==0:
                        chunk=[chunk[0], chunk[1], chunk[2], chunk[3]+1]
                    else:
                        chunk=[chunk[0], chunk[1]-1, chunk[2], chunk[3]]  
                    chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                    if os.path.exists("level"+"".join(chunk1)+".map")!=True:
                        open("level"+"".join(chunk1)+".map","w").write(defaultmap)
                        level.loadFile("level"+"".join(chunk1)+".map")
                        background = level.render(spritesheet.spritesheet("spritesheet.bmp"))
                        screen.blit(background, (0+xoffset, 0+yoffset))
                        screen.blit(character, (400, 300))
                        pygame.display.flip()
                    else:
                        chunk=chunkb
                        chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                        level.writeConfig("level"+"".join(chunk1)+".map", [])
                        if chunk[1]==0:
                            chunk=[chunk[0], chunk[1], chunk[2], chunk[3]+1]
                        else:
                            chunk=[chunk[0], chunk[1]-1, chunk[2], chunk[3]]
                        chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                        level.loadFile("level"+"".join(chunk1)+".map")
                        background = level.render(spritesheet.spritesheet("spritesheet.bmp"))
                        screen.blit(background, (0+xoffset, 0+yoffset))
                        screen.blit(character, (400, 300))
                        pygame.display.flip()
            if event.key == K_1:
                currentselected=1
            if event.key == K_2:
                currentselected=2
            if event.key == K_3:
                currentselected=3
            if event.key == K_4:
                currentselected=4
            if event.key == K_5:
                currentselected=5
            if event.key == K_6:
                currentselected=6
            if event.key == K_7:
                currentselected=7
            if event.key == K_8:
                currentselected=8
            if event.key == K_9:
                currentselected=9
            if event.key == K_0:
                currentselected=0
        #4 is down and 5 is up
        if event.type == MOUSEBUTTONDOWN and event.button==4:
            if currentselected==0:
                currentselected=11
            else:
                currentselected-=1
        elif event.type == MOUSEBUTTONDOWN and event.button==5:
            if currentselected==11:
                currentselected=0
            else:
                currentselected+=1
        elif event.type==MOUSEBUTTONDOWN and event.button==1:
            mouse=[pygame.mouse.get_pos()[0]-400, pygame.mouse.get_pos()[1]-300]
            level.setTile(trunc(((mouse[0]*1.0/32))+playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+playery*1.0/32,0), str(inv[currentselected-1]))
            background = level.render(spritesheet.spritesheet("spritesheet.bmp"))
            screen.blit(background, (0+xoffset, 0+yoffset))
        elif event.type==MOUSEBUTTONDOWN and event.button==3:
            mouse=[pygame.mouse.get_pos()[0]-400, pygame.mouse.get_pos()[1]-300]
            level.setTile(trunc(((mouse[0]*1.0/32))+playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+playery*1.0/32,0), "7")
            background = level.render(spritesheet.spritesheet("spritesheet.bmp"))
            screen.blit(background, (0+xoffset, 0+yoffset))
once = 1
while 1:
    if once>0:
        n =  screen.convert_alpha()
        # red at 50%
        n.fill((255,0,0,127))
        screen.blit(n, (0,0))
        pygame.display.flip()
        once-=1
    font1 = pygame.font.Font(None, 72)
    text1 = font1.render('Game Over', True, (255, 255, 255))
    textRect1 = text1.get_rect()
    textRect1.centerx = screen.get_rect().centerx
    textRect1.y = 100
    screen.blit(text1, textRect1)

    # Add "Press <Enter> To Play"
    font2 = pygame.font.Font(None, 17)
    text2 = font2.render('Press <Enter> To Quit', True, (255, 255, 255))
    textRect2 = text2.get_rect()
    textRect2.centerx = screen.get_rect().centerx
    textRect2.y = 150
    screen.blit(text2, textRect2)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==QUIT:
            chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
            level.writeConfig("level"+"".join(chunk1)+".map", monsters, False)
            pygame.quit()
            running=False
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
                level.writeConfig("level"+"".join(chunk1)+".map", monsters, False)
                pygame.quit()
                running=False
                sys.exit()