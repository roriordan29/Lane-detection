import os
import cv2
import numpy as np

images_dir = "/content/drive/MyDrive/Imagelabels/test label"
annotations_dir = "/content/drive/MyDrive/yolo_annotations"
mask_folder = "/content/drive/MyDrive/Masks"

# Create the mask folder if it does not exist
os.makedirs(mask_folder, exist_ok=True)

for img_file in os.listdir(images_dir):
    if img_file.endswith(".jpeg"):
        print(f"Processing image file: {img_file}")

        # Load the image file
        img_path = os.path.join(images_dir, img_file)
        img = cv2.imread(img_path)

        # Load the corresponding annotation file
        anno_file = img_file.replace(".jpeg", ".txt")
        anno_path = os.path.join(annotations_dir, anno_file)
        with open(anno_path, "r") as f:
            annotations = f.readlines()

        # Initialize a blank mask with the same size as the input image
        mask = np.zeros(img.shape[:2], dtype=np.uint8)

        # Loop over the annotations and create masks
        for annotation in annotations:
            class_id, x_center, y_center, width, height = map(float, annotation.strip().split())
            x1 = int((x_center - width / 2) * img.shape[1])
            y1 = int((y_center - height / 2) * img.shape[0])
            x2 = int((x_center + width / 2) * img.shape[1])
            y2 = int((y_center + height / 2) * img.shape[0])

            print(f"Coordinates: x1={x1}, y1={y1}, x2={x2}, y2={y2}")

            # Fill the corresponding area in the mask
            mask[y1:y2, x1:x2] = int(class_id + 1)

        # Print mask information
print(f"Mask shape: {mask.shape}")
print(f"Unique values in mask: {np.unique(mask)}")

# Save the mask to the mask folder
mask_path = os.path.join(mask_folder, img_file.replace(".jpg", ".png"))
cv2.imwrite(mask_path, mask)
print(f"Saved mask to: {mask_path}")  
