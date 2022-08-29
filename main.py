# Rules of the game can be found in inverting_pattern.py
from pygame.constants import MOUSEBUTTONUP

def main():
    from pygame.constants import KEYUP, K_r#, RESIZABLE, VIDEORESIZE
    from game import Game
    from indicator import Indicator
    import pygame
    import pygame.time
    pygame.init()
    pygame.freetype.init()

    from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    Color
    )
    
    screen_width = 600
    screen_height = 500
    screen = pygame.display.set_mode((screen_width, screen_height)) # , RESIZABLE)
    icon = pygame.image.load("icon/icon.png")
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Blaauw-Fossen Algogame')

    
    idle_color = Color(220, 220, 200)#Color(225, 225, 225) # TODO: why is this grey?
    border_color = Color(240, 240, 240)
    true_color = Color(100, 255, 59)
    milestone_color = Color(255, 209, 0)
    milestone_other_color = Color(255, 232, 179)
    milestone_top_color = Color(255, 222, 102)
    false_color = Color(255, 0, 48)
    more_false_color = Color(200, 0, 10)
    false_color_button = Color(231, 155, 165)
    active_color = Color(165, 255, 155)
    
    highscore_menu_color = Color(90, 60, 60) # TODO: Rediscover why I made this variable
    highscore_color = highscore_menu_color
    time_color = Color(90, 60, 60)
    # TODO: rediscover why I made these variables
    # random_color_range = 20
    # game_resting_color = Color(50, 225, 50)
    # midwidth = screen_width/2+border_width/4

    border_width = 25

    # Arrow settings
    arrow_y = 363
    arrow_x_pad = 138
    arrow_color = Color(150, 140, 140)

    # TODO: this can probably be much smaller
    # LEFT
    left_indicator = Indicator(screen,
    (border_width/2,
    screen_height/2,
    screen_width/2-(border_width/1.5+1),
    screen_height/2-border_width/2+1))

    
    # RIGHT
    right_indicator = Indicator(screen,
    (screen_width/2+(border_width/3+2),
    screen_height/2,
    screen_width/2-(border_width/3+border_width/2+1),
    screen_height/2-border_width/2+1))


    # TOP
    game_indicator = Indicator(screen,
    (0+border_width/2,
    0+border_width/2,
    screen_width-border_width,
    screen_height/2-border_width))

    
    # Pattern generation
    # TODO: procedural pattern generation,
    # that can generate as the level progresses
    score_font = pygame.freetype.Font("font/Montserrat-Regular.ttf", 128)
    highscore_font = pygame.freetype.Font("font/Montserrat-Regular.ttf", 32)
    tutorial_font = pygame.freetype.Font("font/Montserrat-Regular.ttf", 26)
    time_font = pygame.freetype.Font("font/Montserrat-Regular.ttf", 20)

    # How many decimal places to show for time
    time_acc = 2

    game = Game()

    clock = pygame.time.Clock()
    running = True
    # Main loop
    while running:
        # Look at every event in the queue
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
                        left_indicator.color = false_color
                    elif ((game.pattern_pos) & (game.pattern_pos-1) == 0):
                        left_indicator.color = milestone_color
                        right_indicator.color = milestone_other_color
                        game_indicator.color = milestone_top_color
                    else:
                        left_indicator.color = true_color
                        game_indicator.color = true_color
                elif event.key == K_RIGHT:
                    game.process_action("right")
                    if game.lost:
                        right_indicator.color = false_color
                    elif ((game.pattern_pos) & (game.pattern_pos-1) == 0):
                        right_indicator.color = milestone_color
                        left_indicator.color = milestone_other_color
                        game_indicator.color = milestone_top_color
                    else:
                        right_indicator.color = true_color
                        game_indicator.color = true_color
                
                
                if event.key == K_r:
                    game.update_highscore(game.game_time)
                    game = Game(lost=False, )
                    for i in (game_indicator, left_indicator, right_indicator):
                            i.color = active_color

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
                        left_indicator.color = true_color
                        game_indicator.color = true_color
                    else:
                        left_indicator.color=false_color
                elif right_indicator.fill_rect.collidepoint(pygame.mouse.get_pos()):
                    game.process_action("right")
                    if not game.lost:
                        right_indicator.color = true_color
                        game_indicator.color = true_color
                    else:
                        right_indicator.color = false_color

            #TODO: add resize support
            #elif event.type == VIDEORESIZE:
            #    pass
            
            # Did the user click the window close button? If so, stop the loop.
            elif event.type == QUIT:
                game.update_highscore(game.game_time)
                running = False
                
        # Animation logic
        # lagcomp makes sure the colors don't drift off
        # when moving/resizing the window
        lagcomp = clock.get_time()
        if lagcomp > 100:
            lagcomp = 100

        # TODO: re-understand this, is it necessary?
        # left_indicator.recolor(100+lagcomp, target=idle_color)#, steps=game.steps_since_launch)
        # right_indicator.recolor(100+lagcomp, target=idle_color)#, steps=game.steps_since_launch)
        # game_indicator.recolor(100+lagcomp, target=idle_color)#, steps=game.steps_since_launch)
        # left_indicator.recolor(100+lagcomp, target=border_color, borders=True)#, smooth=game.steps_since_launch)
        # right_indicator.recolor(100+lagcomp, target=border_color, borders=True)#, smooth=game.steps_since_launch)
        # game_indicator.recolor(100+lagcomp, target=border_color, borders=True)#, smooth=game.steps_since_launch)


        if game.lost:
            left_indicator.recolor(5*lagcomp, false_color_button)
            right_indicator.recolor(5*lagcomp, false_color_button)
            game_indicator.recolor(5*lagcomp, false_color)
        else:
            for indicator in (left_indicator, right_indicator):
                # Button fade animation
                if indicator.correct:
                    indicator.recolor(0.5*lagcomp, idle_color)#, tot=1000)
                elif indicator.correct == None:
                    indicator.recolor(5*lagcomp, idle_color)
                else:
                    indicator.recolor(5*lagcomp, more_false_color)# tot=1000)
                
            game_indicator.recolor(0.5*lagcomp, target=idle_color)
        
        if game_indicator.correct != False and game.pattern_pos != 0:
            game_indicator.recolor(5*lagcomp, target=idle_color)#, tot=900)
        
        # Lower intro volume if game is started early
        if game.started and game.dynamic_rvol != 0:
            game.fade_restart_volume()
        
        game_indicator.draw()
        left_indicator.draw()
        right_indicator.draw()

        # Drawing paddle arrows (Should i make a function for this?)
        if not game.started:
            #left arrow
            pygame.draw.line(screen, arrow_color, (arrow_x_pad-25, arrow_y), (arrow_x_pad, arrow_y-25), 8)
            pygame.draw.line(screen, arrow_color, (arrow_x_pad-25, arrow_y), (arrow_x_pad, arrow_y+25), 8)
            pygame.draw.line(screen, arrow_color, (arrow_x_pad-25, arrow_y), (arrow_x_pad+35, arrow_y), 5)
            # right arrow
            pygame.draw.line(screen, arrow_color, (screen_width-(arrow_x_pad-25), arrow_y), (screen_width-(arrow_x_pad), arrow_y-25), 8)
            pygame.draw.line(screen, arrow_color, (screen_width-(arrow_x_pad-25), arrow_y), (screen_width-(arrow_x_pad), arrow_y+25), 8)
            pygame.draw.line(screen, arrow_color, (screen_width-(arrow_x_pad-25), arrow_y), (screen_width-(arrow_x_pad+35), arrow_y), 5)

        if (game.lost or not game.started) and game.get_highscore() > 0:
            highscore_font.render_to(screen, (screen_width/18, screen_height/15), f"high: {game.get_highscore()}", fgcolor=(highscore_color))

        if game.lost:
            time_str = str(f"{round(game.game_time, time_acc)}s ({round(game.pattern_pos/game.game_time, time_acc)} bits per second)")
            time_font.render_to(screen, (screen_width/2-time_font.get_rect(time_str)[2]/2, screen_height/2.42), time_str, fgcolor=(time_color))
            tutorial_font.render_to(screen, (screen_width/2-tutorial_font.get_rect("r to restart")[2]/2, screen_height/2.88), "r to restart")
        score_font.render_to(screen, (screen_width/2-score_font.get_rect(str(game.pattern_pos))[2]/2, screen_height/10), str(game.pattern_pos))

        pygame.display.update()
        clock.tick_busy_loop()

if __name__ == '__main__':
    main()