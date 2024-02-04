import open3d as o3d
import numpy as np

DATA_PATH = "./data/NotreDame/notredame.ply"

def show_mesh_alpha_shape(data_path, alpha=0.001):
    pcd = o3d.io.read_point_cloud(data_path)
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
    mesh.compute_vertex_normals()
    o3d.visualization.draw_geometries([mesh], mesh_show_back_face=True)

def show_mesh_ball_pivoting(data_path):
    radii = [0.005, 0.01, 0.02, 0.04]
    pcd = o3d.io.read_point_cloud(data_path)
    pcd.estimate_normals(
    search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
    rec_mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
        pcd, o3d.utility.DoubleVector(radii))
    o3d.visualization.draw_geometries([pcd, rec_mesh])

def show_pcd(data_path):
    pcd = o3d.io.read_point_cloud(data_path)
    o3d.visualization.draw_geometries([pcd])

if __name__ == "__main__":
    show_pcd(DATA_PATH)