from Part import *
import math
from math import sqrt
from FreeCAD import Base

# Block dimension information:
# https://www.cailliau.org/en/Alphabetical/L/Lego/Dimensions/General%20Considerations/
# https://bricks.stackexchange.com/questions/288/what-are-the-dimensions-of-a-lego-brick

mm = 1.0 # base unit is mm
epsilon = 0.01*mm # small overlap for CAD purposes
infinity = 1000*mm # very large number for CAD clipping purposes

def block(number_of_x_knobs,
          number_of_y_knobs,
          number_of_vertical_units,
          **kw):
  solid                     = kw.get('solid', False)
  has_knobs                 = kw.get('has_knobs', True)
  has_knob_dimples          = kw.get('has_knob_dimples', False)
  has_under_tubes           = kw.get('has_under_tubes', True)
  has_under_tube_cavities   = kw.get('has_under_tube_cavities', True)
  has_ridges                = kw.get('has_ridges', False)
  has_struts                = kw.get('has_struts', False)
  has_vertical_holes        = kw.get('has_vertical_holes', False)
  has_horizontal_holes      = kw.get('has_horizontal_holes', False)
  units = unit              = kw.get('unit',                        1.6 * mm   )
  horizontal_pitch          = kw.get('horizontal_pitch',            5.0 * units)
  vertical_pitch            = kw.get('vertical_pitch',              6.0 * units)
  horizontal_play           = kw.get('horizontal_play',             0.1 * mm   )
  bottom_play               = kw.get('bottom_play',                 0.0 * mm   )
  notional_wall_thickness   = kw.get('notional_wall_thickness',     1.0 * unit )
  if has_ridges:
    wall_thickness          = kw.get('wall_thickness',              1.2 * mm   )
  else:
    wall_thickness          = kw.get('wall_thickness',              1.5 * mm   )
  ridge_length              = kw.get('ridge_length',                0.6 * mm   )
  top_thickness             = kw.get('top_thickness',               1.1 * mm   )
  knob_height               = kw.get('knob_height',   1.0 * unit  + 0.2 * mm   )
  knob_diameter             = kw.get('knob_diameter', 3.0 * units + 0.1 * mm   )
  knob_dimple_height        = kw.get('knob_dimple_height',
                                                      knob_height - 0.3 * mm   )
  knob_dimple_diameter      = kw.get('knob_dimple_diameter',
                                                      1.5 * units + 0.2 * mm   )
  under_tube_outer_diameter = kw.get('under_tube_outer_diameter',
                                              (5*sqrt(2)-3)*units - 0.1 * mm   )
  under_tube_inner_diameter = kw.get('under_tube_inner_diameter',
                                                      3.0 * units + 0.1 * mm   )
  strut_gap                 = kw.get('strut_gap',                   2.3 * mm   )
  strut_width               = kw.get('strut_width',                 1.0 * mm   )
  strut_interval            = kw.get('strut_interval',              2          )
  strut_sides               = kw.get('strut_sides',                 2          )
  horizontal_hole_interval  = kw.get('horizontal_hole_interval',    1          )
  horizontal_hole_offset    = kw.get('horizontal_hole_offset', horizontal_pitch)
  horizontal_hole_diameter = kw.get('horizontal_hole_diameter',
                                                        3.0 * units + 0.1 * mm ) # knob diameter
  horizontal_hole_counterbore_diameter = kw.get('horizontal_hole_counterbore_diameter',
                                                       3.75 * units + 0.2 * mm )
  notional_horizontal_hole_counterbore_depth = kw.get('notional_horizontal_hole_counterbore_depth',
                                                                       0.9 * mm)
  horizontal_tube_wall_thickness = kw.get('horizontal_tube_wall_thickness',
                                                           wall_thickness - 0.2)
  horizontal_tube_outer_diameter = kw.get('horizontal_tube_outer_diameter',
                    horizontal_hole_diameter + 2*horizontal_tube_wall_thickness)
  horizontal_hole_vertical_offset = kw.get('horizontal_hole_vertical_offset',
                                                        3.5 * units + 0.2 * mm )
  
  notional_width = number_of_x_knobs * horizontal_pitch
  notional_depth = number_of_y_knobs * horizontal_pitch
  notional_height = number_of_vertical_units * vertical_pitch

  actual_width  = notional_width - 2.0*horizontal_play
  actual_depth  = notional_depth - 2.0*horizontal_play
  actual_height = notional_height

  if has_ridges:
    ridge_width = notional_wall_thickness - horizontal_play - wall_thickness

  number_of_x_under_tubes = number_of_x_knobs - 1
  number_of_y_under_tubes = number_of_y_knobs - 1

  number_of_struts = int(math.floor((number_of_y_knobs - 1)/strut_interval))

  number_of_horizontal_holes = int(math.floor((number_of_y_knobs)/horizontal_hole_interval))
  print('a',number_of_horizontal_holes,horizontal_hole_offset,number_of_y_knobs)
  if horizontal_hole_offset > (horizontal_pitch + 0.1):
    number_of_horizontal_holes -= 1
  
