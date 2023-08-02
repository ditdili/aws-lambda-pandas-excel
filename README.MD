# Excel Processing Lambda

## Description

AWS Lambda to process excel files that are uploaded to S3 bucket. The function is triggered by S3 bucket event. The function will read the excel file using pandas, parse it, and convert it to json format.

## Tech

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
