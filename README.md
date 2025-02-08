# TartanHacks
🎯 How to Run the Program
Place two MP3 files in the same folder and rename them to happy.mp3 and sad.mp3.
You can download royalty-free songs from sites like Pixabay or Free Music Archive.
Run the script:
python face_music_player.py

Smile to play happy music 😃🎵
Stay neutral or frown to play calm music 😐🎶
Press 'Q' to quit the program.

📌 Explanation of Code
🔹 Face Detection & Emotion Recognition
Uses DeepFace (DeepFace.analyze()) to detect emotions in real-time.
Supports multiple emotions: happy, sad, neutral, angry, surprised, etc.
Automatically selects the dominant emotion from the frame.
🔹 Music Playback
Uses Pygame’s mixer module to load and play MP3 files.
Checks the last played emotion to avoid restarting the same song.
🔹 Real-Time Processing
Uses OpenCV (cv2.VideoCapture(0)) to access the webcam.
Continuously analyzes each frame for emotion updates.
