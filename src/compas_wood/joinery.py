#from _typeshed import NoneType
import numpy as np
from compas.plugins import plugin
from compas.geometry import Point
from compas.geometry import Polyline
from compas.datastructures import Mesh, mesh
import pybind11_joinery_solver
import time


@plugin(category='compas_wood_cpp', pluggable_name='compas_wood_cpp_test')
def test():
    """Test if C++ code works

    Parameters
    ----------


    Returns
    -------
    Prints 
        Hello from CPP Wood

    """

    pybind11_joinery_solver.pybind11_test()



@plugin(category='compas_wood_cpp', pluggable_name='compas_wood_cpp_test_joinery_solver')
def get_connection_zones(
    polylines_vertices_XYZ,
    face_vectors_XYZ=None,
    face_joints_types_int=None,
    three_valance_element_indices_and_instruction=None,
    default_joint_parameters=None
    ):
    """Compute joinery

    Parameters
    ----------
    polylines_vertices_XYZ : pairs of polylines
    face_vectors_XYZ : vectors to orient a joint
    face_joints_types_int : joint id, existing in the code
    three_valance_element_indices_and_instruction : special case e.g. alignment of rectangles

    Returns
    -------
    List of Polylines 
        with added joints

    """

    # ==============================================================================
    # Prepare input
    # ==============================================================================
    flat_list_of_points = []
    vertex_count_per_polyline = []
    flat_list_of_face_vectors_XYZ = []
    flat_list_of_face_joints_types_int = []
    flat_list_of_three_valance_element_indices_and_instruction = []
    flat_list_default_joint_paramters = [1000, 0.5, 1,  1000, 0.5, 10 ,  1000, 0.5, 20 ,  1000, 0.5, 30 ,  1000, 0.5, 40 ,  1000, 0.5, 50 ]

    flag0 = face_vectors_XYZ!=None;
    if(flag0):
        flag0 = len(face_vectors_XYZ) == len(polylines_vertices_XYZ)*0.5
    print(flag0)


    flag1 = face_joints_types_int!=None;
    if(flag1):
        flag1 = len(face_joints_types_int) == len(polylines_vertices_XYZ)*0.5

    #print(flag1)
    #print(len(face_vectors_XYZ))
    #print(len(face_joints_types_int))
    #print(len(polylines_vertices_XYZ))

    flag2 = three_valance_element_indices_and_instruction!=None;

    if(default_joint_parameters != None):
        if(len(default_joint_parameters)==6*3):
            flat_list_default_joint_paramters = default_joint_parameters



    for i in range(0, (int)(len(polylines_vertices_XYZ)*0.5)):
        flat_list_of_points.extend(polylines_vertices_XYZ[i*2])
        flat_list_of_points.extend(polylines_vertices_XYZ[i*2+1])
        vertex_count_per_polyline.append(len(polylines_vertices_XYZ[i*2]))
        vertex_count_per_polyline.append(len(polylines_vertices_XYZ[i*2+1]))

        if(flag0 and (len(face_vectors_XYZ[i]) == len(polylines_vertices_XYZ[i*2])+1) ):
            flat_list_of_face_vectors_XYZ.extend(face_vectors_XYZ[i])



        if(flag1 and ( len(face_joints_types_int[i])  == (len(polylines_vertices_XYZ[i*2])+1) ) ):
            flat_list_of_face_joints_types_int.extend(face_joints_types_int[i])

    if(flag2):
        for i in range(0, len(three_valance_element_indices_and_instruction)):
            flat_list_of_three_valance_element_indices_and_instruction.extend(three_valance_element_indices_and_instruction[i])


    # ==============================================================================
    # Convert to Numpy
    # ==============================================================================
    V = np.asarray(flat_list_of_points, dtype=np.float64)
    F = np.asarray(vertex_count_per_polyline, dtype=np.int32)
    D = np.asarray(flat_list_of_face_vectors_XYZ, dtype=np.float64)
    J = np.asarray(flat_list_of_face_joints_types_int, dtype=np.int32)
    X = np.asarray(flat_list_of_three_valance_element_indices_and_instruction, dtype=np.int32)
    P = np.asarray(flat_list_default_joint_paramters, dtype=np.float64)

    search_type = 2
    show_plane_normals = True
    division_distance = 300
    shift = 0.6
    output_type = 4
    triangulate = 0

    # ==============================================================================
    # Test CPP module
    # ==============================================================================
 
    print("Input")
    print("flat_list_of_points " + str(V.size))
    print("vertex_count_per_polyline " + str(F.size))
    print("flat_list_of_face_vectors_XYZ " + str(D.size))
    print("flat_list_of_face_joints_types_int " + str(J.size))
    print("flat_list_of_three_valance_element_indices_and_instruction " + str(X.size))
    print("============================================================================== CPP +")

    # ==============================================================================
    # Execute main CPP method
    # ==============================================================================


    start_time = time.time()
    pointsets, pointsets_group_ids = pybind11_joinery_solver.pybind11_get_connection_zones( V, F, D, J, X, P, search_type,division_distance,shift,output_type,triangulate )
    print("==================================== %s ms ====================================" %  round((time.time() - start_time)*1000.0) )
    #print(type(pointsets))
    # ==============================================================================
    # Process output
    # ==============================================================================

    polylines = []
    
    temp_collection = []
    last_id=pointsets_group_ids[0]

    for i in range (len(pointsets)) :
        points = [Point(*point) for point in pointsets[i]]
        polyline = Polyline(points)
        

        if(last_id != pointsets_group_ids[i]):
            polylines.append(temp_collection)
            temp_collection = []
            #print("Hi")

        temp_collection.append(polyline)
        last_id = pointsets_group_ids[i]
        #print(pointsets_group_ids[i])

    polylines.append(temp_collection)
    print("============================================================================== CPP -")
    print("Output")
    print("Number of Polylines " , len(polylines))


    return polylines



