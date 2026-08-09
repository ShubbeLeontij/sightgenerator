#!/usr/bin/env python3
import shutil

import generator
import json
import math
import os
import argparse


def sight_category(sight_type):
    """
    Function that maps a data.json sight-type key (e.g. "sim_AP_f", "RB_s", "sim_LASER")
    to its coarse category (e.g. "AP", "RB", "LASER"), stripping the "sim_" prefix and
    any "_f"/"_s" (fast/slow shell) suffix.
    :param sight_type: sight-type key as found in data.json
    :return: str category name
    """
    base = sight_type[len("sim_"):] if sight_type.startswith("sim_") else sight_type
    if base.endswith("_f") or base.endswith("_s"):
        base = base[:-2]
    return base


def reader(MODE, sheets=None, _print=print, _input=input):
    """
    Function that reads data.json and creates sights for every tank/sight-type. This is the core of whole program.
    :param MODE: output mode. Development - 0 ; Normal - 1 (default) ; Silent - 2 ; Full silent - 3
    :param sheets: list of sight-type categories that will be used (e.g. "AP", "RB", "LASER"). By default, all are used
    :param _print: output function
    :param _input: input function
    """
    def _output(string, severity=1):
        """
        Function that check should some text be moved to output or not.
        :param string: text that potentially should be moved to output
        :param severity: integer severity of this text
        """
        if MODE <= severity:
            _print(string)

    try:
        os.mkdir(generator.get_path() + "/UserSights")
        _output("Created folder " + generator.get_path() + "/UserSights", 1)
    except:
        pass
    _output("Writing in " + generator.get_path() + "/UserSights", 1)

    # Loading the data
    wrong_entries = 0
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    generator.insert_str = dict[str, str]()
    _output("\nReading data.json", 1)
    for unit_id, entry in data.items():  # Iterating tanks
        if not entry:  # "{}" marker means "don't generate a sight for this tank"
            continue
        # convergence missing (e.g. SPAA without gunConvergence in game files) is treated as infinite,
        # i.e. parallax depends only on distance, never zeroes out
        convergence = entry.get("convergence", math.inf)
        zoom = float(entry["zoom"])

        for sight_type, type_data in entry.items():
            if sight_type in ("zoom", "convergence"):
                continue
            if sheets and sight_category(sight_type) not in sheets:  # Checking allowed list
                continue
            _output(str((unit_id, sight_type, type_data)), 0)
            try:
                speed = type_data["velocity"]
                coord = list(type_data.get("coords", [0.0, 0.0]))
                # Removing 3% speed from AP, 5% from HE and HEAT
                if sight_type == "sim_AP":
                    speed *= 0.97
                if sight_type in ("sim_HEAT", "sim_HE"):
                    speed *= 0.95
                # Create sight using generator
                _output(generator.generator(unit_id, [speed], zoom, [sight_type], [coord], [convergence]), 0)
            except:  # If something went wrong
                wrong_entries += 1
                _output("Wrong entry format. Unit: " + unit_id + " Type: " + sight_type, 1)

    try:
        res = generator.save_presets()
        _output(res, 1)
        generator.increment_version()
    except:
        _output("\nError saving presets!\n", 1)
    _output(str(wrong_entries) + " errors", 1)
    _output("Execution ended with " + str(wrong_entries) + " errors\n", 2)
    if MODE <= 2:
        _input("Press Enter to exit")


def cleaner(MODE, remove_all_tanks=False, _print=print, _input=input):
    def _output(string, severity=1):
        """
        Function that check should some text be moved to output or not.
        :param string: text that potentially should be moved to output
        :param severity: integer severity of this text
        """
        if MODE <= severity:
            _print(string)

    _output("Deleting all from " + generator.get_path() + "/UserSights\n", 1)
    for dir_name in os.listdir(generator.get_path() + "/UserSights"):
        if remove_all_tanks or dir_name != "all_tanks":
            try:
                _output("Deleting " + dir_name, 0)
                shutil.rmtree(os.path.join(generator.get_path() + "/UserSights", dir_name))
            except:
                pass
    _output("Deleted " + generator.get_path() + "/UserSights\n", 1)


if __name__ == "__main__":
    # Read all arguments from terminal and run main function
    parser = argparse.ArgumentParser(description="Creates UserSights folder with WarThunder sights.")
    parser.add_argument("-m", "--mode", help="Output mode. Development - 0 ; Normal - 1 (default) ; Silent - 2 ; Full silent - 3", default=1)
    MODE = int(vars(parser.parse_args())["mode"])

    reader(MODE, _print=print, _input=input)