# Box of basic dimensions
  b = makeBox(notional_width, notional_depth, notional_height)

  # Cut away inner box leaving the edges and top
  if not solid:
    cavity_offset = wall_thickness + horizontal_play
    cavity = makeBox(
      notional_width - 2*cavity_offset,
      notional_depth - 2*cavity_offset,
      notional_height - top_thickness + epsilon)
    cavity.translate((
      cavity_offset,
      cavity_offset,
      -epsilon))
    b = b.cut(cavity)

  # Add side ridges aligned with each knob
  if has_ridges:

    # Top and bottom ridges
    y_bottom = horizontal_play + wall_thickness - epsilon
    y_top = notional_depth - horizontal_play - wall_thickness - ridge_width
    for xi in range(number_of_x_knobs):
      x = (xi + 0.5)*horizontal_pitch - (ridge_length/2.0)
      bottom_ridge = makeBox(ridge_length, ridge_width + epsilon,
                             notional_height - top_thickness + epsilon)
      bottom_ridge.translate((x,y_bottom,0))
      b = b.fuse(bottom_ridge)
      top_ridge = makeBox(ridge_length, ridge_width + epsilon,
                          notional_height - top_thickness + epsilon)
      top_ridge.translate((x,y_top,0))
      b = b.fuse(top_ridge)

    # Left and right ridges
    x_left = horizontal_play + wall_thickness - epsilon
    x_right = notional_width - horizontal_play - wall_thickness - ridge_width
    for yi in range(number_of_y_knobs):
      y = (yi + 0.5)*horizontal_pitch - (ridge_length/2.0)
      left_ridge = makeBox(ridge_width + epsilon, ridge_length,
                           notional_height - top_thickness + epsilon)
      left_ridge.translate((x_left,y,0))
      b = b.fuse(left_ridge)
      right_ridge = makeBox(ridge_width + epsilon, ridge_length,
                            notional_height - top_thickness + epsilon)
      right_ridge.translate((x_right,y,0))
      b = b.fuse(right_ridge)

  # Add struts aligned with under-tube knob
  if has_struts:
    for yi in range(number_of_struts):
      y = (yi + 1) * strut_interval * horizontal_pitch
      if strut_sides == 1:
      	strut_length = notional_width/2.0-2.0*epsilon
      else:
        strut_length = notional_width-2.0*epsilon
      strut = makeBox(strut_length, strut_width, notional_height - strut_gap - epsilon)
      strut.translate((epsilon, y-strut_width/2.0, strut_gap))
      b = b.fuse(strut)
      
  # Make knobs
  if has_knobs:
    for xi in range(number_of_x_knobs):
      x = (xi + 0.5)*horizontal_pitch
      for yi in range(number_of_y_knobs):
        y = (yi + 0.5)*horizontal_pitch
        knob = makeCylinder(knob_diameter/2.0,knob_height + epsilon)
        knob.translate((x, y, notional_height - epsilon))
        b = b.fuse(knob)
        if has_knob_dimples:
            knob_dimple = makeCylinder(
                knob_dimple_diameter/2.0, knob_dimple_height + epsilon)
            knob_dimple.translate((x, y,
                                   notional_height - top_thickness - epsilon))
            b = b.cut(knob_dimple)

  # Make under tubes
  if has_under_tubes:
    for xi in range(number_of_x_under_tubes):
      x = (xi + 1.0)*horizontal_pitch
      for yi in range(number_of_y_under_tubes):
        y = (yi + 1.0)*horizontal_pitch
        tube = makeCylinder(under_tube_outer_diameter/2.0,
                            notional_height - top_thickness + epsilon)
        tube.translate((x, y, 0))
        if has_vertical_holes:
          tube_cavity_height = infinity
        else:
          tube_cavity_height = notional_height - top_thickness
        tube_cavity = makeCylinder(under_tube_inner_diameter/2.0,
                                   tube_cavity_height + epsilon)
        tube_cavity.translate((x, y, -epsilon))
        b = b.fuse(tube)
        if has_under_tube_cavities:
          b = b.cut(tube_cavity)

  # Make horizontal tubes
  if has_horizontal_holes:
    x = epsilon
    for i, yi in enumerate(range(number_of_horizontal_holes)):
      y = horizontal_hole_offset + yi * horizontal_hole_interval * horizontal_pitch

      # Make a solid tube
      tube = makeCylinder(horizontal_tube_outer_diameter/2.0,
			  actual_width - 2*epsilon)
     
      # Rotate the tube 90 degress about y-axis 
      tube.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), 90)

      # Move the tube to the right place
      tube.translate((x, y, horizontal_hole_vertical_offset))

      # Add the tube to the block
      b = b.fuse(tube)

      # Create the tube cavity
      tube_cavity = makeCylinder(horizontal_hole_diameter/2.0,
			         actual_width + 2*infinity)
      tube_cavity.translate((0, 0, -infinity))

      # Rotate the tube cavity 90 degress about y-axis 
      tube_cavity.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), 90)

      # Move the tube cavity to the right place
      tube_cavity.translate((x, y, horizontal_hole_vertical_offset))

      # Cut the tube cavity out of the block
      b = b.cut(tube_cavity)

      # Create the closest counterbore cavity
      counterbore_cavity = makeCylinder(horizontal_hole_counterbore_diameter/2.0,
			                notional_horizontal_hole_counterbore_depth + infinity)
      counterbore_cavity.translate((0, 0, -infinity))
      counterbore_cavity.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), 90)
      counterbore_cavity.translate((x, y, horizontal_hole_vertical_offset))
      b = b.cut(counterbore_cavity)
      
      # Create the opposite counterbore cavity
      counterbore_cavity = makeCylinder(horizontal_hole_counterbore_diameter/2.0,
			                notional_horizontal_hole_counterbore_depth)
      counterbore_cavity.translate((0, 0, -notional_horizontal_hole_counterbore_depth))
      counterbore_cavity.rotate(Base.Vector(0,0,0), Base.Vector(0,1,0), 90)
      counterbore_cavity.translate((x + horizontal_pitch, y, horizontal_hole_vertical_offset))
      b = b.cut(counterbore_cavity)

      # Keystone cutout for printing
      if 1: #i == 0:
        w = 2.0 * mm
        h = 2.0 * mm
        keystone = makeBox(actual_width, w, h)
        keystone.translate((x, y - w/2.0, horizontal_hole_vertical_offset + horizontal_hole_counterbore_diameter/2.0 - h +0.1 ))
        b = b.cut(keystone)
        
  # Clip everything outside off the play boundary
  play_boundary = makeBox(
    actual_width,
    actual_depth,
    infinity-bottom_play)
  play_boundary.translate((
    horizontal_play,
    horizontal_play,
    bottom_play))
  b = b.common(play_boundary)

  return b

