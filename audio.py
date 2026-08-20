import pygame


class MusicManager:
    def __init__(self):
        self.tracks = {
            'menu': 'music/menu.ogg',
            'play': 'music/play.ogg',
            'boss': 'music/boss.ogg',
        }

        self.current_track = None
        self.volume = 0.4

    def play(self, track_name, force=False):
        if self.current_track == track_name and not force:
            pygame.mixer.music.unpause()
            return

        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.tracks[track_name])
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1, fade_ms=400)

        self.current_track = track_name

    def stop(self):
        if self.current_track is None:
            return

        pygame.mixer.music.fadeout(600)
        self.current_track = None
        
    def pause(self):
        pygame.mixer.music.pause()

    def resume(self):
        pygame.mixer.music.unpause()