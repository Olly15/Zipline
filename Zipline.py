import pygame, sys, time, random, math
from pygame.locals import *
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Zipline")
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
game = "menu"
death_time = None
first_time = True

far_hills_image = pygame.image.load("Zipline_Hills.png")

forest_hills_image = pygame.image.load("Forest_Hills.png")
village_hills_image = pygame.image.load("Village_Hills.png")
castle_hills_image = pygame.image.load("Castle_Hills.png")
snow_hills_image = pygame.image.load("Snow_Hills.png")

sunset_image = pygame.image.load("Sunset.png")
sky_image = pygame.image.load("Sky.png")

areas = [forest_hills_image, village_hills_image, castle_hills_image]

swift_image = pygame.image.load("Swift.png")
swift_sound = pygame.mixer.Sound("swift_sound.wav")

eagle1_image = pygame.image.load("Eagle1.png")
eagle2_image = pygame.image.load("Eagle2.png")
eagle_anim = [eagle1_image, eagle2_image]
eagle_sound = pygame.mixer.Sound("eagle_sound.wav")

owl1_image = pygame.image.load("Owl1.png")
owl2_image = pygame.image.load("Owl2.png")
owl_anim = [owl1_image, owl2_image]
owl_sound = pygame.mixer.Sound("owl_sound.wav")

robin1_image = pygame.image.load("Robin1.png")
robin2_image = pygame.image.load("Robin2.png")
robin_anim = [robin1_image, robin2_image]
robin_sound = pygame.mixer.Sound("robin_sound.wav")

pigeon1_image = pygame.image.load("Pigeon1.png")
pigeon2_image = pygame.image.load("Pigeon2.png")
pigeon_anim = [pigeon1_image, pigeon2_image]
pigeon_sound = pygame.mixer.Sound("pigeon_sound.wav")

duck1_image = pygame.image.load("Duck1.png")
duck2_image = pygame.image.load("Duck2.png")
duck_anim = [duck1_image, duck2_image]
duck_sound = pygame.mixer.Sound("duck_sound.wav")

raven1_image = pygame.image.load("Raven1.png")
raven2_image = pygame.image.load("Raven2.png")
raven_anim = [raven1_image, raven2_image]
raven_sound = pygame.mixer.Sound("raven_sound.wav")

seagull1_image = pygame.image.load("Seagull1.png")
seagull2_image = pygame.image.load("Seagull2.png")
seagull_anim = [seagull1_image, seagull2_image]
seagull_sound = pygame.mixer.Sound("seagull_sound.wav")

phoenix1_image = pygame.image.load("Phoenix1.png")
phoenix2_image = pygame.image.load("Phoenix2.png")
phoenix3_image = pygame.image.load("Phoenix3.png")
phoenix_anim = [phoenix1_image, phoenix2_image]
phoenix_existance = False
phoenix_sound = pygame.mixer.Sound("phoenix_sound.wav")

fire1_image = pygame.image.load("Fire1.png")
fire2_image = pygame.image.load("Fire2.png")
fire3_image = pygame.image.load("Fire3.png")
fire4_image = pygame.image.load("Fire4.png")
fire_anim = [fire1_image, fire2_image, fire3_image, fire4_image]
fire_sound = pygame.mixer.Sound("fire_sound.wav")

guy1_image = pygame.image.load("Guy1.png")
guy2_image = pygame.image.load("Guy2.png")

logo_image = pygame.image.load("ZiplineLogo.png")

font = pygame.font.Font(None, 100)
font2 = pygame.font.Font(None, 30)
font3 = pygame.font.Font(None, 20)

music = pygame.mixer.music.load("At_Launch.wav")

