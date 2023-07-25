import logging
import pandas as pd
from src.utils.serialize import serialize
import traceback as tb

if logging.getLogger().hasHandlers():
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)

log = logging.getLogger(__name__)


def main(event, context):
    log.info(f"Event: {serialize(event)}")
    if hasattr(context, "__dict__"):
        log.info(f"Context: {serialize(vars(context))}")

    try:
        bucket = event["Records"][0]["s3"]["bucket"]["name"]
        key = event["Records"][0]["s3"]["object"]["key"]

        body = {
            "bucket": bucket,
            "key": key,
        }

        log.info(serialize(body))

        response = {"statusCode": 200, "body": serialize(body)}
        return response

    except Exception as e:
        message = f"Error converting file: {e}"
        log.error(message)
        log.error(tb.format_exc())
        response = {"statusCode": 500, "body": message}
        return response


if __name__ == "__main__":
    main("", "")
