import pygame
import random
import math
from pygame import mixer

pygame.font.init()
pygame.mixer.init()

screen_width = 800
screen_height = 600
to_fire = False

def set_window():
	pygame.display.set_caption("Space Invaders")

	icon = pygame.image.load('img/logo.png')
	pygame.display.set_icon(icon)

def back_music():
	mixer.music.load('music/background.wav')
	mixer.music.play(-1)


def player(win, x, y):
	playerPng = pygame.image.load('img/space-invaders.png')
	win.blit(playerPng, (x, y))

def enemy(win, x, y, enemyPng):
	win.blit(enemyPng, (x, y))

def fire_bullet(win, x, y):
	global to_fire
	to_fire = True
	bulletImg = pygame.image.load("img/bullet.png")
	win.blit(bulletImg, (x+16, y+10))

def is_collision(enemyX, enemyY, bulletX, bulletY):
	distance = math.sqrt((math.pow(enemyX-bulletX, 2)) + (math.pow(enemyY-bulletY, 2)))

	if distance < 27:
		return True
	else:
		return False

def draw_score(win, score=0):
	font = pygame.font.SysFont('comicsans', 60)
	label = font.render('Score: '+str(score), 1, (255, 255, 255))
	win.blit(label, (10, 10))

def draw_text_middle(win, text, size, color):
	font = pygame.font.SysFont('comicsans', size, bold=True)
	label = font.render(text, 1, color)

	win.blit(label, (screen_width /2 - (label.get_width()/2), screen_height/2 - (label.get_height()/2)))

def check_lost(playerX, playerY, enemyX, enemyY):
	distance = math.sqrt((math.pow(playerX-enemyX, 2)) + (math.pow(playerY-enemyY, 2)))

	if distance < 27:
		return True
	else:
		return False

def main(win, background):
	global to_fire

	playerVel = 0
	playerX = 370
	playerY = 480

	enemyImg = []
	enemyX = []
	enemyY = []
	enemyXvel = []
	enemyYvel = []
	num_of_enemies = 6

	for i in range(num_of_enemies):
		enemyPng = pygame.image.load('img/enemy.png')
		enemyImg.append(pygame.transform.scale(enemyPng, (64, 64)))
		enemyX.append(random.randint(0, screen_width-64-1))
		enemyY.append(random.randint(50, 58))
		enemyXvel.append(2)
		enemyYvel.append(50)

	run = True
	
	bulletX = 0
	bulletY = 480
	bullVel = 10

	score = 0

	set_window()
	back_music()
	while run:
		win.fill((0, 0, 0))

		win.blit(background, (0, 0))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				mixer.music.stop()
				run = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					playerVel = -5
				if event.key == pygame.K_RIGHT:
					playerVel = 5
				if event.key == pygame.K_SPACE:
					if not(to_fire):
						bullet_sound = mixer.Sound('music/laser.wav')
						bullet_sound.play()
						bulletX = playerX
						fire_bullet(win, playerX, bulletY)

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
					playerVel = 0

		playerX += playerVel

		if playerX <=0:
			playerX = 0
		elif playerX >= screen_width - 64:
			playerX = screen_width - 64


		for i in range(num_of_enemies):
			enemyX[i] += enemyXvel[i]

			if enemyX[i] <=0:
				enemyXvel[i] = 2
				enemyY[i] += enemyYvel[i]
			elif enemyX[i] >= screen_width - 64:
				enemyXvel[i] = -2
				enemyY[i] += enemyYvel[i]

			collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
			if collision:
				collision_sound = mixer.Sound('music/explosion.wav')
				collision_sound.play()
				bulletY = 480
				to_fire = False
				score += 1
				enemyX[i] = random.randint(0, screen_width-64-1)
				enemyY[i] = random.randint(50, 58)

			enemy(win, enemyX[i], enemyY[i], enemyImg[i])


		if bulletY <= 0:
			bulletY = 480
			to_fire = False
		
		if to_fire:
			fire_bullet(win, bulletX, bulletY)
			bulletY -= bullVel 

		player(win, playerX, playerY)
		draw_score(win, score)

		pygame.display.update()

		for i in range(num_of_enemies):
			if check_lost(playerX, playerY, enemyX[i], enemyY[i]):
				draw_text_middle(win, "YOU LOSE!", 80, (255, 255, 255))
				pygame.display.update()
				pygame.time.delay(1500)
				mixer.music.stop()
				run = False

def main_menu(win):
	run = True
	while run:
		win.fill((0, 0, 0))
		set_window()
		title = pygame.image.load('img/title.png')
		title = pygame.transform.scale(title, (screen_width//2, screen_height//2))
		win.blit(title, (screen_width//4, screen_height//4))
		pygame.display.update()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				background = pygame.image.load('img/background.jpg')
				background = pygame.transform.scale(background, (800, 600))
				main(win, background)

	pygame.display.quit()

win = pygame.display.set_mode((screen_width, screen_height))
main_menu(win)