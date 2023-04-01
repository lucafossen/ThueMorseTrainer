import pygame
import pygame.freetype
import pygame.time
from pygame.constants import MOUSEBUTTONUP
from pygame.constants import KEYUP, K_r#, RESIZABLE, VIDEORESIZE
from pygame.locals import K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT, Color
from game import Game
from indicator import Indicator

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
BORDER_WIDTH = 25
ARROW_Y = 363
ARROW_X_PAD = 138
TIME_ACC = 2

# Colors
IDLE_COLOR = (220, 220, 200)
BORDER_COLOR = (240, 240, 240)
TRUE_COLOR = (100, 255, 59)
MILESTONE_COLOR = (255, 209, 0)
MILESTONE_OTHER_COLOR = (255, 232, 179)
MILESTONE_TOP_COLOR = (255, 222, 102)
FALSE_COLOR = (255, 0, 48)
MORE_FALSE_COLOR = (200, 0, 10)
FALSE_COLOR_BUTTON = (231, 155, 165)
ACTIVE_COLOR = (165, 255, 155)
HIGHSCORE_MENU_COLOR = (90, 60, 60)
HIGHSCORE_COLOR = HIGHSCORE_MENU_COLOR
TIME_COLOR = (90, 60, 60)
ARROW_COLOR = (150, 140, 140)

# Fonts
pygame.freetype.init()
SCORE_FONT = pygame.freetype.Font("font/Montserrat-Regular.ttf", 128)
BUTTON_FONT = pygame.freetype.Font("font/Montserrat Regular 400.ttf", 17)
HIGHSCORE_FONT = pygame.freetype.Font("font/Montserrat-Regular.ttf", 32)
TUTORIAL_FONT = pygame.freetype.Font("font/Montserrat-Regular.ttf", 26)
TIME_FONT = pygame.freetype.Font("font/Montserrat-Regular.ttf", 20)
# ... rest of the code ...


def handle_events(game):
    global running, left_indicator, right_indicator, game_indicator
    for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == K_ESCAPE:
                    game.update_highscore(game.game_time)
                    running = False
                # Update game state and paddle colors
                elif event.key == K_LEFT:
                    game.process_action("left")
                    if game.lost:
                        left_indicator.color = FALSE_COLOR
                    elif ((game.pattern_pos) & (game.pattern_pos-1) == 0):
                        left_indicator.color = MILESTONE_COLOR
                        right_indicator.color = MILESTONE_OTHER_COLOR
                        game_indicator.color = MILESTONE_TOP_COLOR
                    else:
                        left_indicator.color = TRUE_COLOR
                        game_indicator.color = TRUE_COLOR
                elif event.key == K_RIGHT:
                    game.process_action("right")
                    if game.lost:
                        right_indicator.color = FALSE_COLOR
                    elif ((game.pattern_pos) & (game.pattern_pos-1) == 0):
                        right_indicator.color = MILESTONE_COLOR
                        left_indicator.color = MILESTONE_OTHER_COLOR
                        game_indicator.color = MILESTONE_TOP_COLOR
                    else:
                        right_indicator.color = TRUE_COLOR
                        game_indicator.color = TRUE_COLOR

                if event.key == K_r:
                    game.update_highscore(game.game_time)
                    game.__init__()
                    for i in (game_indicator, left_indicator, right_indicator):
                            i.color = ACTIVE_COLOR

            elif event.type == KEYUP:
                if event.key == K_LEFT and not game.lost:
                    left_indicator.correct = None
                    game_indicator.correct = None
                elif event.key == K_RIGHT and not game.lost:
                    right_indicator.correct = None
                    game_indicator.correct = None

                #elif event.key == K_r:
                    # for i in (game_indicator, left_indicator, right_indicator):
                    #    i.color = i.default_color
            elif event.type == MOUSEBUTTONUP:
                if left_indicator.fill_rect.collidepoint(pygame.mouse.get_pos()):
                    game.process_action("left")
                    if not game.lost:
                        left_indicator.color = TRUE_COLOR
                        game_indicator.color = TRUE_COLOR
                    else:
                        left_indicator.color=FALSE_COLOR
                elif right_indicator.fill_rect.collidepoint(pygame.mouse.get_pos()):
                    game.process_action("right")
                    if not game.lost:
                        right_indicator.color = TRUE_COLOR
                        game_indicator.color = TRUE_COLOR
                    else:
                        right_indicator.color = FALSE_COLOR
                elif restart_button.fill_rect.collidepoint(pygame.mouse.get_pos()):
                    game.update_highscore(game.game_time)
                    game.__init__()
                    for i in (game_indicator, left_indicator, right_indicator):
                            i.color = ACTIVE_COLOR
                elif quit_button.fill_rect.collidepoint(pygame.mouse.get_pos()):
                    game.update_highscore(game.game_time)
                    running = False

            # TODO: add resize support
            # elif event.type == VIDEORESIZE:
            # pass

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                game.update_highscore(game.game_time)
                running = False

def update_game_state(game):
    """Will be implemented in the future
    """
    # Update game state
    pass

