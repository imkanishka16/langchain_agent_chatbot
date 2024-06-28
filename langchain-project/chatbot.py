import chainlit as cl
from langchain.chains import LLMChain, APIChain
from langchain_openai import OpenAI
from langchain.memory.buffer import ConversationBufferMemory
from dotenv import load_dotenv
import requests
from chainlit import AskUserMessage, Message, on_chat_start

load_dotenv()

from api_docs import dialog_api_docs
from prompt import api_response_prompt, api_url_prompt,dialog_assistant_prompt_template


@cl.on_chat_start
def setup_multiple_chains():
    llm = OpenAI(model='gpt-3.5-turbo-instruct',
                 temperature=0)
    conversation_memory = ConversationBufferMemory(memory_key="chat_history",
                                                   max_len=200,
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
    
    if any(keyword in user_message for keyword in ["list","offer"]):
        # If any of the keywords are in the user_message, use api_chain
        response = await api_chain.acall(user_message,
                                         callbacks=[cl.AsyncLangchainCallbackHandler()])
    else:
        # Default to llm_chain for handling general queries
        response = await llm_chain.acall(user_message, 
                                         callbacks=[cl.AsyncLangchainCallbackHandler()])
    response_key = "output" if "output" in response else "text"
    await cl.Message(response.get(response_key, "")).send()


