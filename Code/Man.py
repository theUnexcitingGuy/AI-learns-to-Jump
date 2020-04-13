import pygame
import random
from defs import *
from AI import Net 
import numpy as np 


class Man(): 

	def __init__(self, gameDisplay):
		self.gameDisplay = gameDisplay
		self.state = MAN_ALIVE
		self.img = pygame.image.load(MAN_FILENAME)
		self.rect = self.img.get_rect() #scritto prima di set position *importante*
		self.speed = 0
		self.fitness = 0
		self.time_lived = 0
		self.nnet = Net(NNET_INPUTS, NNET_HIDDEN, NNET_OUTPUTS)
		self.set_position(MAN_START_X, 540)


	def reset(self):
		self.state = MAN_ALIVE
		self.speed = 0
		self.fitness = 0
		self.time_lived = 0
		self.set_position(MAN_START_X, 540)


	def set_position(self, x, y):
		self.rect.centerx = x
		self.rect.centery = y

	def move(self, dt):
		distance = 0
		new_speed = 0

		distance = (self.speed * dt) + (0.5 * GRAVITY * dt * dt) #distanza lungo y
		new_speed = (self.speed + GRAVITY * dt) 

		self.rect.centery += distance #muoviamo ora il personaggio in alto di una distanza pari a quella calcolata
		self.speed += new_speed #muoviamo il personaggio con la velocità calcolata

		if self.rect.top < 0: #se fa un salto che sfora il margine superiore, non lo facciamo sforare e gli diamo velocità uguale a zero
			self.rect.top = 0
			self.speed = 0

		elif self.rect.bottom > 540:
			self.rect.bottom = 540
			self.speed = 0
	
	def jump(self, barriers):
		inputs = self.get_inputs(barriers)
		val = self.nnet.get_max_value(inputs)
		if val >= JUMP_CHANCE and self.rect.bottom == 540:
			self.speed = MAN_START_SPEED #velocità del personaggio quando fa un salto

	def draw(self):
		self.gameDisplay.blit(self.img, self.rect)

	def check_status(self, barriers):
		if 500 > 600:
			self.state = MAN_DEAD
			print('Man died')
		else: 
			self.check_hits(barriers)

	def assign_collision_fitness(self, b):
		self.fitness = -(abs(self.rect.centery - b.rect.top))


	def check_hits(self, barriers):
		for b in barriers: 
			if b.rect.colliderect(self.rect): #se il rettangolo dell'ostacolo coincide con quello del personaggio allora il personaggio muore
				self.state = MAN_DEAD
				self.assign_collision_fitness(b)
				break

	def update(self, dt, barriers):
		if self.state == MAN_ALIVE:
			self.time_lived += dt
			self.move(dt)
			self.jump(barriers)
			self.draw()
			self.check_status(barriers)

	def get_inputs(self, barriers):
		closest = DISPLAY_W * 2
		for b in barriers:
			if b.rect.right < closest and b.rect.right > self.rect.left:
				closest = b.rect.right
				y = b.rect.top #registro l'altezza dell'ostacolo

		horizontal_distance = closest - self.rect.centerx
		vertical_distance = self.rect.centery - y

		#creo array di input, che corrispondono ai valori sopra ma normalizzati, ovvero divisi per il valore massimo rispettivo
		inputs = [
			((horizontal_distance/DISPLAY_W) * 0.99) + 0.01,
			((vertical_distance/DISPLAY_H) * 0.99) + 0.01
		] 

		return inputs

	def create_offspring(m1, m2, gameDisplay):
		 new_man = Man(gameDisplay)
		 new_man.nnet.create_mixed_weights(m1.nnet, m2.nnet)
		 return new_man


class ManCollection():

	def __init__(self, gameDisplay):
		self.gameDisplay = gameDisplay
		self.men = []
		self.create_new_population()
		
	def create_new_population(self):
		self.men = []
		for i in range(0, POPULATION_SIZE):
			self.men.append(Man(self.gameDisplay)) #per ogni iterazione creo un nuovo personaggio e lo aggiungo al vettore popolazione chiamato men

	def update(self, dt, barriers): #funzione per ora che fa saltare a caso il personaggino
		num_alive = 0
		for m in self.men:
			m.update(dt, barriers)
			if m.state == MAN_ALIVE:
				num_alive += 1

		return num_alive

	def evolve_population(self):
		for man in self.men:
			man.fitness += man.time_lived * OBSTACLE_SPEED

		self.men.sort(key = lambda x: x.fitness, reverse = True)

		cut_off = int(len(self.men) * MUTATION_CUT_OFF)
		good_men = self.men[0: cut_off]
		bad_men = self.men[cut_off:]
		num_bad_to_take = int(len(self.men) * MUTATION_BAD_TO_KEEP)

		for m in bad_men:
			m.nnet.modify_weights()

		new_men = [] #nuova popolazione che vado a creare

		idx_bad_to_take = np.random.choice(np.arange(len(bad_men)), num_bad_to_take, replace = False)

		for index in idx_bad_to_take:
			new_men.append(bad_men[index])

		new_men.extend(good_men)

		children_needed = len(self.men) - len(new_men)

		while len(new_men) < len(self.men):
			idx_to_breed = np.random.choice(np.arange(len(good_men)), 2, replace = False)

			if idx_to_breed[0] != idx_to_breed[1]:
				new_man = Man.create_offspring(good_men[idx_to_breed[0]], good_men[idx_to_breed[1]], self.gameDisplay)
				if random.random() < MUTATION_MODIFY_CHANCE_LIMIT:
					new_man.nnet.modify_weights()

				new_men.append(new_man)


		for m in new_men:
			m.reset();

		self.men = new_men






