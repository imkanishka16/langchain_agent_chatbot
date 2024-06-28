import chainlit as cl
from langchain.chains import LLMChain, APIChain
from langchain_openai import OpenAI
from langchain.memory.buffer import ConversationBufferMemory
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from dotenv import load_dotenv
import requests
from chainlit import AskUserMessage, Message, on_chat_start
from PIL import Image
from ice_cream_store_app import main as ocr_main,capture_selfie,verify_images
import io
from api_docs import dialog_api_docs
from langchain_community.llms import CTransformers
from prompt import api_response_prompt, api_url_prompt,dialog_assistant_prompt_template
from test_verification import final_output

load_dotenv()
# Define the API endpoint
API_URL = "http://localhost:5000/register_status"

@cl.on_chat_start
async def main():
    # Greet the user
    content = "Hi! Welcome to the Dialog🙂. I am your Dialog assistant🤖."
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
                
                # Capture the selfie
                selfie_path = capture_selfie()
                
                comparison_image_path = image_path
                
                verification_result = verify_images(selfie_path, comparison_image_path)
                
                result = f"Hello! welcome to Dialog🙂. This is your NIC details:\n{ocr_result}\n\n##########\nYour face verification result: {verification_result}\n########## \n\n📱 Hey there! Ready to connect with the best? Join the Dialog family and experience top-notch telecommunications! 📡✨\n\n Check available services and packages(Ask from me👇)"
                # result = data['message']
            elif response.status_code == 200:
                final_output(nic)
                selfie_path = capture_selfie()
                comparison_image_path = "download/download_image.jpg"
                verification_result = verify_images(selfie_path, comparison_image_path)
                connections = data['connections']
                result = f"##########\nYour face verification result: {verification_result}\n##########\n\n{data['message']} Connections: MBB: {connections['mbb']}, HBB: {connections['hbb']}, DTV: {connections['dtv']}.\n\nWould you like to see available new packages and special offers💥(Ask from me👇)"
            else:
                result = "Unexpected response from the server."

    except requests.exceptions.RequestException as e:
        result = f"Error calling API: {str(e)}"

    # Send the result back to the user
    await cl.Message(content=result).send()
    
    # llm = OpenAI(model='gpt-3.5-turbo-instruct',
    #              temperature=0,
    #              max_tokens=500)
   
    llm = OllamaFunctions(
        model = "llama3",
        temperature = 0
    )
    
    conversation_memory = ConversationBufferMemory(memory_key="chat_history",
                                                   max_len=300,
                                                   return_messages=True,
                                                   )
    llm_chain = LLMChain(llm=llm, prompt=dialog_assistant_prompt_template, 
						memory=conversation_memory)
    cl.user_session.set("llm_chain", llm_chain)
    
    api_chain = APIChain.from_llm_and_api_docs(
            llm=llm,
            api_docs=dialog_api_docs,
            api_url_prompt=api_url_prompt,
            api_response_prompt=api_response_prompt,
            verbose=True,
            limit_to_domains=["http://127.0.0.1:5000/"],  # Allow all endpoints on this domain
        )
    cl.user_session.set("api_chain", api_chain)
    
@cl.on_message
async def handle_message(message: cl.Message):
    user_message = message.content.lower()
    llm_chain = cl.user_session.get("llm_chain")
    api_chain = cl.user_session.get("api_chain")
    
    if any(keyword in user_message for keyword in ["list","offer","new packages"]):
        # If any of the keywords are in the user_message, use api_chain
        response = await api_chain.acall(user_message,
                                         callbacks=[cl.AsyncLangchainCallbackHandler()])
    else:
        # Default to llm_chain for handling general queries
        response = await llm_chain.acall(user_message, 
                                         callbacks=[cl.AsyncLangchainCallbackHandler()])
    response_key = "output" if "output" in response else "text"
    await cl.Message(response.get(response_key, "")).send()


# Run the Chainlit app
if __name__ == "__main__":
    cl.run()