class Guy:
	def __init__(self):
		self.x = -200
		self.y = 300
		self.speed = 0.0
		self.flash_time_end = 0
		self.flashing = False
		self.img = guy1_image
	
	def move(self):
		if pressed_keys[K_SPACE]:
			self.y += 25
			self.img = guy2_image
		else:
			self.img = guy1_image
		if self.x < 200:
			self.x += 4
		else:
			self.x = 200
		
	def spring(self):
		self.speed += (300 - self.y) * 0.01 #This pulls the guy towards the center. 0.01 is the springyness.
		self.speed *= 0.95      #This slows them down over time.0.995 is the friction.
		self.y += self.speed     
		
	def draw(self):
		if time.time() > self.flash_time_end or time.time()%0.1 < 0.05:
			screen.blit(self.img, (self.x, self.y))
		pygame.draw.line(screen, (0, 0, 0), (-1000, 200), (self.x + 10, self.y), 2)
		pygame.draw.line(screen, (0, 0, 0), (self.x+10, self.y), (2000, 430), 2)
		
		if time.time() > self.flash_time_end:
			self.flashing = False

class Far_hill:
	def __init__(self, x):
		self.x = x
		self.y = 200
	
	def move(self):
		self.x -= 1
		if self.x <= -1000:
			self.x = 1000
	
	def draw(self):
		screen.blit(far_hills_image, (self.x, self.y))

class Close_hill:
	def __init__(self, img, x):
		self.x = x
		self.y = 300
		self.img = img
		global area
		global areas
		global current_area
	
	def move(self):
		self.x -= 2
		if self.x <= -1000:
			self.x = 1000
			self.img = areas[area]
	
	def draw(self):
		screen.blit(self.img, (self.x, self.y))

class Swift:
	def __init__(self):
		self.x = 1000
		self.y = random.randrange(100, 401)
		swift_sound.play()
		
		self.is_phoenix = False
	
	def move(self):
		self.x -= 10
		self.hitbox = (self.x + 30, self.y, 30, 100)
	
	def off_screen(self):
		return self.x < -100
	
	def draw(self):
		screen.blit(swift_image, (self.x, self.y))

class Eagle:
	def __init__(self):
		self.x = 2000
		self.y = 50
		self.anim_phase = 0.0
		
		self.is_phoenix = False
		self.sound_played = False
	
	def move(self):
		self.x -= 5
		if self.x < 325:
			self.y += 5
			self.anim_phase = 0
			if not self.sound_played:
				eagle_sound.play()
				self.sound_played = True
		else:
			self.anim_phase += 0.2
			if self.anim_phase >= 2.0:
				self.anim_phase = 0.0
		
		self.hitbox = (self.x, self.y + 40, 100, 30)
	
	def off_screen(self):
		return self.x < -100
	
	def draw(self):
		self.img = eagle_anim[int(self.anim_phase)]
		screen.blit(self.img, (self.x, self.y))

class Owl:
	def __init__(self):
		self.x = -100
		self.y = guy.y
		self.anim_phase = 0.0
		
		self.is_phoenix = False
		owl_sound.play()
	
	def move(self):
		self.x += 4
		self.anim_phase += 0.1
		if self.anim_phase >= 2.0:
			self.anim_phase = 0.0
		
		self.hitbox = (self.x + 25, self.y + 10, 50, 80)
	
	def off_screen(self):
		return self.x > 1000
	
	def draw(self):
		self.img = owl_anim[int(self.anim_phase)]
		screen.blit(self.img, (self.x, self.y))

class Robin:
	def __init__(self):
		self.x = random.randrange(1950, 2051)
		self.y = random.randrange(100, 401)
		self.bottom_y = self.y - 1
		self.top_y = self.y + 200
		self.anim_phase = 1
		self.dir = -1
		
		self.is_phoenix = False
		self.sound_played = False
	
	def move(self):
		self.x -= 8
		self.y += 10 * self.dir
		if not self.bottom_y < self.y < self.top_y:
			self.dir *= -1
			self.anim_phase += 1
			if self.anim_phase == 2:
				self.anim_phase = 0
		
		self.hitbox = (self.x + 5, self.y + 15, 90, 70)
		if self.x <= 1000 and not self.sound_played:
			robin_sound.play()
			self.sound_played = True
	
	def off_screen(self):
		return self.x <= -100
		
	def draw(self):
		screen.blit(robin_anim[self.anim_phase], (self.x, self.y))

