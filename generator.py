import os
import rangefinder

__author__ = "Shubbe Leontij"
__license__ = "GPL"
__version__ = "0.0.2"
__email__ = "leontij03@yandex.ru"


def create_sight(foldername, filename, speed, zoom, sight_type, coord):
    K = 5600  # DON'T TOUCH!!!
    COLOR = '255, 255, 0, 255'  # r, g, b, tr
    SIZE = zoom / 5  # Should be 1 if zoom == 5
    left = True if coord[0] > 0 else False

    default_circles_list = [20, 35, 50, 100, 200, 400, 600]
    if sight_type == 0:  # With Laser Rangefinder
        large_circles_list = []
        small_circles_list = []
        large_dist_list = []
        small_dist_list = []
    elif sight_type == 1:  # Circles AP
        large_circles_list = [1000, 1400, 1800, 2200, 2600, 3000]
        small_circles_list = [800, 1200, 1600, 2000, 2400, 2800]
        large_dist_list = []
        small_dist_list = []
    elif sight_type == 2:  # Circles APDS
        large_circles_list = [1400, 2200, 3000]
        small_circles_list = [1000, 1800, 2600]
        large_dist_list = []
        small_dist_list = []
    elif sight_type == 3:  # Distances AP
        large_circles_list = []
        small_circles_list = []
        large_dist_list = [1000, 1400, 1800, 2200, 2600, 3000]
        small_dist_list = [800, 1200, 1600, 2000, 2400, 2800]
    elif sight_type == 4:  # Distances APDS
        large_circles_list = []
        small_circles_list = []
        large_dist_list = [1400, 2200, 3000]
        small_dist_list = [1000, 1800, 2600]
    else:
        raise Exception
    all_dist_list = sorted(default_circles_list + large_circles_list + small_circles_list + large_dist_list + small_dist_list)

    def point(distance, base=50):
        parallax_x, parallax_y = coord[0] * (1 / distance - 1 / 1000) / (1 / base - 1 / 1000), coord[1] * (1 / distance - 1 / 1000) / (1 / base - 1 / 1000)
        gravity = K * (distance - base) / speed ** 2
        return str(round(parallax_x, 2)) + ', ' + str(round(parallax_y + gravity, 2))

    def crosshair_distance(distance, size):
        if size == 0:
            return 'distance:p3=' + str(distance) + ', 0, 0\n'
        if size == 1:
            return 'distance:p3=' + str(distance) + ', ' + str(distance // 100) + ', 0\n'

    def circle(distance, size):
        return 'circle {\nsegment:p2 = 0, 360;\npos:p2 = ' + point(distance) + ';\ndiameter:r = 0;\nsize:r = ' + str(size) + ';\nmove:b = yes\nthousandth:b = yes;\n}\n'

    def text(distance, delta, size):
        x, y = tuple(map(float, point(distance).split(', ')))
        x = x + delta[0]
        y = y + delta[1]
        return 'text\n{\ntext: t = "' + (str(distance) if distance < 100 else str(distance//100)) + '"\nalign: i = 0\npos: p2 = ' + \
               str(round(x, 2)) + ', ' + str(round(y, 2)) + '\nmove: b = yes\nthousandth: b = yes\nsize: r = ' + str(size) + '\nhighlight: b = yes\n}\n'

    # Start settings
    with open('start.blk') as f:
        output = f.read() + COLOR + '\n'
        index = output.find('\nlineSizeMult:r=1.0')
        output = output[:index] + str(round(SIZE, 2)) + output[index:]

    # Distances
    output += '\ncrosshair_distances {\n'
    for dist in sorted(large_dist_list + small_dist_list):
        if dist in large_dist_list:
            output += crosshair_distance(dist, 1)
        else:
            output += crosshair_distance(dist, 0)
    output += '}\n'

    # Lines
    points = [point(5)]
    output += '\ndrawLines{\n'
    output += 'line{\nline:p4= -0.7, 0, -2, 0\nmove:b=no\nthousandth:b=yes\n}\nline{\nline:p4= 0.7, 0, 2, 0\nmove:b=no\nthousandth:b=yes\n}\n'
    for dist in all_dist_list + [all_dist_list[-1] + 200]:
        points.append(point(dist))
        output += 'line\n{\nline: p4 = ' + points[-1] + ', ' + points[-2] + '\nmove: b = yes\nthousandth: b = yes\n}\n'
    output += rangefinder.left_line if left else rangefinder.right_line
    output += '}\n\n'

    # Circles
    output += 'drawCircles{\ncircle {\nsegment:p2 = 0, 360;\npos:p2 = 0, 0;\ndiameter:r = 0;\nsize:r = 4;\nmove:b = no\nthousandth:b = yes;\n}\n'
    for dist in default_circles_list + large_circles_list:
        output += circle(dist, 4)
    for dist in small_circles_list:
        output += circle(dist, 3.3)
    output += '}\n\n'

    # Text
    output += 'drawTexts{\n'
    output += text(20, [0, 1], 0.6) + text(35, [0, 1], 0.6) + text(50, [0, 1], 0.6) + \
              text(100, [0, -1], 0.6) + text(200, [0, -1], 0.6) + \
              text(400, [-0.5 if left else 0.5, -0.8], 0.6) + text(600, [-0.8 if left else 0.8, -0.5], 0.6)
    for dist in large_circles_list:
        output += text(dist, [-1.5 if left else 1.5, 0], 0.6)
    output += rangefinder.left_text if left else rangefinder.right_text
    output += '}'

    # Writing into file
    path = os.path.dirname(os.path.realpath(__file__)) + '\\output'
    if foldername != '':
        path += '\\' + foldername
        try:
            os.mkdir(path)
        except OSError:
            pass

    with open(path + '\\' + filename + '.blk', 'w') as f:
        f.write(output)
        print("Successfully created sight at %s " % (path + '\\' + filename + '.blk'))


if __name__ == '__main__':
    # Requesting all requirements
    foldername = ''
    filename = input('Output filename: ')  # SimJagdpanther or SimLeo
    speed = int(input('Shell speed in m/s: '))  # 1000 or 1640
    zoom = float(input('Zoom: '))  # 5 or 4
    sight_type = int(input('Sight type: '))
    coord = list(map(float, input('50m coordinates: ').split(',')))  # 10.175 10 or -14.85 3.90

    create_sight(foldername, filename, speed, zoom, sight_type, coord)
