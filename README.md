# SilkscreenMasker
KiCad pcbnew plugin for adding masked regions to images for use on silkscreens. Drawings can be made on any layer (ideally use a user layer). These will be rescaled based on the bounds of all drawings on that layer, and then drawn as masks onto a given image. An output image will also be cropped to the correct aspect to cover these bounds. This can be then used in the KiCad image converter to create the footprint for the image with the masked regions excluded.

This was made using a KiCad 6.99 nightly build. It may work on 5.99 or 6.0, but hasn't been tested.

# How to Use:
- Add drawings to one of the user layers that defile the masked regions
- Open SilkscreenMasker window
- Select base image file to add mask to.
- Select layer that has the masking drawings on
- Enable negative mask if using the negative setting in the KiCad image converter
- Enable flip if the image is going on the bottom side of the PCB
- Save Image
- Open the KiCad image converter
- Load bitmap 
- Currently the output size still needs to be changed
- Export to File

Inspired by [KiBuzzard](https://github.com/gregdavill/KiBuzzard) by Greg Davill
