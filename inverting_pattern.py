# Algorithm for thue-morse sequence
# 1: input binary pattern (eg. True, False, False, True)
# 2: append inverse of stored value to itself (eg "1, 0, 0, 1" becomes "1, 0, 0, 1, 0, 1, 1, 0")
# 3: if iteration number is met: output stored value
# 4: else: repeat step 1 with new pattern

import pygame
import time
import numpy as np

# Returns either 0 or 1 depending on the last move number (n),
# flipped depending on what the first move was (first_move)
def evaluate_move(n, first_move):
    if first_move == "left":
        return bin(n).count("1") % 2
    else:
        return not bin(n).count("1") % 2

# Pattern generation algorithm. No longer used in main
# game (clunky), evaluate_n() used instead.
def add_inverse(pat=[False], iterations=1):
    # Placing naked booleans in lists so they
    # can have more bools added to them
    if isinstance(pat, bool):
        pat_ = [pat]
    else:
        pat_ = pat

    # Break condition
    if iterations == 0:
        return pat_
    else:
        inverted = []
        # Appending the inverse of pat_ to itself
        for i in pat_:
            inverted.append(np.invert(i))
        return add_inverse(pat_ + inverted, iterations-1)

# Plays the thue-morse sequence as audio if run as main
if __name__ == "__main__":
    pygame.mixer.init()
    # Sound files for true and false
    f = pygame.mixer.Sound("sound/l.wav")
    t = pygame.mixer.Sound("sound/r.wav")
    getready = pygame.mixer.Sound("sound/getready.wav")

    pattern = add_inverse(True, 10)
    interval = 0.23

    count = 0
    for boolean in pattern:
        if count == 0:
            for i in range(3):
                getready.play()
                time.sleep(interval*2)
        print(boolean)
        print(f"{count}\n")
        {True:t, False:f}[boolean].play()
        time.sleep(interval)
        count += 1
    # This lets the last sound finish if it is shorter than the interval
    time.sleep(interval)
