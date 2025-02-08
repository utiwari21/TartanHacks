import React, { useEffect, useRef, useState } from "react";
import { Camera } from "lucide-react";

const AppHome = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const wsRef = useRef(null);
  const [emotion, setEmotion] = useState(null);
  const [handAngle, setHandAngle] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Start webcam
    const startWebcam = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
        });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error("Error accessing webcam:", err);
      }
    };

    // Connect WebSocket
    const connectWebSocket = () => {
      wsRef.current = new WebSocket("ws://localhost:8000/ws");

      wsRef.current.onopen = () => {
        setIsConnected(true);
        console.log("WebSocket Connected");
      };

      wsRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.emotion) setEmotion(data.emotion);
        if (data.hand_data) setHandAngle(data.hand_data.angle);
      };

      wsRef.current.onclose = () => {
        setIsConnected(false);
        console.log("WebSocket Disconnected");
        // Attempt to reconnect after 2 seconds
        setTimeout(connectWebSocket, 2000);
      };
    };

    startWebcam();
    connectWebSocket();

    // Cleanup
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  // Send frames to backend
  useEffect(() => {
    const sendFrame = () => {
      if (
        wsRef.current?.readyState === WebSocket.OPEN &&
        videoRef.current &&
        canvasRef.current
      ) {
        const context = canvasRef.current.getContext("2d");
        context.drawImage(
          videoRef.current,
          0,
          0,
          canvasRef.current.width,
          canvasRef.current.height
        );
        const frame = canvasRef.current.toDataURL("image/jpeg");
        wsRef.current.send(frame);
      }
    };

    const interval = setInterval(sendFrame, 100); // Send frame every 100ms

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex items-center mb-4">
            <Camera className="w-6 h-6 text-blue-500 mr-2" />
            <h1 className="text-2xl font-bold">Emotion & Volume Control</h1>
          </div>

          <div className="space-y-4">
            <div className="relative aspect-video bg-black rounded-lg overflow-hidden">
              <video
                ref={videoRef}
                autoPlay
                playsInline
                className="w-full h-full object-cover"
              />
              <canvas
                ref={canvasRef}
                width={640}
                height={480}
                className="hidden"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-gray-50 rounded-lg">
                <h2 className="font-semibold mb-2">Detected Emotion</h2>
                <p className="text-xl">{emotion || "No emotion detected"}</p>
              </div>

              <div className="p-4 bg-gray-50 rounded-lg">
                <h2 className="font-semibold mb-2">Hand Angle</h2>
                <p className="text-xl">
                  {handAngle ? `${handAngle.toFixed(2)}°` : "No hand detected"}
                </p>
              </div>
            </div>

            <div className="p-4 bg-gray-50 rounded-lg">
              <h2 className="font-semibold mb-2">Connection Status</h2>
              <div className="flex items-center">
                <div
                  className={`w-3 h-3 rounded-full mr-2 ${
                    isConnected ? "bg-green-500" : "bg-red-500"
                  }`}
                />
                <p>{isConnected ? "Connected" : "Disconnected"}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AppHome;
