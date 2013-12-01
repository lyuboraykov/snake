import sys
import time
from collections import deque
import os
import termios, fcntl
import random
import console

def get_keyboard_input():
	fd = sys.stdin.fileno()

	oldterm = termios.tcgetattr(fd)
	newattr = termios.tcgetattr(fd)
	newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
	termios.tcsetattr(fd, termios.TCSANOW, newattr)
	
	oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)
	
	try:
	    try:
	        c = sys.stdin.read(1)
	        return (repr(c))
	    except IOError: pass
	finally:
	    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
	    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

def print_in_location(x, y, string):
	"""Use escape sequences to print in specific location"""
	sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, string))
	sys.stdout.flush()

def clear_world():
	"""	Identical to clear in bash. """
	os.system('clear')

def move_snake(direction, snake):
	"""Move the snake by modifying the last and first element in it"""

	#dequeue the last element and prepare it to be enqueued
	last_element = snake.pop()
	last_element.x = snake[0].x
	last_element.y = snake[0].y

	if direction == 'up':
		last_element.y = snake[0].y - 1
	elif direction == 'down':
		last_element.y = snake[0].y + 1
	elif direction == 'left':
		last_element.x = snake[0].x - 1
	elif direction == 'right':
		last_element.x = snake[0].x + 1
	snake.appendleft(last_element)

class SnakeElement:
	"""Should be used in a queue to make the game snake"""
	elementSymbol = '*'
	def __init__(self, x, y):
		self.x = x
		self.y = y

def draw_world(snake, food):
	for el in snake:
		print_in_location(el.x, 
				el.y, el.elementSymbol)
	print_in_location(food.x, food.y, food.elementSymbol)

def has_crashed_itself(snake):
	for el in range(1, len(snake)):
		if snake[el].x == snake[0].x and snake[el].y == snake[0].y:
			return True
	return False

def lose():
	clear_world();
	print ("DAMN YOU LOST")

#commmand line speed argument
if len(sys.argv) > 1:
	speed = sys.argv[1]
else:
	speed = 1.1
time_sleep = 1 / (float(speed) * 10)

snake = deque()

#initialize the snake
for x in range(0, 10):
	snake.append(SnakeElement(10 - x, 10))

direction = 'right'
terminal_size = console.get_terminal_size()
terminal_width = terminal_size[0]
terminal_height = terminal_size[1]

#instance first obstacle
food = SnakeElement (random.randint(0, terminal_width),
 			random.randint(0, terminal_height))

#gameloop
while 1 == 1:
	pressed_key = get_keyboard_input()
	if pressed_key:
		if pressed_key[1] == "A" and direction != 'down':
			direction='up'
		if pressed_key[1] == "D" and direction != 'right':
			direction='left'
		if pressed_key[1] == "C" and direction != 'left':
			direction='right'
		if pressed_key[1] == "B" and direction != 'up':
			direction='down'

	move_snake(direction, snake)
	#left or right walls
	if snake[0].x < 0 or snake[0].x > terminal_width:
		lose()
		break
	#up or down walls
	elif snake[0].y < 0 or snake[0].y > terminal_height:
		lose()
		break
	elif has_crashed_itself(snake):
		lose()
		break
	if snake[0].x == food.x and snake[0].y == food.y:
		snake.append(SnakeElement(food.x, food.y))
		food.x = random.randint(0, terminal_width)
		food.y = random.randint(0, terminal_height)

	clear_world()
	draw_world(snake, food)
	
	time.sleep(time_sleep)