from ocp_vscode import show_object

import cadquery as cq
from cadquery import exporters
import math

import constants as c
import FlapDrumWheel
from helpers import helpers



MOTOR_HOLDER_INNER_DIAMETER = 17


MOTOR_DIAMETER = 5
MOTOR_WIDTH = 3
MOTOR_DEPTH_1 = 1.5
MOTOR_DEPTH_2 = 7

SCREW_DISTANCE = 5.2
SCREW_DIAMETER = 2.3
SCREW_HEIGHT = 6
SCREW_ROTATION_ANGLE = -11.6
SCREW_BORE_DIAMETER = 4.5
SCREW_BORE_DEPTH = 2

MAGNET_HOLDER_Y = 19.8
MAGNET_HOLDER_HEIGHT = 2.9
MAGNET_HOLDER_DIAMETER_OUTER = 3.8
MAGNET_HOLDER_DIAMETER_INNER = 2.1
MAGNET_DEPTH = 1
# set_port(3939)

wheel = FlapDrumWheel.wheel

def barTop(angle, screw: bool = False):
    sPnts = [
        helpers.calc_position(c.DRUM_DIAMETER/2 - SCREW_DISTANCE*0.5, SCREW_ROTATION_ANGLE*-1.8),
        helpers.calc_position(c.DRUM_DIAMETER/2 - SCREW_DISTANCE*1.25, SCREW_ROTATION_ANGLE*-1.8),
        helpers.calc_position(c.DRUM_DIAMETER/2 - SCREW_DISTANCE*1.3, SCREW_ROTATION_ANGLE*-0.4),
        (c.DRUM_DIAMETER/2 - SCREW_DISTANCE*0.8, 0.5)
        ]
    
    start_z = c.BAR_COUNTER_START_Z + c.WHEEL_THICKNESS
    
    result = (
        cq.Workplane("front")
        .tag(f"baseScrew{angle}")
        .transformed(offset=(0,0,start_z), rotate=(0,0,angle))
        .segmentArc(
            c.DRUM_DIAMETER/2 - c.DRUM_THICKNESS,
            c.DRUM_DIAMETER/2 + c.DRUM_THICKNESS,
            width=15,
            gap=c.BAR_COUNTER_GAP,
            height=c.BAR_COUNTER_HEIGHT
            )
    )
    
    if screw:
        result = (
            result
            .workplaneFromTagged(f"baseScrew{angle}")
            .transformed(
                offset=(0,0,c.BAR_COUNTER_START_Z + c.WHEEL_THICKNESS),
                rotate=(0,0,angle)
                )
            .moveTo(c.DRUM_DIAMETER/2 + c.DRUM_THICKNESS, c.BAR_COUNTER_GAP/2)
            .lineTo(*helpers.calc_position(
                c.DRUM_DIAMETER/2 + c.DRUM_THICKNESS,
                SCREW_ROTATION_ANGLE*-2
            ))
            .lineTo(*helpers.calc_position(
                c.DRUM_DIAMETER/2,
                SCREW_ROTATION_ANGLE*-2
            ))
            .spline(sPnts, includeCurrent=True)
            .close()
            .extrude(c.BAR_COUNTER_HEIGHT)
            .faces(">Z")
            .workplane()
            .transformed(rotate=(0,0,angle))
            .moveTo(*helpers.calc_position(c.DRUM_DIAMETER/2 - SCREW_DISTANCE, -SCREW_ROTATION_ANGLE))
            .hole(c.INSERT_DIAMETER/2, c.INSERT_DEPTH)
            )
    
    cut_cone = (
        cq.Workplane("front")
        .transformed(offset=(0,0,start_z))
        .circle(c.DRUM_DIAMETER/2)
        .workplane(offset=c.DRUM_DIAMETER/2)
        .circle(0.1)
        .loft()
        )
    
    cut_cylinder = (
        cq.Workplane("front")
        .circle(c.DRUM_DIAMETER/2 + c.DRUM_THICKNESS/2)
        .extrude(c.DRUM_HEIGHT_OUTER)
        )
    
    result = result - cut_cone
    result = result & cut_cylinder
    
    return result - cut_cone


flapDrumOuter = wheel.add(
    wheel
    .moveTo(0,0)
    .extrude(c.WHEEL_THICKNESS)
    .faces(">Z")
    .workplane()
    .tag("baseTop")
    
    # Drum
    .circle(c.DRUM_DIAMETER/2 + c.DRUM_THICKNESS)
    .extrude(c.DRUM_HEIGHT_OUTER)
    .faces(">Z")
    .hole(c.DRUM_DIAMETER)
    
    # Bars
    #.workplaneFromTagged("baseTop")
    #.rect(BAR_LENGTH, BAR_WIDTH)
    #.rect(BAR_WIDTH, BAR_LENGTH)
    #.extrude(BAR_HEIGHT_CENTER)
    #.faces(">Z")
    #.workplane()
    #.tag("baseBars")
    )


flapDrumOuter = flapDrumOuter + barTop(0, screw=True)
flapDrumOuter = flapDrumOuter + barTop(90)
flapDrumOuter = flapDrumOuter + barTop(180, screw=True)
flapDrumOuter = flapDrumOuter + barTop(270)



exporters.export(flapDrumOuter, 'flapDrumOuter.step')
exporters.export(flapDrumOuter, 'flapDrumOuter.stl')


show_object(flapDrumOuter, name="drum outer")



# original = cq.importers.importStep("C:\\Users\\micha\\Nextcloud2\\Basteln\\Split-Flap-Models\\Unit\\FlapDrumOuter.stp")

# show_object(
#     original,
#     name="original",
#     options=dict(alpha=0.3, color='red')
#     )