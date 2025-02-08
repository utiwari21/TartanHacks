import cv2
import mediapipe as mp
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from math import radians, degrees
import numpy as np
from comtypes import CLSCTX_ALL

# Initialize MediaPipe Hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Access system audio
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Set up OpenCV to capture webcam feed
cap = cv2.VideoCapture(0)

def set_volume(vol):
    """Ensure the volume is set within range (0 to 1)."""
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
            # Get key points for gesture recognition (wrist, thumb tip, and pinky tip)
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
            
            # Calculate the angle of rotation based on wrist and fingertips
            thumb_angle = np.arctan2(thumb_tip.y - wrist.y, thumb_tip.x - wrist.x) * 180 / np.pi
            pinky_angle = np.arctan2(pinky_tip.y - wrist.y, pinky_tip.x - wrist.x) * 180 / np.pi
            hand_angle = (thumb_angle + pinky_angle) / 2
            
            # Print detected hand angle
            print(f"Hand Angle: {hand_angle}")

            # Volume control logic
            current_vol = volume.GetMasterVolumeLevelScalar()
            if hand_angle < 15:  # Rightward gesture → Increase volume
                new_vol = min(current_vol + 500.0, 1.0)
                set_volume(new_vol)
                print(f"Increasing volume to {new_vol:.2f}")
            elif hand_angle > -15:  # Leftward gesture → Decrease volume
                new_vol = max(current_vol - 0.05, 0.0)
                set_volume(new_vol)
                print(f"Decreasing volume to {new_vol:.2f}")

            # Draw hand landmarks on the frame
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Show the frame
    cv2.imshow("Hand Gesture Volume Control", frame)
    
    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
