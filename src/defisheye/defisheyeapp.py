#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Defisheye algorithm.

Developed by: E. S. Pereira.
e-mail: pereira.somoza@gmail.com

Based in the work of F. Weinhaus.
http://www.fmwconcepts.com/imagemagick/defisheye/index.php

Copyright [2019] [E. S. Pereira]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import pkg_resources
import tkinter as tk
import tkinter.ttk as ttk
import pygubu
from tkinter.filedialog import askopenfilename
import cv2
from PIL import Image, ImageTk

from .defisheye import Defisheye


class DefisheyeApp:
    def __init__(self, **kwargs) -> None:
        self.root = tk.Tk()

        self.builder = pygubu.Builder()
        self._ui = pkg_resources.resource_filename(
            "defisheye", f"gui/main.ui")

        self.icon = pkg_resources.resource_filename(
            "defisheye", f"gui/camera.png")

        self.builder.add_from_file(self._ui)
        self.mainwindow = self.builder.get_object("frame1", self.root)

        self.root.title("Defisheye")
        self.root.iconphoto(False, tk.PhotoImage(file=self.icon))

        # Open Image Button
        self._openimageicon = pkg_resources.resource_filename(
            "defisheye", f"gui/open-image.png")
        self._openimagephoto = tk.PhotoImage(file=self._openimageicon)
        self._open_image_btn = self.builder.get_object("openimage")
        self._open_image_btn['image'] = self._openimagephoto
        self._open_image_btn.configure(command=self.open_image)

        # Edit Image Button
        self._editimageicon = pkg_resources.resource_filename(
            "defisheye", f"gui/edit-image.png")
        self._editimagephoto = tk.PhotoImage(file=self._editimageicon)
        self._edit_image_btn = self.builder.get_object("editimage")
        self._edit_image_btn['image'] = self._editimagephoto

        self._edit_image_btn.configure(command=self.process_image)

        # Image Icon
        self._imageicon = pkg_resources.resource_filename(
            "defisheye", f"gui/image200x200.png")
        self._imagephoto = tk.PhotoImage(file=self._imageicon)

        # Original Image
        self._original_image_label = self.builder.get_object("originalimage")
        self._original_image_label['image'] = self._imagephoto

        # Edited Image
        self._edited_image_label = self.builder.get_object("editedimage")
        self._edited_image_label['image'] = self._imagephoto

        # Parameters
        self._vars()
        self._fov_entry = self.builder.get_object("entryfov")
        self._fov_entry['textvariable'] = self._fov

        self._fov.set(180)

        self._pfov_entry = self.builder.get_object("entrypfov")
        self._pfov_entry['textvariable'] = self._pfov
        self._pfov.set(120)

        self._xcenter_entry = self.builder.get_object("entryxcenter")
        self._xcenter_entry['textvariable'] = self._xcenter
        self._xcenter.set(-1)

        self._ycenter_entry = self.builder.get_object("entryycenter")
        self._ycenter.set(-1)
        self._ycenter_entry['textvariable'] = self._ycenter

        self._radius_entry = self.builder.get_object("entryradius")
        self._radius.set(-1)
        self._radius_entry['textvariable'] = self._radius

        self._angle_entry = self.builder.get_object("entryangle")
        self._angle.set(-1)
        self._angle_entry['textvariable'] = self._angle

        self._dtype_combo = self.builder.get_object("combodtype")
        self._dtype_combo['values'] = (
            "linear", "equalarea", 'orthographic', "stereographic")
        self._dtype_combo.current(1)
        self._dtype.set(self._dtype_combo['values'][0])
        self._dtype_combo['textvariable'] = self._dtype

        self._format_combo = self.builder.get_object("comboformat")
        self._format_combo['values'] = ('fullframe', 'circular')
        self._format_combo.current(1)
        self._format.set(self._format_combo['values'][0])
        self._format_combo['textvariable'] = self._format

        self._xpand_entry = self.builder.get_object("xentry")
        self._xpand.set(0)
        self._xpand_entry['textvariable'] = self._xpand

    def _vars(self):
        self._fov = tk.IntVar()
        self._pfov = tk.IntVar()
        self._xcenter = tk.IntVar()
        self._ycenter = tk.IntVar()

        self._radius = tk.IntVar()
        self._angle = tk.IntVar()

        self._dtype = tk.StringVar()
        self._format = tk.StringVar()

        self._xpand = tk.IntVar()

        self._original_image = None
        self._original_imag_file = None

        self._processed_image = None

    def open_image(self):
        f_types = [('Jpg Files', '*.jpg'), ('PNG Files', '*.png')]
        self._original_imag_file = askopenfilename(
            multiple=False, filetypes=f_types)

        img = Image.open(self._original_imag_file)

        # width, height = img.size
        width_new = int(400)
        height_new = int(400)
        img_resized = img.resize((width_new, height_new))

        self._original_image = ImageTk.PhotoImage(img_resized)
        self._original_image_label['image'] = self._original_image

    def process_image(self):

        vkwargs = {"fov": self._fov.get(),
                   "pfov": self._pfov.get(),
                   "xcenter": self._xcenter.get() if self._xcenter.get() != -1 else None,
                   "ycenter": self._ycenter.get() if self._ycenter.get() != -1 else None,
                   "radius": self._radius.get() if self._radius.get() != -1 else None,
                   "pad": self._xpand.get() if self._xpand.get() > 0 else 0,
                   "angle": self._angle.get() if self._angle.get() != -1 else None,
                   "dtype": self._dtype.get(),
                   "format": self._format.get()
                   }

        if self._original_imag_file is not None:
            defisheye = Defisheye(self._original_imag_file, **vkwargs)
            img = defisheye.convert()
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            img = Image.fromarray(img)

            width_new = int(400)
            height_new = int(400)
            img_resized = img.resize((width_new, height_new))

            self._processed_image = ImageTk.PhotoImage(img_resized)

            self._edited_image_label['image'] = self._processed_image

    def run(self):
        self.mainwindow.mainloop()
