import pygame
class Bird(pygame.sprite.Sprite):

    def __init__(self, x, y, flying, game_over):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f"img/bird{num}.png")
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
        self.flying = flying
        self.game_over = game_over

    def update(self):

        if self.flying == True:
            # "падение" при полете
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 768:
                self.rect.y += int(self.vel)

        if self.game_over == False:
            # "прыжок" птицы
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # handle the animation
            flap_cooldown = 5
            self.counter += 1

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]

            # эмитация полета (наклон)
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)

        else:
            # птица "умирает"
            self.image = pygame.transform.rotate(self.images[self.index], -90)