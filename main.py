import os
import calculate
import rangefinder

__author__ = "Shubbe Leontij"
__license__ = "GPL"
__version__ = "0.0.1"
__email__ = "leontij03@yandex.ru"

K = 5600
COLOR = '255, 255, 0, 255'
SIZE = 1  # TODO

# Requesting all requirements
filename = input('Output filename: ')  # SimJagdpanther or SimLeo
speed = int(input('Shell speed in m/s: '))  # 1000 or 1640
coord = list(map(float, input('50m coordinates: ').split()))  # 10.175 10 or -14.85 3.90
left = True if coord[0] > 0 else False
speed_type = 1 if speed < 1200 else 2


def point(distance, base=50):
    parallax_x, parallax_y = coord[0] * (1 / distance - 1 / 1000) / (1 / base - 1 / 1000), coord[1] * (1 / distance - 1 / 1000) / (1 / base - 1 / 1000)
    gravity = K * (distance - base) / speed ** 2
    return str(round(parallax_x, 2)) + ', ' + str(round(parallax_y + gravity, 2))


def circle(distance, size):
    return 'circle {\nsegment:p2 = 0, 360;\npos:p2 = ' + point(distance) + ';\ndiameter:r = 0;\nsize:r = ' + str(size) + ';\nmove:b = yes\nthousandth:b = yes;\n}\n'


def text(distance, delta, size):
    x, y = tuple(map(float, point(distance).split(', ')))
    x = x + delta[0]
    y = y + delta[1]
    return 'text\n{\ntext: t = "' + (str(distance) if distance < 100 else str(distance//100)) + '"\nalign: i = 0\npos: p2 = ' + \
           str(round(x, 2)) + ', ' + str(round(y, 2)) + '\nmove: b = yes\nthousandth: b = yes\nsize: r = ' + str(size) + '\nhighlight: b = yes\n}\n'


default_dist_list = [20, 35, 50, 100, 200, 400]
if speed_type == 1:
    large_dist_list = [600, 1000, 1400, 1800, 2200, 2600, 3000]
    small_dist_list = [800, 1200, 1600, 2000, 2400, 2800]
elif speed_type == 2:
    large_dist_list = [600, 1400, 2200, 3000]
    small_dist_list = [1000, 1800, 2600]
else:
    raise Exception

# Start settings
with open('start.blk') as f:
    output = f.read() + COLOR + '\n'


# Lines
points = [point(5)]
output += 'crosshair_distances {\n}\n\ndrawLines{\n'
output += 'line{\nline:p4= -0.7, 0, -2, 0\nmove:b=no\nthousandth:b=yes\n}\nline{\nline:p4= 0.7, 0, 2, 0\nmove:b=no\nthousandth:b=yes\n}\n'
for dist in [20, 35, 50] + list(range(100, 3200, 100)):
    points.append(point(dist))
    output += 'line\n{\nline: p4 = ' + points[-1] + ', ' + points[-2] + '\nmove: b = yes\nthousandth: b = yes\n}\n'
output += rangefinder.left_line if left else rangefinder.right_line
output += '}\n\n'


# Circles
output += 'drawCircles{\ncircle {\nsegment:p2 = 0, 360;\npos:p2 = 0, 0;\ndiameter:r = 0;\nsize:r = 4;\nmove:b = no\nthousandth:b = yes;\n}\n'
output += circle(20, 8) + circle(35, 8) + circle(50, 6)
for dist in default_dist_list + large_dist_list:
    output += circle(dist, 4)
for dist in small_dist_list:
    output += circle(dist, 3.3)
output += '}\n\n'


# Text
output += 'drawTexts{\n'
output += text(20, [3 if left else -3, 0], 1.5) + text(35, [2.5 if left else -2.5, 0], 1.5) + text(50, [2 if left else -2, 0], 1)
output += text(100, [0, -1], 0.5) + text(200, [0, -1], 0.5) + text(400, [0, -1], 0.5)
for dist in large_dist_list:
    output += text(dist, [-1.5 if left else 1.5, 0], 0.6)
output += rangefinder.left_text if left else rangefinder.right_text
output += '}'


# Writing into file
path = os.path.dirname(os.path.realpath(__file__)) + '/output'
with open(path + '/' + filename + '.blk', 'w') as f:
    f.write(output)
    print("Successfully created sight at %s " % (path + '/' + filename + '.blk'))
