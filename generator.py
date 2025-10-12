#!/usr/bin/env python3
from defaults import *
import os
import re
import json
import userpaths


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

    # Replace other direct dictionary accesses with calls to settings.get_setting
    distLength = settings.get_setting("distLength")
    drawCentralLineVert = settings.get_setting("drawCentralLineVert")
    drawCentralLineHorz = settings.get_setting("drawCentralLineHorz")
    crosshair = settings.get_setting("crosshair")
    
    # Get configurable zoom threshold from settings
    bad_zoom_threshold = settings.get_setting("badZoomThreshold") or BAD_ZOOM_THRESHOLD
    
    # Choose central circle size based on zoom level
    small_zoom_circle_size = settings.get_setting("centralCircleSizeSmallZoom") or s_type["centralCircleSize"]
    centralCircleSize = small_zoom_circle_size if zoom <= bad_zoom_threshold else s_type["centralCircleSize"]
    
    # Choose font size multiplier based on zoom level
    small_zoom_font_mult = settings.get_setting("fontSizeMultSmallZoom") or settings.get_setting("fontSizeMult")
    base_font_mult = small_zoom_font_mult if zoom <= bad_zoom_threshold else settings.get_setting("fontSizeMult")
    fontSizeMult = max(base_font_mult * 0.2 * zoom, MIN_FONT_SIZE)
    
    # Choose line size multiplier based on zoom level
    small_zoom_line_mult = settings.get_setting("lineSizeMultSmallZoom") or settings.get_setting("lineSizeMult")
    base_line_mult = small_zoom_line_mult if zoom <= bad_zoom_threshold else settings.get_setting("lineSizeMult")
    lineSizeMult = round(base_line_mult / base_font_mult, 2)
    
    # Choose rangefinder font size multiplier based on zoom level
    rangefinder_small_zoom_font_mult = settings.get_setting("rangefinderFontSizeMultSmallZoom") or settings.get_setting("rangefinderFontSizeMult") or 1.0
    rangefinder_base_font_mult = rangefinder_small_zoom_font_mult if zoom <= bad_zoom_threshold else (settings.get_setting("rangefinderFontSizeMult") or 1.0)
    rangefinderTextScale = round(rangefinder_base_font_mult * (RANGEFINDER_BAD if zoom < bad_zoom_threshold else RANGEFINDER_GOOD), 2)
    
    rangefinderFontSizeMult = round(1 / base_font_mult, 2)
    isLeft = True if coord[1] < 0 else False
    distancePos = round(float(point(DIST_POINT).split(',')[0]) * -0.01, 4)

    distances_blk = ""
    circles_blk = ""
    lines_blk = ""
    text_blk = ""
    rangefinder_lines = ""
    rangefinder_text = ""

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
        d = RANGEFINDERS_BLK["GoodZoom" if zoom > bad_zoom_threshold else "BadZoom"]["Left" if isLeft else "Right"]
        rangefinder_lines = d["Lines"].replace('$main$', (d["MainLine"] if crosshair in ['', 'no', 'false', 'empty', 'drop'] else ''))
        rangefinder_text = d["Text"].replace('$size$', str(rangefinderTextScale))
        
        # Apply horizontal scaling for small zoom
        if zoom <= bad_zoom_threshold:
            horizontal_scale = settings.get_setting("rangefinderHorizontalScaleSmallZoom") or 1.0
            if horizontal_scale != 1.0:
                rangefinder_lines = scale_rangefinder_horizontal(rangefinder_lines, horizontal_scale)
                rangefinder_text = scale_rangefinder_horizontal(rangefinder_text, horizontal_scale)

    # Start settings
    replacements = {
        "$drawCentralLineVert$": drawCentralLineVert, 
        "$drawCentralLineHorz$": drawCentralLineHorz, 
        "$fontSizeMult$": str(round(fontSizeMult, 2)), 
        "$lineSizeMult$": str(round(lineSizeMult, 2)), 
        "$distancePos$": str(distancePos)
    }
    rep = dict((re.escape(k), v) for k, v in replacements.items())
    start_blk_with_rangefinder_scale = START_BLK.replace("rangefinderTextScale:r=1.0", f"rangefinderTextScale:r={rangefinderTextScale}")
    start = re.compile("|".join(rep.keys())).sub(lambda m: rep[re.escape(m.group(0))], start_blk_with_rangefinder_scale)

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
    if len(line_dist_list) > 1 and crosshair != "drop":
        points = [point(line_dist_list[0])]
        for dist in line_dist_list[1:]:
            points.append(point(dist))
            lines_blk += "line    //to " + str(dist) + "\n{\nline: p4 = " + points[-1] + ", " + points[-2] + "\nmove: b = yes\nthousandth: b = yes\n}\n"
    if isMain:
        if crosshair != "" and crosshair != "no" and crosshair != "false" and crosshair != "empty":
            if crosshair == "partial":
                lines_blk += PARTIAL_CROSSHAIR
            elif crosshair == "drop":
                lines_blk += DROP_LINE_CROSSHAIR
            else:
                lines_blk += crosshair
        if centralLines != "" and centralLines != "no" and centralLines != "false" and centralLines != "empty":
            if centralLines == "brackets":
                # Apply bracket scaling for small zoom
                brackets_scale = settings.get_setting("bracketsScaleSmallZoom") or 1.0
                if zoom <= bad_zoom_threshold and brackets_scale != 1.0:
                    lines_blk += get_scaled_brackets(brackets_scale)
                else:
                    lines_blk += BRACKETS_CENTRAL_LINES
            elif centralLines == "standard":
                lines_blk += STANDARD_CENTRAL_LINES
            else:
                lines_blk += centralLines
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


def get_global_blk_path() -> str:
    home = os.path.expanduser("~")
    if os.name == "nt":
        # Windows
        saves_folder = userpaths.get_my_documents() + "\\My Games\\WarThunder\\Saves"
    else:
        # Linux or mac
        saves_folder = os.path.expanduser("~/.config/WarThunder/Saves/")
    for f in os.scandir(saves_folder):
        if f.is_dir() and f.name.isnumeric():
            return f.path + "/production/global.blk"


def increment_version():
    global_blk_path = get_global_blk_path()
    with open(global_blk_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    findstr = "version:i="
    idx = lines[0].find(findstr)
    if idx == -1:
        return
    new_version = int(lines[0][idx + len(findstr):]) + 1
    with open(global_blk_path, "w", encoding="utf-8") as f:
        f.write(findstr + str(new_version) + '\n' + "".join(lines[1:]))


def clear_sight_bindings():
    global_blk_path = get_global_blk_path()
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


def save_presets() -> str:
    global_blk_path = get_global_blk_path()
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
        f.write(read_file[:start_idx])
        for tankname in list(insert_str.keys()):
            if read_file[start_idx:end_idx].find(tankname + '{') == -1:
                f.write(insert_str[tankname])
        f.write(read_file[start_idx:])
    return "\nPresets saved at " + global_blk_path + '\n'


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
