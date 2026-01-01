import pygame
import random
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('Space-Shooter', 'images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.direction = pygame.math.Vector2()
        self.speed = 300

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN] - keys[pygame.K_UP])

        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()

        if recent_keys[pygame.K_SPACE]:
            print("Laser")

# general setup
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
ICON = pygame.image.load(join('Space-Shooter', 'images', 'player.png'))
pygame.display.set_icon(ICON)
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.RESIZABLE) # create a window
pygame.display.set_caption("Space Invaders")
running = True
clock = pygame.time.Clock()

# surfaces

# plain surface
surf = pygame.Surface((100,200))
surf.fill('gray14')
x = 100


# images
# player_surface = pygame.image.load(join('Space-Shooter', 'images', 'player.png')).convert_alpha()
# player_rect = player_surface.get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
# player_direction = 1

all_sprites = pygame.sprite.Group()
player = Player(all_sprites)

# player_direction = pygame.math.Vector2()
# player_speed = 300

star_surface = pygame.image.load(join('Space-Shooter', 'images', 'star.png')).convert_alpha()
position = [(random.randint(0, WINDOW_WIDTH),random.randint(0, WINDOW_HEIGHT)) for i in range(0,20)]

meteor_surface = pygame.image.load(join('Space-Shooter', 'images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surface.get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))

laser_surface = pygame.image.load(join('Space-Shooter', 'images', 'laser.png')).convert_alpha()
laser_rect = laser_surface.get_frect(bottomleft=(20,WINDOW_HEIGHT-20))

while(running):
    # clock.tick(20) # sets the frame rate

    # dt = clock.tick() # time for one frame in ms (1/frame_rate)

    dt = clock.tick()/1000 # in sec

    # speed = frame_rate * dt * movement (frame rate independent speed)

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        #     print("space")
        # if event.type == pygame.MOUSEMOTION:
        #     # print(event.pos)
        #     player_rect.center = event.pos

    # inputs
    # player_rect.center = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    # if keys[pygame.K_RIGHT]:
    #     player_direction.x = 1
    
    # elif keys[pygame.K_LEFT]:
    #     player_direction.x = -1

    # elif keys[pygame.K_UP]:
    #     player_direction.y = -1
    
    # elif keys[pygame.K_DOWN]:
    #     player_direction.y = 1
    
    # else:
    #     player_direction.x = 0
    #     player_direction.y = 0

    # player_direction.x = int(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
    # player_direction.y = int(keys[pygame.K_DOWN] - keys[pygame.K_UP])

    # player_direction = player_direction.normalize() if player_direction else player_direction # if we do not normalize then diagonally the speed is root2 times
    # player_rect.center += player_direction * player_speed * dt

    # recent_keys = pygame.key.get_just_pressed()
    # if recent_keys[pygame.K_SPACE]:
    #     print("fire")

    all_sprites.update(dt)

    # draw the game

    # fill window with colour
    display_surface.fill('gray5')
    # x += 0.1                            # change the x coordinate in every frame

    # stars
    for i in range(0, 20):
        display_surface.blit(star_surface, position[i])

    display_surface.blit(meteor_surface, meteor_rect)
    display_surface.blit(laser_surface, laser_rect)

    # player_rect.x += player_direction * 0.5
    # if player_rect.right > WINDOW_WIDTH:
    #    player_rect.left += 0.1 # update the position by specifying the position of the left side
    
    # if player_rect.right > WINDOW_WIDTH or player_rect.left < 0:
    #     player_direction *= -1

    # player_rect.x += 20
    # player_rect.y -= 10
    # player_rect.center += (20, -10) # we cannot do this with a tuple

    # player_rect.center += player_direction * player_speed * dt

    # if player_rect.bottom >= WINDOW_HEIGHT or player_rect.top <= 0:
    #     player_direction.y *= -1
    # elif player_rect.left <= 0 or player_rect.right >= WINDOW_WIDTH:
    #     player_direction.x *= -1

    # display_surface.blit(player_surface, player_rect) # put the surface on the display surface

    all_sprites.draw(display_surface)         
        
    pygame.display.update()

pygame.quit()