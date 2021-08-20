import time


#from random import randint
from tkinter import Tk, Canvas, Frame, BOTH, PhotoImage

#from datetime import date

from constants import (
                        P_R,
                        P_O,
                        O_R,
                        O_O,
                        X_X
                        )

class GameWindow(Frame, object):
    
    __currentGame = None
    
    @staticmethod 
    def getInstance(frameTitle="Game", screenDim=[1360, 768], score_plan=None, logger=None):
       """ Static access method. """
       if GameWindow.__currentGame == None:
          #print "Create New"
          GameWindow(frameTitle, screenDim, score_plan, logger)
       return GameWindow.__currentGame
          
         
    def __init__(self, frameTitle="Game", screenDim=[1360, 768], score_plan=None,  logger=None):
        if GameWindow.__currentGame != None:
            raise Exception("This class is a singleton!")
        else:
            GameWindow.__currentGame = self
            super(GameWindow, self).__init__()
            self.logger = logger
            self.option_position = []
            self.score_plan = score_plan
            self.master.title(frameTitle)
            self.windowLength = screenDim[0]
            self.windowHeight = screenDim[1]
            self.canvas = Canvas(self, 
                                 width=self.windowLength,
                                 height=self.windowHeight,
                                 background="black")
            self.canvas.grid(row=4, column=4)
            
            
            self.pack(fill=BOTH, expand=1)
            self.canvas.update() 
            self.acceptChoice = False 
            #self.coinsImg = PhotoImage(file = "./coins.gif")
            self.setup_OptionPos()
           
            
    def setup_OptionPos(self):
        displaySize = (self.windowLength - 60)/5
        displayHeight = (self.windowHeight - 60) /5
        draw_x = displaySize
        draw_y = displayHeight
        
        offset = 80
        drawx = displaySize+(1.5*offset)
        drawy = displayHeight+offset
        # Player tap Robot Tap
        self.option_position.append((drawx, drawy, 
                                    drawx+displaySize+ (offset/2), 
                                    drawy+displayHeight))
        
        # Player tap Robot No Tap
        drawx += drawx - (0.5*offset)
        self.option_position.append((drawx, drawy, 
                                     drawx+displaySize+ (offset/2), 
                                    drawy+displayHeight))
         # Player No tap Robot Tap
        drawx = displaySize+(1.5*offset)
        drawy += drawy
        self.option_position.append((drawx, drawy, 
                                     drawx+displaySize+ (offset/2), 
                                     drawy+displayHeight))
        
        # Player No tap Robot No Tap
        drawx += drawx - (0.5*offset)
        self.option_position.append((drawx, drawy, 
                                     drawx+displaySize+ (offset/2), 
                                     drawy+displayHeight))
        
        
        
        
    def draw_score_board(self, player, robot, last_result):
        displaySize = (self.windowLength - 60)/5
        displayHeight = (self.windowHeight - 60) /5
        light_blue = '#2eaef3'
        my_red = '#ed2727'
        my_green = '#599436'
        player_choice = "X"
        robot_choice = "X"
        if last_result == P_R:
            player_choice = "Keep"
            robot_choice = "Keep"
        elif last_result == P_O:
            player_choice = "Keep"
            robot_choice = "Share"
        elif last_result == O_R:
            player_choice = "Share"
            robot_choice = "Keep"
        elif last_result == O_O:
            player_choice = "Share"
            robot_choice = "Share"
        
        # Draw score board-------------------------------------------
        self.canvas.create_text(self.windowLength - ((displaySize+10)/2),
                                displayHeight,
                                font=("Arial", 22),
                                text="Score",
                                fill=light_blue)
        self.canvas.create_rectangle(self.windowLength - displaySize - 20,
                                     displayHeight - 20, 
                                     self.windowLength - 10,
                                     4*displayHeight + 40,
                                     outline="grey")
        # Draw Player score-----------------------------------------           
        self.canvas.create_text(self.windowLength - ((displaySize+15)/2),
                                displayHeight+60,
                                font=("Arial", 22),
                                text="You Chose",
                                fill="white")  
        
        #self.canvas.create_image(self.windowLength - (displaySize-10)/3, 
        #                         displayHeight+60, 
        #                         image=self.coinsImg)
        
        if last_result!=X_X:
            self.canvas.create_text(self.windowLength - ((displaySize+10)/2),
                                2*displayHeight ,
                                font=("Arial", 18),
                                text="%s(%d)" % (player_choice, player),
                                fill="grey")  
        # Draw Cozmo score----------------------------------------- 
        self.canvas.create_text(self.windowLength - ((displaySize+30)/2),
                                3*displayHeight,
                                font=("Arial", 22),
                                text="Cozmo Chose ",
                                fill="white")  
        #self.canvas.create_image(self.windowLength - (displaySize-60)/3, 
        #                         3*displayHeight, 
        #                         image=self.coinsImg)
        if last_result!=X_X:
            self.canvas.create_text(self.windowLength - ((displaySize+10)/2),
                                3.5*displayHeight ,
                                font=("Arial", 18),
                                text="%s(%d)" % (robot_choice, robot),
                                fill="grey")  
            
        
            

        
    def show_play_screen(self, player_score, robot_score, last_result=X_X):
        self.canvas.delete("all")
        self.currentChoice = -1
        light_blue = '#2eaef3'
        my_green = '#599436'
        my_yellow = '#aaaa00' 
        self.draw_score_board(player_score, robot_score, last_result)
        displaySize = (self.windowLength - 60)/5
        displayHeight = (self.windowHeight - 60) /5
        draw_x = displaySize
        draw_y = displayHeight
        #-------------------------------------------------------
        #Outer text and rectangle
        self.canvas.create_text(self.windowLength/2,
                                20,
                                font=("Arial", 30),
                                text="Cozmo",
                                fill="white") 
        self.canvas.create_text(40,
                                self.windowHeight/2,
                                font=("Arial", 30),
                                text="You",
                                fill="white")
        self.canvas.create_rectangle(displaySize-40, displayHeight-40,
                                     self.windowLength - displaySize-40, 
                                     self.windowHeight - displayHeight,
                                     outline = "grey",
                                     fill = None)
        #-------------------------------------------------------
        #Tap No tap
        self.canvas.create_text(2*displaySize,
                                displayHeight,
                                font=("Arial", 20),
                                text=" Tap Blue\n (To Keep)",
                                fill=light_blue) 
        self.canvas.create_text(3*displaySize + 60,
                                displayHeight,
                                font=("Arial", 20),
                                text=" Tap Yellow\n (To Share)",
                                fill=my_yellow) 
        self.canvas.create_text(displaySize + 20,
                                2*displayHeight,
                                font=("Arial", 20),
                                text=" Tap Blue\n (To Keep)",
                                fill=light_blue) 
        self.canvas.create_text(displaySize + 26,
                                4*displayHeight - 60,
                                font=("Arial", 20),
                                text=" Tap Yellow\n (To Share)",
                                fill=my_yellow) 
        
        #-------------------------------------------------------
        #Scoring boxes 
        for i in range(0, 4):
            self.canvas.create_rectangle(self.option_position[i][0],
                                         self.option_position[i][1],
                                         self.option_position[i][2],
                                         self.option_position[i][3], 
                                         fill = my_green,
                                         outline="grey")
            
        #-------------------------------------------------------
        #Score explain
        offset = 80
        self.canvas.create_text(2*displaySize,
                                self.option_position[0][1] + offset,
                                font=("Arial", 20),
                                text=" You get %s \n Cozmo gets %s" % (self.score_plan[0][0],
                                                                        self.score_plan[0][1]),
                                fill="black") 
        self.canvas.create_text(3*displaySize + 60,
                                self.option_position[1][1]  + offset,
                                font=("Arial", 20),
                                text=" You get %s \n Cozmo gets %s" % (self.score_plan[1][0],
                                                                        self.score_plan[1][1]),
                                fill="black") 
        self.canvas.create_text(2*displaySize,
                                self.option_position[2][1]  + offset,
                                font=("Arial", 20),
                                text=" You get %s \n Cozmo gets %s" % (self.score_plan[2][0],
                                                                        self.score_plan[2][1]),
                                fill="black")
        self.canvas.create_text(3*displaySize  + 60,
                                self.option_position[3][1]  + offset,
                                font=("Arial", 20),
                                text=" You get %s \n Cozmo gets %s" % (self.score_plan[3][0],
                                                                        self.score_plan[3][1]),
                                fill="black")

        self.canvas.update()
        
        
    def show_selection(self, player_selection, correct_selection = -1):
        my_red = '#ed2727'
        my_green = '#599436' 
        my_yellow = '#ffff00' 
        offset = 10
        if player_selection== X_X:
            #Player tap was not registered
            self.show_notap_statement()
        elif correct_selection < 0 or correct_selection == player_selection:
            self.canvas.create_rectangle(self.option_position[player_selection][0] - offset,
                                         self.option_position[player_selection][1] - offset,
                                         self.option_position[player_selection][2] + offset,
                                         self.option_position[player_selection][3] + offset, 
                                         outline=my_yellow,
                                         width = 5)
        else:
            self.canvas.create_rectangle(self.option_position[player_selection][0] - offset,
                                         self.option_position[player_selection][1] - offset,
                                         self.option_position[player_selection][2] + offset,
                                         self.option_position[player_selection][3] + offset, 
                                         outline=my_red,
                                         width = 5)
            self.canvas.create_rectangle(self.option_position[correct_selection][0] - offset,
                                         self.option_position[correct_selection][1] - offset,
                                         self.option_position[correct_selection][2] + offset,
                                         self.option_position[correct_selection][3] + offset, 
                                         outline=my_yellow,
                                         width = 5)
        self.canvas.update()
        
    def show_notap_statement(self):
       
        displayHeight = (self.windowHeight + 30) /5
        draw_x = self.windowLength/2
        draw_y = self.windowHeight-(displayHeight)
        self.canvas.create_text(draw_x,
                                draw_y,
                                font=("Arial", 22),
                                text="Did not hear your selection. Please remember to tap!!!!",
                                fill="red")
        
    def show_goal_statement(self, statement):
        if statement:
            displayHeight = (self.windowHeight - 60) /5
            draw_x = self.windowLength/2
            draw_y = self.windowHeight-(displayHeight/2)
            self.canvas.create_text(draw_x,
                                    draw_y,
                                    font=("Arial", 22),
                                    text="%s" % statement,
                                    fill="white")
        self.canvas.update()

