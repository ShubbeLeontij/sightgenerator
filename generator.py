#!/usr/bin/env python3
from defaults import *
import json
import os
import re
import json


__author__ = "Shubbe Leontij"
__version__ = "4.1"


class Settings:
    def __init__(self, settings_path):
        with open(settings_path, 'r') as f:
            self.settings = json.load(f)

    def get_setting(self, key):
        return self.settings.get(key)

    def set_setting(self, key, value):
        self.settings[key] = value

    def save_settings(self, settings_path):
        with open(settings_path, 'w') as f:
            json.dump(self.settings, f, indent=4)


insert_str = dict[str, str]()
settings = Settings("settings.json")


def create_sight(speed, zoom, sight_type, coord, convergence, isMain=True):
    """
    Function that creates sight layout.
    :param speed: shell's speed in m/s (int type)
    :param zoom: minimum zoom (float type)
    :param sight_type: sight type according to settings.json
    :param coord: list with two floats inside - height and width location of sight relatively to the gun in meters
    :param convergence: convergence in meters i.e. distance with zero parallax (int type)
    :param isMain: boolean showing whether is this sight main or additional
    :return: list containing: start, distances_blk, lines_blk, circles_blk, text_blk. All in blk format
    """
    def point(distance):
        """
        Function that finds location of point on sight depending on distance.
        :param distance: int distance in meters
        :return: str with two parallaxes in milliradian split by ", "
        """
        if distance == 0:
            return "0, 0"
        parallax_x, parallax_y = - coord[1] * (1 / distance - 1 / convergence), coord[0] * (1 / distance - 1 / convergence)
        gravity = 5.0 * distance / speed ** 2  # 5.0 is g/2
        return str(round(parallax_x * 1000, 2)) + ", " + str(round((parallax_y + gravity) * 1000, 2))

    def crosshair_distance(distance, size, side):
        """
        Function that creates string for adding WT generated distances on sight.
        :param distance: int distance in meters
        :param size: big or small - int 1 or 0
        :return: str type generated text
        """
        x = distLength if size else round(distLength * DIST_MULT, 4)
        return "distance { distance:p3=" + str(distance) + ',' + (str(distance // 100) if size else '0') + ',' + ('-' if side == "right" else "") + str(x) + "; textPos:p2=" + ("" if side == "right" else '-') + str(x + DIST_INDENT) + ",0; }\n"

    def circle(distance, size, move=True, diameter=0):
        """
        Function that creates circle marking some distance.
        :param distance: int distance in meters
        :param size: diameter of circle
        :return: str type generated text
        """
        return "circle {    //" + str(distance) + "\nsegment:p2 = 0, 360;\npos:p2 = " + point(distance) + ";\ndiameter:r = " + str(diameter) + ";\nsize:r = " + str(size) + ";\nmove:b = " + ("yes" if move else "no") + "\nthousandth:b = yes;\n}\n"

    def text(distance, delta, size):
        """
        Function that creates text marking some distance.
        :param distance: int distance in meters
        :param delta: list of text shift in milliradians relative to the circle - [horizontal, vertical]
        :param size: size of text
        :return: str type generated text
        """
        x, y = tuple(map(float, point(distance).split(", ")))
        x, y = x + delta[0], y + delta[1]
        return "text\n{\ntext: t = \"" + (str(distance) if distance < 100 else str(distance//100)) + "\"\nalign: i = 0\npos: p2 = " + \
               str(round(x, 2)) + ", " + str(round(y, 2)) + "\nmove: b = yes\nthousandth: b = yes\nsize: r = " + str(size) + "\nhighlight: b = yes\n}\n"

    s_type = None
    for t in settings.get_setting("sightTypes"):
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
    centralCircleSize = s_type["centralCircleSize"]

    # Replace other direct dictionary accesses with calls to settings.get_setting
    distLength = settings.get_setting("distLength")
    drawCentralLineVert = settings.get_setting("drawCentralLineVert")
    drawCentralLineHorz = settings.get_setting("drawCentralLineHorz")
    crosshair = settings.get_setting("crosshair")
    fontSizeMult = max(settings.get_setting("fontSizeMult") * 0.2 * zoom, MIN_FONT_SIZE)
    lineSizeMult = round(settings.get_setting("lineSizeMult") / settings.get_setting("fontSizeMult"), 2)
    rangefinderFontSizeMult = round(1 / settings.get_setting("fontSizeMult"), 2)
    isLeft = True if coord[1] < 0 else False
    distancePos = round(float(point(DIST_POINT).split(',')[0]) * -0.01, 4)

    distances_blk = ""
    circles_blk = ""
    lines_blk = ""
    text_blk = ""
    rangefinder_lines = ""
    rangefinder_text = ""

    # Load rangefinder depending on gamemode and zoom
    if rangefinder:
        d = RANGEFINDERS_BLK["GoodZoom" if zoom > BAD_ZOOM_THRESHOLD else "BadZoom"]["Left" if isLeft else "Right"]
        rangefinder_lines = d["Lines"].replace("$main$", (d["MainLine"] if crosshair == "" or crosshair == "no" or crosshair == "false" or crosshair == "empty" else ""))
        rangefinder_text = d["Text"].replace("$size$", str(round(rangefinderFontSizeMult * (RANGEFINDER_BAD if zoom < BAD_ZOOM_THRESHOLD else RANGEFINDER_GOOD), 2)))

    # Start settings
    replacements = {"$drawCentralLineVert$": drawCentralLineVert, "$drawCentralLineHorz$": drawCentralLineHorz, "$fontSizeMult$": str(round(fontSizeMult, 2)), "$lineSizeMult$": str(round(lineSizeMult, 2)), "$distancePos$": str(distancePos)}
    rep = dict((re.escape(k), v) for k, v in replacements.items())
    start = re.compile("|".join(rep.keys())).sub(lambda m: rep[re.escape(m.group(0))], START_BLK)

    # Distances
    if isMain:
        for dist in sorted(right_dist_list + left_dist_list + small_dist_list):
            if dist in left_dist_list:
                distances_blk += crosshair_distance(dist, 1, "right" if isLeft else "left")
            if dist in right_dist_list:
                distances_blk += crosshair_distance(dist, 1, "left" if isLeft else "right")
            if dist in small_dist_list:
                distances_blk += crosshair_distance(dist, 0, "left" if isLeft else "right")

    # Lines
    if len(line_dist_list) > 1:
        points = [point(line_dist_list[0])]
        for dist in line_dist_list[1:]:
            points.append(point(dist))
            lines_blk += "line    //to " + str(dist) + "\n{\nline: p4 = " + points[-1] + ", " + points[-2] + "\nmove: b = yes\nthousandth: b = yes\n}\n"
    if isMain:
        if crosshair != "" and crosshair != "no" and crosshair != "false" and crosshair != "empty":
            if crosshair == "partial":
                lines_blk += PARTIAL_CROSSHAIR
            else:
                lines_blk += crosshair
        if centralLines != "" and centralLines != "no" and centralLines != "false" and centralLines != "empty":
            if centralLines == "brackets":
                lines_blk += BRACKETS_CENTRAL_LINES
            elif centralLines == "standard":
                lines_blk += STANDARD_CENTRAL_LINES
            else:
                centralLines += centralLines
        lines_blk += rangefinder_lines

    # Circles
    if isMain:
        circles_blk += CENTRAL_CIRCLE_BLK.replace("$size$", str(centralCircleSize)) + "\n"
    for dist in circles_list.keys():
        circles_blk += circle(int(dist), circles_list[dist]["size"])

    # Text
    if isMain:
        text_blk += rangefinder_text
    for dist in circles_list.keys():
        textPos = circles_list[dist]["textPos"]
        textPos[0] = textPos[0] if isLeft else -textPos[0]
        textSize = circles_list[dist]["textSize"]
        if textSize:
            text_blk += text(int(dist), textPos, textSize)

    return [start, distances_blk, lines_blk, circles_blk, text_blk]


def clear_sight_bindings():
    global_blk_path = ""
    for f in os.scandir(settings.get_setting("savesPath") + "/Saves"):
        if f.is_dir() and f.name.isnumeric():
            global_blk_path = f.path + "/production/global.blk"
            break
    if global_blk_path == "":
        return "Error"
    with open(global_blk_path, "r", encoding="utf-8") as f:
        read_file = f.read()
    depth = 1
    start_idx = read_file.find(SIGHT_BLOCK_IDENTIFIER) + len(SIGHT_BLOCK_IDENTIFIER)
    end_idx = start_idx
    for char in read_file[start_idx:]:
        if char == '{':
            depth += 1
        if char == '}':
            depth -= 1
        if depth <= 0:
            break
        end_idx += 1
    with open(global_blk_path, "w", encoding="utf-8") as f:
        f.write(read_file[:start_idx] + "      " + read_file[end_idx:])
    return "Cleared sight bindings with presets"


def save_presets():
    global_blk_path = ""
    for f in os.scandir(settings.get_setting("savesPath") + "/Saves"):
        if f.is_dir() and f.name.isnumeric():
            global_blk_path = f.path + "/production/global.blk"
            break
    if global_blk_path == "":
        return "Error"
    with open(global_blk_path, "r", encoding="utf-8") as f:
        read_file = f.read()
    depth = 1
    start_idx = read_file.find(SIGHT_BLOCK_IDENTIFIER) + len(SIGHT_BLOCK_IDENTIFIER)
    end_idx = start_idx
    for char in read_file[start_idx:]:
        if char == '{':
            depth += 1
        if char == '}':
            depth -= 1
        if depth <= 0:
            break
        end_idx += 1

    with open(global_blk_path, "w") as f:
        f.write(read_file[:start_idx])
        for tankname in list(insert_str.keys()):
            if read_file[start_idx:end_idx].find(tankname + '{') == -1:
                f.write(insert_str[tankname])
        f.write(read_file[start_idx:])
    return "\nPresets saved!"


def generator(path, speed, zoom, sight_type, coord, convergence):
    """
    Function that creates sight .blk file.
    :param path: path where sight should be created
    :param speed: list of shells' speed in m/s (int type)
    :param zoom: list of minimum zooms (float type)
    :param sight_type: list of sight types according to settings.json
    :param coord: list of lists with two floats inside - height and width location of sight relatively to the gun in meters
    :param convergence: list of convergences in meters i.e. distance with zero parallax (int type)
    """
    sight_list = create_sight(speed[0], zoom, sight_type[0], coord[0], convergence[0], True)
    for i in range(1, len(coord)):
        cur_sight_list = create_sight(speed[i], zoom, sight_type[i], coord[i], convergence[i], False)
        sight_list[2] += cur_sight_list[2]
        sight_list[3] += cur_sight_list[3]
        sight_list[4] += cur_sight_list[4]
    tankname = path.rpartition('/')[2]
    filename = '_'.join(sight_type) + '_' + tankname
    cur_path = path + '/' + filename + ".blk"
    output = (ALL_TANKS_TOP if tankname == "all_tanks" else "") + sight_list[0] + "\ncrosshair_distances{\n" + sight_list[1] + "}\n\ndrawLines{\n" + sight_list[2] + "}\n\ndrawCircles{\n" + sight_list[3] + "}\n\ndrawTexts{\n" + sight_list[4] + "}\n"
    try:
        os.mkdir(path)
    except:
        pass
    with open(cur_path, 'w') as f:
        f.write(output)
    if tankname != "all_tanks" and tankname not in insert_str:
        insert_str[tankname] = ("        " + tankname + "{\n          crosshair:t=\"" + filename + "\"\n" + settings.get_setting("preset") + "\n        }\n")
    return "Successfully created sight at %s " % cur_path


if __name__ == "__main__":
    # Requesting all requirements and creating sight in output
    try:
        insert_str = dict[str, str]()
        path = os.path.dirname(os.path.realpath("settings.json")) + "/UserSights/" + input("Tank name: ")
        speed = int(input("Shell speed in m/s: "))
        convergence = int(input("Convergence in meters: "))
        zoom = float(input("Zoom: "))
        sight_type = input("Sight type: ")
        coord = list(map(float, input("Sight coordinates: ").split(',')))
        try:
            os.mkdir(os.path.dirname(os.path.realpath("settings.json")) + "/UserSights/")
        except:
            pass
        print(generator(path, [speed], zoom, [sight_type], [coord], [convergence]))
        print(save_presets())
    except ValueError:
        print("Wrong format string")

    input("\nPress enter to exit")
