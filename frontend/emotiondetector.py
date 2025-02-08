import cv2
import pygame
from deepface import DeepFace
import time
from collections import Counter

# Initialize pygame mixer for audio
pygame.mixer.init()

# Load the camera
cap = cv2.VideoCapture(0)  # 0 for default webcam

# Initialize variables
start_time = time.time()
emotion_list = []  # To store detected emotions

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Display the video feed
    cv2.imshow("Emotion Detection", frame)
    
    # Save a frame as an image for DeepFace analysis
    cv2.imwrite("temp_frame.jpg", frame)
    
    try:
        # Analyze the emotion in the frame
        analysis = DeepFace.analyze(img_path="temp_frame.jpg", actions=['emotion'], enforce_detection=False)
        
        # Extract emotion
        emotion = analysis[0]['dominant_emotion']
        print(f"Detected Emotion: {emotion}")
        
        # Add detected emotion to the list
        emotion_list.append(emotion)

    except Exception as e:
        print(f"Error: {e}")
    
    # Check if 10 seconds have passed
    if time.time() - start_time > 10:
        # Stop the loop after 10 seconds
        break

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Determine the most common emotion detected in the last 10 seconds
if emotion_list:
    most_common_emotion = Counter(emotion_list).most_common(1)[0][0]
    print(f"Most Detected Emotion: {most_common_emotion}")

    # Play the corresponding music based on the most frequent emotion
    if most_common_emotion == "happy":
        pygame.mixer.music.load("happy.mp3")
    elif most_common_emotion == "sad":
        pygame.mixer.music.load("happy.mp3")
    elif most_common_emotion == "neutral":
        pygame.mixer.music.load("neutralmusic.mp3")
    elif most_common_emotion == "fear":
        pygame.mixer.music.load("fearmusic.mp3")
    elif most_common_emotion == "angry":
        pygame.mixer.music.load("angrymusic.mp3")
    elif most_common_emotion == "surprise":
        pygame.mixer.music.load("surprisemusic.mp3")
    else:
        print("No dominant happy or sad emotion detected.")
        pygame.mixer.music.stop()  # Stop music if neither happy nor sad

    print("Music will be loaded")
    pygame.mixer.music.play()
    print("Music SHOULD be loaded")

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
