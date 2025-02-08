import React, { useState, useRef, useEffect } from "react";
import { View, Text, TouchableOpacity } from "react-native";
import { Camera, useCameraDevices } from "react-native-vision-camera";
import * as FileSystem from "expo-file-system";
import { Audio } from "expo-av";

const EmotionMusicApp = () => {
    const [emotion, setEmotion] = useState(null);
    const [sound, setSound] = useState(null);
    const devices = useCameraDevices();
    const camera = useRef(null);
    const device = devices.front; // Use front camera

    useEffect(() => {
        (async () => {
            const permission = await Camera.requestCameraPermission();
            if (permission !== "authorized") {
                alert("Camera access denied!");
            }
        })();
    }, []);

    const captureAndSend = async () => {
        if (camera.current) {
            const photo = await camera.current.takePhoto({});
            const imagePath = photo.path;

            // Convert image to Base64
            const base64Image = await FileSystem.readAsStringAsync(imagePath, {
                encoding: FileSystem.EncodingType.Base64,
            });

            // Send image to backend
            const response = await fetch("http://YOUR_IP:5000/detect-emotion", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ image: base64Image }),
            });

            const result = await response.json();
            setEmotion(result.emotion); // Update detected emotion
            playMusic(result.emotion);
        }
    };

    const playMusic = async (emotion) => {
        let musicFile;
        if (emotion === "happy") {
            musicFile = require("./assets/happy.mp3");
        } else {
            musicFile = require("./assets/sad.mp3");
        }

        if (sound) {
            await sound.unloadAsync();
        }

        const { sound: newSound } = await Audio.Sound.createAsync(musicFile);
        setSound(newSound);
        await newSound.playAsync();
    };

    return (
        <View style={{ flex: 1 }}>
            {device ? (
                <Camera ref={camera} style={{ flex: 1 }} device={device} isActive={true} photo={true} />
            ) : (
                <Text>No Camera Found</Text>
            )}
            <TouchableOpacity onPress={captureAndSend} style={{ padding: 20, backgroundColor: "blue" }}>
                <Text style={{ color: "white" }}>Capture & Detect Emotion</Text>
            </TouchableOpacity>
            {emotion && <Text>Detected Emotion: {emotion}</Text>}
        </View>
    );
};

export default EmotionMusicApp;
