import logging
from src.utils.serialize import serialize
from src.functions.parse_excel import parse_excel
import traceback as tb
import boto3
import os

if logging.getLogger().hasHandlers():
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)  # pragma: no cover

log = logging.getLogger(__name__)


def main(event, context):
    log.info(f"Event: {serialize(event)}")
    if hasattr(context, "__dict__"):
        log.info(f"Context: {serialize(vars(context))}")  # pragma: no cover

    try:
        s3_client = boto3.client("s3")
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = event["Records"][0]["s3"]["object"]["key"]
        local = os.getenv("IS_LOCAL")

        parse_excel_response = parse_excel(
            bucket, key, s3_client=None if local else s3_client
        )

        log.info(serialize(parse_excel_response))

        response = {"statusCode": 200, "body": serialize(parse_excel_response)}

        return response

    except Exception as e:
        message = f"Error converting file {bucket}/{key}: {e}"
        log.error(message)
        log.error(tb.format_exc())
        response = {"statusCode": 500, "body": message}
        return response


if __name__ == "__main__":
    main("", "")  # pragma: no cover
