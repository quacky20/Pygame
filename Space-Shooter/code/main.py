import pygame
import random
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('Space-Shooter', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.direction = pygame.math.Vector2()
        self.speed = 500
        
        # Countdown Timer
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
        
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True            

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) | int(keys[pygame.K_d] - keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_DOWN] - keys[pygame.K_UP]) | int(keys[pygame.K_s] - keys[pygame.K_w])

        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()

        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser((all_sprites, laser_sprites), laser_surface, self.rect.midtop)
            self.can_shoot=False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()
            
        self.laser_timer()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(random.randint(0, WINDOW_WIDTH),random.randint(0, WINDOW_HEIGHT)))
  
class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        
    def update(self, dt):
        self.rect.centery -= 400 * dt 
        if self.rect.bottom < 0:
            self.kill()
            
class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.original_surf = surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.math.Vector2(random.uniform(-0.5, 0.5), 1)
        self.speed = random.randint(400, 500)
        self.rotation = 0
        self.rotate_speed = random.choice([-1,1]) * random.randint(40, 80)
        
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
            
        self.rotation += self.rotate_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)
        
class Explosion(pygame.sprite.Sprite):
    def __init__(self, groups, frames, pos):
        super().__init__(groups)
        self.image = frames[0]
        self.rect = self.image.get_frect(center = pos)
        self.frames = frames
        self.frame_index = 0
        
    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()
        
def collisions():
    global running
    if pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask):
        running = False

    for laser in laser_sprites:
        collided_sprite = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprite:
            laser.kill()
            Explosion(all_sprites, explosion_frames, laser.rect.midtop)
            explosion_sound.play()
        
def display_score():
    current_score = pygame.time.get_ticks() // 100
    text_surface = font.render(str(current_score), True, "#fefff1")
    text_rect = text_surface.get_frect(midbottom = (WINDOW_WIDTH/2, WINDOW_HEIGHT - 50))
    pygame.draw.rect(display_surface, '#fefff1', text_rect.inflate(30, 20).move(0, -5), 5, 10)
    display_surface.blit(text_surface, text_rect)
    
# General Setup
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
ICON = pygame.image.load(join('Space-Shooter', 'images', 'player.png'))
pygame.display.set_icon(ICON)
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Space Invaders")
running = True
clock = pygame.time.Clock()

# imports
star_surf = pygame.image.load(join('Space-Shooter', 'images', 'star.png')).convert_alpha()
meteor_surface = pygame.image.load(join('Space-Shooter', 'images', 'meteor.png')).convert_alpha()
laser_surface = pygame.image.load(join('Space-Shooter', 'images', 'laser.png')).convert_alpha()
font = pygame.font.Font(join('Space-Shooter', 'images', 'Oxanium-Bold.ttf'), 40)
explosion_frames = [pygame.image.load(join('Space-Shooter', 'images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]

laser_sound = pygame.mixer.Sound(join('Space-Shooter', 'audio', 'laser.wav'))
laser_sound.set_volume(0.6)
explosion_sound = pygame.mixer.Sound(join('Space-Shooter', 'audio', 'explosion.wav'))
explosion_sound.set_volume(0.6)
game_music = pygame.mixer.Sound(join('Space-Shooter', 'audio', 'game_music.wav'))
game_music.set_volume(0.2)

game_music.play(loops=-1)

all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
for i in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)


# Custom events -> Meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while(running):
    dt = clock.tick()/1000 # in sec

    # Event Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == meteor_event:
            x, y = random.randint(0, WINDOW_WIDTH), random.randint(-200, -100)
            Meteor((all_sprites, meteor_sprites), meteor_surface, (x, y))
            
    # Updates
    all_sprites.update(dt)
    collisions()

    # Drawing
    display_surface.fill("#241929")
    display_score()
    all_sprites.draw(display_surface)
    
    pygame.display.update()

pygame.quit()