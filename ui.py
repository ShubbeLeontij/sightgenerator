#!/usr/bin/env python3
import generator
import reader
from defaults import *
import tkinter as tk
import tkinter.ttk as ttk
import json
import openpyxl
from tktooltip import ToolTip
from tkinter import messagebox
from ttkthemes.themed_tk import ThemedTk
from tkinter import filedialog


class Root(ThemedTk):
    """
    Enlarged tk.Tk class for easier usage. Simpler create objects and tooltips, clear window and bind function on destroy.
    """

    def __init__(self, theme="", title="", geometry="", on_destroy=None, icon=""):
        """
        Function that creates root and sets title, geometry and icon.
        :param title: title text (str)
        :param geometry: window geometry like in tk.Tk (for example "330x200")
        :param on_destroy: function that will run when root destroys
        :param icon: data for creating IconPhoto
        """
        super().__init__(theme=theme)
        self.objects = []
        self.on_destroy = on_destroy
        if title:
            self.title(title)
        if geometry:
            self.geometry(geometry)
        if icon:
            self.iconphoto(True, tk.PhotoImage(data=icon))

    def destroy(self):
        """
        Function that checks any needed actions before destroying root.
        """
        if self.on_destroy is not None:
            self.on_destroy()
        super().destroy()

    def create(self, obj, relx=None, rely=None, relwidth=None, relheight=None, x=None, y=None, width=None, height=None,
               msg=None, **kwargs):
        """
        Function that create some object inside root.
        :param obj: object class
        :param relx: relative x position
        :param rely: relative y position
        :param relwidth: relative width
        :param relheight: relative height
        :param x: x position in pixels
        :param y: y position in pixels
        :param width: width in pixels
        :param height: height in pixels
        :param msg: text in tooltip for this object. None means no tooltip
        :param kwargs: other keyword arguments that should be passed to object init method
        :return: link to created object
        """
        if "text" in kwargs and type(kwargs["text"]) == list:
            msg = kwargs["text"][1]
            kwargs["text"] = kwargs["text"][0]
        self.objects.append(obj(self, **kwargs))
        # Packing the object appropriately
        if relx is not None and rely is not None:
            if relwidth is not None and relwidth is not None:
                self.objects[-1].place(relx=relx, rely=rely, relheight=relheight, relwidth=relwidth)
            elif relwidth is not None and relheight is None:
                self.objects[-1].place(relx=relx, rely=rely, relwidth=relwidth)
            elif relwidth is None and relheight is not None:
                self.objects[-1].place(relx=relx, rely=rely, relheight=relheight)
            else:
                self.objects[-1].place(relx=relx, rely=rely)
        elif x is not None and y is not None:
            if width is not None and width is not None:
                self.objects[-1].place(x=x, y=y, height=height, width=width)
            elif width is not None and height is None:
                self.objects[-1].place(x=x, y=y, width=width)
            elif width is None and height is not None:
                self.objects[-1].place(x=x, y=y, height=height)
            else:
                self.objects[-1].place(x=x, y=y)
        else:
            self.objects[-1].pack()
        if msg:  # Creating tooltip if msg exists
            ToolTip(self.objects[-1], msg=msg, follow=True)
        return self.objects[-1]

    def clear(self, *lists):
        """
        Function that destroys all objects in this root.
        :param lists: list of additional objects
        """
        self.unbind("<Return>")
        for obj in self.objects + [i for sub in lists for i in sub]:
            obj.destroy()
        self.objects = []
        self.update()


class Output(tk.Text):
    """
    Enlarged tk.Text class for using as output box.
    """

    def __init__(self, *args, **kwargs):
        """
        Function that creates object using tk.Text
        """
        super().__init__(*args, **kwargs)

    def print(self, *args, sep="", end='\n'):
        """
        Function that prints some text into text field.
        :param args: text that should be printed
        :param sep: separator between two texts
        :param end: ending after printing
        """
        try:
            output_string = ""
            for i in args:
                if isinstance(i, int):
                    i = str(i)
                elif not isinstance(i, str):
                    i = json.dumps(i)
                output_string += sep + i

            self.config(state=tk.NORMAL)
            self.insert(tk.END, output_string + end)
            self.config(state=tk.DISABLED)
            self.see(tk.END)
            self.master.update()
        except tk.TclError:
            # Widget has been destroyed, ignore the error
            pass

    def clear(self):
        """
        Function that clears whole output field.
        """
        try:
            self.config(state=tk.NORMAL)
            self.delete(1.0, tk.END)
            self.config(state=tk.DISABLED)
        except tk.TclError:
            # Widget has been destroyed, ignore the error
            pass


class Input(ttk.Entry):
    """
    Enlarged ttk.Entry class for using as input box.
    """

    def __init__(self, *args, text="", **kwargs):
        """
        Function that creates object using tk.Entry and fills it with given text.
        :param text: initial text
        """
        super().__init__(*args, **kwargs)
        if text:
            self.insert(0, text)

    def set(self, value):
        """
        Function that sets new value for IntVar.
        :param value: new text
        """
        self.delete(0, tk.END)
        self.insert(0, value)


