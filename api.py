import json
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from langchain_ollama import OllamaLLM
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate

app = FastAPI()

shared_model = OllamaLLM(model="mistral", temperature=0.0, max_tokens=512)

class InputText(BaseModel):
    input_text: str

@app.post("/extract_cost/")
async def extract_cost(input_data: InputText):
    input_text = input_data.input_text
    
    prompt = """You are an AI-assistant that extracts structured data from service information pages of the flemish government.
    Details about provided structure will be provided between $$$$ symbols

    Context will be provided between #### symbols

    You follow the output structure defined below:
    $$$$
    {format_instructions}
    $$$$

    Service information text:
    ####
    {input_text}
    ####

    Provide only the json-output as answer.
    """

    class CostExtractor(BaseModel):
        cost: Optional[float] = Field(description="Cost of the service in euros.")

    cost_parser = PydanticOutputParser(pydantic_object=CostExtractor)

    system_prompt = PromptTemplate(
        template=prompt,
        input_variables=["input_text"],
        partial_variables={"format_instructions": cost_parser.get_format_instructions()},
    )

    chain = system_prompt | shared_model | cost_parser
    response = chain.invoke({"input_text": input_text})
    response = response.model_dump()
    response["input_text"] = input_text
    return response

@app.post("/extract_organisation/")
async def extract_organisation(input_data: InputText):
    input_text = input_data.input_text
    
    prompt = """You are an AI-assistant that extracts structured data from service information pages of the flemish government.
    Details about provided structure will be provided between $$$$ symbols

    Context will be provided between #### symbols

    You follow the output structure defined below:
    $$$$
    {format_instructions}
    $$$$

    Service information text:
    ####
    {input_text}
    ####

    Provide only the json-output as answer.
    """

    class OrganisationExtractor(BaseModel):
        organisation: str = Field(description="The geographic area or location where the service is applicable.")
        
    organisation_parser = PydanticOutputParser(pydantic_object=OrganisationExtractor)

    system_prompt = PromptTemplate(
        template=prompt,
        input_variables=["input_text"],
        partial_variables={"format_instructions": organisation_parser.get_format_instructions()},
    )

    chain = system_prompt | shared_model | organisation_parser
    response = chain.invoke({"input_text": input_text})
    response = response.model_dump()
    response["input_text"] = input_text
    return response