def myblock(number_of_x_knobs,
	    number_of_y_knobs,
	    number_of_vertical_units,
            **kw):
  units = unit                    = kw.get('unit',                         1.6 * mm   )
  kw['knob_diameter']             = kw.get('knob_diameter', 3.0 * units + 0.15 * mm   )
  kw['bottom_play']               = kw.get('bottom_play',                  0.1 * mm   )
  kw['under_tube_outer_diameter'] = kw.get('under_tube_outer_diameter',
                                                     (5*sqrt(2)-3)*units + 0.1 * mm   )
  return block(number_of_x_knobs,
	       number_of_y_knobs,
	       number_of_vertical_units,
               **kw)

def vsplit(b, v):
  boundary = makeBox(infinity*2, infinity*2, infinity)
  boundary.translate((-infinity,-infinity,v))
  top_b = b.common(boundary)
  bottom_b = b.cut(boundary)
  return top_b, bottom_b
  
def box_corner():
  hunit = 5*1.6
  vunit = 6*1.6

  # middle layer
  b  = myblock(1,2,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,has_knobs=False)
  
  b2 = myblock(1,1,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,has_knobs=False)
  b2.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
  b2.translate((hunit,hunit,0))
  b = b.fuse(b2)
  
  b3 = myblock(1,1,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,has_knobs=False)
  b3.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
  b3.translate((hunit,hunit*2,0))
  b = b.fuse(b3)

  # top layer
  b4  = myblock(1,2,1,has_under_tubes=False,has_horizontal_holes=False,bottom_play=0.0,horizontal_play=0.0,has_knobs=False,solid=True)
  b4.translate((0,0,vunit))
  b = b.fuse(b4)

  b5 = myblock(1,1,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True)
  b5.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
  b5.translate((hunit,hunit,vunit))
  b = b.fuse(b5)

  b6 = myblock(1,1,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True)
  b6.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
  b6.translate((hunit,hunit*2,vunit))
  b = b.fuse(b6)

  # Slot #1 in the top layer
  slot = makeBox(2.5,vunit*.7,vunit*.7)
  slot.translate((1.5,0,vunit*(2-.7)))
  b = b.cut(slot)
  
  # Slot #2 in the top layer
  slot = makeBox(2.5,vunit*.7,vunit*.7)
  slot.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
  slot.translate((0,2*hunit-1.5,vunit*(2-.7)))
  #slot.translate((0,hunit*2-2.5-1.5,vunit*(2-.7)))
  b = b.cut(slot)
  
  # bottom layer
  b7  = myblock(2,2,1,has_under_tubes=True,has_horizontal_holes=False,bottom_play=0.0,horizontal_play=0.0,solid=False,has_knobs=False,
                top_thickness=1.1+2.5)
  b7.translate((0,0,-vunit))

  # Slot in the bottom layer
  slot = makeBox(vunit*.7,hunit*2.0,2.5)
  slot.translate((0,0,-2.5))
  b7 = b7.cut(slot)
  b = b.fuse(b7)

  # Clip everything outside off the play boundary
  play_boundary = makeBox(
    hunit*2-2*0.1,
    hunit*2-2*0.1,
    vunit*3-0.1 + vunit) # extra vunit for knobs
  play_boundary.translate((
    0.1,
    0.1,
    0.1-vunit))
  b = b.common(play_boundary)
  
  return b