class Pigeon:
	def __init__(self):
		self.x = random.randrange(1900, 2101)
		self.y = 100
		self.anim_phase = 0.0
		self.speed = 0
		
		self.is_phoenix = False
		self.sound_played = False
	
	def move(self):
		self.x -= 8
		self.speed += (300 - self.y) * 0.01 #This pulls the guy towards the center. 0.01 is the springyness.      #This slows them down over time.0.995 is the friction.
		self.y += self.speed
		self.anim_phase += 0.1
		if self.anim_phase >= 2.0:
			self.anim_phase = 0.0   
		
		self.hitbox = (self.x + 5, self.y + 5, 90, 80)
		if self.x <= 1000 and not self.sound_played:
			pigeon_sound.play()
			self.sound_played = True
	
	def off_screen(self):
		return self.x <= -100
	
	def draw(self):
		screen.blit(pigeon_anim[int(self.anim_phase)], (self.x, self.y))

class Duck:
	def __init__(self):
		self.x = 2000
		self.y = random.randrange(100, 501)
		self.anim_phase = 0.0
		
		self.is_phoenix = False
		self.sound_played = False
	
	def move(self):
		self.x -= 8
		self.anim_phase += 0.1
		if self.anim_phase >= 2.0:
			self.anim_phase = 0.0
		
		if self.x <= 1000 and not self.sound_played:
			duck_sound.play()
			self.sound_played = True
		
		self.hitbox = (self.x - 5, self.y - 25, 125, 150)
	
	def off_screen(self):
		return self.x <= -300
	
	def draw(self):
		screen.blit(duck_anim[int(self.anim_phase)], (self.x, self.y))
		screen.blit(duck_anim[int(self.anim_phase)], (self.x + 50, self.y - 50))
		screen.blit(duck_anim[int(self.anim_phase)], (self.x + 50, self.y + 50))

class Raven:
	def __init__(self):
		#self.x = random.randrange(1950, 2051)
		self.x = 1000
		self.y = random.randrange(100, 501)
		self.anim_phase = 0.0
		self.dir = 90
		self.phase = "moving"
		
		self.is_phoenix = False
		self.sound_played = False
		
	def move(self):
		if self.phase == "moving":
			self.x -= 8
			if self.x <= 200:
				self.phase = "looping"
		elif self.phase == "done":
			self.x -= 8
		else:
			dx = math.sin(math.radians(self.dir))
			dy = math.cos(math.radians(self.dir))
		
			self.x -= dx * 8
			self.y -= dy * 8
		
			self.dir -= 3
			if self.dir <= -270:
				self.phase = "done"
		
		self.anim_phase += 0.1
		self.hitbox = (self.x + 20, self.y + 20, 100, 70)
		if self.phase == "looping" and not self.sound_played:
			raven_sound.play()
			self.sound_played = True
		
		if self.anim_phase >= 2.0:
			self.anim_phase = 0.0
		
	def off_screen(self):
		return self.x < -100
	
	def draw(self):
		self.img = raven_anim[int(self.anim_phase)]
		rotated = pygame.transform.rotate(self.img, self.dir - 90)
		screen.blit(rotated, (self.x + self.img.get_width()/2 - rotated.get_width()/2, self.y + self.img.get_height()/2 - rotated.get_height()/2))

class Seagull:
	def __init__(self):
		self.x = 300
		self.y = random.randrange(600, 1001)
		self.start_y = self.y
		self.spring_center = self.y - 300
		self.anim_phase = 0.0
		self.dir = 200
		self.speed = 0
		self.hitbox = (self.x, self.y, 200, 100)
		self.last_y = self.y
		self.done = False
		
		self.is_phoenix = False
		self.sound_played = False
	
	def move(self):
		self.speed += (self.spring_center - self.y) * 0.01 #This pulls the guy towards the center. 0.01 is the springyness.      #This slows them down over time.0.995 is the friction.
		self.y += self.speed
		self.x -= (300 - self.speed)/50
		
		self.dir += 10 - abs((self.last_y - self.y)/4)
		self.last_y = self.y
		
		if self.y <= 600:
			self.done = True
		
		self.hitbox = (self.x + 100, self.y, 20, 100)
		if self.y <= 600 and not self.sound_played:
			seagull_sound.play()
			self.sound_played = True
	
	def off_screen(self):
		return (self.y >= 650 and self.done) or self.x <= -100
	
	def draw(self):
		self.img = seagull1_image
		rotated = pygame.transform.rotate(self.img, self.dir)
		screen.blit(rotated, (self.x + self.img.get_width()/2 - rotated.get_width()/2, self.y + self.img.get_height()/2 - rotated.get_height()/2))

