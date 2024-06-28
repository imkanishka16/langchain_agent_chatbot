import cv2
from deepface import DeepFace
import json
import chainlit as cl

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
    result = DeepFace.verify(img1_path=img1_path, img2_path=img2_path)
    return result

@cl.on_message
async def main(message: str):
    # Capture the selfie
    selfie_path = capture_selfie()

    if selfie_path:
        await cl.Message(content=f"Selfie captured and saved to {selfie_path}").send()

        # Ask the user to upload the comparison image
        files = await cl.AskFileMessage(
            content="You need to give NIC image as .png or .jpg format to continue:",
            accept={"image/png": [".png", ".jpg"]}
        ).send()

        if files:
            comparison_image_path = files[0].path
            await cl.Message(content=f"Comparison image saved to {comparison_image_path}").send()

            # Verify the captured selfie against the comparison image
            verification_result = verify_images(selfie_path, comparison_image_path)

            # Send the verification result to Chainlit
            await cl.Message(content="Verification Result:").send()
            await cl.Message(content=json.dumps(verification_result, indent=4)).send()

            # Send both images
            await cl.Image(path=selfie_path, name="Captured Selfie").send()
            await cl.Image(path=comparison_image_path, name="Comparison Image").send()
        else:
            await cl.Message(content="Failed to receive comparison image.").send()
    else:
        await cl.Message(content="Failed to capture selfie.").send()

if __name__ == "__main__":
    cl.run()
