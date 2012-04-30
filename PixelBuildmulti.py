import random
import os, pygame, sys
from pygame.locals import *
import spritesheet
import sound
import math
import client
import time as time1
from monster import Monster
from map import Level
def find(f, seq):
    i=0
    for item in seq:
        if item==f: 
            return i
        i+=1
pygame.mixer.init()
waiting = True
running = True
coins=0
c=client.Client(sys.argv[0].split(":")[0], sys.argv[0].split(":")[1])
placesound=pygame.mixer.Sound("place.wav")
deletesound=pygame.mixer.Sound("delete.wav")
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
counter=100
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
    background.set_colorkey((255, 255, 255))
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
    defaultmap=open("default.map", "r").read()
    xoffset=0
    yoffset=0
    selected=""
    monsterspeed=7
    monsterdirection=random.randint(0,4)
    inv=[]
    inv=['1', '2', '3', '4', '5', '6','7', '8', '9','0', 'q', 'b', 't', 'i', 'd', 'g', 'tr']
    invcount=[100, 100,100, 100,100, 100, 100,100, 100,100, 10000,20000, 100, 100, 100, 100, 100]
    currentselected=1
    currentselectednum=invcount[currentselected-1]
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
    background.set_colorkey((255, 255, 255))
    currentbox=pygame.Surface((48, 64))
    currentbox.fill((255,255,255))
    running=True
    dead=False
    c.Loop()

