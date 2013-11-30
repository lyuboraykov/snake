import sys
import time
from collections import deque
import os
import termios, fcntl

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

def draw_world(snake, obstacles):
	for el in snake:
		print_in_location(el.x, 
				el.y, el.elementSymbol)
	for x in obstacles:
		pass

if len(sys.argv) > 1:
	speed = sys.argv[1]
else:
	speed = 1.1
time_sleep = 1 / (float(speed) * 10)

snake = deque()

#initialize the snake
for x in range(0,5):
	snake.append(SnakeElement(10 - x, 10))

direction = 'right'

#gameloop
while 1 == 1:
	move_snake(direction, snake)
	clear_world()
	draw_world(snake, [])
	
	pressed_key = get_keyboard_input()
	if pressed_key:
		if pressed_key[1] == "A":
			direction='up'
		if pressed_key[1] == "D":
			direction='left'
		if pressed_key[1] == "C":
			direction='right'
		if pressed_key[1] == "B":
			direction='down'
		
	time.sleep(time_sleep)