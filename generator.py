#!/usr/bin/env python3
import os
import json

__author__ = "Shubbe Leontij"
__version__ = "2.2"


def create_sight(path, speed, zoom, sight_type, coord, convergence, floppa_text=''):
    """
    Function that creates sight .blk file.
    :param path: path where sight should be created
    :param speed: shell speed in m/s (int type)
    :param zoom: minimum zoom (float type)
    :param sight_type: sight type according to settings.json
    :param coord: list with two floats inside - height and width location of sight relatively to the gun in meters
    :param convergence: convergence in meters i.e. distance with zero parallax (int type)
    """
    def get_rangefinder(zoom, side):
        """
        Function that returns text for adding rangefinder.
        :param zoom: zoom type - 'bad' or 'good'
        :param side: side where rangefinder should be painted - 'left' or 'right'
        :return: tuple with line str and text str
        """
        if zoom == 'bad':
            string = '$BadZoom'
            fontSize = rangefinderFontSizeMult * 0.70
        elif zoom == 'good':
            string = '$GoodZoom'
            fontSize = rangefinderFontSizeMult * 0.45
        else:
            raise ValueError

        if side == 'left':
            string += 'Left'
        elif side == 'right':
            string += 'Right'
        else:
            raise ValueError

        with open('rangefinder.txt', 'r') as f:
            rangefinder_str = f.read()
            line_str = rangefinder_str.partition(string + 'LineStart$')[2].partition(string + 'LineEnd$')[0]
            text_str = rangefinder_str.partition(string + 'TextStart$')[2].partition(string + 'TextEnd$')[0]

        return line_str, text_str.replace('$size$', str(round(fontSize, 2)))

    def point(distance):
        """
        Function that finds location of point on sight depending on distance.
        :param distance: int distance in meters
        :return: str with two parallaxes in milliradian splitted by ', '
        """
        parallax_x, parallax_y = - coord[1] * (1 / distance - 1 / convergence), coord[0] * (1 / distance - 1 / convergence)
        gravity = 5.0 * distance / speed ** 2
        return str(round(parallax_x * 1000, 2)) + ', ' + str(round((parallax_y + gravity) * 1000, 2))

    def crosshair_distance(distance, size, side):
        """
        Function that creates string for adding WT generated distances on sight.
        :param distance: int distance in meters
        :param size: big or small - int 1 or 0
        :return: str type generated text
        """
        x = str(distLength) if size else str(round(distLength * 2 / 3, 4))
        return 'distance { distance:p3=' + str(distance) + ',' + (str(distance // 100) if size else '0') + ',' + ('-' if side == 'right' else '') + x + '; textPos:p2=' + ('' if side == 'right' else '-') + '0.013,0; }\n'

    def circle(distance, size):
        """
        Function that creates circle marking some distance.
        :param distance: int distance in meters
        :param size: diameter of circle
        :return: str type generated text
        """
        return 'circle {    //' + str(distance) + '\nsegment:p2 = 0, 360;\npos:p2 = ' + point(distance) + ';\ndiameter:r = 0;\nsize:r = ' + str(size) + ';\nmove:b = yes\nthousandth:b = yes;\n}\n'

    def text(distance, delta, size):
        """
        Function that creates text marking some distance.
        :param distance: int distance in meters
        :param delta: list of text shift in milliradians relative to the circle - [horizontal, vertical]
        :param size: size of text
        :return: str type generated text
        """
        x, y = tuple(map(float, point(distance).split(', ')))
        x = x + delta[0]
        y = y + delta[1]
        return 'text\n{\ntext: t = "' + (str(distance) if distance < 100 else str(distance//100)) + '"\nalign: i = 0\npos: p2 = ' + \
               str(round(x, 2)) + ', ' + str(round(y, 2)) + '\nmove: b = yes\nthousandth: b = yes\nsize: r = ' + str(size) + '\nhighlight: b = yes\n}\n'

    def floppa_distance(distance, size):
        """
        Function that creates circle marking some distance.
        :param distance: int distance in meters
        :param size: diameter of circle
        :return: str type generated text
        """
        x, y = tuple(map(float, point(distance).split(', ')))
        return 'text\n{\ntext: t = "' + floppa_char + '"\nalign: i = 0\npos: p2 = ' + str(round(x, 2)) + ', ' + str(round(y, 2)) + '\nmove: b = yes\nthousandth: b = yes\nsize: r = ' + str(round(size, 2)) + '\nhighlight: b = yes\n}\n'

    # Loading settings from json
    settings = json.load(open('settings.json', 'r'))

    s_type = None
    for t in settings["sightTypes"]:
        if sight_type in t["names"]:
            s_type = t
            break
    line_dist_list = s_type["line_dist_list"]
    rangefinder = s_type["rangefinder"]
    right_dist_list = s_type["right_dist_list"]
    left_dist_list = s_type["left_dist_list"]
    small_dist_list = s_type["small_dist_list"]
    circles_list = s_type["circles"]
    centralLines = s_type["centralLines"]
    centralCircle = s_type["centralCircle"]

    badZoomThreshold = settings["badZoomThreshold"]
    distLength = settings["distLength"]
    crosshairColor = settings["crosshairColor"]
    crosshairLightColor = settings["crosshairLightColor"]
    rangefinderProgressBarColor1 = settings["rangefinderProgressBarColor1"]
    rangefinderProgressBarColor2 = settings["rangefinderProgressBarColor2"]
    drawCentralLineVert = settings["drawCentralLineVert"]
    drawCentralLineHorz = settings["drawCentralLineHorz"]
    fontSizeMult = max(settings["fontSizeMult"] * 0.2 * zoom, settings["minFontSize"])
    lineSizeMult = round(settings["lineSizeMult"] / settings["fontSizeMult"], 2)
    rangefinderFontSizeMult = round(1 / settings["fontSizeMult"], 2)

    floppa_char = settings["floppa_char"]
    floppa_char_size = settings["floppa_char_size"]
    bigFloppa = True if floppa_text else False
    isLeft = True if coord[1] < 0 else False
    distancePos = str(round(float(point(2000).split(',')[0]) * -0.01, 4))

    distances_blk = '\ncrosshair_distances{\n'
    circles_blk = '\ndrawCircles{\n'
    lines_blk = '\ndrawLines{\n'
    text_blk = '\ndrawTexts{\n'

    # Load rangefinder depending on gamemode and zoom
    if rangefinder:
        rangefinder_lines, rangefinder_text = get_rangefinder('good' if zoom > badZoomThreshold else 'bad', 'left' if isLeft else 'right')
    else:
        rangefinder_lines, rangefinder_text = '', ''

    # Start settings
    with open('start.txt', 'r') as f:
        output = f.read()
        output = output.replace('$crosshairColor$', crosshairColor)
        output = output.replace('$crosshairLightColor$', crosshairLightColor)
        output = output.replace('$rangefinderProgressBarColor1$', rangefinderProgressBarColor1)
        output = output.replace('$rangefinderProgressBarColor2$', rangefinderProgressBarColor2)
        output = output.replace('$drawCentralLineVert$', drawCentralLineVert)
        output = output.replace('$drawCentralLineHorz$', drawCentralLineHorz)
        output = output.replace('$fontSizeMult$', str(round(fontSizeMult, 2)))
        output = output.replace('$lineSizeMult$', str(round(lineSizeMult, 2)))
        output = output.replace('$distancePos$', distancePos)

    # Distances
    if not bigFloppa:
        for dist in sorted(right_dist_list + left_dist_list + small_dist_list):
            if dist in right_dist_list:
                distances_blk += crosshair_distance(dist, 1, 'right' if isLeft else 'left')
            if dist in left_dist_list:
                distances_blk += crosshair_distance(dist, 1, 'left' if isLeft else 'right')
            if dist in small_dist_list:
                distances_blk += crosshair_distance(dist, 0, 'left' if isLeft else 'right')
    else:
        for dist in sorted(right_dist_list + left_dist_list + small_dist_list):
            if dist in right_dist_list:
                text_blk += floppa_distance(dist, floppa_char_size)
                text_blk += text(dist, [1 if isLeft else -1, 0], 0.8)
            if dist in left_dist_list:
                text_blk += floppa_distance(dist, floppa_char_size)
                text_blk += text(dist, [-1 if isLeft else 1, 0], 0.8)
            if dist in small_dist_list:
                text_blk += floppa_distance(dist, floppa_char_size)

    # Lines
    if not bigFloppa:
        lines_blk += centralLines
        if len(line_dist_list) > 1:
            points = [point(line_dist_list[0])]
            for dist in line_dist_list[1:]:
                points.append(point(dist))
                lines_blk += 'line    //to ' + str(dist) + '\n{\nline: p4 = ' + points[-1] + ', ' + points[-2] + '\nmove: b = yes\nthousandth: b = yes\n}\n'
    else:
        lines_blk += "line{\nline:p4= 0.0, 0.0, 0.0, 80.0\nmove:b=yes\nthousandth:b=yes\n}\nline{\nline:p4= -0.7, 0, -2, 0\nmove:b=no\nthousandth:b=yes\n}\nline{\nline:p4= 0.7, 0, 2, 0\nmove:b=no\nthousandth:b=yes\n}\n"
    lines_blk += rangefinder_lines
    lines_blk += floppa_text  # PAINTING FLOPPA

    # Circles
    if not bigFloppa:
        circles_blk += centralCircle + '\n'
        for dist in circles_list.keys():
            circles_blk += circle(int(dist), circles_list[dist]['size'])
    else:
        text_blk += '\ntext\n{\ntext: t = "' + floppa_char + '"\nalign: i = 0\npos: p2 = 0, 0\nmove: b = no\nthousandth: b = yes\nsize: r = ' + str(floppa_char_size) + '\nhighlight: b = yes\n}\n'
        for dist in circles_list.keys():
            text_blk += floppa_distance(int(dist), circles_list[dist]['size'] * 0.3)

    # Text
    for dist in circles_list.keys():
        textPos = circles_list[dist]['textPos']
        textPos[0] = textPos[0] if isLeft else -textPos[0]
        textSize = circles_list[dist]['textSize']
        if textSize:
            text_blk += text(int(dist), textPos, textSize)
    text_blk += rangefinder_text

    # Writing into file
    output += distances_blk + '}\n' + lines_blk + '}\n' + circles_blk + '}\n' + text_blk + '}\n'  # SUM ALL STRINGS INTO ONE
    try:
        os.mkdir(path)
    except:
        pass

    path = path + ('/F_' if bigFloppa else '/') + sight_type + '_' + path.rpartition('/')[2] + '.blk'
    with open(path, 'w') as f:
        f.write(output)
        if __name__ == '__main__':
            print("Successfully created sight at %s " % path)
        else:
            return "Successfully created sight at %s " % path


if __name__ == '__main__':
    # Requesting all requirements and creating sight in output
    try:
        path = os.path.dirname(os.path.realpath(__file__)) + '/UserSights/' + input('Tank name: ')
        speed = int(input('Shell speed in m/s: '))
        convergence = int(input('Convergence in meters: '))
        zoom = float(input('Zoom: '))
        sight_type = input('Sight type: ')
        coord = list(map(float, input('Sight coordinates: ').split(',')))
        FLOPPA = int(input('Big Floppa: '))
        if FLOPPA:
            with open('floppa.txt', 'r') as floppa_file:
                floppa_text = floppa_file.read()
        else:
            floppa_text = ''
        try:
            os.mkdir(os.path.dirname(os.path.realpath(__file__)) + '/UserSights/')
        except:
            pass
        create_sight(path, speed, zoom, sight_type, coord, convergence, floppa_text)
    except ValueError:
        print('Wrong format string')

    input("\nPress enter to exit")
