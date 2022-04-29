Contacts
--------

For all questions discord Leontij#8405

Installation and launch
-----------------------

Download and unzip the project https://github.com/ShubbeLeontij/sightgenerator/archive/refs/heads/master.zip

Download and install python3 (if not already installed) https://www.python.org/downloads/

In the project folder, you need to run reader.py, a UserSights folder containing sights will be created. 

Settings
--------

path.txt - file containing path to the game folder (for example, C:\Games\War Thunder). 
By default, the file is empty - in this case, UserSights folder containing all sights will be created in the project folder. 

start.txt and rangefinder.txt - files containing some standard settings and rangefinder variants. 
Modify these files only if you are sure what you are doing.

data.xlsx - table used to build sights. Each line is a separate sight. For convenience, the data is divided into sheets. ALL is for AB and RB sights (without parallax), all other sheets for SB.
Columns from left to right: tank name, convergence in meters, projectile muzzle velocity in m/s, gunner's sight zoom without zooming in, sight type, then data from AssetViewer about sight location relative to the barrel. 

settings.json - main settings file (open in any text editor)

General settings:

crosshairColor and crosshairLightColor - two crosshair colors in the format red, green, blue, opacity

rangefinderProgressBarColor1 and rangefinderProgressBarColor2 - colors (in the same format) of the bar that appears while measuring the distance. 

drawCentralLineVert and drawCentralLineHorz - whether to draw vertical and horizontal lines. "yes" or "no"

lineSizeMult - line thickness

fontSizeMult - labels size. The final value will depend on this parameter and zoom. 

minFontSize - minimum value of fontSizeMult. It is necessary in order to see labels tanks with small zoom. 

badZoomThreshold - zoom threshold for rangefinder type selection

distLength - length of markers drawn by the game

Sight types:

names - list of this sight type's aliases. These aliases are used in data.xlsx

rangefinder - whether this sight will have a rangefinder (0 or 1)

right_dist_list and left_dist_list - lists of game markers distances on one and the other side, which will have a label

small_dist_list - list of game markers distances without a label. Also, length of the line is one and a half times less. The markers will be on the same side as the left_dist_list

circles - circles on sight in the following format: "distance": {"size": size of the circle, "textPos": [displacement of the label relative to the circle horizontally and vertically], "textSize": size of the label}
It is important to understand that circles do not consider the deceleration of the projectile, and game markers do not consider parallax, so it is recommended to use circles at short distances, and game markers at long distances. 

line_dist_list - list of distances by which the line is built. More distances can be added to make the line smoother.

centralLines - the text that will go into the drawLines block in the .blk file. By default, it draws lines in the center. 

centralCircle - the text that will go into the drawCircles block in the .blk file. By default, it draws circle in the center. 

Use Case №1
-----------
Let's say you want to have sights without a rangefinder and with markers on different sides instead of small dashes.

Open settings.json in any text editor, find "names": ["sim_AP", "sim_HEAT", "sim_HE"] , change 1 to 0 in the line below. This will remove the rangefinder.
Cut 1000, 1400, 1800, 2200, 2600, 3000 from the small_dist_list line and paste it into the right_dist_list. This will change the markers.
Do not forget to save the file, run reader.py, in the window that appears, make sure that all sights have been created (in case of some error, "Wrong string format" will be written instead of "Successfully created sight...").
Then move created files to the game folder and enjoy sights in the game (for the game to update the sights, press alt+f9)

Use Case №2
-----------
Let's say you want to have sights without central lines, but with a continuous horizontal line.

Open settings.json in any text editor, find drawCentralLineHorz , change no to yes. This will draw a horizontal line.
On each line containing centralLines, change everything after the colon to "". This will remove central lines.
Do not forget to save the file, run reader.py, in the window that appears, make sure that all sights have been created (in case of some error, "Wrong string format" will be written instead of "Successfully created sight...").
Then move created files to the game folder and enjoy sights in the game (for the game to update the sights, press alt+f9)

Use Case №3
-----------
Let's say you want to have cyan sights that turn black when illuminated.

Open settings.json in any text editor, find crosshairColor, change it to "0, 255, 255, 255" , change crosshairLightColor to "0, 0, 0, 255".
Do not forget to save the file, run reader.py, in the window that appears, make sure that all sights have been created (in case of some error, "Wrong string format" will be written instead of "Successfully created sight...").
Then move created files to the game folder and enjoy sights in the game (for the game to update the sights, press alt+f9)