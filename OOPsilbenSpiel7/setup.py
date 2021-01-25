import pygame as pg
import sys, time, random
from pygame.locals import *
import linecache
from wiktionary_de_parser import Parser
import parsewikt3
import numpy



black = (0,0,0)
white = (255,255,255)
zuff = (200,200,200)
lila = (125,33,200)
clock = pg.time.Clock()
fps = 60
things_on_screen = []
pause = False
screenw, screenh = 500,500
right = screenw//6
down = screenh//12

#pg.init()


# global font
screen = pg.display.set_mode((screenh,screenw))
screen.fill(white)
#font = pg.font.SysFont("Arial",30)

def screen_update_and_move(allsyls,current_syl,player): # after every changed object
    screen.fill(zuff)
    for syl in range(current_syl):
        surface = allsyls[syl]
        screen.blit(surface.image,surface.rect) #draw function?
        surface.rect.y += surface.speed
    screen.blit(player.image,player.rect)
    pg.display.flip()


file_path = '/Users/ellie/Downloads/dewiktionary-20210101-pages-articles-multistream-2.xml'

def get_bank():
    bank = parsewikt3.quick_get(30)
    print(bank)
    return bank

# def get_bank():
#     listesilben = []
#     listdef = []
#     for record in Parser(file_path):
#         #if record.has_key('syllables'): # has_key was removed from py3
#         if 'syllables' in record:
#             #print(record['wikitext'])
#             listesilben.append(record['syllables'])
#             text1 = record["wikitext"].replace("{{","")
#             text1 = text1.replace("}}","")
#             text1 = text1.replace("[[","")
#             text1 = text1.replace("]]","")
#             text1 = text1.split("\n\n")
#             print(text1)
#             for i in range(len(text1)):
#                 lines = text1[i].split('\n')
#                 for line in lines:
#                     print(line)
#                     if line[0] == "Bedeutungen":
#                        listdef.append(line[0])
#         if len(listesilben) == 1000:
#              break
#     print(listdef)
#     return random.sample(listesilben,200) # 200 random ones

