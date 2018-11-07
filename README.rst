print3d
=======

This project contains various utilities and documentation related to
3-D printing, particularly the Prusa i3 MK3.  Any software
instructions mentioned below are applicable to the Ubuntu 18.04
Linux-based operating system.

Program Installation
--------------------

FreeCAD
~~~~~~~

FreeCAD allows you to design 3-D parts.  It has a Python scripting
interface.

Download the `FreeCAD AppImage <https://www.freecadweb.org/wiki/Download>`__
for Linux.

You can run this directly::

    ./FreeCAD-13528.glibc2.17-x86_64.AppImage

or you can "install" it like this::

    mkdir -p ~/appimage
    cd ~/appimage
    ~/Downloads/FreeCAD-13528.glibc2.17-x86_64.AppImage --appimage-extract
    mv squashfs-root FreeCad-0.17.13528
    mkdir -p ~/bin
    cd ~/bin
    ln -s ~/appimage/FreeCad-0.17.13528/AppRun freecad
  
One advantage of "installing" FreeCAD is that this will allow you to
set up links to any extra Python libraries you want to use in your
FreeCAD Python scripts so that you don't need to manually specify
those Python module directories on the FreeCAD command line every time
you start the program.  See the section on setting up the `FreeCAD
Utility Libraries`_ for more information.

SVG import does not work properly in Ubuntu 18.04 due to the operating
system using an incompatible version of ``libexpat``.  This can be
resolved by downloading a compatible one from `packages.ubuntu.com
<https://packages.ubuntu.com/xenial-updates/amd64/libexpat1/download>`_
and placing it in the dynamic linker's run-time path.  If you do not
want to "install" FreeCAD as described above, you can run FreeCAD like
this::

    dpkg-deb -R libexpat1_2.1.0-7ubuntu0.16.04.3_amd64.deb libexpat1
    export LD_LIBRARY_PATH=~/Downloads/libexpat1/lib/x86_64-linux-gnu
    ./FreeCAD-13528.glibc2.17-x86_64.AppImage
    
otherwise, you can copy the required libraries into the *lib*
subdirectory of the FreeCAD installation::

    dpkg-deb -R libexpat1_2.1.0-7ubuntu0.16.04.3_amd64.deb libexpat1
    cp -a libexpat1/lib/x86_64-linux-gnu/libexpat.so.1* \
      ~/appimage/FreeCad-0.17.13528/lib/x86_64-linux-gnu/

Inkscape
~~~~~~~~

Inkscape is a 2-D vector drawing program that can be used to make flat
designs that can be extruded into 3-D shapes using FreeCAD.  The
default Ubuntu 18.04 version of Inkscape should work just fine::

    sudo apt-get install inkscape

Instructions on how to export a design from Inkscape into FreeCAD can
be found `here
<https://www.freecadweb.org/wiki/Import_text_and_geometry_from_Inkscape>`__.
Basically, the process is:

- Convert text to paths using the `Path->Object to path` menu.
- Ungroup your objects
- Select all objects and apply a stroke style with a width of 0 mm to
  all objects.  This makes dimensions the same between inkscape and FreeCAD.
- Save as `Plain SVG (*.svg)` file format
- Choose the `SVG as geometry (importSVG)` option when importing the file
  into FreeCAD.
- Choose the `Draft` workbench in the toolbar drop-down box
- Select one of the new path objects in the tree view
- Choose the `Draft->Upgrade` menu option to convert the path to a
  face.  (Sometimes another path is created instead of a face.  If
  this occurs, select the new path object and repeat the process to
  get a face.)
- Choose the `Part` workbench in the toolbar drop-down box.
- Select the new face object
- Choose the `Part->Extrude` menu option
- Choose `Custom direction Z: 1.00` and `Length->Along: 1.0 mm` in the dialog
  box
- Press the `Apply` button.
- The face should be converted to a solid
- More than one path can be selected to extrude multiple objects at one time.

Note that the SVG import option is broken in Ubuntu 18.04, so follow
the instructions in the `FreeCAD` section above to fix this.

PrusaControl
~~~~~~~~~~~~

PrusaControl is a very simple application that allows you "slice" 3-D
part designs so that they can be printed on a 3-D printer.

Download the `PrusaControl AppImage <https://prusacontrol.org/#download>`_
for Linux.

Slic3r
~~~~~~

Slic3r is a fully-featured application application that allows you
"slice" 3-D part designs so that they can be printed on a 3-D printer.
PrusaControl is built on top of Slic3r.

Download the `Slic3r <http://slic3r.org/>`_
`Prusa Edition <https://www.prusa3d.com/slic3r-prusa-edition>`_
`AppImage <https://github.com/prusa3d/Slic3r/releases>`__ for Linux.

FreeCAD Utility Libraries
-------------------------

In order to use some of the FreeCAD macros in this project, you will
need to add some utility libraries to your path.  The first step is
to check out the *print3d* project::

    git clone https://github.com/jwcraftsman/print3d.git

The *FCUtil* python package can be added to FreeCAD's ``PYTHONPATH``
like this::

    ./FreeCAD-13528.glibc2.17-x86_64.AppImage -P ~/git/print3d

If you don't want to have to add the ``-P ~/git/print3d`` option every
time you run FreeCAD, then you must first "install" FreeCAD as
described in the `FreeCAD`_ section of this document, and then make a
link to the *print3d* repo in the appropriate location::

    cd ~/appimage/FreeCad-0.17.13528/
    cd usr/lib/python2.7/dist-packages/
    ln -s ~/git/print3d/FCUtil

FreeCAD Macros
--------------

After installing the `FreeCAD Utility Libraries`_, make symbolic links
to the desired macros in your FreeCAD configuration directory::

    mkdir -p ~/.FreeCAD/Macro
    cd ~/.FreeCAD/Macro
    ln -s ~/git/print3d/FCMacros/*

The *print3d* macros should now be accessible under the
``Macro->Macros`` menu.

Files
-----

:FCUtil/block.py: FreeCAD functions for creating blocks.
		  
:FCMacro/block_test.FCMacro: FreeCAD Macro file that utilizes block.py.

:block.ini: Settings used for printing blocks on a Prusa i3 MK3 with
            Slic3rPE-1.40.1.linux64-full-201807051330.AppImage

Useful Links
------------

- `Prusa Manuals <https://manual.prusa3d.com/c/English_manuals>`_
