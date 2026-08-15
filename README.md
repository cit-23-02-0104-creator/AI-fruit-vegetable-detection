# 🍎 Synthrium – AI Fruit & Vegetable Detection System

**Synthrium** is an AI-powered computer vision web application designed to automatically detect and identify fruits and vegetables from images or live camera input.

The system uses a **Roboflow-trained object detection model** together with a **FastAPI backend** and a responsive web-based interface. Users can upload an image or use their device camera, and the system detects available fruits and vegetables with confidence scores and bounding boxes.

---

## 🚀 Key Features

* 📷 **Live Camera Detection**

  * Detect fruits and vegetables using a device camera.

* 🖼️ **Image-Based Detection**

  * Upload an image and analyze its contents using the AI detection model.

* 🤖 **AI Object Detection**

  * Uses a Roboflow-trained computer vision model.

* 🎯 **Bounding Box Detection**

  * Displays detected objects with their corresponding locations.

* 📊 **Confidence Scores**

  * Shows the confidence level for each detected fruit or vegetable.

* 🔢 **Object Counting**

  * Automatically calculates the number of detected objects.

* 📱 **Responsive Web Interface**

  * Designed to work across desktop and mobile devices.

* 🔐 **HTTPS Camera Support**

  * Includes local HTTPS support for camera access on mobile devices.

* ⚡ **FastAPI Backend**

  * Provides lightweight REST API endpoints for image detection.

* ☁️ **Vercel Deployment Support**

  * Includes configuration for deploying the application using Vercel.

---

## 🧠 How It Works

The system follows a simple AI-based detection pipeline:

```text
User
  │
  ├── Upload Image
  │
  └── Live Camera
          │
          ▼
   Web Interface
          │
          ▼
     FastAPI Backend
          │
          ▼
   Image Pre-processing
          │
          ▼
    Roboflow AI Model
          │
          ▼
   Object Detection
          │
          ▼
 Class + Confidence + Bounding Box
          │
          ▼
     Detection Results
```

---

## 🛠️ Technology Stack

| Technology     | Purpose                                   |
| -------------- | ----------------------------------------- |
| **Python**     | Backend development                       |
| **FastAPI**    | REST API and web backend                  |
| **Roboflow**   | AI object detection model                 |
| **OpenCV**     | Image processing                          |
| **NumPy**      | Numerical and image processing operations |
| **Pillow**     | Image handling                            |
| **HTML5**      | Frontend structure                        |
| **CSS3**       | User interface styling                    |
| **JavaScript** | Camera and frontend interaction           |
| **Uvicorn**    | ASGI application server                   |
| **Vercel**     | Deployment support                        |

---

## 📁 Project Structure

```text
synthrium-fruit-vegetable-detector/
│
├── app.py
│
├── main.py
│
├── requirements.txt
│
├── vercel.json
│
├── Logo.png
│
├── static/
│   ├── index.html
│   └── Logo.png
│
└── certs/
    ├── cert.pem
    └── key.pem
```

### File Description

**`main.py`**
Main FastAPI application. Handles image uploads, AI predictions, API endpoints, local HTTPS support, and communication with the Roboflow model.

**`app.py`**
Standalone image detection script using Roboflow and OpenCV.

**`static/index.html`**
Frontend interface containing the user interface, image upload functionality, camera interface, and detection result display.

**`requirements.txt`**
Contains the Python dependencies required to run the project.

**`vercel.json`**
Configuration file for Vercel deployment.

**`Logo.png`**
Application branding/logo assets.

**`certs/**`**
Local HTTPS certificate files used for secure camera access during local development.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/synthrium-fruit-vegetable-detector.git
```

Navigate into the project:

```bash
cd synthrium-fruit-vegetable-detector
```

---

### 2. Create a Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

If PowerShell blocks activation, you can use:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then:

```bash
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Roboflow Configuration

The application uses a Roboflow object detection model.

Before running the project, configure your Roboflow credentials securely using an environment variable.

### Recommended

Create a `.env` file:

```env
ROBOFLOW_API_KEY=YOUR_ROBOFLOW_API_KEY
```

Then configure the application to read the API key from the environment.

> **Security Note:** Never commit your real Roboflow API key, passwords, private certificates, or other credentials to GitHub.

If an API key has previously been committed to a public repository, it should be revoked and replaced.

---

## ▶️ Running the Application

Start the FastAPI application with:

```bash
python main.py
```

The application will start the local server.

For API development, you can also use:

```bash
uvicorn main:app --reload
```

