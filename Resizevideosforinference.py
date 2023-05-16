import cv2
import os

output_folder = '/content/drive/MyDrive/input/videos'
os.makedirs(output_folder, exist_ok=True)


def resize_video(input_video_path, output_video_path, target_width, target_height):
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Failed to open input video: {input_video_path}")
        return

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, cap.get(cv2.CAP_PROP_FPS), (target_width, target_height))

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        resized_frame = cv2.resize(frame, (target_width, target_height))
        out.write(resized_frame)

    print(f"Processed {frame_count} frames for video: {input_video_path}")
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Example usage:
input_video_path = '/content/drive/MyDrive/Dataset videos (1)/Videos/Daytime urban traffic poor road markings.mp4'
output_video_path = '/content/drive/MyDrive/input/videos/Daytime urban traffic poor road markings.mp4'
target_width, target_height = 1280, 720  # Change these values to match the expected dimensions by YOLOP model
resize_video(input_video_path, output_video_path, target_width, target_height)

import cv2
import os

output_folder = '/content/drive/MyDrive/Resizedvideos1'
os.makedirs(output_folder, exist_ok=True)


def resize_video(input_video_path, output_video_path, target_width, target_height):
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Failed to open input video: {input_video_path}")
        return

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_video_path, fourcc, cap.get(cv2.CAP_PROP_FPS), (target_width, target_height))

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        resized_frame = cv2.resize(frame, (target_width, target_height))
        out.write(resized_frame)

    print(f"Processed {frame_count} frames for video: {input_video_path}")
    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Example usage:
input_video_path = '/content/drive/MyDrive/Resizedvideos/Day time N20 raining.mp4'
output_video_path = '/content/drive/MyDrive/Resizedvideos1/Day time N20 raining.mp4'
target_width, target_height = 1280, 720  # Change these values to match the expected dimensions by YOLOP model
resize_video(input_video_path, output_video_path, target_width, target_height)
