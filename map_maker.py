import random

MAP_SIZE = (200, 180)

map_file = open('map.js', 'w')

line = '    /*            '
for x in range(MAP_SIZE[0]):
    line += '%03d,          ' % x
map_file.write(line)
map_file.write(' */\n');

map_file.write("	var map = [ ");

for y in range(MAP_SIZE[1]):
    line = ''
    for x in range(MAP_SIZE[0]):
        r = random.randint(0, 1000)
        if r > 990:
            line += ' [0, 9],      '
        elif r > 950:
            line += '  4,          '
        else:
            line += '  0,          '
    map_file.write(line)
    map_file.write('\n    /*%03d*/        ' % (y+1))

map_file.write("			];")
map_file.close()