if self.invulnerable and pygame.time.get_ticks() % 200 < 100:
            return
        screen.blit(self.image, self.rect)