# Algorithm for thue-morse sequence
# 1: input binary pattern (eg. True, False, False, True)
# 2: append inverse of stored value to itself (eg "1, 0, 0, 1" becomes "1, 0, 0, 1, 0, 1, 1, 0")
# 3: if iteration number is met: output stored value
# 4: else: repeat step 1 with new pattern

import pygame
import time

# Returns either 0 or 1 depending on the last move number (n),
# flipped depending on what the first move was (first_move)
def evaluate_move(n, first_move="left"):
    if first_move == "left":
        return bin(n).count("1") % 2
    else:
        return not bin(n).count("1") % 2

# Plays the thue-morse sequence as audio if run as main
if __name__ == "__main__":
    pygame.mixer.init()
    # Sound files for true and false
    l = pygame.mixer.Sound("sound/l.wav")
    r = pygame.mixer.Sound("sound/r.wav")
    getready = pygame.mixer.Sound("sound/getready.wav")

    interval = 0.23

    count = 0
    while True:
        if count == 0:
            for i in range(3):
                getready.play()
                time.sleep(interval*2)
        print(f"{count}: {evaluate_move(count)}\n")
        {1:l, 0:r}[evaluate_move(count)].play()
        time.sleep(interval)
        count += 1
