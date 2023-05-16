import json
import numpy as np
import cv2

json_data = '''{"0224.jpeg299751":{"filename":"0224.jpeg","size":299751,"regions":[{"shape_attributes":{"name":"polyline","all_points_x":[840,841],"all_points_y":[396,398]},"region_attributes":{"lane direction":"parallel","lane type":"single white","lane style":"solid"}},{"shape_attributes":{"name":"polyline","all_points_x":[916,844],"all_points_y":[439,394]},"region_attributes":{"lane type":"single white","lane direction":"parallel","lane style":"solid"}},{"shape_attributes":{"name":"polyline","all_points_x":[807,769],"all_points_y":[372,349]},"region_attributes":{"lane type":"single white","lane direction":"parallel","lane style":"solid"}},{"shape_attributes":{"name":"polyline","all_points_x":[1141,1064],"all_points_y":[403,380]},"region_attributes":{"lane type":"single white","lane direction":"parallel","lane style":"solid"}},{"shape_attributes":{"name":"polyline","all_points_x":[1140,1064],"all_points_y":[407,384]},"region_attributes":{"lane type":"single white","lane direction":"parallel","lane style":"solid"}},{"shape_attributes":{"name":"polyline","all_points_x":[994,996,944],"all_points_y":[364,364,349]},"region_attributes":{"lane type":"single white","lane direction":"parallel","lane style":"solid"}},{"shape_attributes":{"name":"polyline","all_points_x":[956,999],"all_points_y":[346,362]},"region_attributes":{"lane type":"single white","lane direction":"parallel","lane style":"solid"}},{"shape_attributes":{"name":"polyline","all_points_x":[585,607],"all_points_y":[352,321]},"region_attributes":{"lane type":"double yellow","lane direction":"parallel","lane style":"solid"}},{"shape_attributes":{"name":"polyline","all_points_x":[479,602],"all_points_y":[468,322]},"region_attributes":{"lane type":"double yellow","lane direction":"parallel","lane style":"solid"}},{"shape_attributes":{"name":"polyline","all_points_x":[450,601],"all_points_y":[468,313]},"region_attributes":{"lane type":"double yellow","lane direction":"prallel","lane style":"solid"}},{"shape_attributes":{"name":"polyline","all_points_x":[461,603],"all_points_y":[469,314]},"region_attributes":{"lane type":"double yellow","lane direction":"parallel","lane style":"solid"}},{"shape_attributes":{"name":"polygon","all_points_x":[1040,1147,868],"all_points_y":[426,412,453]},"region_attributes":{"lane type":"Single white","lane direction":"parallel","lane style":"solid"}},{"shape_attributes":{"name":"rect","x":605,"y":364,"width":494,"height":212},"region_attributes":{"lane type":"Single white","lane direction":"parallel","lane style":"solid"}},{"shape_attributes":{"name":"polyline","all_points_x":[573,694,575,698,579,689,705],"all_points_y":[445,392,450,397,454,409,416]},"region_attributes":{"lane type":"","lane direction":"","lane style":""}},{"shape_attributes":{"name":"polyline","all_points_x":[781,486,930,533,497,822,506,788,534,772,537,774,544,770,549,770,550,769,551,769,554,763],"all_points_y":[522,473,500,470,474,492,472,490,471,486,469,483,470,484,467,481,466,481,465,480,462,477]},"region_attributes":{"lane type":"","lane direction":"","lane style":""}}],"file_attributes":{"caption":"","public_domain":"no","image_url":""}}}'''


# Load the JSON content
data = json.loads(json_data)

print(data)

# Create a blank image with the same dimensions as your input image
height, width = 720, 1280
mask = np.zeros((height, width), dtype=np.uint8)

# Loop through each polyline annotation
for key in data:
    if 'shape_attributes' in data[key]:
        shape_attributes = data[key]['shape_attributes']
        all_points_x = shape_attributes['all_points_x']
        all_points_y = shape_attributes['all_points_y']

        # Create an array of points for the polyline
        points = np.array(list(zip(all_points_x, all_points_y)), dtype=np.int32)

        # Draw the polyline on the mask image
        cv2.polylines(mask, [points], isClosed=False, color=255, thickness=3)

# Save the mask image
cv2.imwrite("mask.png", mask)


import json
import cv2
import os
import numpy as np

# Read JSON file
with open('/content/via_project_23Apr2023_10h38m_json (5).json', 'r') as f:
    data = json.load(f)

# Create output directory for masks
os.makedirs('masks', exist_ok=True)

# Define the image directory if images are not in the same directory as the script
image_directory = '/content/Images'

# Iterate through images
for image_data in data.values():
    filename = image_data['filename']
    img = cv2.imread(os.path.join(image_directory, filename))
    
    if img is None:
        print(f"Failed to load image: {filename}")
        continue

    height, width, _ = img.shape
    mask = np.zeros((height, width), dtype=np.uint8)

    for region in image_data['regions']:
        shape_attributes = region['shape_attributes']
        if shape_attributes['name'] == 'polyline':
            points = np.array([shape_attributes['all_points_x'], shape_attributes['all_points_y']]).T
            # Convert polyline to a closed polygon by connecting the last and first points
            points = np.vstack((points, points[0]))
            cv2.fillPoly(mask, [points], color=(255))

    mask_filename = os.path.splitext(filename)[0] + '_mask.png'
    output_path = os.path.join('masks', mask_filename)
    cv2.imwrite(output_path, mask)
    print(f"Mask saved to: {output_path}")

import json
import cv2
import os
import numpy as np

# Read JSON file
with open('/content/drive/MyDrive/label_annotations_test_update_json (4).json', 'r') as f:
    data = json.load(f)

# Create output directory for masks
os.makedirs('masks', exist_ok=True)

# Define the image directory if images are not in the same directory as the script
image_directory = '/content/drive/MyDrive/Imagelabels/test label'  # Update this line to the folder containing the images

# Get a list of all image files in the folder
image_files = [f for f in os.listdir(image_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Iterate through images
for filename in image_files:
    # Check if there is annotation data for the image
    image_id = f"{filename}{os.stat(os.path.join(image_directory, filename)).st_size}"
    if image_id not in data:
        print(f"No annotation data found for image: {filename}")
        continue

    image_data = data[image_id]
    img = cv2.imread(os.path.join(image_directory, filename))

    if img is None:
        print(f"Failed to load image: {filename}")
        continue

    height, width, _ = img.shape
    mask = np.zeros((height, width), dtype=np.uint8)

    for region in image_data['regions']:
        shape_attributes = region['shape_attributes']
        if shape_attributes['name'] == 'polyline':
            points = np.array([shape_attributes['all_points_x'], shape_attributes['all_points_y']]).T
            # Convert polyline to a closed polygon by connecting the last and first points
            points = np.vstack((points, points[0]))
            cv2.fillPoly(mask, [points], color=(255))

    mask_filename = os.path.splitext(filename)[0] + '_mask.png'
    output_path = os.path.join('masks', mask_filename)
    cv2.imwrite(output_path, mask)
    print(f"Mask saved to: {output_path}")
