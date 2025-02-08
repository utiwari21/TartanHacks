# Music by Mood 🎵🙂

This project detects emotions using a camera and plays music accordingly. 
The user also has the ability to change the volume through their hand gestures.

## 🚀 How to Run

### Backend (Flask)
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend (React Native)
```bash
cd frontend
npm install
npx react-native run-android  # or npx react-native run-ios for iOS
```

### Configuration
- Replace `http://YOUR_IP:5000/detect-emotion` in `App.js` with your actual backend IP address.
- Add `happy.mp3` and `sad.mp3` in the `frontend/assets` folder.
