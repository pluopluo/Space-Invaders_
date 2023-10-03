## importing files
import random
import pygame
from pygame.locals import *
from customcolors import *
from pygame import mixer

## setting up pygame, it's screen, caption, and clock
pygame.init()
screen = pygame.display.set_mode((480,480))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()                           

## setting up the game play
def MainGame():

    def Close_Or_Skip():
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            ## skipping if the enter key is pressed
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:              
                    nonlocal flag_skip
                    if flag_skip == False:
                        flag_skip = True
    
    def Pause(time):
        num_of_time_units = int(time*60)
        for time_unit in range(0,num_of_time_units):
            ## checking if the player has pressed skip when the screen pauses
            Close_Or_Skip()
            if flag_skip == True or flag_skip == 'stage_2':
                if flag_skip == True:
                    Fill_Black()
                break
            clock.tick(60)

    def Collide(object_1,object_2):
        if object_1.xpos + object_1.length > object_2.xpos and object_2.xpos + object_2.length > object_1.xpos:
            if object_1.ypos + object_1.height > object_2.ypos and object_2.ypos + object_2.height > object_1.ypos:
                return True
            
    def Alien_Barrier_Collision(alien,Barrier):
        barrier_iteration_counter = 0
        barrier_struck = False

        ## iterating through the barriers
        while True:
            if barrier_iteration_counter == len(Barrier):
                break

            ## checking if a barrier block hit the alien
            if alien.xpos + alien.length >= Barrier[barrier_iteration_counter].xpos and alien.xpos <= Barrier[barrier_iteration_counter].xpos + Barrier[barrier_iteration_counter].length:
                if alien.ypos + alien.height >= Barrier[barrier_iteration_counter].ypos:
                    barrier_struck = True
            
            ## destroying the barrier block
            if barrier_struck == True:
                Barrier.pop(barrier_iteration_counter)
                barrier_struck = False
            else:
                ## updating the iteration counter only if the barrier isn't destroyed
                barrier_iteration_counter = barrier_iteration_counter + 1

    def Bullet_Barrier_Collision(Barrier,bullet):
        ## declaring nonlocals to the bullet lists and the bullet explosion list
        nonlocal player_1.Bullet_List, Player_2_Bullets, Alien_Bullets, bullet_explosion_list
    
        ## checking what type of bullet it is and what iteration should be performed ont he Barrier
        if bullet in Alien_Bullets:
            Barrier_Iteration = [0,len(Barrier),1]
            
        elif bullet in player_1.Bullet_List or bullet in Player_2_Bullets:
            Barrier_Iteration = [len(Barrier) - 1,-1,-1]
         
        ## checking the Barrier and if the divisor is supposed to be 2
        if Barrier == alien_invasion_line:
            divisor = 2
        else:
            divisor = 1

        target_barrier = None
        ## checking the specific particle the bullet hits
        for i in range(Barrier_Iteration[0],Barrier_Iteration[1],Barrier_Iteration[2]):
            if Collide(bullet,Barrier[i]) == True:
                target_barrier = Barrier[i]
                barrier_iteration_counter = 0
                barrier_struck = False
                while True:
                    # breaking the bullet and the while loop
                    if barrier_iteration_counter >= len(Barrier):
                        if bullet in Alien_Bullets:
                            Alien_Bullets.remove(bullet)
                        if bullet in player_1.Bullet_List:
                            player_1.Bullet_List.remove(bullet)
                        if bullet in Player_2_Bullets:
                            Player_2_Bullets.remove(bullet)
                        break
                
                    ## checking if the xpos is correct
                    if Barrier[barrier_iteration_counter].xpos%(divisor*2) == 0:
                        ## checking if the Barrier particle is in close range of the area hit by the bullet
                        if target_barrier.xpos - bullet.Dr[0]*2 < Barrier[barrier_iteration_counter].xpos < target_barrier.xpos + target_barrier.length + bullet.Dr[0]:
                            if target_barrier.ypos - bullet.Dr[1]*2 < Barrier[barrier_iteration_counter].ypos < target_barrier.ypos + target_barrier.height + bullet.Dr[1]*2:
                                barrier_struck = True
                            
                        ## checking if the Barrier particle is in far range of the area struck by the bullet
                        if target_barrier.xpos - bullet.Dr[2]*2 < Barrier[barrier_iteration_counter].xpos < target_barrier.xpos + target_barrier.height + bullet.Dr[2]*2:
                            if target_barrier.ypos - bullet.Dr[3]*2 < Barrier[barrier_iteration_counter].ypos < target_barrier.ypos + target_barrier.height + bullet.Dr[3]*2:
                                # deciding how far it is and the chance of the Barrier being destroyed
                                y_distance = abs(target_barrier.ypos - Barrier[barrier_iteration_counter].ypos) + 1
                                x_distance = abs(target_barrier.xpos - Barrier[barrier_iteration_counter].xpos) + 1
                                x_range = x_distance//(bullet.Dr[2])
                                y_range = y_distance//(bullet.Dr[3])
                                if random.randint(0,x_range) == 0 and random.randint(0,y_range) == 0:
                                    barrier_struck = True

                    ## destroying the Barrier partlce
                    if barrier_struck == True:
                        Barrier.pop(barrier_iteration_counter)
                        barrier_struck = False
                    else:
                        barrier_iteration_counter = barrier_iteration_counter + 1
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
        nonlocal Alien_Bullets, player_1.Bullet_List, Player_2_Bullets
        nonlocal player_1, player_2, player_1_life, player_2.lives
        nonlocal flag_gameover
 
        ## playing the sound
        Player_Explosion.Sound.play()                

        ## uploading the player_explosion images
        player_explosion = Player_Explosion(player.xpos,player.ypos,40,20)

        ## drawing the player_explosion
        for iteration in range(1,20):
            for animation in range(1,3):
                player_explosion.Draw(animation)
                Close_Or_Skip()
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
            if len(Player_2_Backup) != 0:

                ## resetting the player's attributes
                player_2.Flag_Movement_Direction = None
                player_2.Flag_Struck = False
                player_2.ypos = 400
                player_2.xpos = 90
                
                ## changing the player's lives
                Player_2_Backup.pop(-1)
                player_2.lives.phrase[0] = player_2.lives.phrase[0] - 1

            elif len(Player_2_Backup) == 0:

                ## removing the player from the game
                player_2 = None

        ## checking if the game ends
        if player_1 == None and player_2 == None:
            flag_gameover = True

    def Fill_Alien(Start_Game=False):

        ## nonlocal declaration to the lists and variables
        nonlocal alien_list
        
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

        ## filling the alien_list
        for row in range(len(Alien.layout) - 1,-1,-1):
            for group in range(len(Alien.layout[row]) - 1,-1,-1):
                alien_group = []
                for alien in range(len(Alien.layout[row][group]),0,-1):
                    ## checking the x-value to place the alien because the lists are uneven
                    if len(Alien.layout[row][group]) == 1:
                        xpos = 60
                    else:
                        xpos = alien*30

                    ## adding the alien_list to the group list
                    if row == 4 or row == 3:
                        alien_group.append(Alien(group*60 + xpos + 20,row*30 + 120 + 6*Alien.Counter_Position,2))
                    elif row == 2 or row == 1:
                        alien_group.append(Alien(group*60 + xpos + 20,row*30 + 120 + 6*Alien.Counter_Position,1))
                    else:
                        alien_group.append(Alien(group*60 + xpos + 20,row*30 + 120 + 6*Alien.Counter_Position,3))

                ## adding the group list to the alien list
                alien_list.append(alien_group)

    def Barrier_Refill():
        ## globalizing the Barrier lists
        nonlocal barrier1,barrier2,barrier3,barrier4,alien_invasion_line

        ## filling the Barrier lists
        for row in range(0,len(barrier_layout)):
            for column in range(len(barrier_layout[row])):
                if barrier_layout[row][column] == 1:
                    barrier1.append(Barrier(column*2 + 48,row*2 + 330))
                    barrier2.append(Barrier(column*2 + 156,row*2 + 330))
                    barrier3.append(Barrier(column*2 + 264,row*2 + 330))
                    barrier4.append(Barrier(column*2 + 372,row*2 + 330))
        
        ## filling the alien invasion line
        for row in range(0,1):
            for column in range(0,480):
                alien_invasion_line.append(Barrier(column*2,row*2 + 435))

    def Fill_Black():
        ## filling the screen quickly but not directly
        for xpos in range(0,480,60):
            pygame.draw.rect(screen,black,(xpos,0,60,480))
            Close_Or_Skip()
            pygame.display.update()
            clock.tick(40)

        ## making sure that the function doesn't happen again if the player has skipped
        nonlocal flag_skip
        if flag_skip == True:
            flag_skip  = 'stage_2'

    def Screen_Draw(start_of_game = False):     

    ## limiting the process of drawing everything to be only at the start of the game 
        if start_of_game == True:
            screen.fill(black)

            ## drawing the score messages and the credits
            score_message.Draw()
            player_1_score.Draw()
            player_2_score.Draw()
            high_score.Draw()
            player_1_life.Draw()
            player_2.lives.Draw()
            credit_message.Draw()

            ## drawing the floor
            for barrier_particle in alien_invasion_line:
                barrier_particle.Draw()

            ## drawing the Barrier
            for barrier_particle in barrier1:
                barrier_particle.Draw()
            for barrier_particle in barrier2:
                barrier_particle.Draw()
            for barrier_particle in barrier3:
                barrier_particle.Draw()
            for barrier_particle in barrier4:
                barrier_particle.Draw()
            
            ## drawing the players 
            player_1.Draw('green')
            if player_2 != None:
                player_2.Draw('blue')
            for player in player_1_backup:
                player.Draw('green')
            for player in Player_2_Backup:
                player.Draw('blue')
        
        ## drawing the alien_list and closing the screen if the quit button is pressed
        for group in alien_list:
            for alien in group:
                alien.Draw('white')
                Close_Or_Skip()
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
        Character_Name_List = ['A','B','C','D','E','E','F','G','H','I','J','K','L','M','N',
                                'O','P','Q','R','S','T','U','V','W','X','Y','Z',0,1,2,
                                3,4,5,6,7,8,9,'left','right','equal','asterisk','question_mark','dash','space','yflip']
        
        ## uploading all the character images, transforming it, and storing it in a dictionary with respective value
        Character_Dictionary = {}
        for character_name in Character_Name_List:

            ## loading the image, transforming it, then storing it
            img = pygame.image.load(Game_Element.Basic_Url+'letters\\'+str(character_name)+'.jpeg')
            img = pygame.transform.scale(img,(10,14))
            Character_Dictionary[character_name] = img
            
        def __init__(self,xpos,ypos,phrase):

            ## setting up the xpos, ypos and phrase
            super().__init__(xpos,ypos)
            self.phrase = phrase

        def Draw(self,delay=0):

            ## setting up the counter spacing used for drawing 
            Counter_Spacing = 0

            ## iteration process
            for character in self.phrase:

                ## checking if the player decides to skip
                if Player_Selected == True:
                    if flag_skip == True or flag_skip == 'stage_2':
                        if flag_skip == True:
                            Fill_Black()
                        break 
                
                ## checking if the character is a symbol and changing it to words
                if character == '<':
                    character = 'left'
                elif character == '>':
                    character = 'right'
                elif character == '=':
                    character = 'equal'
                elif character == '*':
                    character = 'asterisk'
                elif character == '?':
                    character = 'question_mark'
                elif character == '-':
                    character = 'dash'
                elif character == ' ':
                    character = 'space'
                
                ## checking if the character is a string number and changing it to an integar
                string_number_list = ['0','1','2','3','4','5','6','7','8','9']
                if character in string_number_list:
                    character = int(character)
                
                ## drawing the letter and increasing the counter spacing
                screen.blit(Words_And_Phrases.Character_Dictionary[character],(self.xpos + Counter_Spacing,self.ypos))
                Counter_Spacing = Counter_Spacing + 15

                ## pausing if there is a delay
                if delay != 0:
                    pygame.display.update()
                    Pause(delay/60)

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

        ## loading and transforming the images and then adding them to the list
        for image_number in range(1,5):
            img = pygame.image.load(Game_Element.Basic_Url+'Alien Letter Flip\Interaction '+str(image_number)+'.jpeg')
            img = pygame.transform.scale(img,(32,15))
            Letter_Flip_Image_List.append(img)
        
        ## setting up the alien images
        Image_List = []

        ## uploading all the images
        for alien_color in ['White','Green']:
            alien_type_list = []
            for alien_type in range(1,4):
                alien_animation_list = []
                for animation_frame in range(1,3):

                    ## loading the image
                    img = pygame.image.load(Game_Element.Basic_Url+'Alien\\'+str(alien_color)+' '+str(alien_type)+' '+str(animation_frame)+'.jpeg')
        
                    ## deciding the width of the alien_list
                    if alien_type == 3:
                        alien_length = 15
                    else:
                        alien_length = 20

                    ## transforming the image
                    img = pygame.transform.scale(img,(alien_length,15))

                    ## storing the images in lists
                    alien_animation_list.append(img)
                alien_type_list.append(alien_animation_list)
            Image_List.append(alien_type_list)

        def __init__(self,xpos,ypos,type):
            super().__init__(xpos,ypos)
            self.type = type

            ## deciding the length and width
            if self.type == 3:
                self.length = 15
                self.height = 15
            else:
                self.length = 20
                self.height = 15

        def Move_Alien(self):
            self.xpos = self.xpos + self.Speed
            
            ## changing the alien's animation
            if self.Current_Animation == 0:
                self.Current_Animation = 1
            elif self.Current_Animation == 1:
                self.Current_Animation = 0

        def Move_Down(self):
            ## changing the alien_list' ypos
            self.ypos = self.ypos + (15 - (Alien.Counter_Position/2))

            ## changing the alien_list' speed based on the collide side
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

            ## checking if the alien_list reach the Barrier
            if self.ypos + self.height > 330 and self.ypos < 370:
                if self.xpos + self.length > 48 and self.xpos < 108:
                    Alien_Barrier_Collision(self,barrier1)
                elif self.xpos + self.length > 156 and self.xpos < 216:
                    Alien_Barrier_Collision(self,barrier2)
                elif self.xpos + self.length > 264 and self.xpos < 324:
                    Alien_Barrier_Collision(self,barrier3)
                elif self.xpos + self.length > 372 and self.xpos < 432:
                    Alien_Barrier_Collision(self,barrier4)

            # checking if the alien_list hit the invasion line or invade
            if self.ypos + self.height == 435:
                nonlocal flag_gameover
                flag_gameover = True

        def Shoot(self):
            ## alien_list shooting a bullet
            if random.randint(1,100) == 1:
                Alien_Bullets.append(Alien_Bullet(self.xpos,self.ypos))

        def Draw(self,color='white'):
            ## drawing the alien based on the color selected
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
            nonlocal player_1.Bullet_List, Player_2_Bullets
            nonlocal player_1_score, player_2_score

            ## checking if the player_1.Bullet_List hit the Barriers
            if self.ypos + self.height > 330 and self.ypos < 370:
                if self.xpos + self.length > 48 and self.xpos < 108:
                    Bullet_Barrier_Collision(barrier1,self)
                elif self.xpos + self.length > 156 and self.xpos < 216:
                    Bullet_Barrier_Collision(barrier2,self)
                elif self.xpos + self.length > 264 and self.xpos < 324:
                    Bullet_Barrier_Collision(barrier3,self)
                elif self.xpos + self.length > 372 and self.xpos < 432:
                    Bullet_Barrier_Collision(barrier4,self)

            ## checking if the bullets hit the alien
            if self in player_1.Bullet_List or self in Player_2_Bullets:
                for group in alien_list:
                    for alien in group:
                        if Collide(alien,self) == True:

                            ## removing the alien
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
                            if self in player_1.Bullet_List:
                                player_1_score.phrase[2] = player_1_score.phrase[2] + increment
                                player_1.Bullet_List.remove(self)
                            elif self in Player_2_Bullets:
                                player_2_score.phrase[2] = player_2_score.phrase[2] + increment
                                Player_2_Bullets.remove(self)

                            ## updating the high score
                            high_score.phrase[2] = high_score.phrase[2] + increment

                            ## checking if the counter alien movement variable should be changed
                            if len(group) == 0:
                                if Alien.Counter_Movement > alien_list.index(group):
                                    Alien.Counter_Movement = Alien.Counter_Movement - 1
                                alien_list.remove(group)
                                
                            ## adding the explosion to the explosion list
                            alien_explosion_list.append(Alien_Explosion(alien.xpos,alien.ypos))

                            ## playing the explosion sound
                            Alien_Explosion.Sound.play()
                            break 

                    ## ending the iteration if the bullet is removed
                    if self not in player_1.Bullet_List and self not in Player_2_Bullets:
                        break

            ## checking if the bullet hits the mystery ship
            if self in player_1.Bullet_List:
                if Collide(self,mystery_ship) == True:

                    ## checking if the player 1 bullets hits the mystery ship at the 15th shot and making it worth 300 points
                        if player_1.Lucky_Shot == True:
                            if (player_1.Shoot_Iteration_Counter - 23)%15 == 0:
                                mystery_ship_explosion_list.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,300))
                                player_1_score.phrase[1] = player_1_score.phrase[1] + 3
                                high_score.phrase[1] = high_score.phrase[1] + 3
                            else:
                                player_1.Lucky_Shot = False

                    ## checking if otherwise and making it worth 200 points
                        if player_1.Lucky_Shot == False:
                            mystery_ship_explosion_list.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,200))
                            player_1_score.phrase[1] = player_1_score.phrase[1] + 2
                            high_score.phrase[1] = high_score.phrase[1] + 2

                    ## checking if the player 1 bullet hits the mystery ship on the 23rd shot 
                        if player_1.Shoot_Iteration_Counter == 23:
                            player_1.Lucky_Shot = True

                    ## relocating the mystery ship
                        mystery_ship.xpos = 2500

                    ## removing the bullet from the bullet list
                        player_1.Bullet_List.remove(self)

                    ## playing the mystery ship's explosion sound
                        Mystery_Ship_Explosion.Sound.play()

            elif self in Player_2_Bullets:
                if Collide(self,mystery_ship) == True:

                    ## checking if the player 2's bullets hits the mystery ship at the 15th shot and making it worth 300 points
                        if player_2.Lucky_Shot == True:
                            if (player_2.Shoot_Iteration_Counter - 23)%15 == 0:
                                mystery_ship_explosion_list.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,300))
                                player_2_score.phrase[1] = player_1_score.phrase[1] + 3
                                high_score.phrase[1] = high_score.phrase[1] + 3
                            else:
                                player_2.Lucky_Shot = False

                    ## checking if otherwise and making it worth 200 points
                        if player_2.Lucky_Shot == False:
                            mystery_ship_explosion_list.append(Mystery_Ship_Explosion(mystery_ship.xpos,mystery_ship.ypos,200))
                            player_2_score.phrase[1] = player_2_score.phrase[1] + 2
                            high_score.phrase[1] = high_score.phrase[1] + 2
                            
                    ## checking if the player 2's bullet hits the mystery ship on the 23rd shot
                        if player_2.Shoot_Iteration_Counter == 23:
                            player_2.Lucky_Shot = True

                    ## relocating the mystery ship
                        mystery_ship.xpos = 2500

                    ## removing the bullet from the bullet list
                        Player_2_Bullets.remove(self)

                    ## playing the mystery ship's explosion sound
                        Mystery_Ship_Explosion.Sound.play()
   
            ## checking if the hundreads or thousands place in the scores should be updated
            Update_Score(player_1_score)
            Update_Score(player_2_score)
            Update_Score(high_score)

            ## checking if the player bullet hits the top of the screen
            if self in player_1.Bullet_List or self in Player_2_Bullets:
                if self.ypos < 0:
                    if self in player_1.Bullet_List:
                        player_1.Bullet_List.remove(self)
                    elif self in Player_2_Bullets:
                        Player_2_Bullets.remove(self)
                    bullet_explosion_list.append(Bullet_Explosion(self.xpos - 6,self.ypos))

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
            nonlocal Alien_Bullets, bullet_explosion_list
            Alien_Bullets_length = len(Alien_Bullets)
            ## checking if the Alien_Bullets hit the Barriers
            if self.ypos + self.height > 330 and self.ypos < 370:
                if self.xpos + self.length > 48 and self.xpos < 108:
                    Bullet_Barrier_Collision(barrier1,self)
                elif self.xpos + self.length > 156 and self.xpos < 216:
                    Bullet_Barrier_Collision(barrier2,self)
                elif self.xpos + self.length > 264 and self.xpos < 324:
                    Bullet_Barrier_Collision(barrier3,self)
                elif self.xpos + self.length > 372 and self.xpos < 432:
                    Bullet_Barrier_Collision(barrier4,self)

            ## checking if the Alien_Bullets hits the boundary line
            if self.ypos + self.height > 435 and len(Alien_Bullets) == Alien_Bullets_length:
                Bullet_Barrier_Collision(alien_invasion_line,self)
                if self in Alien_Bullets:
                    Alien_Bullets.remove(self)
                bullet_explosion_list.append(Bullet_Explosion(self.xpos - 3,self.ypos - 4,))

            ## checking if the alien_bullet hit the player bullet
            if len(Alien_Bullets) == Alien_Bullets_length:
                for bullet in player_1.Bullet_List:
                    if self.xpos + self.length > bullet.xpos and bullet.xpos + bullet.length > self.xpos and self.ypos + self.height > bullet.ypos and bullet.ypos + bullet.height > self.ypos:
                        player_1.Bullet_List.remove(bullet)
                        bullet_explosion_list.append(Bullet_Explosion(bullet.xpos - 6,bullet.ypos - 8))
                        if self.type == 1:
                            if random.randint(1,2) == 1:
                                Alien_Bullets.remove(self)
                        elif self.type == 2:
                            if random.randint(1,3) == 1:
                                Alien_Bullets.remove(self)
                        break

            if len(Alien_Bullets) == Alien_Bullets_length:
                for bullet in Player_2_Bullets:
                    if Collide(self,bullet) == True:
                        Player_2_Bullets.remove(bullet)
                        bullet_explosion_list.append(Bullet_Explosion(bullet.xpos - 6,bullet.ypos - 8))
                        if self.type == 1:
                            if random.randint(1,2) == 1:
                                Alien_Bullets.remove(self)
                        elif self.type == 2:
                            if random.randint(1,3) == 1:
                                Alien_Bullets.remove(self)
                        break

            # ## checking if the alien bullet hits the player
            if len(Alien_Bullets) == Alien_Bullets_length:
                if player_1 != None:
                    if Collide(self,player_1) == True:
                        Alien_Bullets.remove(self)
                        player_1.Flag_Struck = True

            if len(Alien_Bullets) == Alien_Bullets_length:
                if player_2 != None:
                    if Collide(self,player_2) == True:
                        Alien_Bullets.remove(self)
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

        ## setting up it's sound
        Sound = mixer.Sound(Game_Element.Basic_Sound_Url+'alien shot sound.wav')

        ## setting up the Existing_Timer
        Existing_Timer = 10

        def Update_Timer(self):
            ## removing the explosion when the timer reaches zero
            self.Existing_Timer = self.Existing_Timer - 1
            if self.Existing_Timer == 0:
                nonlocal alien_explosion_list
                alien_explosion_list.remove(self)

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
            ## removing the explosion when the timer reaches zero
            self.Existing_Timer = self.Existing_Timer - 1
            if self.Existing_Timer == 0:
                nonlocal mystery_ship_explosion_list
                mystery_ship_explosion_list.remove(self)

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
        please_select_message = Words_And_Phrases(140,140,'PLEASE SELECT')
        one_or_two_players_message = Words_And_Phrases(120,180,'<1 OR 2 PLAYERS>')
        one_player_message = Words_And_Phrases(190,220,'1PLAYER')
        two_player_message = Words_And_Phrases(190,260,'2PLAYER')

        ## setting up the select asterisk
        asterisk = Words_And_Phrases(170,220,'*')

        ## setting up the important credit message
        credit_message = Words_And_Phrases(340,456,'CREDIT 00')

        ## setting up the flag variable to begin the game
        Player_Selected = False

        ## setting up the mode variable
        flag_game_mode = 'one_player'
        
        ## setting up the player's score and the high score
        score_message = Words_And_Phrases(45,20,'SCORE<1> HI-SCORE SCORE<2>')
        player_1_score = Words_And_Phrases(60,60,[0,0,0,0])
        player_2_score = Words_And_Phrases(320,60,[0,0,0,0])
        high_score = Words_And_Phrases(200,60,[0,0,0,0])

        while True:
            screen.fill(black)

            ## drawing the player's score
            score_message.Draw()
            player_1_score.Draw()
            player_2_score.Draw()
            high_score.Draw()
            credit_message.Draw()

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
                        ## changing the asterik's position resetting the game mode
                        asterisk.ypos = 260
                        flag_game_mode = 'two_player'

                    elif event.key == K_UP:
                        ## changing the asterik's position resetting the game mode
                        asterisk.ypos = 220
                        flag_game_mode = 'one_player'

                    elif event.key == K_RETURN:
                        Player_Selected = True

            pygame.display.update()
            clock.tick(60)
            if Player_Selected == True:
                break

