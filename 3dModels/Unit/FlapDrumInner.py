import math

import cadquery as cq
from cadquery import exporters
from ocp_vscode import show_object

import constants as c
from helpers import helpers
import FlapDrumWheel


MOTOR_HOLDER_INNER_DIAMETER = 17


MOTOR_DIAMETER = 5
MOTOR_WIDTH = 3
MOTOR_DEPTH_1 = 1.5
MOTOR_DEPTH_2 = 7

BAR_LENGTH = c.DRUM_DIAMETER - 0.6

MAGNET_HOLDER_Y = 19.8
MAGNET_HOLDER_HEIGHT = 2.9
MAGNET_HOLDER_DIAMETER_OUTER = 3.8
MAGNET_HOLDER_DIAMETER_INNER = 2.1
MAGNET_DEPTH = 1

wheel = FlapDrumWheel.wheel


def bar_top(self, angle):
    result = (
        self.workplaneFromTagged("baseBars")
        .transformed(rotate=(0, 0, angle))
        .moveTo(BAR_LENGTH / 4 + BAR_LENGTH / 8, 0)
        .rect(BAR_LENGTH / 4, c.BAR_WIDTH)
        .workplane(offset=c.BAR_HEIGHT_OUTER)
        .moveTo(BAR_LENGTH / 2 - c.BAR_WIDTH / 2)
        .rect(c.BAR_WIDTH, c.BAR_WIDTH)
        .loft(combine=True)
    )
    return result


def screw_connection(self, angle):
    sPnts = [
        helpers.calc_position(
            c.DRUM_DIAMETER / 2 - c.SCREW_DISTANCE * 0.5, c.SCREW_ROTATION_ANGLE * 1.6
        ),
        helpers.calc_position(
            c.DRUM_DIAMETER / 2 - c.SCREW_DISTANCE * 1.25, c.SCREW_ROTATION_ANGLE * 1.6
        ),
        helpers.calc_position(
            c.DRUM_DIAMETER / 2 - c.SCREW_DISTANCE * 1.75, c.SCREW_ROTATION_ANGLE * 0.3
        ),
        (c.DRUM_DIAMETER / 2 - c.SCREW_DISTANCE * 2, c.BAR_WIDTH / -2),
    ]
    result = (
        self.workplaneFromTagged("baseTop")
        .transformed(rotate=(0, 0, angle))
        .moveTo(c.DRUM_DIAMETER / 2 - c.SCREW_DISTANCE * 2, 0)
        .lineTo(c.DRUM_DIAMETER / 2, 0)
        .lineTo(*helpers.calc_position(c.DRUM_DIAMETER / 2, c.SCREW_ROTATION_ANGLE * 2))
        .lineTo(
            *helpers.calc_position(
                c.DRUM_DIAMETER / 2 - c.DRUM_THICKNESS, c.SCREW_ROTATION_ANGLE * 2
            )
        )
        .spline(sPnts, includeCurrent=True)
        .close()
        .extrude(c.SCREW_BLOCK_HEIGHT_INNER)
        .faces("<Z")
        .workplane()
        .transformed(rotate=(0, 0, angle))
        .moveTo(
            *helpers.calc_position(
                c.DRUM_DIAMETER / 2 - c.SCREW_DISTANCE, -c.SCREW_ROTATION_ANGLE
            )
        )
        .cboreHole(c.SCREW_DIAMETER, c.SCREW_BORE_DIAMETER, c.SCREW_BORE_DEPTH)
    )
    return result


cq.Workplane.barTop = bar_top
cq.Workplane.screwConnection = screw_connection

flapDrumInner = wheel.add(
    wheel.moveTo(0, 0)
    .extrude(c.WHEEL_THICKNESS)
    .faces(">Z")
    .workplane()
    .tag("baseTop")
    # Drum
    .circle(c.DRUM_DIAMETER / 2 - c.DRUM_THICKNESS)
    .circle(c.DRUM_DIAMETER / 2)
    .extrude(c.DRUM_HEIGHT_INNER)
    # Bars
    .workplaneFromTagged("baseTop")
    .rect(BAR_LENGTH, c.BAR_WIDTH)
    .rect(c.BAR_WIDTH, BAR_LENGTH)
    .extrude(c.BAR_HEIGHT_CENTER)
    .faces(">Z")
    .workplane()
    .tag("baseBars")
    .barTop(0)
    .barTop(90)
    .barTop(180)
    .barTop(270)
    # Magnet Holder
    .workplaneFromTagged("baseBars")
    .moveTo(0, MAGNET_HOLDER_Y)
    .circle(c.BAR_WIDTH / 2)
    .workplane(offset=MAGNET_HOLDER_DIAMETER_OUTER / 2)
    .moveTo(0, MAGNET_HOLDER_Y)
    .circle(MAGNET_HOLDER_DIAMETER_OUTER / 2)
    .workplane(offset=MAGNET_HOLDER_HEIGHT)
    .tag("magnetHolderTop")
    .moveTo(0, MAGNET_HOLDER_Y)
    .circle(MAGNET_HOLDER_DIAMETER_OUTER / 2)
    .loft(ruled=True, combine=True)
    .workplaneFromTagged("magnetHolderTop")
    .moveTo(0, MAGNET_HOLDER_Y)
    .hole(MAGNET_HOLDER_DIAMETER_INNER, depth=MAGNET_DEPTH)
    # Center
    .workplaneFromTagged("baseTop")
    .circle(c.CENTER_DIAMETER_BOTTOM / 2)
    .workplane(offset=c.CENTER_HEIGHT)
    .circle(c.CENTER_DIAMETER_TOP / 2)
    .loft(ruled=True, combine=True)
    # Screw Connection
    .screwConnection(0)
    .screwConnection(180)
)

motor_bolt = (
    cq.Workplane("front", origin=(0, 0, c.WHEEL_THICKNESS + c.CENTER_HEIGHT))
    .circle(MOTOR_DIAMETER / 2)
    .extrude(-MOTOR_DEPTH_1)
    .faces("<Z")
    .rect(MOTOR_WIDTH, MOTOR_DIAMETER)
    .extrude(-MOTOR_DEPTH_2)
)
motor_bolt = motor_bolt & (
    cq.Workplane("front", origin=(0, 0, c.WHEEL_THICKNESS + c.CENTER_HEIGHT))
    .circle(MOTOR_DIAMETER / 2)
    .extrude(-MOTOR_DEPTH_1 - MOTOR_DEPTH_2)
)

flapDrumInner = flapDrumInner - motor_bolt


exporters.export(flapDrumInner, "FlapDrumInner.step")
exporters.export(flapDrumInner, "FlapDrumInner.stl")


show_object(flapDrumInner, name="wheel")

show_object(motor_bolt, name="Motor Bolt", options=dict(alpha=0.3, color="green"))


# original = cq.importers.importStep("C:\\Users\\micha\\Nextcloud2\\Basteln\\Split-Flap-Models\\Unit\\FlapDrumInner.stp")

# show_object(
#     original,
#     name="original",
#     options=dict(alpha=0.3, color='red')
#     )
