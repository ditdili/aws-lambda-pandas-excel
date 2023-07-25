# Excel Pandas Processing Lambda

## Description

This is a lambda function that will process an excel file and return a json object with the data. The excel file is expected to be in the following format:

## Tech:

- Python 3.10
- Serverless Framework
- AWS Lambda
- AWS S3 Bucket trigger
- Pandas through AWS Lambda Layer and venv in local development
- Logger and Serializer setup

## Installation

- Deploy using serverless framework

```bash
serverless deploy
```

## Local invocation

- Create a virtual environment and install dependencies

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

- Invoke the function locally

```bash
serverless invoke local --function main --path mocks/event.json
```

## Testing

Make sure that pytest is used from the virtual environment

```bash
which pytest
```

To run test files locally. It will include print statement as well if "-s" flag is used:

```bash
pytest --no-header -v -s --log-cli-level=INFO
```

To run coverage report:

```bash
coverage run -m pytest --no-header -v -s --log-cli-level=INFO && coverage report -m
```
