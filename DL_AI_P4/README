# 👁️ AI Vision Recognition System – Image & Text Recognition Pipeline

A production-style **Computer Vision pipeline** that performs **Optical Character Recognition (OCR)** and **basic Object Detection** using Python and OpenCV. The system processes an input image, applies multiple preprocessing techniques, extracts text using Tesseract OCR, detects objects using contour analysis, and generates annotated outputs and structured reports.

This project was developed as **Project 4** during my **AI Internship at DecodeLabs**.

---

## 🚀 Features

- 📷 Image loading and validation
- 🖼️ Automatic image resizing
- 🎨 Image preprocessing pipeline
  - Grayscale conversion
  - Noise reduction
  - CLAHE enhancement
  - Gaussian Blur
  - Adaptive Thresholding
  - Morphological Closing
- 🔍 Multi-stage OCR using Tesseract
- 📍 Region-based OCR for improved text recognition
- 📦 Contour-based object detection
- 🟩 Bounding box visualization
- 📊 OCR confidence scoring
- 📄 Automatic JSON report generation
- 💾 Save annotated images and recognized text
- 🏗️ Modular and production-ready project architecture

---

# 🏗️ Project Architecture

```
                Input Image
                     │
                     ▼
             Image Validation
                     │
                     ▼
              Image Preprocessing
                     │
     ┌───────────────┴───────────────┐
     ▼                               ▼
 Optical Character Recognition   Object Detection
          (OCR)                (Contour Analysis)
     ▼                               ▼
 Text Extraction             Bounding Boxes
     └───────────────┬───────────────┘
                     ▼
          Report Generation
                     ▼
            Save Output Files
```

---

# 📂 Project Structure

```
AI-Vision-Recognition-System/
│
├── images/
│     ├── sample1.jpg
│     └── logo.jpeg
│
├── output/
│
├── image_loader.py
├── preprocessing.py
├── ocr_engine.py
├── object_detector.py
├── utils.py
├── main.py
├── requirements.txt
└── README.md
```

---

# 🛠️ Technologies Used

- Python 3
- OpenCV
- NumPy
- Tesseract OCR
- pytesseract
- JSON

---

# 📋 How It Works

## 1️⃣ Load Image

The user provides an input image.

Supported formats include:

- JPG
- JPEG
- PNG
- BMP

---

## 2️⃣ Image Preprocessing

The image is enhanced before OCR using:

- Resize
- Grayscale Conversion
- Noise Reduction
- CLAHE Contrast Enhancement
- Gaussian Blur
- Adaptive Thresholding
- Morphological Closing

These preprocessing steps improve OCR accuracy.

---

## 3️⃣ Optical Character Recognition (OCR)

The system performs OCR on multiple image variants and automatically selects the best result based on confidence.

Recognized text includes:

- Characters
- Words
- Logos
- Printed text

The system also displays an OCR confidence score.

---

## 4️⃣ Object Detection

Objects are detected using contour analysis.

Detected regions are highlighted with bounding boxes.

---

## 5️⃣ Report Generation

The pipeline automatically generates:

- Annotated image
- Processed image
- Recognized text file
- JSON report

---

# 📊 Example Output

```
=========================================
AI Vision Recognition Report
=========================================

Image Size: 1024 × 1024

Objects Detected: 3

Text Blocks: 2

OCR Confidence: 95.00 %

Processing Time: 15.01 sec

Status: SUCCESS

=========================================

OCR RESULTS

VOR
VOICE OF REHMAT

=========================================

Detected Objects

Polygon
Polygon
Polygon
```

---

# 📁 Generated Output

```
output/

original_*.png

processed_*.png

annotated_*.png

recognized_text_*.txt

report_*.json
```

---

# ▶️ Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/AI-Vision-Recognition-System.git
```

Navigate to the project directory:

```bash
cd AI-Vision-Recognition-System
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# ⚙️ Install Tesseract OCR

## Windows

Download and install Tesseract OCR:

https://github.com/UB-Mannheim/tesseract/wiki

or

https://github.com/tesseract-ocr/tesseract

Then update the path in `ocr_engine.py`:

```python
pytesseract.pytesseract.tesseract_cmd = \
r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

# ▶️ Run the Project

```bash
python main.py images/logo.jpeg --output output
```

---

# 📈 Project Workflow

1. Load image
2. Validate input
3. Resize image
4. Apply preprocessing
5. Perform OCR on multiple image variants
6. Detect objects using contours
7. Draw bounding boxes
8. Generate OCR report
9. Save results

---

# 📚 Learning Outcomes

This project demonstrates:

- Computer Vision Fundamentals
- Image Processing
- Optical Character Recognition (OCR)
- Image Enhancement Techniques
- Object Detection
- Contour Analysis
- Report Generation
- Modular Python Development
- Production-Style AI Pipeline Design

---

# 🔮 Future Improvements

- EasyOCR integration as a fallback OCR engine
- YOLOv8 object detection
- Face detection support
- QR Code and Barcode recognition
- PDF document OCR
- Batch image processing
- OCR confidence visualization
- Streamlit web application
- Real-time webcam text recognition

---

# 👨‍💻 Author

**Rehmat Ali**

AI Intern | Computer Engineering Student

GitHub: https://github.com/rehmatali609

LinkedIn:https://www.linkedin.com/in/rehmat-ali-49a09932b

---

# 📄 License

This project is intended for educational and learning purposes as part of the **DecodeLabs Artificial Intelligence Internship Program**.
