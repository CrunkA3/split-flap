import math

import cadquery as cq
from cadquery import exporters

WHEEL_DIAMETER = 69.3

NUM_FLAP_HOLES = 45
FLAP_HOLE_DIAMETER = 2
FLAP_HOLE_DISTANCE = 32.45

wheel = (
    cq.Workplane("front")
    .circle(WHEEL_DIAMETER / 2)
    )

for i in range(NUM_FLAP_HOLES):
    angle_deg = (i + 0.25) * (360 / NUM_FLAP_HOLES)
    angle_rad = math.radians(angle_deg)
    x = FLAP_HOLE_DISTANCE * math.cos(angle_rad)
    y = FLAP_HOLE_DISTANCE * math.sin(angle_rad)
    wheel = wheel.add(
        wheel
        .moveTo(x, y)
        .circle(FLAP_HOLE_DIAMETER/2)
        )

exporters.export(wheel, 'wheel.dxf')