Once the server is running, open the displayed local address in a web browser.

---

## 🔌 API Endpoints

### `GET /`

Returns the main Synthrium web interface.

### `POST /api/detect`

Accepts an uploaded image and performs fruit and vegetable detection.

Example request:

```text
POST /api/detect
Content-Type: multipart/form-data
```

Response example:

```json
{
  "image_width": 1280,
  "image_height": 720,
  "detections": [
    {
      "class": "Apple",
      "confidence": 0.95,
      "x1": 120,
      "y1": 80,
      "x2": 350,
      "y2": 300,
      "width": 230,
      "height": 220
    }
  ],
  "count": 1
}
```

### `POST /api/detect-frame`

Provides detection functionality for camera frames.

---

## 📷 Detection Process

The application performs the following steps:

1. User selects an image or opens the camera.
2. The frontend sends the image/frame to the FastAPI backend.
3. The backend temporarily processes the image.
4. The Roboflow model performs object detection.
5. Detected objects are extracted from the prediction.
6. Class names and confidence values are returned.
7. Bounding boxes are displayed in the web interface.
8. The total number of detected objects is shown to the user.

---

## 🎯 Detection Output

For every detected object, the system can provide:

* Object/class name
* Confidence score
* Bounding box coordinates
* Bounding box width
* Bounding box height
* Total number of detected objects

---

## 📱 Camera Support

Synthrium supports camera-based detection through the browser.

Because modern browsers generally require a secure context for camera access, the application includes local HTTPS support.

When running locally, the application can generate/use a self-signed certificate.

> Browsers may display a security warning for locally generated certificates. This is expected during local development.

---

## ☁️ Deployment

The project contains a `vercel.json` configuration file for Vercel deployment.

Typical deployment flow:

```text
GitHub Repository
        │
        ▼
     Vercel
        │
        ▼
   FastAPI Backend
        │
        ▼
   Roboflow Model
```

For production deployment, configure the Roboflow API key through the deployment platform's environment-variable settings instead of storing it inside the source code.

---

## 🔒 Security Considerations

This project uses external AI services and therefore API credentials must be handled securely.

### Do not commit:

```text
.env
API keys
private keys
passwords
secret credentials
```

Add sensitive files to `.gitignore`:

```gitignore
# Python
__pycache__/
*.py[cod]

# Virtual Environment
venv/
.venv/

# Environment variables
.env
.env.*

# IDE
.vscode/
.idea/

# Generated files
output.jpg

# Secrets
*.pem
*.key
```

---

## 📌 Current Capabilities

| Feature              | Status |
| -------------------- | ------ |
| Image Upload         | ✅      |
| AI Object Detection  | ✅      |
| Fruit Detection      | ✅      |
| Vegetable Detection  | ✅      |
| Bounding Boxes       | ✅      |
| Confidence Scores    | ✅      |
| Object Counting      | ✅      |
| Live Camera          | ✅      |
| FastAPI Backend      | ✅      |
| Responsive UI        | ✅      |
| Local HTTPS          | ✅      |
| Vercel Configuration | ✅      |

---

## 🔮 Future Improvements

Potential future enhancements include:

* 🍌 Support for a larger number of fruit and vegetable classes
* 📈 Detection history and analytics
* 🗄️ Database integration
* 👤 User authentication
* 📊 Detection statistics dashboard
* 🌐 Multi-language support
* 📱 Progressive Web App (PWA) support
* ⚡ Faster real-time detection
* 🧠 Improved model accuracy
* ☁️ Production-grade cloud deployment

---

## 🎓 Project Purpose

Synthrium demonstrates how **Artificial Intelligence, Computer Vision, REST APIs, and modern web technologies** can be combined to create a practical image recognition application.

The project can be used as a foundation for applications involving:

* Automated food recognition
* Smart inventory systems
* Agricultural monitoring
* Retail automation
* Food classification
* Computer vision research
* AI-based educational projects

---

## 👩‍💻 Development

Developed as an AI-based computer vision application using Python, FastAPI, Roboflow, OpenCV, HTML, CSS, and JavaScript.

---

## 📄 License

This project is intended for educational and research purposes.

A suitable open-source license such as the **MIT License** can be added if the project is intended for public reuse.

---

## ⭐ Acknowledgements

* **Roboflow** – Computer vision model training and inference
* **FastAPI** – Backend API framework
* **OpenCV** – Image processing
* **Uvicorn** – Python ASGI server

---

### ⭐ If you find this project useful, consider giving the repository a star!
