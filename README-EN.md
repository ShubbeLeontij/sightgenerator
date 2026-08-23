# Installation

There are two installation methods, the first is simpler, and the second gives more freedom of customization (if ui offers not enough, you can try editing the defaults.py file or other program files), but requires the user to have basic terminal skills for installation.
1) Folder with exe file\
Download zip: https://github.com/ShubbeLeontij/sightgenerator/releases/download/6.0/sightgenerator.zip \
You do not need to download anything additionally, however, at the first start, the antivirus may react - allow it to run the file.

2) Python project\
Clone the project: https://github.com/ShubbeLeontij/sightgenerator, download and install python3: https://www.python.org/downloads/ (if not already installed), make sure `ADD Python to PATH` and `td/tk and IDLE` are checked.
Install the required libraries `python -m pip install -r requirements.txt`.
In the project folder, you need to run `ui.py`.

# Settings

There are many options in the settings menu, most of which are explained by tooltips.
If it is still not clear what this setting is responsible for, there is PREVIEW, roughly showing what the changes will lead to.

The left side of the menu is the global settings that apply to all sights.
The right part is separate for each sight type - they are switched using the menu in the upper right corner.
Sights are generated with three types, chosen by the shell's muzzle velocity: simulator_s (below 600 m/s), simulator (600-1100 m/s) and simulator_f (above 1100 m/s).
All of them take parallax into account and differ mainly in the distances the markers are drawn for - the slower the shell, the closer together the markers are.
On top of that every tank gets an arcade and a realistic sight, built from its standard shell: there is no parallax in those gamemodes, so the sight sits on the gun and convergence is ignored, and the arcade one differs from the realistic one only by the absence of a rangefinder.
Those two also come in three speed variants (arcade_s/arcade/arcade_f and realistic_s/realistic/realistic_f in settings.json), picked by the same speed thresholds.
Finally, a tank with a laser rangefinder gets one more sight - simulator_laser. Such a tank measures the range in game and its ballistic computer aims the gun itself, so this sight carries neither the stadiametric rangefinder nor the far distance marks, only the parallax markers of the near distances.

For simulator sights or if you just want to use circles instead of the standard markers, there is the EDIT SIM CIRCLES menu - in it each line creates a distance marker using a circle.

After changing the settings, remember to press SAVE SETTINGS AND EXIT TO MAIN MENU, simply closing the window will cancel all changes.

If you want to know what sights the tank gets, you can open data.json - the file sights are built from. Each top-level key is a tank's unit id.
Inside it, "zoom" is the gunner's sight zoom (minimum), "convergence" is the convergence distance in meters (zero-parallax distance, null means no convergence), "coords" is the sight's height/side offset from the gun in meters, "standard" is the shell whose sight is bound to the tank in global.blk and "laser" tells whether the tank has a laser rangefinder.
Every other key is a shell of that tank - one sight is created for each of them, named after the shell, plus arcade.blk and realistic.blk for the standard one and simulator_laser.blk when "laser" is true. A shell holds its "speed" in m/s (the sight type is chosen by it), the game's shell "type", and its "mass" in kg, "caliber" in meters and "cx" (drag coefficient), from which the air resistance is calculated. The caliber is the diameter of the body that actually flies, so for a discarding-sabot shell it is the penetrator, not the barrel.
An empty `{}` entry means no sight is generated for that tank, and shells without "speed" (missiles and rockets) are skipped.

# Presets

The project supports presets created in the in-game sight editing menu. 
You can select a saved preset using the button in the settings menu - when launched it will be applied to tanks where no other sight with preset was selected. 
Thus, when entering the game, all sights will be selected, you only need to go to the in-game menu if you need a different sight. 

This is implemented by editing the global.blk file linked to your account. 
It is located at ~/.config/WarThunder/Saves/account-id/production/ for Linux and MacOS or Documents/My Games/WarThunder/Saves/account-id/production/ for Windows.
You can get your ID at https://store.gaijin.net/user.php
Also, to avoid accidental changes and bugs from this project, it is recommended to make a backup of global.blk (or better the entire Saves folder) before launching the program.

To clear sight preset bindings, use the Clear Bindings button in the main menu.

# Launch

In the main menu every sight is always created, and the radiobuttons only choose which one becomes the default sight written to global.blk: arcade, realistic, or simulator - the tank's laser sight if it has a laser rangefinder, otherwise the sight of its standard shell.
To create sights, press RUN or Enter button on the keyboard.

# Contacts

For all questions https://discord.gg/qjvECBPUxq