class Flag(ttk.Checkbutton):
    """
    Enlarged ttk.Checkbutton class for using as input box.
    """

    def __init__(self, *args, default=0, **kwargs):
        """
        Function that creates object using tk.Checkbutton and connects it with IntVar.
        :param default: default variable value
        """
        self.var = tk.IntVar()
        self.var.set(default)
        super().__init__(*args, variable=self.var, **kwargs)

    def get(self):
        """
        Function that returns IntVar value.
        """
        return self.var.get()

    def set(self, value):
        """
        Function that sets new value for IntVar.
        :param value: new IntVar value
        """
        return self.var.set(value)


def main_menu():
    """
    Function that describes tkinter window main menu behavior.
    """

    def run():
        """
        Function that runs reader.
        """
        save_paths()
        reader.reader(0 if mode_flag.get() else 1, sheets=[flag["text"] if flag.get() else None for flag in sheet_flags],
                      _print=output_text.print, _input=lambda *args: None)

    def clear():
        """
        Function that runs cleaner.
        """
        save_paths()
        if messagebox.askokcancel(title=LABELS[LANG]["deleting"], message=LABELS[LANG]["areYouSure"]):
            reader.cleaner(0 if mode_flag.get() else 1, True, _print=output_text.print, _input=lambda *args: None)

    def change_language():
        """
        Function that changes language to the opposite and reloads main menu.
        """
        global LANG
        LANG = "RU" if LANG == "EN" else "EN"
        with open("settings.json", 'r') as f:
            settings = json.load(f)
        settings["lang"] = LANG
        with open("settings.json", 'w') as f:
            json.dump(settings, f, indent=4)
        generator.settings = generator.Settings("settings.json")
        main_menu()

    def save_paths():
        """
        Function that saves path to json file.
        """
        with open("settings.json", 'r') as f:
            settings = json.load(f)
        settings["path"] = path_input.get()
        with open("settings.json", 'w') as f:
            json.dump(settings, f, indent=4)
        generator.settings = generator.Settings("settings.json")
        output_text.print("Paths saved!\n")

    def clear_bindings():
        output_text.print(generator.clear_sight_bindings())
        generator.increment_version()

    # Create output frame with scrollbar
    root.clear()
    output_text = root.create(Output, relx=0.0, rely=0.5, relwidth=0.97, relheight=0.50, bg="black", fg="white")
    scrollbar = root.create(ttk.Scrollbar, relx=0.97, rely=0.50, relwidth=0.03, relheight=0.50, command=output_text.yview)
    output_text["yscrollcommand"] = scrollbar.set
    output_text.clear()

    # Create output mode radiobuttons
    mode_flag = root.create(Flag, relx=0.02, rely=0.30, text=LABELS[LANG]["devMode"])
    mode_flag.set(0)

    # Create checkbuttons for table sheets
    workbook = openpyxl.load_workbook("data.xlsx")
    sheet_flags = []
    ab_list = ["AB", "RB", "CLEAN"]
    sim_list = ["AP", "HE", "HEAT", "APDS", "LASER"]
    i, j, k = tk.IntVar(value=0), tk.IntVar(value=0), tk.IntVar(value=0)
    for sheet_name in workbook.sheetnames:
        if sheet_name in ab_list:
            if not i.get():
                root.create(ttk.Label, relx=0.45, rely=0.15, relwidth=0.10, relheight=0.04,
                            text=LABELS[LANG]["abrb"]).bind("<Button-1>", lambda event: [[((flag.set(0) if i.get() else flag.set(1)) if flag["text"] in ab_list else 0) for flag in sheet_flags], i.set(not i.get())])
            i.set(i.get() + 1)
            sheet_flags.append(root.create(Flag, relx=0.45, rely=0.15 + 0.05 * i.get(), text=sheet_name, default=1))
        elif sheet_name in sim_list:
            if not j.get():
                root.create(ttk.Label, relx=0.57, rely=0.15, relwidth=0.10, relheight=0.04,
                            text=LABELS[LANG]["sim"]).bind("<Button-1>", lambda event: [[((flag.set(0) if j.get() else flag.set(1)) if flag["text"] in sim_list else 0) for flag in sheet_flags], j.set(not j.get())])
            j.set(j.get() + 1)
            sheet_flags.append(root.create(Flag, relx=0.57, rely=0.15 + 0.05 * j.get(), text=sheet_name, default=1))
        else:
            if not k.get():
                root.create(ttk.Label, relx=0.69, rely=0.15, relwidth=0.10, relheight=0.04,
                            text=LABELS[LANG]["other"]).bind("<Button-1>", lambda event: [[((flag.set(0) if k.get() else flag.set(1)) if flag["text"] not in ab_list + sim_list else 0) for flag in sheet_flags], k.set(not k.get())])
            k.set(k.get() + 1)
            sheet_flags.append(root.create(Flag, relx=0.69, rely=0.15 + 0.05 * k.get(), text=sheet_name, default=1))

    # Create action buttons
    root.bind("<Return>", lambda event: run())
    root.create(ttk.Button, relx=0.02, rely=0.35, relwidth=0.17, relheight=0.14, command=run, text=LABELS[LANG]["run"])
    root.create(ttk.Button, relx=0.02, rely=0.21, relwidth=0.41, relheight=0.08, command=settings_menu, text=LABELS[LANG]["changeSettings"])

    # root.create(ttk.Button, relx=0.83, rely=0.02, relwidth=0.15, relheight=0.17, command=save_path, text=LABELS[LANG]["Save"])
    root.create(ttk.Button, relx=0.21, rely=0.31, relwidth=0.22, relheight=0.08, command=clear_bindings, text=LABELS[LANG]["clearBindings"])
    root.create(ttk.Button, relx=0.21, rely=0.41, relwidth=0.22, relheight=0.08, command=clear, text=LABELS[LANG]["clear"])
    root.create(ttk.Button, relx=0.75, rely=0.37, relwidth=0.22, relheight=0.08, command=change_language, text=LABELS[LANG]["changeLanguage"])
    settings = generator.Settings("settings.json")
    root.create(ttk.Label, relx=0.02, rely=0.02, relwidth=0.30, relheight=0.08, text=LABELS[LANG]["path"])
    path_input = root.create(Input, relx=0.34, rely=0.02, relwidth=0.54, relheight=0.08, text=settings.get_setting("path"))
    root.create(ttk.Button, relx=0.89, rely=0.02, relwidth=0.08, relheight=0.08, text="...", command=lambda : path_input.set(filedialog.askdirectory()))


