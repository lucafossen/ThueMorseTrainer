import pygame
from pygame.locals import Color

dark_color = Color(25, 25, 0)

# TODO: clean up this mess
class Indicator:
    def __init__(self, screen, rect, color=dark_color, border_color=dark_color, border_width=25):#default_color, true_color, active_color, false_color, border_color, border_width):
        self.screen = screen
        self.rect = rect
        self.default_color = color
        self.color = color
        # self.true_color = true_color
        # self.active_color = active_color
        # self.false_color = false_color
        self.default_border_color = border_color
        self.border_color = border_color
        self.border_width = border_width

        # self.color = default_color
        self.border_rect = pygame.Rect(
                                    self.rect[0]-self.border_width/2,
                                    self.rect[1]-self.border_width/2,
                                    self.rect[2]+self.border_width,
                                    self.rect[3]+self.border_width
                                    )

        self.fill_rect = pygame.Rect(
                                    self.rect[0],
                                    self.rect[1],
                                    self.rect[2],
                                    self.rect[3]
                                    )
        self.correct = None
    
    def draw(self):
        # print([self.border_color[i] for i in range(3)])
        #print([int(i) for i in self.color])
        pygame.draw.rect(self.screen, [int(i) for i in self.border_color], self.border_rect)
        pygame.draw.rect(self.screen, [int(i) for i in self.color], self.fill_rect)

    # def check_action(self, action, solution):
    #     if {"right":True, "left":False}[action] == solution:
    #         self.correct = True
    #         self.color = self.true_color
    #         return True
    #     else:
    #         self.correct = False
    #         self.color = self.false_color
    #         return False

    def recolor(self, speed_in, target=None, borders=False):#, tot=1000, steps=None):
        speed = speed_in / 1000
        # if target == None:
        #     target = self.default_color
        # if steps == None:
        #     steps = tot
        # #print("smooth!")
        # r0 = self.color[0]
        # g0 = self.color[1]
        # b0 = self.color[2]
        # rf = target[0]
        # gf = target[1]
        # bf = target[2]
        # #total_steps = 5000
        # dr = (rf-r0)/tot
        # dg = (gf-g0)/tot
        # db = (bf-b0)/tot
        # r = int(r0+dr*steps)
        # g = int(g0+dg*steps)
        # b = int(b0+db*steps)
        # #print(r, g, b)
        # smooth_color = Color(r, g, b)
        # if not borders:
        #     self.color = smooth_color
        # else:
        #     self.border_color = smooth_color
        
        # else:
        
        #for i in range(3):
        if not borders:
            #print("########")
            #print(int(round(speed*(target[0]-self.color[0]))))
            #print(f"{speed:.3f}")
            
            self.color = list(self.color)#(255, 0, 0)
            # 
            #self.color = [target[i]-self.default_color[i] for i in range(3)]
            
            #print(self.border_color, self.color)
            #self.color = (target[i]-self.color[i] for i in range(3))
            self.color[0] += (target[0]-self.color[0])*speed
            self.color[1] += (target[1]-self.color[1])*speed
            self.color[2] += (target[2]-self.color[2])*speed
        else:
            # self.border_color = [target[i]-self.default_border_color[i] for i in range(3)]
            
            self.border_color = list(self.border_color)
            self.border_color[0] += (target[0]-self.border_color[0])*speed
            self.border_color[1] += (target[1]-self.border_color[1])*speed
            self.border_color[2] += (target[2]-self.border_color[2])*speed
  
