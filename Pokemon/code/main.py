from settings import *
from support import *
from gameTimer import Timer
from monster import *
from random import choice, sample
from ui import *
from attack import AttackAnimationSprite

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Pokemon')
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 30)
        self.import_assets()
        self.audio['music'].play(loops = -1)
        self.player_active = True
        self.died = None

        # groups 
        self.all_sprites = pygame.sprite.Group()
        
        # data
        player_monster_list = sample(list(MONSTER_DATA.keys()), 3)
        self.player_monster = [Monster(name, self.back_surfs[name]) for name in player_monster_list]
        self.monster = self.player_monster[0]
        self.all_sprites.add(self.monster)
        opponent_name = choice(list(MONSTER_DATA.keys()))
        self.opponent = Opponent(self.all_sprites, opponent_name, self.front_surfs[opponent_name])
        
        # ui
        self.ui = UI(self.monster, self.player_monster, self.simple_surfs, self.get_input)
        self.opponent_ui = OpponentUI(self.opponent)
        
        # timers
        self.timers = {'player end': Timer(2000, func = self.opponent_turn), 'opponent end': Timer(2000, func = self.player_turn), 'attack info': Timer(750), 'more info': Timer(750)}

    def get_input(self, state, data = None,):
        if state == 'attack':
            self.apply_attack(self.opponent, data)
            
        elif state == 'heal':
            self.monster.health += 50
            AttackAnimationSprite(self.all_sprites, self.monster, self.attack_frames['green'])
            self.audio['green'].play()
            
        elif state == 'switch':
            self.monster.kill()
            self.monster = data
            self.all_sprites.add(self.monster)
            self.ui.monster = self.monster
            
        elif state == 'escape':
            self.running = False
            
        self.player_active = False
        self.timers['player end'].activate()
            
    def apply_attack(self, target, attack):
        attack_data = ABILITIES_DATA[attack]
        attack_multiplier = ELEMENT_DATA[attack_data['element']][target.element]
        
        target.health -= attack_data['damage'] * attack_multiplier
        
        AttackAnimationSprite(self.all_sprites, target, self.attack_frames[attack_data['animation']])
        self.timers['attack info'].activate()
        self.attack_message = f'{self.monster.name} used {attack}' if target == self.opponent else f'{self.opponent.name} used {attack}'
        
        self.audio[attack_data['animation']].play()

    def attack_info(self):
        text_surf = self.font.render(self.attack_message, True, COLORS['black'])
        text_rect = text_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 40))
        self.display_surface.blit(text_surf, text_rect)
        
    def more_info(self):
        if self.died:
            text_surf = self.font.render(f'{self.died} died', True, COLORS['black'])
            text_rect = text_surf.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
            self.display_surface.blit(text_surf, text_rect)
        
    def opponent_turn(self):
        if self.opponent.health <= 0:
            self.player_active = True
            self.opponent.kill()
            self.died = self.opponent.name
            self.timers['more info'].activate()
            monster_name = choice(list(MONSTER_DATA.keys()))
            self.opponent = Opponent(self.all_sprites,monster_name, self.front_surfs[monster_name])
            self.opponent_ui.monster = self.opponent
        else:
            attack = choice(self.opponent.abilities)
            self.apply_attack(self.monster, attack)
            self.timers['opponent end'].activate()
            
            if self.monster.health <= 0:
                available_monsters = [monster for monster in self.player_monster if monster.health > 0]
                if available_monsters:
                    self.died = self.monster.name
                    self.timers['more info'].activate()
                    self.monster.kill()
                    self.monster = available_monsters[0]
                    self.all_sprites.add(self.monster)
                    self.ui.monster = self.monster
                else:
                    self.running = False
    
    def player_turn(self):
        self.player_active = True

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def import_assets(self):
        self.back_surfs = folder_importer('Pokemon', 'images', 'back')
        self.front_surfs = folder_importer('Pokemon', 'images', 'front')
        self.bg_surfs = folder_importer('Pokemon', 'images', 'other')
        self.simple_surfs = folder_importer('Pokemon', 'images', 'simple')
        self.attack_frames = tile_importer(4, 'Pokemon', 'images', 'attacks')
        self.audio = audio_importer('Pokemon', 'audio')
        
    def draw_monster_floor(self):
        for sprite in self.all_sprites:
            if isinstance(sprite, Creature):
                floor_rect = self.bg_surfs['floor'].get_frect(center = sprite.rect.midbottom + pygame.math.Vector2(0, - 10))
                self.display_surface.blit(self.bg_surfs['floor'], floor_rect)
    
    def run(self):
        while self.running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
           
            # update
            self.update_timers()
            self.all_sprites.update(dt)
            if self.player_active:
                self.ui.update()

            # draw  
            self.display_surface.blit(self.bg_surfs['bg'], (0, 0))
            self.draw_monster_floor()
            self.all_sprites.draw(self.display_surface)
            self.ui.draw()
            if self.timers['attack info'].active:
                self.attack_info()
            if self.timers['more info'].active:
                self.more_info()
            self.opponent_ui.draw()
            pygame.display.update()
        
        pygame.quit()
    
if __name__ == '__main__':
    game = Game()
    game.run()