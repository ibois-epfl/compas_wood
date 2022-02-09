# compas_wood
from compas_wood.joinery import joints
import data_set_plates


# viewer
from compas_wood.viewer_helpers import display

# ==============================================================================
# Create a list of polyline pairs - input, then generate joints and display them
# ==============================================================================


def test_joints():

    # Get a list of polyline pairs
    input = data_set_plates.c_15()
    # input = data_set_plates_annen.annen_polylines()

    # Compute joint polylines
    element_pairs_list, joint_areas_polylines, joint_types = joints(input, 2)

    # print((len)(joint_areas_polylines))
    # print((len)(joint_types))
    # print(element_pairs_list)

    # Display via Compas_View2
    display(input, joint_areas_polylines, None, 0.01, 0, 0, 0, False, joint_types)


# ==============================================================================
# call the compas_wood methods
# ==============================================================================
test_joints()
