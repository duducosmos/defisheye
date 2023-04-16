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


class DefisheyeApp:
    def __init__(self, **kwargs) -> None:
        self.root = tk.Tk()

        self.builder = pygubu.Builder()
        self._ui = pkg_resources.resource_filename(
            "defisheye", f"gui/main.ui")

        self.builder.add_from_file(self._ui)
        self.mainwindow = self.builder.get_object("frame1", self.root)

        # Open Image Button
        self._openimageicon = pkg_resources.resource_filename(
            "defisheye", f"gui/open-image.png")
        self._openimagephoto = tk.PhotoImage(file=self._openimageicon)
        self._open_image_btn = self.builder.get_object("openimage")
        self._open_image_btn['image'] = self._openimagephoto

        # Edit Image Button
        self._editimageicon = pkg_resources.resource_filename(
            "defisheye", f"gui/edit-image.png")
        self._editimagephoto = tk.PhotoImage(file=self._editimageicon)
        self._edit_image_btn = self.builder.get_object("editimage")
        self._edit_image_btn['image'] = self._editimagephoto

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
        self._fov = self.builder.get_object("entryfov")
        self._fov.insert(0, "180")

        self._pfov = self.builder.get_object("entrypfov")
        self._pfov.insert(0, "120")

        self._xcenter = self.builder.get_object("entryxcenter")

        self._ycenter = self.builder.get_object("entryycenter")

        self._radius = self.builder.get_object("entryradius")

        self._angle = self.builder.get_object("entryangle")

        self._dtype = self.builder.get_object("combodtype")
        self._dtype['values'] = (
            "linear", "equalarea", 'orthographic', "stereographic")
        self._dtype.current(0)

        self._format = self.builder.get_object("comboformat")
        self._format['values'] = ('fullframe', 'circular')
        self._format.current(0)

    def run(self):
        self.mainwindow.mainloop()