class Phoenix:
	def __init__(self):
		self.x = 700
		self.y = random.randrange(100, 501)
		self.fire_x = 1100
		self.fire_y = self.y
		self.anim_phase = 0.0
		self.hitbox = (self.x, self.y, 200, 200)
		self.dir = 0
		self.speed = 1
		self.phase = "spinning"
		self.is_phoenix = True
		phoenix_sound.play()
		self.sound_played = False
	
	def move(self):
		self.anim_phase += 0.5
		if self.anim_phase >= 4.0:
			self.anim_phase = 0.0
		
		self.hitbox = (self.fire_x, self.fire_y + 50, 50, 100)
		
		if self.phase == "spinning":
			self.speed *= 1.01
			self.dir += self.speed
			
			self.fire_dx = math.sin(math.radians(self.dir))
			self.fire_dy = math.cos(math.radians(self.dir))
		
			self.fire_x -= self.fire_dx * (self.speed * 6)
			self.fire_y -= self.fire_dy * (self.speed * 6)
			
			if self.fire_y <= self.y - 300:
				swift_sound.play()
			
			if self.speed >= 50:
				self.phase = "firing"
				self.img = phoenix3_image
				self.dir = 0
				self.fire_x = 500
				self.fire_y = self.y
				self.fire_dir = 90
		
		elif self.phase == "firing":
			self.fire_x -= 10
			if not self.sound_played:
				fire_sound.play()
				self.sound_played = True
	
	def off_screen(self):
		return self.fire_x <= -200
	
	def draw(self):
		screen.blit(fire_anim[int(self.anim_phase)], (self.x, self.y))
			
		self.img = fire_anim[int(self.anim_phase)]
		if self.phase == "spinning":
			rotated = pygame.transform.rotate(self.img, self.dir - 180)
		else:
			rotated = pygame.transform.rotate(self.img, self.fire_dir - 180)
		screen.blit(rotated, (self.fire_x + self.img.get_width()/2 - rotated.get_width()/2, self.fire_y + self.img.get_height()/2 - rotated.get_height()/2))
			
		if self.phase == "spinning":
			self.img = phoenix1_image
		else:
			self.img = phoenix3_image
		rotated = pygame.transform.rotate(self.img, self.dir)
		screen.blit(rotated, (self.x + self.img.get_width()/2 - rotated.get_width()/2, self.y + self.img.get_height()/2 - rotated.get_height()/2))

class Message:
	def __init__(self):
		self.x = 150
		self.y = 200
		
	def move(self):
		if guy.x == 200:
			self.x -= 4
	
	def draw(self):
		text = font.render("Use Space to Bounce", True, (0, 0, 0))
		pygame.draw.rect(screen, (0, 0, 0), (self.x + 140, self.y, 220, 70), 5)
		screen.blit(text, (self.x, self.y))
		
		
guy = Guy()
far_hills = (Far_hill(0), Far_hill(1000))
close_hills = (Close_hill(forest_hills_image, 0), Close_hill(forest_hills_image, 1000))
birds = []

