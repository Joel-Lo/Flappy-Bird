import pygame, sys, random, signal, dbm

def load_high_score():
    try:
        with dbm.open('flappy_settings', 'c') as db:
            if b'highscore' in db:
                return int(db[b'highscore'].decode('utf-8'))
    except Exception:
        return 0
    return 0

def save_high_score(score_to_save):
    try:
        with dbm.open('flappy_settings', 'c') as db:
            db[b'highscore'] = str(int(score_to_save)).encode('utf-8')
    except Exception:
        pass

def sigint_handler(sig, frame):
        print("\nDeactivating Flappy Bird")
        print()
        print("Game deactivated") 
        save_high_score(high_score)
        pygame.quit()
        sys.exit() 

signal.signal(signal.SIGINT, sigint_handler)

def draw_floor():
	screen.blit(floor_surface,(floor_x_pos,900))
	screen.blit(floor_surface,(floor_x_pos + 576,900))

def create_pipe():
	random_pipe_pos = random.randint(450, 900)
	bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
	return bottom_pipe,top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 5
	visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
	return visible_pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 1024:
			screen.blit(pipe_surface,pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface,False,True)
			screen.blit(flip_pipe,pipe)

def check_collision(pipes):
	global can_score
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			death_sound.play()
			can_score = True
			return False

	if bird_rect.top <= -100 or bird_rect.bottom >= 900:
		can_score = True
		death_sound.play()
		return False

	return True

def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird,-bird_movement * 3,1)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
	return new_bird,new_bird_rect

def score_display(game_state):

	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)),True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)

	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(255,255,255))
		score_rect = score_surface.get_rect(center = (288,100))
		screen.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
		high_score_rect = high_score_surface.get_rect(center = (288,850))
		screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
		save_high_score(high_score)
	return high_score

def pipe_score_check():
	global score, can_score 
	
	if pipe_list:
		for pipe in pipe_list:
			if 95 < pipe.centerx < 105 and can_score:
				score += 1
				score_sound.play()
				can_score = False
			if pipe.centerx < 0:
				can_score = True

pygame.init()

bird_color = input("Choose bird colour: \n1. Blue \n2. Red \n3. Yellow \n\nOption ")

screen = pygame.display.set_mode((576,1024))

pygame.display.set_caption("Flappy Bird")

if bird_color in ("Blue", "1", "1. Blue"):
	pygame.display.set_icon(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())  
	bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-downflap.png').convert_alpha())
	bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
	bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-upflap.png').convert_alpha())

elif bird_color in ("Red", "2", "2. Red"):
	pygame.display.set_icon(pygame.image.load('assets/redbird-upflap.png').convert_alpha())  
	bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-downflap.png').convert_alpha())
	bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-midflap.png').convert_alpha())
	bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-upflap.png').convert_alpha())

elif bird_color in ("Yellow", "3", "3. Yellow"):
	pygame.display.set_icon(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())  
	bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
	bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
	bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())

else: 
    pygame.display.set_icon(pygame.image.load('assets/redbird-upflap.png').convert_alpha())  
    bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-downflap.png').convert_alpha())
    bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-midflap.png').convert_alpha())
    bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/redbird-upflap.png').convert_alpha())

clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',40)

gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = load_high_score()
can_score = True
bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center = (288,512))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
bgm = pygame.mixer.Sound('sound/Sugar Honey Ice Tea.mp3')
score_sound_countdown = 100
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT,100)

bgm.play()
bgm.play(-1)
bgm.set_volume(0.5)

while True:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			save_high_score(high_score)
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				bird_movement = 0
				bird_movement -= 10
				flap_sound.play()
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rect.center = (100,512)
				bird_movement = 0
				score = 0

		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())

		if event.type == BIRDFLAP:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0

			bird_surface,bird_rect = bird_animation()

	screen.blit(bg_surface,(0,0))

	if game_active:
		bird_movement += gravity
		rotated_bird = rotate_bird(bird_surface)
		bird_rect.centery += bird_movement
		screen.blit(rotated_bird,bird_rect)
		game_active = check_collision(pipe_list)

		pipe_list = move_pipes(pipe_list)
		draw_pipes(pipe_list)
		
		pipe_score_check()
		score_display('main_game')
	else:
		screen.blit(game_over_surface,game_over_rect)
		high_score = update_score(score,high_score)
		score_display('game_over')

	floor_x_pos -= 1
	draw_floor()
	if floor_x_pos <= -576:
		floor_x_pos = 0
	

	pygame.display.update()
	clock.tick(120)