@plugin(category='compas_wood_cpp', pluggable_name='compas_wood_cpp_closed_mesh_from_poylylines')
def closed_mesh_from_polylines(
    polylines_vertices_XYZ,
    ):
    """Compute joinery

    Parameters
    ----------
    polylines_vertices_XYZ : pairs of polylines

    Returns
    -------
    Mesh
        from the pairs of polylines

    """

    # ==============================================================================
    # Prepare input
    # ==============================================================================
    flat_list_of_points = []
    vertex_count_per_polyline = []
   


    for i in range(0, (int)(len(polylines_vertices_XYZ)*0.5)):
        flat_list_of_points.extend(polylines_vertices_XYZ[i*2])
        flat_list_of_points.extend(polylines_vertices_XYZ[i*2+1])
        vertex_count_per_polyline.append(len(polylines_vertices_XYZ[i*2]))
        vertex_count_per_polyline.append(len(polylines_vertices_XYZ[i*2+1]))




    # ==============================================================================
    # Convert to Numpy
    # ==============================================================================
    V = np.asarray(flat_list_of_points, dtype=np.float64)
    F = np.asarray(vertex_count_per_polyline, dtype=np.int32)


    # ==============================================================================
    # Test CPP module
    # ==============================================================================
 
    print("Input")
    print("flat_list_of_points " + str(V.size))
    print("vertex_count_per_polyline " + str(F.size))
    print("============================================================================== CPP +")

    # ==============================================================================
    # Execute main CPP method
    # ==============================================================================


    start_time = time.time()
    output_V, output_F = pybind11_joinery_solver.pybind11_closed_mesh_from_polylines( V, F )
    """
    print("V")
    for i in output_V:
        print(i)
    print("F")
    for i in output_F:
        print(i)
    """
    print("==================================== %s ms ====================================" %  round((time.time() - start_time)*1000.0) )
    # ==============================================================================
    # Process output
    # ==============================================================================
    print("Number of Mesh Vertices " , len(output_V))
    print("Number of Mesh Faces " , len(output_F))
    mesh = Mesh.from_vertices_and_faces(output_V,output_F)
    print("Is Mesh Valid " + (str)(mesh.is_valid()) )
    

    print("============================================================================== CPP -")
    print("Output")
    return mesh