def box_side(length):
  hunit = 5*1.6
  vunit = 6*1.6

  # middle layer
  b  = myblock(1,1,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,has_knobs=False,
               horizontal_hole_offset=0.5*hunit)
  b.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
  b.translate((0,hunit,0))

  ba = myblock(1,1,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,has_knobs=False,
               horizontal_hole_offset=0.5*hunit)
  ba.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
  ba.translate((0,hunit*length,0))
  b = b.fuse(ba)

  b2 = myblock(1,1,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,has_knobs=False,
               horizontal_hole_offset=0.5*hunit)
  b2.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
  b2.translate((hunit,hunit,0))
  b = b.fuse(b2)
  
  b2a = myblock(1,1,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,has_knobs=False,
               horizontal_hole_offset=0.5*hunit)
  b2a.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
  b2a.translate((hunit,hunit*length,0))
  b = b.fuse(b2a)
  
  b3 = myblock(1,length-2,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,has_knobs=False,
    horizontal_hole_interval=2, horizontal_hole_offset=2.0*hunit)
  b3.translate((0,hunit,0))
  b = b.fuse(b3)

  b3a = myblock(1,length-2,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,has_knobs=False,
    horizontal_hole_interval=2)
  b3a.translate((hunit,hunit,0))
  b = b.fuse(b3a)

  # top layer
  b4  = myblock(1,length,1,has_under_tubes=False,has_horizontal_holes=False,bottom_play=0.0,horizontal_play=0.0,has_knobs=False,solid=True)
  b4.translate((0,0,vunit))
  b = b.fuse(b4)

  b5 = myblock(1,1,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,
               horizontal_hole_offset=0.5*hunit)
  b5.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
  b5.translate((hunit,hunit,vunit))
  b = b.fuse(b5)

  b5a = myblock(1,1,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,
               horizontal_hole_offset=0.5*hunit)
  b5a.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
  b5a.translate((hunit,hunit*length,vunit))
  b = b.fuse(b5a)

  b6 = myblock(1,length-2,1,has_under_tubes=False,has_horizontal_holes=False,bottom_play=0.0,horizontal_play=0.0,solid=True)
  b6.translate((hunit,hunit,vunit))
  b = b.fuse(b6)

  # Slot #1 in the top layer
  slot = makeBox(2.5,length*hunit,vunit*.7)
  slot.translate((1.5,0,vunit*(2-.7)))
  b = b.cut(slot)
  
  # bottom layer
  b7  = myblock(2,length,1,has_under_tubes=True,has_horizontal_holes=False,bottom_play=0.0,horizontal_play=0.0,solid=False,has_knobs=False,
                top_thickness=1.1+2.5,has_struts=0,strut_sides=1)
  b7.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 180)
  b7.translate((2*hunit,length*hunit,-vunit))

  # Slot in the bottom layer
  slot = makeBox(vunit*.7,hunit*length,2.5)
  slot.translate((0,0,-2.5))
  b7 = b7.cut(slot)
  b = b.fuse(b7)

  # Clip everything outside off the play boundary
  play_boundary = makeBox(
    hunit*2-2*0.1,
    hunit*length-2*0.1,
    vunit*3-0.1 + vunit) # extra vunit for knobs
  play_boundary.translate((
    0.1,
    0.1,
    0.1-vunit))
  b = b.common(play_boundary)
  
  return b
  