curPreset = ""


def settings_menu():
    """
    Function that describes tkinter window settings menu behavior.
    """

    def save():
        """
        Function that saves all settings to json file.
        """
        def is_parasite_string(line: str) -> bool:
            if line.find("nv") != -1:
                return True
            if line.find("thermal") != -1:
                return True
            if line.find("nightvision") != -1:
                return True
            return False

        load_sight_type("save")
        if curPreset != "":
            settings["preset"] = '\n'.join(line for line in curPreset.split('\n') if not is_parasite_string(line.lower())) if fixThermals.get() else curPreset
        settings["lineSizeMult"] = float(lineSizeMult.get())
        settings["fontSizeMult"] = float(fontSizeMult.get())
        settings["distLength"] = float(distLength.get())
        settings["lineSizeMultSmallZoom"] = float(lineSizeMultSmallZoom.get())
        settings["fontSizeMultSmallZoom"] = float(fontSizeMultSmallZoom.get())
        settings["rangefinderFontSizeMult"] = float(rangefinderFontSizeMult.get())
        settings["rangefinderFontSizeMultSmallZoom"] = float(rangefinderFontSizeMultSmallZoom.get())
        settings["centralCircleSizeSmallZoom"] = float(centralCircleSizeSmallZoom.get())
        settings["bracketsScaleSmallZoom"] = float(bracketsScaleSmallZoom.get())
        settings["badZoomThreshold"] = float(badZoomThreshold.get())
        settings["rangefinderHorizontalScaleSmallZoom"] = float(rangefinderHorizontalScaleSmallZoom.get())
        with open("settings.json", 'w') as f:
            json.dump(settings, f, indent=4)
        generator.settings = generator.Settings("settings.json")

    def preview():
        """
        Function that creates tkinter window for preview for certain sight type and draws whole sight model.
        """
        color = "black"
        canvas_tk = Root(theme="breeze", title=LABELS[LANG]["canvas"] + ' ' + settings["sightTypes"][cur_type_index]["names"][0],
                         geometry="300x300")
        canvas_tk.resizable(False, False)
        canvas = canvas_tk.create(tk.Canvas, x=0, y=0, width=300, height=300, background="lightgrey")

        canvas.create_oval(150 - float(items["centralCircleSize"].get()) / 2,
                           100 - float(items["centralCircleSize"].get()) / 2,
                           150 + float(items["centralCircleSize"].get()) / 2,
                           100 + float(items["centralCircleSize"].get()) / 2, fill=color, outline="")
        if items["rangefinder"].get():
            canvas.create_line(195, 100, 285, 100, fill=color, width=float(lineSizeMult.get()))
            canvas.create_line(195, 131, 210, 131, fill=color, width=float(lineSizeMult.get()))
            canvas.create_line(210, 121, 225, 121, fill=color, width=float(lineSizeMult.get()))
            canvas.create_line(225, 116, 240, 116, fill=color, width=float(lineSizeMult.get()))
            canvas.create_line(240, 112, 255, 112, fill=color, width=float(lineSizeMult.get()))
            canvas.create_line(255, 109, 270, 109, fill=color, width=float(lineSizeMult.get()))
            canvas.create_line(270, 108, 285, 108, fill=color, width=float(lineSizeMult.get()))
            canvas.create_text(202, 136, text="8", fill=color, font=("TkDefaultFont", int(RANGEFINDER_GOOD * 15)))
            canvas.create_text(217, 126, text="12", fill=color, font=("TkDefaultFont", int(RANGEFINDER_GOOD * 15)))
            canvas.create_text(232, 121, text="16", fill=color, font=("TkDefaultFont", int(RANGEFINDER_GOOD * 15)))
            canvas.create_text(247, 117, text="20", fill=color, font=("TkDefaultFont", int(RANGEFINDER_GOOD * 15)))
            canvas.create_text(262, 114, text="24", fill=color, font=("TkDefaultFont", int(RANGEFINDER_GOOD * 15)))
            canvas.create_text(277, 113, text="28", fill=color, font=("TkDefaultFont", int(RANGEFINDER_GOOD * 15)))
        if settings["crosshair"] == "partial":
            canvas.create_line(0, 100, 125, 100, fill=color, width=float(lineSizeMult.get()))
            canvas.create_line(175, 100, 300, 100, fill=color, width=float(lineSizeMult.get()))
            canvas.create_line(150, 0, 150, 75, fill=color, width=float(lineSizeMult.get()))
        if settings["crosshair"] == "drop":
            canvas.create_line(150, 100, 150, 300, fill=color, width=float(lineSizeMult.get()))
        if settings["drawCentralLineHorz"] == "yes":
            canvas.create_line(0, 100, 300, 100, fill=color, width=float(lineSizeMult.get()))
        if settings["drawCentralLineVert"] == "yes":
            canvas.create_line(150, 0, 150, 300, fill=color, width=float(lineSizeMult.get()))
        if settings["sightTypes"][cur_type_index]["centralLines"] == "brackets":
            canvas.create_line(153, 106, 156, 106, fill=color, width=float(lineSizeMult.get()))
            canvas.create_line(144, 106, 147, 106, fill=color, width=float(lineSizeMult.get()))
            canvas.create_line(153, 94, 156, 94, fill=color, width=float(lineSizeMult.get()))
            canvas.create_line(144, 94, 147, 94, fill=color, width=float(lineSizeMult.get()))
            canvas.create_line(156, 94, 156, 106, fill=color, width=float(lineSizeMult.get()))
            canvas.create_line(144, 94, 144, 106, fill=color, width=float(lineSizeMult.get()))
            canvas.create_line(156, 100, 166, 100, fill=color, width=float(lineSizeMult.get()))
            canvas.create_line(134, 100, 144, 100, fill=color, width=float(lineSizeMult.get()))
        elif settings["sightTypes"][cur_type_index]["centralLines"] == "standard":
            canvas.create_line(157, 100, 170, 100, fill=color, width=float(lineSizeMult.get()))
            canvas.create_line(130, 100, 143, 100, fill=color, width=float(lineSizeMult.get()))
        if settings["sightTypes"][cur_type_index]["names"][0] in ["sim_APDS", "AB_f", "RB_f"]:
            speed = 1500
        elif settings["sightTypes"][cur_type_index]["names"][0] in ["sim_AP", "AB", "RB"]:
            speed = 800
        elif settings["sightTypes"][cur_type_index]["names"][0] in ["sim_AP_s", "AB_s", "RB_s"]:
            speed = 500
        else:
            speed = 1000
        dist_list = list(map(int, items["line_dist_list"].get().split()))
        for i in range(1, len(dist_list)):
            if settings["sightTypes"][cur_type_index]["names"][0].count("AB") or settings["sightTypes"][cur_type_index]["names"][0].count("RB"):
                canvas.create_line(150, 50000 * dist_list[i] / speed ** 2 + 100, 150,
                                   50000 * dist_list[i - 1] / speed ** 2 + 100, fill=color,
                                   width=float(lineSizeMult.get()))
            else:
                x1 = 156.25 - 5000 / dist_list[i] if dist_list[i] else 150
                y1 = 5000 / dist_list[i] + 50000 * dist_list[i] / speed ** 2 + 93.75 if dist_list[i] else 100
                x2 = 156.25 - 5000 / dist_list[i - 1] if dist_list[i - 1] else 150
                y2 = 5000 / dist_list[i - 1] + 50000 * dist_list[i - 1] / speed ** 2 + 93.75 if dist_list[
                    i - 1] else 100
                canvas.create_line(x1, y1, x2, y2, fill=color, width=float(lineSizeMult.get()))
        for dist, circle_dict in settings["sightTypes"][cur_type_index]["circles"].items():
            if settings["sightTypes"][cur_type_index]["names"][0].count("AB") or settings["sightTypes"][cur_type_index]["names"][0].count("RB"):
                x, y = 150, 50000 * int(dist) / speed ** 2 + 100
            else:
                x, y = 156.25 - 5000 / int(dist), 5000 / int(dist) + 50000 * int(dist) / speed ** 2 + 93.75
            canvas.create_oval(x - circle_dict["size"] / 2, y - circle_dict["size"] / 2, x + circle_dict["size"] / 2,
                               y + circle_dict["size"] / 2, fill=color, outline="")
            canvas.create_text(x - circle_dict["textPos"][0] * 10, y + circle_dict["textPos"][1] * 10,
                               text=dist if int(dist) < 100 else str(int(dist) // 100),
                               font=("TkDefaultFont", int(circle_dict["textSize"] * float(fontSizeMult.get()) * 15)),
                               fill=color)
        for dist in list(map(int, items["small_dist_list"].get().split())):
            if settings["sightTypes"][cur_type_index]["names"][0].count("AB") or settings["sightTypes"][cur_type_index]["names"][0].count("RB"):
                x, y = 150, 50000 * int(dist) / speed ** 2 + 100
            else:
                x, y = 156.25 - 5000 / int(DIST_POINT), 50000 * int(dist) / speed ** 2 + 100
            canvas.create_line(x, y, x + float(1000 * DIST_MULT * float(distLength.get())), y, fill=color,
                               width=float(lineSizeMult.get()))
        for dist in list(map(int, items["right_dist_list"].get().split())):
            if settings["sightTypes"][cur_type_index]["names"][0].count("AB") or settings["sightTypes"][cur_type_index]["names"][0].count("RB"):
                x, y = 150, 50000 * int(dist) / speed ** 2 + 100
            else:
                x, y = 156.25 - 5000 / int(DIST_POINT), 50000 * int(dist) / speed ** 2 + 100
            canvas.create_line(x, y, x + 1000 * float(distLength.get()), y, fill=color, width=float(lineSizeMult.get()))
            canvas.create_text(x + 1000 * (float(distLength.get()) + DIST_INDENT), y, text=dist if int(dist) < 100 else str(int(dist) // 100), font=("TkDefaultFont", int(float(fontSizeMult.get()) * 10)), fill=color)
        for dist in list(map(int, items["left_dist_list"].get().split())):
            if settings["sightTypes"][cur_type_index]["names"][0].count("AB") or settings["sightTypes"][cur_type_index]["names"][0].count("RB"):
                x, y = 150, 50000 * int(dist) / speed ** 2 + 100
            else:
                x, y = 156.25 - 5000 / int(DIST_POINT), 50000 * int(dist) / speed ** 2 + 100
            canvas.create_line(x, y, x - 1000 * float(distLength.get()), y, fill=color, width=float(lineSizeMult.get()))
            canvas.create_text(x - 1000 * (float(distLength.get()) + DIST_INDENT), y, text=dist if int(dist) < 100 else str(int(dist) // 100), font=("TkDefaultFont", int(float(fontSizeMult.get()) * 10)), fill=color)

        canvas_tk.mainloop()

    def load_sight_type(event):
        """
        Function that shows all settings for certain sight type.
        """

        def edit_circles():
            """
            Function that creates tkinter window for editing circles settings.
            """

            def save_circles():
                """
                Function that saves circles settings to program memory (not json file) after closing tkinter window.
                """
                settings["sightTypes"][cur_type_index]["circles"] = dict()
                for d in list(circles.values()):
                    try:
                        cur_dist = d["dist"].get()
                        settings["sightTypes"][cur_type_index]["circles"][cur_dist] = dict()
                        settings["sightTypes"][cur_type_index]["circles"][cur_dist]["size"] = float(d["size"].get())
                        settings["sightTypes"][cur_type_index]["circles"][cur_dist]["textPos"] = list(map(float, d["textPos"].get().split(',')))
                        settings["sightTypes"][cur_type_index]["circles"][cur_dist]["textSize"] = float(d["textSize"].get())
                    except:
                        if crosshair_var.get() and central_lines_var:
                            pass  # without this python garbage collector will kill this variable

            def create_row(i, dist=None):
                """
                Function that creates another row for circle.
                :param i: index of circle
                :param dist: distance of this circle
                """
                d = dict()
                d["button"] = edit_tk.create(ttk.Button, x=3, y=45 + 33 * i, width=30, height=30, text='🗑️',
                                             command=lambda: ([obj.destroy() for obj in list(circles[i].values())],
                                                              circles.__setitem__(i, dict())))
                d["dist"] = edit_tk.create(Input, x=36, y=45 + 33 * i, width=60, height=30,
                                           text=dist if dist else str(i))
                d["size"] = edit_tk.create(Input, x=99, y=45 + 33 * i, width=60, height=30, text=str(
                    settings["sightTypes"][cur_type_index]["circles"][dist]["size"]) if dist else "1.0")
                d["textPos"] = edit_tk.create(Input, x=162, y=45 + 33 * i, width=72, height=30, text=", ".join(map(str, settings["sightTypes"][cur_type_index]["circles"][dist]["textPos"] if dist else [0.0, 0.0])))
                d["textSize"] = edit_tk.create(Input, x=237, y=45 + 33 * i, width=60, height=30, text=str(settings["sightTypes"][cur_type_index]["circles"][dist]["textSize"]) if dist else "1.0")
                return d

            edit_tk = Root(theme="breeze", title=LABELS[LANG]["editCircles"], on_destroy=save_circles)
            edit_tk.resizable(False, False)

            edit_tk.create(ttk.Button, x=3, y=3, width=30, height=30, text='+', command=lambda: (
                circles.__setitem__(i.get(), create_row(i.get())), i.set(i.get() + 1),
                edit_tk.geometry("300x" + str(45 + 33 * i.get()))))
            edit_tk.create(ttk.Label, x=36, y=3, text=LABELS[LANG]["distance"])
            edit_tk.create(ttk.Label, x=99, y=3, text=LABELS[LANG]["size"])
            edit_tk.create(ttk.Label, x=153, y=3, text=LABELS[LANG]["textPos"])
            edit_tk.create(ttk.Label, x=240, y=3, text=LABELS[LANG]["textSize"])
            circles = dict()
            i = tk.IntVar()
            i.set(0)
            for dist in settings["sightTypes"][cur_type_index]["circles"].keys():
                circles[i.get()] = create_row(i.get(), dist)
                i.set(i.get() + 1)
            edit_tk.geometry("300x" + str(45 + 33 * i.get()))
            edit_tk.mainloop()

        global cur_type_index
        if event:
            settings["sightTypes"][cur_type_index]["rangefinder"] = items["rangefinder"].get()
            settings["sightTypes"][cur_type_index]["centralCircleSize"] = float(items["centralCircleSize"].get())
            settings["sightTypes"][cur_type_index]["right_dist_list"] = list(
                map(int, items["right_dist_list"].get().split()))
            settings["sightTypes"][cur_type_index]["left_dist_list"] = list(
                map(int, items["left_dist_list"].get().split()))
            settings["sightTypes"][cur_type_index]["small_dist_list"] = list(
                map(int, items["small_dist_list"].get().split()))
            settings["sightTypes"][cur_type_index]["line_dist_list"] = list(
                map(int, items["line_dist_list"].get().split()))
        for obj in items.values():
            obj.destroy()
        for s_type in settings["sightTypes"]:
            if types_box.get() in s_type["names"]:
                cur_type_index = settings["sightTypes"].index(s_type)
                break
        items["aliases_label"] = root.create(ttk.Label, relx=0.66, rely=0.29, relwidth=0.31, relheight=0.04, text=LABELS[LANG]["aliases"] + ", ".join(settings["sightTypes"][cur_type_index]["names"]), justify=tk.LEFT, anchor="nw", wraplength=200)
        items["edit_button"] = root.create(ttk.Button, relx=0.66, rely=0.34, relwidth=0.31, relheight=0.05, text=LABELS[LANG]["editSimCircles"], command=edit_circles)
        items["rangefinder"] = root.create(Flag, relx=0.66, rely=0.40, text=LABELS[LANG]["stadiametricRangefinder"], default=1 if settings["sightTypes"][cur_type_index]["rangefinder"] else 0)

        items["right_dist_list_label"] = root.create(ttk.Label, relx=0.66, rely=0.44, text=LABELS[LANG]["rightDistList"])
        items["right_dist_list"] = root.create(Input, relx=0.66, rely=0.47, relwidth=0.31, relheight=0.05, text=' '.join(map(str, settings["sightTypes"][cur_type_index]["right_dist_list"])))
        items["left_dist_list_label"] = root.create(ttk.Label, relx=0.66, rely=0.53, text=LABELS[LANG]["leftDistList"])
        items["left_dist_list"] = root.create(Input, relx=0.66, rely=0.56, relwidth=0.31, relheight=0.05, text=' '.join(map(str, settings["sightTypes"][cur_type_index]["left_dist_list"])))
        items["small_dist_list_label"] = root.create(ttk.Label, relx=0.66, rely=0.62, text=LABELS[LANG]["smallDistList"])
        items["small_dist_list"] = root.create(Input, relx=0.66, rely=0.65, relwidth=0.31, relheight=0.05, text=' '.join(map(str, settings["sightTypes"][cur_type_index]["small_dist_list"])))
        items["line_dist_list_label"] = root.create(ttk.Label, relx=0.66, rely=0.71, text=LABELS[LANG]["lineDistList"])
        items["line_dist_list"] = root.create(Input, relx=0.66, rely=0.74, relwidth=0.31, relheight=0.05, text=' '.join(map(str, settings["sightTypes"][cur_type_index]["line_dist_list"])))

        items["centralCircle_label"] = root.create(ttk.Label, relx=0.66, rely=0.80, text=LABELS[LANG]["centralCircleSize"])
        items["centralCircleSize"] = root.create(Input, relx=0.86, rely=0.80, relwidth=0.11, relheight=0.05, text=settings["sightTypes"][cur_type_index]["centralCircleSize"])
        
        # Update central lines variable based on sight type settings
        if settings["sightTypes"][cur_type_index]["centralLines"] == "brackets":
            central_lines_var.set(2)
        elif settings["sightTypes"][cur_type_index]["centralLines"] == "standard":
            central_lines_var.set(1)
        elif settings["sightTypes"][cur_type_index]["centralLines"] == "no":
            central_lines_var.set(0)
        else:
            central_lines_var.set(-1)

    def no_crosshair():
        """
        Function for saving crosshair setting.
        """
        settings["drawCentralLineVert"] = "no"
        settings["drawCentralLineHorz"] = "no"
        settings["crosshair"] = ""

    def partial_crosshair():
        """
        Function for saving crosshair setting.
        """
        settings["drawCentralLineVert"] = "no"
        settings["drawCentralLineHorz"] = "no"
        settings["crosshair"] = "partial"

    def full_crosshair():
        """
        Function for saving crosshair setting.
        """
        settings["drawCentralLineVert"] = "yes"
        settings["drawCentralLineHorz"] = "yes"
        settings["crosshair"] = ""

    def drop_line_crosshair():
        """
        Function for saving crosshair setting.
        """
        settings["drawCentralLineVert"] = "no"
        settings["drawCentralLineHorz"] = "no"
        settings["crosshair"] = "drop"

    def update_central_lines(line_type):
        """
        Function for updating central lines setting for current sight type.
        """
        global cur_type_index
        if cur_type_index is not None and cur_type_index < len(settings["sightTypes"]):
            settings["sightTypes"][cur_type_index]["centralLines"] = line_type

    def load_preset():
        global curPreset
        with open(filedialog.askopenfilename(), "r") as f:
            curPreset = "".join(f.readlines()[1:])


    with open("settings.json", 'r') as f:
        settings = json.loads(f.read())
    
    # Initialize current type index
    global cur_type_index
    cur_type_index = 0
    
    root.clear()
    root.bind("<Return>", lambda event: (save(), main_menu()))
    # Top row - main action buttons
    root.create(ttk.Button, relx=0.02, rely=0.02, relwidth=0.20, relheight=0.10, text=LABELS[LANG]["loadPreset"], command=load_preset)
    root.create(ttk.Button, relx=0.24, rely=0.02, relwidth=0.15, relheight=0.10, command=preview, text=LABELS[LANG]["preview"])
    root.create(ttk.Button, relx=0.41, rely=0.02, relwidth=0.30, relheight=0.10, command=lambda: (save(), main_menu()), text=LABELS[LANG]["saveSettings"])
    fixThermals = root.create(Flag, relx=0.73, rely=0.02, text=LABELS[LANG]["fixThermals"])
    
    # Left column - Basic settings and crosshair types
    root.create(ttk.Label, relx=0.02, rely=0.15, text="=== " + LABELS[LANG]["basicSettings"] + " ===", font=("TkDefaultFont", 10, "bold"))
    root.create(ttk.Label, relx=0.02, rely=0.21, text=LABELS[LANG]["lineSizeMult"])
    lineSizeMult = root.create(Input, relx=0.20, rely=0.21, relwidth=0.08, relheight=0.05, text=settings["lineSizeMult"])
    root.create(ttk.Label, relx=0.02, rely=0.27, text=LABELS[LANG]["fontSizeMult"])
    fontSizeMult = root.create(Input, relx=0.20, rely=0.27, relwidth=0.08, relheight=0.05, text=settings["fontSizeMult"])
    root.create(ttk.Label, relx=0.02, rely=0.33, text=LABELS[LANG]["distLength"])
    distLength = root.create(Input, relx=0.20, rely=0.33, relwidth=0.08, relheight=0.05, text=settings["distLength"])
    root.create(ttk.Label, relx=0.02, rely=0.39, text=LABELS[LANG]["badZoomThreshold"])
    badZoomThreshold = root.create(Input, relx=0.20, rely=0.39, relwidth=0.08, relheight=0.05, text=settings.get("badZoomThreshold", 3.49))

    # Vertical separator
    root.create(ttk.Separator, relx=0.30, rely=0.14, relwidth=0.002, relheight=0.80, orient='vertical')
    
    # Central Lines (crosshair settings)
    root.create(ttk.Label, relx=0.02, rely=0.45, text="=== " + LABELS[LANG]["centralLines"] + " ===", font=("TkDefaultFont", 10, "bold"))
    
    # Initialize variables for both crosshair and sight type central lines
    crosshair_var = tk.IntVar()
    central_lines_var = tk.IntVar()
    
    # Set crosshair variable based on current settings
    if settings["drawCentralLineVert"] == "yes" and settings["drawCentralLineHorz"] == "yes":
        crosshair_var.set(3)
    elif settings["crosshair"] == "partial":
        crosshair_var.set(2)
    elif settings["crosshair"] == "drop":
        crosshair_var.set(1)
    elif settings["crosshair"] == "" or settings["crosshair"] == "no" or settings["crosshair"] == "false":
        crosshair_var.set(0)
    else:
        crosshair_var.set(-1)
    
    root.create(ttk.Radiobutton, relx=0.02, rely=0.51, variable=crosshair_var, value=0, command=no_crosshair,
                text=LABELS[LANG]["noCrosshair"])
    root.create(ttk.Radiobutton, relx=0.02, rely=0.55, variable=crosshair_var, value=1, command=drop_line_crosshair,
                text=LABELS[LANG]["dropLineCrosshair"][0], 
                msg=LABELS[LANG]["dropLineCrosshair"][1])
    root.create(ttk.Radiobutton, relx=0.02, rely=0.59, variable=crosshair_var, value=2, command=partial_crosshair,
                text=LABELS[LANG]["partialCrosshair"])
    root.create(ttk.Radiobutton, relx=0.02, rely=0.63, variable=crosshair_var, value=3, command=full_crosshair,
                text=LABELS[LANG]["fullCrosshair"])
    
    # Sight Type Central Lines (below crosshair settings)
    root.create(ttk.Label, relx=0.02, rely=0.68, text=LABELS[LANG]["sightType"], font=("TkDefaultFont", 9, "bold"))
    root.create(ttk.Radiobutton, relx=0.02, rely=0.72, variable=central_lines_var, value=0, command=lambda: update_central_lines("no"),
                text=LABELS[LANG]["noCentralCrosshair"])
    root.create(ttk.Radiobutton, relx=0.02, rely=0.76, variable=central_lines_var, value=1, command=lambda: update_central_lines("standard"), 
                text=LABELS[LANG]["standardCrosshair"])
    root.create(ttk.Radiobutton, relx=0.02, rely=0.80, variable=central_lines_var, value=2, command=lambda: update_central_lines("brackets"),
                text=LABELS[LANG]["bracketsCrosshair"])

    # Middle column - Small zoom settings
    root.create(ttk.Label, relx=0.33, rely=0.15, text="=== " + LABELS[LANG]["smallZoomSettings"] + " ===", font=("TkDefaultFont", 10, "bold"))
    root.create(ttk.Label, relx=0.33, rely=0.21, text=LABELS[LANG]["lineSizeSmallZoom"])
    lineSizeMultSmallZoom = root.create(Input, relx=0.53, rely=0.21, relwidth=0.08, relheight=0.05, text=settings.get("lineSizeMultSmallZoom", 1.3))
    root.create(ttk.Label, relx=0.33, rely=0.28, text=LABELS[LANG]["fontSizeSmallZoom"])
    fontSizeMultSmallZoom = root.create(Input, relx=0.53, rely=0.28, relwidth=0.08, relheight=0.05, text=settings.get("fontSizeMultSmallZoom", 2.0))
    root.create(ttk.Label, relx=0.33, rely=0.35, text=LABELS[LANG]["rangefinderFontMult"])
    rangefinderFontSizeMult = root.create(Input, relx=0.53, rely=0.35, relwidth=0.08, relheight=0.05, text=settings.get("rangefinderFontSizeMult", 1.0))
    root.create(ttk.Label, relx=0.33, rely=0.42, text=LABELS[LANG]["rangefinderFontSmall"])
    rangefinderFontSizeMultSmallZoom = root.create(Input, relx=0.53, rely=0.42, relwidth=0.08, relheight=0.05, text=settings.get("rangefinderFontSizeMultSmallZoom", 1.2))
    root.create(ttk.Label, relx=0.33, rely=0.49, text=LABELS[LANG]["centralCircleSmall"])
    centralCircleSizeSmallZoom = root.create(Input, relx=0.53, rely=0.49, relwidth=0.08, relheight=0.05, text=settings.get("centralCircleSizeSmallZoom", 7.0))
    root.create(ttk.Label, relx=0.33, rely=0.56, text=LABELS[LANG]["bracketsScaleSmall"])
    bracketsScaleSmallZoom = root.create(Input, relx=0.53, rely=0.56, relwidth=0.08, relheight=0.05, text=settings.get("bracketsScaleSmallZoom", 2.0))
    root.create(ttk.Label, relx=0.33, rely=0.63, text=LABELS[LANG]["rangefinderHScaleSmall"])
    rangefinderHorizontalScaleSmallZoom = root.create(Input, relx=0.53, rely=0.63, relwidth=0.08, relheight=0.05, text=settings.get("rangefinderHorizontalScaleSmallZoom", 1.0))
    
    # Vertical separator
    root.create(ttk.Separator, relx=0.63, rely=0.14, relwidth=0.002, relheight=0.80, orient='vertical')

    # Right column - Sight types and controls
    root.create(ttk.Label, relx=0.66, rely=0.15, text="=== " + LABELS[LANG]["sightConfiguration"] + " ===", font=("TkDefaultFont", 10, "bold"))
    root.create(ttk.Label, relx=0.66, rely=0.20, text=LABELS[LANG]["sightType"])
    sight_types = [s_type["names"][0] for s_type in settings["sightTypes"]]
    items = {}
    types_box = root.create(ttk.Combobox, relx=0.66, rely=0.23, relwidth=0.31, relheight=0.05, values=sight_types,
                            state="readonly")
    types_box.set(sight_types[0])
    types_box.bind("<<ComboboxSelected>>", load_sight_type)

    load_sight_type(None)


if __name__ == "__main__":
    # Load labels, create main window and enter mainloop
    try:
        with open("lang.txt", 'r') as langfile:
            LABELS["CUSTOM"] = json.load(langfile)
            LANG = "CUSTOM"
    except:
        with open("settings.json", 'r') as f:
            settings = json.load(f)
        if settings.get("lang") == "EN":
            LANG = "EN"
        elif settings.get("lang") == "RU":
            LANG = "RU"
        else:
            LANG = "EN"
    root = Root(theme="breeze", title=LABELS[LANG]["title"], geometry="1000x650", icon=ICON)
    main_menu()
    root.mainloop()
