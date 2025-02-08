import cv2
import mediapipe as mp
from pycaw.pycaw import AudioUtilities
from math import radians, degrees
import numpy as np

# Initialize MediaPipe Hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Access system audio
audio = AudioUtilities.GetSpeakers()
interface = audio.Activate()
volume = interface.GetVolume()

# Set up OpenCV to capture webcam feed
cap = cv2.VideoCapture(0)

def set_volume(vol):
    # Ensure the volume is between 0 and 1
    volume.SetMasterVolumeLevelScalar(vol, None)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame horizontally for a later mirror effect
    frame = cv2.flip(frame, 1)
    
    # Convert to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame to detect hand landmarks
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get key points for gesture recognition (e.g., wrist and fingertips)
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            
            # Calculate the angle of rotation based on wrist and fingertips
            thumb_angle = np.arctan2(thumb_tip.y - wrist.y, thumb_tip.x - wrist.x) * 180 / np.pi
            pinky_angle = np.arctan2(pinky_tip.y - wrist.y, pinky_tip.x - wrist.x) * 180 / np.pi
            hand_angle = (thumb_angle + pinky_angle) / 2
            
            # Print detected hand angle
            print(f"Hand Angle: {hand_angle}")

            # Logic for volume control based on hand movement
            if hand_angle > 15:  # Rightward gesture to increase volume
                current_vol = volume.GetMasterVolumeLevelScalar()
                new_vol = min(current_vol + 0.05, 1.0)  # Increase volume
                set_volume(new_vol)
            elif hand_angle < -15:  # Leftward gesture to decrease volume
                current_vol = volume.GetMasterVolumeLevelScalar()
                new_vol = max(current_vol - 0.05, 0.0)  # Decrease volume
                set_volume(new_vol)

            # Draw hand landmarks and gestures on the frame
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Show the frame
    cv2.imshow("Hand Gesture Volume Control", frame)
    
    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
