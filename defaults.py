# Some setting that I don't want to include in .json. Normally you don't want to change this.
SIGHT_BLOCK_IDENTIFIER = "tankSightSettings{"
MIN_FONT_SIZE = 0.35
BAD_ZOOM_THRESHOLD = 3.49
RANGEFINDER_BAD = 0.66
RANGEFINDER_GOOD = 0.45
DIST_INDENT = 0.01
DIST_MULT = 0.66
DIST_POINT = 2000
ALL_TANKS_TOP = "matchExpClass {\nexp_tank:b = yes\nexp_heavy_tank:b = yes\nexp_tank_destroyer:b = yes\nexp_SPAA:b = yes\n}\n\n"
PARTIAL_CROSSHAIR = "line{\nline:p4= 0, -2.5, 0, -400\nmove:b=no\nthousandth:b=yes\n}\nline{\nline:p4= 2.5, 0, 400, 0\nmove:b=no\nthousandth:b=yes\n}\nline{\nline:p4= -2.5, 0, -400, 0\nmove:b=no\nthousandth:b=yes\n}\n"
DROP_LINE_CROSSHAIR = "line{\nline:p4= 0, 0, 0, 400\nmove:b=no\nthousandth:b=yes\n}\n"
BRACKETS_CENTRAL_LINES = "line{\nline:p4= 0.6, 0, 1.6, 0\nmove:b=no\nthousandth:b=yes\n}\nline{\nline:p4= -0.6, 0, -1.6, 0\nmove:b=no\nthousandth:b=yes\n}\nline{\nline:p4= -0.6, -0.6, -0.6, 0.6\nmove:b=no\nthousandth:b=yes\n}\nline{\nline:p4= 0.6, -0.6, 0.6, 0.6\nmove:b=no\nthousandth:b=yes\n}\nline{\nline:p4= 0.6, 0.6, 0.3, 0.6\nmove:b=no\nthousandth:b=yes\n}\nline{\nline:p4= -0.6, 0.6, -0.3, 0.6\nmove:b=no\nthousandth:b=yes\n}\nline{\nline:p4= 0.6, -0.6, 0.3, -0.6\nmove:b=no\nthousandth:b=yes\n}\nline{\nline:p4= -0.6, -0.6, -0.3, -0.6\nmove:b=no\nthousandth:b=yes\n}\n"
STANDARD_CENTRAL_LINES = "line{\nline:p4= -0.7, 0, -2, 0\nmove:b=no\nthousandth:b=yes\n}\nline{\nline:p4= 0.7, 0, 2, 0\nmove:b=no\nthousandth:b=yes\n}\n"
START_BLK = "\nrangefinderTextScale:r=1.0\nrangefinderVerticalOffset:r=1.6\nrangefinderHorizontalOffset:r=55\nfontSizeMult:r=$fontSizeMult$\nlineSizeMult:r=$lineSizeMult$\ndrawCentralLineVert:b=$drawCentralLineVert$\ndrawCentralLineHorz:b=$drawCentralLineHorz$\ndrawDistanceCorrection:b=yes\ndistanceCorrectionPos:p2=-0.1, -0.05\ndrawSightMask:b=yes\ncrosshairDistHorSizeMain:p2=0, 0\ncrosshairHorVertSize:p2=0.5, 0.5\ncrosshairDistHorSizeAdditional:p2=0.007, 0.0025\nrangefinderUseThousandth:b=yes\ncrosshair_hor_ranges{}\n\n// ballistic range indicators\ndrawUpward:b = no\ndistancePos:p2 = $distancePos$,0\nmove:b = yes\ncrosshairDistHorSizeMain:p2 = 0,0\ntextPos:p2 = 0.010, 0\ntextAlign:i = 1\ntextShift:r = 0\ndrawAdditionalLines:b = no\ncrosshairDistHorSizeAdditional:p2 = 0.0,0.0\ndrawDistanceCorrection:b = no\n"
CENTRAL_CIRCLE_BLK = "circle {\nsegment:p2 = 0, 360;\npos:p2 = 0, 0;\ndiameter:r = 0;\nsize:r = $size$;\nmove:b = no\nthousandth:b = yes;\n}"
RANGEFINDERS_BLK = {
    "BadZoom": {
        "Right": {
            "MainLine": "\n//main\nline { line:p4 = 30.5,   0, 6.8, 0; thousandth:b = true; move:b=no; }",
            "Lines": "\n//RANGEFINDER\n$main$\n//4\nline { line:p4 = 7,  6.0, 8, 6.0; thousandth:b = true; }\n//5\nline { line:p4 = 8.7, 5.2, 10.3, 5.2; thousandth:b = true; }\n//6\nline { line:p4 = 11, 4.3, 12, 4.3; thousandth:b = true; }\n//7\nline { line:p4 = 12.7, 3.7, 14.3, 3.7; thousandth:b = true; }\n//8\nline { line:p4 = 15, 3.1, 16, 3.1; thousandth:b = true; }\n//9\nline { line:p4 = 16.7, 2.75, 18.3, 2.75; thousandth:b = true; }\n//10\nline { line:p4 = 19, 2.5, 20, 2.5; thousandth:b = true; }\n//12\nline { line:p4 = 20.7, 2.2, 22.7, 2.2; thousandth:b = true; }\n//14\nline { line:p4 = 23.3, 1.95, 25.3, 1.95; thousandth:b = true; }\n//16\nline { line:p4 = 25.9, 1.8, 27.9, 1.8; thousandth:b = true; }\n//18\nline { line:p4 = 28.5, 1.6, 30.5, 1.6; thousandth:b = true; }\n//4-\nline { line:p4 = 7, 6, 7, 7; thousandth:b = true; }\n//6-\nline { line:p4 = 11, 4.3, 11, 6; thousandth:b = true; }\n//8-\nline { line:p4 = 15, 3.1, 15, 5; thousandth:b = true; }\n//10-\nline { line:p4 = 19, 2.5, 19, 4; thousandth:b = true; }\n//14-\nline { line:p4 = 23.3, 1.95, 23.3, 3.45; thousandth:b = true; }\n//18-\nline { line:p4 = 28.5, 1.6, 28.5, 3.1; thousandth:b = true; }\n",
            "Text": "\n//RANGEFINDER NUMBERS\n\ntext {\ntext:t = \"4\"\nalign:i = 0\npos:p2 = 7, 8.8\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext{\ntext:t=\"5\"\nalign:i=0\npos:p2= 9.5,6.6\nsize:r = $size$\nmove:b=no\nthousandth:b=yes\nhighlight:b=yes\n}\ntext {\ntext:t = \"6\"\nalign:i = 0\npos:p2 = 11, 7.6\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext{\ntext:t=\"7\"\nalign:i=0\npos:p2= 13.5,5.2\nsize:r = $size$\nmove:b=no\nthousandth:b=yes\nhighlight:b=yes\n}\ntext {\ntext:t = \"8\"\nalign:i = 0\npos:p2 = 15, 6.6\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext{\ntext:t=\"9\"\nalign:i=0\npos:p2= 17.5,4.1\nsize:r = $size$\nmove:b=no\nthousandth:b=yes\nhighlight:b=yes\n}\ntext {\ntext:t = \"10\"\nalign:i = 0\npos:p2 = 19, 5.7\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext{\ntext:t=\"12\"\nalign:i=0\npos:p2= 21.5,3.4\nsize:r = $size$\nmove:b=no\nthousandth:b=yes\nhighlight:b=yes\n}\ntext {\ntext:t = \"14\"\nalign:i = 0\npos:p2 = 23.3, 5.1\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext{\ntext:t=\"16\"\nalign:i=0\npos:p2= 26.7,2.9\nsize:r = $size$\nmove:b=no\nthousandth:b=yes\nhighlight:b=yes\n}\ntext{\ntext:t=\"18\"\nalign:i=0\npos:p2= 28.5,4.5\nsize:r = $size$\nmove:b=no\nthousandth:b=yes\nhighlight:b=yes\n}\n"
        },
        "Left": {
            "MainLine": "\n//main\nline { line:p4 = -30.5,   0, -6.8, 0; thousandth:b = true; move:b=no; }",
            "Lines": "\n//RANGEFINDER\n$main$\n//4\nline { line:p4 = -7,  6.0, -8, 6.0; thousandth:b = true; }\n//5\nline { line:p4 = -8.7, 5.2, -10.3, 5.2; thousandth:b = true; }\n//6\nline { line:p4 = -11, 4.3, -12, 4.3; thousandth:b = true; }\n//7\nline { line:p4 = -12.7, 3.7, -14.3, 3.7; thousandth:b = true; }\n//8\nline { line:p4 = -15, 3.1, -16, 3.1; thousandth:b = true; }\n//9\nline { line:p4 = -16.7, 2.75, -18.3, 2.75; thousandth:b = true; }\n//10\nline { line:p4 = -19, 2.5, -20, 2.5; thousandth:b = true; }\n//12\nline { line:p4 = -20.7, 2.2, -22.7, 2.2; thousandth:b = true; }\n//14\nline { line:p4 = -23.3, 1.95, -25.3, 1.95; thousandth:b = true; }\n//16\nline { line:p4 = -25.9, 1.8, -27.9, 1.8; thousandth:b = true; }\n//18\nline { line:p4 = -28.5, 1.6, -30.5, 1.6; thousandth:b = true; }\n//4-\nline { line:p4 = -7, 6, -7, 7; thousandth:b = true; }\n//6-\nline { line:p4 = -11, 4.3, -11, 6; thousandth:b = true; }\n//8-\nline { line:p4 = -15, 3.1, -15, 5; thousandth:b = true; }\n//10-\nline { line:p4 = -19, 2.5, -19, 4; thousandth:b = true; }\n//14-\nline { line:p4 = -23.3, 1.95, -23.3, 3.45; thousandth:b = true; }\n//18-\nline { line:p4 = -28.5, 1.6, -28.5, 3.1; thousandth:b = true; }\n",
            "Text": "\n//RANGEFINDER NUMBERS\n\ntext {\ntext:t = \"4\"\nalign:i = 0\npos:p2 = -7, 8.8\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext{\ntext:t=\"5\"\nalign:i=0\npos:p2= -9.5,6.6\nsize:r = $size$\nmove:b=no\nthousandth:b=yes\nhighlight:b=yes\n}\ntext {\ntext:t = \"6\"\nalign:i = 0\npos:p2 = -11, 7.6\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext{\ntext:t=\"7\"\nalign:i=0\npos:p2= -13.5,5.2\nsize:r = $size$\nmove:b=no\nthousandth:b=yes\nhighlight:b=yes\n}\ntext {\ntext:t = \"8\"\nalign:i = 0\npos:p2 = -15, 6.6\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext{\ntext:t=\"9\"\nalign:i=0\npos:p2= -17.5,4.1\nsize:r = $size$\nmove:b=no\nthousandth:b=yes\nhighlight:b=yes\n}\ntext {\ntext:t = \"10\"\nalign:i = 0\npos:p2 = -19, 5.7\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext{\ntext:t=\"12\"\nalign:i=0\npos:p2= -21.5,3.4\nsize:r = $size$\nmove:b=no\nthousandth:b=yes\nhighlight:b=yes\n}\ntext {\ntext:t = \"14\"\nalign:i = 0\npos:p2 = -23.3, 5.1\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext{\ntext:t=\"16\"\nalign:i=0\npos:p2= -26.7,2.9\nsize:r = $size$\nmove:b=no\nthousandth:b=yes\nhighlight:b=yes\n}\ntext{\ntext:t=\"18\"\nalign:i=0\npos:p2= -28.5,4.5\nsize:r = $size$\nmove:b=no\nthousandth:b=yes\nhighlight:b=yes\n}\n"
        }
    },
    "GoodZoom": {
        "Right": {
            "MainLine": "\n//main\nline { line:p4 = 20.1, 0, 4.5, 0; thousandth:b = true; move:b=no; }",
            "Lines": "\n//RANGEFINDER\n$main$\n//8\nline { line:p4 = 4.5, 3.1, 5.8, 3.1; thousandth:b = true; }\n//10\nline { line:p4 = 5.8, 2.6, 7.1, 2.6; thousandth:b = true; }\n//12\nline { line:p4 = 7.1, 2.1, 8.4, 2.1; thousandth:b = true; }\n//14\nline { line:p4 = 8.4, 1.9, 9.7, 1.9; thousandth:b = true; }\n//16\nline { line:p4 = 9.7, 1.6, 11.0, 1.6; thousandth:b = true; }\n//18\nline { line:p4 = 11.0, 1.4, 12.3, 1.4; thousandth:b = true; }\n//20\nline { line:p4 = 12.3, 1.2, 13.6, 1.2; thousandth:b = true; }\n//22\nline { line:p4 = 13.6, 1.05, 14.9, 1.05; thousandth:b = true; }\n//24\nline { line:p4 = 14.9, 0.95, 16.2, 0.95; thousandth:b = true; }\n//26\nline { line:p4 = 16.2, 0.89, 17.5, 0.89; thousandth:b = true; }\n//28\nline { line:p4 = 17.5, 0.82, 18.8, 0.82; thousandth:b = true; }\n//30\nline { line:p4 = 18.8, 0.73, 20.1, 0.73; thousandth:b = true; }\n",
            "Text": "\n//RANGEFINDER NUMBERS\n\ntext {\ntext:t = \"8\"\nalign:i = 0\npos:p2 = 5.2, 3.7\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"10\"\nalign:i = 0\npos:p2 = 6.45, 3.2\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"12\"\nalign:i = 0\npos:p2 = 7.8, 2.7\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"14\"\nalign:i = 0\npos:p2 = 9.05, 2.5\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"16\"\nalign:i = 0\npos:p2 = 10.35, 2.2\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"18\"\nalign:i = 0\npos:p2 = 11.65, 2.01\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"20\"\nalign:i = 0\npos:p2 = 12.95, 1.81\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"22\"\nalign:i = 0\npos:p2 = 14.25, 1.70\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"24\"\nalign:i = 0\npos:p2 = 15.55, 1.61\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"26\"\nalign:i = 0\npos:p2 = 16.85, 1.51\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"28\"\nalign:i = 0\npos:p2 = 18.15, 1.46\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"30\"\nalign:i = 0\npos:p2 = 19.45, 1.41\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\n"
        },
        "Left": {
            "MainLine": "\n//main\nline { line:p4 = -20.1, 0, -4.5, 0; thousandth:b = true; move:b=no; }",
            "Lines": "\n//RANGEFINDER\n$main$\n//8\nline { line:p4 = -4.5, 3.1, -5.8, 3.1; thousandth:b = true; }\n//10\nline { line:p4 = -5.8, 2.6, -7.1, 2.6; thousandth:b = true; }\n//12\nline { line:p4 = -7.1, 2.1, -8.4, 2.1; thousandth:b = true; }\n//14\nline { line:p4 = -8.4, 1.9, -9.7, 1.9; thousandth:b = true; }\n//16\nline { line:p4 = -9.7, 1.6, -11.0, 1.6; thousandth:b = true; }\n//18\nline { line:p4 = -11.0, 1.4, -12.3, 1.4; thousandth:b = true; }\n//20\nline { line:p4 = -12.3, 1.2, -13.6, 1.2; thousandth:b = true; }\n//22\nline { line:p4 = -13.6, 1.05, -14.9, 1.05; thousandth:b = true; }\n//24\nline { line:p4 = -14.9, 0.95, -16.2, 0.95; thousandth:b = true; }\n//26\nline { line:p4 = -16.2, 0.89, -17.5, 0.89; thousandth:b = true; }\n//28\nline { line:p4 = -17.5, 0.82, -18.8, 0.82; thousandth:b = true; }\n//30\nline { line:p4 = -18.8, 0.73, -20.1, 0.73; thousandth:b = true; }\n",
            "Text": "\n//RANGEFINDER NUMBERS\n\ntext {\ntext:t = \"8\"\nalign:i = 0\npos:p2 = -5.2, 3.7\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"10\"\nalign:i = 0\npos:p2 = -6.45, 3.2\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"12\"\nalign:i = 0\npos:p2 = -7.7, 2.7\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"14\"\nalign:i = 0\npos:p2 = -9.05, 2.5\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"16\"\nalign:i = 0\npos:p2 = -10.35, 2.2\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"18\"\nalign:i = 0\npos:p2 = -11.65, 2.01\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"20\"\nalign:i = 0\npos:p2 = -13.05, 1.81\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"22\"\nalign:i = 0\npos:p2 = -14.35, 1.70\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"24\"\nalign:i = 0\npos:p2 = -15.55, 1.61\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"26\"\nalign:i = 0\npos:p2 = -16.85, 1.51\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"28\"\nalign:i = 0\npos:p2 = -18.15, 1.46\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\ntext {\ntext:t = \"30\"\nalign:i = 0\npos:p2 = -19.45, 1.41\nmove:b = no\nthousandth:b = yes\nsize:r = $size$\nhighlight:b=yes\n}\n"
        }
    }
}
LABELS = {
    "EN": {
        "title": "Sightgenerator by Leontij, mod by Ian",
        "aliases": "Aliases: ",
        "editSimCircles": ["EDIT SIM\nCIRCLES", "Circles helpful mostly for simulator gamemode. There is parallax mechanic in tank sim and to counter it, this program creates flight path of shell, so basically circles are distance markers."],
        "saveSettings": "SAVE SETTINGS AND\nEXIT TO MAIN MENU",
        "stadiametricRangefinder": ["Stadiametric rangefinder", "Should program draw stadiametric rangefinder. This rangefinder helps find distance, by measuring enemy tank height."],
        "rightDistList": ["Distance marks on right side", "Those marks drawn by game engine and compatible with all type of shells. Write integers (in meters) separated by a space. Creating two marks less than 20 meters apart may cause the sight to not be drawn."],
        "leftDistList": ["Distance marks on left side", "Those marks drawn by game engine and compatible with all type of shells. Write integers (in meters) separated by a space. Creating two marks less than 20 meters apart may cause the sight to not be drawn."],
        "smallDistList": ["Distance marks without number near it", "Narrow marks without number near it. Write integers (in meters) separated by a space. Creating two marks less than 20 meters apart may cause the sight to not be drawn."],
        "lineDistList": ["Distances by which the line is built", "More distances can be added to make the line smoother. Because of the difficulty in calculating this distance usually does not match what the game draws, set a higher number. Write integers (in meters) separated by a space."],
        "centralCircleSize": ["Central circle size:", "Dot in the middle of the screen, your crosshair"],
        "loadPreset": ["LOAD PRESET", "Presets you can make in WT sight settings menu. Once saved they are located at WarThunder/UserSights/tank_sight_presets"],
        "fixThermals": ["Fix light color\nin thermals", "With this you can enable crosshair lighting while in thermals."],
        "lineSizeMult": ["Line size multiplier:", "Line size affects only how thick lines and distance lines."],
        "fontSizeMult": ["Font size multiplier:", "Font size affects on distance marks numbers, progress bars, circles, numbers and letters."],
        "distLength": "Game marker length:",
        "noLines": ["No central crosshair", "Affects only the central part."],
        "standardLines": ["Standard - · -", "Affects only the central part."],
        "bracketsLines": ["Brackets [·]", "Affects only the central part."],
        "noCrosshair": ["No lines", "Clear view, but might be offbeat."],
        "partialCrosshair": ["Partial lines", "Lines goes from edges, but does not touch middle of screen. Clearer view, has benefits of other variations."],
        "fullCrosshair": ["Full lines", "Continuous lines from right to left and from top to bottom. May interfere with the view, but gives better understanding of the positioning of the sight."],
        "dropLineCrosshair": ["Vertical line", "Clear view, but with shell trajectory drop line."],
        "sightType": "Sight Type:",
        "noCentralCrosshair": "No central crosshair",
        "standardCrosshair": "Standard crosshair",
        "bracketsCrosshair": "Brackets",
        "centralLines": "Central Lines",
        "badZoomThreshold": "Bad zoom threshold:",
        "smallZoomSettings": "Small Zoom Settings",
        "basicSettings": "Basic Settings",
        "lineSizeSmallZoom": "Line Size (Small Zoom)",
        "fontSizeSmallZoom": "Font Size (Small Zoom)",
        "rangefinderFontMult": "Rangefinder Font Mult",
        "rangefinderFontSmall": "Rangefinder Font (Small)",
        "centralCircleSmall": "Central Circle (Small)",
        "bracketsScaleSmall": "Brackets Scale (Small)",
        "rangefinderHScaleSmall": "Rangefinder H-Scale (Small)",
        "distance": ["Distance", "The distance at which the circle will be drawn. One integer in meters."],
        "size": ["Circle\nsize", "The size of the mark itself."],
        "textPos": ["Text Position\n(x, y)", "Relative offset of distance label."],
        "textSize": ["Text\nsize", "Distance label size."],
        "editCircles": "Edit Circles",
        "changeSettings": "SIGHT SETTINGS",
        "run": ["RUN*", "Make sure that you set all the settings according to your preferences"],
        "clearBindings": "Clear Bindings",
        "path": ["Sights folder path", "Path where sights should\nbe created. For example\nC:\\Games\\War Thunder\nEmpty means project folder"],
        "devMode": "Dev mode",
        "clear": ["Clear Folder*", "WARNING!!! This action will completely remove all contents of Sights Folder."],
        "abrb": ["AB/RB", "Click here to check/uncheck all."],
        "sim": ["Sim", "Click here to check/uncheck all."],
        "other": ["Other", "Click here to check/uncheck all."],
        "deleting": "Deleting...",
        "areYouSure": "Are you sure you want to remove all sigths?",
        "preview": ["SIGHT PREVIEW", "If you have any questions, just test how it looks by this feature. Exact repetition not guaranteed, approximate result shown."],
        "changeLanguage": "Сменить язык",
        "canvas": "Preview",
        "sightConfiguration": "Sight Configuration"
    },
    "RU": {
        "title": "Sightgenerator by Leontij, mod by Ian",
        "aliases": "Псевдонимы: ",
        "editSimCircles": ["РЕДАКТИРОВАТЬ\nКРУГИ", "Круги полезны в основном для симуляторного режима, в нем есть механика параллакса, и чтобы компенсировать его, эта программа создает траекторию полета снаряда относительно прицела и пушки, так что в основном круги являются метками дистанции."],
        "saveSettings": "СОХРАНИТЬ НАСТРОЙКИ\nИ ВЫЙТИ В ГЛАВНОЕ МЕНЮ",
        "stadiametricRangefinder": ["Стадиометрический дальномер", "Будет ли программа рисовать стад. дальномер. Этот дальномер помогает замерить дистанцию по высоте вражеского танка."],
        "rightDistList": ["Метки дистанции справа", "Эти метки рисуются движком игры и подходят под любой снаряд. Указывать целые числа (в метрах) через пробел. Создание двух меток с разницей менее 20 метров может вызвать непрорисовку прицела."],
        "leftDistList": ["Метки дистанции слева", "Эти метки рисуются движком игры и подходят под любой снаряд. Указывать целые числа (в метрах) через пробел. Создание двух меток с разницей менее 20 метров может вызвать непрорисовку прицела."],
        "smallDistList": ["Метки дистанции без обозначения", "Узкие метки без циферного обозначения. Указывать целые числа (в метрах) через пробел. Создание двух меток с разницей менее 20 метров может вызвать непрорисовку прицела."],
        "lineDistList": ["Дистанции, по которым строится линия", "Для большей плавности линии можно добавить больше дистанций. Из-за сложности в вычислениях обычно эта дистанция не совпадает с тем что рисует игра, указывайте с запасом. Указывать целые числа (в метрах) через пробел."],
        "centralCircleSize": ["Размер центрального круга:", "Точка в середине вашего экрана."],
        "loadPreset": ["ЗАГРУЗИТЬ КОНФИГУРАЦИЮ", "Конфигурации из меню настройки прицела WT. После сохраниения они находятся в WarThunder/UserSights/tank_sight_presets"],
        "fixThermals": ["Исправление подсветки\nв тепловизоре", "С этим можно включать подсветку прицела в тепловизоре."],
        "lineSizeMult": ["Множитель толщины линий:","Размер линий влияет только на толщину линий и линий идущих от меток дистанций."],
        "fontSizeMult": ["Множитель размера текста:","Размер шрифта влияет на размер цифр у меток дистанций, прогресс-бары, круги, цифры и буквы."],
        "distLength": "Длина игровых меток:",
        "noLines": ["Без центрального перекрестия", "Влияет только на центральную часть."],
        "standardLines": ["Стандартное перекрестье - · -", "Влияет только на центральную часть."],
        "bracketsLines": ["Скобочки [·]", "Влияет только на центральную часть."],
        "noCrosshair": ["Без линий", "Минимум занятого пространства, но может быть непривычно."],
        "partialCrosshair": ["Частичные линии", "Линии идут от краёв, но не касаются центра экрана. Лучше видимость, есть плюсы от обоих вариантов."],
        "fullCrosshair": ["Сплошные линии", "Непрерывные линии справа налево и сверху вниз. Может мешать обзору, но даёт хорошее понимание позиционирования прицела."],
        "dropLineCrosshair": ["Вертикальная линия", "Минимум занятого пространства, но с линией траектории падения снаряда."],
        "sightType": "Тип прицела:",
        "noCentralCrosshair": "Без центрального перекрестия",
        "standardCrosshair": "Стандартное перекрестие", 
        "bracketsCrosshair": "Скобочки",
        "centralLines": "Центральные линии",
        "badZoomThreshold": "Предел \"малого зума\":",
        "smallZoomSettings": "Настройки малого зума",
        "basicSettings": "Основные настройки",
        "lineSizeSmallZoom": "Размер линий (м. зум)",
        "fontSizeSmallZoom": "Размер шрифта (м. зум)",
        "rangefinderFontMult": "Шрифт дальномера",
        "rangefinderFontSmall": "Шрифт дальномера (м. зум)",
        "centralCircleSmall": "Центр. круг (м. зум)",
        "bracketsScaleSmall": "Масштаб скобок (м. зум)",
        "rangefinderHScaleSmall": "Гориз. масштаб д-мера (м. зум)",
        "distance": ["Дистан-\nция", "Дистанция, на которой будет нарисован круг. Одно целое число метров."],
        "size": ["Размер\nкруга", "Размер самой метки."],
        "textPos": ["Положение\nтекста (x, y)", "Относительное смещение подписи дистанции."],
        "textSize": ["Размер\nтекста", "Размер подписи дистанции."],
        "editCircles": "Редактировать круги",
        "changeSettings": "НАСТРОЙКИ ПРИЦЕЛА",
        "run": ["ЗАПУСК*", "Удостоверьтесь что все настройки выставлены по вашим предпочтениям"],
        "clearBindings": "Очистить Привязку прицелов",
        "path": ["Путь до папки с прицелами", "Путь до папки, в которой будут\nсозданы прицелы. Например\nC:\\Games\\War Thunder\nПустое поле означает папку проекта"],
        "devMode": "Dev mode",
        "clear": ["Очистить Папку*", "ОСТОРОЖНО!!! Полностью удалит всё содержимое папки с прицелами."],
        "abrb": ["AB/RB", "Нажми здесь чтобы отметить/убрать везде."],
        "sim": ["Sim", "Нажми здесь чтобы отметить/убрать везде."],
        "other": ["Другое", "Нажми здесь чтобы отметить/убрать везде."],
        "deleting": "Удаление...",
        "areYouSure": "Вы уверены, что хотите удалить все прицелы?",
        "preview": ["ПРЕДПРОСМОТР", "Если у вас есть вопросы к работе какого-то из пунктов, просто нажмите эту кнопку и проверьте как оно будет выглядеть. Точное повторение не гарантировано, показан приблизительный результат."],
        "changeLanguage": "Change language",
        "canvas": "Предпросмотр",
        "sightConfiguration": "Конфигурация прицела"
    }
}
ICON = ("iVBORw0KGgoAAAANSUhEUgAAAOAAAADhCAYAAADRcblEAAAhUXpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjarZtpch03sKX/YxW9BMwJL"
        "AdjRO+gl9/fwSVlWZaHiPdEW6TIyypUDmdI4Lrz//7vdf+HP82H7HKxVnutnj+55x4HXzT/+TPe38Hn9/f7c75+xL//9H13vr7wkW8lPqfPP1"
        "v9ev3398OPC3w+Db4qP12ora8fzD//oOev67dfLhQ/n5JWpK/314X614VS/PwgfF1gfB7L197s50eYX8+2vx+xff53+iu3Py/7L/82orcL90k"
        "xnhSS5++Y8mcBSf9HlwZfdP4OqcTPt0dK7zta5ediBOR3cfI/rcr9mpV7fp+VH1/9kpRUP993fOPPwaw/Pv/2+6H88v2vC7oX4p/unNaPO//p"
        "+36F8+vjfP9/727uvmfhKUauhLR+PdT3o7yveOEk5On9WuXD+L/wtb2PzkdzVO8i5dsvP/lYoYdIWm7IYYcRbjjv8wqLJeZ4ovE5xhXT+15LF"
        "ntcyTuylfURbjRytVMjc4v0Jr4bf6wlvPv2d7sVGjfegVfGwMXCJ/3xf+fjby90r0o+BN++4nSU36jKYhnKnP7mVSQk3O86Ki/A3x+//lFeEx"
        "ksL8yNBxx+fi4xS/iqLdVReolOvLDw+dNrwfbXBQgR9y4sJiQy4CstEGrwFqOFQBwb+RlcqNE0cZKCUErcrDLmlCrJaVH35ncsvNfGEj/fBrN"
        "IREk1GamhmciVgI36sdyooVFSyaWUWqy00suoqeZaaq1WBX7DkmUrVs2sWbfRUsuttNqsNdd6Gz32BDiWXrv11nsfg5sOrjz47cELxphxppln"
        "mXXabLPPsSiflVdZddlqbvU1dtxpgxO7bttt9z1OOJTSyaeceuy008+4lNpNN99y67Xbbr/jR9aCe20X/vLx37MWvrMWX6b0QvuRNX7V7PsSQ"
        "XBSlDMyFnMg46YMUNBROfMt5BydUqec+R7pihJZZVFydlDGyGA+IZYbfuTuj8z9KW8u5/9R3uJ35pxS97+ROafU/U3m/pq332Rti22WT+5lSG"
        "2ooPpE+/GC00ZsQ6T2t5+n79UiwHvBqNCW427VQJ+2qvk0+8lhlbRPnrmNFEEgIWeKw9bp/mb6ZjU/d/LWzlwAoHJbpls70n+dzPnWD2kAEEn"
        "FujtF0nDjJiWea9c7V2vrtEU2eUEwdABRYTnGvR0dutfaFovnmqHuNrlm4OHmZombu1Qozs8XgtzPI+NgLHCnEfqoPNuOxfUTa17ZDmw6Cyvb"
        "Rnz93eTsTtJ9q0ES96xb9zQyv/aN5L5vFr73tpDXncFtULjcmUl5y2HeNfexUc+xdgHmzM3aMtLUgxZ/YKUyR6tUVagXBPLpzHauO5ueKMrtI"
        "MXbz1UoN4gBWG8W12i7+bwpzJ3PHbWu1a0AYBf0yrtXP2uZq7sY2zl3rVbgn56sU8r3JKqEKmRZY2yFBFKqs6QJGa1kJCIQRnRFOftSeyM5C8"
        "dI9rlpzeaTzU55lmKr1sFD8NHzrJ0wp32psp6oiUUPUiCpAjezhwUcOB5rgv0Wbz2skV/yPUBdtA8legChs0MgAzOvXs46JZF3yK37mYT3q44"
        "9e3G+Wkc8nkxpdR6uE56RZyf+CmomVSwMxZTUX+UcGr/OMMcESDohsnKhr+Ao2UCrdf6iBn2Fxm4snTq3QHMSp4p660tE0maygjy8ZYVB5y1q"
        "louMTKG6Qc/yElbv2xmx95JGOTxGXaqbc0DEuFmUpzNoFx4s7HZYCD3X1HQ0GWXu8hDUUEcmDuO5kIyDl6XVYuaBB+u5afe1K1ybyD9ybs8Yb"
        "xwoIDDSUxQ5uK/r/luz/+XzqLNmxQycvRHB3tAgxnOetKlpItTfT9AgdNjsarJLZPsFEsYgDz2Unk6Beuts2WqJZYEErjV+G8k0wCr1V4+Hh1"
        "nbl0m3z0pMq7qcSqUZ+LOo63RJOrdaAsCRj6/ZEbYsbX2wET1SCqun3G5MJI7knYwQX/7UIYANAOyMtma+rBXUOHvFAXJDR1HxXO0CWwueJ+q"
        "7ZcrBqBsEVVM1R9rulgCK9XBJa6Uzq01UG/hze7BemtuUXC4JSQnvJRiHBRxCJutAcnYNtAeEskeF2k4hfK3s24GHSWDTuwULdFb8yY3WADl3"
        "yXyJfgHyKavQDqtYG7gUZMIl6JWhO5QNboqUalxrmRrRcT8gJ2QKNtPgPl8LSaWY6Z1QqMxGAUYwNV1dgq7lgwYBs4ZKaK8JdjQXiBx9Rqsu8"
        "2sUSxdqKru0fCulUOKiqyl50JE6IVxjVklWFRTOh/70xGG4eToJUUjJ2rxgcBsBziQcg9ZaFyIx2q9BYuXmMZTikjs540482OZJIkJrsYoA8U"
        "iyg5NJkYJIBGYZ1KAtbcJcC2gHzEoouKPpB8/LcyzE9RmVJ61uhrLWjA0Ao+n8WlDNqSAxwpaMHXj9EuSsIItE1L8VVUCcgF9DcAw05l7EKFz"
        "yTwwXUFdvoG1P5HlavKHpihQDv2GQP9zQJUpZ/IiGmwD6Vr/UU6SyKYICbvCRiHLu9cJFna+a2h3sC5PH4prcPGNc77kGAR35vrGpNcoOpHTW"
        "SYxAwXc0Bbm7JFGBgHdsbCQNlF2RFDzfpLgWYowl0RXIYeRoIZN9xOn2BJxHzzdBxAFy6pkCw9VM/uhx20lXHn6gnKB2nhYIgkGpPRlolaAS6"
        "b6/+Pmz8HHDhvQ/bv52iNUXlqrq3mQkXhhwkFU6jlUBrAVeY62HCja/adOLHAOX8iOekMXrmTxt1TUSjPXgnKA2GfsqOcutTboqONi9WzBeca"
        "lBKibh6BoUBw7SGz4ovMO6VB75Ly2W2sKovhkVmFrce6YDHQEjGABEHTpt0qCozewbTHVPrdDFecqJn8Z+TfxEd89AlZLEFtEwKFn9yGUK5Jo"
        "ux+ozaKni+we4puVQTdRTIf+05TL0HVXpem265pUapetS6DkDlRoAGEKaJyEYJPsUHhPETUAJmqOSsSydEFlkL+hsa0W08xCXBuSnCR0zvcTx"
        "FhcT72NQl+oKvkZWD5XXWRX0Fy8YqFqPC/RpMsQJ6qTXWBJKaAbSuzZSQhjWM9iqeQ9KhodT16nx/I/PlOiYcD8rko2DaFWN5LUAA3DBWeQAH"
        "Qa5oqQN+hYAAQssiqRP+OJcZTMjPqOryikd3KDuKxk35g0FulHF0edIgE48goANt7JDskH2Onp7zQDj4HuBtOsq+Sz8h6YFI/YGlWqWBan55o"
        "r8aTcTFpP8r2sKWiOIF5fEAMAH3NjenYLc2egbmFOgGTtYTSEno6QrqRPDYAcOdorKBDZU3BM1GcSM0C83Rxmd7rQ0rpO2iOFKbEBuLcch+rQ"
        "BZrV266tr/0uYA5IKcEDcIYBco0DGOKDjeXTaupZF+cK6CMRSBJ+gpl/iDfqwUYsxQ7oUyIQUsHDEMbqhnuFpq/TxZzi0TTgvLmZdB2mFUkVY"
        "KmjCh9vwcZUMZHRgjDDfwqg5gJGnJVLxFpq9qgAD6AiE1QUpiAlsL8QwKoAuAvM8VFQhzcXq6VCzrO4n99h8HIZt5Gjv+pXkSUyRV/gw5999R"
        "rzMDE/y28UVdHgpTWbUJKUpBCkonmKjZ5rdgWxO6dxIdy98NOqoTNokCLMajPrpXfdpXkRrnIQS1Z1h3IYrHbmiq+bEGKcmawTSLT0LTP0bZH"
        "C/gQpxZ07rSKtBiJWw5IAEQHMDXch+yhbQJd0HuXcxwU1jH75bcatY03l4mcCgatp0xU/obxAhnbjVK3OUJZboSPoIa0CDMPdFcFl1hzLkd6q"
        "sbxdvroc+vpHMJjICxYU6a6ivgVa/EQWNolmzZNThSkBMyw5ffTICWlYIJYJtssmFCQ119/3MY5U+CCPNDhviFy9E8TQTqgxXyyO5XbAl+U7Z"
        "MhKXMQieckvSqHfvgL9Q10n6s6B3eaj/YPxASRaPOi29NUwN1heT60ffWbBBh5PAuvEicVLoE+AEUITnlFxpgNVc5BJlhwpNOOsKlYPZ4jfUD"
        "lGxKcNyx1mblsYMZTDhwL8iHSwIjkDDW56l0u8Pl4v96GP3K27+pcEXacRIVRCKsACHRYKVkkoFiBpCDXjtuqG5w8j4DYz5xWUBS6nS5yyIjk"
        "GaH7LH6zEjRubxVQjKUjSU5MtBsWcjcY7yPQPmHOXzAagl2bA5CBP4VrfEN9YgCgrlwogV7pp8VIQdcYzovDBdioB8k9K8s0/VKuLGoLpdK/I"
        "lUDya4xm/hXwK2Bir/UDy+FiEEnJgUxjVXEtSLygb0BxTTotlGdgI+e5/738UeRYm5oJgpyXLK1ogJu+nFfe+MGUsl+Jl2RooBkDy0Lg8ephw"
        "AFpOCAEprzePdGuHCaGgifAIHTEoEcV9dGFq8BJxlSAi1GQLweWz5XewxlQu0DoCQIjy30sXj3FwEVo3lKphsXqKBWvWb8Af3Z9ofMCR4sScr"
        "ZJA4S3vYcS8YjHc6kA18FoWahX+gWPjAlVZJmtnOXnwrNjFFnDYGGXWIIOFisxSULyUuNflLp1IC+ITAiQaFjkkNYg69CQkhSDucDgOxeOCMb"
        "tkf0xAfrVNnpco7NAstAg6HUqHOlEk2iyaPZwruxGANHQiTAc/UqDoHIp4AJLQLTI7yVAUkAYqzuaSRLXkNzihQQzcgaD1R/CKUP+ejvjfidb"
        "wW1Vbz0EayC/ioNuDdnzAvVicAcfRUzAi/oC29ihsjGTDtnsgBizxjRVloUzT/BFkXRIV0GhGL1mOcqQQtiD3eSvNEH+/LPfbdWKzwdCguWT1"
        "f0Bsg7B3S0sOv+FBLp70PjGerzPp5PtYWpLOwMRxJOYQEtA+yD01CkAqbg1QTmgdTk8SeKi3Umlr4j3N1STdiFClQSqMBibINjSqDzyZqAhSX"
        "eKUEEI6wJEjofKo+6OSLRmfffLdTm1DZWK8Q4DsQSMiQ+bKg8z6TBo6KlE98BhNUE2EBKrWICpdT1wuYpQlRIKp5D2s2FSeI4b4wLeBfYAUDz"
        "JrRUifNdoaPquu94vVgpfQWZ2CrFgY/B4dgx7YnWTLdDwbaZf6pBmvmk6jwB3TJD6Bqya10qFdpWDJ2r+X2tfnYBdIYFWE7ADlI0LJB2rUnLJ"
        "SkJLWFF+An3LCZ6iK8E1naJrqUWETlQMe7Kbug2VxKNUjxBQBGmcS3xnNkVD6X7MUkIuC4xHmsCRLmj7jV4OC80Wcwbw8qPCHFIAl/YimLzA9"
        "6X4NXK4QYwDbXLmjMm7HHiVKrT/3WP+D5pJi+3xRoBNp+HjofIp6agD6RvZ2bnojBNgi4jZQirMgRvJBmKHLEN6+RHcBY/610rOqpmdr7e32o"
        "G40TeA6+DhySzYBFhZJ3KhvGFiDacSsZtbAiMaktBZBTuANqY44vhrRWZT3BWWqRoKz7yQXJoMI0YwgKXVgUk9ZC2tIP4/ARVCNF2WiZGnXIj"
        "c+QdyaPGrlBZUyQlrBAhitiVFcYk/8IqZuIdhNHJpI7XzCLXDZorQhp7J0D72XJ/wBxWAxEC50ijQTrxEbeSuI1juvuz68YS7YFTswRKvtIc6"
        "QneDOWbhFgQP0l07UENzK5zfux41f6n8X1yY3P3hdNG+xiJZYl54jA2iPAlMiz5rMucmUb1TkGnQM/HojUDQ8pYLmwfdrWorPACg1h+PZMAik"
        "pkurgdcLpA2qcTElNWy0cAl1Thp9EREcHUHPyS2yDNPXpjE0FTu2PAt304wsZk0a6VTkFjCAyMRRoHIJMALBL8xXnxX5V7cbCRsgy46wIYuZG"
        "gqY7Jo3cUUT+6Xp95BxI1ACLIhmHPTMefNfrNaOa23XxJpPzX2ZnwcKF2HRqUrNm0gYMqJS7VQ52PJhchY98gqJFieAeFpjrTYQaf0CpfoP13"
        "NOQXYAOLYlmhEYb3SQ8PfpHuQS5gBrC1+i0dEL9IaziiPzNBO9CQsbCJqLNCCS/KJKgUGgW24FPf+NUJqLWX5TcZLFB35NREwB0bMbx3bQZdA"
        "PsU0YuBAukuBae1NwivNrXolPIzBYMRl0uiZVbFZE3HjNqhD8sxDktlHJgeAEDVczwpjYIA9ECwgq//YU/VpKnvCwoSxHnm6QmjllybTnZ1w3"
        "aMShwxvpDt2fIqeUYA/Mp5JILBv6eqgC7uGJu17g0G4qF9wffgxiZGXyhmhMKozeE5gghnArxjNRB+k2pUaGeEA+poXFvp3H6QyKM9esyVZL/"
        "OoRMW8dDQEx69XgDyG5EbESrTsOcBT7AooPDGVdKLDEijR2RCvqMAh8oO7gvoh6zQ7wKbzuRg13fGmaVA/6cXuA0WjtTosTE6SgO9SM9AlwpA"
        "HUDIinhczXEIDomEbhqu+MnqJlNSxHVlISaCxQYV+KVLuvDgNJdRXcQfbYHATmQlNCuRGi588GHgI9QBep1chuy5CyimWYNABWDIooTtTXO89"
        "BVLe2ChAggD4PQ99uuWset6P1WE6XjVwx0b0o9V2Qn1OjE8D5Omo0kC0eEFonAelRGvSQgFdUGhwhawRUIymCJwtoiIVDv9Jn9apjxq6y6wtw"
        "PHzjUtUokx6QztxxYlYCfNQpnYDcqch6xKDkujRcuhW9Ae5TMsJJh7LC4XdMcGhchBYDaEVKMWilgOFaS9Pc5dMkClHbX6lowIZBNyTM7oP+d"
        "gtYIsK0sM6evANQ9PwbIpa36QRghC0viF3XwC2QDAM+7UuGeB08qdgsrLzqJXDB4DWd8QmndwW/ar/G48pE5uC1TTvntj+GVNC7ci715niaoJ"
        "2ArGlM/RRT7OCeHe1bao5dtBcKF8wq6qArJlrps5YtKF4CL9yRZEdGmeRoLCdT/BS4Nm7hYFSgTPQMmtIj98a7DwYclx6VyqAZgWaCLl7T/vm"
        "hHjwcCmyCL+dvBqkIH1zN91QBUVj7jtihfZLLdF4qmB+KGN0HheHr6OijXUm6vaKLRRP40Y5i39Y1pfgg+wM5uKJwBRwkrQ441OXl+aagGGjh"
        "wuO9QvYtXk8JFolThKSEc39RNX0MOVZkzaI6sZ6EgCU27T4GQEgGlbi3QbqjwFeDIxk3GlxnhST3Y9H4vkkJhBaddDn4rvGsDJp20Fhei/Fik"
        "WKVyOrDVLuaA5R8vidMLJFmIglwHnbRaVsIXlIHaPKl2SZhbFUnH3g2UAzlSjs07DuP+87eRclN+UgYVRvqmjQ56IBs31y1w3Y8fT74jWpYD/"
        "A/SyxpBEjiLhabqKIr8hnadOUp3lC1a7LhOm2KXclAyE4eQEmrVpTPpVfumUUilvoMk1UCgsq3cAOX3KEh/gMLDozmWCReZHw2hDw/onVqIFe"
        "YvHTF5vIIIHHGDwWqmI76aE6crFfT0MZ1VUfG1yWqMDbLX5MVgcVxVektHXNBnetMRANujEpFsqNMaZOuqAUd0CCYLTuCAe5WKRpRlVR6xNle"
        "8TGSU8KEeOsICiGOIrHfmwz3W/dRFR2uUjeSZmN4sMkR+0IDgly0fS2avHQ8miYqHnhxlTWC0WRt77f7oj22kVF/2GL5T/2ka0SCZu8azdW3a"
        "zjRoNi4CAf6M0pwPEyMBjJniRRwH71DlMvgQptSu1JvOEUpk6ktJZzG1swSZUyrxALSXfrAcXmdGhmFjmvApaELNQUP/3mHHJUXY3W0BCZP5S"
        "zs5sEmHOE18dDBEyQGejq3N/QAJJImZl5DhqjTBOi89M7KIWuULvj/Jo/wbZPHEAo1XFrFaS4EHZRLuKcXtSFLZTTaQuwKUfEQGzePs3ahSGM"
        "V2p/r6VSGUQoFcZTn6O0COLQUlIQI1LkSegMPfZB4ogtMK3g5ByThtMPQBElz8VBmJ7EE7ZpowLbeCQfZ3vMmFOARGpW64EbIE/pGOx4XXRUc"
        "3AcsZx2fUi9CCzBJOTjxz+ZeniB05g44KzSfdBGKq8WC7mjt7vTZSzKHe0vcamtDHUkF2iPedLBLUqtknVtZ+23YHbTN33tI99cfECYlZMyjk"
        "4NoQCQuZQO8ntmMRHSN6rU70MrM2vABrnBHm9xR0tp2/i+u/Y/PBdlF+aK70rXhKN9UQRjpvp5ta/5wCUCR00jrnYsKIuDP4EvgzjUacm6iIJ"
        "F6/e0P6/Qh6ndF9Af1naZOQdQPzuMEEX4ZXUz0kTcLRNaWjTy8XDnqp6AT49X25qD7W8FBStIiYrS920QxCZkBKHWNCBJFnOEYTygQ71WDVE3"
        "8iRLwVF6bHLfWG4KNqSEO2mqQtRDe9OPt/zVD8umAt2bTOsuwKUCkDip8LyneqSGRHWyWOk/nhRo4a9J03AFBnFBwlVQAaDchIJFYRXvaGvWi"
        "3mC6ijelEegptIfz+sWliwLIYYg/wDIce9s6bNXe4Okg1xGGu+m0AE5hTLsxaHc7EEsdHovuKd1DhpSftwtS8vjnsfv3Z7RD3xV1i/c112PLp"
        "iNdcdIjOjTjNbnaBE6alk+I11nf7jwA8wzQPIhdKI47a5iqU1DR0aEZzdvBIZKYtZmCE4o0tFoWyEIAk94YUsWBYbo1WNfJFG2KhTeMiIk0va"
        "NVuByTIQOOj/LcRf8Jx4sORaaAxatljN26QeaTaDYlHvajNKkzbe04jRdF38hdSiudpaMy7/gHj4dQPmd2bbvZtPxPw9ZfRmOkKN93WnBrS6y"
        "1AMkcTRvSO822iPDYQJeh/UhW1rGZjE+HjmgMr1EQwcTbSqp5yHudAVpT7sAethxPCTchDWENCjpS7khHRC0F2nW00Zy2QQ8AKfFEJVjCqWgI"
        "gWK98IlMW9CmRPECzYio0nC9VjuymgqB14kzcxoODO2KFSor6PgOaJSQdqGNnzf+Z1IhttnRBXBunTgw9IJ2hOS8qjPN0WBSTa8Q9aJ5//bSj"
        "lwuTgq+fIfV0zOV+XN6Dc2yz1iae4L/466h/f56dMqPLpIFMdJP2vReBbE5Gu0dI6QEpHkimhbMPDpVIE9KGnfVznZwhm2QcwF1zGsXtDXTRG"
        "YVHU+cGvgnIH2iFKA/xOGSYQD0R7WpE1HSyB818k9DwSLMwInpWK1o5bzh55tiTB1TS3npVAhawmEzEBzYHeAMqoSmk/b6/UET6lS+tgxTk28"
        "6xfSOivyOutE1HSSCaIFA2Gu7d+DyaOu76HjqG/kDy7AwIaOa/ouK2DqkU/UGgXZ0UgiMR153JBGlB/ge6J2okc77phaI4U0TBx1AoBQ1wMsj"
        "K1codVx212CEZwEC2wHPvN7o8UwlZOFreQZF9KGjEngomlR7U9p874jOoKGwX64lCjyIewcQYDJ5dDRRbmQNzgJOuobaMtV2VMhXZ3yxwOtPR"
        "1XcH4/aaT6NcrBTQYczUeiwyKtqk42gYkCxxLOhXHTi4msTYHRUOywik6rNBlEE69IBUjzVAeYL/EgJNu6uzSkqEMOgmVYZrJ5+tCpfSp2sg6"
        "ddQFYhHpq96SRMQ4l0wFE4JGd2NVDRmSea73pWoXOFWCgdvYYg9q7Cuew0xdGWxdCArUIbb6KnEj4ICYqDG3NbTVYxLxN9iMoxvufRP0n7u/A"
        "KqtlBBPcxdN9/N+unfGfTIfGDJjgoZyIJl2rLDndq2h8Ky9mQVoTBsP8o5AXl6RQSiAWXY/KqjuQl+nNuqpZqBuggSJYY5Jwn8jrp/J6jDCq4"
        "VNb9ND86pC8Ka/dzYcmjYxuibbDKA2bdqo5taISetNU3NI2W9XFE7rSkrfuoueIh6RddBasHmUe6FtoY2paftBIistXfUqYDu/J7TKgM/RClH"
        "pFIqm+pXWxR1jbN9Egl6l3HodFBUwe9g90Jl1dv/S7HHXKrslQYvCHMpibRNBSFjO4+80ydE9VEnegVUggnrPm2a17jgLPc0NUnQ2F+jahwOW"
        "FVeg6dqLOZOuLxjp/jN6Y66NBwlWVR+ZAI5dcyKqJeVlR0NEF6LzbCxiuxd1S7zomlo/kgQNiqdls1sAHyeBS9F0KH6acOEFATGp+JRVieNsr"
        "/ESnhIoi7UPkTc8n37Mi4IaDtDSSOw793jAdWNbbAjQjgwNVBYBej/9TIaNpk1xsA5Ezb0Oa39hI1j8bFRI3DCxeKRy5E3QfzUoLpfNbfF/ZE"
        "dldvGHqeuFMyqKFE1WK8u/ZYwBgugARyEzVIi0zNTa1p2hhxFjqMelPVeUjz8nf2zqW/0ZiOsgGAVH64FUPViKVvLqYh+JPwk9DUmweEQl0n0"
        "Ie8BA9AHaIJbL8xbPzYaDGaUegGQGms62QJAvoZd9keib4jIzo2swkW1d6zBPSR1XtTyZYj9Kt5jCEgvg5gpe10Azlq/AQWGQWYZeAL/SEAQp"
        "RNlLxKPcXPQUiNcXHDhrmG03GQU2cMjsvacdH2TLuvxRf+benYE7I/aypHMb7Zms7AatAQataed8+VfnwageiH6xB6hPjz6EuPc/zWyfvak6l"
        "+w5tUYfsBE51Qo551PNZ+OjuOORg4yLNov1J1VA8r1YutzxEC8hx1frnoTQ5UZIc05kQ1emkRvSnviKFgroZuSrIQE1wlgFgjHfqDp9/p0LZ2"
        "Xno/l85jXqijxk0EufjRthKic6X5aOzo7Y0OrWo6uElydP5yoBHTO5tUKxyKB1rIbL3Bgiyc9EZ5VQ3WtMGovQCrepMF4B9iMam8qXPTPMVPu"
        "7oYof7Z2s2Xh+A7s/JybRY/pexfedMuFLhbqHxqxLe3QD9oFp1kJtwEAl27pU7jwLg0/M0UIqu58O90IoiFK9wnaoAAtipGehtoK9KxvaJrzx"
        "PXL9ZEuf67MXF/e2Do9Djl1KRtgbTbj3yFTh3uhTfRhi75RuH1Ft52Rtfggqi8t2WW8sqjw0v4z+rfTIQCqj7oUI9ODB2JMp1fQU3UgW/BIPd"
        "+JGuKZqAItAkCspL0tKQqR32xhrZKacGpbW1aHmOB0vFnTO1uhndGHmRzEY+Sog6bE54rLo4UVaT5ptcJxCXBjMcZfpveIrK03woOH36L5rz1"
        "aE+msaKhQ0RUObTT1AoZ6kO7aYvw3OdE6NS8dUxnHwgQFkYeqTCKBeknWtAPc1tnkagg5V4KEO+39caYpOvlzzH5ozeiTB2UISYamgIqi7utw"
        "j0OzURI3UW9afbt7VK3ep/G9Tpop2PffcM4g0fngtgOwPQdUHmn2eobZw9aJm5KPSGPNXFC2mvYJmOvbSav3WkN1Fa6CLAbnrsyI9swW2w64E"
        "zQss6prB2O5PGQuzx5LWxX3fSPMPjocLbX+y5Nk2VMlXipzxKpA/CoabsOH3yQrMUrp3pLVfTovoDtoF21j4H/IK4xGD0xiZc0Nz2LRGsC0tv"
        "FlNcPbQ5WTcqfvnY6ql91nBKBScyGJh/IMGpO72fRm1V/fp8YoQmUm94PJT6DV7luJTjdZalAScMgnLaXaakAETtCG46jWkplnZDRFFuBFYgu"
        "HfFbOi/4derD6QC62FTnuSoE/9lGwMzed0pK75daOgutoz5Aswxy1DtcHspIZeFszkH5fw6c/VtvY4ru7u7/A3ZlVZPNrgNrAAABhGlDQ1BJQ"
        "0MgcHJvZmlsZQAAeJx9kT1Iw0AcxV9TpSqVInYQcchQO1kQFXHUKhShQqgVWnUwufQLmjQkKS6OgmvBwY/FqoOLs64OroIg+AHi6OSk6CIl/i"
        "8ptIj14Lgf7+497t4BQr3MNKtrHNB020wl4mImuyoGXtGLEAYQRUxmljEnSUl0HF/38PH1LsazOp/7c/SrOYsBPpF4lhmmTbxBPL1pG5z3icO"
        "sKKvE58RjJl2Q+JHrisdvnAsuCzwzbKZT88RhYrHQxkobs6KpEU8RR1RNp3wh47HKeYuzVq6y5j35C4M5fWWZ6zRHkMAiliBBhIIqSijDRoxW"
        "nRQLKdqPd/APu36JXAq5SmDkWEAFGmTXD/4Hv7u18pMTXlIwDnS/OM7HKBDYBRo1x/k+dpzGCeB/Bq70lr9SB2Y+Sa+1tMgRENoGLq5bmrIHX"
        "O4AQ0+GbMqu5Kcp5PPA+xl9UxYYvAX61rzemvs4fQDS1FXyBjg4BKIFyl7v8O6e9t7+PdPs7wek63K7PthGMgAADRppVFh0WE1MOmNvbS5hZG"
        "9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+Cjx4OnhtcG1ldGEgeG1sbnM"
        "6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDQuNC4wLUV4aXYyIj4KIDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3"
        "dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+CiAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgIHhtbG5zOnhtc"
        "E1NPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvbW0vIgogICAgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC"
        "9zVHlwZS9SZXNvdXJjZUV2ZW50IyIKICAgIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIKICAgIHhtbG5zOkd"
        "JTVA9Imh0dHA6Ly93d3cuZ2ltcC5vcmcveG1wLyIKICAgIHhtbG5zOnRpZmY9Imh0dHA6Ly9ucy5hZG9iZS5jb20vdGlmZi8xLjAvIgogICAg"
        "eG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIgogICB4bXBNTTpEb2N1bWVudElEPSJnaW1wOmRvY2lkOmdpbXA6ZGNmM"
        "GEyMWYtNDhmMy00ZjJhLWI4NTYtMzhiMjBlMDkzZjUxIgogICB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOjViMjRjOGI0LTRjOTktNGViOS"
        "04ZTFiLWFmNzI1MTE5Y2YxZCIKICAgeG1wTU06T3JpZ2luYWxEb2N1bWVudElEPSJ4bXAuZGlkOmEwODY1N2ZhLWYzMDQtNGY3Ni05MDNkLTI"
        "1MTVlZmNkNzNlOSIKICAgZGM6Rm9ybWF0PSJpbWFnZS9wbmciCiAgIEdJTVA6QVBJPSIyLjAiCiAgIEdJTVA6UGxhdGZvcm09IkxpbnV4Igog"
        "ICBHSU1QOlRpbWVTdGFtcD0iMTY2MzI2MzU0MjEwNTAzNSIKICAgR0lNUDpWZXJzaW9uPSIyLjEwLjI0IgogICB0aWZmOk9yaWVudGF0aW9uP"
        "SIxIgogICB4bXA6Q3JlYXRvclRvb2w9IkdJTVAgMi4xMCI+CiAgIDx4bXBNTTpIaXN0b3J5PgogICAgPHJkZjpTZXE+CiAgICAgPHJkZjpsaQ"
        "ogICAgICBzdEV2dDphY3Rpb249InNhdmVkIgogICAgICBzdEV2dDpjaGFuZ2VkPSIvIgogICAgICBzdEV2dDppbnN0YW5jZUlEPSJ4bXAuaWl"
        "kOjY3YWMxMTYyLTM2ODUtNDFlMC05YWU1LThiNGU0ZDU3ZmIzMCIKICAgICAgc3RFdnQ6c29mdHdhcmVBZ2VudD0iR2ltcCAyLjEwIChMaW51"
        "eCkiCiAgICAgIHN0RXZ0OndoZW49IjIwMjItMDktMTVUMjA6Mzk6MDIrMDM6MDAiLz4KICAgIDwvcmRmOlNlcT4KICAgPC94bXBNTTpIaXN0b"
        "3J5PgogIDwvcmRmOkRlc2NyaXB0aW9uPgogPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC"
        "AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICA"
        "gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg"
        "ICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgI"
        "CAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC"
        "AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA"
        "gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAg"
        "ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgI"
        "CAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC"
        "AgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA"
        "gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg"
        "ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgI"
        "CAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogIC"
        "AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA"
        "gICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg"
        "ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgI"
        "CAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgIC"
        "AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICA"
        "gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg"
        "ICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgI"
        "CAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC"
        "AgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA"
        "gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAg"
        "ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgI"
        "CAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC"
        "AgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSJ3Ij8+Mu/dGwAAAAZ"
        "iS0dEAP8AAAAAMyd88wAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+YJDxEnAnCVOhYAABFtSURBVHja7Z3Pa6NFGMefvFtKQzYtlIUG"
        "LLKCRDwYqeuSBvTgK773UHITIZfsIYEeSpAezGEvISw5LJjLXvoHLNKr9lA9KLLLIlgFZS8ua4UWZDEp0lKyOx58W9u1ffPO+847M+/M9wMvw"
        "ppffWaeeX7MM89kCGhJv99nMzMztL+/T8PhkEajEf311180HA7p8PCQjo6O6Pnz50RElM1mKZfL0dTUFM3NzdHVq1fp2rVrND8/T7Ozs3R0dE"
        "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")