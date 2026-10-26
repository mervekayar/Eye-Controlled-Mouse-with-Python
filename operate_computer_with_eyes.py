
import cv2
import mediapipe as mp
import pyautogui
import os
import time
import math

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "face_landmarker.task"
)

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=RunningMode.VIDEO,
    num_faces=1
)

screen_w, screen_h = pyautogui.size()

pyautogui.PAUSE = 0.01

cam = cv2.VideoCapture(0)

timestamp_ms = 0
last_click_time = 0
click_cooldown = 1.0

BLINK_THRESHOLD = 0.18

try:
    with FaceLandmarker.create_from_options(options) as face_landmarker:

        while True:
            success, image = cam.read()

            if not success:
                print("Could not capture camera image")
                break

            image = cv2.flip(image, 1)

            window_h, window_w = image.shape[:2]

            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb_image
            )

            timestamp_ms = max(
                timestamp_ms + 1,
                int(time.monotonic() * 1000)
            )

            result = face_landmarker.detect_for_video(
                mp_image,
                timestamp_ms
            )

            if result.face_landmarks:

                landmarks = result.face_landmarks[0]

                iris_indices = range(468, 478)

                for idx in iris_indices:
                    if idx >= len(landmarks):
                        continue

                    point = landmarks[idx]
                    x = int(point.x * window_w)
                    y = int(point.y * window_h)

                    cv2.circle(
                        image,
                        (x, y),
                        3,
                        (0, 0, 255),
                        -1
                    )

                eye_indices = [33, 133, 159, 145, 362, 263, 386, 374]

                for idx in eye_indices:
                    point = landmarks[idx]
                    x = int(point.x * window_w)
                    y = int(point.y * window_h)

                    cv2.circle(
                        image,
                        (x, y),
                        3,
                        (0, 255, 255),
                        -1
                    )

                left_eye_top = landmarks[159]
                left_eye_bottom = landmarks[145]
                left_eye_left = landmarks[33]
                left_eye_right = landmarks[133]

                vertical_distance = math.dist(
                    (left_eye_top.x, left_eye_top.y),
                    (left_eye_bottom.x, left_eye_bottom.y)
                )

                horizontal_distance = math.dist(
                    (left_eye_left.x, left_eye_left.y),
                    (left_eye_right.x, left_eye_right.y)
                )

                eye_ratio = (
                    vertical_distance / horizontal_distance
                    if horizontal_distance > 0
                    else 1
                )

                iris_points = landmarks[468:478]

                iris_x = sum(p.x for p in iris_points) / len(iris_points)
                iris_y = sum(p.y for p in iris_points) / len(iris_points)

                mouse_x = int(iris_x * screen_w)
                mouse_y = int(iris_y * screen_h)

                mouse_x = max(0, min(screen_w - 1, mouse_x))
                mouse_y = max(0, min(screen_h - 1, mouse_y))

                pyautogui.moveTo(mouse_x, mouse_y)

                current_time = time.time()

                if (
                    eye_ratio < BLINK_THRESHOLD
                    and current_time - last_click_time > click_cooldown
                ):
                    pyautogui.click()
                    last_click_time = current_time
                    print("Mouse clicked")

                cv2.putText(
                    image,
                    f"Eye ratio: {eye_ratio:.2f}",
                    (20, 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

            cv2.imshow("Eye controlled with mouse", image)

            key = cv2.waitKey(1) & 0xFF

            if key == 27:
                break

finally:
    cam.release()
    cv2.destroyAllWindows()
