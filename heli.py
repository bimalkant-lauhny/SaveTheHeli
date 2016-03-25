import pygame,sys
from pygame.locals import *
import time
from random import *

pygame.init()

surfaceWidth = 800
surfaceHeight = 500

imageHeight = 47
imageWidth = 107

DISPLAYSURF = pygame.display.set_mode((surfaceWidth,surfaceHeight))
pygame.display.set_caption('HeliCopter')
CLOCK = pygame.time.Clock()

BLACK = (0,0,0)
WHITE = (255,255,255)

SUNSET = (253,72,47)

GREENYELLOW = (184,255,0)
ORANGE = (255,113,0)
YELLOW = (255,236,0)
PURPLE = (252,67,255)
colorChoices = [GREENYELLOW,ORANGE,YELLOW,PURPLE]

def blocks(x_block, y_block, block_width, block_height, gap, color):
	pygame.draw.rect(DISPLAYSURF,color,[x_block,y_block,block_width,block_height])
	y_block2 = y_block + block_height + gap
	pygame.draw.rect(DISPLAYSURF,color,[x_block,y_block2,block_width,surfaceHeight - y_block2])

def makeTextObjs(text, font, color):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()

def replay_or_quit():
	for event in pygame.event.get([pygame.KEYDOWN,pygame.KEYUP,pygame.QUIT]):
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			continue
		return event.key
	return None

def helicopter(x,y):
	DISPLAYSURF.blit(img,(x,y))

def score(current_score):
	scoreTextSurf, scoreTextRect = makeTextObjs('Score:'+str(current_score),pygame.font.Font('freesansbold.ttf',20),WHITE)
	scoreTextRect.center = 40, 20
	DISPLAYSURF.blit(scoreTextSurf, scoreTextRect)

def msgSurface(text):
	smallText = pygame.font.Font('freesansbold.ttf',20)
	largeText = pygame.font.Font('freesansbold.ttf',150)
	titleTextSurf, titleTextRect = makeTextObjs(text,largeText,SUNSET)
	titleTextRect.center = surfaceWidth/2, surfaceHeight/2
	DISPLAYSURF.blit(titleTextSurf, titleTextRect)
	typTextSurf, typTextRect = makeTextObjs('Press any key to continue',smallText,SUNSET)
	typTextRect.center = surfaceWidth/2, ((surfaceHeight/2) + 100)
	DISPLAYSURF.blit(typTextSurf, typTextRect)
	pygame.display.update()
	time.sleep(1)
	if replay_or_quit() == None:
		CLOCK.tick()	
	main()

def gameOver():
	pygame.mixer.music.stop()
	msgSurface('Kaboom!')

img  = pygame.image.load('heli2.png')

def main():
	x = 150
	y = 200
	y_move = 0

	x_block = surfaceWidth
	y_block = 0
	gap = imageHeight * 3
	block_width = 75
	block_height = randint(0,surfaceHeight-gap)
	block_move = 3

	blockColor = colorChoices[randrange(0,len(colorChoices))]

	current_score = 0
	game_over = False
	pygame.mixer.music.load('RideonSea.mp3')
	pygame.mixer.music.play(-1,0.0)
	while not game_over:
		DISPLAYSURF.fill(BLACK)
		for event in pygame.event.get():
			if event.type == QUIT:
				game_over = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					y_move = -5
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					y_move = 5
		y += y_move
		helicopter(x,y)

		if y>surfaceHeight-20 or y<0:
			gameOver()
		if x_block < (-1*block_width):
			x_block = surfaceWidth
			block_height = randint(0,surfaceHeight-gap)
			block_move += 0.5
			gap -= 1
			blockColor = colorChoices[randrange(0,len(colorChoices))]

		blocks(x_block,y_block,block_width,block_height,gap,blockColor)
		x_block -= block_move

		#block collision handling
		if x + imageWidth > x_block and x < x_block + block_width: #if heli within boundaries of blocks
			if y < block_height or y + imageHeight > block_height + gap: #heli collides
					gameOver()
		#Score updating
		if x > x_block and x < x_block + block_move:
			current_score += 1

		score(current_score)
		pygame.display.update()
		CLOCK.tick(30)

main()
pygame.quit()
sys.exit()
