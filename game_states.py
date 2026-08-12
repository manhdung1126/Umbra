import pygame
from portal import Portal


class State:
    def __init__(self, game):
        self.game = game

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass


class MenuState(State):
    def handle_event(self, event):
        action = self.game.main_menu.handle_event(event)
        if action == 'start':
            self.game.start_game()
        elif action == 'quit':
            self.game.running = False

    def update(self):
        self.game.main_menu.update()

    def draw(self, screen):
        self.game.main_menu.draw(screen)


class PlayingState(State):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            player = self.game.player
            if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                player.jump()
            if event.key == pygame.K_u:
                player.attack('attack1')
            if event.key == pygame.K_i:
                player.attack('attack2')
            if event.key == pygame.K_j:
                player.dash()
            if event.key == pygame.K_e:
                for chest in self.game.chests:
                    if chest.can_interact(player):
                        chest.open(player)

                portal = self.game.portal
                if portal and portal.can_interact(player):
                    self.game.advance_to_next_level()
                    return
            if event.key == pygame.K_ESCAPE:
                self.game.change_state('paused')

    def update(self):
        game = self.game
        player = game.player
        enemies = game.enemies
        boss = game.boss

        # Chests
        for chest in game.chests[:]:
            chest.update()

        # Player
        player.update(game.solid_platforms, game.all_platforms, game.LEVEL_WIDTH, game.LEVEL_HEIGHT)
        if not player.alive:
            for enemy in enemies:
                enemy.state = 'patrol'
                enemy.attacking = False
            if boss:
                boss.state = 'idle'
                boss.attacking = False
                boss.casting = False
            if player.frame_index >= len(player.animations['death']) - 1:
                game.change_state('game_over')

        # Enemies
        for enemy in enemies[:]:
            enemy.update(game.solid_platforms, game.all_platforms, player)

            if (not enemy.alive and enemy.status == 'death'
                    and enemy.frame_index >= len(enemy.animations.get('death', [])) - 2):
                if enemy in enemies:
                    enemies.remove(enemy)

        # Boss
        if boss:
            boss.update(game.solid_platforms, game.all_platforms, player)

            # Boss vừa chết -> mở cổng dịch chuyển cạnh vị trí spawn của boss
            if not boss.alive and not game.portal and game.boss_spawn_pos:
                spawn_x, spawn_y = game.boss_spawn_pos
                offset_x, offset_y = getattr(game, 'portal_offset', (300, 0))
                game.portal = Portal(spawn_x + offset_x, spawn_y + offset_y)

        # Portal
        if game.portal:
            game.portal.update()

        # Camera
        target_camera_x = player.hitbox.x - game.WIDTH * 0.45
        target_camera_x = max(0, min(target_camera_x, game.LEVEL_WIDTH - game.WIDTH))
        game.camera_x += (target_camera_x - game.camera_x) * 0.12

        target_camera_y = player.hitbox.centery - game.HEIGHT * 0.5
        target_camera_y = max(0, min(target_camera_y, game.LEVEL_HEIGHT - game.HEIGHT))
        game.camera_y += (target_camera_y - game.camera_y) * 0.12

        # Kiểm tra va chạm đòn tấn công của player
        if player.alive:
            attack_hitbox = player.get_attack_hitbox()
            if attack_hitbox:
                for enemy in enemies:
                    if (enemy.alive
                            and attack_hitbox.colliderect(enemy.hitbox)
                            and enemy not in player.enemies_hit_attack):
                        enemy.take_damage(10)
                        player.enemies_hit_attack.add(enemy)

                if (boss and boss.alive
                        and attack_hitbox.colliderect(boss.hitbox)
                        and boss not in player.enemies_hit_attack):
                    boss.take_damage(20)
                    player.enemies_hit_attack.add(boss)

        # Kiểm tra va chạm đòn tấn công của enemy
        for enemy in enemies:
            if enemy.alive:
                enemy_attack_hitbox = enemy.get_attack_hitbox()
                if enemy_attack_hitbox and not enemy.player_already_hit:
                    if enemy_attack_hitbox.colliderect(player.hitbox):
                        player.take_damage(enemy.attack_damage)
                        enemy.player_already_hit = True

        # Kiểm tra va chạm đòn tấn công của boss (melee + spell)
        if boss and boss.alive:
            boss_melee_hitbox = boss.get_attack_hitbox()
            if boss_melee_hitbox and not boss.player_already_hit:
                if boss_melee_hitbox.colliderect(player.hitbox):
                    player.take_damage(boss.melee_damage)
                    boss.player_already_hit = True

            for spell in boss.spells:
                spell_hitbox = spell.get_hitbox()
                if spell_hitbox and not spell.player_already_hit:
                    if spell_hitbox.colliderect(player.hitbox):
                        player.take_damage(spell.damage)
                        spell.player_already_hit = True

    def draw(self, screen):
        self.game.draw_game_scene(screen)


class PausedState(State):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_state('playing')
            return

        action = self.game.pause_menu.handle_event(event)
        if action == 'resume':
            self.game.change_state('playing')
        elif action == 'restart':
            self.game.restart_current_level()
        elif action == 'quit':
            self.game.change_state('menu')

    def update(self):
        self.game.pause_menu.update()

    def draw(self, screen):
        self.game.draw_game_scene(screen)
        self.game.pause_menu.draw(screen)


class GameOverState(State):
    def handle_event(self, event):
        action = self.game.game_over_menu.handle_event(event)
        if action == 'restart':
            self.game.restart_current_level()
        elif action == 'quit':
            self.game.change_state('menu')

    def update(self):
        self.game.game_over_menu.update()

    def draw(self, screen):
        self.game.draw_game_scene(screen)
        self.game.game_over_menu.draw(screen)


class VictoryState(State):
    def handle_event(self, event):
        action = self.game.victory_menu.handle_event(event)
        if action == 'play_again':
            self.game.start_game()
        elif action == 'quit':
            self.game.change_state('menu')

    def update(self):
        self.game.victory_menu.update()

    def draw(self, screen):
        self.game.draw_game_scene(screen)
        self.game.victory_menu.draw(screen)