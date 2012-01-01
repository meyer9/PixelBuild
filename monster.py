import pygame
import random

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
		self.xspeed = random.randint(-11, 11)
		self.yspeed = random.randint(-11, 11)
		self.nextTurnTime=2000
		self.readyx=0

	def update(self, current_time, bottom):
		if self.next_update_time <= current_time:
			if self.nextTurnTime <= current_time:
				self.xspeed=random.randint(-10, 10)
				self.yspeed=random.randint(-10, 10)
				self.nextTurnTime+=2000
			if self.rect.left>0 and self.rect.left<900:
				self.rect.left+=self.xspeed
			if self.rect.left<=0:
				if current_time>=self.readyx:
					self.xspeed=abs(self.xspeed)
					self.readyx+=1000
					self.rect.left=40
			if self.rect.left>=900:
				if current_time>=self.readyx:
					self.xspeed=-abs(self.xspeed)
					self.readyx+=1000
					self.rect.left=890
			if current_time>=self.readyx:
				self.readyx+=10