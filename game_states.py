import pygame


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
            if event.key == pygame.K_ESCAPE:
                self.game.change_state('paused')

    def update(self):
        game = self.game
        player = game.player
        enemies = game.enemies

        # Player
        player.update(game.solid_platforms, game.all_platforms, game.LEVEL_WIDTH)
        if not player.alive:
            for enemy in enemies:
                enemy.state = 'patrol'
                enemy.attacking = False
            if player.frame_index >= len(player.animations['death']) - 1:
                game.change_state('game_over')

        # Enemies
        for enemy in enemies[:]:
            enemy.update(game.solid_platforms, game.all_platforms, player)

            if (not enemy.alive and enemy.status == 'death'
                    and enemy.frame_index >= len(enemy.animations.get('death', [])) - 2):
                if enemy in enemies:
                    enemies.remove(enemy)

        # Camera
        target_camera_x = player.hitbox.x - game.WIDTH * 0.45
        target_camera_x = max(0, min(target_camera_x, game.LEVEL_WIDTH - game.WIDTH))
        game.camera_x += (target_camera_x - game.camera_x) * 0.12

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

        # Kiểm tra va chạm đòn tấn công của enemy
        for enemy in enemies:
            if enemy.alive:
                enemy_attack_hitbox = enemy.get_attack_hitbox()
                if enemy_attack_hitbox and not enemy.player_already_hit:
                    if enemy_attack_hitbox.colliderect(player.hitbox):
                        player.take_damage(enemy.attack_damage)
                        enemy.player_already_hit = True

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
            self.game.start_game()
        elif action == 'quit':
            self.game.change_state('menu')

    def update(self):
        self.game.game_over_menu.update()

    def draw(self, screen):
        self.game.draw_game_scene(screen)
        self.game.game_over_menu.draw(screen)