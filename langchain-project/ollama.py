from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_experimental.llms.ollama_functions import OllamaFunctions

#Pydantic schema for structured response
class Person(BaseModel):
    name:str = Field(description="The person's name",required=True)
    height:float = Field(description="The person's height", required = True)
    hair_color: str = Field(description="The person's hair color")
    
context = """Alex is 7 feet tall.
and she is blonde
"""

#prompt template llama 3
prompt = PromptTemplate.from_template(
    """
    <|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are a smart assistant take the following context and question below and return your answer in JSON.
    <|eot_id|><|start_header_id|>user<|end_header_id|>
    QUESTION:{question}\n
    CONTEXT: {context}\n
    JSON:
    <|eot_id|>
    <|start_header_id|>assistant<|end_header_id|>
    """
)

#chain
llm = OllamaFunctions(
    model="llama3",
    format="json",
    temperature= 0
)

structured_llm = llm.with_structured_output(Person)
chain = prompt|structured_llm

response = chain.invoke(
    {
        "question":"who is taller?",
        "context":context
    }
)

print(response)
