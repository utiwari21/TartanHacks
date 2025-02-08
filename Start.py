import cv2
from deepface import DeepFace
import pygame

# Initialize pygame for music playback
pygame.mixer.init()

# Define music files (change to your own MP3s)
happy_music = "happy.mp3"   # Add a real path to an upbeat song
sad_music = "sad.mp3"       # Add a real path to a calm/sad song

# Start video capture
cap = cv2.VideoCapture(0)

# Variable to store the last emotion detected
last_emotion = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Show live video feed
    cv2.imshow("Face Emotion Music Player", frame)

    try:
        # Analyze the frame for facial expression
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = analysis[0]['dominant_emotion']  # Get the detected emotion

        print(f"Detected Emotion: {emotion}")

        # Play happy music if user is happy, sad music otherwise
        if emotion == 'happy' and last_emotion != 'happy':
            pygame.mixer.music.load(happy_music)
            pygame.mixer.music.play()
            last_emotion = 'happy'
        elif emotion in ['neutral', 'sad'] and last_emotion not in ['neutral', 'sad']:
            pygame.mixer.music.load(sad_music)
            pygame.mixer.music.play()
            last_emotion = 'neutral'

    except Exception as e:
        print("Face not detected:", str(e))

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
