import pygame
import sys
import os
from constants import *
pygame.font.init()

MENUFONT = '8-BIT_WONDER.TTF'
ARROWS = pygame.transform.scale(pygame.image.load(os.path.join('pics/arrows.png')), (100, 200))

# For the Menu we have used a doubly linked list in order to move through the different tabs on the menu
# With this method, the time complexity of selecting and moving through the selected element on the list is O(1)

class Node:
    def __init__(self, value): # Time complexity: O(1)
        self.value = value
        self.next = None
        self.prev = None
    
class DoublyLinkedList:
    def __init__(self, value):
        self.start_node = Node(value)

    def append(self, value): # Time complexity: O(n). Worst case: O(n). This function traverses the linked list to the point of insertion (end of the list) and then inserts it 
        current = self.start_node
        while current.next is not None:
            current = current.next
        new_node = Node(value)
        current.next = new_node
        new_node.prev = current

    def print_list(self): # Time complexity: O(n). Worst case: O(n). This function was only used for testing. It prints all the values from the linked list.
        current = self.start_node
        while current is not None:
            print(current.value)
            current = current.next


class Menu():
    def __init__(self, win): # Time complexity: O(n). Worst case: O(n). Function to initialize the menu. It creates linked list with n elements
        self.window = win
        # Create linked list with the different menu options
        self.dlist = DoublyLinkedList("START GAME")
        self.dlist.append("DIFFICULTY") 
        self.dlist.append("CREDITS")
        self.dlist.append("QUIT")
        self.node = self.dlist.start_node # Set currrent node to the starting node ("Start Game")

    def draw_menu(self): # Time complexity: O(1). This function draws the menu
        self.window.fill(black)
        self.draw_text(self.node.value, 40, width / 2, height / 2 - 20) # Call draw_text() sending the current node.value 

    def draw_text(self, text, size, x, y ): # Time complexity: O(1). Worst case: O(1). This function draws the text of the menu
        font = pygame.font.Font(MENUFONT,60)
        font2 = pygame.font.Font(MENUFONT,size)
        font3 = pygame.font.Font(MENUFONT,20)
        self.window.blit(font.render("MAIN MENU", True, white), (150,150))
        self.window.blit(font3.render("UP / DOWN / ENTER / BACKSPACE", True, white), (150,600))
        line2 = font2.render(text, True, white) # render the text sent to the function
        text_rect = line2.get_rect()
        text_rect.center = (x,y) # Set center of the rect around the text so that it centers the text no matter its length
        self.window.blit(ARROWS, (x-50, y-100))
        self.window.blit(line2,text_rect)
        

    def check_events(self): # Time complexity: O(1). Worst case: O(n) This function checks for n events that happen within the FPS rate
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return self.node.value    
                if event.key == pygame.K_BACKSPACE:
                    return "BACK"
                if event.key == pygame.K_DOWN:
                    if self.node.next != None:
                        self.node = self.node.next
                if event.key == pygame.K_UP:
                    if self.node.prev != None:
                        self.node = self.node.prev

    def draw_credits(self): # Time complexity: O(1). Worst case: O(1). This function draws the credits
        self.window.fill(black)
        font = pygame.font.Font(MENUFONT,40)
        font2 = pygame.font.Font(MENUFONT,30)
        font3 = pygame.font.Font(MENUFONT,20)

        self.window.blit(font3.render("BACKSPACE", True, white), (20, 20))
        self.window.blit(font.render("Credits", True, white), (270, height/2 - 160))
        self.window.blit(font2.render("Made by", True, white), (300, height/2 - 40))
        self.window.blit(font3.render("Diego Sanmartin", True, white), (260, height/2 + 20))
        self.window.blit(font3.render("Tomas Vintimilla", True, white), (250, height/2 + 60))
        self.window.blit(font3.render("Saad Sahir", True, white), (320, height/2 + 100))
        self.window.blit(font3.render("Carlo Pastor", True, white), (290, height/2 + 140))

    def draw_difficulty(self, current): # Time complexity: O(1). Worst case: O(1). This function draws the difficulty menu
        self.window.fill(black)
        font = pygame.font.Font(MENUFONT,40)
        font2 = pygame.font.Font(MENUFONT,30)
        font3 = pygame.font.Font(MENUFONT,20)
        self.window.blit(font.render("GAME DIFFICULTY", True, white), (150,150))
        self.window.blit(ARROWS, (width/2-50, height/2-100))
        self.window.blit(font2.render(str(current), True, white), (width/2 -10, height/2 - 15))
        if current >= 5:
            self.window.blit(font3.render("Careful The higher the level", True, white), (150, 600))
            self.window.blit(font3.render("the slower the cpu will play", True, white), (150, 640))

    def check_events_difficulty(self, initial_level, current_level):  # Time complexity: O(1). Worst case: O(n) This function checks for n events that happen within the FPS rate
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    current_level += 100    
                if event.key == pygame.K_BACKSPACE: 
                    current_level = initial_level + 100
                if event.key == pygame.K_DOWN:
                    if current_level > 1:
                        current_level -= 1
                if event.key == pygame.K_UP:
                    if current_level < 9:
                        current_level += 1
        return current_level

    def draw_winner(self, winner, difficulty_level): # Time complexity: O(1). Worst case: O(1). This function draws the winner screen
        self.window.fill(black)
        font = pygame.font.Font(MENUFONT,60)
        font2 = pygame.font.Font(MENUFONT,40)
        self.window.blit(font.render("GAME OVER", True, white), (150,150))
        if winner == "white":
            line2 = font2.render("You were beaten", True, white)
            line3 = font2.render("By CPU level " + str(difficulty_level), True, white)
        else:
            line2 = font2.render("You defeated", True, white)
            line3 = font2.render("CPU level " + str(difficulty_level), True, white)        
        text_rect = line2.get_rect()
        text_rect.center = (width / 2, height / 2 - 20)
        self.window.blit(line2,text_rect)
        text_rect3 = line3.get_rect()
        text_rect3.center = (width / 2, height / 2 + 60)
        self.window.blit(line3,text_rect3)

