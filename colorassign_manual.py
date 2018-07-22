from sklearn.cluster import KMeans
from functools import reduce
import numpy as np
import imageio as imageio
import colorsys
import math
import sys, getopt
import json
from tkinter import Tk
from demo import Demo


RANDOM_STATE = None  # For stable results when testing, set to 1.
NCLUST = 10          # number of clusters
CLUSTERITER = 1e5    # maximum k-means iterations


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
    # Convert RGB into HSV parts
    hsv = [[rgb255_to_hsv(rgb_color_array) for rgb_color_array in row] for row in rgb]

    # transform HSV from cylindrical to cartesian coordinates
    hsv_cartesian = [[hsv_to_hsvc(hsv_color_array) for hsv_color_array in row] for row in hsv]

    # Perform clustering via kmeans
    flattened_hsv_cartesian = [cell for row in hsv_cartesian for cell in row]
    image_kmeans = KMeans(n_clusters=NCLUST, random_state=RANDOM_STATE, max_iter=CLUSTERITER).fit(flattened_hsv_cartesian)

    # Produced image of cluster labels.
    indexed_image = np.reshape(image_kmeans.labels_, (len(rgb), len(rgb[0])))

    # Find centroids of color labels.
    centroids = image_kmeans.cluster_centers_
    centroids_polar = [hsvc_to_hsv(hsvc_array) for hsvc_array in centroids]
    centroids_rgb = [hsv_to_rgb255(hsv_array) for hsv_array in centroids_polar]

    root = Tk()
    color_chooser = Demo(root, indexed_image, centroids_rgb)
    root.mainloop()

    return {
        'indexedImage': indexed_image,
        'lumen': color_chooser.selection_dictionary['lumen'],
        'nuclei': color_chooser.selection_dictionary['nuclei'],
        'stroma': color_chooser.selection_dictionary['stroma'],
        'cytoplasm': color_chooser.selection_dictionary['cytoplasm']
    }


if __name__ == '__main__':
    inputfile = None
    outputfile = None
    argv = sys.argv[1:]
    try:
        opts, args = getopt.getopt(argv, 'hi:o:',['ifile=','ofile='])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--ofile'):
            outputfile = arg

    if inputfile == None:
        print('Input file is required')
        sys.exit()

    image = imageio.imread(inputfile)
    result = colorassign_manual(image)

    if outputfile != None:
        result['indexedImage'] = result['indexedImage'].tolist()
        result = json.dumps(result)
        f = open(outputfile, 'w')
        f.write(result)
    else:
        print('Lumen: ' + str(result['lumen']) + ' Nuclei: ' +
                str(result['nuclei']) + ' Stroma: ' +
                str(result['stroma']) + ' Cytoplasm: ' +
                str(result['cytoplasm']))