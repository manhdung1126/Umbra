import pygame
from boss import Boss
from support import import_sprite_sheet
from spell import Spell

class WitchBoss(Boss):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hitbox = pygame.Rect(0, 0, 160, 240)
        self.hitbox.bottomleft = (x, y)
        self.sprite_offset_x = -145
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)

        self.max_health = 1
        self.health = self.max_health
        self.attacking = False
        self.melee_damage = 100
        self.attack_range = 250
        self.attack_chase = 500
        self.melee_time = 0
        self.melee_cooldown = 1800
        self.animation_speed_melee = 0.2

        self.casting = False
        self.spells = []
        self.spell_damage = 50
        self.cast_cooldown = 2500
        self.cast_time = 0
        self.cast_spawn_frame = 6
        self.spell_spawned = False
        self.spell_target_x = 0
        self.spell_ground_y = 0
        self.spell_width = 140
        self.spell_height = 240
        self.spell_hit_frames = [7,8,9,10,11]
        self.animation_speed_cast = 0.15

        self.status = 'idle'
        self.state = 'idle'
        self.notice_radius = 600
        self.give_up_radius = 1000
        self.chase_speed = 2.5
        

    def import_assets(self):
        FRAME_WIDTH = 140
        FRAME_HEIGHT = 93
        SCALE = 4
        self.animations = {
            'idle' : import_sprite_sheet('graphics/boss2/idle.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
            'walk' : import_sprite_sheet('graphics/boss2/walk.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
            'hurt' : import_sprite_sheet('graphics/boss2/hurt.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
            'death' : import_sprite_sheet('graphics/boss2/death.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
            'attack' : import_sprite_sheet('graphics/boss2/attack.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
            'cast' : import_sprite_sheet('graphics/boss2/cast.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
            'spell' : import_sprite_sheet('graphics/boss2/spell.png', FRAME_WIDTH, FRAME_HEIGHT, SCALE),
        }

    def patrol(self):
        pass

    def start_melee(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.melee_time < self.melee_cooldown:
            return False

        self.state = 'melee'
        self.attacking = True
        self.casting = False
        self.melee_time = current_time
        self.frame_index = 0
        self.player_already_hit = False
        return True

    def start_cast(self, player):
        current_time = pygame.time.get_ticks()

        if current_time - self.cast_time < self.cast_cooldown:
            return False

        self.state = 'cast'
        self.casting = True
        self.attacking = False
        self.cast_time = current_time
        self.frame_index = 0
        self.spell_spawned = False

        # Khóa vị trí player khi boss bắt đầu cast
        self.spell_target_x = player.hitbox.centerx
        self.spell_ground_y = player.hitbox.bottom
        return True

    def face_player(self, player):
        self.facing_right = player.hitbox.centerx > self.hitbox.centerx
        self.direction = 1 if self.facing_right else -1


    def update_state(self, player, platforms):
        pass

    def choose_action(self, player, all_platforms):
        if self.attacking or self.casting or self.hurt:
            return

        distance_x = self.get_distance_horizontal_to_player(player)
        can_interact = self.can_interact_with_player(player, all_platforms)

        self.face_player(player)

        if distance_x > self.notice_radius:
            self.state = 'idle'

        elif not can_interact:
            self.start_cast(player)

        elif distance_x <= self.attack_range:
            self.start_melee()

        elif distance_x <= self.attack_chase:
            self.state = 'chase'

        else:
            self.start_cast(player)

    def chase_player(self, player):
        distance_x = self.get_distance_horizontal_to_player(player)
        
        if distance_x > self.attack_range:
            self.hitbox.x += self.direction * self.chase_speed

    def get_attack_hitbox(self):
        if not self.attacking:
            return None

        current_frame = int(self.frame_index)
        if current_frame not in [6, 7, 8, 9]:
            return None

        attack_width = 300
        attack_height = 120

        if self.facing_right:
            attack_hitbox = pygame.Rect(self.hitbox.right - 80, 
                                        self.hitbox.centery,
                                        attack_width, attack_height
                                        )
        else :
            attack_hitbox = pygame.Rect(self.hitbox.left - attack_width + 80, 
                                        self.hitbox.centery,
                                        attack_width, attack_height
                                        )
        
        return attack_hitbox

    def spawn_spell(self):
        if not self.casting or self.spell_spawned:
            return

        if int(self.frame_index) >= self.cast_spawn_frame:
            spell = Spell(
                x=self.spell_target_x,
                ground_y=self.spell_ground_y,
                animations=self.animations['spell'],
                damage=self.spell_damage,
                hit_frames=self.spell_hit_frames,
                width=self.spell_width,
                height=self.spell_height,
            )

            self.spells.append(spell)
            self.spell_spawned = True

    def update_spells(self): 
        for spell in self.spells[:]:
            spell.update()
            if spell.finished:
                self.spells.remove(spell)

    def get_status(self):
        if not self.alive:
            self.status = 'death'
        elif self.hurt:
            self.status = 'hurt'
        elif self.casting:
            self.status = 'cast'
        elif self.attacking:
            self.status = 'attack'
        elif self.state == 'chase':
            self.status = 'walk'
        else:
            self.status = 'idle'

    def animate(self):
        animation = self.animations[self.status]

        if self.status == 'cast':
            self.frame_index += self.animation_speed_cast
        elif self.status == 'attack':
            self.frame_index += self.animation_speed_melee
        else:
            self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            if self.status == 'death':
                self.frame_index = len(animation) - 1
            else:
                self.frame_index = 0
                if self.status == 'hurt':
                    self.hurt = False

            if self.status == 'attack':
                self.attacking = False
                self.state = 'idle'

            elif self.status == 'cast':
                self.casting = False
                self.state = 'idle'

        self.image = animation[int(self.frame_index)]

        if self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
            
        self.rect = self.image.get_rect()
        self.rect.bottom = self.hitbox.bottom
        
        if self.facing_right:
            self.rect.centerx = self.hitbox.centerx - self.sprite_offset_x
        else:
            self.rect.centerx = self.hitbox.centerx + self.sprite_offset_x

    def update(self, solid_platforms, all_platforms, player):
        if not self.alive:
            self.animate()
            return

        self.choose_action(player, all_platforms)

        if self.state == 'chase' and not self.attacking and not self.casting:
            self.chase_player(player)

            hit_wall = self.check_collision(solid_platforms)

            if hit_wall:
                self.start_cast(player)
        else:
            self.check_collision(solid_platforms)

        self.check_vertical_collisions(all_platforms)
        self.apply_gravity()

        self.spawn_spell()
        self.update_spells()
        self.get_status()
        self.update_poise()
        self.animate()

    def draw(self, screen, cam_x, cam_y):
        for spell in self.spells:
            spell.draw(screen, cam_x, cam_y)
        super().draw(screen, cam_x, cam_y)
        
            