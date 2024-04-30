﻿import tkinter as tk
from tkinter import scrolledtext

from const import Const
from path import Path


class OutputArea:
    def __init__(self, parent, ctx):
        self.ctx = ctx
        self.text_area = scrolledtext.ScrolledText(parent, undo=True, maxundo=-1)
        self.text_area.configure(Const.TEXT_AREA_CONFIG)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        parent.add(self.text_area, minsize=Const.AREA_MIN_SIZE, stretch="always")

        self.ctx_menu = tk.Menu(self.text_area, tearoff=False)
        self.text_area.bind("<Button-3>", self._on_ctx_menu)

        self.text_area.bind("<Button-2>", self._on_middle_click)

        self.counter = 0

    def append_text(self, text):
        self.text_area.insert(tk.END, text)
        if self.ctx["auto_scroll"]:
            self.text_area.see(tk.END)

    def append_output(self, output):
        if output is None:
            return
        output = self.ctx["output_format"].format(self.counter, output)
        self.counter += 1
        self.append_text(output)

        with open(Path.output_log, "a", encoding="utf-8-sig") as f:
            f.write(output)

    def clear(self):
        self.text_area.delete("1.0", tk.END)
        self.counter = 0

    def _speech(self, e):
        line_num = self.text_area.index(f"@{e.x},{e.y}").split(".")[0]
        text = self.text_area.get(f"{line_num}.0", f"{line_num}.end") + "\n"
        self.ctx.style_bert_vits2.generate(text)

    def _send_to_input(self, e):
        text = None
        if self.text_area.tag_ranges(tk.SEL):
            text = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        else:
            line_num = self.text_area.index(f"@{e.x},{e.y}").split(".")[0]
            text = self.text_area.get(f"{line_num}.0", f"{line_num}.end") + "\n"
        self.ctx.input_area.insert_text(text)

    def _on_middle_click(self, e):
        if self.ctx["middle_click_speech"]:
            self._speech(e)
        else:
            self._send_to_input(e)
        return "break"

    def _on_ctx_menu(self, event):
        self.ctx_menu.delete(0, tk.END)

        if self.ctx.style_bert_vits2.models is None:
            self.ctx.style_bert_vits2.get_models()

        if self.ctx.style_bert_vits2.models is not None:
            self.ctx_menu.add_command(label="読み上げる", command=lambda: self._speech(event))

        self.ctx_menu.add_command(label="入力欄に送る", command=lambda: self._send_to_input(event))

        self.ctx_menu.add_separator()

        self.ctx_menu.add_command(label="クリア", command=self.clear)

        self.text_area.mark_set(tk.INSERT, f"@{event.x},{event.y}")
        self.ctx_menu.post(event.x_root, event.y_root)