while 1:
	clock.tick(60)
	
	pressed_keys = pygame.key.get_pressed()
	
	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit()
	
	screen.fill((209, 93, 5))
		
	pygame.draw.circle(screen, (255, 150, 0), (500, 400), 200)
	pygame.draw.rect(screen, (0, 0, 255), (0, 300, 1000, 300))
		
	pygame.draw.line(screen, (255, 0, 0), (475, 305), (525, 305), 5)
	pygame.draw.line(screen, (250, 50, 0), (470, 315), (530, 315), 5)
	pygame.draw.line(screen, (225, 75, 0), (450, 325), (550, 325), 5)
		
	pygame.draw.line(screen, (255, 100, 0), (400, 335), (600, 335), 5)
	pygame.draw.line(screen, (255, 125, 0), (350, 345), (650, 345), 5)
	pygame.draw.line(screen, (255, 150, 0), (325, 355), (675, 355), 5)
	pygame.draw.line(screen, (255, 200, 0), (350, 365), (650, 365), 5)
	pygame.draw.line(screen, (255, 255, 0), (400, 375), (600, 375), 5)
	
	if game == "playing":

# Dealing with far hills:	
		for far_hill in far_hills:
			if guy.x == 200:
				far_hill.move()
			far_hill.draw()

# Dealing with close hills:	
		for close_hill in close_hills:
			if guy.x == 200:
				close_hill.move()
			close_hill.draw()
		
		if time.time() >= area_enter + area_length:
			new_area = random.randrange(0, 3)
			while new_area == area:
				new_area = random.randrange(0, 3)
			area = new_area
			area_enter = time.time()
			area_length = random.randrange(20, 41)
		
# Dealing with message:
		if message:
			message.move()
			message.draw()
			if message.x <= -1000:
				message = None	
		
# Dealing with guy:		
		guy.move()
		guy.spring()
		guy.draw()
		
		for bird in birds:
			if pygame.Rect(guy.x, guy.y, 20, 40).colliderect(bird.hitbox) and not guy.flashing:
				guy.health -= 1
				guy.flash_time_end = time.time() + 2
				guy.flashing = True
		
		pygame.draw.rect(screen, (0, 0, 0), (25, 10, 750, 50), 5)
		pygame.draw.rect(screen, (255, 255, 0), (30, 15, 740/guy.max_health * guy.health, 40))
		for dash in range(1, guy.max_health):
			pygame.draw.line(screen, (0, 0, 0), ((750/guy.max_health * dash) + 23, 60), ((750/guy.max_health * dash) + 23, 35), 5)
		
		text = font.render(str(int(time.time()*10 - game_start*10)) + "m", True, (0, 0, 0))
		screen.blit(text, (800, 10))
		
		if guy.health == 0:
			game = "dead"
			death_time = str(int(time.time()*10 - game_start*10))

