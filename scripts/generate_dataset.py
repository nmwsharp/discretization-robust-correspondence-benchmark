import os, sys, subprocess, shutil, random

import numpy as np
from sklearn.neighbors import KDTree
import openmesh

# import polyscope as ps
# ps.init()

# options
test_only = True

scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__))) 
root_dir = os.path.abspath(os.path.join(scripts_dir, ".."))
orig_dir = os.path.join(root_dir, "orig")
out_dir = os.path.join(root_dir, "wild")


import torch
from torch_geometric.data import Data


def read_ply(path):
    mesh = openmesh.read_trimesh(path)
    pos = torch.from_numpy(mesh.points()).to(torch.float)
    face = torch.from_numpy(mesh.face_vertex_indices())
    face = face.t().to(torch.long).contiguous()
    if face.shape[0] > 0:
        return Data(pos=pos, face=face)
    else:
        return Data(pos=pos)



def exec_cmd(cmd_str):
    # print("EXEC: {}".format(cmd_str))

    with subprocess.Popen(cmd_str, shell=True, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'), preexec_fn=os.setsid) as process:

        try:
            output = process.communicate(timeout=99999999999)[0]
        except subprocess.TimeoutExpired:
            print("  Timeout on {} :(".format(cmd_str))
            os.killpg(process.pid, subprocess.signal.SIGINT)  # send signal to the process group
            output = process.communicate()[0]
        except Exception as e:
            print("  EXCEPTION ON {} !!!!".format(cmd_str))
            print(str(e))

        return output


# Adaptive isotropic remeshing to have uniform triangles, at about the same resolution as the input.
def mutate_mesh_iso(in_filename, out_filename):

    cmd_str = 'meshlabserver -i {} -o {} -s {}/iso.mlx'.format(in_filename, out_filename, scripts_dir)
    exec_cmd(cmd_str)

# Runs marching cubes on the mesh, roughly doubling resolution
def mutate_mesh_mc(in_filename, out_filename):
    
    cmd_str = 'meshlabserver -i {} -o {} -s {}/mc.mlx'.format(in_filename, out_filename, scripts_dir)
    exec_cmd(cmd_str)

# Create a nonuniformly-dense mesh by refining around 5 randomly chosen faces, then smoothing out with isotropic remeshing
def mutate_mesh_dense(in_filename, out_filename):

    # Count the number of faces in the input file
    data_orig = read_ply(in_filename)
    verts_orig = data_orig.pos.detach().numpy()
    faces_orig = data_orig.face.transpose(0,1).contiguous().detach().numpy()
    n_face = faces_orig.shape[0]

    # Pick 5 random verts and substitute them in to the script
    rand_faces = random.sample(list(range(n_face)), 5)

    # Read in the raw script
    with open(os.path.join(scripts_dir, "dens.mlx"), 'r') as file:
        raw_script = file.read().replace('\n', '')

    # Substitute in the faces to refine around
    sub_script = raw_script.format(*rand_faces)

    # Write the replaced script to file
    tmp_script_path = os.path.join(scripts_dir, "dens_tmp.mlx")
    with open(tmp_script_path, 'w') as file:
        file.write(sub_script)

    cmd_str = 'meshlabserver -i {} -o {} -s {}/dens_tmp.mlx'.format(in_filename, out_filename, scripts_dir)
    exec_cmd(cmd_str)

    # Delete the replaced script
    os.remove(tmp_script_path) 

# Perform two rounds of midpoint subdiving to make the mesh much finer, then simplify it back to ~2x the original resolution. Tends to leave lots of funky triangles and nonuniformly sampled patches.
def mutate_mesh_qes(in_filename, out_filename):
    
    cmd_str = 'meshlabserver -i {} -o {} -s {}/qes.mlx'.format(in_filename, out_filename, scripts_dir)
    exec_cmd(cmd_str)


# Sample a point cloud with normals
def mutate_mesh_cloud(in_filename, out_filename):
    
    cmd_str = 'meshlabserver -i {} -o {} -m vn -s {}/cloud.mlx'.format(in_filename, out_filename, scripts_dir)
    exec_cmd(cmd_str)


mutators = {
    'iso' : mutate_mesh_iso,
    'mc' : mutate_mesh_mc,
    'dense' : mutate_mesh_dense,
    'qes' : mutate_mesh_qes,
    'cloud' : mutate_mesh_cloud,
}


# Read the files to process
to_process = sorted([f for f in os.listdir(orig_dir)
                     if os.path.isfile(os.path.join(orig_dir, f))])

for in_file in to_process:

    # Parse out the name from the FAUST format
    name_prefix = in_file[:7]
    num = in_file[7:10]

    # Optionally skip training set
    if test_only and int(num) < 80:
        continue
    
    print("\nProcessing {} {}  num {}".format(in_file, name_prefix, num))
    in_filename = os.path.join(orig_dir, in_file)
        
    # Read the original mesh, we will need it below
    data_orig = read_ply(in_filename)
    verts_orig = data_orig.pos.detach().numpy()
    faces_orig = data_orig.face.transpose(0,1).contiguous().detach().numpy()

    for mut in mutators:

        out_filename = os.path.join(out_dir, name_prefix + mut + "_" + num + ".ply")
        label_filename = os.path.join(out_dir, name_prefix + mut + "_" + num + ".txt")

        ## Construct the mutated mesh
        mutators[mut](in_filename, out_filename)

        
        ## Use nearest neighbors on the original shape to find correspondence
        
        # Read in the mesh we just created
        data_mut = read_ply(out_filename)
        verts_mut = data_mut.pos.detach().numpy()
        # faces_mut = data_mut.face.transpose(0,1).contiguous().detach().numpy()

        # look up labels from reference
        kdt = KDTree(verts_orig, leaf_size=30, metric='euclidean')
        labels = kdt.query(verts_mut, k=1, return_distance=False)[:,0]

        np.savetxt(label_filename, labels, fmt="%d")

        print("  method: {}  result mesh has {} verts".format(mut, verts_mut.shape[0]))
        

        # Visualize. Always visualize.
        # ps_mut = ps.register_surface_mesh("mut", verts_mut, faces_mut)
        # ps_orig = ps.register_surface_mesh("orig", verts_orig, faces_orig)
        # ps_mut.add_scalar_quantity("labels", labels)
        # ps.show()

