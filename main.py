

import pygame  
import random
from const import *
import socket
import shutil
#from mkfiles_serv import mk
from mkfiles_serv import *

serverLocalIP = socket.gethostbyname(socket.gethostname())

# Удаляем остаточные файлы (На всяций случай)
try:
	rm()
except:
	pass

# Создаем файлы для сэссии
mk()


# Рисует всех змеек и яблоко
def draw():
	screen.fill((0,0,0))
    
	apple = list(map(int, open("server/apple/apple.txt").read().split("\n")))
	pygame.draw.rect(screen, (255,0,0) , (apple[0]+1,apple[1]+1, 19, 19))

	files = os.listdir("server/coord")
	for i in range(len(files)):
		snake = open(f"server/coord/{files[i]}").read().split("\n")

		for j in range(len(snake)):
			snake[j] = list(map(int, snake[j].split(" ")))
		for block in snake:
			pygame.draw.rect(screen, COLORS[i] , (block[0] + 1, block[1] + 1, 19, 19))

	clock.tick(FPS)
	pygame.display.update()


def createApple(): # Создаёт яблоки на поле и запиывает в файл
    apple = [random.randint(0,WIDTH//20 - 2)*20, random.randint(0,HEIGHT//20 - 2)*20]

    appleFile = open(f"server/apple/apple.txt","w")
    for coord in range(len(apple)):
        if coord == len(apple) - 1:
            appleFile.write(f"{apple[coord]}")
        else:
            appleFile.write(f"{apple[coord]}\n")
    appleFile.close()


# Обрабатывает нажатия клавиш и закрытие окна
def events():
	global done, speed
	fileSpeedText = list(open(f"server/speed/{serverLocalIP}.txt").read().split('\n'))
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT:  
			done = True  
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT and fileSpeedText != ["20", "0"]:
				fileSpeedText = ["-20", "0"]
			elif event.key == pygame.K_RIGHT and fileSpeedText != ["-20", "0"]:
				fileSpeedText = ["20", "0"]
			elif event.key == pygame.K_UP and fileSpeedText != ["0", "20"]:
				fileSpeedText = ["0", "-20"]
			elif event.key == pygame.K_DOWN and fileSpeedText != ["0", "-20"]:
				fileSpeedText = ["0", "20"]
	speedFile = open(f"server/speed/{serverLocalIP}.txt","w")
	for i in range(len(fileSpeedText)):
		if i != len(fileSpeedText) - 1:
			speedFile.write(f"{fileSpeedText[i]}\n")
		else:
			speedFile.write(f"{fileSpeedText[i]}")

# Перемещаяет все координаты змеек в файлах в зависимиости от скорости
def moveSnakes():
	ls = os.listdir("server/coord")
	for file in ls:
		snake = open(f"server/coord/{file}").read().split("\n")

		for i in range(len(snake)):
			snake[i] = list(map(int, snake[i].split(" ")))


		for i in range(len(snake)- 1):
			snake[i] = snake[i+1]

		speed = list(map(int, open(f"server/speed/{file}").read().split("\n")))
		snake[-1] = [snake[i][0] + speed[0],snake[i][1] + speed[1]]

		fileSnake = open(f"server/coord/{file}","w")
		for i in range(len(snake)):
			if i != len(snake) - 1:
				fileSnake.write(f"{snake[i][0]} {snake[i][1]}\n")
			else:
				fileSnake.write(f"{snake[i][0]} {snake[i][1]}")


def eatApple():
	ls = os.listdir("server/coord")
	for file in ls:
		snake = open(f"server/coord/{file}").read().split("\n")
		for i in range(len(snake)):
			snake[i] = list(map(int, snake[i].split(" ")))
		apple = list(map(int, open("server/apple/apple.txt").read().split("\n")))

		if apple == snake[-1]:
			snake.insert(0,snake[0])

			fileSnake = open(f"server/coord/{file}","w")
			for i in range(len(snake)):
				if i != len(snake) - 1:
					fileSnake.write(f"{snake[i][0]} {snake[i][1]}\n")
				else:
					fileSnake.write(f"{snake[i][0]} {snake[i][1]}")
			createApple()

def win_status():
	global done
	ls = os.listdir("server/coord")
	snakes = []
	for file in ls:
		snakes.append(open(f"server/coord/{file}").read().split("\n"))

		for i in range(len(snakes[-1])):
			snakes[-1][i] = list(map(int, snakes[-1][i].split(" ")))
		snakes[-1].append(file) # В последней ячейки списка будет храниться IP пользователя
	heads = []
	otherPartsOfBody = []

	live = [True for _ in range(PLAYERS)]

	for i in range(len(snakes)):
		heads.append(snakes[i][-2]) # В предпоследней ячейке координаты головы
		otherPartsOfBody += snakes[i][:-2]

	for i in range(len(snakes)):
		if heads[i] in otherPartsOfBody or not( 0 < heads[i][0] <= WIDTH - BLOCK_X * 2) or not(0 < heads[i][1] <= HEIGHT - BLOCK_Y * 2):
			live[i] = False

	if live.count(False) >= 1:
		done = True

done = False  


ls = os.listdir("server/speed")
for file in ls:
	open(f"server/speed/{file}","w").write("20\n0")


snake1 = [[20,40],[40,40],[60,40]]
snake2 = [[20,440],[40,440],[60, 440]]


# Создать координаты первой змейки
servSnake = open(f"server/coord/{serverLocalIP}.txt","w")
for i in range(len(snake1)):
	if i != len(snake1) - 1:
		servSnake.write(f"{snake1[i][0]} {snake1[i][1]}\n")
	else:
		servSnake.write(f"{snake1[i][0]} {snake1[i][1]}")
servSnake.close()



pygame.init()  
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()  
pygame.display.set_caption('Online Snake')

createApple()


while not done:  

	events()

	moveSnakes()

	draw()

	eatApple()
 
	win_status() 

pygame.display.flip()

# Удаляем файлы сэссии
rm()

'''
БАГИ

1) изменение напрвления движения на противоположный пром быстром нажатии двух клавиш
Например : змейка двиегается влево, нажмем клавишу ввера, сразу после чего клавишу вправо => змейка развернётся и умрет
Ошибка заключается в задержке  (не выявлено)
'''