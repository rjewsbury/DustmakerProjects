from dustmaker import *

filenames = {
    'newtutorial1':'Beginner-Tutorial-CCW-5863',
    'newtutorial2':'Combat-Tutorial-CCW-5862',
    'newtutorial3':'Advanced-Tutorial-CCW-5861',
    'downhill':'Downhill-CCW-5881',
    'shadedgrove':'Shaded-Grove-CCW-5883',
    'dahlia':'Dahlia-CCW-5882',
    'fields':'Fields-CCW-5857',
    'momentum':'Valley-CCW-5884',
    'fireflyforest':'Firefly-Forest-CCW-5895',
    'tunnels':'Tunnels-CCW-5880',
    'momentum2':'Dusk-Run-CCW-5887',
    'suntemple':'Overgrown-Temple-CCW-5888',
    'ascent':'Ascent-CCW-5885',
    'summit':'Summit-CCW-5886',
    'grasscave':'Grass-Cave-CCW-5850',
    'den':'Wild-Den-CCW-5896',
    'autumnforest':'Ruins-CCW-5897',
    'garden':'Ancient-Garden-CCW-5894',
    'hyperdifficult':'Night-Temple-CCW-5889',
    'atrium':'Atrium-CCW-5864',
    'secretpassage':'Secret-Passage-CCW-5865',
    'alcoves':'Alcoves-CCW-5866',
    'mezzanine':'Mezzanine-CCW-5867',
    'cave':'Caverns-CCW-5868',
    'cliffsidecaves':'Cliffside-Caves-CCW-5869',
    'library':'Library-CCW-5870',
    'courtyard':'Courtyard-CCW-5871',
    'precarious':'Archive-CCW-5872',
    'treasureroom':'Knight-Hall-CCW-5873',
    'arena':'Store-Room-CCW-5875',
    'ramparts':'Ramparts-CCW-5855',
    'moontemple':'Moon-Temple-CCW-5876',
    'observatory':'Observatory-CCW-5877',
    'parapets':'Ghost-Parapets-CCW-5878',
    'brimstone':'Tower-CCW-5879',
    'vacantlot':'Vacant-Lot-CCW-7997',
    'sprawl':'Landfill-CCW-7998',
    'development':'Development-CCW-7999',
    'abandoned':'Abandoned-Carpark-CCW-8001',
    'park':'Park-CCW-8002',
    'boxes':'Construction-Site-CCW-8003',
    'chemworld':'Apartments-CCW-8004',
    'factory':'Warehouse-CCW-8005',
    'tunnel':'Forgotten-Tunnel-CCW-5851',
    'basement':'Basement-CCW-8006',
    'scaffold':'Scaffolding-CCW-8007',
    'cityrun':'Rooftops-CCW-8008',
    'clocktower':'Clocktower-CCW-8009',
    'concretetemple':'Concrete-Temple-CCW-5852',
    'alley':'Alleyway-CCW-8010',
    'hideout':'Hideout-CCW-5853',
    'control':'Control-CCW-8016',
    'ferrofluid':'Ferrofluid-CCW-8017',
    'titan':'Titan-CCW-8018',
    'satellite':'Satellite-Debris-CCW-8019',
    'vat':'Vats-CCW-8020',
    'venom':'Server-Room-CCW-8021',
    'security':'Security-CCW-8022',
    'mary':'Research-CCW-8023',
    'wiringfixed':'Wiring-CCW-8024',
    'containment':'Containment-CCW-8025',
    'orb':'Power-Room-CCW-8027',
    'pod':'Access-CCW-8028',
    'mary2':'Backup-Shift-CCW-8029',
    'coretemple':'Core-Temple-CCW-5854',
    'abyss':'Abyss-CCW-8030',
    'dome':'Dome-CCW-8031',
    'kilodifficult':'Kilo-Difficult-CCW-8032',
    'megadifficult':'Mega-Difficult-CCW-8033',
    'gigadifficult':'Giga-Difficult-CCW-5856',
    'teradifficult':'Tera-Difficult-CCW-8034',
    'petadifficult':'Peta-Difficult-CCW-8035',
    'exadifficult':'Exa-Difficult-CCW-8036',
    'zettadifficult':'Zetta-Difficult-CCW-8037',
    'yottadifficult':'Yotta-Difficult-CCW-8038',
    'Main Nexus DX':'',
    'Nexus DX':'',
    'virtualnexus':'',
    'customnexus':'',
    'nexus_mp':''
}

f0 = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/user/level_src/virtualnexusCCW'
f1 = 'C:/Program Files (x86)/Steam/steamapps/common/Dustforce/content/levels2/customnexus'

with open(f0, "rb") as f:
   main_map = read_map(f.read())

for key in list(main_map.entities):
    entity = main_map.entities[key][2]
    #print(key, main_map.entities[key])
    # if entity.type == 'score_book':
    #     print(key, entity)
    # if entity.type == 'custom_score_book':
    #     print(key, entity)
    # if entity.type == 'z_string_list':
    #     print(key, entity)
    if entity.type is 'level_door':
        entity.vars['file_name'].value = filenames[entity.vars['file_name'].value]
    # if entity.type is 'camera_node':
    #     print(entity.vars['control_width'])

main_map.rotate(3)

main_map.name(main_map.name() + '_modified')
with open(f0 + "_modified", "wb") as f:
    f.write(write_map(main_map))
