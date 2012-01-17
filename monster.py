import pygame
import random
import math

def trunc(f, n):
    slen = len('%.*f' % (n, f))
    try:
        return int(str(f)[:slen])
    except:
        return int(str(f)[:slen-1])

class Monster(pygame.sprite.Sprite):
	def __init__(self, image, speed, initial_position, level):
		pygame.sprite.Sprite.__init__(self)
		self.level=level
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft=initial_position
		self.next_update_time = 0
		self.xspeed = 0
		self.yspeed = random.randint(-11, 11)
		self.nextTurnTime=2000
		self.readyx=0

	def update(self, current_time, bottom, playerx, playery):
		if self.next_update_time <= current_time:
			diffX = float(playerx - self.rect.left)+2
			diffY = float(playery - self.rect.top)+2
			diffLength = math.sqrt(diffX**2 + diffY**2)
			if diffLength/32<7:
				if diffLength>5:
					self.xspeed = diffX / diffLength * 3
					self.yspeed = diffY / diffLength * 3
				else:
					return 0
				try:
					if self.xspeed>0:
						if self.level.getTile(trunc((self.rect.left+25)/32,0), trunc((self.rect.top+16)/32,0))["name"]=="floor":
							self.rect.left+=self.xspeed
					else:
						if self.level.getTile(trunc((self.rect.left+12)/32,0), trunc((self.rect.top+16)/32,0))["name"]=="floor":
							self.rect.left+=self.xspeed
					if self.yspeed>0:
						if self.level.getTile(trunc((self.rect.left+16)/32,0), trunc((self.rect.top+25)/32,0))["name"]=="floor":
							self.rect.top+=self.yspeed
					else:
						if self.level.getTile(trunc((self.rect.left+16)/32,0), trunc((self.rect.top+4)/32,0))["name"]=="floor":
							self.rect.top+=self.yspeed
				except:
					pass
