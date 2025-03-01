import cv2 as cv
import numpy as np
import mediapipe as mp

class PoseDetector:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()
        self.mp_drawing = mp.solutions.drawing_utils  # For drawing keypoints

    def process_frame(self, frame):
        """Convert frame and detect pose landmarks."""
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        return results

    def draw_landmarks(self, frame, results):
        """Draw pose landmarks at the correct positions."""
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(frame, results.pose_landmarks,
                                           self.mp_pose.POSE_CONNECTIONS)

        return frame

    def get_landmark(self, results, landmark_name):
        """Get a specific landmark by name."""
        if results.pose_landmarks:
            landmark = results.pose_landmarks.landmark[self.
            mp_pose.PoseLandmark[landmark_name]]
            return landmark
        return None

    def is_hand_raised(self, frame, results):
        if results.pose_landmarks:
            height, width, _ = frame.shape  # Get frame size

            # Get y-coordinates (normalized) of wrists and shoulders
            y1, y2 = (results.pose_landmarks.landmark[15].y,
                      results.pose_landmarks.landmark[16].y) #left, right wrist
            y1, y2 = y1 * height, y2 * height  # Convert to pixel coordinates

            y3, y4 = (results.pose_landmarks.landmark[11].y,
                      results.pose_landmarks.landmark[12].y)
            y3, y4 = y3 * height, y4 * height  # Convert to pixel coordinates

            # Check if any of the wrists are raised above the shoulders
            if y1 < y3 or y2 < y4:
                return True
        return False

    def is_squatting(self,frame,results):

        if results.pose_landmarks:
            wid, hei, _ = frame.shape
            # left and right knee-joint
            y1, y2 = (results.pose_landmarks.landmark[25].y*hei,
                      results.pose_landmarks.landmark[26].y*hei)
            #left and right waist point
            y3, y4 = (results.pose_landmarks.landmark[23].y*hei,
                      results.pose_landmarks.landmark[24].y*hei)

            if(y1<=y3 and y2<=y4):
                if hasattr(self, 'previous_hip_y'):
                    if self.previous_hip_y - hip_y > threshold:
                        self.previous_hip_y = hip_y
                        return True
                else:
                    self.previous_hip_y = hip_y
        return False




    def is_jumping(self,frame,results):
        wid, hei, _ = frame.shape

        if results.pose_landmarks:
            # left & right hip
            y1, y2 = (results.pose_landmarks.landmark[27].y*hei,
                      results.pose_landmarks.landmark[28].y*hei,)
            hip_y = (y1+y2)//2
            threshold = 10
            if hasattr(self, 'previous_hip_y'):
                if self.previous_hip_y - hip_y > threshold:
                    self.previous_hip_y = hip_y
                    return True
            else:
                self.previous_hip_y = hip_y
        return False

    def is_leaning_right(self,frame,results):
        threshold = 100
        wid, hei, _ = frame.shape
        midx,midy = wid//2, hei//2
        if results.pose_landmarks:
            #get the position for the nose
            x,y = (results.pose_landmarks.landmark[0].x*wid,
                   results.pose_landmarks.landmark[0].y*hei)
            if midx-x>threshold:
                return True
        return False

    def is_leaning_left(self, frame, results):
        threshold = 100
        wid, hei, _ = frame.shape
        midx, midy = wid // 2, hei // 2
        if results.pose_landmarks:
            # get the position for the nose
            x, y = (results.pose_landmarks.landmark[0].x*wid,
                    results.pose_landmarks.landmark[0].y*hei)
            if x-midx > threshold:
                return True
        return False
