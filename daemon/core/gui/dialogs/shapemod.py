"""
shape input dialog
"""
import tkinter as tk
from tkinter import font, ttk

from core.gui.dialogs.colorpicker import ColorPickerDialog
from core.gui.dialogs.dialog import Dialog
from core.gui.graph import tags
from core.gui.graph.shapeutils import is_draw_shape, is_shape_text
from core.gui.themes import FRAME_PAD, PADX, PADY

FONT_SIZES = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]
BORDER_WIDTH = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


class ShapeDialog(Dialog):
    def __init__(self, master, app, shape):
        if is_draw_shape(shape.shape_type):
            title = "Add Shape"
        else:
            title = "Add Text"
        super().__init__(master, app, title, modal=True)
        self.canvas = app.canvas
        self.fill = None
        self.border = None
        self.shape = shape
        data = shape.shape_data
        self.shape_text = tk.StringVar(value=data.text)
        self.font = tk.StringVar(value=data.font)
        self.font_size = tk.IntVar(value=data.font_size)
        self.text_color = data.text_color
        fill_color = data.fill_color
        if not fill_color:
            fill_color = "#CFCFFF"
        self.fill_color = fill_color
        self.border_color = data.border_color
        self.border_width = tk.IntVar(value=0)
        self.bold = tk.BooleanVar(value=data.bold)
        self.italic = tk.BooleanVar(value=data.italic)
        self.underline = tk.BooleanVar(value=data.underline)
        self.draw()

    def draw(self):
        self.top.columnconfigure(0, weight=1)
        self.draw_label_options()
        if is_draw_shape(self.shape.shape_type):
            self.draw_shape_options()
        self.draw_spacer()
        self.draw_buttons()

    def draw_label_options(self):
        label_frame = ttk.LabelFrame(self.top, text="Label", padding=FRAME_PAD)
        label_frame.grid(sticky="ew")
        label_frame.columnconfigure(0, weight=1)

        entry = ttk.Entry(label_frame, textvariable=self.shape_text)
        entry.grid(sticky="ew", pady=PADY)

        # font options
        frame = ttk.Frame(label_frame)
        frame.grid(sticky="nsew", pady=PADY)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        combobox = ttk.Combobox(
            frame,
            textvariable=self.font,
            values=sorted(font.families()),
            state="readonly",
        )
        combobox.grid(row=0, column=0, sticky="nsew")
        combobox = ttk.Combobox(
            frame, textvariable=self.font_size, values=FONT_SIZES, state="readonly"
        )
        combobox.grid(row=0, column=1, padx=PADX, sticky="nsew")
        button = ttk.Button(frame, text="Color", command=self.choose_text_color)
        button.grid(row=0, column=2, sticky="nsew")

        # style options
        frame = ttk.Frame(label_frame)
        frame.grid(sticky="ew")
        for i in range(3):
            frame.columnconfigure(i, weight=1)
        button = ttk.Checkbutton(frame, variable=self.bold, text="Bold")
        button.grid(row=0, column=0, sticky="ew")
        button = ttk.Checkbutton(frame, variable=self.italic, text="Italic")
        button.grid(row=0, column=1, padx=PADX, sticky="ew")
        button = ttk.Checkbutton(frame, variable=self.underline, text="Underline")
        button.grid(row=0, column=2, sticky="ew")

    def draw_shape_options(self):
        label_frame = ttk.LabelFrame(self.top, text="Shape", padding=FRAME_PAD)
        label_frame.grid(sticky="ew", pady=PADY)
        label_frame.columnconfigure(0, weight=1)

        frame = ttk.Frame(label_frame)
        frame.grid(sticky="ew")
        for i in range(1, 3):
            frame.columnconfigure(i, weight=1)
        label = ttk.Label(frame, text="Fill Color")
        label.grid(row=0, column=0, padx=PADX, sticky="w")
        self.fill = ttk.Label(frame, text=self.fill_color, background=self.fill_color)
        self.fill.grid(row=0, column=1, sticky="ew", padx=PADX)
        button = ttk.Button(frame, text="Color", command=self.choose_fill_color)
        button.grid(row=0, column=2, sticky="ew")

        label = ttk.Label(frame, text="Border Color")
        label.grid(row=1, column=0, sticky="w", padx=PADX)
        self.border = ttk.Label(
            frame, text=self.border_color, background=self.border_color
        )
        self.border.grid(row=1, column=1, sticky="ew", padx=PADX)
        button = ttk.Button(frame, text="Color", command=self.choose_border_color)
        button.grid(row=1, column=2, sticky="ew")

        frame = ttk.Frame(label_frame)
        frame.grid(sticky="ew", pady=PADY)
        frame.columnconfigure(1, weight=1)
        label = ttk.Label(frame, text="Border Width")
        label.grid(row=0, column=0, sticky="w", padx=PADX)
        combobox = ttk.Combobox(
            frame, textvariable=self.border_width, values=BORDER_WIDTH, state="readonly"
        )
        combobox.grid(row=0, column=1, sticky="nsew")

    def draw_buttons(self):
        frame = ttk.Frame(self.top)
        frame.grid(sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        button = ttk.Button(frame, text="Add shape", command=self.click_add)
        button.grid(row=0, column=0, sticky="ew", padx=PADX)
        button = ttk.Button(frame, text="Cancel", command=self.cancel)
        button.grid(row=0, column=1, sticky="ew")

    def choose_text_color(self):
        color_picker = ColorPickerDialog(self, self.app, self.text_color)
        self.text_color = color_picker.askcolor()

    def choose_fill_color(self):
        color_picker = ColorPickerDialog(self, self.app, self.fill_color)
        color = color_picker.askcolor()
        self.fill_color = color
        self.fill.config(background=color, text=color)

    def choose_border_color(self):
        color_picker = ColorPickerDialog(self, self.app, self.border_color)
        color = color_picker.askcolor()
        self.border_color = color
        self.border.config(background=color, text=color)

    def cancel(self):
        self.shape.delete()
        self.canvas.shapes.pop(self.shape.id)
        self.destroy()

    def click_add(self):
        if is_draw_shape(self.shape.shape_type):
            self.add_shape()
        elif is_shape_text(self.shape.shape_type):
            self.add_text()
        self.destroy()

    def make_font(self):
        """
        create font for text or shape label
        :return: list(font specifications)
        """
        size = int(self.font_size.get())
        text_font = [self.font.get(), size]
        if self.bold.get():
            text_font.append("bold")
        if self.italic.get():
            text_font.append("italic")
        if self.underline.get():
            text_font.append("underline")
        return text_font

    def save_text(self):
        """
        save info related to text or shape label

        :return: nothing
        """
        data = self.shape.shape_data
        data.text = self.shape_text.get()
        data.font = self.font.get()
        data.font_size = int(self.font_size.get())
        data.text_color = self.text_color
        data.bold = self.bold.get()
        data.italic = self.italic.get()
        data.underline = self.underline.get()

    def save_shape(self):
        """
        save info related to shape

        :return: nothing
        """
        data = self.shape.shape_data
        data.fill_color = self.fill_color
        data.border_color = self.border_color
        data.border_width = int(self.border_width.get())

    def add_text(self):
        """
        add text to canvas

        :return: nothing
        """
        text = self.shape_text.get()
        text_font = self.make_font()
        self.canvas.itemconfig(
            self.shape.id, text=text, fill=self.text_color, font=text_font
        )
        self.save_text()

    def add_shape(self):
        self.canvas.itemconfig(
            self.shape.id,
            fill=self.fill_color,
            dash="",
            outline=self.border_color,
            width=int(self.border_width.get()),
        )
        shape_text = self.shape_text.get()
        size = int(self.font_size.get())
        x0, y0, x1, y1 = self.canvas.bbox(self.shape.id)
        _y = y0 + 1.5 * size
        _x = (x0 + x1) / 2
        text_font = self.make_font()
        if self.shape.text_id is None:
            self.shape.text_id = self.canvas.create_text(
                _x,
                _y,
                text=shape_text,
                fill=self.text_color,
                font=text_font,
                tags=tags.SHAPE_TEXT,
            )
            self.shape.created = True
        else:
            self.canvas.itemconfig(
                self.shape.text_id,
                text=shape_text,
                fill=self.text_color,
                font=text_font,
            )
        self.save_text()
        self.save_shape()
