from tools import colors, text_format, font


class GameStats:
    def __init__(self, game):
        self.game = game
        self.reset_stats()
        self.score = 0
        self.level = 1
        self.lives_left = self.game.settings.lives_limit

    def reset_stats(self):
        self.lives_left = self.game.settings.lives_limit
        self.score = 0
        self.level = 1

    def display_stats(self):
        text_score = text_format(f"SCORE  {self.score}", font, 14, colors['white'])
        self.game.screen.blit(text_score, (15, 10))

        text_level = text_format(f"LEVEL {self.level}", font, 14, colors['white'])
        self.game.screen.blit(text_level, (785, 10))

        text_lives = text_format(f"LIVES {self.lives_left}", font, 14, colors['white'])
        self.game.screen.blit(text_lives, (15, 970))

