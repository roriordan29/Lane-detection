import csv
import os
import cv2
import json
import numpy as np

# set the path to your CSV file
csv_file = "/content/drive/MyDrive/label_annotations_test_UpdateTrain_csv.csv"

# set the path to the directory containing the images
image_dir = "/content/drive/MyDrive/Imagelabels/test label/"

# set the output directory for the YOLO annotations
output_dir = "/content/drive/MyDrive/yolo_annotationstrain"

# create the output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# define a dictionary to map class names to class IDs
class_dict = {"Lane": 0, "Non lane": 1,}

# loop through each row in the CSV file and generate the YOLO mask
with open(csv_file, "r") as f:
    reader = csv.reader(f)
    next(reader, None)  # skip the header row
    for row in reader:
        try:
            filename, _, _, _, _, shape_attributes, region_attributes = row

            # extract the polygon vertices from the shape_attributes field
            shape_attributes_dict = json.loads(shape_attributes)
            vertices = []
            for key in ["all_points_x", "all_points_y"]:
                vertices.append(shape_attributes_dict[key])

            # extract the class name and convert it to a class ID
            class_name = json.loads(region_attributes).get("laneType")
            class_id = class_dict[class_name]

            # read the image and create a mask with the same dimensions
            img_path = os.path.join(image_dir, filename)
            img = cv2.imread(img_path)
            mask = np.zeros_like(img[:, :, 0], dtype=np.uint8)

            # fill the polygon with the corresponding class ID
            polygon = np.array(vertices).T
            cv2.fillPoly(mask, [polygon], class_id)

            # write the YOLO mask to a file
            mask_file = os.path.join(output_dir, os.path.splitext(filename)[0] + ".png")
            cv2.imwrite(mask_file, mask)
            
import csv
import os
import cv2
import json

# set the path to your CSV file
csv_file = "/content/drive/MyDrive/label_annotations_test_UpdateTrain_csv.csv"

# set the path to the directory containing the images
image_dir = "/content/drive/MyDrive/test"

# set the output directory for the YOLO annotations
output_dir = "/content/drive/MyDrive/yolo_annotationstraining"

# create the output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# define a dictionary to map class names to class IDs
class_dict = {"Lane": 0, "Non lane": 1,}

# loop through each row in the CSV file and generate the YOLO annotations
with open(csv_file, "r") as f:
    reader = csv.reader(f)
    next(reader, None)  # skip the header row
    for row in reader:
        try:
            filename, _, _, _, _, shape_attributes, region_attributes = row

            # extract the polygon vertices from the shape_attributes field
            shape_attributes_dict = json.loads(shape_attributes)
            vertices = []
            for key in ["all_points_x", "all_points_y"]:
                vertices.extend(shape_attributes_dict[key])

            # extract the class name and convert it to a class ID
            class_name = json.loads(region_attributes).get("laneType")
            class_id = class_dict[class_name]

            # read the image dimensions
            img_path = os.path.join(image_dir, filename)
            img = cv2.imread(img_path)
            img_height, img_width, _ = img.shape

            # convert the polygon vertices to YOLO format
            x_min, y_min, x_max, y_max = min(vertices[0::2]), min(vertices[1::2]), max(vertices[0::2]), max(vertices[1::2])
            x_center = (x_min + x_max) / 2.0
            y_center = (y_min + y_max) / 2.0
            w = x_max - x_min
            h = y_max - y_min

            # write the YOLO annotation to a file
            annotation_file = os.path.join(output_dir, os.path.splitext(filename)[0] + ".txt")
            with open(annotation_file, "a") as f:
                f.write(f"{class_id} {x_center / img_width:.6f} {y_center / img_height:.6f} {w / img_width:.6f} {h / img_height:.6f}\n")
