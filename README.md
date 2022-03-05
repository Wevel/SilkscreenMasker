# SilkscreenMasker
KiCad pcbnew plugin for adding masked regions to images for use on silkscreens. Drawings can be made on any layer (ideally use a user layer). These will be rescaled based on the bounds of all drawings on that layer, and then drawn as masks onto a given image. An output image will also be cropped to the correct aspect to cover these bounds. This can be then used in the KiCad image converter to create the footprint for the image with the masked regions excluded.

This was made using a KiCad 6.99 nightly build. It may work on 5.99 or 6.0, but hasn't been tested.

## How to Use:
- Add drawings to one of the user layers that defile the masked regions
- Open SilkscreenMasker window
- Select base image file to add mask to.
- Select layer that has the masking drawings on
- Enable negative mask if using the negative setting in the KiCad image converter
- Enable flip if the image is going on the bottom side of the PCB
- Set the over draw value to set the number of pixels to increase line widths by
- Save Image
- Open the KiCad image converter
- Load bitmap 
- Export to File

![Example of plugin being used](https://github.com/Wevel/SilkscreenMasker/blob/main/Pics/SilkscreenMaskerGUI.png?raw=true "Example of plugin being used")

## Why
Lets say you made some interesting pattern, in this case I made a cloud image in Photoshop:

<img src="https://github.com/Wevel/SilkscreenMasker/blob/main/Pics/SilkscreenNoMask.png?raw=true" width="400" height="400">

But this goes right over the silkscreen we already had, and also doesn't look very good near through holes and the PCB edge. We can design a mask in one of the user layers that defines the areas that we don't want covered, and use that to generate a new image that won't have silkscreen in these places:

<img src="https://github.com/Wevel/SilkscreenMasker/blob/main/Pics/Mask.png?raw=true" width="400" height="400">

Which gives us this (note that the image here is also flipped as it is for the bottom side of the PCB):

<img src="https://github.com/Wevel/SilkscreenMasker/blob/main/Pics/SilkscreenWithMask.png?raw=true" width="400" height="400">

## But this already exists
Possibly, but I couldn't find it, and I wanted to try writing a plugin for KiCad anyway.

If you have any issues, or want me to add any feature: contact me on my Twitter [@Wevel50000](https://twitter.com/Wevel50000).

Inspired by [KiBuzzard](https://github.com/gregdavill/KiBuzzard) by Greg Davill.
