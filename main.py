import cv2
import pytesseract
import numpy as np
import re
import json

def extract_passport_info(image_path):
    try:
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Image not found or unable to load.")
        
        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply sharpening filter to the image
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        sharpened = cv2.filter2D(image, -1, kernel)
        
        # Apply denoising to the sharpened image
        denoised_image = cv2.fastNlMeansDenoisingColored(sharpened, None, 10, 10, 7, 21)
        
        # Convert the denoised image to grayscale
        gray_denoised = cv2.cvtColor(denoised_image, cv2.COLOR_BGR2GRAY)
        
        # Detect text in the image using pytesseract
        detection = pytesseract.image_to_data(denoised_image, output_type=pytesseract.Output.DICT)
        
        detected_texts = []

        # Loop over each detected text box
        for i in range(len(detection['text'])):
            try:
                # Consider texts with confidence more than 60%
                if detection['text'][i] and int(detection['conf'][i]) > 60:  
                    (x, y, w, h) = (detection['left'][i], detection['top'][i], detection['width'][i], detection['height'][i])
                    # Draw a rectangle around the text
                    cv2.rectangle(denoised_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # Annotate the image with the detected text
                    cv2.putText(denoised_image, detection['text'][i], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    detected_texts.append(detection['text'][i])
            except Exception as e:
                print(f"Error processing detection index {i}: {e}")
        
        # Define regex patterns for extracting specific information
        s_pattern = r'\b[M|F]\b'
        pno_pattern = r'\b[A-Z]\d{7}\b'
        d_pattern = r'\b((0[1-9]|[12]\d|30)[-/](0[1-9]|1[0-2])[-/]\d{4}|\d{4}[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|30))\b'
        n_pattern = r'\bINDIAN\b'
        c_pattern = r'\bIND\b'
        words_pattern = r'\b(?!(?:INDIA|INDIAN|GOVERNMENT OF INDIA|GOVERNMENT|REPUBLIC|OF)\b)\b[A-Z]{4,}\b'
        
        # Initialize variables to store extracted information
        PASSNO = None
        SURNAME = None
        FULLNAME = None
        NATIONALITY = None
        C_CODE = None
        DOB = None
        DOI = None
        DOE = None
        GENDER = None
        POB = None
        POE = None
        words = []
        dates = []
        
        # Extract information using regex patterns
        for i in detected_texts:
            try:
                # Extract gender
                s_matches = re.findall(s_pattern, i)
                if s_matches:
                    GENDER = s_matches[0]

                # Extract passport number
                pno_matches = re.findall(pno_pattern, i)
                if pno_matches:
                    PASSNO = pno_matches[0]

                # Extract nationality
                n_matches = re.findall(n_pattern, i)
                if n_matches:
                    NATIONALITY = n_matches[0]
                
                # Extract country code
                c_matches = re.findall(c_pattern, i)
                if c_matches:
                    C_CODE = c_matches[0]

                # Extract words
                words_matches = re.findall(words_pattern, i)
                if words_matches:
                    words.extend(words_matches)

                # Extract dates
                d_matches = re.findall(d_pattern, i)
                if d_matches:
                    dates.extend(d_matches)
            except Exception as e:
                print(f"Error processing text '{i}': {e}")

        # Assign dates to respective variables
        if len(dates) > 0:
            DOB = dates[0]
        if len(dates) > 1:
            DOI = dates[1]
        if len(dates) > 2:
            DOE = dates[2]

        # Assign remaining text elements to respective variables
        if len(words) > 0:
            SURNAME = words[0]
        if len(words) >= 3:
            POE = words[-1]
            POB = words[-3] + ", " + words[-2]
        if len(words) >= 5:
            balanced_list = words[1:len(words)-3]
            if len(balanced_list) >= 2:
                FULLNAME = balanced_list[0] + " " + balanced_list[1]

        # Ensure DOB, DOI, DOE are in correct format
        DOB = DOB[0] if DOB and isinstance(DOB, list) else DOB
        DOI = DOI[0] if DOI and isinstance(DOI, list) else DOI
        DOE = DOE[0] if DOE and isinstance(DOE, list) else DOE
        
        # Create a dictionary to store the extracted information
        passport_info = {
            "PASSNO": PASSNO,
            "SURNAME": SURNAME,
            "GIVENNAME": FULLNAME,
            "NATIONALITY": NATIONALITY,
            "C_CODE": C_CODE,
            "DOB": DOB[0] if DOB else None,
            "DOI": DOI[0] if DOI else None,
            "DOE": DOE[0] if DOE else None,
            "GENDER": GENDER,
            "POB": POB,
            "POE": POE
        }
        
        # Convert the dictionary to a JSON object
        passport_info_json = json.dumps(passport_info, indent=4)
        
        return passport_info_json

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)

# Define the image path
image_path = ""

# Extract passport information and print the JSON result
passport_info_json = extract_passport_info(image_path)
print(passport_info_json)
