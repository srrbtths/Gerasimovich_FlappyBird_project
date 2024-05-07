import pygame


class Pipe(pygame.sprite.Sprite):

    def __init__(self, x, y, position, pipe_gap, scroll_speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()
        self.scroll_speed = scroll_speed

        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True) # "перевернутая" труба сверху
            self.rect.bottomleft = [x, y - int(pipe_gap / 2)]
        elif position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 2)]

    # удаляем из памяти когда труба уходит за экран
    def update(self):
        self.rect.x -= self.scroll_speed
        if self.rect.right < 0:
            self.kill()