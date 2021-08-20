"""
This where we generate all possible combination plan
"""
from random import shuffle
# Emotion A: Angry S: Sad
# Strategy: R: Random, T: Tit-for-Tat (Copy previous??"
COMBINATION_STARTS = [["Red", "A", "T"],
                ["Red", "A", "R"],
                 ["Red", "S", "T"],
                 ["Red", "S", "R"],
                 ["Blue", "A", "T"], 
                 ["Blue", "A", "R"],
                 ["Blue", "S", "T"],
                 ["Blue", "S", "R"]]

BLOCK_COMBOS = [[('Red', 'A', 'T'), ('Blue', 'S', 'R'), ('Red', 'A', 'R'), ('Blue', 'S', 'T')],
[('Red', 'A', 'T'), ('Blue', 'S', 'T'), ('Red', 'A', 'R'), ('Blue', 'S', 'R')],
[('Red', 'A', 'R'), ('Blue', 'S', 'T'), ('Red', 'A', 'T'), ('Blue', 'S', 'R')],
[('Red', 'A', 'R'), ('Blue', 'S', 'R'), ('Red', 'A', 'T'), ('Blue', 'S', 'T')],
[('Red', 'S', 'T'), ('Blue', 'A', 'R'), ('Red', 'S', 'R'), ('Blue', 'A', 'T')],
[('Red', 'S', 'T'), ('Blue', 'A', 'T'), ('Red', 'S', 'R'), ('Blue', 'A', 'R')],
[('Red', 'S', 'R'), ('Blue', 'A', 'T'), ('Red', 'S', 'T'), ('Blue', 'A', 'R')],
[('Red', 'S', 'R'), ('Blue', 'A', 'R'), ('Red', 'S', 'T'), ('Blue', 'A', 'T')],
[('Blue', 'A', 'T'), ('Red', 'S', 'R'), ('Blue', 'A', 'R'), ('Red', 'S', 'T')],
[('Blue', 'A', 'T'), ('Red', 'S', 'T'), ('Blue', 'A', 'R'), ('Red', 'S', 'R')],
[('Blue', 'A', 'R'), ('Red', 'S', 'T'), ('Blue', 'A', 'T'), ('Red', 'S', 'R')],
[('Blue', 'A', 'R'), ('Red', 'S', 'R'), ('Blue', 'A', 'T'), ('Red', 'S', 'T')],
[('Blue', 'S', 'T'), ('Red', 'A', 'R'), ('Blue', 'S', 'R'), ('Red', 'A', 'T')],
[('Blue', 'S', 'T'), ('Red', 'A', 'T'), ('Blue', 'S', 'R'), ('Red', 'A', 'R')],
[('Blue', 'S', 'R'), ('Red', 'A', 'T'), ('Blue', 'S', 'T'), ('Red', 'A', 'R')],
[('Blue', 'S', 'R'), ('Red', 'A', 'R'), ('Blue', 'S', 'T'), ('Red', 'A', 'T')]]

# Which block Combo each of our participant will get
PPT_PLAN = [15, 11, 10, 2, 1, 9, 13, 7, 4, 12, 3, 0, 8, 14, 6, 5, 10, 14, 11, 6, 4, 1, 3, 7, 8, 15, 0, 2, 9, 12, 13, 5]

def generate_blocks():
    block_combinations = []
    for pattern in COMBINATION_STARTS:
        r1 = pattern[0]
        e1 = pattern[1]
        s1 = pattern[2]
        # robot
        if r1 == "Red":
            r2 = "Blue"
        else:
            r2 = "Red"
        #emotion
        if e1 == "A":
            e2 = "S"
        else:
            e2 = "A"
        #strategy
        if s1 == "T":
            s2 = "R"
        else:
            s2 = "T"
        block_combinations.append([(r1, e1, s1), 
                                      (r2, e2, s2), 
                                      (r1, e1, s2), 
                                      (r2, e2, s1)])
        block_combinations.append([(r1, e1, s1), 
                                      (r2, e2, s1), 
                                      (r1, e1, s2), 
                                      (r2, e2, s2)])
    print("There are %d possible block combination" % len(block_combinations))
    for block in block_combinations:
        print(block)

def generate_plan(total_ppt):
    block_options = []
    deal_block = []
    option_count = len(BLOCK_COMBOS)
    for i in range(0, option_count):
        block_options.append(i)
        
    for j in range(0, total_ppt, option_count):
        shuffle(block_options)
        deal_block = deal_block + block_options
        
    print(deal_block)
    return deal_block
    
if __name__ == "__main__":
    #generate_blocks()
    #generate_plan(32)
    pass
        
        