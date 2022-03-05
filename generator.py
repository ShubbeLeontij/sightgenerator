import os
import json

__author__ = "Shubbe Leontij"
__license__ = "GPL"
__version__ = "1.4"
__email__ = "leontij03@yandex.ru"


def create_sight(path, speed, zoom, sight_type, coord, convergence):
    """
    Function that creates sight .blk file.
    :param path: path where sight should be created
    :param speed: shell speed in m/s (int type)
    :param zoom: minimum zoom (float type)
    :param sight_type: sight type according to settings.json
    :param coord: list with two floats inside - height and width location of sight relatively to the gun in meters
    :param convergence: convergence in meters i.e. distance with zero parallax (int type)
    """
    def point(distance):
        """
        Function that finds location of point on sight depending on distance.
        :param distance: int distance in meters
        :return: str with two parallaxes in milliradian splitted by ', '
        """
        if parallax:
            parallax_x, parallax_y = - coord[1] * (1 / distance - 1 / convergence), coord[0] * (1 / distance - 1 / convergence)
        else:
            parallax_x, parallax_y = 0, 0

        gravity = 5.0 * distance / speed ** 2
        return str(round(parallax_x * 1000, 2)) + ', ' + str(round((parallax_y + gravity) * 1000, 2))

    def crosshair_distance(distance, size, side):
        """
        Function that creates string for adding WT generated distances on sight.
        :param distance: int distance in meters
        :param size: big or small - int 1 or 0
        :return: str type generated text
        """
        x = '0.0065' if size else '0.0045'
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

    # Loading settings from json
    settings = json.load(open('settings.json', 'r'))

    line_dist_list = []
    right_circles_list = []
    left_circles_list = []
    small_circles_list = []
    right_dist_list = []
    left_dist_list = []
    small_dist_list = []
    sim_circles_list = settings["sim_circles_list"]
    s_type = settings["sightTypes"][sight_type]
    line_dist_list = s_type["line_dist_list"]
    rangefinder = s_type["rangefinder"]
    parallax = s_type["parallax"]
    if s_type["circles"]:
        right_circles_list = s_type["right_dist_list"]
        left_circles_list = s_type["left_dist_list"]
        small_circles_list = s_type["small_dist_list"]
    else:
        right_dist_list = s_type["right_dist_list"]
        left_dist_list = s_type["left_dist_list"]
        small_dist_list = s_type["small_dist_list"]
    smallCirclesSize = settings["smallCirclesSize"]
    largeCirclesSize = settings["largeCirclesSize"]
    circlesTextSize = settings["circlesTextSize"]
    lineSizeZoomDependence = settings["lineSizeZoomDependence"]
    badZoomThreshold = settings["badZoomThreshold"]
    crosshairColor = settings["crosshairColor"]
    crosshairLightColor = settings["crosshairLightColor"]
    rangefinderProgressBarColor1 = settings["rangefinderProgressBarColor1"]
    rangefinderProgressBarColor2 = settings["rangefinderProgressBarColor2"]
    drawCentralLineVert = settings["drawCentralLineVert"]
    drawCentralLineHorz = settings["drawCentralLineHorz"]
    fontSizeMult = max(settings["fontSizeMult"] * 0.2 * zoom, settings["minFontSize"])
    isLeft = True if coord[1] < 0 else False
    distancePos = str(round(-float(point(2000).split(',')[0]) * zoom * 0.0025, 4))
    if lineSizeZoomDependence == "sum":
        lineSizeMult = settings["lineSizeMult"] - fontSizeMult
    else:
        lineSizeMult = settings["lineSizeMult"]

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
    output += '\ncrosshair_distances {\n'
    for dist in sorted(right_dist_list + left_dist_list + small_dist_list):
        if dist in right_dist_list:
            output += crosshair_distance(dist, 1, 'right' if isLeft else 'left')
        if dist in left_dist_list:
            output += crosshair_distance(dist, 1, 'left' if isLeft else 'right')
        if dist in small_dist_list:
            output += crosshair_distance(dist, 0, 'left')
    output += '}\n'

    # Lines
    points = [point(5)]
    output += '\ndrawLines{\n'
    output += 'line{\nline:p4= -0.7, 0, -2, 0\nmove:b=no\nthousandth:b=yes\n}\nline{\nline:p4= 0.7, 0, 2, 0\nmove:b=no\nthousandth:b=yes\n}\n'
    for dist in line_dist_list:
        points.append(point(dist))
        output += 'line    //to ' + str(dist) + '\n{\nline: p4 = ' + points[-1] + ', ' + points[-2] + '\nmove: b = yes\nthousandth: b = yes\n}\n'
    output += rangefinder_lines
    output += '}\n\n'

    # Circles
    output += 'drawCircles{\ncircle {\nsegment:p2 = 0, 360;\npos:p2 = 0, 0;\ndiameter:r = 0;\nsize:r = 4;\nmove:b = no\nthousandth:b = yes;\n}\n'
    if parallax:
        for dist in sim_circles_list.keys():
            output += circle(int(dist), sim_circles_list[dist]['size'])
    for dist in right_circles_list + left_circles_list:
        output += circle(dist, largeCirclesSize)
    for dist in small_circles_list:
        output += circle(dist, smallCirclesSize)
    output += '}\n\n'

    # Text
    output += 'drawTexts{\n'
    if parallax:
        for dist in sim_circles_list.keys():
            textPos = sim_circles_list[dist]['textPos']
            textPos[0] = textPos[0] if isLeft else -textPos[0]
            textSize = sim_circles_list[dist]['textSize']
            output += text(int(dist), textPos, textSize)
    for dist in right_circles_list + left_circles_list:
        output += text(dist, [-1.5 if isLeft else 1.5, 0], circlesTextSize)
    output += rangefinder_text
    output += '}'

    # Writing into file
    try:
        os.mkdir(path)
    except OSError:
        pass

    path = path + '\\' + sight_type + '_' + path.rpartition('\\')[2] + '.blk'
    with open(path, 'w') as f:
        f.write(output)
        print("Successfully created sight at %s " % path)


def get_rangefinder(zoom, side):
    """
    Function that returns text for adding rangefinder.
    :param zoom: zoom type - 'bad' or 'good'
    :param side: side where rangefinder should be painted - 'left' or 'right'
    :return: tuple with line str and text str
    """
    if zoom == 'bad':
        string = '$BadZoom'
    elif zoom == 'good':
        string = '$GoodZoom'
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

    return line_str, text_str


if __name__ == '__main__':
    # Requesting all requirements and creating sight in output
    try:
        path = os.path.dirname(os.path.realpath(__file__)) + '\\output'
        speed = int(input('Shell speed in m/s: '))
        convergence = int(input('Convergence in meters: '))
        zoom = float(input('Zoom: '))
        sight_type = input('Sight type: ')
        coord = list(map(float, input('Sight coordinates: ').split(',')))

        create_sight(path, speed, zoom, sight_type, coord, convergence)
    except ValueError:
        print('Wrong format string')

    input("\nPress enter to exit")
