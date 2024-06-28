from langchain import PromptTemplate

dialog_assistant_prompt = """
you are helpful telecomunication assistant call 'Dialog'.
Dialog provides mobile broadband, home broadband, and Dialog TV connection services. 
You do not provide information outside of this scope. 
If user ask about call to user given API. Please call user given endpoint without any hesitation. That is one of your task.

Question: {question}
Answer:"""
#If a question is not about telecommunication, respond with, "I specialize only in telecommunication-related queries.
dialog_assistant_prompt_template = PromptTemplate(
    input_variables=["question"],
    template=dialog_assistant_prompt
)


api_url_template = """
Given the following API Documentation for dialog's official 
telecommunication API: {api_docs}
Your task is to construct the most efficient API URL to answer 
the user's question, ensuring the 
call is optimized to include only necessary information.
Question: {question}
API URL:
"""

api_url_prompt = PromptTemplate(input_variables=['api_docs', 'question'],
                                template=api_url_template)


api_response_template = """
Given the API Documentation for Dialog's official API:
{api_docs}
and the specific user question:
{question}
and the API URL:
{api_url}
You have retrieved the following JSON response:
{api_response}

Please extract and list all the information contained in the {api_response} in a clear and concise manner. Include all the details provided in the JSON, such as descriptions and URLs.
If there are any urls in {api_response} need to provide pointwise.

directly address user query. 
Summary:
"""

api_response_prompt = PromptTemplate(input_variables=['api_docs', 
                                                      'question', 
                                                      'api_url',
                                                      'api_response'],
                                     template=api_response_template)