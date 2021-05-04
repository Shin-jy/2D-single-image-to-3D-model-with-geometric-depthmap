import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

import cv2
import pdb



print("Read Input & Output")

color_raw = o3d.io.read_image("./input/input.jpg")#color_raw

depth_map = cv2.imread("./output/depthMap.jpg")#depthmap reversing
depth_map = 255 - depth_map
cv2.imwrite("./output/reverse_depth.jpg",depth_map)

depth_raw = o3d.io.read_image("./output/reverse_depth.jpg")#depth_raw
rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(color_raw, depth_raw)

rgbd = np.asarray(rgbd_image)
print(rgbd)
#rgbd = rgbd_image.convert_rgb_to_intensity
#rgbd = cv2.imread(rgbd_image)
#cv2.imwrite("./output/rgbd_image.jpg",rgbd)


plt.subplot(1, 2, 1)
plt.title('Grayscale image')
plt.imshow(rgbd_image.color)
plt.subplot(1, 2, 2)
plt.title('Depth image')
plt.imshow(rgbd_image.depth)
plt.show()



pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
        rgbd_image,
        o3d.camera.PinholeCameraIntrinsic(
            o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault))
# Flip it, otherwise the pointcloud will be upside down
pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
o3d.visualization.draw_geometries([pcd])




print("Statistical oulier removal")
cl, ind = pcd.remove_statistical_outlier(nb_neighbors=20,                                                     std_ratio=4.0)
inlier_cloud = pcd.select_by_index(ind)
outlier_cloud = pcd.select_by_index(ind, invert=True)

o3d.visualization.draw_geometries([inlier_cloud])


print("Showing outliers (red) and inliers (gray): ")
outlier_cloud.paint_uniform_color([1, 0, 0])
inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])





#print("Downsample the point cloud with a voxel of 0.02")
#voxel_down_pcd = pcd.voxel_down_sample(voxel_size=0.00001)
#o3d.visualization.draw_geometries([voxel_down_pcd])






#print("Statistical oulier removal")
#cl, ind = voxel_down_pcd.remove_statistical_outlier(nb_neighbors=20
#                                                    std_ratio=2.0)
#inlier_cloud = voxel_down_pcd.select_by_index(ind)
#outlier_cloud = voxel_down_pcd.select_by_index(ind, invert=True)

#o3d.visualization.draw_geometries([inlier_cloud])
#print("Showing outliers (red) and inliers (gray): ")
#outlier_cloud.paint_uniform_color([1, 0, 0])
#inlier_cloud.paint_uniform_color([0.8, 0.8, 0.8])
#o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])







###########
#clustering
###########
#with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
#    labels = np.array(pcd.cluster_dbscan(eps=0.00001, min_points=5))
#
#max_label = labels.max()
#print(f"point cloud has {max_label + 1} clusters")
#colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
#colors[labels < 0] = 0
#pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
#o3d.visualization.draw_geometries([pcd])


###################
#plane segmentation
###################
#plane_model, inliers = pcd.segment_plane(distance_threshold=0.001, ransac_n=3, num_iterations=2000)
#[a, b, c, d] = plane_model
#print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

#inlier_cloud = pcd.select_by_index(inliers)
#inlier_cloud.paint_uniform_color([1.0, 0, 0])
#outlier_cloud = pcd.select_by_index(inliers, invert=True)
#o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])


###################
#Downsampling
###################
#print("Downsample the point cloud with a voxel of 0.02")
#voxel_down_pcd = pcd.voxel_down_sample(voxel_size=0.00001)
#o3d.visualization.draw_geometries([voxel_down_pcd])


#o3d.io.write_point_cloud("./test.ply", pcd, write_ascii=False, compressed=False, print_progress=False)

#pcd = o3d.io.read_point_cloud("./test.ply")
#o3d.visualization.draw_geometries([pcd])

