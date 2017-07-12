from imageMaker.PropImage import PropImage

''' 
a collection of prop images. used to be in main, but main was getting cluttered
'''

#print('$1:', '\tsize =',$1.size, '\tcolors =',len($1.colors))
FOLDER = './Images/'

#credits background
#Image preferably 516 x 256
wallpaper_temp = PropImage(FOLDER+'wallpaper_temp.png')
print('wallpaper_temp:', '\tsize =',wallpaper_temp.size, '\tcolors =',len(wallpaper_temp.colors))

#man
dustman = PropImage(FOLDER+'dustman.png')
print('dustman:', '\t\tsize =',dustman.size, '\tcolors =',len(dustman.colors))

#sprite
leafsprite = PropImage(FOLDER+'leafsprite.png')
print('leafsprite:', '\tsize =',leafsprite.size, '\tcolors =',len(leafsprite.colors))

#girl
dustgirl = PropImage(FOLDER+'dustgirl.png')
print('dustgirl:', '\t\tsize =',dustgirl.size, '\tcolors =',len(dustgirl.colors))

#wraith
dustwraith = PropImage(FOLDER+'dustwraith.png')
print('dustwraith:', '\tsize =',dustwraith.size, '\tcolors =',len(dustwraith.colors))

#shovel
shovel_knight = PropImage(FOLDER+'shovel.png')
print('shovel_knight:', '\tsize =',shovel_knight.size, '\tcolors =',len(shovel_knight.colors))

#kirby
kirby = PropImage(FOLDER+'kirby_suck.png')
print('kirby:', '\t\t\tsize =',kirby.size, '\tcolors =',len(kirby.colors))

#mario
mario = PropImage(FOLDER+'mario.png')
print('mario:', '\t\t\tsize =',mario.size, '\tcolors =',len(mario.colors))

#sonic
sonic = PropImage(FOLDER+'sonic.png', transparency=(0,255,0))
print('sonic:', '\t\t\tsize =',sonic.size, '\tcolors =',len(sonic.colors))

#liliac
liliac = PropImage(FOLDER+'liliac.png', transparency=(0,255,0))
print('liliac:', '\t\tsize =',liliac.size, '\tcolors =',len(liliac.colors))

#megaman
megaman = PropImage(FOLDER+'megamanx.png', transparency=(0,255,0))
print('megaman:', '\t\tsize =',megaman.size, '\tcolors =',len(megaman.colors))

#link
link = PropImage(FOLDER+'link.png', transparency=(12,255,0))
print('link:', '\t\t\tsize =',link.size, '\tcolors =',len(link.colors))

#fez
fez = PropImage(FOLDER+'fez.png', transparency=(0,255,0))
print('fez:', '\t\t\tsize =',fez.size, '\tcolors =',len(fez.colors))

#metroid
metroid = PropImage(FOLDER+'metroid.png', transparency=(0,0,0))
print('metroid:', '\t\tsize =',metroid.size, '\tcolors =',len(metroid.colors))

#vines
vines = PropImage(FOLDER+'vines.png', transparency=(255,255,255))
print('vines:', '\t\t\tsize =',vines.size, '\tcolors =',len(vines.colors))

#wide_cloud
wide_cloud = PropImage(FOLDER+'cloud3.png', transparency=(0,0,0))
print('wide_cloud:', '\tsize =',wide_cloud.size, '\tcolors =',len(wide_cloud.colors))

#small_cloud
small_cloud = PropImage(FOLDER+'cloud2.png', transparency=(0,0,0))
print('small_cloud:', '\tsize =',small_cloud.size, '\tcolors =',len(small_cloud.colors))

#big_cloud
big_cloud = PropImage(FOLDER+'cloud1.png', transparency=(0,0,0))
print('big_cloud:', '\t\tsize =',big_cloud.size, '\tcolors =',len(big_cloud.colors))

#dark_pine
dark_pine = PropImage(FOLDER+'tree3.png', transparency=(0,0,0))
print('dark_pine:', '\t\tsize =',dark_pine.size, '\tcolors =',len(dark_pine.colors))

#oak
oak = PropImage(FOLDER+'tree2.png', transparency=(0,0,0))
print('oak:', '\t\t\tsize =',oak.size, '\tcolors =',len(oak.colors))

#light_pine
light_pine = PropImage(FOLDER+'tree1.png', transparency=(0,0,0))
print('light_pine:', '\tsize =',light_pine.size, '\tcolors =',len(light_pine.colors))

#islands
islands = PropImage(FOLDER+'background.png', transparency=(255,255,255))
print('islands:', '\t\tsize =',islands.size, '\tcolors =',len(islands.colors))

foreground_mario = PropImage(FOLDER+'foreground_mario.png', transparency=(0,0,255))
print('front_mario:', '\t\tsize =',foreground_mario.size, '\tcolors =',len(foreground_mario.colors))

background_mario = PropImage(FOLDER+'background_mario.png', transparency=(0,0,255))
print('back_mario:', '\t\tsize =',background_mario.size, '\tcolors =',len(background_mario.colors))

font = PropImage(FOLDER+'font.png', transparency=(255,255,255))
print('font:', '\t\tsize =',font.size, '\tcolors =',len(font.colors))