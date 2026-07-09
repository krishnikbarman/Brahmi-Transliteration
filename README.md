# 🏛️ Brahmi Script Recognition & Devanagari Transliteration

A Deep Learning based Computer Vision system for recognizing ancient Brahmi script characters and transliterating them into modern Devanagari using TensorFlow, MobileNetV2, and Streamlit.

---

## 📖 Overview

Brahmi is one of the oldest writing systems of the Indian subcontinent and the ancestor of many modern Indian scripts. Reading Brahmi inscriptions requires specialized knowledge, making digitization and preservation difficult.

This project aims to automate the recognition of Brahmi script characters and transliterate them into their corresponding Devanagari characters using Deep Learning.

---

## 🎯 Objectives

- Recognize Brahmi characters from images.
- Convert recognized characters into Devanagari.
- Build a reusable OCR pipeline.
- Provide a simple Streamlit interface for users.

---

## ✨ Features

- 416 Brahmi character classes
- Custom dataset preprocessing
- Dataset balancing and augmentation
- MobileNetV2 Transfer Learning
- Automatic image preprocessing
- Character prediction with confidence score
- Streamlit web application
- JSON-based character mapping

---

## 📂 Dataset

| Property | Value |
|----------|-------|
| Classes | 416 |
| Images | 6240 |
| Images per class | 15 |
| Image Size | 224 × 224 |

### Dataset Preparation

- Dataset Cleaning
- Class Balancing
- Image Augmentation
- Image Preprocessing
- Normalization

---

## 🧠 Model

Transfer Learning using **MobileNetV2**

Architecture:

```
Input Image
      │
      ▼
Preprocessing
      │
      ▼
MobileNetV2 Feature Extractor
      │
      ▼
Dense Layers
      │
      ▼
416 Character Classes
      │
      ▼
Devanagari Output
```

---

## 📊 Results

| Metric | Value |
|---------|-------|
| Validation Accuracy | **72.44%** |
| Validation Loss | **1.0711** |

The model performs well on dataset images and augmented samples. Tests on manually drawn characters revealed domain adaptation challenges, providing scope for future improvements.

---

## 🛠️ Tech Stack

- Python
- TensorFlow / Keras
- MobileNetV2
- NumPy
- OpenCV
- Pillow
- Streamlit
- Matplotlib

---

## 📁 Project Structure

```
Brahmi-Transliteration
│
├── app.py
├── README.md
├── requirements.txt
├── LICENSE
│
├── configs/
├── fonts/
├── mapping/
├── model/
├── notebooks/
├── scripts/
└── results/
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/krishnikbarman/Brahmi-Transliteration.git

cd Brahmi-Transliteration
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## 🖥️ Usage

1. Launch the Streamlit application.
2. Upload a Brahmi character image.
3. The model preprocesses the image.
4. The trained MobileNetV2 predicts the character.
5. The corresponding Devanagari character is displayed along with the confidence score.

---

## 🔮 Future Work

- Sentence-level transliteration
- Handwritten Brahmi recognition
- Transformer-based architectures
- Domain adaptation for user-drawn inputs
- Mobile deployment
- Ancient inscription recognition

---

## 👨‍💻 Author

**Krishnik Barman**

B.Tech Computer Science & Engineering

Interested in Artificial Intelligence, Deep Learning, Computer Vision, and Ancient Script Digitization.

---

## ⭐ Acknowledgements

This project was developed as part of research and experimentation in Deep Learning and Ancient Indian Script Recognition using Transfer Learning.