class Screen():
    def __init__(self):
        
        self.root = None
        self.gameScreen = None
        
    def setup(self, score_plan, singleScreen=False): 
        self.root = Tk()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # This is for the separate participant window
        extended_screen_width = int(screen_width * 1.5)
        extended_screen_height = int(screen_height * 1.3)

        
        
        if singleScreen:
            # When we are checking we will not have double screen
            self.gameScreen = GameWindow.getInstance(score_plan = score_plan,
                                                     screenDim=[screen_width,
                                                                screen_height])   
            self.root.geometry("%sx%s+%s+%s" % (screen_width, 
                                                screen_height, 
                                                0,
                                                0))
        else:
            # When we are with participant we will want double screen
            # ASSUMPTION: Participant screen is to the right of the main screen
            self.gameScreen = GameWindow.getInstance(score_plan = score_plan,
                                                     screenDim=[extended_screen_width,
                                                            extended_screen_height])   
            
            self.root.geometry("%sx%s+%s+%s" % (extended_screen_width, 
                                                extended_screen_height, 
                                                screen_width,
                                                0))
        self.root.resizable(0, 0)
    
        
        
            
            
        
        
if __name__ =='__main__':
    checkScreen = Screen()
    from constants import SCORE_SETS
    from game_engine import GoalStatements
    checkScreen.setup(score_plan=SCORE_SETS["score_set2"], singleScreen=True)
    statements = GoalStatements(score_plan=SCORE_SETS["score_set2"]).statements
    ex = checkScreen.gameScreen   
    while True:
        ex.show_play_screen(10,0, P_O)
        ex.show_selection(P_O,2)
        ex.show_goal_statement(statements[1])
        time.sleep(0.5)
    try:
        pass
        checkScreen.root.mainloop()
    finally:
        try:
            ex.master.destroy()
        except:
            pass
            
               
