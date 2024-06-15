# Passport Scraper

This project uses OpenCV and Tesseract OCR to extract and annotate textual information from Indian passport images. The script processes the image to enhance text recognition accuracy and extracts key details such as passport number, full name, surname, nationality, country code, date of birth, date of issue, date of expiry, gender, place of birth, and place of issue.

## Features:
- **Image Preprocessing**: Converts the image to grayscale, sharpens it, and applies denoising to improve text detection accuracy.
- **Text Detection and Extraction**: Utilizes Tesseract OCR to detect and extract text from the preprocessed image.
- **Information Parsing**: Uses regular expressions to identify and extract specific information such as passport number, dates, and names from the detected text.
- **Error Handling**: Incorporates comprehensive error handling to manage and report potential issues during text detection and parsing.
- **Annotated Output**: Draws rectangles around detected text and annotates the image with the recognized text for visual verification.

## Installation
1. **Install Dependencies**:
    - Ensure you have OpenCV and Tesseract installed.
    - Install required Python packages using `pip`:
      ```bash
      pip install opencv-python pytesseract numpy
      ```

2. **Tesseract Installation**:
    - Download and install Tesseract OCR from [here](https://github.com/tesseract-ocr/tesseract).

## Usage
1. **Run the Script**:
    - Place your passport image in the specified path.
    - Modify the `image_path` variable to point to your image.
    - Run the script:
      ```python
      python extract_passport_info.py
      ```

2. **Output**:
    - The script will print the extracted passport information in JSON format.

## Example
```python
image_path = "path/to/your/passport/image.jpg"
passport_info_json = extract_passport_info(image_path)
print(passport_info_json)
