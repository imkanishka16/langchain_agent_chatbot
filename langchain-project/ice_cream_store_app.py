from flask import Flask, jsonify, request
from data_store import list, offers,register,new_packages
from data_store import register
import easyocr
import requests
from PIL import Image
import ipywidgets as widgets
from IPython.display import display
from io import BytesIO
import numpy as np
import os
from werkzeug.utils import secure_filename
import tempfile
import cv2
import pytesseract
import re
from deepface import DeepFace
import data_store
app = Flask(__name__)

def is_nic_registered(nic_number, register_data):
    for person in register_data["registered"]:
        if person["NIC"] == nic_number:
            return True
    return False

# Ensure pytesseract can find the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply bilateral filter to reduce noise and keep edges sharp
    filtered = cv2.bilateralFilter(gray, 11, 17, 17)
    
    # Apply adaptive thresholding to get a binary image
    thresh = cv2.adaptiveThreshold(filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    
    return thresh

def extract_name(image):
    # Use Tesseract to do OCR on the image
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config)
    
    # Use regex to find the pattern starting with "1,2."
    name_pattern = r"1,2\.\s*([A-Z\s]+)"
    match = re.search(name_pattern, text)
    
    if match:
        return match.group(1).strip()
    return "Name not found"

def extract_id(image):
    # Use Tesseract to do OCR on the image
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, config=custom_config)
    
    # Use regex to find the pattern starting with "4d." and ending with a space
    # id_pattern = r"4d\.\s*(\d+)"
    id_pattern = r"4d\.\s*(\d+\s*V?)"
    match = re.search(id_pattern, text)
    
    if match:
        return match.group(1).strip()
    return "ID not found"

def main(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Preprocess the image
    preprocessed_image = preprocess_image(image)
    
    # Extract the name from the preprocessed image
    name = extract_name(preprocessed_image)
    id = extract_id(preprocessed_image)
    
    # print(f"Your Name: {name}")
    # print(f"Your NIC: {id}")
    return f"Your Name: {name} \n Your NIC: {id}"

# Function to capture a selfie from the live camera
def capture_selfie():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        # Display the frame
        cv2.imshow('Press Space to Capture', frame)

        # Wait for the space key to capture the image
        if cv2.waitKey(1) & 0xFF == ord(' '):
            captured_image_path = 'selfie.jpg'
            cv2.imwrite(captured_image_path, frame)
            break

    cap.release()
    cv2.destroyAllWindows()
    return captured_image_path

# Function to verify two images using DeepFace
def verify_images(img1_path, img2_path):
    try:
        if img1_path and img2_path:  # Check both image paths
            # Verify the captured selfie against the comparison image
            result = DeepFace.verify(img1_path=img1_path, img2_path=img2_path)
            
            # Check the result and return appropriate message
            if result["verified"]:
                return "Same Person"
            else:
                return "Not the Same Person"
        else:
            return "Image paths are not valid."
    except Exception as e:
        print(f"Error: {e}")
        return None

@app.route('/register_status', methods=['POST'])
def check_register_nic():
    """
    Check user registration status.
    Registers a new user if the NIC is not already in the data store.
    """
    data = request.form  # Accessing form data correctly
    nic_number = data.get('nic_number')
    # image_file = request.files.get('image_file')
    
    if nic_number is None:
        return jsonify({'error': 'NIC number is required'}), 400
    
    if is_nic_registered(nic_number, register):
        # Fetch and return existing connections
        for person in register["registered"]:
            if person["NIC"] == nic_number:
                return jsonify({
                    'message': f'The NIC {nic_number} is already registered under the name {person["name"]}.',
                    'connections': {
                        'mbb': person["mbb"],
                        'hbb': person["hbb"],
                        'dtv': person["dtv"]
                    }
                }), 200
    else:
        return jsonify({'message': 'You need to give NIC image as .png or .jpg format to continue'}), 201
        # name = data.get('name')

        # if name is None:
        #     return jsonify({'error': 'Name is required for registering a new NIC'}), 400

        # if image_file is None:
        #     return jsonify({'error': 'Image file is required for extracting NIC details'}), 400

        # # Save the uploaded image file to a temporary location
        # with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        #     image_path = temp_file.name
        #     image_file.save(image_path)

        # # Extract text from the image
        # nic_details = main(image_path)
        

        # # Register the new NIC
        # register["registered"].append({"name": name, "NIC": nic_number})

        # # Clean up: remove the saved file after processing
        # os.remove(image_path)

        # return jsonify({
        #     # 'message': f'This is your NIC details: {nic_details} \nNIC {nic_number} has been registered under the name {name}.'
        #     'message': f'This is your NIC details:\n{nic_details}'
        # }), 201


@app.route('/list',methods = ['GET'])
def get_menu():
    """
    Retrieves the list data.
    Returns:
        A tuple containing the list data as JSON and the HTTP status code.
    """
    return jsonify(list), 200

# @app.route('/special_offers', methods = ['GET'])
# def get_special_offer():
#     """
#     Retrieves the special offer
#     Return:
#         A tuple containing the special offers data as JSON and the HTTP status code.
#     """
#     return jsonify(offers), 200
@app.route('/special_offers', methods=['GET'])
def get_special_offer():
    offers_list = data_store.offers["offers"]
    formatted_offers = ""
    for offer in offers_list:
        formatted_offers += f"description = {offer['description']}\n"
        formatted_offers += f"url = {offer['url']}\n\n"
    return formatted_offers, 200, {'Content-Type': 'text/plain; charset=utf-8'}


@app.route('/new_package', methods = ['GET'])
def get_new_packages():
    """
    Retrieves the special offer
    Return:
        A tuple containing the special offers data as JSON and the HTTP status code.
    """
    return jsonify(new_packages), 200

# @app.route('/customer-reviews', methods = ['GET'])
# def get_customer_reviews():
#     """
#     Retrieve the customer reviews data
#     Returns:
#         A tuple containing the customer reviews data as JSON and the HTTP status code.
#     """
#     return jsonify(customer_reviews), 200

# @app.route('/customizations', methods = ['GET'])
# def get_custoizations():
#     """
#     Retrive the customizations data
#     Returns:
#         A tuple containing the customizations data as JSON and the HTTP status code
#     """
#     return jsonify(customizations), 200

if __name__ == '__main__':
    app.run(debug = True)