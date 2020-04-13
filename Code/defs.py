# PATH FINDING VARIABLES

DISPLAY_W = 960
DISPLAY_H = 540
FPS = 30

DATA_FONT_SIZE = 18
DATA_FONT_COLOR = (40, 40, 40)
BG_FILENAME = '../BG.png'

#obstacle variables
OBSTACLE_FILENAME = '../barrier.png'
OBSTACLE_SPEED = 400/1000
OBSTACLE_DONE = 1
OBSTACLE_MOVING = 0

#variables for defining multiple obstacles
OBSTACLE_START_X = DISPLAY_W #where a new obstacle appears
OBSTACLE_FIRST = 700 #where the first obstacle appears

#variables for the Man
MAN_FILENAME = '../Man.png'
MAN_START_SPEED = -0.628 #speed of the man going upwards
MAN_START_X = 100
MAN_START_Y = 300
MAN_ALIVE = 1
MAN_DEAD = 0
GRAVITY = 0.0068 #prima era a 0.007

#population variables
POPULATION_SIZE = 60

#AI variables
NNET_INPUTS = 2
NNET_HIDDEN = 5
NNET_OUTPUTS = 1

JUMP_CHANCE = 0.5

#genetic variables
MUTATION_WEIGHT_MODIFY_CHANCE = 0.2
MUTATION_ARRAY_MIX_PERC = 0.5
MUTATION_CUT_OFF = 0.4
MUTATION_BAD_TO_KEEP = 0.2
MUTATION_MODIFY_CHANCE_LIMIT = 0.4





