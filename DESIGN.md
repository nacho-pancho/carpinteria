# Design

The central object of design is a _Piece_.
A piece may be a simple plank, a complex piece, or the part of a furniture

## Concepts


* Pieces fit in Voids. 
* Voids have a Volume
* Within a Volume, the space is arranged according to its Layout
* The layout specifies how pieces added to a Volume are arranged within the Volume
* For example, a GridLayout of 2 x 2 x 1 will have four pieces taking up all the depth of the volume, and sharing the width and height of the Volume.
* The EffectiveVolume of a Void can be modified from its BaseVolume in two ways: a Padding (extending its size beyond its BaseVolume) and Margin (leaving internal space unused, effectively reducing the available volume). 

## Layout rules

The layout of the pieces follows the concepts of UIs: pieces may have:
* absolute minimum size
* absolute maximum size
* a relative weight in all three directions

The rules then are as follows:
* a piece may not be smaller than the aboslute minimum, if defined
* it cannot be larger than the absolute maximum, if defined
* for those dimensions which are free, the objects will fill as much as they can as given by their _weight_.
* If the weight in one dimension is 100%, it takes up everytuing.
* If it is 0%, it takes nothing buts its aboslute minimum (one must be defined)
* If it is any number in between, say w_i for the i-th parth they will take a proportion a = w_i/(sum_j w_j)
* padding is always added, regardless of any layout
* margin is always respected; it always reduces the available volume; if it becomes negative, a waring is produced

## Coordinates

* Right handed system
* X increases to the right
* Y increases to the back
* Z increases up

## Display

We use PyVista for the display.
Some notes:
* box faces appear in this order: left, right, back, front, bottom, up