def box_side_bottom(length):
  hunit = 5*1.6
  vunit = 6*1.6
  slot_width = 2.5 # mm
  slot_depth = 0.7*vunit
  
  # middle layer end inside
  b  = myblock(1,1,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,has_knobs=False,
               horizontal_hole_offset=0.5*hunit)
  b.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
  b.translate((0,hunit,0))

  ba = myblock(1,1,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,has_knobs=False,
               horizontal_hole_offset=0.5*hunit)
  ba.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
  ba.translate((0,hunit*length,0))
  b = b.fuse(ba)

  # middle layer end outside
  b2 = myblock(1,1,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,has_knobs=False,
               horizontal_hole_offset=0.5*hunit)
  b2.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
  b2.translate((hunit,hunit,0))
  b = b.fuse(b2)
  
  b2a = myblock(1,1,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,has_knobs=False,
               horizontal_hole_offset=0.5*hunit)
  b2a.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
  b2a.translate((hunit,hunit*length,0))
  b = b.fuse(b2a)
  
  # middle layer outside
  b3 = myblock(1,2,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,has_knobs=False,
    horizontal_hole_interval=2)
  b3.translate((hunit,hunit,0))
  b = b.fuse(b3)

  b3a = myblock(1,2,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,has_knobs=False,
    horizontal_hole_interval=2)
  b3a.translate((hunit,hunit*(length-3),0))
  b = b.fuse(b3a)

  # top layer end outside
  b5 = myblock(1,1,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,has_knobs=False,
               horizontal_hole_offset=0.5*hunit)
  b5.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
  b5.translate((hunit,hunit,vunit))
  b = b.fuse(b5)

  b5a = myblock(1,1,1,has_under_tubes=False,has_horizontal_holes=True,bottom_play=0.0,horizontal_play=0.0,solid=True,has_knobs=False,
               horizontal_hole_offset=0.5*hunit)
  b5a.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), -90)
  b5a.translate((hunit,hunit*length,vunit))
  b = b.fuse(b5a)

  # Slot #1 in the top layer
  #slot = makeBox(slot_width,length*hunit,slot_depth)
  #slot.translate((1.5,0,vunit*2-slot_depth))
  #b = b.cut(slot)
  
  # bottom layer
  b7  = myblock(2,length,1,has_under_tubes=False,has_horizontal_holes=False,bottom_play=0.0,horizontal_play=0.0,solid=False,has_knobs=False,
                top_thickness=1.1+slot_width,has_struts=0,strut_sides=1)
  b7.rotate(Base.Vector(0,0,0), Base.Vector(0,0,1), 180)
  b7.translate((2*hunit,length*hunit,-vunit))

  # Slot in the bottom layer
  slot = makeBox(slot_depth,hunit*length,slot_width)
  slot.translate((0,0,-slot_width))
  b7 = b7.cut(slot)
  b = b.fuse(b7)

  # Top of slot
  b8 = makeBox(hunit,hunit*length,1.0)
  b = b.fuse(b8)
  
  # Right wall of slot
  b9 = makeBox(1.0,hunit*(length-2),slot_depth+1.0)
  b9.translate((hunit-1.0,hunit,0))
  b = b.fuse(b9)
  b9a1 = makeBox(1.0,hunit+slot_depth+1,vunit)
  b9a1.translate((hunit-1.0,0,slot_depth))
  b = b.fuse(b9a1)
  b9a2 = makeBox(1.0,hunit+slot_depth+1,vunit)
  b9a2.translate((hunit-1.0,hunit*(length-1)-slot_depth-1,slot_depth))
  b = b.fuse(b9a2)
  b9b1 = makeBox(1.0,2*hunit,vunit)
  b9b1.translate((hunit-1.0,hunit,0))
  b = b.fuse(b9b1)
  b9b2 = makeBox(1.0,2*hunit,vunit)
  b9b2.translate((hunit-1.0,hunit*(length-3),0))
  b = b.fuse(b9b2)
  
  # Left wall of slot
  b10 = makeBox(1.0,hunit*(length-2),slot_depth+1.0)
  b10.translate((hunit-1.0-1.0-slot_width,hunit,0))
  b = b.fuse(b10)
  b10a1 = makeBox(1.0,slot_depth+1,vunit)
  b10a1.translate((hunit-1.0-1.0-slot_width,hunit,slot_depth))
  b = b.fuse(b10a1)
  b10a2 = makeBox(1.0,slot_depth+1,vunit)
  b10a2.translate((hunit-1.0-1.0-slot_width,hunit*(length-1)-slot_depth-1,slot_depth))
  b = b.fuse(b10a2)
  b10b1 = makeBox(1.0,hunit+slot_depth+1,slot_depth)
  b10b1.translate((hunit-1.0-1.0-slot_width,0,vunit))
  b = b.fuse(b10b1)
  b10b2 = makeBox(1.0,hunit+slot_depth+1,slot_depth)
  b10b2.translate((hunit-1.0-1.0-slot_width,hunit*(length-1)-slot_depth-1,vunit))
  b = b.fuse(b10b2)

  # Block holes
  b11 = makeBox(hunit,1.0,vunit)
  b11.translate((0,hunit,0))
  b = b.fuse(b11)
  b11a = makeBox(hunit,1.0,vunit)
  b11a.translate((0,hunit*(length-1)-1.0,0))
  b = b.fuse(b11a)

  
  # Clip everything outside off the play boundary
  play_boundary = makeBox(
    hunit*2-2*0.1,
    hunit*length-2*0.1,
    vunit*3-0.1 + vunit) # extra vunit for knobs
  play_boundary.translate((
    0.1,
    0.1,
    0.1-vunit))
  b = b.common(play_boundary)
  
  return b
  