while running:
    c.Loop()
    if len(c.blockdata)>1:
        level.setTile(c.blockdata['data'][0], c.blockdata['data'][1], c.blockdata['data'][2])
    currentbox.fill((255,255,255))
    currentselectednum=invcount[currentselected-1]
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
    text2 = font.render(str(currentselectednum), True, (0,0, 0), (255, 255, 255))
    currentbox.blit(text, (4,4))
    currentbox.blit(text1, (8,14))
    text2.set_colorkey((255, 255, 255))
    currentbox.blit(text2, (20 ,56))

    screen.blit(currentbox, (0, 536))
    screen.blit(character, (400, 300))
    pygame.display.flip()
    if not dead:
        background.fill(0)
    chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
    for mon in monsters:
        monsterstat=mon.update(time, 150, playerx, playery)
        if monsterstat==0:
            dead=True
        elif monsterstat==1:
            coins+=2
            print coins
        
    
    background = level.render(spritesheet.spritesheet("spritesheet.bmp"))
    background.set_colorkey((255, 255, 255))
    for mon in monsters:
        background.blit(mon.image, (mon.rect[0],mon.rect[1]))

    for event in pygame.event.get():
        if event.type==QUIT:
            chunk1=[str(chunk[0]), str(chunk[1]), str(chunk[2]), str(chunk[3])]
            level.writeConfig("level"+"".join(chunk1)+".map", monsters)
            pygame.quit()
            running=False
            sys.exit()
            break
        elif event.type == KEYDOWN:
            if event.key == K_w:
                if playery>0:
                    if level.getTile(trunc((playerx+16)/32,0), trunc((playery+4)/32,0))["name"]=="floor":
                        yoffset+=5
                        playery-=5
                    elif level.getTile(trunc((playerx+16)/32,0), trunc((playery+4)/32,0))["name"]=="pool":
                        yoffset+=3
                        playery-=3
                else:
                    level.writeConfig("level"+"".join(chunk1)+".map", monsters)
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
                    print "level"+"".join(chunk1)+".map"
                    if os.path.exists("level"+"".join(chunk1)+".map")!=True:
                        open("level"+"".join(chunk1)+".map","w").write(defaultmap)
                        level.loadFile("level"+"".join(chunk1)+".map")
                        background = level.render(spritesheet.spritesheet("spritesheet.bmp"))
                        background.set_colorkey((255, 255, 255))
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
                        background.set_colorkey((255, 255, 255))
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
                    level.writeConfig("level"+"".join(chunk1)+".map", monsters)
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
                        background.set_colorkey((255, 255, 255))
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
                        background.set_colorkey((255, 255, 255))
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
                    level.writeConfig("level"+"".join(chunk1)+".map", monsters)
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
                        background.set_colorkey((255, 255, 255))
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
                        background.set_colorkey((255, 255, 255))
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
                    level.writeConfig("level"+"".join(chunk1)+".map", monsters)
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
                        background.set_colorkey((255, 255, 255))
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
                        background.set_colorkey((255, 255, 255))
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
                currentselected=len(inv)
            else:
                currentselected-=1
        elif event.type == MOUSEBUTTONDOWN and event.button==5:
            if currentselected==len(inv):
                currentselected=0
            else:
                currentselected+=1
        elif event.type==MOUSEBUTTONDOWN and event.button==1:
            if invcount[currentselected-1]>0:
                placesound.play()
                mouse=[pygame.mouse.get_pos()[0]-400, pygame.mouse.get_pos()[1]-300]
                try:
                    if level.getTile(trunc(((mouse[0]*1.0/32))+playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+playery*1.0/32,0))["name"]=="floor":
    #Traceback (most recent call last):
    #   File "/Users/jmeyer2k/Desktop/PixelBuild/Development/PixelBuild.py", line 376, in <module>
    #     if level.getTile(trunc(((mouse[0]*1.0/32))+playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+playery*1.0/32,0))["name"]=="floor":
    # KeyError: 'name'
                        if level.getTile(trunc(((mouse[0]*1.0/32))+playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+playery*1.0/32,0), False)!=inv[currentselected-1]:
                            level.setTile(trunc(((mouse[0]*1.0/32))+playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+playery*1.0/32,0), str(inv[currentselected-1]))
                            c.newdata={"action":"placeblock", "data":[trunc(((mouse[0]*1.0/32))+playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+playery*1.0/32,0), str(inv[currentselected-1])]}
                            background = level.render(spritesheet.spritesheet("spritesheet.bmp"))
                            background.set_colorkey((255, 255, 255))
                            screen.blit(background, (0+xoffset, 0+yoffset))
                            screen.blit(currentbox, (0, 536))
                            screen.blit(character, (400, 300))
                            invcount[currentselected-1]-=1
                            for mon in monsters:
                                background.blit(mon.image, (mon.rect[0],mon.rect[1]))
                            pygame.display.flip()

                except:
                    pass 
        elif event.type==MOUSEBUTTONDOWN and event.button==3:
            try:
                deletesound.play()
                mouse=[pygame.mouse.get_pos()[0]-400, pygame.mouse.get_pos()[1]-300]
                invcount[find(level.getTile(trunc(((mouse[0]*1.0/32))+playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+playery*1.0/32,0), False), inv)]+=1
                if level.getTile(trunc(((mouse[0]*1.0/32))+playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+playery*1.0/32,0))['name']!='floor':
                    level.setTile(trunc(((mouse[0]*1.0/32))+playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+playery*1.0/32,0), "g")
                    c.newdata={"action":"placeblock", "data":[trunc(((mouse[0]*1.0/32))+playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+playery*1.0/32,0), "g"]}
                else:
                    level.setTile(trunc(((mouse[0]*1.0/32))+playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+playery*1.0/32,0), "7")
                    c.newdata={"action":"placeblock", "data":[trunc(((mouse[0]*1.0/32))+playerx*1.0/32, 0), trunc(((mouse[1]*1.0/32))+playery*1.0/32,0), "7"]}            
                background = level.render(spritesheet.spritesheet("spritesheet.bmp"))
                background.set_colorkey((255, 255, 255))
                screen.blit(background, (0+xoffset, 0+yoffset))
                screen.blit(currentbox, (0, 536))
                screen.blit(character, (400, 300))
                for mon in monsters:
                    background.blit(mon.image, (mon.rect[0],mon.rect[1]))
                pygame.display.flip()
            except:
                pass
        time1.sleep(.01)
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
            level.writeConfig("level"+"".join(chunk1)+".map", monsters, False, invcount)
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