def render(game):
    global screen, clock, left_indicator, right_indicator, game_indicator, restart_button, quit_button, running
    # Animation logic

    # lagcomp makes sure the colors don't drift off
    # when moving/resizing the window
    lagcomp = clock.get_time()
    if lagcomp > 100:
        lagcomp = 100

    if game.lost:
        left_indicator.recolor(5*lagcomp, FALSE_COLOR_BUTTON)
        right_indicator.recolor(5*lagcomp, FALSE_COLOR_BUTTON)
        game_indicator.recolor(5*lagcomp, FALSE_COLOR)
    else:
        for indicator in (left_indicator, right_indicator):
            # Button fade animation
            if indicator.correct:
                indicator.recolor(0.5*lagcomp, IDLE_COLOR)#, tot=1000)
            elif indicator.correct == None:
                indicator.recolor(5*lagcomp, IDLE_COLOR)
            else:
                indicator.recolor(5*lagcomp, MORE_FALSE_COLOR)# tot=1000)

        game_indicator.recolor(0.5*lagcomp, target=IDLE_COLOR)

    if game_indicator.correct != False and game.pattern_pos != 0:
        game_indicator.recolor(5*lagcomp, target=IDLE_COLOR)#, tot=900)

    # Lower intro volume if game is started early
    if game.started and game.dynamic_rvol != 0:
        game.fade_restart_volume()

    game_indicator.draw()
    left_indicator.draw()
    right_indicator.draw()

    # Drawing paddle arrows (Should i make a function for this?)
    if not game.started:
        #left arrow
        pygame.draw.line(screen, ARROW_COLOR, (ARROW_X_PAD-25, ARROW_Y), (ARROW_X_PAD, ARROW_Y-25), 8)
        pygame.draw.line(screen, ARROW_COLOR, (ARROW_X_PAD-25, ARROW_Y), (ARROW_X_PAD, ARROW_Y+25), 8)
        pygame.draw.line(screen, ARROW_COLOR, (ARROW_X_PAD-25, ARROW_Y), (ARROW_X_PAD+35, ARROW_Y), 5)
        # right arrow
        pygame.draw.line(screen, ARROW_COLOR, (SCREEN_WIDTH-(ARROW_X_PAD-25), ARROW_Y), (SCREEN_WIDTH-ARROW_X_PAD, ARROW_Y-25), 8)
        pygame.draw.line(screen, ARROW_COLOR, (SCREEN_WIDTH-(ARROW_X_PAD-25), ARROW_Y), (SCREEN_WIDTH-ARROW_X_PAD, ARROW_Y+25), 8)
        pygame.draw.line(screen, ARROW_COLOR, (SCREEN_WIDTH-(ARROW_X_PAD-25), ARROW_Y), (SCREEN_WIDTH-(ARROW_X_PAD+35), ARROW_Y), 5)

    # Font renders:
    # Game not in progress
    if not game.in_progress:
        # Render high score
        if game.get_highscore() > 0:
            HIGHSCORE_FONT.render_to(screen, (SCREEN_WIDTH/18, SCREEN_HEIGHT/15), f"high: {game.get_highscore()}", fgcolor=HIGHSCORE_COLOR)
        # Render restart and quit button
        restart_button.draw()
        BUTTON_FONT.render_to(screen, (46, 159), 'restart')
        quit_button.draw()
        BUTTON_FONT.render_to(screen, (55, 202), 'quit')

    # After loss
    if game.lost:
        time_str = str(f"{round(game.game_time, TIME_ACC)}s ({round(game.pattern_pos/game.game_time, TIME_ACC)} bits per second)")
        TIME_FONT.render_to(screen, (SCREEN_WIDTH/2-TIME_FONT.get_rect(time_str)[2]/2, SCREEN_HEIGHT/2.42), time_str, fgcolor=TIME_COLOR)
        TUTORIAL_FONT.render_to(screen, (SCREEN_WIDTH/2-TUTORIAL_FONT.get_rect("r to restart")[2]/2, SCREEN_HEIGHT/2.88), "r to restart")
    SCORE_FONT.render_to(screen, (SCREEN_WIDTH/2-SCORE_FONT.get_rect(str(game.pattern_pos))[2]/2, SCREEN_HEIGHT/10), str(game.pattern_pos))

    pygame.display.update()
    clock.tick_busy_loop()

def main():
    global screen, clock, left_indicator, right_indicator, game_indicator, restart_button, quit_button, running
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # , RESIZABLE)
    icon = pygame.image.load("icon/icon.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Thue Morse Trainer')

    # TODO: this can probably be much smaller
    # LEFT
    left_indicator = Indicator(screen,
    (BORDER_WIDTH/2,
    SCREEN_HEIGHT/2,
    SCREEN_WIDTH/2-(BORDER_WIDTH/1.5+1),
    SCREEN_HEIGHT/2-BORDER_WIDTH/2+1))


    # RIGHT
    right_indicator = Indicator(screen,
    (SCREEN_WIDTH/2+(BORDER_WIDTH/3+2),
    SCREEN_HEIGHT/2,
    SCREEN_WIDTH/2-(BORDER_WIDTH/3+BORDER_WIDTH/2+1),
    SCREEN_HEIGHT/2-BORDER_WIDTH/2+1))

    # TOP
    game_indicator = Indicator(screen,
    (0+BORDER_WIDTH/2,
    0+BORDER_WIDTH/2,
    SCREEN_WIDTH-BORDER_WIDTH,
    SCREEN_HEIGHT/2-BORDER_WIDTH))

    # Restart
    restart_button = Indicator(screen, (25, 150, 100, 30), (200, 190, 170), border_width=4)
    quit_button = Indicator(screen, (25, 195, 100, 30), (200, 190, 170), border_width=4)

    # Initialize game objects
    game = Game()
    clock = pygame.time.Clock()

    # Main game loop
    running = True
    while running:
        handle_events(game)
        update_game_state(game)
        render(game)

if __name__ == '__main__':
    main()