import open3d as o3d
from utils import show_pcd
import numpy as np
DATA_PATH = "./data/NotreDame/notredame.out" 
PLY_PATH = "./data/NotreDame/notredame.ply" 

class Camera:
    def __init__(self, cam_param=None, R=None, t=None):
        """
            <f> <k1> <k2>   [the focal length, followed by two radial distortion coeffs]
            <R>             [a 3x3 matrix representing the camera rotation]
            <t>             [a 3-vector describing the camera translation]
        """
        self.cam_param = cam_param 
        self.R = np.array(R) if R is not None else []
        self.t = np.array(t) if t is not None else []

class Point:
    def __init__(self=None, position=None, color=None, view_list=None):
        """
            <position>      [a 3-vector describing the 3D position of the point]
            <color>         [a 3-vector describing the RGB color of the point]
            <view list>     [a list of views the point is visible in]
        """
        self.position = position if position is not None else []
        self.color = color if color is not None else []
        self.view_list = view_list if view_list is not None else []
        
def read_bundle(path):
    cameras = []
    points = []
    with open(path) as f:
        lines = [line for line in f]
        num_cameras, num_points = map(int, lines[1].split(" "))
        for i, line in enumerate(lines):
            if i in [0,1]: continue
            if i in range(2, 2 + num_cameras*5):
                if  i % 5 == 2: 
                    _cam = [list(map(float, lines[i+j].split(" "))) for j in range(5)]
                    cameras.append(Camera(_cam[0], [_cam[1],_cam[2], _cam[3]], _cam[4]))
            elif (i - num_cameras*5) % 3 == 2:  
                _points = [list(map(float, lines[i+j].split(" "))) for j in range(3)]
                points.append(Point(_points[0], _points[1], _points[2]))

    return cameras, points

def create_point_cloud(points):
    all_points = np.array([point.position for point in points]) 
    all_colors = np.array([point.color for point in points]) 
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(all_points)
    point_cloud.colors = o3d.utility.Vector3dVector(all_colors / 255.0)
    return point_cloud

ply_header = lambda x : f"""
ply
format ascii 1.0
element face 0
property list uchar int vertex_indices
element vertex {x}
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
""".strip()

def write_ply_file(ply_file, cameras, points, decimate_step=1, write_cameras=1):
    f = open(ply_file, "w")
    num_cameras, num_points = len(cameras), len(points)
    num_points_decimate = num_points / decimate_step
    num_points_out = num_points_decimate + 2 * num_cameras if write_cameras else num_points_decimate
    f.write(ply_header(int(num_points_out)))
    f.write("\n")
    for i in range(0, num_points, decimate_step):
        f.write(f"{points[i].position[0]} {points[i].position[1]} {points[i].position[2]} {int(points[i].color[0])} {int(points[i].color[1])} {int(points[i].color[2])}\n")
    if (write_cameras):
        for i in range(num_cameras):
            Rinv = cameras[i].R.T
            c = -1.0 * Rinv @ cameras[i].t
            if (i % 2) == 0:
                f.write(f"{c[0]} {c[1]} {c[2]} 0 255 0\n")
            else:
                f.write(f"{c[0]} {c[1]} {c[2]} 255 0 0\n")
            p_cam = np.array([0.0, 0.0, -0.3])
            p = Rinv @ p_cam
            for i in range(3): 
                p[i] += c[i]
            f.write(f"{p[0]} {p[1]} {p[2]} 255 255 0\n")
    f.close()

if __name__ == "__main__":
    cameras, points = read_bundle(DATA_PATH)
    # pc = create_point_cloud(points)
    # o3d.visualization.draw_geometries([pc])

    write_ply_file(PLY_PATH, cameras, points, write_cameras=0)
    show_pcd(PLY_PATH)