# Dealing with birds:
		if guy.x == 200:
			if time.time() >= last_bird_spawn + next_bird_spawn:
				next_bird = random.randrange(0, 3)
			
				if area == 0:
					if next_bird == 0:
						birds.append(Swift())
					elif next_bird == 1:
						birds.append(Eagle())
					elif next_bird == 2:
						birds.append(Owl())
			
				if area == 1:
					if next_bird == 0:
						birds.append(Robin())
					elif next_bird == 1:
						birds.append(Pigeon())
					elif next_bird == 2: 
						birds.append(Duck())
			
				if area == 2:
					if next_bird == 0:
						birds.append(Raven())
					elif next_bird == 1:
						birds.append(Seagull())
					elif next_bird == 2 and not phoenix_existance:
						birds.append(Phoenix())
						phoenix_existance = True
				
				last_bird_spawn = time.time()
				
				if gamemode == "easy":
					next_bird_spawn = random.randrange(20, 31)
				elif gamemode == "normal":
					next_bird_spawn = random.randrange(15, 26)
				elif gamemode == "hard":
					next_bird_spawn = random.randrange(10, 21)
				next_bird_spawn /= 10
		
			i = 0
			while i < len(birds):
				birds[i].move()
				birds[i].draw()
			
				if birds[i].off_screen():
					if birds[i].is_phoenix:
						phoenix_existance = False
					birds.remove(birds[i])
					i -= 1
				i += 1
		
	elif game == "menu":
	
		for far_hill in far_hills:
			far_hill.draw()
		for close_hill in close_hills:
			close_hill.draw()
		guy.draw()
		
		screen.blit(logo_image, (0, 20))
		
		if death_time:
			text = font.render(str(death_time) + "m travelled", True, (0, 0, 0))
			screen.blit(text, (screen.get_width()/2 - text.get_width()/2, 325))
		
		text = font.render("Easy", True, (0, 0, 0))
		screen.blit(text, (150, 450))
		
		text = font.render("Normal", True, (0, 0, 0))
		screen.blit(text, (350, 450))
		
		text = font.render("Hard", True, (0, 0, 0))
		screen.blit(text, (640, 450))
		
		text = font2.render("Game designed by Olly Crowe", True, (0, 0, 0))
		screen.blit(text, (25, 575))
		
		text = font3.render('Music: "At Launch" Kevin MacLeod (incompetech.com)', True, (0, 0, 0))
		screen.blit(text, (400, 550))
		
		text = font3.render("Licensed under Creative Commons: By Attribution 3.0 License", True, (0, 0, 0))
		screen.blit(text, (400, 565))
		
		text = font3.render("http://creativecommons.org/licenses/by/3.0/", True, (0, 0, 0))
		screen.blit(text, (400, 580))
		
		if pygame.Rect(150, 450, 160, 60).collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
			game = "playing"
			gamemode = "easy"
			next_bird_spawn = random.randrange(20, 31)
			next_bird_spawn /= 10
			guy.max_health = 7
			guy.health = guy.max_health
			game_start = time.time()
			area_enter = time.time()
			last_bird_spawn = time.time()
			area = 0
			area_length = random.randrange(20, 41)
			if first_time:
				pygame.mixer.music.play(-1)
			message = Message()
			first_time = False
		
		if pygame.Rect(350, 450, 250, 60).collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
			game = "playing"
			gamemode = "normal"
			next_bird_spawn = random.randrange(15, 26)
			next_bird_spawn /= 10
			guy.max_health = 5
			guy.health = guy.max_health
			game_start = time.time()
			area_enter = time.time()
			last_bird_spawn = time.time()
			area = 0
			area_length = random.randrange(20, 41)
			if first_time:
				pygame.mixer.music.play(-1)
			message = Message()
			first_time = False
		
		if pygame.Rect(640, 450, 175, 60).collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
			game = "playing"
			gamemode = "hard"
			next_bird_spawn = random.randrange(10, 21)
			next_bird_spawn /= 10
			guy.max_health = 3
			guy.health = guy.max_health
			game_start = time.time()
			area_enter = time.time()
			last_bird_spawn = time.time()
			area = 0
			area_length = random.randrange(20, 41)
			if first_time:
				pygame.mixer.music.play(-1)
			message = Message()
			first_time = False
	
	elif game == "dead":
	
		for far_hill in far_hills:
			far_hill.move()
			far_hill.draw()
		
		for close_hill in close_hills:
			close_hill.move()
			close_hill.draw()
		
		for bird in birds:
			bird.move()
			bird.draw()
		
		guy.x -= 6
		guy.y += 10
		screen.blit(guy1_image, (guy.x, guy.y))
		
		pygame.draw.rect(screen, (0, 0, 0), (25, 10, 750, 50), 5)
		pygame.draw.rect(screen, (255, 255, 0), (30, 15, 740/guy.max_health * guy.health, 40))
		for dash in range(1, guy.max_health):
			pygame.draw.line(screen, (0, 0, 0), ((750/guy.max_health * dash) + 23, 60), ((750/guy.max_health * dash) + 23, 35), 5)
		
		text = font.render(death_time + "m", True, (0, 0, 0))
		screen.blit(text, (800, 10))
		
		pygame.draw.line(screen, (0, 0, 0), (-1000, 200), (2000, 430), 2)
		
		if guy.y >= 1000:
			guy = Guy()
			far_hills = (Far_hill(0), Far_hill(1000))
			close_hills = (Close_hill(forest_hills_image, 0), Close_hill(forest_hills_image, 1000))
			birds = []
			game = "menu"
			
	pygame.display.update()