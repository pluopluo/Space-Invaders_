## importing code files
## basic python setup
import random
import pygame
from pygame.locals import *
from customcolors import *
from pygame import mixer
def show_text(msg, x, y, color, size):
        fontobj= pygame.font.SysFont("freesans", size)
        msgobj = fontobj.render(msg,False,color)
        screen.blit(msgobj,(x, y))
pygame.init()
screen = pygame.display.set_mode((480,480))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()                         

## setting up the game play
def MainGame_1():

    def Close():
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            ## skipping if the enter key is pressed
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:              
                    nonlocal Flag_Skip
                    if Flag_Skip == False:
                        Flag_Skip = True

    def Pause(time):
        for counter in range(0,time*10):
            Close()
            clock.tick(10)

    def Collide(object_1,object_2):
        if object_1.xpos + object_1.length > object_2.xpos and object_2.xpos + object_2.length > object_1.xpos:
            if object_1.ypos + object_1.height > object_2.ypos and object_2.ypos + object_2.height > object_1.ypos:
                return True
            
    def Alien_Barrier_Collision(alien,Barrier):
        Barrier_Iteration_Counter = 0
        Barrier_Struck = False
        while True:
            if Barrier_Iteration_Counter == len(Barrier):
                break
            if alien.xpos + alien.length >= Barrier[Barrier_Iteration_Counter].xpos and alien.xpos <= Barrier[Barrier_Iteration_Counter].xpos + Barrier[Barrier_Iteration_Counter].length:
                if alien.ypos + alien.height >= Barrier[Barrier_Iteration_Counter].ypos:
                    Barrier_Struck = True
            if Barrier_Struck == True:
                Barrier.pop(Barrier_Iteration_Counter)
                Barrier_Struck = False
            else:
                Barrier_Iteration_Counter = Barrier_Iteration_Counter + 1

    def Bullet_Barrier_Collision(Barrier,bullet):
        ## declaring nonlocals to the bullet lists and the bullet explosion list
        nonlocal player_1_bullets, player_2_bullets, alien_bullets, Bullet_Explosion_List
    
        ## checking what type of bullet it is and what iteration should be performed ont he Barrier
        if bullet in alien_bullets:
            Barrier_Iteration = [0,len(Barrier),1]
            
        elif bullet in player_1_bullets or bullet in player_2_bullets:
            Barrier_Iteration = [len(Barrier) - 1,-1,-1]
         
        ## checking the Barrier and if the divisor is supposed to be 2
        if Barrier == alien_invasion_line:
            divisor = 2
        else:
            divisor = 1

        Target_Barrier = None
        ## checking the specific particle the bullet hits
        for i in range(Barrier_Iteration[0],Barrier_Iteration[1],Barrier_Iteration[2]):
            if Collide(bullet,Barrier[i]) == True:
                Target_Barrier = Barrier[i]
                Barrier_Iteration_Counter = 0
                Barrier_Struck = False
                while True:
                    # breaking the bullet and the while loop
                    if Barrier_Iteration_Counter >= len(Barrier):
                        if bullet in alien_bullets:
                            alien_bullets.remove(bullet)
                        if bullet in player_1_bullets:
                            player_1_bullets.remove(bullet)
                        if bullet in player_2_bullets:
                            player_2_bullets.remove(bullet)
                        break
                
                    ## checking if the xpos is correct
                    if Barrier[Barrier_Iteration_Counter].xpos%(divisor*2) == 0:
                        ## checking if the Barrier particle is in close range of the area hit by the bullet
                        if Target_Barrier.xpos - bullet.Dr[0]*2 < Barrier[Barrier_Iteration_Counter].xpos < Target_Barrier.xpos + Target_Barrier.length + bullet.Dr[0]:
                            if Target_Barrier.ypos - bullet.Dr[1]*2 < Barrier[Barrier_Iteration_Counter].ypos < Target_Barrier.ypos + Target_Barrier.height + bullet.Dr[1]*2:
                                Barrier_Struck = True
                            
                        ## checking if the Barrier particle is in far range of the area struck by the bullet
                        if Target_Barrier.xpos - bullet.Dr[2]*2 < Barrier[Barrier_Iteration_Counter].xpos < Target_Barrier.xpos + Target_Barrier.height + bullet.Dr[2]*2:
                            if Target_Barrier.ypos - bullet.Dr[3]*2 < Barrier[Barrier_Iteration_Counter].ypos < Target_Barrier.ypos + Target_Barrier.height + bullet.Dr[3]*2:
                                # deciding how far it is and the chance of the Barrier being destroyed
                                y_distance = abs(Target_Barrier.ypos - Barrier[Barrier_Iteration_Counter].ypos) + 1
                                x_distance = abs(Target_Barrier.xpos - Barrier[Barrier_Iteration_Counter].xpos) + 1
                                x_range = x_distance//(bullet.Dr[2])
                                y_range = y_distance//(bullet.Dr[3])
                                if random.randint(0,x_range) == 0 and random.randint(0,y_range) == 0:
                                    Barrier_Struck = True

                    ## destroying the Barrier partlce
                    if Barrier_Struck == True:
                        Barrier.pop(Barrier_Iteration_Counter)
                        Barrier_Struck = False
                    else:
                        Barrier_Iteration_Counter = Barrier_Iteration_Counter + 1
                break
            
    def Update_Score(score):            
        if score.phrase[2] >= 10:
            score.phrase[1] = score.phrase[1] + 1
            score.phrase[2] = score.phrase[2] - 10
        if score.phrase[1] >= 10:
            score.phrase[0] = score.phrase[0] + 1
            score.phrase[1] = score.phrase[1] - 10
        if score.phrase[0] >= 10:
            score.phrase[0] = score.phrase[0] - 10
        
    def Player_Explode(player):
        ## nonlocal declaration to variables and lists
        nonlocal alien_bullets, player_1_bullets, player_2_bullets
        nonlocal player_1, player_2, player_1_life, player_2_life
        nonlocal Flag_Gameover
 
        ## playing the sound
        Player_Explosion.Sound.play()                

        ## uploading the player_explosion images
        player_explosion = Player_Explosion(player.xpos,player.ypos,40,20)

        ## drawing the player_explosion
        for iteration in range(1,20):
            for animation in range(1,3):
                player_explosion.Draw(animation)
                Close()
                pygame.display.update()
                clock.tick(15)
                
        ## emptying the player explosion from the screen by drawing a black rectangle
        player_explosion.Draw(3)
        
        ## drawing the player afterwards
        if player == player_1:
            if player_2 != None:
                player_2.Draw('blue')
                player_2.Flag_Movement_Direction = None
        elif player == player_2:
            if player_1 != None:
                player_1.Draw('green')
                player_1.Flag_Movement_Direction = None
        
        pygame.display.update()
        Pause(2)


        if player == player_1:
            if len(player_1_backup) != 0:

                ## resetting the player's attributes
                player_1.Flag_Movement_Direction = None
                player_1.Flag_Struck = False
                player_1.ypos = 400
                player_1.xpos = 50

                ## changing the player's lives
                player_1_backup.pop(-1)
                player_1_life.phrase[0] = player_1_life.phrase[0] - 1

            elif len(player_1_backup) == 0:

                ## removing the player from the game
                player_1 = None


        elif player == player_2:
            if len(player_2_backup) != 0:

                ## resetting the player's attributes
                player_2.Flag_Movement_Direction = None
                player_2.Flag_Struck = False
                player_2.ypos = 400
                player_2.xpos = 90
                
                ## changing the player's lives
                player_2_backup.pop(-1)
                player_2_life.phrase[0] = player_2_life.phrase[0] - 1

            elif len(player_2_backup) == 0:

                ## removing the player from the game
                player_2 = None

        ## checking if the game ends
        if player_1 == None and player_2 == None:
            Flag_Gameover = True

    def Alien_Refill(Start_Game=False):

        ## nonlocal declaration to the lists and variables
        nonlocal aliens
        nonlocal Flag_Game_Level

        ## resetting all the alien attributes
        Alien.Timer = 20
        Alien.Animation = 0
        Alien.Flag_Collide_Side = None
        Alien.Flag_Down_Step = None
        Alien.Speed = 5

        ## resetting alien movement sounds and position moving down the screen afters each level
        Alien.Counter_Background_Sound = 1 
        if Start_Game == True:
            Flag_Game_Level = 0
        
        ## increasing the level of the game
        Flag_Game_Level = Flag_Game_Level + 1

        ## layouts for various levels
        if Flag_Game_Level == 1:
            alien_x_distance = 30
            alien_y_distance = 30
            alien_y_start_pos = 120
            alien_x_start_pos = 100
            alien_layout = [[1,1,1,1,1],
                            [1,1,1,1,1],
                            [1,1,1,1,1],
                            [1,1,1,1,1]]
        
        elif Flag_Game_Level == 2:
            alien_x_distance = 30
            alien_y_distance = 30
            alien_y_start_pos = 120
            alien_x_start_pos = 100
            alien_layout = [[1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1]]

        elif Flag_Game_Level == 3:
            alien_x_distance = 20
            alien_y_distance = 20
            alien_y_start_pos = 120
            alien_x_start_pos = 100
            alien_layout = [[0,0,1,0,0,0,0,0,1,0,0],
                            [0,0,0,1,0,0,0,1,0,0,0],
                            [0,0,1,1,1,1,1,1,1,0,0],
                            [0,1,1,0,1,1,1,0,1,1,0],
                            [1,1,1,1,1,1,1,1,1,1,1],
                            [1,0,1,1,1,1,1,1,1,0,1],
                            [1,0,1,0,0,0,0,0,1,0,1],
                            [0,0,0,1,1,0,1,1,0,0,0]]
   

        elif Flag_Game_Level == 4:
            alien_x_distance = 20
            alien_y_distance = 15
            alien_y_start_pos = 120
            alien_x_start_pos = 100
            alien_layout = [[1,1,0,0,0,0,0,0,1,1],
                            [1,1,0,0,0,0,0,0,1,1],
                            [1,1,0,0,0,0,0,0,1,1],
                            [1,1,0,0,2,0,0,0,1,1],
                            [0,1,1,0,0,0,0,1,1,0],
                            [0,1,1,0,0,0,0,1,1,0],
                            [0,1,1,0,0,0,0,1,1,0],
                            [0,0,1,1,0,0,1,1,0,0],
                            [0,0,1,1,0,0,1,1,0,0],                 
                            [0,0,0,1,1,1,1,0,0,0],  
                            [0,0,0,1,1,1,1,0,0,0],
                            [0,0,0,0,1,1,0,0,0,0]]


        elif Flag_Game_Level == 5:
            alien_x_distance = 30
            alien_y_distance = 30
            alien_y_start_pos = 100
            alien_x_start_pos = 120
            alien_layout = [[2,0,2,0,2,0,2],
                            [0,0,0,0,0,0,0],
                            [0,0,2,0,2,0,0],
                            [0,0,0,0,0,0,0],
                            [2,0,2,0,2,0,2]]
        

        elif Flag_Game_Level == 6:
            alien_x_distance = 20
            alien_y_distance = 20
            alien_y_start_pos = 80
            alien_x_start_pos = 40
            alien_layout = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],
                            [0,0,0,0,1,0,0,0,0,0,1,0,0,0,0],
                            [0,0,0,1,0,2,0,0,2,0,0,1,0,0,0],
                            [0,0,0,1,0,0,0,0,0,0,0,1,0,0,0],
                            [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                            [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1],
                            [0,0,1,1,1,1,1,1,1,1,1,1,1,0,0],
                            [0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
                            [0,0,1,0,0,0,0,1,0,0,0,0,1,0,0],
                            [0,1,0,0,0,0,0,1,0,0,0,0,0,1,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

        elif Flag_Game_Level == 7:
            alien_x_distance = 20
            alien_y_distance = 20
            alien_y_start_pos = 40
            alien_x_start_pos = 110
            alien_layout = [[0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,3,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0],
                            [1,1,1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1,1,1],
                            [1,1,1,1,1,1,1,1,1,1,1,1]]
        
        elif Flag_Game_Level == 8:
            alien_x_distance = 20
            alien_y_distance = 20
            alien_y_start_pos = 100
            alien_x_start_pos = 60
            alien_layout = [[0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [3,0,0,0,0,0,3,0,0,0,0,0,3],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0]]
        

        elif Flag_Game_Level == 9:
            alien_x_distance = 20
            alien_y_distance = 15
            alien_y_start_pos = 60
            alien_x_start_pos = 40
            alien_layout = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0],
                            [0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0],
                            [0,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0],
                            [0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
                            [0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,0,0,0,0],
                            [0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0],
                            [0,0,0,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0],
                            [0,0,0,0,0,1,1,0,1,1,1,0,0,1,1,0,0,0,0],
                            [0,0,0,0,1,1,0,1,1,0,1,1,0,1,1,0,0,0,0],
                            [0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,0,0,0,0],
                            [0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]


        elif Flag_Game_Level == 10:
            alien_x_distance = 20
            alien_y_distance = 20
            alien_y_start_pos = 100
            alien_x_start_pos = 60
            alien_layout = [[0],
                            [4],
                            [0]]
            
        elif Flag_Game_Level == 11:
            alien_x_distance = 30
            alien_y_distance = 30
            alien_y_start_pos = 60
            alien_x_start_pos = 60
            alien_layout = [[0,0,0,0,0,0,0,0,0],
                            [2,0,2,0,2,0,2,0,2],
                            [0,0,0,0,0,0,0,0,0],
                            [2,0,2,0,2,0,2,0,2],
                            [0,0,0,0,0,0,0,0,0],
                            [2,0,2,0,2,0,2,0,2],
                            [0,0,0,0,0,0,0,0,0],
                            [2,0,2,0,2,0,2,0,2]]
            
        elif Flag_Game_Level == 12:
            alien_x_distance = 20
            alien_y_distance = 15
            alien_y_start_pos = 80
            alien_x_start_pos = 60
            alien_layout = [[1,1,1,1,1,0,1,0,0,0,1,0,1,1,1,1],
                            [0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0],
                            [0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0],
                            [0,0,1,0,0,0,1,1,1,1,1,0,1,1,1,1],
                            [0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0],
                            [0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0],
                            [0,0,1,0,0,0,1,0,0,0,1,0,1,1,1,1],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [1,1,1,1,0,1,0,0,0,1,0,1,1,1,1,0],
                            [1,0,0,0,0,1,1,0,0,1,0,1,0,0,0,1],
                            [1,0,0,0,0,1,0,1,0,1,0,1,0,0,0,1],
                            [1,1,1,1,0,1,0,1,0,1,0,1,0,0,0,1],
                            [1,0,0,0,0,1,0,1,0,1,0,1,0,0,0,1],
                            [1,0,0,0,0,1,0,0,1,1,0,1,0,0,0,1],
                            [1,1,1,1,0,1,0,0,0,1,0,1,1,1,1,0]]

    
        ## filling the aliens
        for row in range(len(alien_layout) - 1,-1,-1):
            for column in range(len(alien_layout[row]) - 1,-1,-1):
                if alien_layout[row][column] >= 1:
                    ## adding the aliens to the group list
                    if row > 3/5*len(alien_layout):
                        aliens.append(Alien(column*alien_x_distance + alien_x_start_pos,row*alien_y_distance + alien_y_start_pos,2,alien_layout[row][column]))
                    elif row > 1/5*len(alien_layout):
                        aliens.append(Alien(column*alien_x_distance + alien_x_start_pos,row*alien_y_distance + alien_y_start_pos,1,alien_layout[row][column]))
                    else:
                        aliens.append(Alien(column*alien_x_distance + alien_x_start_pos,row*alien_y_distance + alien_y_start_pos,3,alien_layout[row][column]))


    def Barrier_Refill():
        ## globalizing the Barrier lists
        nonlocal Barrier1,Barrier2,Barrier3,Barrier4,alien_invasion_line

        ## filling the Barrier lists
        for row in range(0,len(Barrier_layout)):
            for column in range(len(Barrier_layout[row])):
                if Barrier_layout[row][column] == 1:
                    Barrier1.append(Barrier(column*2 + 48,row*2 + 330))
                    Barrier2.append(Barrier(column*2 + 156,row*2 + 330))
                    Barrier3.append(Barrier(column*2 + 264,row*2 + 330))
                    Barrier4.append(Barrier(column*2 + 372,row*2 + 330))
        
        ## filling the alien invasion line
        for row in range(0,1):
            for column in range(0,480):
                alien_invasion_line.append(Barrier(column*2,row*2 + 435))

    def Fill_Black():
        nonlocal Flag_Skip
        Flag_Skip  = 'stage_2'
        for xpos in range(0,480,120):
            pygame.draw.rect(screen,black,(xpos,0,120,480))
            Close()
            pygame.display.update()
            clock.tick(20)

    def Screen_Draw():      
        screen.fill(black)

        ## drawing the score
        score_message.Draw()
        player_1_score.Draw()
        player_2_score.Draw()
        high_score.Draw()
        player_1_life.Draw()
        player_2_life.Draw()

        ## drawing the floor
        for Barrier_particle in alien_invasion_line:
            Barrier_particle.Draw()

        ## drawing the Barrier
        for Barrier_particle in Barrier1:
            Barrier_particle.Draw()
        for Barrier_particle in Barrier2:
            Barrier_particle.Draw()
        for Barrier_particle in Barrier3:
            Barrier_particle.Draw()
        for Barrier_particle in Barrier4:
            Barrier_particle.Draw()
        

        ## drawing the players 
        player_1.Draw('green')
        if player_2 != None:
            player_2.Draw('blue')
        for player in player_1_backup:
            player.Draw('green')
        for player in player_2_backup:
            player.Draw('blue')
        
        ## drawing the aliens and closing the screen if the quit button is pressed
        for alien in aliens:
            alien.Draw('white')
            Close()
            pygame.display.update()
            clock.tick(60)

    def Level_Draw():
        nonlocal Flag_Game_Level

        # emptying out the screen
        pygame.draw.rect(screen,black,(0,180,480,300))

        # drawing the level message
        level_message_list = ['L','E','V','E','L','space',Flag_Game_Level]
        level_message = Words_And_Phrases(187,180,level_message_list)
        level_message.Draw()

        pygame.display.update()
        Pause(2)

    ## main class
    class Game_Element:
        Basic_Sound_Url = 'Space-Invaders\Sounds\\'
        Basic_Url = 'Space-Invaders\Images\\'
        def __init__(self,xpos,ypos):
            self.xpos = xpos
            self.ypos = ypos

    class Words_And_Phrases(Game_Element):
        ## uploading all the character names
        Character_Dictionary = {}
        Character_Name_List = ['A','B','C','D','E','E','F','G','H','I','J','K','L','M','N',
                                'O','P','Q','R','S','T','U','V','W','X','Y','Z','SPACE',0,1,2,
                                 3,4,5,6,7,8,9,'left','right','equal','asterisk','question_mark','dash','space','yflip']
        
        ## uploading all the character
        Character_Image_List = []
        for character_name in Character_Name_List:
            Character_Image_List.append(pygame.image.load(Game_Element.Basic_Url+'letters\\'+str(character_name)+'.jpeg'))
     
        ## storing the resized character images into a dictionary with the value of the respective character name 
        for index in range(len(Character_Name_List)):
            character_image = Character_Image_List[index]
            resized_character_image = pygame.transform.scale(character_image,(10,14))
            Character_Dictionary[Character_Name_List[index]] = resized_character_image
            
        def __init__(self,xpos,ypos,phrase):
            super().__init__(xpos,ypos)
            self.phrase = phrase
        def Draw(self,delay=0):
            Counter_Spacing = 0
            for character in self.phrase:

                ## checking if it is to be skipped
                if Player_Selected == True:
                    if Flag_Skip == True or Flag_Skip == 'stage_2':
                        if Flag_Skip == True:
                            Fill_Black()
                        break

                ## drawing the letter
                screen.blit(Words_And_Phrases.Character_Dictionary[character],(self.xpos + Counter_Spacing,self.ypos))
                Counter_Spacing = Counter_Spacing + 15

                ## pausing if there is a delay
                if delay != 0:
                    Close()
                    pygame.display.update()
                    clock.tick(delay)

    class Alien(Game_Element):                                                                                                                                                                                 
        ## movement
        Speed = 5
        Timer = 20
        Flag_Collide_Side = None
        Flag_Down_Step = False
        
        ## counters
        Counter_Background_Sound = 1

        ## animation
        Current_Animation = 0
        
        ## setting up the letter interaction images from the start screen
        Letter_Flip_Image_List = []

        for image_number in range(1,5):

            ## loading and transforming the image then adding it to the list
            img = pygame.image.load(Game_Element.Basic_Url+'Alien Letter Flip\Interaction '+str(image_number)+'.jpeg')
            img = pygame.transform.scale(img,(32,15))
            Letter_Flip_Image_List.append(img)
        
        ## setting up the alien images
        Image_List = []

        for alien_size in [1,2,3,4,5]:
            alien_color_list = []
            for alien_color in ['White','Green']:
                alien_type_list = []
                for alien_type in range(1,4):
                    alien_animation_list = []
                    for animation_frame in range(1,3):

                        ## deciding the length of the aliens depending on it's type
                        if alien_type == 3:
                            alien_length = 15
                        else:
                            alien_length = 20

                        ## loading the image
                        img = pygame.image.load(Game_Element.Basic_Url+'Alien\\'+str(alien_color)+' '+str(alien_type)+' '+str(animation_frame)+'.jpeg')
                        alien_scale_factor = 2**(alien_size - 1)

                        ## transforming the image
                        img = pygame.transform.scale(img,(alien_length*alien_scale_factor,15*alien_scale_factor))

                        ## storing the images in lists
                        alien_animation_list.append(img)
                    alien_type_list.append(alien_animation_list)
                alien_color_list.append(alien_type_list)
            Image_List.append(alien_color_list)

        def __init__(self,xpos,ypos,type,size):
            super().__init__(xpos,ypos)
            self.type = type
            self.size = size
            self.health = 2**(self.size - 1)

            ## deciding it's length and width
            if self.type == 3:
                self.length = 15
                self.height = 15
            else:
                self.length = 20
                self.height = 15
            
            self.length = self.length*self.health
            self.height = self.height*self.health
 
        def Move_Alien(self):
            self.xpos = self.xpos + self.Speed

            ## checking if the alien hits the edge
            if self.xpos + self.length >= 440:
                Alien.Flag_Collide_Side = 'right'
            elif self.xpos <= 35:
                Alien.Flag_Collide_Side = 'left'

        def Move_Down(self):
            self.ypos = self.ypos + 15
            if Alien.Flag_Collide_Side == 'left':
                Alien.Speed = 5
            elif Alien.Flag_Collide_Side == 'right':
                Alien.Speed = -5
            Alien.Flag_Collide_Side = None

        def Check(self):

            ## checking if the aliens reach the Barrier
            if self.ypos + self.height > 330 and self.ypos < 370:
                if self.xpos + self.length > 48 and self.xpos < 108:
                    Alien_Barrier_Collision(self,Barrier1)
                elif self.xpos + self.length > 156 and self.xpos < 216:
                    Alien_Barrier_Collision(self,Barrier2)
                elif self.xpos + self.length > 264 and self.xpos < 324:
                    Alien_Barrier_Collision(self,Barrier3)
                elif self.xpos + self.length > 372 and self.xpos < 432:
                    Alien_Barrier_Collision(self,Barrier4)

            # checking if the aliens hit the invasion line or invade
            if self.ypos + self.height >= 435:
                nonlocal Flag_Gameover
                Flag_Gameover = True

        def Shoot(self):
            ## aliens shooting a bullet at player 1
            if player_1 != None:
                if self.xpos + self.length > player_1.xpos and player_1.xpos + player_1.length > self.xpos:
                    if random.randint(1,70) == 1:
                        alien_bullets.append(Alien_Bullet(self.xpos + self.length/2,self.ypos + self.height))
            
            # aliens shooting a bullet at player 2
            if player_2 != None:
                if self.xpos + self.length > player_2.xpos and player_2.xpos + player_2.length > self.xpos:
                    if random.randint(1,70) == 1:
                        alien_bullets.append(Alien_Bullet(self.xpos + self.length/2,self.ypos + self.height))

        def Split(self):

            ## removing the alien from the screen
            aliens.remove(self)

            ## checking if the alien should explode
            if self.size == 1:
                    
                    ## adding the explosion to the explosion list
                    Alien_Explosion_List.append(Alien_Explosion(self.xpos,self.ypos))
            
            ## checking if the size is greater then 1 and making it split
            elif self.size > 1:
                    
                    ## adding more aliens to the screen
                    for row in range(0,2):
                        for column in range(0,2):
                            aliens.append(Alien(self.xpos + row*self.length/2,self.ypos + column*self.height/2,self.type,self.size - 1))

        def Draw(self,color='white'):
            if color == 'white':
                return screen.blit(Alien.Image_List[self.size - 1][0][self.type - 1][Alien.Current_Animation],(self.xpos,self.ypos))
            elif color == 'green':
                return screen.blit(Alien.Image_List[self.size - 1][1][self.type - 1][Alien.Current_Animation],(self.xpos,self.ypos))
            elif color == 'red':
                return screen.blit(Alien.Image_List[self.size - 1][2][self.type - 1][Alien.Current_Animation],(self.xpos,self.ypos))

        def Draw_Letter_Take(self):
            return screen.blit(Alien.Letter_Flip_Image_List[self.Current_Animation],(self.xpos - 8,self.ypos))
        def Draw_Letter_Place(self):
            return screen.blit(Alien.Letter_Flip_Image_List[self.Current_Animation + 2],(self.xpos - 8,self.ypos))

    class Player(Game_Element):
        ## setting up the shoot sound
        Shoot_Sound = mixer.Sound(Game_Element.Basic_Sound_Url+'player shoot sound.wav')

        ## setting up the flag variables
        Flag_Struck = False
        Flag_Movement_Direction = None

        ## setting up the counter variables
        Shoot_Iteration_Counter = 0
        Lucky_Shot = False
        
        ## setting up the player's image
        Img = pygame.image.load(Game_Element.Basic_Url+'Player\\player green.jpeg')
        Green_Image = pygame.transform.scale(Img,(30,20))

        Img = pygame.image.load(Game_Element.Basic_Url+'Player\\player blue.jpeg')
        Blue_Image = pygame.transform.scale(Img,(30,20))

        ## setting up the shoot timer
        Shoot_Timer = 0

        def __init__(self,xpos,ypos):
            super().__init__(xpos,ypos)
            self.length = 30
            self.height = 20
            self.uplift = 0

        def Move_Player(self):
            ## updating the shoot timer
            if self.Shoot_Timer > 0:
                self.Shoot_Timer = self.Shoot_Timer - 1
            
            if self.Flag_Movement_Direction == 'left':
                self.xpos = self.xpos - 3
            elif self.Flag_Movement_Direction == 'right':
                self.xpos = self.xpos + 3
            if self.xpos > 410:
                self.xpos = 410
            elif self.xpos < 35:
                self.xpos = 35
        
        def Draw(self,color='green'):
            if color == 'green':
                return screen.blit(Player.Green_Image,(self.xpos,self.ypos))
            elif color == 'blue':
                return screen.blit(Player.Blue_Image,(self.xpos,self.ypos))

    class Mystery_Ship(Game_Element):
        ## adding the images
        Img = pygame.image.load(Game_Element.Basic_Url+'Mystery Ship\Mystery Ship Red.jpeg')
        Image = pygame.transform.scale(Img,(32,14))
        
        ## adding the sounds
        Low_Sound = mixer.Sound(Game_Element.Basic_Sound_Url+'mystery ship low sound.wav')
        Sound_Iteration_Counter = 10

        def __init__(self,xpos,ypos):
            super().__init__(xpos,ypos)
            self.length = 32
            self.height = 14

        def Move_Mystery_Ship(self):
            ## moving the mystery ship
            self.xpos = self.xpos - 2
            ## checking if it should be replaced and the sound counter is also fixed
            if self.xpos + self.length < 0:
                self.xpos = 2500
                self.Sound_Iteration_Counter = 10

        def Draw(self):
            return screen.blit(Mystery_Ship.Image,(self.xpos,self.ypos))
            
        def Play_Sound(self):
            ## playing it's sound
            if self.xpos < 480:
                if self.Sound_Iteration_Counter >= 10:
                    self.Low_Sound.play()
                    self.Sound_Iteration_Counter = 0
                self.Sound_Iteration_Counter = self.Sound_Iteration_Counter + 1
                
    class Player_Bullet(Game_Element):
        ## uploading images
        img = pygame.image.load(Game_Element.Basic_Url+'Player Bullet\player bullet white.jpeg')
        White_Image = pygame.transform.scale(img,(2,16))
        img = pygame.image.load(Game_Element.Basic_Url+'Player Bullet\player bullet blue.jpeg')
        Blue_Image = pygame.transform.scale(img,(2,16))
        img = pygame.image.load(Game_Element.Basic_Url+'Player Bullet\player bullet green.jpeg')
        Green_Image = pygame.transform.scale(img,(2,16))

        ## setting up the sound
        Alien_Collide_Sound = mixer.Sound(Game_Element.Basic_Sound_Url+'alien shot sound.wav')

        ## setting up the destruction ranges
        Dr = [2,5,4,7]

        def __init__(self,xpos,ypos):
            super().__init__(xpos,ypos)
            self.height = 16
            self.length = 2 

        def Move_Bullet(self):
            self.ypos = self.ypos - 5

        def Check(self):
            ## declaring nonlocals to the bullets and scores
            nonlocal player_1_bullets, player_2_bullets
            nonlocal player_1_score, player_2_score

            ## checking if the player_1_bullets hit the Barriers
            if self.ypos + self.height > 330 and self.ypos < 370:
                if self.xpos + self.length > 48 and self.xpos < 108:
                    Bullet_Barrier_Collision(Barrier1,self)
                elif self.xpos + self.length > 156 and self.xpos < 216:
                    Bullet_Barrier_Collision(Barrier2,self)
                elif self.xpos + self.length > 264 and self.xpos < 324:
                    Bullet_Barrier_Collision(Barrier3,self)
                elif self.xpos + self.length > 372 and self.xpos < 432:
                    Bullet_Barrier_Collision(Barrier4,self)

            ## checking if the bullets hit the alien
            if self in player_1_bullets or self in player_2_bullets:
                for alien in aliens:
                    if Collide(alien,self) == True:

                        ## playing the alien collide sound
                        Player_Bullet.Alien_Collide_Sound.play()

                        ## subtracting health from the aliens
                        alien.health = alien.health - 1
                        
                        ## checking if the alien's health is equal to zero
                        if alien.health == 0:

                            ## splitting the alien
                            alien.Split()
                        else:
                            ## removing the bullet from the player bullet's list
                            if self in player_1_bullets:
                                player_1_bullets.remove(self)
                            elif self in player_2_bullets:
                                player_2_bullets.remove(self)
                            
                            ## breaking otherwise because the player's score are not updated unless the alien disappears
                            break

                        ## checking how much should be added to the scores based on the alien type
                        increment = 0
                        if alien.type == 2:
                            increment = 1
                        elif alien.type == 1:
                            increment = 2
                        elif alien.type == 3:
                            increment = 3

                        ## updating the player scores and removing the player's bullet
                        if self in player_1_bullets:
                            player_1_bullets.remove(self)
                            player_1_score.phrase[2] = player_1_score.phrase[2] + increment
                        elif self in player_2_bullets:
                            player_2_bullets.remove(self)

                        ## updating the high score
                        high_score.phrase[2] = high_score.phrase[2] + increment
                        break 

                    if self not in player_1_bullets and self not in player_2_bullets:
                        break

            ## checking if the bullet hits the mystery ship
            if self in player_1_bullets:
                if Collide(self,mystery_ship) == True:

                    ## checking if the player 1 bullets hits the mystery ship at the 15th shot and making it worth 300 points
                        if player_1.Lucky_Shot == True:
                            if (player_1.Shoot_Iteration_Counter - 23)%15 == 0:
                                Mystery_Ship_Explosion_List.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,300))
                                player_1_score.phrase[1] = player_1_score.phrase[1] + 3
                                high_score.phrase[1] = high_score.phrase[1] + 3
                            else:
                                player_1.Lucky_Shot = False

                    ## checking if otherwise and making it worth 200 points
                        if player_1.Lucky_Shot == False:
                            Mystery_Ship_Explosion_List.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,200))
                            player_1_score.phrase[1] = player_1_score.phrase[1] + 2
                            high_score.phrase[1] = high_score.phrase[1] + 2

                    ## checking if the player 1 bullet hits the mystery ship on the 23rd shot 
                        if player_1.Shoot_Iteration_Counter == 23:
                            player_1.Lucky_Shot = True

                    ## relocating the mystery ship
                        mystery_ship.xpos = 2500

                    ## removing the bullet from the bullet list
                        player_1_bullets.remove(self)

                    ## playing the mystery ship's explosion sound
                        Mystery_Ship_Explosion.Sound.play()

            elif self in player_2_bullets:
                if Collide(self,mystery_ship) == True:

                    ## checking if the player 2's bullets hits the mystery ship at the 15th shot and making it worth 300 points
                        if player_2.Lucky_Shot == True:
                            if (player_2.Shoot_Iteration_Counter - 23)%15 == 0:
                                Mystery_Ship_Explosion_List.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,300))
                                player_2_score.phrase[1] = player_1_score.phrase[1] + 3
                                high_score.phrase[1] = high_score.phrase[1] + 3
                            else:
                                player_2.Lucky_Shot = False

                    ## checking if otherwise and making it worth 200 points
                        if player_2.Lucky_Shot == False:
                            Mystery_Ship_Explosion_List.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,200))
                            player_2_score.phrase[1] = player_2_score.phrase[1] + 2
                            high_score.phrase[1] = high_score.phrase[1] + 2
                            
                    ## checking if the player 2's bullet hits the mystery ship on the 23rd shot
                        if player_2.Shoot_Iteration_Counter == 23:
                            player_2.Lucky_Shot = True

                    ## relocating the mystery ship
                        mystery_ship.xpos = 2500

                    ## removing the bullet from the bullet list
                        player_2_bullets.remove(self)

                    ## playing the mystery ship's explosion sound
                        Mystery_Ship_Explosion.Sound.play()
   
            ## checking if the hundreads or thousands place in the scores should be updated
            Update_Score(player_1_score)
            Update_Score(player_2_score)
            Update_Score(high_score)

            ## checking if the player bullet hits the top of the screen
            if self in player_1_bullets or self in player_2_bullets:
                if self.ypos < 0:
                    if self in player_1_bullets:
                        player_1_bullets.remove(self)
                    elif self in player_2_bullets:
                        player_2_bullets.remove(self)
                    Bullet_Explosion_List.append(Bullet_Explosion(self.xpos - 6,self.ypos))

        def Draw(self,color='white'):
            if color == 'white':
                return screen.blit(Player_Bullet.White_Image,(self.xpos,self.ypos))
            elif color == 'blue':
                return screen.blit(Player_Bullet.Blue_Image,(self.xpos,self.ypos))
            elif color == 'green':
                return screen.blit(Player_Bullet.Green_Image,(self.xpos,self.ypos))

    class Alien_Bullet(Game_Element):
        ## class variables
        Current_Animation = 1
        
        layout_1 = [[2,2,2,2,2,6],
                    [2,2,2,6,2,2],
                    [2,2,6,2,2,2],
                    [6,2,2,2,2,2]]
        layout_2 = [[2,2,4,5,2,4,5],
                    [2,2,4,5,2,4,5],
                    [5,4,2,5,4,2,2],
                    [5,4,2,5,4,2,2]]
        layout_3 = [[2,1,2,3,2,1,2],
                    [1,2,3,2,1,2,3],
                    [2,3,2,1,2,3,2],
                    [3,2,1,2,3,2,1]]
        
        ## uploading all the alien bullet images
        Image_List = []
        for color in ['White','Green']:
            color_list = []
            for image_particle in range(1,7):
                img = pygame.image.load(Game_Element.Basic_Url+'Alien Bullet\\alien bullet '+str(image_particle)+' '+str(color)+'.jpeg')
                img = pygame.transform.scale(img,(6,2))
                color_list.append(img)   
            Image_List.append(color_list)

        def __init__(self,xpos,ypos):
            ## setting up the cordinates and the type 
            self.xpos = xpos
            self.ypos = ypos
            self.type = random.randint(1,3)

            ## setting up the attributes such as the varying lengths, heights, the Barrier destruction range
            if self.type == 1:
                self.length = 6
                self.height = 12
                self.Dr = [2,5,4,7]
            elif self.type == 2:
                self.length = 6
                self.height = 14
                self.Dr = [2,5,4,8]
            elif self.type == 3:
                self.length = 6
                self.height = 14
                self.Dr = [3,5,5,7]
      
        def Move_Alien_Bullet(self):
                ## updating the animation
                self.Current_Animation = self.Current_Animation + 1
                if self.Current_Animation == 4:
                    self.Current_Animation = 0
                ## updating the y cordinates
                self.ypos = self.ypos + 3

        def Check(self):
            nonlocal alien_bullets, Bullet_Explosion_List
            alien_bullets_length = len(alien_bullets)
            ## checking if the alien_bullets hit the Barriers
            if self.ypos + self.height > 330 and self.ypos < 370:
                if self.xpos + self.length > 48 and self.xpos < 108:
                    Bullet_Barrier_Collision(Barrier1,self)
                elif self.xpos + self.length > 156 and self.xpos < 216:
                    Bullet_Barrier_Collision(Barrier2,self)
                elif self.xpos + self.length > 264 and self.xpos < 324:
                    Bullet_Barrier_Collision(Barrier3,self)
                elif self.xpos + self.length > 372 and self.xpos < 432:
                    Bullet_Barrier_Collision(Barrier4,self)

            ## checking if the alien_bullets hits the boundary line
            if self.ypos + self.height > 435 and len(alien_bullets) == alien_bullets_length:
                Bullet_Barrier_Collision(alien_invasion_line,self)
                if self in alien_bullets:
                    alien_bullets.remove(self)
                Bullet_Explosion_List.append(Bullet_Explosion(self.xpos - 3,self.ypos - 4,))

            ## checking if the alien_bullet hit the player bullet
            if len(alien_bullets) == alien_bullets_length:
                for bullet in player_1_bullets:
                    if self.xpos + self.length > bullet.xpos and bullet.xpos + bullet.length > self.xpos and self.ypos + self.height > bullet.ypos and bullet.ypos + bullet.height > self.ypos:
                        player_1_bullets.remove(bullet)
                        Bullet_Explosion_List.append(Bullet_Explosion(bullet.xpos - 6,bullet.ypos - 8))
                        if self.type == 1:
                            if random.randint(1,2) == 1:
                                alien_bullets.remove(self)
                        elif self.type == 2:
                            if random.randint(1,3) == 1:
                                alien_bullets.remove(self)
                        break

            if len(alien_bullets) == alien_bullets_length:
                for bullet in player_2_bullets:
                    if Collide(self,bullet) == True:
                        player_2_bullets.remove(bullet)
                        Bullet_Explosion_List.append(Bullet_Explosion(bullet.xpos - 6,bullet.ypos - 8))
                        if self.type == 1:
                            if random.randint(1,2) == 1:
                                alien_bullets.remove(self)
                        elif self.type == 2:
                            if random.randint(1,3) == 1:
                                alien_bullets.remove(self)
                        break

            # ## checking if the alien bullet hits the player
            if len(alien_bullets) == alien_bullets_length:
                if player_1 != None:
                    if Collide(self,player_1) == True:
                        alien_bullets.remove(self)
                        player_1.Flag_Struck = True

            if len(alien_bullets) == alien_bullets_length:
                if player_2 != None:
                    if Collide(self,player_2) == True:
                        alien_bullets.remove(self)
                        player_2.Flag_Struck = True

        def Draw(self):
            ## drawing the alien bullet
            counter_xpos = 0
            ## checking what type it is and drawing the right images
            if self.type == 1:
                for image_particle in Alien_Bullet.layout_1[self.Current_Animation]:
                    if self.ypos + 2 > 330:
                        screen.blit(Alien_Bullet.Image_List[1][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                    else:
                        screen.blit(Alien_Bullet.Image_List[0][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                    counter_xpos = counter_xpos + 2
            if self.type == 2:
                for image_particle in Alien_Bullet.layout_2[self.Current_Animation]:
                    if self.ypos + 2 > 330:
                        screen.blit(Alien_Bullet.Image_List[1][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                    else:
                        screen.blit(Alien_Bullet.Image_List[0][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                    counter_xpos = counter_xpos + 2
            if self.type == 3:
                for image_particle in Alien_Bullet.layout_3[self.Current_Animation]:
                    if self.ypos + 2 > 330:
                        screen.blit(Alien_Bullet.Image_List[1][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                    else:
                        screen.blit(Alien_Bullet.Image_List[0][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                    counter_xpos = counter_xpos + 2

    class Barrier(Game_Element):
        ## setting up the images according to this
        img = pygame.image.load(Game_Element.Basic_Url+'Barrier\\barrier particle.jpeg')
        green_image = pygame.transform.scale(img,(2,2))
        def __init__(self,xpos,ypos):
            super().__init__(xpos,ypos)
            self.length = 2
            self.height = 2
        def Draw(self):
            return screen.blit(Barrier.green_image,(self.xpos,self.ypos))

    ## setting up the scinario classes
    class Alien_Explosion(Game_Element):
        ## setting up the image
        Img = pygame.image.load(Game_Element.Basic_Url+'Alien Explosion\\alien explosion white.jpeg')
        White_Image = pygame.transform.scale(Img,(20,13))
        Img = pygame.image.load(Game_Element.Basic_Url+'Alien Explosion\\alien explosion green.jpeg')
        Green_Image = pygame.transform.scale(Img,(20,13))

        ## setting up the Existing_Timer
        Existing_Timer = 10

        def Update_Timer(self):
            self.Existing_Timer = self.Existing_Timer - 1
            if self.Existing_Timer == 0:
                nonlocal Alien_Explosion_List
                Alien_Explosion_List.remove(self)
        def Draw(self):
            if self.ypos + 13 > 330:
                screen.blit(Alien_Explosion.Green_Image,(self.xpos,self.ypos))
            else: 
                screen.blit(Alien_Explosion.White_Image,(self.xpos,self.ypos))

    class Mystery_Ship_Explosion(Alien_Explosion):

        ## uploading the images
        Img = pygame.image.load(Game_Element.Basic_Url+'Mystery Ship Explosion\\mystery ship explosion red.jpeg')
        Explosion_Image = pygame.transform.scale(Img,(42,16))
        Img = pygame.image.load(Game_Element.Basic_Url+'Mystery Ship Explosion\\mystery ship score 200 red.jpeg')
        Score_200_Image = pygame.transform.scale(Img,(40,14)) 
        Img = pygame.image.load(Game_Element.Basic_Url+'Mystery Ship Explosion\\mystery ship score 200 red.jpeg')
        Score_300_Image = pygame.transform.scale(Img,(40,14)) 

        ## setting up the existing timer
        Existing_Timer = 20

        ## setting up the sound
        Sound = mixer.Sound(Game_Element.Basic_Sound_Url+'mystery ship high sound.wav')

        def __init__(self,xpos,ypos,points=200):
            super().__init__(xpos,ypos)
            self.points = points

        def Update_Timer(self):
            self.Existing_Timer = self.Existing_Timer - 1
            if self.Existing_Timer == 0:
                nonlocal Mystery_Ship_Explosion_List
                Mystery_Ship_Explosion_List.remove(self)

        def Draw(self):
            if self.Existing_Timer > 10:
                screen.blit(Mystery_Ship_Explosion.Explosion_Image,(self.xpos - 4,self.ypos))
            else:
                if self.points == 300:
                    screen.blit(Mystery_Ship_Explosion.Score_300_Image,(self.xpos - 4,self.ypos))
                else:
                    screen.blit(Mystery_Ship_Explosion.Score_200_Image,(self.xpos - 4,self.ypos))

    class Bullet_Explosion(Game_Element):
        Img = pygame.image.load(Game_Element.Basic_Url+'Bullet Explosions\\bullet and bullet explosion.jpeg')
        Image = pygame.transform.scale(Img,(12,16))
        Explosion_Timer = 4
        def Draw(self):
            return screen.blit(Bullet_Explosion.Image,(self.xpos,self.ypos))

    class Player_Explosion(Game_Element):
        ## uploading the sound
        Sound = mixer.Sound(Game_Element.Basic_Sound_Url+'player explosion sound.wav')
        ## uploading the player explosion images
        Image_List = []
        for image_number in range(1,4):
            img = pygame.image.load(Game_Element.Basic_Url+'Player Explosion\player explosion '+str(image_number)+'.jpeg')
            Image_List.append(pygame.transform.scale(img,(40,20)))
        def __init__(self,xpos,ypos,length,height):
            super().__init__(xpos,ypos)
            self.length = length
            self.height = height
        def Draw(self,image_number):
            if image_number == 1:
                screen.blit(Player_Explosion.Image_List[0],(self.xpos,self.ypos))
            elif image_number == 2:
                screen.blit(Player_Explosion.Image_List[1],(self.xpos,self.ypos))
            elif image_number == 3:
                screen.blit(Player_Explosion.Image_List[2],(self.xpos,self.ypos))
    
    ## The Game Loop
    while True:
    ## setting up the menu 1
        ## setting up the words and messages
        please_select_message_list = ['P','L','E','A','S','E','space','S','E','L','E','C','T']
        please_select_message = Words_And_Phrases(140,100,please_select_message_list)

        one_or_two_players_message_list = [1,'space','O','R','space',2,'space','P','L','A','Y','E','R','S']
        one_or_two_players_message = Words_And_Phrases(135,140,one_or_two_players_message_list)

        one_player_message_list = [1,'P','L','A','Y','E','R']
        one_player_message = Words_And_Phrases(190,180,one_player_message_list)

        two_player_message_list = [2,'P','L','A','Y','E','R']
        two_player_message = Words_And_Phrases(190,220,two_player_message_list)

        ## setting up the select asterisk
        asterisk_list = ['asterisk']
        asterisk = Words_And_Phrases(170,180,asterisk_list)

        ## setting up the flag variable to begin the game
        Player_Selected = False

        ## setting up the mode variable
        Flag_Game_Mode = 'one_player'
        
        while True:
            screen.fill(black)

            ## drawing the phrases
            please_select_message.Draw()
            one_or_two_players_message.Draw()
            one_player_message.Draw()
            two_player_message.Draw()
            asterisk.Draw()

            ## basic key functions
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        asterisk = Words_And_Phrases(170,220,asterisk_list)
                        Flag_Game_Mode = 'two_player'
                    elif event.key == K_UP:
                        asterisk = Words_And_Phrases(170,180,asterisk_list)
                        Flag_Game_Mode = 'one_player'
                    elif event.key == K_RETURN:
                        Player_Selected = True
            pygame.display.update()
            clock.tick(60)
            if Player_Selected == True:
                break


        ## setting up the player's score and the high score
        score_message_list = ['S','C','O','R','E','left',1,'right','space','H','I','dash','S','C','O','R','E','space','S','C','O','R','E','left',2,'right']
        score_message = Words_And_Phrases(45,20,score_message_list)
        player_1_score = Words_And_Phrases(60,60,[0,0,0,0])
        player_2_score = Words_And_Phrases(320,60,[0,0,0,0])
        high_score = Words_And_Phrases(200,60,[0,0,0,0])

## setting up the menu 2

        ## skip flag variable
        Flag_Skip = False

        ## emptying the screen
        screen.fill(black)
        
        # drawing the player's score and high score

        score_message.Draw()
        player_1_score.Draw()
        player_2_score.Draw()
        high_score.Draw()

        # setting up and drawing the words and messages
        play_message_list = ['P','L','A']
        play_message = Words_And_Phrases(210,150,play_message_list)
        play_message.Draw(10)

        y_message = Words_And_Phrases(255,150,['yflip'])
        y_message.Draw(10)

        Space_Invaders_message_list = ['S','P','A','C','E','space','I','N','V','A','D','E','R','S']
        Space_Invaders_message = Words_And_Phrases(135,190,Space_Invaders_message_list)
        Space_Invaders_message.Draw(10)

        ## drawing the score_advance_table
        score_advance_table_message = ['asterisk','S','C','O','R','E','space','A','D','V','A','N','C','E','space','T','A','B','L','E','asterisk']
        score_advance_table = Words_And_Phrases(80,250,score_advance_table_message)
        score_advance_table.Draw(10)

        ## drawing the alien display
        if Flag_Skip == False:
            mystery_ship_display = Mystery_Ship(144,285)
            mystery_ship_display.Draw()
            
            alien_3_display = Alien(153,320,3,1)
            alien_3_display.Draw('white')

            alien_1_display = Alien(150,355,1,1)
            alien_1_display.Draw('white')

            alien_2_display = Alien(150,390,2,1)
            alien_2_display.Draw('white')

        ## drawing the alien values

        mystery_point_message_list = ['equal','question_mark','space','M','Y','S','T','E','R','Y']
        mystery_point_message = Words_And_Phrases(180,285,mystery_point_message_list)
        mystery_point_message.Draw(10)
        
        thirty_points_message_list = ['equal',3,0,'space','P','O','I','N','T','S']
        thirty_points_message = Words_And_Phrases(180,320,thirty_points_message_list)
        thirty_points_message.Draw(10)

        twenty_points_message_list = ['equal',2,0,'space','P','O','I','N','T','S']
        twenty_points_message = Words_And_Phrases(180,355,twenty_points_message_list)
        twenty_points_message.Draw(10)

        ten_points_message_list = ['equal',1,0,'space','P','O','I','N','T','S']
        ten_points_message = Words_And_Phrases(180,390,ten_points_message_list)
        ten_points_message.Draw(10)

    ## setting up the short alien film

        # making the alien
        start_alien = Alien(605,149,3,1)
        start_alien.Speed = -5

        ## moving the alien towards the letter to take it
        while True:
            ## breaking the loop if the skip variable is true
            if Flag_Skip == True or Flag_Skip == 'stage_2':
                if Flag_Skip == True:
                    Fill_Black()
                break
            ## drawing the words
            pygame.draw.rect(screen,black,(0,150,480,15))
            play_message.Draw()
            y_message.Draw()

            ## drawing the alien
            start_alien.Draw()
            start_alien.Move_Alien()

            ## checking if the alien reaches the cordinate of 265 where it will take the letter
            if start_alien.xpos == 260:

                ## changing the alien speed
                start_alien.Speed = 5

                Close()
                pygame.display.update()
                clock.tick(30)
                break

            Close()
            pygame.display.update()
            clock.tick(30)

        ## moving the alien away from the letter to take it away
        while True:
            ## breaking the loop if the skip variable is true
            if Flag_Skip == True or Flag_Skip == 'stage_2':
                if Flag_Skip == True:
                    Fill_Black()
                break
            
            ## drawing the words
            pygame.draw.rect(screen,black,(0,150,480,15))
            play_message.Draw()

            ## drawing the alien
            start_alien.Draw_Letter_Take()
            start_alien.Move_Alien()

            ## checking if the alien reaches the cordinate of 600 where it will flip the letter
            if start_alien.xpos == 600:

                ## changing the alien speed
                start_alien.Speed = -5

                Close()
                pygame.display.update()
                clock.tick(30)
                break

            Close()
            pygame.display.update()
            clock.tick(30)

        ## moving the alien towards the letter to replace it
        while True:
            ## breaking the loop if the skip variable is true
            if Flag_Skip == True or Flag_Skip == 'stage_2':
                if Flag_Skip == True:
                    Fill_Black()
                break
            ## drawing the words
            pygame.draw.rect(screen,black,(0,150,480,15))
            play_message.Draw()
            ## drawing the alien
            start_alien.Draw_Letter_Place()
            ## checking if the alien reaches the cordinate of 260 where it place the flipped letter
            if start_alien.xpos == 260:

                # flipping the letter
                y_message_list = ['Y']
                y_message = Words_And_Phrases(255,150,y_message_list)

                ## changing the alien speed
                start_alien.Speed = 5

                Close()
                pygame.display.update()
                clock.tick(30)
                break

            ## moving the alien
            start_alien.Move_Alien()

            Close()
            pygame.display.update()
            clock.tick(30)
        
        ## moving the alien away from the letter
        while True:
            ## breaking the loop if the skip variable is true
            if Flag_Skip == True or Flag_Skip == 'stage_2':
                if Flag_Skip == True:
                    Fill_Black()
                break
            ## drawing the words
            pygame.draw.rect(screen,black,(0,150,480,15))
            play_message.Draw()
            y_message.Draw()

            ## drawing the alien
            start_alien.Move_Alien()
            start_alien.Draw()

            ## checking if the alien reaches the cordinate of 600 where the game will begin
            if start_alien.xpos == 600:
                Close()
                pygame.display.update()
                clock.tick(30)
                break

            Close()
            pygame.display.update()
            clock.tick(30)

        ## deleting the start alien from no use
        del start_alien

        ## ending the flag skip if it has not happened
        if Flag_Skip != 'stage_2':
            Flag_Skip = 'done'
        else:
            Flag_Skip = 'stage_3'

# setting up the final signal for the game to begin
    ## drawing the first part
        for xpos in range(0,600,120):
            screen.fill(black)
            ## drawing the scores
            score_message.Draw()
            player_1_score.Draw()
            player_2_score.Draw()
            high_score.Draw()

            ## drawing the buttons
            push_message_list = ['P','U','S','H']
            push_message = Words_And_Phrases(210,180,push_message_list)
            push_message.Draw()

            ## drawing the message describing the one player buttons used
            if Flag_Game_Mode == 'one_player':
                only_one_player_button_message_list = ['O','N','L','Y','space',1,'P','L','A','Y','E','R','space','B','U','T','T','O','N']
                only_one_player_button_message = Words_And_Phrases(97,230,only_one_player_button_message_list)
                only_one_player_button_message.Draw()

            ## drawing the message describing the two player buttons used
            elif Flag_Game_Mode == 'two_player':
                only_two_player_button_message_list = [2,'P','L','A','Y','E','R','space','B','U','T','T','O','N']
                only_two_player_button_message = Words_And_Phrases(135,230,only_two_player_button_message_list)
                only_two_player_button_message.Draw()

            ## drawing the disappearing rectangle
            pygame.draw.rect(screen,black,(xpos,0,480 - xpos,480))

            ## displaying the rectangle and screen only when the player has skpped
            if Flag_Skip == 'stage_3':
                Close()
                pygame.display.update()
                clock.tick(20)

        pygame.display.update()
####        Pause(2)

    ## drawing the second part
        for i in range(1,31):
            screen.fill(black)
            if Flag_Game_Mode == 'one_player':
                ## blinking the first player's score and drawing the one player message
                one_player_message.Draw()
                if i%2 == 0:
                    player_1_score.Draw()

            if Flag_Game_Mode == 'two_player':
                ## blinking both players's score and drawing the two player message
                two_player_message.Draw()
                if i%2 == 0:
                    player_2_score.Draw()
                    player_1_score.Draw()
            else:
                player_2_score.Draw()

            ## drawing the rest of the score info
            score_message.Draw()
            high_score.Draw()
            
            Close()
            pygame.display.update()
####            clock.tick(15)

## setting up the basic variables
        ## setting up the Gameover Flag Variable
        Flag_Gameover = False
        Flag_Game_Level = 1
        
####        Level_Draw()

## setting up the elements

        ## setting up the player, their backup, and their live 
        player_1 = None
        player_2 = None
        player_1_backup = []
        player_2_backup = []
        player_1_life = Words_And_Phrases(10,456,[])
        player_2_life = Words_And_Phrases(460,456,[])

        if Flag_Game_Mode == 'one_player' or Flag_Game_Mode == 'two_player':
            player_1 = Player(50,400)
            player_1_backup = [Player(30,450),Player(70,450)]
            player_1_life.phrase = [2]
        if Flag_Game_Mode == 'two_player':
            player_2 = Player(90,400)
            player_2_backup = [Player(420,450),Player(380,450)]
            player_2_life.phrase = [2]
            
        aliens = []
        Alien_Refill(True)

        ## alien attributes
        Alien_Explosion_List = []

        ## setting up the Mystery_Ship
        mystery_ship = Mystery_Ship(2500,90)
        Mystery_Ship_Explosion_List = []
        
        ## setting up the Barrier layout
        Barrier_layout = [[0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
                        [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
                        [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
                        [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
                        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1]]

        ## setting up the Barrier and alien invasion line
        Barrier1 = []
        Barrier2 = []
        Barrier3 = []
        Barrier4 = []
        alien_invasion_line = []
        Barrier_Refill()

        ## setting up the bullet lists
        player_1_bullets = []
        player_2_bullets = []
        alien_bullets = []
        Bullet_Explosion_List = []
        
    # setting up the screen
####        Screen_Draw()

    ## starting the game
        while True:
            screen.fill(black)

        ## moving the player
            if player_1 != None:
                player_1.Move_Player()
            if player_2 != None:
                player_2.Move_Player()

        ## moving the mystery ship
            mystery_ship.Move_Mystery_Ship()
            mystery_ship.Play_Sound()

        ## moving aliens and changing animations only if there is at least one alien on the screen
            if len(Alien_Explosion_List) == 0:
                Alien.Timer = Alien.Timer - 1
                if  Alien.Timer <= 0:
                    Alien.Timer = 20

                    ## updating the alien's animation 
                    if Alien.Current_Animation == 0:
                        Alien.Current_Animation = 1
                    elif Alien.Current_Animation == 1:
                        Alien.Current_Animation = 0

                    ## moving the aliens down whenever the aliens reach a side
                    if Alien.Flag_Collide_Side != None:
                        for alien in aliens:
                            alien.Move_Down()
                            alien.Shoot()
                            alien.Check()
                    
                    ## moving the aliens regularly
                    elif Alien.Flag_Collide_Side == None:
                        for alien in aliens:
                            alien.Move_Alien()
                            alien.Shoot()
                            alien.Check()


                
                ## playing the background music of the alien movement
                    mixer.music.load(Game_Element.Basic_Sound_Url+'background sound '+str(Alien.Counter_Background_Sound)+'.wav')
                    mixer.music.play()
                    Alien.Counter_Background_Sound = Alien.Counter_Background_Sound + 1
                    if Alien.Counter_Background_Sound == 5:
                        Alien.Counter_Background_Sound = 1

        ## moving the alien bullets
            alien_bullet_Iteration_Counter = 0
            while True:
                if alien_bullet_Iteration_Counter >= len(alien_bullets):
                    break
                alien_bullets_length = len(alien_bullets)
                alien_bullets[alien_bullet_Iteration_Counter].Move_Alien_Bullet()
                alien_bullets[alien_bullet_Iteration_Counter].Check()
                if len(alien_bullets) == alien_bullets_length:
                    alien_bullet_Iteration_Counter = alien_bullet_Iteration_Counter + 1

        ## moving the player bullets
            for bullet in player_1_bullets:
                bullet.Move_Bullet()
                bullet.Check()
            for bullet in player_2_bullets:
                bullet.Move_Bullet()
                bullet.Check()

        ## updating the alien dead timer
            Alien_Explosion_Iteration_Counter = 0
            while True:
                if Alien_Explosion_Iteration_Counter == len(Alien_Explosion_List):
                    break
                Alien_Explosion_Length = len(Alien_Explosion_List)
                Alien_Explosion_List[Alien_Explosion_Iteration_Counter].Update_Timer()
                if Alien_Explosion_Length == len(Alien_Explosion_List):
                    Alien_Explosion_Iteration_Counter = Alien_Explosion_Iteration_Counter + 1
            
            Mystery_Ship_Explosion_Iteration_Counter = 0
            while True:
                if Mystery_Ship_Explosion_Iteration_Counter == len(Mystery_Ship_Explosion_List):
                    break
                Mystery_Ship_Explosion_Length = len(Mystery_Ship_Explosion_List)
                Mystery_Ship_Explosion_List[Mystery_Ship_Explosion_Iteration_Counter].Update_Timer()
                if Mystery_Ship_Explosion_Length == len(Mystery_Ship_Explosion_List):
                    Mystery_Ship_Explosion_Iteration_Counter = Mystery_Ship_Explosion_Iteration_Counter + 1
 
            ## The Key Loop
            for event in pygame.event.get():
                ## quit 
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        if player_1 != None:
                            player_1.Flag_Movement_Direction = 'right'
                        else:
                            player_2.Flag_Movement_Direction = 'right'
                    elif event.key == K_LEFT:
                        if player_1 != None:
                            player_1.Flag_Movement_Direction = 'left'
                        else:
                            player_2.Flag_Movement_Direction = 'left'
                    elif event.key == K_a:
                        if player_2 != None:
                            player_2.Flag_Movement_Direction = 'left'
                        else:
                            player_1.Flag_Movement_Direction = 'left'
                    elif event.key == K_d:
                        if player_2 != None:
                            player_2.Flag_Movement_Direction = 'right'
                        else:
                            player_1.Flag_Movement_Direction = 'right'

                ## shooting bullets using space
                    if event.key == K_SPACE:
                        if player_1 != None:
                            if player_1.Shoot_Timer <= 0 and len(player_1_bullets) == 0:
                                player_1.Shoot_Timer = 60
                                player_1.Shoot_Iteration_Counter = player_1.Shoot_Iteration_Counter + 1
                                player_1_bullets.append(Player_Bullet(player_1.xpos + 14,player_1.ypos - 10))


                                ## playing the sound
                                Player.Shoot_Sound.play()
                        else:
                            if player_2.Shoot_Timer <= 0 and len(player_2_bullets) == 0:
                                player_2.Shoot_Iteration_Counter = player_2.Shoot_Iteration_Counter + 1
                                player_2.Shoot_Timer = 60
                                player_2_bullets.append(Player_Bullet(player_2.xpos + 14,player_2.ypos - 10))

                                ## playing the sound
                                Player.Shoot_Sound.play()

                ## shooting bullets using x
                    if event.key == K_x: 
                        if player_2 != None:
                            if player_2.Shoot_Timer <= 0 and len(player_2_bullets) == 0:
                                player_2.Shoot_Timer = 60
                                player_2_bullets.append(Player_Bullet(player_2.xpos + 14,player_2.ypos - 10))

                                ## playing the sound
                                Player.Shoot_Sound.play()
                        else:
                            if player_1.Shoot_Timer <= 0 and len(player_1_bullets) == 0:
                                player_1.Shoot_Timer = 60
                                player_1_bullets.append(Player_Bullet(player_1.xpos + 14,player_1.ypos - 10))

                                ## playing the sound
                                Player.Shoot_Sound.play()


                ## checking if the keys are lifted
                if event.type == KEYUP:
                    if event.key == K_RIGHT:
                        if player_1 != None:
                            if player_1.Flag_Movement_Direction == 'right':
                                player_1.Flag_Movement_Direction = None
                        else:
                            if player_2.Flag_Movement_Direction == 'right':
                                player_2.Flag_Movement_Direction = None
                    elif event.key == K_LEFT:
                        if player_1 != None:
                            if player_1.Flag_Movement_Direction == 'left':
                                player_1.Flag_Movement_Direction = None
                        else:
                            if player_2.Flag_Movement_Direction == 'left':
                                player_2.Flag_Movement_Direction = None
                    if event.key == K_a:
                        if player_2 != None:
                            if player_2.Flag_Movement_Direction == 'left':
                                player_2.Flag_Movement_Direction = None
                        else:
                            if player_1.Flag_Movement_Direction == 'left':
                                player_1.Flag_Movement_Direction = None
                    elif event.key == K_d:
                        if player_2 != None:
                            if player_2.Flag_Movement_Direction == 'right':
                                player_2.Flag_Movement_Direction = None
                        else:
                            if player_1.Flag_Movement_Direction == 'right':
                                player_1.Flag_Movement_Direction = None

    ## drawing things 
        ## drawing the alien invasion line
            for Barrier_particle in alien_invasion_line:
                Barrier_particle.Draw()

        ## drawing the score
            score_message.Draw()
            player_1_score.Draw()
            player_2_score.Draw()
            high_score.Draw()            
            player_1_life.Draw()
            player_2_life.Draw()
            
        ## drawing the player
            if player_1 != None:
                player_1.Draw('green')
            if player_2 != None:
                player_2.Draw('blue')
            for player in player_1_backup:
                player.Draw('green')
            for player in player_2_backup:
                player.Draw('blue')
            
        ## drawing the Barriers
            for Barrier_particle in Barrier1:
                Barrier_particle.Draw()
            for Barrier_particle in Barrier2:
                Barrier_particle.Draw()
            for Barrier_particle in Barrier3:
                Barrier_particle.Draw()
            for Barrier_particle in Barrier4:
                Barrier_particle.Draw()
                
        ## drawing the Mystery_Ship
            mystery_ship.Draw()

        ## drawing the aliens
            for alien in aliens:
                if alien.ypos >= 315:
                    alien.Draw('green')
                else:
                    alien.Draw('white')

        ## drawing the Alien_Explosion and Mystery Ship Explosion
            for explosion in Alien_Explosion_List:
                explosion.Draw()
            for explosion in Mystery_Ship_Explosion_List:
                explosion.Draw()
                
        ## drawing the player bullet with the specific color
            for bullet in player_1_bullets:
                if Flag_Game_Mode == 'two_player':
                    bullet.Draw('green')
                else:
                    bullet.Draw('white')
            for bullet in player_2_bullets:
                bullet.Draw('blue')
            
        ## drawing the alien bullets;
            for bullet in alien_bullets:
                bullet.Draw()

        ## updating the player bullet timer
            if Player.Shoot_Timer > 0:
                Player.Shoot_Timer = Player.Shoot_Timer - 1
                
        ##drawing the explosion caused by the player and alien bullets
            bullet_explosion_Iteration_Counter = 0
            while True:
                if bullet_explosion_Iteration_Counter == len(Bullet_Explosion_List):
                    break
                Bullet_Explosion_List[bullet_explosion_Iteration_Counter].Draw()
                Bullet_Explosion_List[bullet_explosion_Iteration_Counter].Explosion_Timer = Bullet_Explosion_List[bullet_explosion_Iteration_Counter].Explosion_Timer - 1
                if Bullet_Explosion_List[bullet_explosion_Iteration_Counter].Explosion_Timer == 0:
                    Bullet_Explosion_List.pop(bullet_explosion_Iteration_Counter)
                else:
                    bullet_explosion_Iteration_Counter = bullet_explosion_Iteration_Counter + 1

        ## updating the windo
            pygame.display.update()
            clock.tick(60)

            ## checking if all the aliens are shot
            if len(aliens) == 0 and len(Alien_Explosion_List) == 0:
                ## emptying all the bullet lists
                alien_bullets = []
                player_1_bullets = []
                player_2_bullets = []

                ## resetting the player's xpos 
                if player_1 != None:
                    player_1.xpos = 50
                    player_1.Flag_Movement_Direction = None
                elif player_2 != None:
                    player_2.xpos = 90
                    player_2.Flag_Movement_Direction = None



                ## Refilling Aliens and Barriers
                Alien_Refill()
                Barrier_Refill()

                ## drawing the new level and preparing the screen
                Level_Draw()
                Screen_Draw()


        ## checking if the players are hit
            if player_1 != None:
                if player_1.Flag_Struck == True:
                    Player_Explode(player_1)

            if player_2 != None:
                if player_2.Flag_Struck == True:
                    Player_Explode(player_2)

        ## ending the game
            if Flag_Gameover == True:
                ## drawing the Game Over Sign
                game_over_message_list = ['G','A','M','E','O','V','E','R']
                game_over_message = Words_And_Phrases(180,120,game_over_message_list)
                game_over_message.Draw()
                pygame.display.update()
                Pause(2)
                break


## basic python setup
import random
import pygame
from pygame.locals import *
from customcolors import *
from pygame import mixer
def show_text(msg, x, y, color, size):
        fontobj= pygame.font.SysFont("freesans", size)
        msgobj = fontobj.render(msg,False,color)
        screen.blit(msgobj,(x, y))
pygame.init()
screen = pygame.display.set_mode((480,480))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()                         

## setting up the game play
def MainGame_2():

    def Close():
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            ## skipping if the enter key is pressed
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:              
                    nonlocal Flag_Skip
                    if Flag_Skip == False:
                        Flag_Skip = True

    def Pause(time):
        for counter in range(0,time*10):
            Close()
            clock.tick(10)

    def Collide(object_1,object_2):
        if object_1.xpos + object_1.length > object_2.xpos and object_2.xpos + object_2.length > object_1.xpos:
            if object_1.ypos + object_1.height > object_2.ypos and object_2.ypos + object_2.height > object_1.ypos:
                return True
            
    def Alien_Barrier_Collision(alien,Barrier):
        Barrier_Iteration_Counter = 0
        Barrier_Struck = False
        while True:
            if Barrier_Iteration_Counter == len(Barrier):
                break
            if alien.xpos + alien.length >= Barrier[Barrier_Iteration_Counter].xpos and alien.xpos <= Barrier[Barrier_Iteration_Counter].xpos + Barrier[Barrier_Iteration_Counter].length:
                if alien.ypos + alien.height >= Barrier[Barrier_Iteration_Counter].ypos:
                    Barrier_Struck = True
            if Barrier_Struck == True:
                Barrier.pop(Barrier_Iteration_Counter)
                Barrier_Struck = False
            else:
                Barrier_Iteration_Counter = Barrier_Iteration_Counter + 1

    def Bullet_Barrier_Collision(Barrier,bullet):
        ## declaring nonlocals to the bullet lists and the bullet explosion list
        nonlocal player_1_bullets, player_2_bullets, alien_bullets, Bullet_Explosion_List
    
        ## checking what type of bullet it is and what iteration should be performed ont he Barrier
        if bullet in alien_bullets:
            Barrier_Iteration = [0,len(Barrier),1]
            
        elif bullet in player_1_bullets or bullet in player_2_bullets:
            Barrier_Iteration = [len(Barrier) - 1,-1,-1]
         
        ## checking the Barrier and if the divisor is supposed to be 2
        if Barrier == alien_invasion_line:
            divisor = 2
        else:
            divisor = 1

        Target_Barrier = None
        ## checking the specific particle the bullet hits
        for i in range(Barrier_Iteration[0],Barrier_Iteration[1],Barrier_Iteration[2]):
            if Collide(bullet,Barrier[i]) == True:
                Target_Barrier = Barrier[i]
                Barrier_Iteration_Counter = 0
                Barrier_Struck = False
                while True:
                    # breaking the bullet and the while loop
                    if Barrier_Iteration_Counter >= len(Barrier):
                        if bullet in alien_bullets:
                            alien_bullets.remove(bullet)
                        if bullet in player_1_bullets:
                            player_1_bullets.remove(bullet)
                        if bullet in player_2_bullets:
                            player_2_bullets.remove(bullet)
                        break
                
                    ## checking if the xpos is correct
                    if Barrier[Barrier_Iteration_Counter].xpos%(divisor*2) == 0:
                        ## checking if the Barrier particle is in close range of the area hit by the bullet
                        if Target_Barrier.xpos - bullet.Dr[0]*2 < Barrier[Barrier_Iteration_Counter].xpos < Target_Barrier.xpos + Target_Barrier.length + bullet.Dr[0]:
                            if Target_Barrier.ypos - bullet.Dr[1]*2 < Barrier[Barrier_Iteration_Counter].ypos < Target_Barrier.ypos + Target_Barrier.height + bullet.Dr[1]*2:
                                Barrier_Struck = True
                            
                        ## checking if the Barrier particle is in far range of the area struck by the bullet
                        if Target_Barrier.xpos - bullet.Dr[2]*2 < Barrier[Barrier_Iteration_Counter].xpos < Target_Barrier.xpos + Target_Barrier.height + bullet.Dr[2]*2:
                            if Target_Barrier.ypos - bullet.Dr[3]*2 < Barrier[Barrier_Iteration_Counter].ypos < Target_Barrier.ypos + Target_Barrier.height + bullet.Dr[3]*2:
                                # deciding how far it is and the chance of the Barrier being destroyed
                                y_distance = abs(Target_Barrier.ypos - Barrier[Barrier_Iteration_Counter].ypos) + 1
                                x_distance = abs(Target_Barrier.xpos - Barrier[Barrier_Iteration_Counter].xpos) + 1
                                x_range = x_distance//(bullet.Dr[2])
                                y_range = y_distance//(bullet.Dr[3])
                                if random.randint(0,x_range) == 0 and random.randint(0,y_range) == 0:
                                    Barrier_Struck = True

                    ## destroying the Barrier partlce
                    if Barrier_Struck == True:
                        Barrier.pop(Barrier_Iteration_Counter)
                        Barrier_Struck = False
                    else:
                        Barrier_Iteration_Counter = Barrier_Iteration_Counter + 1
                break
            
    def Update_Score(score):            
        if score.phrase[2] >= 10:
            score.phrase[1] = score.phrase[1] + 1
            score.phrase[2] = score.phrase[2] - 10
        if score.phrase[1] >= 10:
            score.phrase[0] = score.phrase[0] + 1
            score.phrase[1] = score.phrase[1] - 10
        if score.phrase[0] >= 10:
            score.phrase[0] = score.phrase[0] - 10
        
    def Player_Explode(player):
        ## nonlocal declaration to variables and lists
        nonlocal alien_bullets, player_1_bullets, player_2_bullets
        nonlocal player_1, player_2, player_1_life, player_2_life
        nonlocal Flag_Gameover
 
        ## playing the sound
        Player_Explosion.Sound.play()                

        ## uploading the player_explosion images
        player_explosion = Player_Explosion(player.xpos,player.ypos,40,20)

        ## drawing the player_explosion
        for iteration in range(1,20):
            for animation in range(1,3):
                player_explosion.Draw(animation)
                Close()
                pygame.display.update()
                clock.tick(15)
                
        ## emptying the player explosion from the screen by drawing a black rectangle
        player_explosion.Draw(3)
        
        ## drawing the player afterwards
        if player == player_1:
            if player_2 != None:
                player_2.Draw('blue')
                player_2.Flag_Movement_Direction = None
        elif player == player_2:
            if player_1 != None:
                player_1.Draw('green')
                player_1.Flag_Movement_Direction = None
        
        pygame.display.update()
        Pause(2)


        if player == player_1:
            if len(player_1_backup) != 0:

                ## resetting the player's attributes
                player_1.Flag_Movement_Direction = None
                player_1.Flag_Struck = False
                player_1.ypos = 400
                player_1.xpos = 50

                ## changing the player's lives
                player_1_backup.pop(-1)
                player_1_life.phrase[0] = player_1_life.phrase[0] - 1

            elif len(player_1_backup) == 0:

                ## removing the player from the game
                player_1 = None


        elif player == player_2:
            if len(player_2_backup) != 0:

                ## resetting the player's attributes
                player_2.Flag_Movement_Direction = None
                player_2.Flag_Struck = False
                player_2.ypos = 400
                player_2.xpos = 90
                
                ## changing the player's lives
                player_2_backup.pop(-1)
                player_2_life.phrase[0] = player_2_life.phrase[0] - 1

            elif len(player_2_backup) == 0:

                ## removing the player from the game
                player_2 = None

        ## checking if the game ends
        if player_1 == None and player_2 == None:
            Flag_Gameover = True

    def Alien_Refill(Start_Game=False):

        ## nonlocal declaration to the lists and variables
        nonlocal aliens
        
        ## resetting all the alien attributes
        Alien.Timer = 2
        Alien.Animation = 0
        Alien.Flag_Collide_Side = None
        Alien.Flag_Down_Step = None
        Alien.Speed = 5

        ## resetting the alien movement iteration and sounds
        Alien.Counter_Movement  = 0
        Alien.Counter_Background_Sound = 1 
        if Start_Game == True:
            Alien.Counter_Position = 0

        ## filling the aliens
        for row in range(len(Alien.layout) - 1,-1,-1):
            for group in range(len(Alien.layout[row]) - 1,-1,-1):
                alien_group = []
                for alien in range(len(Alien.layout[row][group]),0,-1):
                    ## checking the x-value to place the alien because the lists are uneven
                    if len(Alien.layout[row][group]) == 1:
                        xpos = 60
                    else:
                        xpos = alien*30

                    ## adding the aliens to the group list
                    if row == 4 or row == 3:
                        alien_group.append(Alien(group*60 + xpos + 20,row*30 + 120 + 6*Alien.Counter_Position,2))
                    elif row == 2 or row == 1:
                        alien_group.append(Alien(group*60 + xpos + 20,row*30 + 120 + 6*Alien.Counter_Position,1))
                    else:
                        alien_group.append(Alien(group*60 + xpos + 20,row*30 + 120 + 6*Alien.Counter_Position,3))

                ## adding the group list to the alien list
                aliens.append(alien_group)

    def Barrier_Refill():
        ## globalizing the Barrier lists
        nonlocal Barrier1,Barrier2,Barrier3,Barrier4,alien_invasion_line

        ## filling the Barrier lists
        for row in range(0,len(Barrier_layout)):
            for column in range(len(Barrier_layout[row])):
                if Barrier_layout[row][column] == 1:
                    Barrier1.append(Barrier(column*2 + 48,row*2 + 330))
                    Barrier2.append(Barrier(column*2 + 156,row*2 + 330))
                    Barrier3.append(Barrier(column*2 + 264,row*2 + 330))
                    Barrier4.append(Barrier(column*2 + 372,row*2 + 330))
        
        ## filling the alien invasion line
        for row in range(0,1):
            for column in range(0,480):
                alien_invasion_line.append(Barrier(column*2,row*2 + 435))

    def Fill_Black():
        for xpos in range(0,480,120):
            pygame.draw.rect(screen,black,(xpos,0,120,480))
            Close()
            pygame.display.update()
            clock.tick(20)
        nonlocal Flag_Skip
        Flag_Skip  = 'stage_2'

    def Screen_Draw():      
        screen.fill(black)

        ## drawing the score
        score_message.Draw()
        player_1_score.Draw()
        player_2_score.Draw()
        high_score.Draw()
        player_1_life.Draw()
        player_2_life.Draw()

        ## drawing the floor
        for Barrier_particle in alien_invasion_line:
            Barrier_particle.Draw()

        ## drawing the Barrier
        for Barrier_particle in Barrier1:
            Barrier_particle.Draw()
        for Barrier_particle in Barrier2:
            Barrier_particle.Draw()
        for Barrier_particle in Barrier3:
            Barrier_particle.Draw()
        for Barrier_particle in Barrier4:
            Barrier_particle.Draw()
        

        ## drawing the players 
        player_1.Draw('green')
        if player_2 != None:
            player_2.Draw('blue')
        for player in player_1_backup:
            player.Draw('green')
        for player in player_2_backup:
            player.Draw('blue')
        
        ## drawing the aliens and closing the screen if the quit button is pressed
        for group in aliens:
            for alien in group:
                alien.Draw('white')
                Close()
                pygame.display.update()
                clock.tick(60)

    ## main class
    class Game_Element:
        Basic_Sound_Url = 'Sounds\\'
        Basic_Url = 'Images\\'
        def __init__(self,xpos,ypos):
            self.xpos = xpos
            self.ypos = ypos

    class Words_And_Phrases(Game_Element):
        ## uploading all the character names
        Character_Dictionary = {}
        Character_Name_List = ['A','B','C','D','E','E','F','G','H','I','J','K','L','M','N',
                                'O','P','Q','R','S','T','U','V','W','X','Y','Z','SPACE',0,1,2,
                                 3,4,5,6,7,8,9,'left','right','equal','asterisk','question_mark','dash','space','yflip']
        
        ## uploading all the character
        Character_Image_List = []
        for character_name in Character_Name_List:
            Character_Image_List.append(pygame.image.load(Game_Element.Basic_Url+'letters\\'+str(character_name)+'.jpeg'))
     
        ## storing the resized character images into a dictionary with the value of the respective character name 
        for index in range(len(Character_Name_List)):
            character_image = Character_Image_List[index]
            resized_character_image = pygame.transform.scale(character_image,(10,14))
            Character_Dictionary[Character_Name_List[index]] = resized_character_image
            
        def __init__(self,xpos,ypos,phrase):
            super().__init__(xpos,ypos)
            self.phrase = phrase
        def Draw(self,delay=0):
            Counter_Spacing = 0
            for character in self.phrase:

                ## checking if it is to be skipped
                if Player_Selected == True:
                    if Flag_Skip == True or Flag_Skip == 'stage_2':
                        if Flag_Skip == True:
                            Fill_Black()
                        break

                ## drawing the letter
                screen.blit(Words_And_Phrases.Character_Dictionary[character],(self.xpos + Counter_Spacing,self.ypos))
                Counter_Spacing = Counter_Spacing + 15

                ## pausing if there is a delay
                if delay != 0:
                    Close()
                    pygame.display.update()
                    clock.tick(delay)

    class Alien(Game_Element):                                                                                                                                                                                 
        ## movement
        Speed = 5
        Timer = 2
        Flag_Collide_Side = None
        Flag_Down_Step = False
        
        ## counters
        Counter_Position = 0
        Counter_Movement = 0
        Counter_Background_Sound = 1

        ## animation
        Current_Animation = 0

        ## layout    
        layout = [[[0],[0,0],[0,0],[0,0],[0,0],[0,0]],
                  [[0],[0,0],[0,0],[0,0],[0,0],[0,0]],
                  [[0],[0,0],[0,0],[0,0],[0,0],[0,0]],
                  [[0],[0,0],[0,0],[0,0],[0,0],[0,0]],
                  [[0],[0,0],[0,0],[0,0],[0,0],[0,0]]]
        
        ## setting up the letter interaction images from the start screen
        Letter_Flip_Image_List = []

        for image_number in range(1,5):
            img = pygame.image.load(Game_Element.Basic_Url+'Alien Letter Flip\Interaction '+str(image_number)+'.jpeg')
            Letter_Flip_Image_List.append(pygame.transform.scale(img,(32,15)))
        
        ## setting up the alien images
        Image_List = []

        for color in ['White','Green']:
            color_list = []
            for type in range(1,4):
                animation_list = []
                ## deciding the width of the aliens
                if type == 3:
                    length = 15
                else:
                    length = 20
                ## uploading all the images
                for animation in range(1,3):
                    img = pygame.image.load(Game_Element.Basic_Url+'Alien\\'+str(color)+' '+str(type)+' '+str(animation)+'.jpeg')
                    ## storing the images in lists
                    animation_list.append(pygame.transform.scale(img,(length,15)))
                color_list.append(animation_list)
            Image_List.append(color_list)

        def __init__(self,xpos,ypos,type):
            super().__init__(xpos,ypos)
            self.type = type
            if self.type == 3:
                self.length = 15
                self.height = 15
            else:
                self.length = 20
                self.height = 15

        def Move_Alien(self):
            self.xpos = self.xpos + self.Speed
            if self.Current_Animation == 0:
                self.Current_Animation = 1
            elif self.Current_Animation == 1:
                self.Current_Animation = 0

        def Move_Down(self):
            self.ypos = self.ypos + (15 - (Alien.Counter_Position/2))
            if Alien.Flag_Collide_Side == 'left':
                Alien.Speed = 5
            elif Alien.Flag_Collide_Side == 'right':
                Alien.Speed = -5

        def Check(self):
            ## checking if the alien hits the edge
            if self.xpos + self.length >= 440:
                Alien.Flag_Collide_Side = 'right'
            elif self.xpos <= 35:
                Alien.Flag_Collide_Side = 'left'

            ## checking if the aliens reach the Barrier
            if self.ypos + self.height > 330 and self.ypos < 370:
                if self.xpos + self.length > 48 and self.xpos < 108:
                    Alien_Barrier_Collision(self,Barrier1)
                elif self.xpos + self.length > 156 and self.xpos < 216:
                    Alien_Barrier_Collision(self,Barrier2)
                elif self.xpos + self.length > 264 and self.xpos < 324:
                    Alien_Barrier_Collision(self,Barrier3)
                elif self.xpos + self.length > 372 and self.xpos < 432:
                    Alien_Barrier_Collision(self,Barrier4)

            # checking if the aliens hit the invasion line or invade
            if self.ypos + self.height == 435:
                nonlocal Flag_Gameover
                Flag_Gameover = True

        def Shoot(self):
            ## aliens shooting a bullet
            if random.randint(1,100) == 1:
                alien_bullets.append(Alien_Bullet(self.xpos,self.ypos))

        def Draw(self,color='white'):
            if color == 'white':
                return screen.blit(Alien.Image_List[0][self.type - 1][self.Current_Animation],(self.xpos,self.ypos))
            elif color == 'green':
                return screen.blit(Alien.Image_List[1][self.type - 1][self.Current_Animation],(self.xpos,self.ypos))
            elif color == 'red':
                return screen.blit(Alien.Image_List[2][self.type - 1][self.Current_Animation],(self.xpos,self.ypos))

        def Draw_Letter_Take(self):
            return screen.blit(Alien.Letter_Flip_Image_List[self.Current_Animation],(self.xpos - 8,self.ypos))
        def Draw_Letter_Place(self):
            return screen.blit(Alien.Letter_Flip_Image_List[self.Current_Animation + 2],(self.xpos - 8,self.ypos))

    class Player(Game_Element):
        ## setting up the shoot sound
        Shoot_Sound = mixer.Sound(Game_Element.Basic_Sound_Url+'player shoot sound.wav')

        ## setting up the flag variables
        Flag_Struck = False
        Flag_Movement_Direction = None

        ## setting up the counter variables
        Shoot_Iteration_Counter = 0
        Lucky_Shot = False
        
        ## setting up the player's image
        Img = pygame.image.load(Game_Element.Basic_Url+'Player\\player green.jpeg')
        Green_Image = pygame.transform.scale(Img,(30,20))

        Img = pygame.image.load(Game_Element.Basic_Url+'Player\\player blue.jpeg')
        Blue_Image = pygame.transform.scale(Img,(30,20))

        ## setting up the shoot timer
        Shoot_Timer = 0

        def __init__(self,xpos,ypos):
            super().__init__(xpos,ypos)
            self.length = 30
            self.height = 20

        def Move_Player(self):
            ## updating the shoot timer
            if self.Shoot_Timer > 0:
                self.Shoot_Timer = self.Shoot_Timer - 1
            
            if self.Flag_Movement_Direction == 'left':
                self.xpos = self.xpos - 3
            elif self.Flag_Movement_Direction == 'right':
                self.xpos = self.xpos + 3
            if self.xpos > 410:
                self.xpos = 410
            elif self.xpos < 35:
                self.xpos = 35
        
        def Draw(self,color='green'):
            if color == 'green':
                return screen.blit(Player.Green_Image,(self.xpos,self.ypos))
            elif color == 'blue':
                return screen.blit(Player.Blue_Image,(self.xpos,self.ypos))

    class Mystery_Ship(Game_Element):
        ## adding the images
        Img = pygame.image.load(Game_Element.Basic_Url+'Mystery Ship\Mystery Ship Red.jpeg')
        Image = pygame.transform.scale(Img,(32,14))
        
        ## adding the sounds
        Low_Sound = mixer.Sound(Game_Element.Basic_Sound_Url+'mystery ship low sound.wav')
        Sound_Iteration_Counter = 10

        def __init__(self,xpos,ypos):
            super().__init__(xpos,ypos)
            self.length = 32
            self.height = 14

        def Move_Mystery_Ship(self):
            ## moving the mystery ship
            self.xpos = self.xpos - 2
            ## checking if it should be replaced and the sound counter is also fixed
            if self.xpos + self.length < 0:
                self.xpos = 2500
                self.Sound_Iteration_Counter = 10

        def Draw(self):
            return screen.blit(Mystery_Ship.Image,(self.xpos,self.ypos))
            
        def Play_Sound(self):
            ## playing it's sound
            if self.xpos < 480:
                if self.Sound_Iteration_Counter >= 10:
                    self.Low_Sound.play()
                    self.Sound_Iteration_Counter = 0
                self.Sound_Iteration_Counter = self.Sound_Iteration_Counter + 1
                
    class Player_Bullet(Game_Element):
        ## uploading images
        img = pygame.image.load(Game_Element.Basic_Url+'Player Bullet\player bullet white.jpeg')
        White_Image = pygame.transform.scale(img,(2,16))
        img = pygame.image.load(Game_Element.Basic_Url+'Player Bullet\player bullet blue.jpeg')
        Blue_Image = pygame.transform.scale(img,(2,16))
        img = pygame.image.load(Game_Element.Basic_Url+'Player Bullet\player bullet green.jpeg')
        Green_Image = pygame.transform.scale(img,(2,16))

        ## setting up the destruction ranges
        Dr = [2,5,4,7]

        def __init__(self,xpos,ypos):
            super().__init__(xpos,ypos)
            self.height = 16
            self.length = 2 

        def Move_Bullet(self):
            self.ypos = self.ypos - 5

        def Check(self):
            ## declaring nonlocals to the bullets and scores
            nonlocal player_1_bullets, player_2_bullets
            nonlocal player_1_score, player_2_score

            ## checking if the player_1_bullets hit the Barriers
            if self.ypos + self.height > 330 and self.ypos < 370:
                if self.xpos + self.length > 48 and self.xpos < 108:
                    Bullet_Barrier_Collision(Barrier1,self)
                elif self.xpos + self.length > 156 and self.xpos < 216:
                    Bullet_Barrier_Collision(Barrier2,self)
                elif self.xpos + self.length > 264 and self.xpos < 324:
                    Bullet_Barrier_Collision(Barrier3,self)
                elif self.xpos + self.length > 372 and self.xpos < 432:
                    Bullet_Barrier_Collision(Barrier4,self)

            ## checking if the bullets hit the alien
            if self in player_1_bullets or self in player_2_bullets:
                for group in aliens:
                    for alien in group:
                        if Collide(alien,self) == True:
                            group.remove(alien)
                            ## checking how much should be added to the scores based on the alien type
                            increment = 0
                            if alien.type == 2:
                                increment = 1
                            elif alien.type == 1:
                                increment = 2
                            elif alien.type == 3:
                                increment = 3

                            ## updating the player scores
                            if self in player_1_bullets:
                                player_1_score.phrase[2] = player_1_score.phrase[2] + increment
                                player_1_bullets.remove(self)
                            elif self in player_2_bullets:
                                player_2_score.phrase[2] = player_2_score.phrase[2] + increment
                                player_2_bullets.remove(self)

                            ## updating the high score
                            high_score.phrase[2] = high_score.phrase[2] + increment

                            ## checking if the counter alien movement variable should be changed
                            if len(group) == 0:
                                if Alien.Counter_Movement > aliens.index(group):
                                    Alien.Counter_Movement = Alien.Counter_Movement - 1
                                aliens.remove(group)
                                
                            ## adding the explosion to the explosion list
                            Alien_Explosion_List.append(Alien_Explosion(alien.xpos,alien.ypos))

                            ## playing the explosion sound
                            Alien_Explosion.Sound.play()
                            break 

                    if self not in player_1_bullets and self not in player_2_bullets:
                        break

            ## checking if the bullet hits the mystery ship
            if self in player_1_bullets:
                if Collide(self,mystery_ship) == True:

                    ## checking if the player 1 bullets hits the mystery ship at the 15th shot and making it worth 300 points
                        if player_1.Lucky_Shot == True:
                            if (player_1.Shoot_Iteration_Counter - 23)%15 == 0:
                                Mystery_Ship_Explosion_List.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,300))
                                player_1_score.phrase[1] = player_1_score.phrase[1] + 3
                                high_score.phrase[1] = high_score.phrase[1] + 3
                            else:
                                player_1.Lucky_Shot = False

                    ## checking if otherwise and making it worth 200 points
                        if player_1.Lucky_Shot == False:
                            Mystery_Ship_Explosion_List.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,200))
                            player_1_score.phrase[1] = player_1_score.phrase[1] + 2
                            high_score.phrase[1] = high_score.phrase[1] + 2

                    ## checking if the player 1 bullet hits the mystery ship on the 23rd shot 
                        if player_1.Shoot_Iteration_Counter == 23:
                            player_1.Lucky_Shot = True

                    ## relocating the mystery ship
                        mystery_ship.xpos = 2500

                    ## removing the bullet from the bullet list
                        player_1_bullets.remove(self)

                    ## playing the mystery ship's explosion sound
                        Mystery_Ship_Explosion.Sound.play()

            elif self in player_2_bullets:
                if Collide(self,mystery_ship) == True:

                    ## checking if the player 2's bullets hits the mystery ship at the 15th shot and making it worth 300 points
                        if player_2.Lucky_Shot == True:
                            if (player_2.Shoot_Iteration_Counter - 23)%15 == 0:
                                Mystery_Ship_Explosion_List.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,300))
                                player_2_score.phrase[1] = player_1_score.phrase[1] + 3
                                high_score.phrase[1] = high_score.phrase[1] + 3
                            else:
                                player_2.Lucky_Shot = False

                    ## checking if otherwise and making it worth 200 points
                        if player_2.Lucky_Shot == False:
                            Mystery_Ship_Explosion_List.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,200))
                            player_2_score.phrase[1] = player_2_score.phrase[1] + 2
                            high_score.phrase[1] = high_score.phrase[1] + 2
                            
                    ## checking if the player 2's bullet hits the mystery ship on the 23rd shot
                        if player_2.Shoot_Iteration_Counter == 23:
                            player_2.Lucky_Shot = True

                    ## relocating the mystery ship
                        mystery_ship.xpos = 2500

                    ## removing the bullet from the bullet list
                        player_2_bullets.remove(self)

                    ## playing the mystery ship's explosion sound
                        Mystery_Ship_Explosion.Sound.play()
   
            ## checking if the hundreads or thousands place in the scores should be updated
            Update_Score(player_1_score)
            Update_Score(player_2_score)
            Update_Score(high_score)

            ## checking if the player bullet hits the top of the screen
            if self in player_1_bullets or self in player_2_bullets:
                if self.ypos < 0:
                    if self in player_1_bullets:
                        player_1_bullets.remove(self)
                    elif self in player_2_bullets:
                        player_2_bullets.remove(self)
                    Bullet_Explosion_List.append(Bullet_Explosion(self.xpos - 6,self.ypos))

        def Draw(self,color='white'):
            if color == 'white':
                return screen.blit(Player_Bullet.White_Image,(self.xpos,self.ypos))
            elif color == 'blue':
                return screen.blit(Player_Bullet.Blue_Image,(self.xpos,self.ypos))
            elif color == 'green':
                return screen.blit(Player_Bullet.Green_Image,(self.xpos,self.ypos))

    class Alien_Bullet(Game_Element):
        ## class variables
        Current_Animation = 1
        
        layout_1 = [[2,2,2,2,2,6],
                    [2,2,2,6,2,2],
                    [2,2,6,2,2,2],
                    [6,2,2,2,2,2]]
        layout_2 = [[2,2,4,5,2,4,5],
                    [2,2,4,5,2,4,5],
                    [5,4,2,5,4,2,2],
                    [5,4,2,5,4,2,2]]
        layout_3 = [[2,1,2,3,2,1,2],
                    [1,2,3,2,1,2,3],
                    [2,3,2,1,2,3,2],
                    [3,2,1,2,3,2,1]]
        
        ## uploading all the alien bullet images
        Image_List = []
        for color in ['White','Green']:
            color_list = []
            for image_particle in range(1,7):
                img = pygame.image.load(Game_Element.Basic_Url+'Alien Bullet\\alien bullet '+str(image_particle)+' '+str(color)+'.jpeg')
                img = pygame.transform.scale(img,(6,2))
                color_list.append(img)   
            Image_List.append(color_list)

        def __init__(self,xpos,ypos):
            ## setting up the cordinates and the type 
            self.xpos = xpos
            self.ypos = ypos
            self.type = random.randint(1,3)

            ## setting up the attributes such as the varying lengths, heights, the Barrier destruction range
            if self.type == 1:
                self.length = 6
                self.height = 12
                self.Dr = [2,5,4,7]
            elif self.type == 2:
                self.length = 6
                self.height = 14
                self.Dr = [2,5,4,8]
            elif self.type == 3:
                self.length = 6
                self.height = 14
                self.Dr = [3,5,5,7]
      
        def Move_Alien_Bullet(self):
                ## updating the animation
                self.Current_Animation = self.Current_Animation + 1
                if self.Current_Animation == 4:
                    self.Current_Animation = 0
                ## updating the y cordinates
                self.ypos = self.ypos + 3

        def Check(self):
            nonlocal alien_bullets, Bullet_Explosion_List
            alien_bullets_length = len(alien_bullets)
            ## checking if the alien_bullets hit the Barriers
            if self.ypos + self.height > 330 and self.ypos < 370:
                if self.xpos + self.length > 48 and self.xpos < 108:
                    Bullet_Barrier_Collision(Barrier1,self)
                elif self.xpos + self.length > 156 and self.xpos < 216:
                    Bullet_Barrier_Collision(Barrier2,self)
                elif self.xpos + self.length > 264 and self.xpos < 324:
                    Bullet_Barrier_Collision(Barrier3,self)
                elif self.xpos + self.length > 372 and self.xpos < 432:
                    Bullet_Barrier_Collision(Barrier4,self)

            ## checking if the alien_bullets hits the boundary line
            if self.ypos + self.height > 435 and len(alien_bullets) == alien_bullets_length:
                Bullet_Barrier_Collision(alien_invasion_line,self)
                if self in alien_bullets:
                    alien_bullets.remove(self)
                Bullet_Explosion_List.append(Bullet_Explosion(self.xpos - 3,self.ypos - 4,))

            ## checking if the alien_bullet hit the player bullet
            if len(alien_bullets) == alien_bullets_length:
                for bullet in player_1_bullets:
                    if self.xpos + self.length > bullet.xpos and bullet.xpos + bullet.length > self.xpos and self.ypos + self.height > bullet.ypos and bullet.ypos + bullet.height > self.ypos:
                        player_1_bullets.remove(bullet)
                        Bullet_Explosion_List.append(Bullet_Explosion(bullet.xpos - 6,bullet.ypos - 8))
                        if self.type == 1:
                            if random.randint(1,2) == 1:
                                alien_bullets.remove(self)
                        elif self.type == 2:
                            if random.randint(1,3) == 1:
                                alien_bullets.remove(self)
                        break

            if len(alien_bullets) == alien_bullets_length:
                for bullet in player_2_bullets:
                    if Collide(self,bullet) == True:
                        player_2_bullets.remove(bullet)
                        Bullet_Explosion_List.append(Bullet_Explosion(bullet.xpos - 6,bullet.ypos - 8))
                        if self.type == 1:
                            if random.randint(1,2) == 1:
                                alien_bullets.remove(self)
                        elif self.type == 2:
                            if random.randint(1,3) == 1:
                                alien_bullets.remove(self)
                        break

            # ## checking if the alien bullet hits the player
            if len(alien_bullets) == alien_bullets_length:
                if player_1 != None:
                    if Collide(self,player_1) == True:
                        alien_bullets.remove(self)
                        player_1.Flag_Struck = True

            if len(alien_bullets) == alien_bullets_length:
                if player_2 != None:
                    if Collide(self,player_2) == True:
                        alien_bullets.remove(self)
                        player_2.Flag_Struck = True

        def Draw(self):
            ## drawing the alien bullet
            counter_xpos = 0
            ## checking what type it is and drawing the right images
            if self.type == 1:
                for image_particle in Alien_Bullet.layout_1[self.Current_Animation]:
                    if self.ypos + 2 > 330:
                        screen.blit(Alien_Bullet.Image_List[1][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                    else:
                        screen.blit(Alien_Bullet.Image_List[0][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                    counter_xpos = counter_xpos + 2
            if self.type == 2:
                for image_particle in Alien_Bullet.layout_2[self.Current_Animation]:
                    if self.ypos + 2 > 330:
                        screen.blit(Alien_Bullet.Image_List[1][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                    else:
                        screen.blit(Alien_Bullet.Image_List[0][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                    counter_xpos = counter_xpos + 2
            if self.type == 3:
                for image_particle in Alien_Bullet.layout_3[self.Current_Animation]:
                    if self.ypos + 2 > 330:
                        screen.blit(Alien_Bullet.Image_List[1][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                    else:
                        screen.blit(Alien_Bullet.Image_List[0][image_particle- 1],(self.xpos,self.ypos + counter_xpos))
                    counter_xpos = counter_xpos + 2

    class Barrier(Game_Element):
        ## setting up the images according to this
        img = pygame.image.load(Game_Element.Basic_Url+'Barrier\\barrier particle.jpeg')
        green_image = pygame.transform.scale(img,(2,2))
        def __init__(self,xpos,ypos):
            super().__init__(xpos,ypos)
            self.length = 2
            self.height = 2
        def Draw(self):
            return screen.blit(Barrier.green_image,(self.xpos,self.ypos))

    ## setting up the scinario classes
    class Alien_Explosion(Game_Element):
        ## setting up the image
        Img = pygame.image.load(Game_Element.Basic_Url+'Alien Explosion\\alien explosion white.jpeg')
        White_Image = pygame.transform.scale(Img,(20,13))
        Img = pygame.image.load(Game_Element.Basic_Url+'Alien Explosion\\alien explosion green.jpeg')
        Green_Image = pygame.transform.scale(Img,(20,13))

        ## setting up the Existing_Timer
        Existing_Timer = 10

        ## setting up the sound
        Sound = mixer.Sound(Game_Element.Basic_Sound_Url+'alien shot sound.wav')
        def Update_Timer(self):
            self.Existing_Timer = self.Existing_Timer - 1
            if self.Existing_Timer == 0:
                nonlocal Alien_Explosion_List
                Alien_Explosion_List.remove(self)
        def Draw(self):
            if self.ypos + 13 > 330:
                screen.blit(Alien_Explosion.Green_Image,(self.xpos,self.ypos))
            else: 
                screen.blit(Alien_Explosion.White_Image,(self.xpos,self.ypos))

    class Mystery_Ship_Explosion(Alien_Explosion):

        ## uploading the images
        Img = pygame.image.load(Game_Element.Basic_Url+'Mystery Ship Explosion\\mystery ship explosion red.jpeg')
        Explosion_Image = pygame.transform.scale(Img,(42,16))
        Img = pygame.image.load(Game_Element.Basic_Url+'Mystery Ship Explosion\\mystery ship score 200 red.jpeg')
        Score_200_Image = pygame.transform.scale(Img,(40,14)) 
        Img = pygame.image.load(Game_Element.Basic_Url+'Mystery Ship Explosion\\mystery ship score 200 red.jpeg')
        Score_300_Image = pygame.transform.scale(Img,(40,14)) 

        ## setting up the existing timer
        Existing_Timer = 20

        ## setting up the sound
        Sound = mixer.Sound(Game_Element.Basic_Sound_Url+'mystery ship high sound.wav')

        def __init__(self,xpos,ypos,points=200):
            super().__init__(xpos,ypos)
            self.points = points

        def Update_Timer(self):
            self.Existing_Timer = self.Existing_Timer - 1
            if self.Existing_Timer == 0:
                nonlocal Mystery_Ship_Explosion_List
                Mystery_Ship_Explosion_List.remove(self)

        def Draw(self):
            if self.Existing_Timer > 10:
                screen.blit(Mystery_Ship_Explosion.Explosion_Image,(self.xpos - 4,self.ypos))
            else:
                if self.points == 300:
                    screen.blit(Mystery_Ship_Explosion.Score_300_Image,(self.xpos - 4,self.ypos))
                else:
                    screen.blit(Mystery_Ship_Explosion.Score_200_Image,(self.xpos - 4,self.ypos))

    class Bullet_Explosion(Game_Element):
        Img = pygame.image.load(Game_Element.Basic_Url+'Bullet Explosions\\bullet and bullet explosion.jpeg')
        Image = pygame.transform.scale(Img,(12,16))
        Explosion_Timer = 4
        def Draw(self):
            return screen.blit(Bullet_Explosion.Image,(self.xpos,self.ypos))

    class Player_Explosion(Game_Element):
        ## uploading the sound
        Sound = mixer.Sound(Game_Element.Basic_Sound_Url+'player explosion sound.wav')
        ## uploading the player explosion images
        Image_List = []
        for image_number in range(1,4):
            img = pygame.image.load(Game_Element.Basic_Url+'Player Explosion\player explosion '+str(image_number)+'.jpeg')
            Image_List.append(pygame.transform.scale(img,(40,20)))
        def __init__(self,xpos,ypos,length,height):
            super().__init__(xpos,ypos)
            self.length = length
            self.height = height
        def Draw(self,image_number):
            if image_number == 1:
                screen.blit(Player_Explosion.Image_List[0],(self.xpos,self.ypos))
            elif image_number == 2:
                screen.blit(Player_Explosion.Image_List[1],(self.xpos,self.ypos))
            elif image_number == 3:
                screen.blit(Player_Explosion.Image_List[2],(self.xpos,self.ypos))
    
    ## The Game Loop
    while True:
    ## setting up the menu 1
        ## setting up the words and messages
        please_select_message_list = ['P','L','E','A','S','E','space','S','E','L','E','C','T']
        please_select_message = Words_And_Phrases(140,100,please_select_message_list)

        one_or_two_players_message_list = [1,'space','O','R','space',2,'space','P','L','A','Y','E','R','S']
        one_or_two_players_message = Words_And_Phrases(135,140,one_or_two_players_message_list)

        one_player_message_list = [1,'P','L','A','Y','E','R']
        one_player_message = Words_And_Phrases(190,180,one_player_message_list)

        two_player_message_list = [2,'P','L','A','Y','E','R']
        two_player_message = Words_And_Phrases(190,220,two_player_message_list)

        ## setting up the select asterisk
        asterisk_list = ['asterisk']
        asterisk = Words_And_Phrases(170,180,asterisk_list)

        ## setting up the flag variable to begin the game
        Player_Selected = False

        ## setting up the mode variable
        Flag_Game_Mode = 'one_player'
        
        while True:
            screen.fill(black)

            ## drawing the phrases
            please_select_message.Draw()
            one_or_two_players_message.Draw()
            one_player_message.Draw()
            two_player_message.Draw()
            asterisk.Draw()

            ## basic key functions
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        asterisk = Words_And_Phrases(170,220,asterisk_list)
                        Flag_Game_Mode = 'two_player'
                    elif event.key == K_UP:
                        asterisk = Words_And_Phrases(170,180,asterisk_list)
                        Flag_Game_Mode = 'one_player'
                    elif event.key == K_RETURN:
                        Player_Selected = True
            pygame.display.update()
            clock.tick(60)
            if Player_Selected == True:
                break


        ## setting up the player's score and the high score
        score_message_list = ['S','C','O','R','E','left',1,'right','space','H','I','dash','S','C','O','R','E','space','S','C','O','R','E','left',2,'right']
        score_message = Words_And_Phrases(45,20,score_message_list)
        player_1_score = Words_And_Phrases(60,60,[0,0,0,0])
        player_2_score = Words_And_Phrases(320,60,[0,0,0,0])
        high_score = Words_And_Phrases(200,60,[0,0,0,0])

## setting up the menu 2

        ## skip flag variable
        Flag_Skip = False

        ## emptying the screen
        screen.fill(black)
        
        # drawing the player's score and high score

        score_message.Draw()
        player_1_score.Draw()
        player_2_score.Draw()
        high_score.Draw()

        # setting up and drawing the words and messages
        play_message_list = ['P','L','A']
        play_message = Words_And_Phrases(210,150,play_message_list)
        play_message.Draw(10)

        y_message = Words_And_Phrases(255,150,['yflip'])
        y_message.Draw(10)

        Space_Invaders_message_list = ['S','P','A','C','E','space','I','N','V','A','D','E','R','S']
        Space_Invaders_message = Words_And_Phrases(135,190,Space_Invaders_message_list)
        Space_Invaders_message.Draw(10)

        ## drawing the score_advance_table
        score_advance_table_message = ['asterisk','S','C','O','R','E','space','A','D','V','A','N','C','E','space','T','A','B','L','E','asterisk']
        score_advance_table = Words_And_Phrases(80,250,score_advance_table_message)
        score_advance_table.Draw(10)

        ## drawing the alien display
        if Flag_Skip == False:
            mystery_ship_display = Mystery_Ship(144,285)
            mystery_ship_display.Draw()
            
            alien_3_display = Alien(153,320,3)
            alien_3_display.Draw('white')

            alien_1_display = Alien(150,355,1)
            alien_1_display.Draw('white')

            alien_2_display = Alien(150,390,2)
            alien_2_display.Draw('white')

        ## drawing the alien values

        mystery_point_message_list = ['equal','question_mark','space','M','Y','S','T','E','R','Y']
        mystery_point_message = Words_And_Phrases(180,285,mystery_point_message_list)
        mystery_point_message.Draw(10)
        
        thirty_points_message_list = ['equal',3,0,'space','P','O','I','N','T','S']
        thirty_points_message = Words_And_Phrases(180,320,thirty_points_message_list)
        thirty_points_message.Draw(10)

        twenty_points_message_list = ['equal',2,0,'space','P','O','I','N','T','S']
        twenty_points_message = Words_And_Phrases(180,355,twenty_points_message_list)
        twenty_points_message.Draw(10)

        ten_points_message_list = ['equal',1,0,'space','P','O','I','N','T','S']
        ten_points_message = Words_And_Phrases(180,390,ten_points_message_list)
        ten_points_message.Draw(10)

    ## setting up the short alien film

        # making the alien
        start_alien = Alien(605,149,3)
        start_alien.Speed = -5

        ## moving the alien towards the letter to take it
        while True:
            ## breaking the loop if the skip variable is true
            if Flag_Skip == True or Flag_Skip == 'stage_2':
                if Flag_Skip == True:
                    Fill_Black()
                break
            ## drawing the words
            pygame.draw.rect(screen,black,(0,150,480,15))
            play_message.Draw()
            y_message.Draw()

            ## drawing the alien
            start_alien.Draw()
            start_alien.Move_Alien()

            ## checking if the alien reaches the cordinate of 265 where it will take the letter
            if start_alien.xpos == 260:

                ## changing the alien speed
                start_alien.Speed = 5

                Close()
                pygame.display.update()
                clock.tick(30)
                break

            Close()
            pygame.display.update()
            clock.tick(30)

        ## moving the alien away from the letter to take it away
        while True:
            ## breaking the loop if the skip variable is true
            if Flag_Skip == True or Flag_Skip == 'stage_2':
                if Flag_Skip == True:
                    Fill_Black()
                break
            
            ## drawing the words
            pygame.draw.rect(screen,black,(0,150,480,15))
            play_message.Draw()

            ## drawing the alien
            start_alien.Draw_Letter_Take()
            start_alien.Move_Alien()

            ## checking if the alien reaches the cordinate of 600 where it will flip the letter
            if start_alien.xpos == 600:

                ## changing the alien speed
                start_alien.Speed = -5

                Close()
                pygame.display.update()
                clock.tick(30)
                break

            Close()
            pygame.display.update()
            clock.tick(30)

        ## moving the alien towards the letter to replace it
        while True:
            ## breaking the loop if the skip variable is true
            if Flag_Skip == True or Flag_Skip == 'stage_2':
                if Flag_Skip == True:
                    Fill_Black()
                break
            ## drawing the words
            pygame.draw.rect(screen,black,(0,150,480,15))
            play_message.Draw()
            ## drawing the alien
            start_alien.Draw_Letter_Place()
            ## checking if the alien reaches the cordinate of 260 where it place the flipped letter
            if start_alien.xpos == 260:

                # flipping the letter
                y_message_list = ['Y']
                y_message = Words_And_Phrases(255,150,y_message_list)

                ## changing the alien speed
                start_alien.Speed = 5

                Close()
                pygame.display.update()
                clock.tick(30)
                break

            ## moving the alien
            start_alien.Move_Alien()

            Close()
            pygame.display.update()
            clock.tick(30)
        
        ## moving the alien away from the letter
        while True:
            ## breaking the loop if the skip variable is true
            if Flag_Skip == True or Flag_Skip == 'stage_2':
                if Flag_Skip == True:
                    Fill_Black()
                break
            ## drawing the words
            pygame.draw.rect(screen,black,(0,150,480,15))
            play_message.Draw()
            y_message.Draw()

            ## drawing the alien
            start_alien.Move_Alien()
            start_alien.Draw()

            ## checking if the alien reaches the cordinate of 600 where the game will begin
            if start_alien.xpos == 600:
                Close()
                pygame.display.update()
                clock.tick(30)
                break

            Close()
            pygame.display.update()
            clock.tick(30)

        ## deleting the start alien from no use
        del start_alien

        ## ending the flag skip if it has not happened
        if Flag_Skip != 'stage_2':
            Flag_Skip = 'done'
        else:
            Flag_Skip = 'stage_3'

# setting up the final signal for the game to begin
    ## drawing the first part
        for xpos in range(0,600,120):
            screen.fill(black)
            ## drawing the scores
            score_message.Draw()
            player_1_score.Draw()
            player_2_score.Draw()
            high_score.Draw()

            ## drawing the buttons
            push_message_list = ['P','U','S','H']
            push_message = Words_And_Phrases(210,180,push_message_list)
            push_message.Draw()

            ## drawing the message describing the one player buttons used
            if Flag_Game_Mode == 'one_player':
                only_one_player_button_message_list = ['O','N','L','Y','space',1,'P','L','A','Y','E','R','space','B','U','T','T','O','N']
                only_one_player_button_message = Words_And_Phrases(97,230,only_one_player_button_message_list)
                only_one_player_button_message.Draw()

            ## drawing the message describing the two player buttons used
            elif Flag_Game_Mode == 'two_player':
                only_two_player_button_message_list = [2,'P','L','A','Y','E','R','space','B','U','T','T','O','N']
                only_two_player_button_message = Words_And_Phrases(135,230,only_two_player_button_message_list)
                only_two_player_button_message.Draw()

            ## drawing the disappearing rectangle
            pygame.draw.rect(screen,black,(xpos,0,480 - xpos,480))

            ## displaying the rectangle and screen only when the player has skpped
            if Flag_Skip == 'stage_3':
                Close()
                pygame.display.update()
                clock.tick(20)
        
        pygame.display.update()
        Pause(2)

    ## drawing the second part
        for i in range(1,30):
            screen.fill(black)
            if Flag_Game_Mode == 'one_player':
                ## blinking the first player's score and drawing the one player message
                one_player_message.Draw()
                if i%2 == 0:
                    player_1_score.Draw()

            if Flag_Game_Mode == 'two_player':
                ## blinking both players's score and drawing the two player message
                two_player_message.Draw()
                if i%2 == 0:
                    player_2_score.Draw()
                    player_1_score.Draw()
            else:
                player_2_score.Draw()

            ## drawing the rest of the score info
            score_message.Draw()
            high_score.Draw()
            
            Close()
            pygame.display.update()
            clock.tick(15)


## setting up the elements
        ## setting up the Gameover Flag Variable
        Flag_Gameover = False

        ## setting up the player, their backup, and their live 
        player_1 = None
        player_2 = None
        player_1_backup = []
        player_2_backup = []
        player_1_life = Words_And_Phrases(10,456,[])
        player_2_life = Words_And_Phrases(460,456,[])

        if Flag_Game_Mode == 'one_player' or Flag_Game_Mode == 'two_player':
            player_1 = Player(50,400)
            player_1_backup = [Player(30,450),Player(70,450)]
            player_1_life.phrase = [2]
        if Flag_Game_Mode == 'two_player':
            player_2 = Player(90,400)
            player_2_backup = [Player(420,450),Player(380,450)]
            player_2_life.phrase = [2]
            
        aliens = []
        Alien_Refill(True)

        ## alien attributes
        Alien_Explosion_List = []

        ## setting up the Mystery_Ship
        mystery_ship = Mystery_Ship(2500,90)
        Mystery_Ship_Explosion_List = []
        
        ## setting up the Barrier layout
        Barrier_layout = [[0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
                        [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
                        [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
                        [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
                        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
                        [1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1]]

        ## setting up the Barrier and alien invasion line
        Barrier1 = []
        Barrier2 = []
        Barrier3 = []
        Barrier4 = []
        alien_invasion_line = []
        Barrier_Refill()

        ## setting up the bullet lists
        player_1_bullets = []
        player_2_bullets = []
        alien_bullets = []
        Bullet_Explosion_List = []
        
    # setting up the screen
        Screen_Draw()

    ## starting the game
        while True:
            screen.fill(black)

        ## moving the player
            if player_1 != None:
                player_1.Move_Player()
            if player_2 != None:
                player_2.Move_Player()

        ## moving the mystery ship
            mystery_ship.Move_Mystery_Ship()
            mystery_ship.Play_Sound()

        ## moving aliens and changing animations only if there is at least one alien on the screen
            if len(Alien_Explosion_List) == 0:
                Alien.Timer = Alien.Timer - 1
                if  Alien.Timer <= 0:
                    Alien.Timer = 2
                    if Alien.Flag_Down_Step == True:
                        for i in range(len(aliens[Alien.Counter_Movement])):
                            aliens[Alien.Counter_Movement][i].Move_Down()
                            aliens[Alien.Counter_Movement][i].Shoot()
                            aliens[Alien.Counter_Movement][i].Check()
                    for i in range(len(aliens[Alien.Counter_Movement])):
                        aliens[Alien.Counter_Movement][i].Move_Alien()
                        aliens[Alien.Counter_Movement][i].Shoot()
                        aliens[Alien.Counter_Movement][i].Check()
                    Alien.Counter_Movement = Alien.Counter_Movement + 1

        ## checking if all the aliens have moved
            if Alien.Counter_Movement == len(aliens):
                Alien.Counter_Movement = 0

            ## stoping the aliens from continously moving down
                if Alien.Flag_Collide_Side != None and Alien.Flag_Down_Step == True:
                    Alien.Flag_Down_Step = False
                    Alien.Flag_Collide_Side = None

            ## enabling the aliens to move down
                if Alien.Flag_Collide_Side != None:
                    Alien.Flag_Down_Step = True
                
            ## playing the background music of the alien movement
                mixer.music.load(Game_Element.Basic_Sound_Url+'background sound '+str(Alien.Counter_Background_Sound)+'.wav')
                mixer.music.play()
                Alien.Counter_Background_Sound = Alien.Counter_Background_Sound + 1
                if Alien.Counter_Background_Sound == 5:
                    Alien.Counter_Background_Sound = 1

        ## moving the alien bullets
            alien_bullet_Iteration_Counter = 0
            while True:
                if alien_bullet_Iteration_Counter >= len(alien_bullets):
                    break
                alien_bullets_length = len(alien_bullets)
                alien_bullets[alien_bullet_Iteration_Counter].Move_Alien_Bullet()
                alien_bullets[alien_bullet_Iteration_Counter].Check()
                if len(alien_bullets) == alien_bullets_length:
                    alien_bullet_Iteration_Counter = alien_bullet_Iteration_Counter + 1

        ## moving the player bullets
            for bullet in player_1_bullets:
                bullet.Move_Bullet()
                bullet.Check()
            for bullet in player_2_bullets:
                bullet.Move_Bullet()
                bullet.Check()

        ## updating the alien dead timer
            Alien_Explosion_Iteration_Counter = 0
            while True:
                if Alien_Explosion_Iteration_Counter == len(Alien_Explosion_List):
                    break
                Alien_Explosion_Length = len(Alien_Explosion_List)
                Alien_Explosion_List[Alien_Explosion_Iteration_Counter].Update_Timer()
                if Alien_Explosion_Length == len(Alien_Explosion_List):
                    Alien_Explosion_Iteration_Counter = Alien_Explosion_Iteration_Counter + 1
            
            Mystery_Ship_Explosion_Iteration_Counter = 0
            while True:
                if Mystery_Ship_Explosion_Iteration_Counter == len(Mystery_Ship_Explosion_List):
                    break
                Mystery_Ship_Explosion_Length = len(Mystery_Ship_Explosion_List)
                Mystery_Ship_Explosion_List[Mystery_Ship_Explosion_Iteration_Counter].Update_Timer()
                if Mystery_Ship_Explosion_Length == len(Mystery_Ship_Explosion_List):
                    Mystery_Ship_Explosion_Iteration_Counter = Mystery_Ship_Explosion_Iteration_Counter + 1
 
            ## The Key Loop
            for event in pygame.event.get():
                ## quit 
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        if player_1 != None:
                            player_1.Flag_Movement_Direction = 'right'
                        else:
                            player_2.Flag_Movement_Direction = 'right'
                    elif event.key == K_LEFT:
                        if player_1 != None:
                            player_1.Flag_Movement_Direction = 'left'
                        else:
                            player_2.Flag_Movement_Direction = 'left'
                    elif event.key == K_a:
                        if player_2 != None:
                            player_2.Flag_Movement_Direction = 'left'
                        else:
                            player_1.Flag_Movement_Direction = 'left'
                    elif event.key == K_d:
                        if player_2 != None:
                            player_2.Flag_Movement_Direction = 'right'
                        else:
                            player_1.Flag_Movement_Direction = 'right'

                ## shooting bullets using space
                    if event.key == K_SPACE:
                        if player_1 != None:
                            if player_1.Shoot_Timer <= 0 and len(player_1_bullets) == 0:
                                player_1.Shoot_Timer = 60
                                player_1.Shoot_Iteration_Counter = player_1.Shoot_Iteration_Counter + 1
                                player_1_bullets.append(Player_Bullet(player_1.xpos + 14,player_1.ypos - 10))


                                ## playing the sound
                                Player.Shoot_Sound.play()
                        else:
                            if player_2.Shoot_Timer <= 0 and len(player_2_bullets) == 0:
                                player_2.Shoot_Iteration_Counter = player_2.Shoot_Iteration_Counter + 1
                                player_2.Shoot_Timer = 60
                                player_2_bullets.append(Player_Bullet(player_2.xpos + 14,player_2.ypos - 10))

                                ## playing the sound
                                Player.Shoot_Sound.play()

                ## shooting bullets using x
                    if event.key == K_x: 
                        if player_2 != None:
                            if player_2.Shoot_Timer <= 0 and len(player_2_bullets) == 0:
                                player_2.Shoot_Timer = 60
                                player_2_bullets.append(Player_Bullet(player_2.xpos + 14,player_2.ypos - 10))

                                ## playing the sound
                                Player.Shoot_Sound.play()
                        else:
                            if player_1.Shoot_Timer <= 0 and len(player_1_bullets) == 0:
                                player_1.Shoot_Timer = 60
                                player_1_bullets.append(Player_Bullet(player_1.xpos + 14,player_1.ypos - 10))

                                ## playing the sound
                                Player.Shoot_Sound.play()


                ## checking if the keys are lifted
                if event.type == KEYUP:
                    if event.key == K_RIGHT:
                        if player_1 != None:
                            if player_1.Flag_Movement_Direction == 'right':
                                player_1.Flag_Movement_Direction = None
                        else:
                            if player_2.Flag_Movement_Direction == 'right':
                                player_2.Flag_Movement_Direction = None
                    elif event.key == K_LEFT:
                        if player_1 != None:
                            if player_1.Flag_Movement_Direction == 'left':
                                player_1.Flag_Movement_Direction = None
                        else:
                            if player_2.Flag_Movement_Direction == 'left':
                                player_2.Flag_Movement_Direction = None
                    if event.key == K_a:
                        if player_2 != None:
                            if player_2.Flag_Movement_Direction == 'left':
                                player_2.Flag_Movement_Direction = None
                        else:
                            if player_1.Flag_Movement_Direction == 'left':
                                player_1.Flag_Movement_Direction = None
                    elif event.key == K_d:
                        if player_2 != None:
                            if player_2.Flag_Movement_Direction == 'right':
                                player_2.Flag_Movement_Direction = None
                        else:
                            if player_1.Flag_Movement_Direction == 'right':
                                player_1.Flag_Movement_Direction = None

    ## drawing things 
        ## drawing the alien invasion line
            for Barrier_particle in alien_invasion_line:
                Barrier_particle.Draw()

        ## drawing the score
            score_message.Draw()
            player_1_score.Draw()
            player_2_score.Draw()
            high_score.Draw()            
            player_1_life.Draw()
            player_2_life.Draw()
            
        ## drawing the player
            if player_1 != None:
                player_1.Draw('green')
            if player_2 != None:
                player_2.Draw('blue')
            for player in player_1_backup:
                player.Draw('green')
            for player in player_2_backup:
                player.Draw('blue')
            
        ## drawing the Barriers
            for Barrier_particle in Barrier1:
                Barrier_particle.Draw()
            for Barrier_particle in Barrier2:
                Barrier_particle.Draw()
            for Barrier_particle in Barrier3:
                Barrier_particle.Draw()
            for Barrier_particle in Barrier4:
                Barrier_particle.Draw()
                
        ## drawing the Mystery_Ship
            mystery_ship.Draw()

        ## drawing the aliens
            for group in aliens:
                for alien in group:
                    if alien.ypos >= 315:
                        alien.Draw('green')
                    else:
                        alien.Draw('white')

        ## drawing the Alien_Explosion and Mystery Ship Explosion
            for explosion in Alien_Explosion_List:
                explosion.Draw()
            for explosion in Mystery_Ship_Explosion_List:
                explosion.Draw()
                
        ## drawing the player bullet with the specific color
            for bullet in player_1_bullets:
                if Flag_Game_Mode == 'two_player':
                    bullet.Draw('green')
                else:
                    bullet.Draw('white')
            for bullet in player_2_bullets:
                bullet.Draw('blue')
            
        ## drawing the alien bullets;
            for bullet in alien_bullets:
                bullet.Draw()

        ## updating the player bullet timer
            if Player.Shoot_Timer > 0:
                Player.Shoot_Timer = Player.Shoot_Timer - 1
                
        ##drawing the explosion caused by the player and alien bullets
            bullet_explosion_Iteration_Counter = 0
            while True:
                if bullet_explosion_Iteration_Counter == len(Bullet_Explosion_List):
                    break
                Bullet_Explosion_List[bullet_explosion_Iteration_Counter].Draw()
                Bullet_Explosion_List[bullet_explosion_Iteration_Counter].Explosion_Timer = Bullet_Explosion_List[bullet_explosion_Iteration_Counter].Explosion_Timer - 1
                if Bullet_Explosion_List[bullet_explosion_Iteration_Counter].Explosion_Timer == 0:
                    Bullet_Explosion_List.pop(bullet_explosion_Iteration_Counter)
                else:
                    bullet_explosion_Iteration_Counter = bullet_explosion_Iteration_Counter + 1

        ## updating the window
            pygame.display.update()
            clock.tick(60)

            ## checking if all the aliens are shot
            if len(aliens) == 0 and len(Alien_Explosion_List) == 0:
                ## emptying all the bullet lists
                alien_bullets = []
                player_1_bullets = []
                player_2_bullets = []

                ## changing the alien's counter ypos
                Alien.Counter_Position = Alien.Counter_Position + 1
                if Alien.Counter_Position == 10:
                    Alien.Counter_Position = 0

                ## resetting the player's xpos 
                if player_1 != None:
                    player_1.xpos = 50
                    player_1.Flag_Movement_Direction = None
                elif player_2 != None:
                    player_2.xpos = 90
                    player_2.Flag_Movement_Direction = None

                ## Refilling Aliens and Barriers
                Alien_Refill()
                Barrier_Refill()

                Screen_Draw()

        ## checking if the players are hit
            if player_1 != None:
                if player_1.Flag_Struck == True:
                    Player_Explode(player_1)

            if player_2 != None:
                if player_2.Flag_Struck == True:
                    Player_Explode(player_2)

        ## ending the game
            if Flag_Gameover == True:
                ## drawing the Game Over Sign
                game_over_message_list = ['G','A','M','E','O','V','E','R']
                game_over_message = Words_And_Phrases(180,120,game_over_message_list)
                game_over_message.Draw()
                pygame.display.update()
                Pause(2)
                break

def Menu():

    class Game_Element:
        Basic_Sound_Url = 'Sounds\\'
        Basic_Url = 'Images\\'
        def __init__(self,xpos,ypos):
            self.xpos = xpos
            self.ypos = ypos

    class Words_And_Phrases(Game_Element):
        ## uploading all the character names
        Character_Dictionary = {}
        Character_Name_List = ['A','B','C','D','E','E','F','G','H','I','J','K','L','M','N',
                                'O','P','Q','R','S','T','U','V','W','X','Y','Z','SPACE',0,1,2,
                                 3,4,5,6,7,8,9,'left','right','equal','asterisk','question_mark','dash','space','yflip']
        
        ## uploading all the character
        Character_Image_List = []
        for character_name in Character_Name_List:
            Character_Image_List.append(pygame.image.load(Game_Element.Basic_Url+'letters\\'+str(character_name)+'.jpeg'))
     
        ## storing the resized character images into a dictionary with the value of the respective character name 
        for index in range(len(Character_Name_List)):
            character_image = Character_Image_List[index]
            resized_character_image = pygame.transform.scale(character_image,(10,14))
            Character_Dictionary[Character_Name_List[index]] = resized_character_image
            
        def __init__(self,xpos,ypos,phrase):
            super().__init__(xpos,ypos)
            self.phrase = phrase
        def Draw(self):
            Counter_Spacing = 0

            for character in self.phrase:
                ## drawing the letter
                screen.blit(Words_And_Phrases.Character_Dictionary[character],(self.xpos + Counter_Spacing,self.ypos))
                Counter_Spacing = Counter_Spacing + 15

    def Middle(phrase):
        space = 480 - len(phrase)*15
        print(space/2)
        
    while True:

        ## setting up the messages
        Space_Invaders_Message_List = ['S','P','A','C','E','space','I','N','V','A','D','E','R','S']
        Space_Invaders_Message = Words_And_Phrases(135,100,Space_Invaders_Message_List)
        Space_Invaders_Message.Draw()

        Space_Invaders_2_Message_List = ['S','P','A','C','E','space','I','N','V','A','D','E','R','S',2]
        Space_Invaders_2_Message = Words_And_Phrases(100,140,Space_Invaders_2_Message_List)
        Space_Invaders_2_Message.Draw()

        Middle(Space_Invaders_Message_List)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        clock.tick(60)
        pygame.display.update()
Menu()