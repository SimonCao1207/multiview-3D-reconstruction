import os

class ImageLoader:
    def __init__(self, path="./data/NotreDame/list.txt"):
        self.img_dct = {}
        with open(path, 'r') as f:
            for line in f:
                img_dir = line.strip()
                img_group = img_dir.split("/")[1].split("_")[0]
                if img_group not in self.img_dct:
                    self.img_dct[img_group] = [img_dir]
                else:
                    self.img_dct[img_group].append(img_dir)
        pass


class SFM():
    def __init__(self, img_dir):
        self.img_obj = ImageLoader(img_dir)
    
    def triangulation(self):
        """
            Triangulates 3d points from 2d vectors and projection matrices
            returns projection matrix of first camera, projection matrix of second camera, point cloud 
        """
        pass

    def PnP(self):
        """
            Finds an object pose from 3D-2D point correspondences using the RANSAC scheme.
            returns rotational matrix, translational matrix, image points, object points, rotational vector
        """
        pass

    def reprojection_error(self):
        """
            Calculate the reprojection error ie the distance between the projected points and the actual points.
            returns total error, object points
        """
        pass

    def optimal_projection_error(self):
        """
            Calculates of the reprojection error during bundle adjustment
            returns error 
        """

    def bundle_adjustment(self):
        """
            Bundle adjustment for the image and object points
            returns object points, image points, transformation matrix
        """
        pass

    def common_points(self):
        """
            Finds the common points between image 1 and 2 , image 2 and 3
            returns common points of image 1-2, common points of image 2-3, mask of common points 1-2 , mask for common points 2-3 
        """
        pass

    def __call__(self):
        pass

if __name__ == "__main__":
    imgObj = ImageLoader()
    img_dct = imgObj.img_dct
    img_dct_new = {}
    for k, v in img_dct.items():
        if len(v) > 1:
            img_dct_new[k] = v
    print(img_dct_new)