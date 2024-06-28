# import cv2
# from deepface import DeepFace
# import json

# # Function to capture a selfie from the live camera
# def capture_selfie():
#     cap = cv2.VideoCapture(0)
#     if not cap.isOpened():
#         print("Error: Could not open video stream.")
#         return None

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Error: Failed to capture image.")
#             break

#         # Display the frame
#         cv2.imshow('Press Space to Capture', frame)

#         # Wait for the space key to capture the image
#         if cv2.waitKey(1) & 0xFF == ord(' '):
#             captured_image_path = 'selfie.jpg'
#             cv2.imwrite(captured_image_path, frame)
#             break

#     cap.release()
#     cv2.destroyAllWindows()
#     return captured_image_path

# # Capture the selfie
# selfie_path = capture_selfie()

# # Function to verify two images using DeepFace
# def verify_images(img1_path, img2_path):
#     if selfie_path:
#         result = DeepFace.verify(img1_path=img1_path, img2_path=img2_path)
#         return(print(json.dumps(result, indent=4)))
    
#     # return result

# # Capture the selfie
# selfie_path = capture_selfie()

# # Check if the selfie was captured successfully
# if selfie_path:
#     # Define the path to the second image
#     comparison_image_path = 'licence2.jpg'
    
#     # Verify the captured selfie against the comparison image
#     verification_result = verify_images(selfie_path, comparison_image_path)
    
#     # Print the result
#     print(json.dumps(verification_result, indent=4))
# else:
#     print("Failed to capture selfie.")

import cv2
from deepface import DeepFace
import json

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

# # Function to verify two images using DeepFace
# def verify_images(img1_path, img2_path):
#     try:
#         result = DeepFace.verify(img1_path=img1_path, img2_path=img2_path)
#         return result
#     except Exception as e:
#         print(f"Error: {e}")
#         return None
    
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

# Capture the selfie
selfie_path = capture_selfie()
comparison_image_path = 'licence2.jpg'
verification_result = verify_images(selfie_path, comparison_image_path)
print(verification_result)
# # Check if the selfie was captured successfully
# if selfie_path:
#     # Define the path to the second image
#     comparison_image_path = 'licence2.jpg'
    
#     # Verify the captured selfie against the comparison image
#     verification_result = verify_images(selfie_path, comparison_image_path)
    
#     # Check the result and print appropriate message
#     if verification_result is not None:
#         if verification_result["verified"]:
#             print("Same Person")
#         else:
#             print("Not the Same Person")    
#     else:
#         print("Verification failed.")
# else:
#     print("Failed to capture selfie.")
