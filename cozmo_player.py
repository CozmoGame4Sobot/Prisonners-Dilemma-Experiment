import asyncio
import copy
import cozmo
import time
from cozmo.util import degrees, distance_mm, Pose
from datetime import datetime

import sys

from asyncio.locks import Lock
from constants import ( PLAYER_ID,
                        COZMO_ID,
                        
                        P_R,
                        P_O,
                        O_R,
                        O_O,
                        X_X,
                        
                        COZMO_DEFECT,
                        COZMO_COOP,
                        COZMO_CHOICE,
                        COZMO_BASELINE,
                        
                        PRACTICE,
                        TIT_FOR_TAT,
                        RANDOM,
                        BASELINE,
                        
                        NEUTRAL,
                        SAD,
                        ANGRY,
                        
                        RED_CODE,
                        BLUE_CODE,
                        
                        RESULT_STATEMENT)

from game_engine import SpeedTapEngine, GoalStatements
from human_player import Human_Listener
from game_cubes import BlinkyCube
from random import randint, shuffle
from screen import Screen
from idlelib.PyShell import fix_x11_paste
from turtledemo import planet_and_moon

cozmo.world.World.light_cube_factory = BlinkyCube

class CozmoPlayerActions(object):
    """
    A singleton class defining how cozmo will act
    """
    
    __instance = None
    
    def __new__(cls):
      if not CozmoPlayerActions.__instance:
          CozmoPlayerActions.__instance = object.__new__(cls)
          CozmoPlayerActions.__instance.emotion = NEUTRAL
          CozmoPlayerActions.__instance.strategy = PRACTICE
          CozmoPlayerActions.__instance.tablet_code = None
          CozmoPlayerActions.__instance.rounds_to_play = 10
          CozmoPlayerActions.__instance.strategy = 'P'
          CozmoPlayerActions.__instance.singleScreen = False
      return  CozmoPlayerActions.__instance
    
        
    def set_strategy(self, strategy, colour, emotion):
        """
        setup initial strategy and emotion
        """
        self.strategy = strategy
        self.practice = False
        if self.strategy == PRACTICE:
            self.practice = True
            self.rounds_to_play = 11
            self.emotion = NEUTRAL
        elif self.strategy == BASELINE:
            self.rounds_to_play = 11
            self.emotion = NEUTRAL 
        elif self.strategy == TIT_FOR_TAT: #we only have emotions for Tit-for-tat
            self.rounds_to_play = 16
            if emotion == 'S':
                self.emotion = SAD
            elif emotion == 'A':
                self.emotion = ANGRY
        else:
            self.rounds_to_play = 10

        if colour == "R":
            self.tablet_code = RED_CODE
        else:
            self.tablet_code = BLUE_CODE
        
        
        
           
    def set_singleScreen(self):
        """
        During experiment this should not be called from commandline
        """
        self.singleScreen = True
    
    def setup_ScorePlan(self, score_plan):
        """
        Setup score plan and practice goal statements
        """
        self.score_plan = score_plan
        self.goals_statment_list = GoalStatements(score_plan).statements
        
    def set_game_lose_reaction(self, is_sad):
        self.sad_not_angry = is_sad
                
    
    def cozmo_tap_decision(self, game_robot, speed_tap_game, goal=None):
        """
        This module decides whether cozmo should tap or not
        @param game_robot: The cozmo robot handle
        @param speed_tap_game: The game engine that needs to register the tap
        @param goal: If this is a practice round then cozmo taps if the goal requires it to tap 
        """
        #print("Goal %d  to grab:%s" %(goal, [P_R, O_R]))
        #if self.strategy == PRACTICE:
        #    tap_decision = goal in [P_R, O_R ] #randint(0, 10) in [0, 4, 8, 5, 10]           
        #elif self.strategy == RANDOM:
        #    tap_decision = goal in [P_R, O_R]
        #elif self.strategy == TIT_FOR_TAT:
        #    tap_decision = goal in [1, 1, 1, 0, 0, 1]   
        #else:
        #    tap_decision = goal in [COZMO_DEFECT]
            
        if not self.practice:
            tap_decision = goal in [P_R, O_R ]
            
        else:
            tap_decision = goal in [P_R, O_R]
        time.sleep(1.5)
        game_robot.move_lift(-3)
        time.sleep(.1)
        game_robot.move_lift(4)
        time.sleep(.1)
        game_robot.play_anim('anim_speedtap_tap_02')#.wait_for_completed()
        
        if tap_decision:
            cozmo.logger.info("PD : Cozmo tapped grab")
            cozmo_tapped = speed_tap_game.register_tap(tap_type=COZMO_DEFECT)
        else:
            cozmo.logger.info("PD : Cozmo tapped share")
            cozmo_tapped = speed_tap_game.register_tap(tap_type=COZMO_COOP)
        
        time.sleep(0.5)
        return True
    
    def select_wait(self):
        wait_anims = ['anim_speedtap_wait_short',
          'anim_speedtap_wait_medium',
          'anim_speedtap_wait_medium_02',
          'anim_speedtap_wait_medium_03',
          'anim_speedtap_wait_long'
          ]
        selected = randint(0,4)
        return wait_anims[selected]
    
    def select_win_game(self):
        if self.emotion == NEUTRAL:
            reaction_anim = "anim_speedtap_foundblock_01"
        else:
            #reaction_anim =  "anim_keepaway_wingame_02" # Te-Yi's first choice
            reaction_anim = "anim_keepaway_wingame_01"
            cozmo.logger.info("PD : Cozmo win game reacion")
        return reaction_anim
        
    def select_lose_game(self):
        
        if self.emotion == SAD:
            reaction_anim = "anim_memorymatch_failgame_cozmo_03" 
            cozmo.logger.info("PD : Cozmo sad lose game reacion")            
        elif self.emotion == ANGRY:
            #lose_game_anim = "anim_guarddog_getout_busted_01" #Te-Yi's first choice
            reaction_anim = "anim_guarddog_getout_busted_01" #"anim_memorymatch_failgame_cozmo_02"
            cozmo.logger.info("PD : Cozmo angry lose game reacion") 
        else:
            reaction_anim = "anim_speedtap_foundblock_01"

        return reaction_anim 
    
    def select_lose_hand(self):
        if self.emotion == SAD:
            reaction_anim = "anim_memorymatch_failgame_cozmo_03" 
            cozmo.logger.info("PD : Cozmo sad lose game reacion")            
        elif self.emotion == ANGRY:
            reaction_anim = "anim_guarddog_getout_busted_01" #"anim_memorymatch_failgame_cozmo_02"
            cozmo.logger.info("PD : Cozmo angry lose game reacion") 
        else:
            reaction_anim = "anim_speedtap_foundblock_01"

        return reaction_anim 
        
    
    def act_out(self, game_robot, act_type):
        selected_anim = None
        if act_type == "lose_hand":
            # There needs to be two moods for sad and angry
            selected_anim = self.select_lose_hand()
        elif act_type == "win_hand":
            #selected_anim = "anim_speedtap_winhand_0%s" % randint(1, 3)
            selected_anim = "anim_keepaway_wingame_02"	#happy animation
        elif act_type == "neutral":
            selected_anim = "anim_speedtap_foundblock_01"
        elif act_type == "stand_back":
            game_robot.drive_wheels(-100, -100, duration=1.5)
            time.sleep(1.5)
            game_robot.move_lift(-3)
            time.sleep(0.2)
        elif act_type == "check_score":
            game_robot.drive_wheels(100, -100, duration=1)
            game_robot.set_head_angle(degrees(10)).wait_for_completed()
            if self.practice:
                time.sleep(2)
            else:
                time.sleep(0.5)
            game_robot.drive_wheels(-100, 100, duration=1)
            game_robot.set_head_angle(degrees(0)).wait_for_completed()
            time.sleep(0.5)
        elif act_type == "win_game":
            selected_anim = self.select_win_game()
        elif act_type == "lose_game":
            selected_anim = self.select_lose_game()
        else:
            selected_anim = self.select_wait()
           
        
        if selected_anim:
            game_robot.play_anim(selected_anim).wait_for_completed()
            
