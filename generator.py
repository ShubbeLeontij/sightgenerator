#!/usr/bin/env python3
from defaults import *
import json
import os
import re


__author__ = "Shubbe Leontij, mod by Ian Sysoev"
__version__ = "3.7.modified"


def create_sight(speed, zoom, sight_type, coord, convergence, bigFloppa, isMain=True):
    """
    Function that creates sight layout.
    :param speed: shell's speed in m/s (int type)
    :param zoom: minimum zoom (float type)
    :param sight_type: sight type according to settings.json
    :param coord: list with two floats inside - height and width location of sight relatively to the gun in meters
    :param convergence: convergence in meters i.e. distance with zero parallax (int type)
    :param bigFloppa: type of Floppa (0, 1 or 2)
    :param isMain: boolean showing whether is this sight main or additional
    :return: list containing: start, distances_blk, lines_blk, circles_blk, text_blk. All in blk format
    """
    def point(distance):
        """
        Function that finds location of point on sight depending on distance.
        :param distance: int distance in meters
        :return: str with two parallaxes in milliradian split by ', '
        """
        if distance == 0:
            return '0, 0'
        parallax_x, parallax_y = - coord[1] * (1 / distance - 1 / convergence), coord[0] * (1 / distance - 1 / convergence)
        gravity = 5.0 * distance / speed ** 2  # 5.0 is g/2
        return str(round(parallax_x * 1000, 2)) + ', ' + str(round((parallax_y + gravity) * 1000, 2))

    def crosshair_distance(distance, size, side):
        """
        Function that creates string for adding WT generated distances on sight.
        :param distance: int distance in meters
        :param size: big or small - int 1 or 0
        :return: str type generated text
        """
        x = distLength if size else round(distLength * DIST_MULT, 4)
        return 'distance { distance:p3=' + str(distance) + ',' + (str(distance // 100) if size else '0') + ',' + ('-' if side == 'right' else '') + str(x) + '; textPos:p2=' + ('' if side == 'right' else '-') + str(x + DIST_INDENT) + ',0; }\n'

    def circle(distance, size, move=True, diameter=0):
        """
        Function that creates circle marking some distance.
        :param distance: int distance in meters
        :param size: diameter of circle
        :return: str type generated text
        """
        return 'circle {    //' + str(distance) + '\nsegment:p2 = 0, 360;\npos:p2 = ' + point(distance) + ';\ndiameter:r = ' + str(diameter) + ';\nsize:r = ' + str(size) + ';\nmove:b = ' + ('yes' if move else 'no') + '\nthousandth:b = yes;\n}\n'

    def text(distance, delta, size):
        """
        Function that creates text marking some distance.
        :param distance: int distance in meters
        :param delta: list of text shift in milliradians relative to the circle - [horizontal, vertical]
        :param size: size of text
        :return: str type generated text
        """
        x, y = tuple(map(float, point(distance).split(', ')))
        x, y = x + delta[0], y + delta[1]
        return 'text\n{\ntext: t = "' + (str(distance) if distance < 100 else str(distance//100)) + '"\nalign: i = 0\npos: p2 = ' + \
               str(round(x, 2)) + ', ' + str(round(y, 2)) + '\nmove: b = yes\nthousandth: b = yes\nsize: r = ' + str(size) + '\nhighlight: b = yes\n}\n'

    def floppa_circle(distance, size, move=True):
        """
        Function that creates circle marking some distance.
        :param distance: int distance in meters
        :param size: diameter of circle
        :return: str type generated text
        """
        x, y = tuple(map(float, point(distance).split(', ')))
        x, y = x + size * FLOPPA_OFFSET[0], y + size * FLOPPA_OFFSET[1]
        return 'text\n{\ntext: t = "' + FLOPPA_CHAR + '"\nalign: i = 0\npos: p2 = ' + str(round(x, 2)) + ', ' + str(round(y, 2)) + '\nmove: b = ' + ('yes' if move else 'no') + '\nthousandth: b = yes\nsize: r = ' + str(round(size, 2)) + '\nhighlight: b = yes\n}\n'

    def floppa_distance(distance, size, side):
        """
        Function that creates string for adding WT generated distances on sight if it has floppa.
        :param distance: int distance in meters
        :param size: filler, always size = 1
        :param side: filler, always side = right
        :return: str type generated text
        """
        x, y = tuple(map(float, point(distance).split(', ')))
        return 'distance { distance:p3=' + str(distance) + ',-' + str(distance // 100) + ',-' + str(distLength) + '; textPos:p2=' + str(0.01 * x + (0.003 if distance < 1000 else 0.010)) + ',0; }\n'

    def get_scaled_brackets(scale_factor):
        """
        Function that generates brackets with scaling.
        :param scale_factor: float multiplier for bracket size
        :return: str type generated brackets blk
        """
        # Original coordinates from BRACKETS_CENTRAL_LINES
        lines = [
            (0.6, 0, 1.6, 0),     # right horizontal
            (-0.6, 0, -1.6, 0),   # left horizontal  
            (-0.6, -0.6, -0.6, 0.6), # left vertical
            (0.6, -0.6, 0.6, 0.6),   # right vertical
            (0.6, 0.6, 0.3, 0.6),    # top right
            (-0.6, 0.6, -0.3, 0.6),  # top left
            (0.6, -0.6, 0.3, -0.6),  # bottom right
            (-0.6, -0.6, -0.3, -0.6) # bottom left
        ]
        
        brackets_blk = ""
        for x1, y1, x2, y2 in lines:
            scaled_x1 = x1 * scale_factor
            scaled_y1 = y1 * scale_factor
            scaled_x2 = x2 * scale_factor
            scaled_y2 = y2 * scale_factor
            brackets_blk += f"line{{\nline:p4= {scaled_x1}, {scaled_y1}, {scaled_x2}, {scaled_y2}\nmove:b=no\nthousandth:b=yes\n}}\n"
        
        return brackets_blk

    # Loading settings from json
    with open('settings.json', 'r') as f:
        settings = json.load(f)

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
    
    # Get configurable zoom threshold from settings
    bad_zoom_threshold = settings.get("badZoomThreshold", BAD_ZOOM_THRESHOLD)
    
    # Choose central circle size based on zoom level
    small_zoom_circle_size = settings.get("centralCircleSizeSmallZoom", s_type["centralCircleSize"])
    centralCircleSize = small_zoom_circle_size if zoom <= bad_zoom_threshold else s_type["centralCircleSize"]
    
    distLength = settings["distLength"]
    crosshairColor = settings["crosshairColor"]
    crosshairLightColor = settings["crosshairLightColor"]
    rangefinderProgressBarColor1 = settings["rangefinderProgressBarColor1"]
    rangefinderProgressBarColor2 = settings["rangefinderProgressBarColor2"]
    drawCentralLineVert = settings["drawCentralLineVert"]
    drawCentralLineHorz = settings["drawCentralLineHorz"]
    crosshair = settings["crosshair"]
    # Choose font size multiplier based on zoom level
    small_zoom_font_mult = settings.get("fontSizeMultSmallZoom", settings["fontSizeMult"])
    base_font_mult = small_zoom_font_mult if zoom <= bad_zoom_threshold else settings["fontSizeMult"]
    fontSizeMult = max(base_font_mult * 0.2 * zoom, MIN_FONT_SIZE)
    
    # Choose line size multiplier based on zoom level
    small_zoom_line_mult = settings.get("lineSizeMultSmallZoom", settings["lineSizeMult"])
    base_line_mult = small_zoom_line_mult if zoom <= bad_zoom_threshold else settings["lineSizeMult"]
    lineSizeMult = round(base_line_mult / base_font_mult, 2)
    
    # Choose rangefinder font size multiplier based on zoom level
    rangefinder_small_zoom_font_mult = settings.get("rangefinderFontSizeMultSmallZoom", settings.get("rangefinderFontSizeMult", 1.0))
    rangefinder_base_font_mult = rangefinder_small_zoom_font_mult if zoom <= bad_zoom_threshold else settings.get("rangefinderFontSizeMult", 1.0)
    rangefinderTextScale = round(rangefinder_base_font_mult * (RANGEFINDER_BAD if zoom < bad_zoom_threshold else RANGEFINDER_GOOD), 2)
    
    rangefinderFontSizeMult = round(1 / base_font_mult, 2)

    isLeft = True if coord[1] < 0 else False
    distancePos = round(float(point(DIST_POINT).split(',')[0]) * -0.01, 4)
    if bigFloppa == 2:
        distancePos = 0

    distances_blk = ''
    circles_blk = ''
    lines_blk = ''
    text_blk = ''

    # Function to scale rangefinder coordinates horizontally
    def scale_rangefinder_horizontal(text_content, scale_factor):
        """
        Scale x-coordinates of rangefinder lines and text positions by the given factor.
        Only affects x-coordinates, keeping y-coordinates unchanged.
        """
        if scale_factor == 1.0:
            return text_content
        
        import re
        
        # Scale line coordinates: line:p4 = x1, y1, x2, y2
        def replace_line_coords(match):
            coords = match.group(1).split(',')
            if len(coords) >= 4:
                # Scale x1 and x2, keep y1 and y2 unchanged
                x1 = float(coords[0].strip()) * scale_factor
                y1 = float(coords[1].strip())
                x2 = float(coords[2].strip()) * scale_factor  
                y2 = float(coords[3].strip())
                return f"line:p4 = {x1}, {y1}, {x2}, {y2}"
            return match.group(0)
        
        # Scale text positions: pos:p2 = x, y
        def replace_pos_coords(match):
            coords = match.group(1).split(',')
            if len(coords) >= 2:
                # Scale x, keep y unchanged
                x = float(coords[0].strip()) * scale_factor
                y = float(coords[1].strip())
                return f"pos:p2 = {x}, {y}"
            return match.group(0)
        
        # Apply scaling to line coordinates
        result = re.sub(r'line:p4\s*=\s*([^\n;]+)', replace_line_coords, text_content)
        # Apply scaling to position coordinates - match only until end of line
        result = re.sub(r'pos:p2\s*=\s*([^\n]+)', replace_pos_coords, result)
        
        return result

    # Load rangefinder depending on gamemode and zoom
    if rangefinder:
        d = RANGEFINDERS_BLK["GoodZoom" if zoom > bad_zoom_threshold or bigFloppa else "BadZoom"]["Left" if isLeft else "Right"]
        rangefinder_lines = d["Lines"].replace('$main$', (d["MainLine"] if bigFloppa or crosshair in ['', 'no', 'false', 'empty', 'drop'] else ''))
        rangefinder_text = d["Text"].replace('$size$', str(rangefinderTextScale))
        
        # Apply horizontal scaling for small zoom
        if zoom <= bad_zoom_threshold:
            horizontal_scale = settings.get("rangefinderHorizontalScaleSmallZoom", 1.0)
            if horizontal_scale != 1.0:
                rangefinder_lines = scale_rangefinder_horizontal(rangefinder_lines, horizontal_scale)
                rangefinder_text = scale_rangefinder_horizontal(rangefinder_text, horizontal_scale)
    elif not bigFloppa:
        rangefinder_lines = ''
        rangefinder_text = ''
    else:
        rangefinder_lines = RANGEFINDERS_BLK["GoodZoom"]["Left" if isLeft else "Right"]["MainLine"] + (FLOPPA_LINES_ADD if sight_type == "sim_LASER" else '')
        rangefinder_text = FLOPPA_TEXT_ADD

    # Start settings
    replacements = {'$crosshairColor$': crosshairColor, '$crosshairLightColor$': crosshairLightColor, '$rangefinderProgressBarColor1$': rangefinderProgressBarColor1,
                    '$rangefinderProgressBarColor2$': rangefinderProgressBarColor2, '$drawCentralLineVert$': drawCentralLineVert, '$drawCentralLineHorz$': drawCentralLineHorz,
                    '$fontSizeMult$': str(round(fontSizeMult, 2)), '$lineSizeMult$': str(round(lineSizeMult, 2)), '$rangefinderTextScale$': str(rangefinderTextScale),
                    '$distancePos$': str(distancePos)}
    rep = dict((re.escape(k), v) for k, v in replacements.items())
    start = re.compile("|".join(rep.keys())).sub(lambda m: rep[re.escape(m.group(0))], START_BLK)

    # Distances
    if bigFloppa == 0:
        if isMain:
            for dist in sorted(right_dist_list + left_dist_list + small_dist_list):
                if dist in left_dist_list:
                    distances_blk += crosshair_distance(dist, 1, 'right' if isLeft else 'left')
                if dist in right_dist_list:
                    distances_blk += crosshair_distance(dist, 1, 'left' if isLeft else 'right')
                if dist in small_dist_list:
                    distances_blk += crosshair_distance(dist, 0, 'left' if isLeft else 'right')
    elif bigFloppa == 1:
        for dist in sorted(right_dist_list + left_dist_list + small_dist_list):
            if dist in left_dist_list:
                text_blk += floppa_circle(dist, FLOPPA_SIZE)
                text_blk += text(dist, [FLOPPA_INDENT if isLeft else -FLOPPA_INDENT, 0], FLOPPA_SIZE_COEF)
            if dist in right_dist_list:
                text_blk += floppa_circle(dist, FLOPPA_SIZE)
                text_blk += text(dist, [-FLOPPA_INDENT if isLeft else FLOPPA_INDENT, 0], FLOPPA_SIZE_COEF)
            if dist in small_dist_list:
                text_blk += floppa_circle(dist, FLOPPA_SIZE)
    elif bigFloppa == 2:
        if isMain:
            for dist in sorted(right_dist_list + left_dist_list + small_dist_list):
                if dist in left_dist_list:
                    distances_blk += floppa_distance(dist, 1, 'right' if isLeft else 'left')
                if dist in right_dist_list:
                    distances_blk += floppa_distance(dist, 1, 'left' if isLeft else 'right')
                if dist in small_dist_list:
                    distances_blk += floppa_distance(dist, 0, 'left' if isLeft else 'right')

    # Lines
    if len(line_dist_list) > 1:
        points = [point(line_dist_list[0])]
        for dist in line_dist_list[1:]:
            points.append(point(dist))
            lines_blk += 'line    //to ' + str(dist) + '\n{\nline: p4 = ' + points[-1] + ', ' + points[-2] + '\nmove: b = yes\nthousandth: b = yes\n}\n'
    if isMain:
        if crosshair != '' and crosshair != 'no' and crosshair != 'false' and crosshair != 'empty':
            if crosshair == 'partial':
                lines_blk += PARTIAL_CROSSHAIR
            elif crosshair == 'drop' and sight_type in ['AB', 'AB_s', 'AB_f', 'RB', 'RB_s', 'RB_f']:
                lines_blk += 'line{\nline:p4= 0.0, 0.0, 0.0, 400\nmove:b=no\nthousandth:b=yes\n}\n'
            else:
                lines_blk += crosshair
        if centralLines != '' and centralLines != 'no' and centralLines != 'false' and centralLines != 'empty':
            if centralLines == 'brackets':
                # Apply zoom-based scaling for brackets
                if zoom <= bad_zoom_threshold:
                    brackets_scale = settings.get("bracketsScaleSmallZoom", 1.5)
                else:
                    brackets_scale = 1.0
                lines_blk += get_scaled_brackets(brackets_scale)
            elif centralLines == 'standard':
                lines_blk += STANDARD_CENTRAL_LINES
            else:
                centralLines += centralLines
        lines_blk += rangefinder_lines

    # Circles
    if not bigFloppa:
        if isMain:
            circles_blk += CENTRAL_CIRCLE_BLK.replace('$size$', str(centralCircleSize)) + '\n'
        for dist in circles_list.keys():
            circles_blk += circle(int(dist), circles_list[dist]['size'])
    else:
        if isMain:
            circles_blk += circle(0, 4.5, move=False)
            text_blk += floppa_circle(0, centralCircleSize * FLOPPA_COEF, move=False)  # may be should be 'if centralCircleSize * FLOPPA_COEF > 0.8 else 0.8'
        for dist in circles_list.keys():
            text_blk += floppa_circle(int(dist), circles_list[dist]['size'] * FLOPPA_COEF)

    # Text
    if isMain:
        text_blk += rangefinder_text
    for dist in circles_list.keys():
        textPos = circles_list[dist]['textPos']
        textPos[0] = textPos[0] if isLeft else -textPos[0]
        textSize = circles_list[dist]['textSize']
        if textSize:
            text_blk += text(int(dist), textPos, textSize)

    return [start, distances_blk, lines_blk, circles_blk, text_blk]


def generator(path, speed, zoom, sight_type, coord, convergence, FLOPPA):
    """
    Function that creates sight .blk file.
    :param path: path where sight should be created
    :param speed: list of shells' speed in m/s (int type)
    :param zoom: list of minimum zooms (float type)
    :param sight_type: list of sight types according to settings.json
    :param coord: list of lists with two floats inside - height and width location of sight relatively to the gun in meters
    :param convergence: list of convergences in meters i.e. distance with zero parallax (int type)
    :param FLOPPA: type of Floppa (0, 1 or 2)
    """
    sight_list = create_sight(speed[0], zoom, sight_type[0], coord[0], convergence[0], FLOPPA, True)
    for i in range(1, len(coord)):
        cur_sight_list = create_sight(speed[i], zoom, sight_type[i], coord[i], convergence[i], FLOPPA, False)
        sight_list[2] += cur_sight_list[2]
        sight_list[3] += cur_sight_list[3]
        sight_list[4] += cur_sight_list[4]
    if FLOPPA:
        sight_list[2] += FLOPPA_BLK_TEXT
    output = (ALL_TANKS_TOP if path.endswith('all_tanks') else '') + sight_list[0] + '\ncrosshair_distances{\n' + sight_list[1] + '}\n\ndrawLines{\n' + sight_list[2] + '}\n\ndrawCircles{\n' + sight_list[3] + '}\n\ndrawTexts{\n' + sight_list[4] + '}\n'
    if FLOPPA == 1:
        suffix = '/F_'
    elif FLOPPA == 2:
        suffix = '/FD_'
    else:
        suffix = '/'
    try:
        os.mkdir(path)
    except:
        pass
    cur_path = path + suffix + '_'.join(sight_type) + '_' + path.rpartition('/')[2] + '.blk'
    with open(cur_path, 'w') as f:
        f.write(output)
        return "Successfully created sight at %s " % cur_path


if __name__ == '__main__':
    # Requesting all requirements and creating sight in output
    try:
        path = os.path.dirname(os.path.realpath('settings.json')) + '/UserSights/' + input('Tank name: ')
        speed = int(input('Shell speed in m/s: '))
        convergence = int(input('Convergence in meters: '))
        zoom = float(input('Zoom: '))
        sight_type = input('Sight type: ')
        coord = list(map(float, input('Sight coordinates: ').split(',')))
        FLOPPA = int(input('Big Floppa: '))
        try:
            os.mkdir(os.path.dirname(os.path.realpath('settings.json')) + '/UserSights/')
        except:
            pass
        print(generator(path, [speed], zoom, [sight_type], [coord], [convergence], FLOPPA))
    except ValueError:
        print('Wrong format string')

    input("\nPress enter to exit")
