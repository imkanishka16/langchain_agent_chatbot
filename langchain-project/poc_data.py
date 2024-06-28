import chainlit as cl
from langchain.chains import LLMChain, APIChain
from langchain_openai import OpenAI
from langchain.memory.buffer import ConversationBufferMemory
from dotenv import load_dotenv
import requests
from chainlit import AskUserMessage, Message, on_chat_start
from PIL import Image
from ice_cream_store_app import main as ocr_main,capture_selfie,verify_images
import io


load_dotenv()
# Define the API endpoint
API_URL = "http://localhost:5000/register_status"

@cl.on_chat_start
async def main():
    # Greet the user
    content = "Hi! Welcome to the Dialog. I am your Dialog assistant."
    await cl.Message(content=content).send()

    # Ask for the NIC
    nic_msg = await cl.AskUserMessage(content="Enter your NIC?", timeout=20).send()
    if nic_msg:
        nic = nic_msg["output"]  # Extract NIC from the 'content' key

    # # Ask for the name
    # name_msg = await cl.AskUserMessage(content="Enter your name?", timeout=20).send()
    # if name_msg:
    #     name = name_msg["output"]  # Extract name from the 'content' key

    # # Ask the user to upload the NIC image
    # files = await cl.AskFileMessage(
    #     content="Please upload your NIC as a PNG image to begin!",
    #     accept={"image/png": [".png",".jpg"]}
    # ).send()

    # if not files:
    #     await cl.Message(content="No file uploaded. Aborting.").send()
    #     return

    # image_file = files[0]
    # image = Image.open(image_file.path)

    # Prepare payload with NIC and name
    payload = {
        "nic_number": nic,
        # "name": name
    }

    try:
        # Make the POST request to the API with image file
            # with open(image_file.path, "rb") as f:
            #     image_bytes = f.read()
            # files = {"image_file": image_bytes}
            response = requests.post(API_URL, data=payload)
            
            response.raise_for_status()
            data = response.json()

            if response.status_code == 201:
                files = await cl.AskFileMessage(
                    content="You need to give NIC image as .png or .jpg format to continue:",
                    accept={"image/png": [".png",".jpg"]}
                ).send()
                image_file = files[0]
                image_path = image_file.path
                with open(image_file.path, "rb") as f:
                    image_bytes = f.read()
                files = {"image_file": image_bytes}
                ocr_result = ocr_main(image_path)
                result = f"Hello! welcome to Dialog. You are registered as our new customer this is your NIC details:\n{ocr_result}"
                # result = data['message']
            elif response.status_code == 200:
                connections = data['connections']
                result = f"{data['message']} Connections: MBB: {connections['mbb']}, HBB: {connections['hbb']}, DTV: {connections['dtv']}."
            else:
                result = "Unexpected response from the server."

    except requests.exceptions.RequestException as e:
        result = f"Error calling API: {str(e)}"

    # Send the result back to the user
    await cl.Message(content=result).send()
    

# Run the Chainlit app
if __name__ == "__main__":
    cl.run()

