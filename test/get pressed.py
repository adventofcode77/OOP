import pygame, time
from pygame import *

pygame.init()

def main():
    screen = pygame.display.set_mode((500,500))
    screen.fill((0,0,0))
    player = pygame.Rect(200,200,50,50)
    font = pygame.font.SysFont("Arial",30)
    text_surface = font.render("player",False,(255,255,255))
    clock = pygame.time.Clock()
    step = 5

    while True:
        event.pump()
        #ohne event.pump() oder for event in pygame.event.get():
        # if event.type == pygame.QUIT:
        # exit()
        # hat die nächste linie keys = key.get_pressed() nicht funktioniert

        keys = key.get_pressed()
        # ich glaube, dass definiert keys als alle tasten, die im moment gedrückt werden

        if keys[pygame.K_LEFT]: # wenn die liste von im moment gedrückten tasten die LEFT taste hat
            print("left")
            print(player.x)
            player.x -= step

        screen.blit(text_surface,player)
        pygame.display.update()

main()

if __name__ == '__main__':
     main()
