from settings import * 
from sprites import *
from groups import AllSprites
from support import *
from gameTimer import Timer
from random import randint

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True

        # groups 
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        
        # load game
        self.load_assets()
        self.setup()
        
        # timer 
        self.bee_timer = Timer(2000, func=self.create_bee, autostart=True, repeat=True)

    def create_bee(self):
        Bee(groups = (self.all_sprites, self.enemy_sprites),
            frames = self.bee_frames,
            pos = ((self.level_width + WINDOW_WIDTH),(randint(0, self.level_height))), 
            speed=randint(300,500))

    def create_bullet(self, pos, direction):
        x = pos[0] + direction * 34 if direction == 1 else pos[0] + direction * 34 - self.bullet_surf.get_width()
        Bullet((self.all_sprites, self.bullet_sprites), (x, pos[1]), self.bullet_surf, direction)
        Fire(self.all_sprites, pos, self.fire_surf, self.player)
        self.audio['shoot'].play()

    def load_assets(self):
        # graphics
        self.player_frames = import_folder('Platformer', 'images', 'player')
        self.bullet_surf = import_image('Platformer', 'images', 'gun', 'bullet')
        self.fire_surf = import_image('Platformer', 'images', 'gun', 'fire')
        self.bee_frames = import_folder('Platformer', 'images', 'enemies', 'bee')
        self.worm_frames = import_folder('Platformer', 'images', 'enemies', 'worm')
        
        
        # sounds
        self.audio = audio_importer('Platformer', 'audio')

    def setup(self):
        map = load_pygame(join('Platformer', 'data', 'maps', 'world.tmx'))
        
        self.level_width = map.width * TILE_SIZE
        self.level_height = map.height * TILE_SIZE
        
        for x, y, image in map.get_layer_by_name('Main').tiles():
            Sprite((self.all_sprites, self.collision_sprites), (x * TILE_SIZE, y * TILE_SIZE), image)
            
        for x, y, image in map.get_layer_by_name('Decoration').tiles():
            Sprite(self.all_sprites, (x * TILE_SIZE, y * TILE_SIZE), image)
            
        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player(groups = self.all_sprites,
                                    pos = (obj.x, obj.y),
                                    collision_sprites = self.collision_sprites,
                                    frames = self.player_frames,
                                    create_bullet = self.create_bullet)
                
            if obj.name == 'Worm':
                Worm(groups=(self.all_sprites, self.enemy_sprites),
                    frames = self.worm_frames,
                    rect = pygame.FRect(obj.x, obj.y, obj.width, obj.height))
        
        self.audio['music'].play(loops = -1)
        
    def collision(self):
        # bullets and enemies
        for bullet in self.bullet_sprites:
            sprite_collision = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
            if sprite_collision:
                self.audio['impact'].play()
                bullet.kill()
                for sprite in sprite_collision:
                    sprite.destroy()
        
        # enemies and player
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False
        
    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000 

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
            
            # update
            self.bee_timer.update()
            self.all_sprites.update(dt)
            self.collision()

            # draw 
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run() 