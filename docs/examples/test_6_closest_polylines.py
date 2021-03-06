# compas_wood
from compas.geometry import midpoint_point_point
from compas.geometry import scale_vector

from compas.geometry import Point
from compas.geometry import Polyline
from compas_wood.joinery import test
from compas_wood.joinery import closest_polylines
import data_set_beams

# viewer
from compas_wood.viewer_helpers import display

import os

os.system("cls" if os.name == "nt" else "clear")

# ==============================================================================
# Create a list of polyline pairs - input, then generate joints and display them
# ==============================================================================


def test_closest_polylines():

    polylines = data_set_beams.polylines_5()
    segment_radii = data_set_beams.polylines_radii_5()

    segment_normals = data_set_beams.polylines_vector_3()

    # Generate connections
    neighbours, pair_points = closest_polylines(polylines, segment_radii, 20)

    # Display normals
    normals = []
    for i in range(len(polylines)):
        p0 = midpoint_point_point(polylines[i][0], polylines[i][1])
        v = scale_vector(segment_normals[i], 15)
        p1 = Point(p0[0] + v[0], p0[1] + v[1], p0[2] + v[2])
        pline = Polyline([p0, p1])
        normals.append(pline)
    polylines.extend(normals)

    # Display via Compas_View2
    display(polylines, pair_points, None, 0.01, 0, 0)


# ==============================================================================
# call the compas_wood methods
# ==============================================================================
test()
test_closest_polylines()
