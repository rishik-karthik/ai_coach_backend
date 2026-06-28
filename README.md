---

```markdown
# 🏋️‍♂️ AI Real-time GYM Coach (Backend)

An intelligent, real-time computer vision application that tracks exercise form, counts repetitions, and provides live AI-driven audio and text feedback. Built to seamlessly integrate with a decoupled frontend, this backend leverages WebRTC for low-latency video streaming, MediaPipe for biomechanical landmarking, and Groq's LLMs for dynamic coaching.

---

## 🚀 The Elevator Pitch (For Interviews)
"I built a real-time AI fitness coach that analyzes user movements through their webcam. It processes video frames via WebRTC, maps human pose landmarks using MediaPipe, and evaluates exercise form (like squats). It then uses Groq's ultra-fast LLM API to generate personalized feedback, which is synthesized into audio using gTTS and streamed back to the user without interrupting their workout. During deployment, I successfully decoupled the architecture, hosting the static frontend on Netlify and the Python backend in a headless Linux cloud environment, engineering custom solutions for OpenGL graphics dependencies."

---

## 🛠️ Tech Stack & Dependencies

### Core Python Packages (`requirements.txt`)
* **`streamlit (1.54.0)`**: Serves as the backend framework and UI host for the WebRTC components.
* **`streamlit-webrtc (0.64.5)`**: Manages real-time bidirectional audio/video streams over UDP.
* **`mediapipe (>=0.10.30)`**: Google's ML framework for extracting 33 3D pose landmarks per frame.
* **`opencv-python-headless (4.10.0.84)`**: Server-optimized OpenCV for matrix/image manipulation (avoids crashing headless servers by skipping GUI dependencies).
* **`groq (>=0.12.0)`**: Injects dynamic AI coaching logic based on the user's workout data.
* **`gtts (2.5.3)`**: Google Text-to-Speech for synthesizing the Groq LLM text into audio instructions.
* **`pandas (2.2.3)`**: Handles structured data logging and metric calculations.

### System-Level Dependencies (`packages.txt`)
Because MediaPipe requires hardware acceleration for 3D rendering on headless Linux containers, these system graphics drivers are explicitly required via `apt-get`:
* `libgl1` (Core OpenGL)
* `libgles2` (OpenGL for Embedded Systems)
* `libegl1` (EGL interface linking rendering APIs to the native windowing system)

---

## 🧠 System Architecture & Data Flow

Understanding this flow is critical for system design discussions.

1. **Client Connection:** The user opens the Netlify frontend, which connects to this backend via a WebRTC offer/answer mechanism.
2. **Video Ingestion:** `streamlit-webrtc` captures the webcam stream in the browser and sends frames to the server via UDP (prioritizing speed over packet loss, essential for real-time video).
3. **Vision Processing (The Loop):** * A frame is converted into an OpenCV NumPy array.
   * MediaPipe `PoseLandmarker` processes the array to extract spatial coordinates (X, Y, Z, Visibility) of body joints.
4. **Biomechanical Logic:** The `SquatDetector` (or similar class) calculates joint angles (e.g., Hip-Knee-Ankle) using vector mathematics to determine the phase of the exercise (eccentric vs. concentric) and count valid repetitions.
5. **AI Inference:** If poor form is detected, the coordinates and context are sent to the **Groq API**, which returns a contextual coaching cue.
6. **Audio Synthesis:** `gTTS` converts the Groq text into an audio payload.
7. **Client Feedback:** The processed video frame (with drawn landmarks) and the generated audio are streamed back to the client's browser.

---

## 💡 Key Engineering Challenges & Solutions (Interview Talking Points)

### 1. Threading & State Management
**The Challenge:** WebRTC processes video frames in an entirely separate thread from the main Streamlit application. Normal Python variables cannot safely share state (like `rep_count`) between these threads.
**The Solution:** Implemented thread-safe logic and custom class instances (`VideoProcessorClass`) to maintain the state of the workout (reps, form status) across thousands of continuous frames without race conditions.

### 2. Headless Cloud Deployment & Dependency Hell
**The Challenge:** Deploying a computer vision app to a cloud server repeatedly crashed with `ImportError: libGL.so.1` and `OSError: libEGL.so.1`.
**The Solution:** Identified that standard `opencv-python` looks for desktop GUI modules that don't exist on cloud servers. Swapped to `opencv-python-headless`. Further diagnosed that MediaPipe's underlying C++ bindings required specific OS-level graphics drivers. Engineered a `packages.txt` pipeline to inject `libgl1`, `libgles2`, and `libegl1` directly into the Linux container before Python booted.

### 3. API Security in the Cloud
**The Challenge:** Securely integrating the Groq API key without exposing it in public repositories via local `.env` files.
**The Solution:** Stripped `python-dotenv` from the production environment and refactored the auth flow to fall back cleanly on `st.secrets`, allowing cloud platforms (Streamlit/Render) to inject the environment variables natively and securely.

---

## 💻 Local Setup & Installation

**1. Clone the repository**
```bash
git clone [https://github.com/rishik-karthik/ai_coach_backend.git](https://github.com/rishik-karthik/ai_coach_backend.git)
cd ai_coach_backend

```

**2. Create a virtual environment**

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

```

**3. Install dependencies**

```bash
pip install -r requirements.txt

```

**4. Set up environment variables**
Create a `.streamlit/secrets.toml` file in the root directory and add your Groq key:

```toml
GROQ_API_KEY = "your_api_key_here"

```

**5. Run the server**

```bash
python -m streamlit run main.py

```

---

## 🔮 Future Enhancements

* **Expanded Exercise Library:** Utilizing the existing architecture to track Push-Pull-Legs (PPL) specific movements like deadlifts and overhead presses.
* **Database Integration:** Linking user metrics to a MongoDB/Supabase instance to track progressive overload over time.

```