def log_deal_plan(plan):
    cozmo.logger.info("PD : %s" % list(map(lambda x: 'Share' if x==1 else 'Grab' if x==0 else 'Missing', plan)))


    
def cozmo_tap_game(robot: cozmo.robot.Robot):
    # Initialize all the game engines screens and listners
    speed_tap_game = SpeedTapEngine(robot)
    robot_game_action = CozmoPlayerActions()
    display_screen = Screen()
    display_screen.setup(robot_game_action.score_plan,
                         singleScreen=robot_game_action.singleScreen)
    game_screen = display_screen.gameScreen
    #display_screen.start()
    display_screen.root.mainloop(1)
    game_screen.show_play_screen(0, 0)
    
    # Setup the game so cozmo and player knows their cube
    
    time.sleep(0.25)        # sleep to give the cozmo cube to stop flashing
    
    robot_cube, player_coop_cube, player_defect_cube = speed_tap_game.cozmo_setup_game(robot_game_action.score_plan)
  
    if robot_cube in [player_coop_cube, player_defect_cube]:
        print("Participant cannot play on the same cube as cozmo")
        game_screen.master.destroy() 
        exit(0)
        
    # Setup listeners on player's cubes
    monitor_player_tap = Human_Listener(robot, player_coop_cube, player_defect_cube, speed_tap_game)
    
    # initialise variables
    
    
    correctChoice = -1                  # Correct choice is for practice round
    track_correct_practice = 0
    game_complete = False
    winner = 0
    score_to = 5 
    pass_criteria = 3                   # Only applies for practice rounds
    
    goal_statement = ""
    preset_goals = [P_R,
                    P_O,
                    O_R,
                    O_O]    
    
    # This is needed for RANDOM choices
    #cozmo_fixture =  COZMO_CHOICE[randint(0, 2)][:robot_game_action.rounds_to_play]
    
    # Now all decided so lets suffle it up
    #shuffle(cozmo_fixture)
    
    # Start the game and player tap listeners
    monitor_player_tap.game_on = True
    monitor_player_tap.start()
    deal_count = 1
    
    
    if robot_game_action.practice:
        cozmo.logger.info("PD : Playing practice round")
        cozmo_fixture =  COZMO_CHOICE[randint(0, 2)][:robot_game_action.rounds_to_play]
    elif robot_game_action.strategy == BASELINE:
        cozmo_fixture =  COZMO_BASELINE
        cozmo.logger.info("PD : Playing BASELINE round")
        cozmo.logger.info("PD : Strategy = BASELINE")
    elif robot_game_action.strategy == TIT_FOR_TAT:
        cozmo_fixture =  COZMO_BASELINE
        cozmo.logger.info("PD : Playing experiment round")
        cozmo.logger.info("PD : Strategy = TIT_FOR_TAT")
    else:
        cozmo.logger.info("PD : Playing experiment round")
        cozmo.logger.info("PD : Strategy = RANDOM")
        cozmo.logger.info("PD : Cozmo initial plan fixture")
        log_deal_plan(cozmo_fixture)
        
    cozmo.logger.info("PD : Score set: %s" % robot_game_action.score_plan)
        
    try:
        while deal_count < robot_game_action.rounds_to_play :
            #print("cozmo_fixture %s" % cozmo_fixture)
            cozmo.logger.info("PD : Deal started")
            if robot_game_action.practice:
                if track_correct_practice%4 == 0:
                    shuffle(preset_goals)
                    #cozmo.logger.info("PD : Preset Goals :%s" % preset_goals)
                correctChoice = preset_goals[(track_correct_practice-1)%4]
                cozmo.logger.info("PD : Practice Goal : %s" % robot_game_action.goals_statment_list[correctChoice])
            goal_statement = robot_game_action.goals_statment_list[correctChoice]
            
            
            
            game_screen.show_play_screen(speed_tap_game.player_score,
                                         speed_tap_game.robot_score)
            game_screen.show_goal_statement(goal_statement)
            
            # Cozmo get in ready position
            robot_game_action.act_out(robot, "wait")
            
           
            # Deal the hand
            speed_tap_game.deal_hand()
            cozmo.logger.info("PD : Hand delt : %s" % deal_count)
            #print("Pre: %s" % datetime.now())
            monitor_player_tap.listen = True
            if robot_game_action.strategy==PRACTICE:
                cozmo_goal = correctChoice
            elif robot_game_action.strategy == BASELINE:# and speed_tap_game.robot_next_move:
                # If player defected last time cozmo will defect
                #print("%d  defect=%d" % (speed_tap_game.robot_next_move, COZMO_DEFECT))
                #cozmo_goal = speed_tap_game.robot_next_move
                if deal_count<=5:
                    cozmo_goal = cozmo_fixture[deal_count - 1]
                else:
                    cozmo_goal = speed_tap_game.player_move
                    cozmo_fixture.append(cozmo_goal)
            elif robot_game_action.strategy == TIT_FOR_TAT:# and speed_tap_game.robot_next_move:
                # If player defected last time cozmo will defect
                #print("%d  defect=%d" % (speed_tap_game.robot_next_move, COZMO_DEFECT))
                #cozmo_goal = speed_tap_game.robot_next_move
                if deal_count<=5:
                    cozmo_goal = cozmo_fixture[deal_count - 1]
                else:
                    cozmo_goal = speed_tap_game.player_move
                    cozmo_fixture.append(cozmo_goal)
            else:
                cozmo_goal = cozmo_fixture[deal_count - 1]
            # Get Cozmo to decide whether it is going to tap
            tapped = robot_game_action.cozmo_tap_decision(robot, speed_tap_game, cozmo_goal)
            
            
            
            # If player has tapped it would be registered by now      
            monitor_player_tap.listen = False
            #print("Player move : %s" % speed_tap_game.player_move)
            speed_tap_game.deactivate_current_deal() 
            cozmo.logger.info("PD : Hand deactivated : %s" % deal_count)
            speed_tap_game.score_last_deal(refresh = False)  # For not having a running total set refresh to True   
            result = speed_tap_game.result_track[-1]
            cozmo.logger.info("PD : Result : %s" % RESULT_STATEMENT[result])
            game_screen.show_play_screen(speed_tap_game.player_score,  speed_tap_game.robot_score, result)
            
            cozmo.logger.info("PD : After hand %s player score : %s" % (deal_count, speed_tap_game.player_score))
            cozmo.logger.info("PD : After hand %s cozmo score  : %s" % (deal_count, speed_tap_game.robot_score))
            game_screen.show_selection(result, correctChoice) 
            if robot_game_action.practice:
                game_screen.show_goal_statement(goal_statement)
            else:
                game_screen.show_goal_statement("")
             
            if robot_game_action.practice:
                # We need to track practice round so that
                # we know the player has correctly understood the game
                if result==correctChoice:
                    track_correct_practice += 1
                    cozmo.logger.info("PD : CORRECT for %s times" % track_correct_practice)
                else:
                    cozmo.logger.info("PD : INCORRECT choice. Chances left: %s " % (robot_game_action.rounds_to_play - deal_count -1))                    
                    # One wrong implies all wrong
                    track_correct_practice = 0                                   
                # We are not tracking scores across games for 
                # practice so reset deal                
                speed_tap_game.reset_deals()
                                  
                     
            deal_count += 1                
            
            #time.sleep(2)
            # Cozmo check out score
            robot_game_action.act_out(robot, "stand_back")
            robot_game_action.act_out(robot, "check_score")
            
            # This is where the robot needs to act angry or sad or neutral depending on relative scores
            # speed_tap_game.player_score, speed_tap_game.robot_score,
            #if robot_game_action.strategy == TIT_FOR_TAT and speed_tap_game.robot_score < speed_tap_game.player_score:
            #    robot_game_action.act_out(robot, "lose_hand")
            
            # This is where the robot needs to act angry or sad or neutral depending on result
            # condition to win_hand still to be checked with Te-Yi/Bish
            if robot_game_action.strategy == TIT_FOR_TAT and result == O_O :   # player and cozmo share
                robot_game_action.act_out(robot, "win_hand")
                
            if robot_game_action.strategy == TIT_FOR_TAT and  result == P_O :   # player grab cozmo share
                robot_game_action.act_out(robot, "lose_hand")
            
            
            # Stop light cubes
            robot_cube.stop_light_chaser()
            player_coop_cube.stop_light_chaser()
            player_defect_cube.stop_light_chaser()
            robot_cube.set_lights_off()
            player_coop_cube.set_lights_off()
            player_defect_cube.set_lights_off()
            
            # clean up
            if robot_game_action.practice and track_correct_practice >= pass_criteria:
                cozmo.logger.info("PD : Practice Passed") 
                print("PRACTICE PASSED")
                game_screen.show_goal_statement("PRACTICE PASSED")
                time.sleep(2)
                break
            elif not robot_game_action.practice and result == X_X : #X_X is when player missed to tap the cube
                if robot_game_action.rounds_to_play >= 25:
                    cozmo.logger.info("PD : Over 10-15 rounds of missing data. We will stop.")
                    break;
                else:
                    cozmo.logger.info("PD : Rounds incremented to compensate for missing data")
                    robot_game_action.rounds_to_play += 1
                    # We missed a even paced tap/no tap decision by cozmo so append it 
                    # at the end to maintain balance
                    #cozmo_fixture.append(cozmo_goal)
                    #cozmo_fixture[deal_count - 1] = cozmo_goal
                    cozmo_fixture.insert(deal_count-1, cozmo_goal)
                    cozmo_fixture[deal_count - 2] = -1 
                    cozmo.logger.info("PD : Updated cozmo plan")
                    log_deal_plan(cozmo_fixture)
                    #if deal_count>5:
                       
            
            # Reposition Cozmo close to its cube
            if deal_count <= robot_game_action.rounds_to_play:
                robot.move_lift(3)
                robot.go_to_object(robot_cube, distance_mm(35.0)).wait_for_completed()
                '''
                if robot_game_action.practice or deal_count%5 == 0:
                    #robot.drive_wheels(-50, -50, duration=0.5)
                    robot.go_to_object(robot_cube, distance_mm(35.0)).wait_for_completed()
                else:
                    robot.drive_wheels(100, 100, duration=1.5)
                    time.sleep(1.5)
                    #robot.go_to_object(robot_cube, distance_mm(35.0)).wait_for_completed()
                 '''  
                
                cozmo.logger.info("PD : Ready for next deal")            
            
            
            
        # clear up games to show result    
        robot_cube.stop_light_chaser()
        player_coop_cube.stop_light_chaser()
        player_defect_cube.stop_light_chaser()
        robot_cube.set_lights_off()
        player_coop_cube.set_lights_off()
        player_defect_cube.set_lights_off()
        cozmo.logger.info("PD : Done playing")   
        robot_game_action.act_out(robot, "stand_back")
       
        time.sleep(2)
        
        robot.go_to_object(robot_cube, distance_mm(60.0)).wait_for_completed()
        
        #display_screen.root.mainloop()
        
        if robot_game_action.practice and deal_count >= robot_game_action.rounds_to_play:
            cozmo.logger.info("PD : Practice Failed") 
            game_screen.show_goal_statement("")
            print("PRACTICE FAILED")
            game_screen.show_goal_statement("PRACTICE FAILED")
            time.sleep(2)
        elif not robot_game_action.practice and deal_count >= robot_game_action.rounds_to_play:
            cozmo.logger.info("PD : Game Finished") 
            print("Game Finished")
            game_screen.show_goal_statement("Game Finished")
            time.sleep(2)
        
    finally:
         monitor_player_tap.game_on = False
         robot_cube.stop_light_chaser()
         player_coop_cube.stop_light_chaser()
         player_defect_cube.stop_light_chaser()
         robot_cube.set_lights_off()
         player_coop_cube.set_lights_off()
         player_defect_cube.set_lights_off()
         monitor_player_tap.join()
         
         del speed_tap_game
         del player_coop_cube
         del player_defect_cube
         del robot_cube

    
    game_screen.master.destroy() 