## setting up the menu 2
        ## flag skip variable
        flag_skip = False

        ## emptying the screen
        screen.fill(black)
        
        # drawing the player's score and high score
        score_message.Draw()
        player_1_score.Draw()
        player_2_score.Draw()
        high_score.Draw()
        credit_message.Draw()

        # setting up and drawing the words and messages
        play_message = Words_And_Phrases(210,150,'PLA')
        play_message.Draw(6)

        y_message = Words_And_Phrases(255,150,['yflip'])
        y_message.Draw(6)

        space_invaders_message = Words_And_Phrases(135,190,'SPACE INVADERS')
        space_invaders_message.Draw(6)

        Pause(0.5)

        ## drawing the score_advance_table
        score_advance_table = Words_And_Phrases(80,250,'*SCORE ADVANCE TABLE*')
        score_advance_table.Draw()

        ## drawing the alien display only if the player hasn't skipped
        if flag_skip == False:
            mystery_ship_display = Mystery_Ship(144,285)
            mystery_ship_display.Draw()
                
            alien_3_display = Alien(153,320,3)
            alien_3_display.Draw('white')

            alien_1_display = Alien(150,355,1)
            alien_1_display.Draw('white')

            alien_2_display = Alien(150,390,2)
            alien_2_display.Draw('white')

        ## drawing the alien values
        mystery_point_message = Words_And_Phrases(180,285,'=? MYSTERY')
        mystery_point_message.Draw(6)
        
        thirty_points_message = Words_And_Phrases(180,320,'=30 POINTS')
        thirty_points_message.Draw(6)

        twenty_points_message = Words_And_Phrases(180,355,'=20 POINTS')
        twenty_points_message.Draw(6)

        ten_points_message = Words_And_Phrases(180,390,'=10 POINTS')
        ten_points_message.Draw(6)

    ## setting up the short alien film

        # making the alien
        start_alien = Alien(605,149,3)
        start_alien.Speed = -5

        ## moving the alien towards the letter to take it
        while True:

            ## checking if the player decides to skip and the break the loop if that happens
            Close_Or_Skip()
            if flag_skip == True or flag_skip == 'stage_2':
                if flag_skip == True:
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

                pygame.display.update()
                clock.tick(30)
                break

            pygame.display.update()
            clock.tick(30)

        ## moving the alien away from the letter to take it away
        while True:

            ## checking if the player decides to skip and breaking the loop if the skip variable is true
            Close_Or_Skip()
            if flag_skip == True or flag_skip == 'stage_2':
                if flag_skip == True:
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

                pygame.display.update()
                clock.tick(30)
                break

            pygame.display.update()
            clock.tick(30)

        ## moving the alien towards the letter to replace it
        while True:
            ## checking if the player decides to skip and breaking the loop if the skip variable is true
            Close_Or_Skip()
            if flag_skip == True or flag_skip == 'stage_2':
                if flag_skip == True:
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
                y_message = Words_And_Phrases(255,150,'Y')

                ## changing the alien speed
                start_alien.Speed = 5

                pygame.display.update()
                clock.tick(30)
                break

            ## moving the alien
            start_alien.Move_Alien()

            pygame.display.update()
            clock.tick(30)
        
        ## moving the alien away from the letter
        while True:

            ## breaking the loop if the skip variable is true
            Close_Or_Skip()
            if flag_skip == True or flag_skip == 'stage_2':
                if flag_skip == True:
                    Fill_Black()
                break

            ## drawing the words
            pygame.draw.rect(screen,black,(0,150,480,15))
            play_message.Draw()
            y_message.Draw()

            ## drawing the alien
            start_alien.Move_Alien()
            start_alien.Draw()

            ## checking if the alien reaches the cordinate of 600 and ending the loop
            if start_alien.xpos == 600:
                pygame.display.update()
                clock.tick(30)
                break

            pygame.display.update()
            clock.tick(30)

        ## deleting the start alien from no use
        del start_alien

    ## checking if the player hasn't skipped and setting up the menu 3 and menu 4
        if flag_skip == False:

        ## setting up the menu 3

            ## filling the screen black quickly but not directly
            Fill_Black()

            ## drawing the scores
            score_message.Draw()
            player_1_score.Draw()
            player_2_score.Draw()
            high_score.Draw()
            credit_message.Draw()

            ## drawing the buttons
            push_message = Words_And_Phrases(210,180,'PUSH')
            push_message.Draw()

            ## drawing the message describing the one player buttons used
            if flag_game_mode == 'one_player':
                only_one_player_button_message = Words_And_Phrases(90,230,'ONLY 1 PLAYER BUTTON')
                only_one_player_button_message.Draw()

            ## drawing the message describing the two player buttons used
            elif flag_game_mode == 'two_player':
                only_two_player_button_message = Words_And_Phrases(127,230,'2 PLAYER BUTTON')
                only_two_player_button_message.Draw()
            
            ## updating the screen only without the flagskip variable
            pygame.display.update()
            Pause(2)

        ## setting up menu 4
            ## filling the screen black quickly but not directly
            Fill_Black()

            for time in range(1,30):
                screen.fill(black)

                ## checking if the player decides to skip and breaking from the for loop if it happened
                Close_Or_Skip()
                if flag_skip == True or flag_skip == 'stage_2':
                    if flag_skip == True:
                        Fill_Black()
                    break

                if flag_game_mode == 'one_player':
                    ## drawing the play player 1 message and blinking the player 1 score
                    play_one_player_message = Words_And_Phrases(135,180,'PLAY PLAYER<1>')
                    play_one_player_message.Draw()
                    if time%2 == 0:
                        player_1_score.Draw()

                if flag_game_mode == 'two_player':
                    ## drawing the play player 2 message and blinking the player 1 and the player 2 score 
                    play_two_player_message = Words_And_Phrases(135,220,'PLAY PLAYER<2>')
                    play_two_player_message.Draw()
                    if time%2 == 0:
                        player_2_score.Draw()
                        player_1_score.Draw()
                else:
                    player_2_score.Draw()

                ## drawing the rest of the score info and the credit message
                score_message.Draw()
                high_score.Draw()
                credit_message.Draw()

                pygame.display.update()
                clock.tick(15)

        ## ending the flag skip
        flag_skip = 'done'

        ## changing the credit's xpos if the player mode is 2 player
        if flag_game_mode == 'two_player':
            credit_message.xpos = 173

