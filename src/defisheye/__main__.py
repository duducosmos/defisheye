#!/usr/bin/env python3.6
# -*- Coding: UTF-8 -*-
"""
Defisheye algorithm.

Developed by: E. S. Pereira.
e-mail: pereira.somoza@gmail.com

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
import os
import argparse
from .defisheye import Defisheye
from .defisheyeapp import DefisheyeApp

import argcomplete
from tqdm import tqdm


__author__ = "Eduardo S. Pereira"
__date__ = "02/2023"
__version__ = "1.1.0"


def get_images(input_dir, out_dir, types_images: list = ["png", "jpg", "jpeg"]):
    files = os.listdir(input_dir)
    images = [image for image in files if image.split(".")[-1] in types_images]
    input_images = [os.path.join(input_dir, image) for image in images]
    output_images = [os.path.join(out_dir, image) for image in images]
    return zip(input_images, output_images)


def process_image(input_image, output_image, **kwargs):
    obj = Defisheye(input_image, **kwargs)
    return obj.convert(outfile=output_image)


def batch_process(input_dir, output_dir, **kwargs):
    to_process = get_images(input_dir, output_dir)

    def individual(image_info):
        input_image = image_info[0]
        output_image = image_info[1]
        return process_image(input_image, output_image, **kwargs)

    for in_out_image in tqdm(list(to_process)):
        individual(in_out_image)


def mainapp():
    app = DefisheyeApp()
    app.run()
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Defisheye algorithm")

    parser.add_argument("--image", type=str, default=None,
                        help="Input image to process")

    parser.add_argument("--images_folder", type=str, default=None,
                        help="Input image folder for batch process")

    parser.add_argument("--save_dir", type=str, default=None,
                        help="output directory", required=False)

    parser.add_argument("--fov", type=int, default=180,
                        help="output directory", required=False)

    parser.add_argument("--pfov", type=int, default=120,
                        help="output directory", required=False)

    parser.add_argument("--xcenter", type=int, default=None,
                        help="output directory", required=False)

    parser.add_argument("--ycenter", type=int, default=None,
                        help="output directory", required=False)

    parser.add_argument("--radius", type=int, default=None,
                        help="output directory", required=False)

    parser.add_argument("--angle", type=int, default=0,
                        help="output directory", required=False)

    parser.add_argument("--dtype", type=str, default="equalarea",
                        help="output directory", required=False)

    parser.add_argument("--format", type=str, default="fullframe",
                        help="output directory", required=False)

    argcomplete.autocomplete(parser)

    cfg = parser.parse_args()

    vkwargs = {"fov": cfg.fov,
               "pfov": cfg.pfov,
               "xcenter": cfg.xcenter,
               "ycenter": cfg.ycenter,
               "radius": cfg.radius,
               "angle": cfg.angle,
               "dtype": cfg.dtype,
               "format": cfg.format
               }

    if cfg.image is not None:

        if cfg.save_dir is None:
            normpath = os.path.normpath(cfg.image)
            basedirs = os.path.split(normpath)[0]
            outdir = os.path.join(basedirs[0], "Defisheye")
        else:
            outdir = cfg.save_dir

        os.makedirs(outdir, exist_ok=True)

    elif cfg.images_folder is not None:
        if cfg.save_dir is None:
            normpath = os.path.normpath(cfg.images_folder)
            basedirs = os.path.split(normpath)
            outdir = os.path.join(basedirs[0], basedirs[1] + "-Defisheye")
        else:
            outdir = cfg.save_dir

        os.makedirs(outdir, exist_ok=True)

        batch_process(cfg.images_folder, outdir, **vkwargs)

    else:
        raise Exception(msg="Nor image neither images folder passed.")

    return 0
