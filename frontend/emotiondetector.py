import cv2
import pygame
from deepface import DeepFace

# Initialize pygame mixer for audio
pygame.mixer.init()

# Load the camera
cap = cv2.VideoCapture(0)  # 0 for default webcam

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

        # Play corresponding music
        if emotion == "happy":
            pygame.mixer.music.load("happymusic.mp3")
        elif emotion == "sad":
            pygame.mixer.music.load("sadmusic.mp3")
        else:
            continue  # Skip if the emotion is neither happy nor sad

        pygame.mixer.music.play()
    
    except Exception as e:
        print(f"Error: {e}")
    
    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
pygame.mixer.quit()