## setting up the elements
        ## setting up the Gameover Flag Variable
        flag_gameover = False

        ## setting up the player, their backup, and their live 
        player_1 = None
        player_2 = None
        player_1_backup = []
        Player_2_Backup = []
        player_1_life = Words_And_Phrases(10,456,[])
        player_2.lives = Words_And_Phrases(460,456,[])

        if flag_game_mode == 'one_player' or flag_game_mode == 'two_player':
            player_1 = Player(50,400)
            player_1_backup = [Player(30,450),Player(70,450)]
            player_1_life.phrase = [2]
        if flag_game_mode == 'two_player':
            player_2 = Player(90,400)
            Player_2_Backup = [Player(420,450),Player(380,450)]
            player_2.lives.phrase = [2]
            
        alien_list = []
        Fill_Alien(True)

        ## alien attributes
        alien_explosion_list = []

        ## setting up the Mystery_Ship
        mystery_ship = Mystery_Ship(2500,90)
        mystery_ship_explosion_list = []
        
        ## setting up the Barrier layout
        barrier_layout = [[0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
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
        barrier1 = []
        barrier2 = []
        barrier3 = []
        barrier4 = []
        alien_invasion_line = []
        Barrier_Refill()

        ## setting up the bullet lists
        player_1.Bullet_List = []
        Player_2_Bullets = []
        Alien_Bullets = []
        bullet_explosion_list = []
        
    # setting up the screen
        Fill_Black()
        Screen_Draw(True)

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

        ## moving alien_list and changing animations only if there is at least one alien on the screen
            if len(alien_explosion_list) == 0:
                Alien.Timer = Alien.Timer - 1
                if  Alien.Timer <= 0:
                    Alien.Timer = 2
                    if Alien.Flag_Down_Step == True:
                        for i in range(len(alien_list[Alien.Counter_Movement])):
                            alien_list[Alien.Counter_Movement][i].Move_Down()
                            alien_list[Alien.Counter_Movement][i].Shoot()
                            alien_list[Alien.Counter_Movement][i].Check()
                    for i in range(len(alien_list[Alien.Counter_Movement])):
                        alien_list[Alien.Counter_Movement][i].Move_Alien()
                        alien_list[Alien.Counter_Movement][i].Shoot()
                        alien_list[Alien.Counter_Movement][i].Check()
                    Alien.Counter_Movement = Alien.Counter_Movement + 1

        ## checking if all the alien_list have moved
            if Alien.Counter_Movement == len(alien_list):
                Alien.Counter_Movement = 0

            ## stoping the alien_list from continously moving down
                if Alien.Flag_Collide_Side != None and Alien.Flag_Down_Step == True:
                    Alien.Flag_Down_Step = False
                    Alien.Flag_Collide_Side = None

            ## enabling the alien_list to move down
                if Alien.Flag_Collide_Side != None:
                    Alien.Flag_Down_Step = True
                
            ## playing the background music of the alien movement
                mixer.music.load(Game_Element.Basic_Sound_Url+'background sound '+str(Alien.Counter_Background_Sound)+'.wav')
                mixer.music.play()
                Alien.Counter_Background_Sound = Alien.Counter_Background_Sound + 1
                if Alien.Counter_Background_Sound == 5:
                    Alien.Counter_Background_Sound = 1

        ## moving the alien bullets
            alien_bullet_iteration_counter = 0
            while True:
                if alien_bullet_iteration_counter >= len(Alien_Bullets):
                    break
                Alien_Bullets_length = len(Alien_Bullets)
                Alien_Bullets[alien_bullet_iteration_counter].Move_Alien_Bullet()
                Alien_Bullets[alien_bullet_iteration_counter].Check()
                if len(Alien_Bullets) == Alien_Bullets_length:
                    alien_bullet_iteration_counter = alien_bullet_iteration_counter + 1

        ## moving the player bullets
            for bullet in player_1.Bullet_List:
                bullet.Move_Bullet()
                bullet.Check()
            for bullet in Player_2_Bullets:
                bullet.Move_Bullet()
                bullet.Check()

        ## updating the alien dead timer
            Alien_Explosion_Iteration_Counter = 0
            while True:
                if Alien_Explosion_Iteration_Counter == len(alien_explosion_list):
                    break
                Alien_Explosion_Length = len(alien_explosion_list)
                alien_explosion_list[Alien_Explosion_Iteration_Counter].Update_Timer()
                if Alien_Explosion_Length == len(alien_explosion_list):
                    Alien_Explosion_Iteration_Counter = Alien_Explosion_Iteration_Counter + 1
            
            Mystery_Ship_Explosion_Iteration_Counter = 0
            while True:
                if Mystery_Ship_Explosion_Iteration_Counter == len(mystery_ship_explosion_list):
                    break
                Mystery_Ship_Explosion_Length = len(mystery_ship_explosion_list)
                mystery_ship_explosion_list[Mystery_Ship_Explosion_Iteration_Counter].Update_Timer()
                if Mystery_Ship_Explosion_Length == len(mystery_ship_explosion_list):
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
                            if player_1.Shoot_Timer <= 0 and len(player_1.Bullet_List) == 0:
                                player_1.Shoot_Timer = 60
                                player_1.Shoot_Iteration_Counter = player_1.Shoot_Iteration_Counter + 1
                                player_1.Bullet_List.append(Player_Bullet(player_1.xpos + 14,player_1.ypos - 10))


                                ## playing the sound
                                Player.Shoot_Sound.play()
                        else:
                            if player_2.Shoot_Timer <= 0 and len(Player_2_Bullets) == 0:
                                player_2.Shoot_Iteration_Counter = player_2.Shoot_Iteration_Counter + 1
                                player_2.Shoot_Timer = 60
                                Player_2_Bullets.append(Player_Bullet(player_2.xpos + 14,player_2.ypos - 10))

                                ## playing the sound
                                Player.Shoot_Sound.play()

                ## shooting bullets using x
                    if event.key == K_x: 
                        if player_2 != None:
                            if player_2.Shoot_Timer <= 0 and len(Player_2_Bullets) == 0:
                                player_2.Shoot_Timer = 60
                                Player_2_Bullets.append(Player_Bullet(player_2.xpos + 14,player_2.ypos - 10))

                                ## playing the sound
                                Player.Shoot_Sound.play()
                        else:
                            if player_1.Shoot_Timer <= 0 and len(player_1.Bullet_List) == 0:
                                player_1.Shoot_Timer = 60
                                player_1.Bullet_List.append(Player_Bullet(player_1.xpos + 14,player_1.ypos - 10))

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
            for barrier_particle in alien_invasion_line:
                barrier_particle.Draw()

        ## drawing the score and the credits
            score_message.Draw()
            player_1_score.Draw()
            player_2_score.Draw()
            high_score.Draw()            
            player_1_life.Draw()
            player_2.lives.Draw()
            credit_message.Draw()
            
        ## drawing the player
            if player_1 != None:
                player_1.Draw('green')
            if player_2 != None:
                player_2.Draw('blue')
            for player in player_1_backup:
                player.Draw('green')
            for player in Player_2_Backup:
                player.Draw('blue')
            
        ## drawing the Barriers
            for barrier_particle in barrier1:
                barrier_particle.Draw()
            for barrier_particle in barrier2:
                barrier_particle.Draw()
            for barrier_particle in barrier3:
                barrier_particle.Draw()
            for barrier_particle in barrier4:
                barrier_particle.Draw()
                
        ## drawing the Mystery_Ship
            mystery_ship.Draw()

        ## drawing the alien_list
            for group in alien_list:
                for alien in group:
                    if alien.ypos >= 315:
                        alien.Draw('green')
                    else:
                        alien.Draw('white')

        ## drawing the Alien_Explosion and Mystery Ship Explosion
            for explosion in alien_explosion_list:
                explosion.Draw()
            for explosion in mystery_ship_explosion_list:
                explosion.Draw()
                
        ## drawing the player bullet with the specific color
            for bullet in player_1.Bullet_List:
                if flag_game_mode == 'two_player':
                    bullet.Draw('green')
                else:
                    bullet.Draw('white')
            for bullet in Player_2_Bullets:
                bullet.Draw('blue')
            
        ## drawing the alien bullets;
            for bullet in Alien_Bullets:
                bullet.Draw()

        ## updating the player bullet timer
            if Player.Shoot_Timer > 0:
                Player.Shoot_Timer = Player.Shoot_Timer - 1
                
        ##drawing the explosion caused by the player and alien bullets
            bullet_explosion_Iteration_Counter = 0
            while True:
                if bullet_explosion_Iteration_Counter == len(bullet_explosion_list):
                    break
                bullet_explosion_list[bullet_explosion_Iteration_Counter].Draw()
                bullet_explosion_list[bullet_explosion_Iteration_Counter].Explosion_Timer = bullet_explosion_list[bullet_explosion_Iteration_Counter].Explosion_Timer - 1
                if bullet_explosion_list[bullet_explosion_Iteration_Counter].Explosion_Timer == 0:
                    bullet_explosion_list.pop(bullet_explosion_Iteration_Counter)
                else:
                    bullet_explosion_Iteration_Counter = bullet_explosion_Iteration_Counter + 1

        ## updating the window
            pygame.display.update()
            clock.tick(60)

            ## checking if all the alien_list are shot
            if len(alien_list) == 0 and len(alien_explosion_list) == 0:
                ## emptying all the bullet lists
                Alien_Bullets = []
                player_1.Bullet_List = []
                Player_2_Bullets = []

                ## changing the alien's counter ypos because they move farther downward as each level passes
                Alien.Counter_Position = Alien.Counter_Position + 1
                if Alien.Counter_Position == 10:
                    Alien.Counter_Position = 0

                ## making the players stop and resetting the player's xpos 
                if player_1 != None:
                    player_1.Flag_Movement_Direction = None
                elif player_2 != None:
                    player_2.Flag_Movement_Direction = None

                ## Refilling alien_list and Barriers
                Fill_Alien()
                Barrier_Refill()

                ## drawing the elements 
                Screen_Draw()

        ## checking if the players are hit
            if player_1 != None:
                if player_1.Flag_Struck == True:
                    Player_Explode(player_1)

            if player_2 != None:
                if player_2.Flag_Struck == True:
                    Player_Explode(player_2)

        ## ending the game
            if flag_gameover == True:
                ## drawing the Game Over Sign
                game_over_message = Words_And_Phrases(180,120,'GAMEOVER')
                game_over_message.Draw()
                pygame.display.update()
                Pause(2)
                break
MainGame()