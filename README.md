# 🎨 AirCanvas

AirCanvas is a computer vision project that allows you to draw on your screen in real-time simply by pinching your fingers together in the air. 

Built in 45-60 minutes, this project serves as a practical bridge between software-defined tracking and traditional hardware input concepts.

## 🧠 The Hardware Concept: Software as an ADC
This project replicates how hardware reads X/Y positions from a resistive touchscreen via an Analog-to-Digital Converter (ADC). 

Instead of measuring voltage drops across a physical screen, AirCanvas measures the Euclidean distance between your thumb and index finger. The "pinch threshold" in the code acts as our digital trigger—identical to an ADC sampling a voltage spike to register a physical touch.

## ✨ Features
* **Real-time Tracking:** Webcam feed runs smoothly with a mirror-image flip for natural drawing.
* **Pinch-to-Draw:** Drawing only occurs when the thumb and index fingers are pinched together.
* **Release-to-Stop:** Separating fingers immediately halts the drawing stroke.
* **Color Selection:** Hover your pinched fingers over the on-screen UI boxes to swap between Blue and Red.
* **Persistent Canvas:** Strokes are stored on an independent canvas array, ensuring the screen doesn't clear when you move.

## 🛠 Tech Stack
* **Python 3.x**
* **MediaPipe Hands:** For 3D hand landmark detection.
* **OpenCV (cv2):** For webcam processing, drawing primitives, and bitwise image blending.
* **NumPy:** For maintaining the background canvas state.

## 🚀 Quick Start

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR_USERNAME/AirCanvas.git](https://github.com/YOUR_USERNAME/AirCanvas.git)
cd AirCanvas