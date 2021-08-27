import argparse
import asyncio
import copy
import cozmo
from datetime import datetime
import getopt
import logging
import os
import sys 
import time
from cozmo_player import CozmoPlayerActions, cozmo_tap_game
from constants import SCORE_SETS, PRACTICE


def add_file_logger(log_path, emotion, strategy):
    ''' setup file logger'''
    #if practice:
    #    filename="Pract_%s.log" % datetime.now().strftime("%H%M%S_%d%m%Y")
    #else:
    #    filename="Exp_%s.log" % datetime.now().strftime("%H%M%S_%d%m%Y")
   
    filename= strategy + "_" + emotion + "_" + "%s.log" % datetime.now().strftime("%H%M%S_%d%m%Y")
    filePath = os.path.join(log_path, filename)
    
    # create error file handler and set level to info
    handler = logging.FileHandler(os.path.join(log_path, filename),"w", encoding=None, delay="true")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    
    # add file handler to cozmo
    cozmo.logger.addHandler(handler)
    
def handle_selection(cozmo_action):    
    help_string = 'tap_game.py -h (--help) [-s (--sad), -a (--angry)] [-l (--logPath) -i(--ignoreLogging)]   < Note the log options must be the last option>'
    log_path = None
    configParam = {"strategy" : None,
                   "participantID":None,
                   "score_plan": None}
    log_path = None
    parser = argparse.ArgumentParser()
    parser.add_argument("--participantID", type=int, required=True,
                         help="Participant ID is required to record logs correctly")
    parser.add_argument("--ignoreLog", type=bool, nargs='?', const=True, default=False,
                        help="Provide this argument to indicate logs are to be ignores")
    parser.add_argument("--strategy", choices=['P', 'T', 'R', 'B'],    
                        help="Choose to play practice(P), tit-for-tat(T), random(R) or Baseline(B)")
    parser.add_argument("--colour", choices=['B', 'R'],    
                        help="Choose to play Blue(B) or Red(R)")
    parser.add_argument("--emotion", choices=['A', 'S'], default="",   
                        help="Choose to play Angry(A) or Sad(S)")
    parser.add_argument("--singleScreen", type=bool, nargs='?', const=True, default=False,    
                        help="For checking game on single screen")
   
    parser.add_argument("--log", type=str, default="./logs", 
                        help="Entire log directory path. The filename is defined by the code")
    args = parser.parse_args()
    
    # Check log option entered and directory
    if not args.ignoreLog:
        if args.log=="<root>/PrisonnersDilemma/logs":
            log_path = os.path.join(os.path.abspath(os.sep), 'PrisonnersDilemma')
            log_path = os.path.join(log_path, "logs")
        else:
            log_path = args.log
        
        if not log_path  or not os.path.isdir(log_path):
            print("ERROR!!! Please create the log directory '%s' on your system." % log_path)
            print("If you want to log at an alternative location use --log=<log_path> to enter it")
            exit(0)
        else:
            if args.participantID:
                log_path = os.path.join(log_path, 'P%s' % args.participantID)
                if not os.path.isdir(log_path):
                    os.mkdir(log_path)
            configParam["logPath"] = log_path
    
    # No need to change this as per experiment design 
    cozmo_action.setup_ScorePlan(SCORE_SETS["score_set2"])
        
    configParam["participantID"] = args.participantID
    
    if args.participantID <= 0:
        print("ERROR! Cannot proceed without participant ID.") 
        exit(0)
    
    
    configParam["strategy"] = args.strategy
    configParam["colour"] = args.colour
    configParam["emotion"] = args.emotion
    cozmo_action.set_strategy(args.strategy, 
                              args.colour,
                              args.emotion)
    
        
    if args.singleScreen:
        cozmo_action.set_singleScreen()
       
        
    if configParam and log_path:
        add_file_logger(log_path, args.emotion, args.strategy) 
    return configParam       
    
         
if __name__ == "__main__":
  
   cozmo_action = CozmoPlayerActions()
   if handle_selection(cozmo_action):
       loop = asyncio.get_event_loop()
       tablet_connector = cozmo.AndroidConnector(adb_cmd=None, serial=cozmo_action.tablet_code) 
       cozmo.run_program(cozmo_tap_game, connector=tablet_connector)
       
   del cozmo_action
   exit(0)
    
   
    
