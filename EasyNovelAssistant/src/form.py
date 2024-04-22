﻿import tkinter as tk

from const import Const
from gen_area import GenArea
from input_area import InputArea
from menu.file_menu import FileMenu
from menu.gen_menu import GenMenu
from menu.help_menu import HelpMenu
from menu.model_menu import ModelMenu
from menu.sample_menu import SampleMenu
from output_area import OutputArea
from tkinterdnd2 import DND_FILES, TkinterDnD


class Form:
    WIN_MIN_W = 640
    WIN_MIN_H = 480

    def __init__(self, ctx):
        self.ctx = ctx

        self.win = TkinterDnD.Tk()
        self.win.drop_target_register(DND_FILES)
        self.win.title("EasyNovelAssistant")
        self.win.minsize(self.WIN_MIN_W, self.WIN_MIN_H)
        win_geom = f'{self.ctx["win_width"]}x{self.ctx["win_height"]}'
        if self.ctx["win_x"] != 0 or self.ctx["win_y"] != 0:
            win_geom += f'+{ctx["win_x"]}+{self.ctx["win_y"]}'
        self.win.geometry(win_geom)
        self.win.protocol("WM_DELETE_WINDOW", self.ctx.finalize)
        self.win.dnd_bind("<<Drop>>", lambda e: self.ctx.dnd_file(e))

        self.menu_bar = tk.Menu(self.win)
        self.win.config(menu=self.menu_bar)

        self.file_menu = FileMenu(self, ctx)
        self.model_menu = ModelMenu(self, ctx)
        self.gen_menu = GenMenu(self, ctx)
        self.sample_menu = SampleMenu(self, ctx)
        self.help_menu = HelpMenu(self, ctx)

        self.pane_h = tk.PanedWindow(self.win, orient=tk.HORIZONTAL, sashpad=2)

        self.input_area = InputArea(self.pane_h, ctx)

        self.pane_v = tk.PanedWindow(self.pane_h, orient=tk.VERTICAL, sashpad=2)
        self.pane_h.add(self.pane_v, width=ctx["pane_v_width"], minsize=Const.AREA_MIN_SIZE, stretch="always")

        self.output_area = OutputArea(self.pane_v, ctx)
        self.gen_area = GenArea(self.pane_v, ctx)

        self.pane_h.pack(fill=tk.BOTH, expand=True)

        self.input_area.set_text(ctx["input_text"])

    def run(self):
        self.win.lift()
        self.win.mainloop()

    def update_title(self):
        title = "EasyNovelAssistant"
        if self.ctx.kobold_cpp.model_name is not None:
            title += f" - {self.ctx.kobold_cpp.model_name}"
        if self.ctx.generator.enabled:
            title += " [生成中]"
        if self.ctx.file_path is not None:
            title += f" - {self.ctx.file_path}"
        self.win.title(title)

    def update_config(self):
        ctx = self.ctx
        ctx["win_width"] = self.win.winfo_width()
        ctx["win_height"] = self.win.winfo_height()
        ctx["win_x"] = self.win.winfo_x()
        ctx["win_y"] = self.win.winfo_y()

        input_area_width = self.input_area.text_area.winfo_width()
        if input_area_width != -1:
            ctx["input_area_width"] = input_area_width

        pane_v_width = self.pane_v.winfo_width()
        if pane_v_width != -1:
            ctx["pane_v_width"] = pane_v_width

        gen_area_height = self.gen_area.text_area.winfo_height()
        if gen_area_height != -1:
            ctx["gen_area_height"] = gen_area_height

        ctx["input_text"] = self.input_area.get_text()
