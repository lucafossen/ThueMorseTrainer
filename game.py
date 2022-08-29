import inverting_pattern
from sound import Sound
# TODO: is this needed?
# from os import listdir
# from os.path import isfile, join
import json
from datetime import datetime
import time


class Game:
    global left_sound, right_sound
    global fail_left, fail_right
    global restart_volume, restart_sound

    # My sound channels
    left_sound = Sound("l.wav", 0)
    right_sound = Sound("r.wav", 1)
    fail_left = Sound("fail_left.wav", 4)
    fail_right = Sound("fail_right.wav", 4)
    
    #TODO: find way of doing this that sounds good when approaching every milestone
    # milestone_warnings = [Sound("milestone_warnings/soon.wav", 6),
    #                     Sound("milestone_warnings/sooner.wav", 6),
    #                     Sound("milestone_warnings/ok_really_close_now.wav", 6),
    #                     Sound("milestone_warnings/its_so_close_now_please_believe_me.wav", 6), ]

    restart_volume = 0.32
    restart_sound = Sound("restart.wav", 5, volume=restart_volume)

    milestone_paths = []
    for num in range(14):
        milestone_paths.append(f"powers/{2**num}.wav")
    milestone_sounds = [Sound(path, 6, volume=1) for path in milestone_paths]

    global steps_since_launch
    steps_since_launch = 0

    global highscore

    def __init__(self, lost=False):
        self.steps_since_launch = steps_since_launch        
        self.pattern_pos = 0
        self.milestone_pos = 0
        self.won = False
        self.lost = lost
        self.highscore = self.get_highscore(high_path)
        self.starting_action = None
        self.started = False

        self.dynamic_rvol = 1
        self.which_channel = True
        restart_sound.play()

        # Start and finish times for individual games
        self.start_time = None
        self.game_time = None # finish_time - 

    def get_highscore(self, read=False):
        if read:
            try:
                with open(high_path, "r") as in_file:
                    data = json.load(in_file)
                    return data["score"]
            except:
                with open(high_path, "w", encoding="utf-8") as out_file:
                    json.dump(init_highscore, out_file, ensure_ascii=False, indent=4)
                    return init_highscore["score"]
        else:
            return(self.highscore)
    
    #Variables important for writing to data.json
    global init_highscore
    init_highscore = {
                        "score": 0,
                        "time": 0,
                        "datetime": None
                        }
    global high_path
    high_path = "data.json"
    
    def update_highscore(self, time="Error loading time"):
        # if score == None:
        #     score = self.pattern_pos
        # if time == None:
        #     time = self.game_time

        #try:
        with open(high_path, "r") as in_file:
            data = json.load(in_file)
            # if score != None:
            if self.pattern_pos > data["score"]:
                in_file.close()
                with open(high_path, "w", encoding="utf-8") as out_file:
                    out_dict = {"score":self.pattern_pos, "time":time, "datetime":str(datetime.now())}
                    json.dump(out_dict, out_file, ensure_ascii=False, indent=4)
                out_file.close()

        # If opening the file for reading fails, create one   
        # except:
        #     with open(high_path, "w", encoding="utf-8") as out_file:
        #             # highscore = init_highscore["score"]
        #             json.dump(init_highscore, out_file, ensure_ascii=False, indent=4)
        #             # return init_highscore["score"]


    def start_game(self, starting_action):
        global fresh_launch
        self.starting_action = starting_action

        self.started = True
        self.start_time = time.time()
        
        #steps_since_launch = False

    def process_action(self, action):
        #correct = None
        #milestone = None
        # Checking if the game is not finished
        if not self.won and not self.lost:
            # If the game has just begun
            if self.pattern_pos == 0:
                self.start_game(action)
            
            # If the action is correct
            if {"right":1, "left":0}[action] == inverting_pattern.evaluate_move(self.pattern_pos, self.starting_action):
                self.pattern_pos += 1
                # Set volumes of regular beeps lower if milestone sound is also supposed to play
                if ((self.pattern_pos) & (self.pattern_pos-1) == 0):
                    right_sound.sound.set_volume(0.7)
                    left_sound.sound.set_volume(0.7)
                else:
                    right_sound.sound.set_volume(1)
                    left_sound.sound.set_volume(1)
                # Play appropriate sound
                if action == "right":
                    right_sound.play()
                if action == "left":
                    left_sound.play()
                self.update_highscore(self.game_time)
                
                #print(self.pattern_pos, self.highscore)
                if self.pattern_pos > self.highscore:
                    #print(f"{self.pattern_pos} is bigger than {self.highscore}, which should be equal to {self.get_highscore()}")
                    self.set_time()
                    self.update_highscore(self.game_time)

                    self.highscore = self.pattern_pos
                    
                    #print(f"{self.pattern_pos},{self.highscore},{self.get_highscore()} should all be equal now")
                 

                # If the player has reached the end of the pattern
                # if self.pattern_pos == len(self.pattern):
                #     self.won = True
                    #self.pattern = inverting_pattern.add_inverse(self.pattern)
                    #print("generated new pattern")
                # If the player has reached a milestone (power of 2)
                if ((self.pattern_pos) & (self.pattern_pos-1) == 0):# and self.pattern_pos != 0):
                    #milestone = self.milestone_pos
                    self.milestone_sounds[self.milestone_pos].play()
                    if self.milestone_pos < 13:
                        self.milestone_pos += 1
                
                self.correct = True
                
            # If the action is incorrect
            else:
                self.set_time()
                self.correct = False
                self.lost = True
                self.update_highscore(self.game_time)
                {"left":fail_left, "right":fail_right}[action].play()

        # TODO: why is this here?
        # return self.highscore  #(correct, self.milestone_pos, self.won, self.lost, milestone)
    
    def fade_restart_volume(self):
        if self.dynamic_rvol < 0.001:
            self.dynamic_rvol = 0
        else:
            self.dynamic_rvol *= 0.99
        restart_sound.sound.set_volume(restart_volume*self.dynamic_rvol)
    
    def quit(self):
        self.update_highscore(self.game_time)
    
    def set_time(self):
        self.game_time = float(time.time() - self.start_time)

    # TODO: is this needed?
    # def get_time(self):
    #     if self.start_time != None and self.finish_time != None:
    #         return 
        # else:
        #     return 1231