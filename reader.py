#!/usr/bin/env python3
import shutil

import generator
from defaults import *
import json
import math
import os
import argparse


def reader(MODE, default_mode="simulator", _print=print, _input=input):
    """
    Function that reads data.json and creates every sight of every tank. This is the core of whole program.
    :param MODE: output mode. Development - 0 ; Normal - 1 (default) ; Silent - 2 ; Full silent - 3
    :param default_mode: sight that is written to global.blk as the default one - "arcade", "realistic" or
    "simulator" (the standard shell's sight)
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
        # convergence missing or null (e.g. SPAA without gunConvergence in game files) is treated as
        # infinite, i.e. parallax depends only on distance, never zeroes out
        convergence = entry.get("convergence") or math.inf
        zoom = float(entry["zoom"])
        coord = list(entry.get("coords", [0.0, 0.0]))
        standard = entry.get("standard")

        # Arcade and realistic sights are made once per tank from its standard shell - there is no parallax
        # in those gamemodes, so the sight sits on the gun (no coords) and convergence never matters
        # Standard shell without speed is reported by the shell loop below, so here it is simply skipped
        standard_speed = entry.get(standard, {}).get("speed") if standard else None
        for gamemode in ("arcade", "realistic") if standard_speed else ():
            sight_type = gamemode + generator.speed_category(standard_speed)
            _output(str((unit_id, gamemode, sight_type, standard, standard_speed)), 0)
            try:
                _output(generator.generator(unit_id, [standard_speed], zoom, [sight_type], [[0.0, 0.0]],
                                            [math.inf], filename=gamemode, bind=gamemode == default_mode,
                                            shells=[entry.get(standard)]), 0)
            except:  # If something went wrong
                wrong_entries += 1
                _output("Wrong entry format. Unit: " + unit_id + " Gamemode: " + gamemode, 1)

        if entry.get("laser"):
            sight_type = "simulator_laser"
            try:
                _output(generator.generator(unit_id, [standard_speed], zoom, [sight_type], [coord],
                                            [convergence], filename=sight_type, bind=True,
                                            shells=[entry.get(standard)]), 0)
            except:  # If something went wrong
                wrong_entries += 1
                _output("Wrong entry format. Unit: " + unit_id + " Gamemode: " + sight_type, 1)

        for shell_name, shell in entry.items():  # Iterating shells of the tank
            if shell_name in ("zoom", "convergence", "coords", "standard", "laser"):
                continue
            speed = shell.get("speed") if isinstance(shell, dict) else None
            if not speed:  # Shells without muzzle velocity (missiles and rockets) get no sight
                # wrong_entries += 1
                _output("No shell speed. Unit: " + unit_id + " Shell: " + shell_name, 0)
                continue
            sight_type = "simulator" + generator.speed_category(speed)
            _output(str((unit_id, shell_name, sight_type, shell)), 0)
            try:
                # Create sight using generator, the standard shell being the default sight in simulator mode
                _output(generator.generator(unit_id, [speed], zoom, [sight_type], [coord], [convergence],
                                            filename=shell_name, shells=[shell],
                                            bind=default_mode == "simulator" and shell_name == standard), 0)
            except:  # If something went wrong
                wrong_entries += 1
                _output("Wrong entry format. Unit: " + unit_id + " Shell: " + shell_name, 1)

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
    parser.add_argument("-d", "--default", help="Sight written to global.blk as the default one", choices=("arcade", "realistic", "simulator"), default="simulator")
    args = vars(parser.parse_args())

    reader(int(args["mode"]), args["default"], _print=print, _input=input)
