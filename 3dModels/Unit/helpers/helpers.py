"""
Helper functions for FlapDrum
"""

import math

import cadquery as cq


def calc_position(distance, angle) -> tuple[float, float]:
    """Calculates the position from distance and angle to x,y"""
    angle_rad = math.radians(angle)
    x = distance * math.cos(angle_rad)
    y = distance * math.sin(angle_rad)
    return (x, y)


def arc(self, *, r1: float, r2: float, start_deg: float, sweep_deg: float):
    """Create an arc"""

    pt_outer_1 = calc_position(r2, start_deg)
    pt_inner_1 = calc_position(r1, start_deg)

    pt_outer_2 = calc_position(r2, start_deg + sweep_deg / 2)
    pt_inner_2 = calc_position(r1, start_deg + sweep_deg / 2)

    pt_outer_3 = calc_position(r2, start_deg + sweep_deg)
    pt_inner_3 = calc_position(r1, start_deg + sweep_deg)

    result = (
        self.moveTo(*pt_outer_1)
        .threePointArc(point1=pt_outer_2, point2=pt_outer_3)
        .lineTo(*pt_inner_3)
        .threePointArc(point1=pt_inner_2, point2=pt_inner_1)
        .close()
    )
    return result


def segment_arc(self, r1: float, r2: float, width: float, gap: float, height: float):
    """Creates a segmented arc"""

    radial_width = r2 - r1
    r_mid = (r1 + r2) / 2.0
    r1_bottom = r_mid - 0.1
    r2_bottom = r_mid + 0.1

    # Berechne den Winkel (in Grad) des Bogens,
    # so dass der Bogen an r_mid eine Länge von gap_tangential hat
    arc_angle_rad = (width - gap) / r_mid  # Winkel in Radiant
    arc_angle_deg = arc_angle_rad * 180.0 / math.pi
    arc_angle_deg = arc_angle_deg / 4

    # Berechne den Winkel (in Grad) der Tangential-Lücke,
    # so dass der Bogen an r_mid eine Länge von gap_tangential hat
    gap_angle_rad = gap / r_mid  # Winkel in Radiant
    gap_angle_deg = gap_angle_rad * 180.0 / math.pi

    # Positionierung: zwei Bögen, links und rechts, mit tangentialem Spalt zwischen ihnen
    # Wir zentrieren das Paar symmetrisch um X-Achse:
    # rechter Bogen beginnt bei angle = + (gap/2) und läuft im positiven Winkel um arc_angle_deg
    # linker Bogen beginnt bei angle = - (gap/2) - arc_angle_deg und läuft bis - (gap/2)
    half_gap = gap_angle_deg / 2.0

    # rechter Bogen: Start bei +half_gap
    right_start = half_gap

    # linker Bogen: endet bei -half_gap, beginnt um arc_angle_deg früher
    left_start = -half_gap - arc_angle_deg

    # arc1 = (
    #     self.arc(
    #         r1=r1_bottom, r2=r2_bottom, start_deg=right_start, sweep_deg=arc_angle_deg
    #     )
    #     .workplane(offset=radial_width)
    #     .arc(r1=r1, r2=r2, start_deg=right_start, sweep_deg=arc_angle_deg)
    #     .workplane(offset=height - radial_width)
    #     .arc(r1=r1, r2=r2, start_deg=right_start, sweep_deg=arc_angle_deg)
    #     .loft(combine=True, ruled=True)
    # )

    # arc2 = (
    #     self.arc(
    #         r1=r1_bottom, r2=r2_bottom, start_deg=left_start, sweep_deg=arc_angle_deg
    #     )
    #     .workplane(offset=radial_width)
    #     .arc(r1=r1, r2=r2, start_deg=left_start, sweep_deg=arc_angle_deg)
    #     .workplane(offset=height - radial_width)
    #     .arc(r1=r1, r2=r2, start_deg=left_start, sweep_deg=arc_angle_deg)
    #     .loft(combine=True, ruled=True)
    # )
    # return arc1 + arc2

    arc1 = self.arc(
        r1=r1, r2=r2, start_deg=right_start, sweep_deg=arc_angle_deg
    ).extrude(height)
    arc2 = self.arc(
        r1=r1, r2=r2, start_deg=left_start, sweep_deg=arc_angle_deg
    ).extrude(height)
    return arc1 + arc2


# link the plugin into CadQuery
cq.Workplane.arc = arc
cq.Workplane.segmentArc = segment_arc
