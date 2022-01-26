import cv2
import mediapipe as mp
import numpy as np

mp_holistic = mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)


def extract_keypoints(results):
    start_keypoint = results.pose_landmarks.landmark[0] if results.pose_landmarks else 0
    pose = np.array(
        [[res.x - start_keypoint.x, res.y - start_keypoint.y, res.z - start_keypoint.z, res.visibility]
         for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(
        132)

    face = np.array(
        [[res.x, res.y, res.z] for res in
         results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(1404)

    lh = np.array(
        [[res.x - start_keypoint.x, res.y - start_keypoint.y, res.z - start_keypoint.z] for res in
         results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(
        21 * 3)

    rh = np.array(
        [[res.x - start_keypoint.x, res.y - start_keypoint.y, res.z - start_keypoint.z] for res in
         results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(
        21 * 3)

    return np.concatenate([pose, face, lh, rh])


class MediapipeHolistic:
    def process_image(self, img):
        image = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False

        results = mp_holistic.process(image)

        return extract_keypoints(results)
