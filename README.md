# Number-Plate-Detection
Sure! Here's a professional and clear `README.md` for your Indian Number Plate Detection project, including installation, usage, and dataset notes:

---

```markdown
# 🇮🇳 Indian Number Plate Detection and Recognition

This project performs **number plate detection and recognition** for Indian vehicles using computer vision and OCR techniques. It focuses on identifying number plates in video frames, extracting license numbers, and formatting them to match Indian vehicle registration rules.

## 📌 Features

- Vehicle and license plate detection
- OCR-based number plate reading using EasyOCR
- Format validation for Indian number plates (`AA NN AA NNNN`)
- Bounding box interpolation for smoother tracking
- CSV logging of frame-wise detection results

---

## 📁 Project Structure

```

project/
│
├── main.py                    # Main pipeline script
├── util.py                    # Utilities: OCR, validation, formatting
├── interpolate.py             # Bounding box interpolation script
├── test.csv                   # Raw detection output (before interpolation)
├── test\_interpolated.csv      # Final output after interpolation
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation

````

---

## 🔧 Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/indian-number-plate-detection.git
cd indian-number-plate-detection
````

2. **Install dependencies**

We recommend using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Dependencies include:

* `easyocr`
* `opencv-python`
* `numpy`
* `scipy`

---

## 🏁 Usage

### 1. Run Detection

Use your video input to detect cars and plates:

```bash
python main.py --video input.mp4
```

This will:

* Detect vehicles and plates
* Run OCR
* Output results to `test.csv`

### 2. Interpolate Missing Frames

To fill gaps and ensure smoother tracking:

```bash
python interpolate.py
```

This generates `test_interpolated.csv` with interpolated values.

---

## 🧠 Indian Number Plate Format

The recognized format is validated and corrected based on:

```
AA NN AA NNNN
```

Where:

* `A` = Alphabet
* `N` = Number

Example: `MH12AB1234`

OCR errors (e.g., `O` → `0`, `I` → `1`) are corrected using a custom mapping.

---

## 📦 Sample Datasets

You can test the pipeline using:

* Kaggle Dataset: [Car Number Plate Video](https://www.kaggle.com/datasets/nimishshandilya/car-number-plate-video)
* YouTube: [Delhi Traffic Footage](https://www.youtube.com/watch?v=68DN6V7zPDk)

---

## 📊 Output Format

CSV Columns:

* `frame_nmr`: Frame number
* `car_id`: Vehicle ID
* `car_bbox`: Bounding box for car `[x1 y1 x2 y2]`
* `license_plate_bbox`: Bounding box for plate `[x1 y1 x2 y2]`
* `license_plate_bbox_score`: Confidence score for plate detection
* `license_number`: Detected license number
* `license_number_score`: OCR confidence score

---

## 🙌 Acknowledgements

* [EasyOCR](https://github.com/JaidedAI/EasyOCR)
* [OpenCV](https://opencv.org/)
* Kaggle/YouTube for publicly available datasets

---

## 📜 License

MIT License. Feel free to use, modify, and contribute.

---

## 🤝 Contributing

Pull requests are welcome. Please ensure consistency with the Indian format validation and provide test cases with new code.

```

---

Let me know if you want the README tailored for a Jupyter notebook version or want to include demo visuals/gifs for your GitHub repo!
```
