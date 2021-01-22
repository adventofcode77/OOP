import pygame as pg
import sys, time, random
from pygame.locals import *
import linecache
from wiktionary_de_parser import Parser
import numpy



black = (0,0,0)
white = (255,255,255)
zuff = (200,200,200)
lila = (125,33,200)
clock = pg.time.Clock()
fps = 60
things_on_screen = []
pause = False

#pg.init()


# global font
screen = pg.display.set_mode((500,500))
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
    listesilben = []
    for record in Parser(file_path):
        #if record.has_key('syllables'): # has_key was removed from py3
        if 'syllables' in record:
            #print(record['syllables'])
            listesilben.append(record['syllables'])
        if len(listesilben) == 1000:
             break
    return random.sample(listesilben,200) # 200 random ones

# array = get_bank()
# flat = list(numpy.concatenate(array).flat)
#
# def get_rects():
#         rects = []
#         for syl in flat:
#             x = random.randrange(50,450,50)
#             syl = silbe.Silbe(syl,x,0)
#             rects.append(syl)
#         return rects


# def update_screen(): #did not work
#         time.sleep(2)
#         pg.display.update()
#         screen.fill(white)


# filename = "parsed_dict"
# line_number = 1
# line = "kfgj"
# line = linecache.getline(filename, line_number)
# print ("line %i of %s:" % (line_number, filename))
# print (len(line))

# lines = ('lines_dict','w')
# listofdictlines = []
# filename = filename.readlines()
# for line in filename:
#     listofdictlines.append(line)
#     lines.write(line)
# filename.close()
