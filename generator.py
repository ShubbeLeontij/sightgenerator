#!/usr/bin/env python3
from defaults import *
from bisect import bisect_left
from functools import lru_cache
import math
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


def speed_category(speed) -> str:
    """
    Function that chooses sight type by shell's muzzle velocity.
    :param speed: shell's speed in m/s
    :return: sight type suffix
    """
    if speed < SLOW_SPEED_THRESHOLD:
        return "_s"
    if speed > FAST_SPEED_THRESHOLD:
        return "_f"
    return ""


def drag_factor(shell) -> float:
    """
    Function that finds how strongly the air slows a shell down.
    :param shell: dict with "mass" (kg), "caliber" (m, the diameter of the body that actually flies - for a
    discarding-sabot shell that of its penetrator), "cx" (drag coefficient) and "type" of the shell, as they
    are stored in data.json. A missing cx is taken from DEFAULT_CX by the shell type, while a missing mass
    or caliber means "no data" i.e. no air resistance at all
    :return: float k in 1/m, the shell losing speed as a = -k * v^2
    """
    if not shell:
        return 0.0
    mass, caliber = shell.get("mass"), shell.get("caliber")
    # A shell whose game files state no cx still flies through the same air, so its type answers for it
    cx = shell.get("cx") or DEFAULT_CX.get(shell.get("type") or "", DEFAULT_CX_FALLBACK)
    if not mass or not caliber:
        return 0.0
    area = math.pi * caliber ** 2 / 4
    return AIR_DENSITY * cx * area * DRAG_MULT / (2 * mass)


@lru_cache(maxsize=64)
def trajectory(speed, k, max_range):
    """
    Function that integrates the flight path of a shell fired horizontally, with gravity and air drag.
    :param speed: shell's muzzle velocity in m/s
    :param k: drag factor in 1/m from drag_factor()
    :param max_range: distance in meters up to which the path is needed
    :return: tuple of two lists - distances flown in meters and how far the shell fell by then in meters
    """
    distances, drops = [0.0], [0.0]
    x, y, vx, vy, t = 0.0, 0.0, float(speed), 0.0, 0.0
    while x < max_range and t < BALLISTIC_MAX_TIME:
        v = math.hypot(vx, vy)
        if v <= 0:
            break
        dt = BALLISTIC_STEP / v
        # Midpoint method - one half step to find the accelerations in the middle of the step
        ax, ay = -k * v * vx, -k * v * vy - GRAVITY
        mvx, mvy = vx + ax * dt / 2, vy + ay * dt / 2
        mv = math.hypot(mvx, mvy)
        m_ax, m_ay = -k * mv * mvx, -k * mv * mvy - GRAVITY
        x, y = x + mvx * dt, y + mvy * dt
        vx, vy = vx + m_ax * dt, vy + m_ay * dt
        t += dt
        distances.append(x)
        drops.append(-y)
    return distances, drops


def drop_angle(distance, speed, shell=None, max_range=0):
    """
    Function that finds how much the sight mark of a distance has to sit above the gun axis.
    :param distance: int distance in meters
    :param speed: shell's muzzle velocity in m/s
    :param shell: dict with the shell's ballistic data (see drag_factor), None meaning no air resistance
    :param max_range: the farthest distance the sight needs, so that one trajectory serves all its marks
    :return: float angle in radians
    """
    k = drag_factor(shell)
    if not k:  # No ballistic data - fall back to the vacuum trajectory
        return GRAVITY * distance / (2 * speed ** 2)
    distances, drops = trajectory(speed, k, max(max_range, distance) + BALLISTIC_RANGE_RESERVE)
    if distances[-1] < distance:  # Shell never gets that far, no sensible mark to draw
        return GRAVITY * distance / (2 * speed ** 2)
    i = bisect_left(distances, distance)
    if distances[i] == distance:
        drop = drops[i]
    else:  # Interpolating between the two steps around the distance
        part = (distance - distances[i - 1]) / (distances[i] - distances[i - 1])
        drop = drops[i - 1] + part * (drops[i] - drops[i - 1])
    # Flat fire approximation - firing at this angle raises the whole path by drop at the target
    return drop / distance


