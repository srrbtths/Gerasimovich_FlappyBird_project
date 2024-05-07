import pygame
import random
import pygame_gui
import database

from bird_class import Bird
from pipe_class import Pipe
from button_class import Button

def draw_text(text, font, text_col, x, y, screen):
    img = font.render(str(text), True, text_col)
    text_rect = img.get_rect(center=(x / 2, y))
    screen.blit(img, text_rect)

    img = font.render(str(text), True, text_col)

def reset_game(pipe_group, flappy, screen_height):
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    score = 0

    return score

def main():

    pygame.init()

    screen_width = 864
    screen_height = 936
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Flappy Bird')

    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((screen_width, screen_height))

    input_text_rect = pygame.Rect((screen_width // 2 - 150, screen_height // 2 - 25), (300, 50))
    input_text_rect.center = (screen_width // 2, screen_height // 2 - 150)
    input_text = pygame_gui.elements.UITextEntryBox(
        relative_rect=input_text_rect,
        manager=manager,
        object_id='#name_entry'
    )

    pipe_gap = 200
    pipe_frequency = 1500
    last_pipe = pygame.time.get_ticks() - pipe_frequency
    score = 0
    count_for_sound = 1
    pass_pipe = False

    # загрузка изображений
    bg = pygame.image.load('img/background.png')
    ground_img = pygame.image.load('img/ground.png')
    res_button_img = pygame.image.load('img/restart.png')
    start_button_img = pygame.image.load('img/start.png')
    exit_button_img = pygame.image.load('img/exit.png')

    # анимация пола
    ground_scroll = 0
    scroll_speed = 5
    level_up = 5

    flying = False
    game_over = False

    pipe_group = pygame.sprite.Group()
    bird_group = pygame.sprite.Group()

    flappy = Bird(100, int(screen_height / 2), flying, game_over)
    bird_group.add(flappy)

    # кнопки
    rest_button = Button(screen_width, screen_height // 2 + 150, res_button_img, screen)
    start_button = Button(screen_width, screen_height // 2, start_button_img, screen)
    exit_button = Button(screen_width, screen_height // 2 + 130, exit_button_img, screen)

    start = False
    run = True
    user_name = ''

    while run:
        UI_REFRESH_RATE = clock.tick(60)/1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and start and flappy.flying == False and flappy.game_over == False:
                flappy.flying = True
            if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED or event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                user_name = input_text.get_text()
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                input_text._set_visible(False)

            manager.process_events(event)

        manager.update(UI_REFRESH_RATE)
        screen.blit(bg, (0, 0))

        pipe_group.draw(screen)
        bird_group.draw(screen)
        bird_group.update()

        if start == False:
            draw_text('enter your name', pygame.font.SysFont('Bauhaus 93', 60),
                      (255,255,255), screen_width, 250, screen)

            manager.draw_ui(screen)
            if start_button.draw():
                if user_name != '':
                    start = True
                    flappy.flying = True
            if exit_button.draw():
                run = False

        # перемещение "пола"
        screen.blit(ground_img, (ground_scroll, 768))

        # счетчик
        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                    and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                    and pass_pipe == False:
                pass_pipe = True
            if pass_pipe == True:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    pass_pipe = False
                    pygame.mixer.music.load('snd/flappy.mp3')
                    pygame.mixer.music.play(0)

                    if score >= level_up:
                        scroll_speed += 0.5
                        level_up += 5

        draw_text(str(score), pygame.font.SysFont('Bauhaus 93', 60),
                      (255,255,255), screen_width, 40, screen)
        draw_text(user_name, pygame.font.SysFont('bahnschrift', 60, True),
                      (255,255,255), screen_width - 650, 40, screen)


        # обработка удара о трубу и потолок
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            if count_for_sound > 0:
                pygame.mixer.music.load('snd/drop.mp3')
                pygame.mixer.music.play()
                count_for_sound -= 1
            flappy.game_over = True

        # обработка удара об пол
        if flappy.rect.bottom >= 768:
            if count_for_sound > 0:
                pygame.mixer.music.load('snd/drop.mp3')
                pygame.mixer.music.play()
                count_for_sound -= 1
            flappy.game_over = True
            flappy.flying = False


        if flappy.flying == True and flappy.game_over == False:

            # генерация труб
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, -1, pipe_gap, scroll_speed)
                top_pipe = Pipe(screen_width, int(screen_height / 2) + pipe_height, 1, pipe_gap, scroll_speed)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now

            pipe_group.update()

            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0

        # check for game over and reset
        if flappy.game_over == True:
            draw_text('TOP PLAYERS:', pygame.font.SysFont('Bauhaus 93', 60),
                      (255,255,255), screen_width, screen_height // 2 -200, screen)
            top_score = database.add_score(user_name, score)
            y = screen_height // 2 - 100
            for name, max_score in top_score:
                draw_text(f"{name}: {max_score}", pygame.font.SysFont('bahnschrift', 40), (0, 128, 0),
                          screen_width, y, screen)
                y += 35
            if rest_button.draw():
                flappy.game_over = False
                flappy.flying = True
                score = reset_game(pipe_group,flappy, screen_height)
                count_for_sound = 1
                level_up = 5
                scroll_speed = 4


        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()