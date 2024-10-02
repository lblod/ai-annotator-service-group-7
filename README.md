# Flemish Government Service Information Extractor

## Introduction
This project is a FastAPI-based web application that extracts structured data from service information pages of the Flemish government. The application uses the LangChain library and the OllamaLLM model to process the input text and extract relevant information, such as the cost of the service and the organization responsible for it.

## Installation
To run this application, you'll need to have the following dependencies installed:

- Python 3.7 or later
- FastAPI
- Pydantic
- LangChain
- OllamaLLM

You can install these dependencies using pip:

```
pip install fastapi pydantic langchain langchain-ollama
```

## Usage
The application provides two endpoints:

1. `/extract_cost/`: This endpoint takes an `input_text` parameter and returns a JSON response containing the extracted cost of the service.

Example usage:

```
curl -X POST -H "Content-Type: application/json" -d '{"input_text": "The cost of this service is 25 euros."}' http://localhost:8000/extract_cost/
```

Response:
```json
{
  "cost": 25.0,
  "input_text": "The cost of this service is 25 euros."
}
```

2. `/extract_organisation/`: This endpoint takes an `input_text` parameter and returns a JSON response containing the extracted organization responsible for the service.

Example usage:

```
curl -X POST -H "Content-Type: application/json" -d '{"input_text": "This service is provided by the Flemish government."}' http://localhost:8000/extract_organisation/
```

Response:
```json
{
  "organisation": "Flemish government",
  "input_text": "This service is provided by the Flemish government."
}
```

## Code Structure
The code is organized as follows:

- `app.py`: This file contains the FastAPI application and the two endpoints for extracting cost and organization information.
- `InputText`: This is a Pydantic model that defines the input data structure for the endpoints.
- `CostExtractor` and `OrganisationExtractor`: These are Pydantic models that define the output data structure for the respective endpoints.
- `shared_model`: This is an instance of the `OllamaLLM` model, which is used to process the input text.
- `system_prompt`: This is a `PromptTemplate` object that defines the prompt used to extract the desired information from the input text.
- `cost_parser` and `organisation_parser`: These are `PydanticOutputParser` objects that are used to parse the model's output and convert it to the desired Pydantic model.
- `chain`: This is a LangChain "chain" that combines the prompt, model, and output parser to perform the extraction task.

## Notable Features
- **Performance Optimization**: The application uses the `OllamaLLM` model, which is a high-performance language model that can process text efficiently.
- **Security Considerations**: The application uses Pydantic models to validate the input and output data, which helps to ensure that the application is secure and robust.

## Contributing
If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request on the project's GitHub repository.

## License
This project is licensed under the [MIT License](LICENSE).