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
  
The advantage of "installing" FreeCAD is that this will allow you to
set up links to any extra Python libraries you want to use in your
FreeCAD Python scripts so that you don't need to manually specify
those Python module directories on the FreeCAD command line every time
you start the program.  See the section on setting up the `FreeCAD
Utility Libraries`_ for more information.

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
		  
:FCMacro/test_block.FCMacro: FreeCAD Macro file that utilizes block.py.

:block.ini: Settings used for printing blocks on a Prusa i3 MK3 with
            Slic3rPE-1.40.1.linux64-full-201807051330.AppImage

Useful Links
------------

- `Prusa Manuals <https://manual.prusa3d.com/c/English_manuals>`_
