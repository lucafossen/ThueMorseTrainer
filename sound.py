import pygame
pygame.mixer.quit()
pygame.mixer.init(44100, -16, 2, 256)


class Sound():
    def __init__(self, file, channel, channel2=None, volume=1):
        #self.channel = pygame.mixer.Channel(channel)
        self.file = "sound/"+str(file)
        self.sound = pygame.mixer.Sound(self.file)
        self.sound.set_volume(volume)

        self.channel = pygame.mixer.Channel(channel)
        # If no secondary channel is specified, use only one
        if channel2 != None:
            self.channel2 = pygame.mixer.Channel(channel2)
        else:
            self.channel2 = None
        self.swapped_channel = False

    def play(self):
        if self.channel2 == None:
            self.channel.play(self.sound)
        else:
            if not self.swapped_channel:
                self.channel.play(self.sound)
                self.swapped_channel = not self.swapped_channel
            else:
                self.channel2.play(self.sound)
                self.swapped_channel = not self.swapped_channel
