# api.py
import re
from flask import request, jsonify, make_response
from langchain_ollama import OllamaLLM
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from typing import Optional, List


shared_model = OllamaLLM(base_url="http://hackathon-ai-7.s.redhost.be:11434", model="mistral", temperature=0.0, max_tokens=512)

class InputText(BaseModel):
    input_text: str

class CostExtractor(BaseModel):
    cost: Optional[float] = Field(description="Cost of the service in euros.")
    cost_string: Optional[str] = Field(description="If cost value is provided as string not as number return exact! words. Example: twenty euro")

class OrganisationExtractor(BaseModel):
    organisations_list: List[str] = Field(description="Identify and list the full names of flemish government organizations mentioned in the text, and separately list their corresponding abbreviations.")
    organisations_list_string: List[str] = Field(description="Identify and list the full names of flemish government organizations mentioned in the text. Return exact part of text where organisation was mentioned")

@app.route('/extract_cost/', methods=['POST', 'OPTIONS'])
def extract_cost():
    if request.method== "OPTIONS":
        return _build_cors_preflight_response()

    input_data = request.get_json()
    input_text = input_data['input_text']

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

    cost_parser = PydanticOutputParser(pydantic_object=CostExtractor)

    system_prompt = PromptTemplate(
        template=prompt,
        input_variables=["input_text"],
        partial_variables={"format_instructions": cost_parser.get_format_instructions()},
    )

    chain = system_prompt | shared_model | cost_parser
    response = chain.invoke({"input_text": input_text})
    response = response.model_dump()
    return _corsify_actual_response(jsonify(response))

@app.route('/extract_organisation/', methods=['POST','OPTIONS'])
def extract_organisation():
    if request.method== "OPTIONS":
        return _build_cors_preflight_response()
    input_data = request.get_json()
    input_text = input_data['input_text']

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

    organisation_parser = PydanticOutputParser(pydantic_object=OrganisationExtractor)

    system_prompt = PromptTemplate(
        template=prompt,
        input_variables=["input_text"],
        partial_variables={"format_instructions": organisation_parser.get_format_instructions()},
    )

    chain = system_prompt | shared_model | organisation_parser
    response = chain.invoke({"input_text": input_text})
    response = response.model_dump()
    new_organisations_list = []

    for org in response["organisations_list"]:
        match = re.search(r'\((.*?)\)', org)
        if match:
            abbreviation = match.group(1)
            new_org = re.sub(r'\(.*?\)', '', org).strip()
            new_organisations_list.append(new_org)
            new_organisations_list.append(abbreviation)
        else:
            new_organisations_list.append(org)

    response["organisations_list"] = new_organisations_list
    return _corsify_actual_response(jsonify(response))

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