def create_sight(speed, zoom, sight_type, coord, convergence, isMain=True, shell=None):
    """
    Function that creates sight layout.
    :param speed: shell's speed in m/s (int type)
    :param zoom: minimum zoom (float type)
    :param sight_type: sight type according to settings.json
    :param coord: list with two floats inside - height and width location of sight relatively to the gun in meters
    :param convergence: convergence in meters i.e. distance with zero parallax (int type)
    :param isMain: boolean showing whether is this sight main or additional
    :param shell: dict with the shell's "mass", "caliber", "cx" and "type" from data.json, used to account
    for air resistance. Without it the shell is dropped through vacuum
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
        gravity = drop_angle(distance, speed, shell, max_range)
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

    s_type = settings.get_setting("sightTypes")[sight_type]
    line_dist_list = s_type["line_dist_list"]
    rangefinder = s_type["rangefinder"]
    right_dist_list = s_type["right_dist_list"]
    left_dist_list = s_type["left_dist_list"]
    small_dist_list = s_type["small_dist_list"]
    circles_list = s_type["circles"]
    centralLines = s_type["centralLines"]
    centralCircleSize = s_type["centralCircleSize"]
    # The farthest mark of the sight, rounded up so that sights of one shell share one cached trajectory
    max_range = max([DIST_POINT] + line_dist_list + right_dist_list + left_dist_list + small_dist_list +
                    [int(d) for d in circles_list])
    max_range = math.ceil(max_range / BALLISTIC_RANGE_RESERVE) * BALLISTIC_RANGE_RESERVE

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


def get_path() -> str:
    if os.name == "nt":
        # Windows
        saves_folder = userpaths.get_my_documents() + "\\My Games\\WarThunder\\Saves\\"
    else:
        # Linux or mac
        saves_folder = os.path.expanduser("~/.config/WarThunder/Saves/")
    id = Settings("settings.json").get_setting("id")
    if id != "":
        return saves_folder + str(id) + "/production"
    for f in os.scandir(saves_folder):
        if f.is_dir() and f.name.isnumeric():
            return f.path + "/production"
    raise Exception("Can not find UserSights location")


def increment_version():
    with open(get_path() + "/global.blk", "r", encoding="utf-8") as f:
        lines = f.readlines()
    findstr = "version:i="
    idx = lines[0].find(findstr)
    if idx == -1:
        return
    new_version = int(lines[0][idx + len(findstr):]) + 1
    with open(get_path() + "/global.blk", "w", encoding="utf-8") as f:
        f.write(findstr + str(new_version) + '\n' + "".join(lines[1:]))


def clear_sight_bindings():
    with open(get_path() + "/global.blk", "r", encoding="utf-8") as f:
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
    with open(get_path() + "/global.blk", "w", encoding="utf-8") as f:
        f.write(read_file[:start_idx] + "      " + read_file[end_idx:])
    return "Cleared sight bindings with presets"


def save_presets() -> str:
    with open(get_path() + "/global.blk", "r", encoding="utf-8") as f:
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

    with open(get_path() + "/global.blk", "w", encoding="utf-8") as f:
        f.write(read_file[:start_idx])
        for tankname in list(insert_str.keys()):
            if read_file[start_idx:end_idx].find(tankname + '{') == -1:
                f.write(insert_str[tankname])
        f.write(read_file[start_idx:])
    return "\nPresets saved at " + get_path() + "/global.blk\n"


def bind_preset(name, filename):
    """
    Function that remembers which sight should be bound to the tank in global.blk.
    :param name: tank name
    :param filename: name of the .blk sight file (without extension)
    """
    if name == "all_tanks":
        return
    if name in insert_str:
        return
    insert_str[name] = ("        " + name + "{\n          crosshair:t=\"" + filename + "\"\n" + settings.get_setting("preset") + "\n        }\n")


def generator(name, speed, zoom, sight_type, coord, convergence, filename=None, bind=True, shells=None):
    """
    Function that creates sight .blk file.
    :param name: tank name
    :param speed: list of shells' speed in m/s (int type)
    :param zoom: list of minimum zooms (float type)
    :param sight_type: list of sight types according to settings.json
    :param coord: list of lists with two floats inside - height and width location of sight relatively to the gun in meters
    :param convergence: list of convergences in meters i.e. distance with zero parallax (int type)
    :param filename: name of the .blk file to create. By default it is built from the sight types and tank name
    :param bind: boolean showing whether this sight should be bound to the tank in global.blk
    :param shells: list of dicts with the shells' ballistic data from data.json (see create_sight), one per
    mount. Without it the sights are built without air resistance
    """
    shells = shells if shells else [None] * len(coord)
    sight_list = create_sight(speed[0], zoom, sight_type[0], coord[0], convergence[0], True, shells[0])
    for i in range(1, len(coord)):
        cur_sight_list = create_sight(speed[i], zoom, sight_type[i], coord[i], convergence[i], False, shells[i])
        sight_list[2] += cur_sight_list[2]
        sight_list[3] += cur_sight_list[3]
        sight_list[4] += cur_sight_list[4]
    filename = filename if filename else '_'.join(sight_type) + '_' + name
    folder = get_path() + "/UserSights/" + name
    output = (ALL_TANKS_TOP if name == "all_tanks" else "") + sight_list[0] + "\ncrosshair_distances{\n" + sight_list[1] + "}\n\ndrawLines{\n" + sight_list[2] + "}\n\ndrawCircles{\n" + sight_list[3] + "}\n\ndrawTexts{\n" + sight_list[4] + "}\n"
    try:
        os.mkdir(folder)
    except:
        pass
    with open(folder + "/" + filename + ".blk", 'w') as f:
        f.write(output)
    if bind:
        bind_preset(name, filename)
    return "Successfully created sight at %s " % (folder + "/" + filename + ".blk")


if __name__ == "__main__":
    # Requesting all requirements and creating sight in output
    try:
        insert_str = dict[str, str]()
        name = input("Tank name: ")
        speed = int(input("Shell speed in m/s: "))
        convergence = int(input("Convergence in meters: "))
        zoom = float(input("Zoom: "))
        sight_type = speed_category(speed)
        filename = input("Sight name: ")
        coord = list(map(float, input("Sight coordinates: ").split(',')))
        shell_data = input("Shell mass in kg, caliber in m, cx and type (leave empty for no air drag): ")
        shell = None
        if shell_data.strip():
            mass, caliber, cx, shell_type = (shell_data.split(',') + [""])[:4]
            shell = {"mass": float(mass), "caliber": float(caliber), "cx": float(cx), "type": shell_type.strip()}
        try:
            os.mkdir(get_path() + "/UserSights/")
        except:
            pass
        print(generator(name, [speed], zoom, [sight_type], [coord], [convergence], filename=filename,
                        shells=[shell]))
        print(save_presets())
    except ValueError:
        print("Wrong format string")

    input("\nPress enter to exit")
