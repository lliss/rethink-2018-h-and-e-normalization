from sklearn.cluster import KMeans
from functools import reduce
import numpy as np
import imageio as imageio
import colorsys
import math
from demo import Demo
from tkinter import Tk



def pol2cart(rho, phi, z):
    x = rho * math.cos(phi)
    y = rho * math.sin(phi)
    return [x, y, z]


def cart2pol(x, y, z):
    rho = math.sqrt(x * x + y * y)
    phi = math.atan2(y, x)
    return [rho, phi, z]


def hsv_to_hsvc(hsv):
    # Hue is the the angular component of the coordinate,
    # hence the strange order.
    return pol2cart(hsv[1], 2 * math.pi * hsv[0], hsv[2])


def rgb255_to_hsv(rgb):
    return colorsys.rgb_to_hsv(rgb[0] / 255, rgb[1] / 255, rgb[2] / 255)
    

def hsv_to_rgb255(hsv):
    rgb = colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])
    return [rgb[0] * 255, rgb[1] * 255, rgb[2] *255]
    

def hsvc_to_hsv(hsvc):
    polar = cart2pol(hsvc[0], hsvc[1], hsvc[2])
    return [((polar[1] % (2 * math.pi)) / (2 * math.pi)) , polar[0], polar[2]]


def colorassign_manual(rgb):
    # Color assignment

    # Program options and constants
    # Cluster parameters
    NCLUST = 10                # number of clusters
    CLUSTERITER = 1e5          # maximum k-means iterations

    ## Manual color assignment

    # Convert RGB into HSV parts
    #hsv = [[colorsys.rgb_to_hsv(rgb_color_array[0] / 255, rgb_color_array[1] / 255, rgb_color_array[2] / 255) for rgb_color_array in row] for row in rgb]
    hsv = [[rgb255_to_hsv(rgb_color_array) for rgb_color_array in row] for row in rgb]
    
    # transform HSV from cylindrical to cartesian coordinates
    # hsv_cartesian = [[pol2cart(2 * math.pi * hsv_color_array[0], hsv_color_array[1], hsv_color_array[2]) for hsv_color_array in row] for row in hsv]
    hsv_cartesian = [[hsv_to_hsvc(hsv_color_array) for hsv_color_array in row] for row in hsv]

    
    # Perform clustering via kmeans
    flattened_hsv_cartesian = [cell for row in hsv_cartesian for cell in row]
    image_kmeans = KMeans(n_clusters=NCLUST, random_state=1, max_iter=CLUSTERITER).fit(flattened_hsv_cartesian)
    
    # Produced image of cluster labels.
    indexed_image = np.reshape(image_kmeans.labels_, (len(rgb), len(rgb[0])))

    # Find centroids of color labels in HSVC space.
    centroids = image_kmeans.cluster_centers_
    centroids_polar = [hsvc_to_hsv(hsvc_array) for hsvc_array in centroids]
    centroids_rgb = [hsv_to_rgb255(hsv_array) for hsv_array in centroids_polar]
    print(centroids[0][0], centroids[0][1], centroids[0][2])
    print(centroids)

    root = Tk()    
    color_chooser = Demo(root, indexed_image, centroids_rgb)
    root.mainloop()
    #root.destroy()
    print(color_chooser.test)
#
#    # identify centroids in HSV-C space
#    centroidc = NaN(NCLUST,3);
#    for i = 1:NCLUST:
#        centroidc(i,:) = mean(hsvc(:,idx==i),2);
#    hsvc=None;
#
#    # transform centroids to HSV space
#    centroid = NaN(size(centroidc));
#    for i in range(1,NCLUST)
#        [centroid(i,1),centroid(i,2),centroid(i,3)] = cart2pol(centroidc(i,1),centroidc(i,2),centroidc(i,3));
#        centroid(i,1) = mod(centroid(i,1),2*pi)/2/pi;
#    end
#
#    # define colormap
#    cmap = hsv2rgb(centroid);
#
#    # user defined classes (GUI)
#    classidx = HEselector5(idx,cmap);
#
#    # parse classidx into classes
#    lumen = find(classidx==1);
#    nuclei = find(classidx==2);
#    stroma = find(classidx==3);
#    cytoplasm = find(classidx==4);

#return {'imageMap': idx, 'lumen': lumen, 'nuclei': nuclei, 'stroma': stroma, 'cytoplasm': cytoplasm}
# 
   

image = imageio.imread('path/to/image.tif')
colorassign_manual(image)