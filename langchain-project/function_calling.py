import requests
# from langchain_core.tools import tool,initialize_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain.agents import create_tool_calling_agent, AgentExecutor,AgentType
from langchain_experimental.llms.ollama_functions import OllamaFunctions


@tool
def get_special_offers():
    """
    Fetch special offers by sending a GET request to the API.

    Args:
        base_url (str): The base URL of the API (e.g., 'http://localhost:5000').

    Returns:
        str: The response text from the API, containing special offers formatted as plain text.
    """
    url = f"http://localhost:5000/special_offers"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors\
        print(response.text)
        return response.text
    
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"
  
@tool
def get_new_packages():
    """
    Fetch new packages by sending a GET request to the API.

    Args:
        base_url (str): The base URL of the API (e.g., 'http://localhost:5000').

    Returns:
        dict: The response text from the API containing new packages.
    """
    url = f"http://localhost:5000/new_package"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(response.text)
        return response.text
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
    
@tool
def get_menu():
    """
    Fetch the list data by sending a GET request to the API.

    Args:
        base_url (str): The base URL of the API (e.g., 'http://localhost:5000').

    Returns:
        dict: The response text from the API containing the list data.
    """
    url = f"http://localhost:5000/list"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(response.text)
        return response.text
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}
    
def choose_tool(user_query):
  """
  Selects the appropriate tool based on the user's query.

  Args:
      user_query (str): The user's question or request.

  Returns:
      str: The name of the selected tool (e.g., "get_special_offers")
          or None if no matching tool is found.
  """
  if "offers" in user_query.lower():
    return "get_special_offers"
  elif "new packages" in user_query.lower():
    return "get_new_packages"
  elif "menu" in user_query.lower():
    return "get_menu"
  else:
    return None

    
    
tools = {
    "model":"llama3",
    "function":[
      {
          "name": "get_special_offers",
          "description": "Get available special offers from dialog(dialog is telecommunication company)",
      },
      {
          "name": "get_new_packages",
          "description":"Get newly introduce packages by Dialog"
      },
      {
          "name":"get_menu",
          "description":"Get list of all packages (mobile broadband, home broaldband and dialog tv connenction)"
      }]
}

# get_special_offers()
# get_new_packages()


# prompt = ChatPromptTemplate.from_messages([
#     ("system", "you're a helpful assistant"), 
#     ("human", "{input}"), 
#     ("placeholder", "{agent_scratchpad}"),
# ])

if __name__ == "__main__":  # Ensures this part only runs when executed as a script
    llm = OllamaFunctions(
        model="llama3",
        temperature=0
    )

    tools_bind = [get_special_offers, get_new_packages, get_menu]
    llm_with_tools = llm.bind_tools(tools_bind)

    user_query = "what are available offers?"
    selected_tool = choose_tool(user_query)

    if selected_tool:
        # Call the selected tool and process the response
        response = getattr(llm_with_tools, selected_tool)()
        print(response)
    else:
        print("Sorry, I couldn't find a relevant tool for your query.")

# llm = OllamaFunctions(
#         model = "llama3",
#         temperature = 0
#     )

# tools_bind = [get_special_offers,get_new_packages,get_menu]
# llm_with_tools = llm.bind_tools(tools_bind)

# user_query = "what are available offers?"
# selected_tool = choose_tool(user_query)

# if selected_tool:
#   # Call the selected tool and process the response
#   response = getattr(llm_with_tools, selected_tool)()
#   print(response)
# else:
#   print("Sorry, I couldn't find a relevant tool for your query.")

# llm_with_tools.invoke([
# 	("system", "You're a helpful assistant"), 
# 	("human", "what are available offers?"),
# ])
# agent = create_tool_calling_agent(llm, tools, prompt)
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
# agent_executor.invoke({"input": "What are available offers?", })
# mrkl = initialize_agent(tools, llm, agent=AgentType., verbose=True)