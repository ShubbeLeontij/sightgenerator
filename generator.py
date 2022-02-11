import os
import json

__author__ = "Shubbe Leontij"
__license__ = "GPL"
__version__ = "1.2"
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
        if gamemode == 'sim':
            parallax_x, parallax_y = - coord[1] * (1 / distance - 1 / convergence), coord[0] * (1 / distance - 1 / convergence)
        elif gamemode == 'ab' or gamemode == 'rb':
            parallax_x, parallax_y = 0, 0
        else:
            raise ValueError

        gravity = 5.0 * distance / speed ** 2
        return str(round(parallax_x * 1000, 2)) + ', ' + str(round((parallax_y + gravity) * 1000, 2))

    def crosshair_distance(distance, size):
        """
        Function that creates string for adding WT generated distances on sight.
        :param distance: int distance in meters
        :param size: big or small - int 1 or 0
        :return: str type generated text
        """
        if size == 0:
            return 'distance:p3=' + str(distance) + ', 0, 0\n'
        if size == 1:
            return 'distance:p3=' + str(distance) + ', ' + str(distance // 100) + ', 0\n'

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
    isLeft = True if coord[1] < 0 else False
    settings = json.load(open('settings.json', 'r'))

    gamemode = settings["gamemode"].lower()
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
    fontSizeMult = settings["fontSizeMult"] * 0.2 * zoom
    if lineSizeZoomDependence == "sum":
        lineSizeMult = settings["lineSizeMult"] - fontSizeMult
    else:
        lineSizeMult = settings["lineSizeMult"]

    sim_circles_list = settings["sim_circles_list"]
    line_dist_list = []
    large_circles_list = []
    small_circles_list = []
    large_dist_list = []
    small_dist_list = []
    found = False
    for s_type in settings["sightTypes"]:
        if s_type["type"] == sight_type:
            found = True
            line_dist_list = s_type["line_dist_list"]
            if s_type["circles"]:
                large_circles_list = s_type["large_dist_list"]
                small_circles_list = s_type["small_dist_list"]
            else:
                large_dist_list = s_type["large_dist_list"]
                small_dist_list = s_type["small_dist_list"]
    if not found:
        print("Incorrect sight type")
        return

    # Load rangefinder depending on gamemode and zoom
    if gamemode == 'ab':
        rangefinder_lines, rangefinder_text = '', ''
    elif gamemode == 'rb' or gamemode == 'sim':
        rangefinder_lines, rangefinder_text = rangefinder('good' if zoom > badZoomThreshold else 'bad', 'left' if isLeft else 'right')
    else:
        raise ValueError

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
    for dist in line_dist_list:
        points.append(point(dist))
        output += 'line\n{\nline: p4 = ' + points[-1] + ', ' + points[-2] + '\nmove: b = yes\nthousandth: b = yes\n}\n'
    output += rangefinder_lines
    output += '}\n\n'

    # Circles
    output += 'drawCircles{\ncircle {\nsegment:p2 = 0, 360;\npos:p2 = 0, 0;\ndiameter:r = 0;\nsize:r = 4;\nmove:b = no\nthousandth:b = yes;\n}\n'
    if gamemode == 'sim':
        for dist in sim_circles_list:
            output += circle(dist, largeCirclesSize)
    for dist in large_circles_list:
        output += circle(dist, largeCirclesSize)
    for dist in small_circles_list:
        output += circle(dist, smallCirclesSize)
    output += '}\n\n'

    # Text
    output += 'drawTexts{\n'
    if gamemode == 'sim':
        for dist in sim_circles_list:
            if dist < 100:
                output += text(dist, [0, 1], circlesTextSize)
            elif dist < 300:
                output += text(dist, [0, -1], circlesTextSize)
            elif dist < 500:
                output += text(dist, [-0.5 if isLeft else 0.5, -0.7], circlesTextSize)
            else:
                output += text(dist, [-0.7 if isLeft else 0.7, -0.5], circlesTextSize)
    for dist in large_circles_list:
        output += text(dist, [-1.5 if isLeft else 1.5, 0], circlesTextSize)
    output += rangefinder_text
    output += '}'

    # Writing into file
    try:
        os.mkdir(path)
    except OSError:
        pass

    path = path + '\\' + gamemode + '_' + sight_type + '_' + path.rpartition('\\')[2] + '.blk'
    with open(path, 'w') as f:
        f.write(output)
        print("Successfully created sight at %s " % path)


def rangefinder(zoom, side):
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
