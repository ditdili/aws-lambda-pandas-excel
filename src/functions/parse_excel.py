import pandas as pd
from src.utils.constants import COLUMNS_DICT


def read_to_df(bucket: str, key: str, s3_client=None) -> pd.DataFrame:
    if s3_client:
        obj = s3_client.get_object(Bucket=bucket, Key=key)["Body"].read()
        df = pd.read_excel(obj, sheet_name="Invoices")
    else:
        df = pd.read_excel(f"{bucket}/{key}", sheet_name="Invoices")

    return df


def parse_excel(bucket: str, key: str, s3_client=None) -> pd.DataFrame:
    try:
        df = read_to_df(bucket, key, s3_client)

        if not set(COLUMNS_DICT.keys()).issubset(df.columns):
            missing_columns = set(COLUMNS_DICT.keys()) - set(df.columns)
            raise ValueError(f"Missing columns: {', '.join(missing_columns)}")

        df.rename(columns=COLUMNS_DICT, inplace=True)
        df["currency"] = df["amount"].str.extract(r"([A-Za-z]+)")
        df["amount"] = df["amount"].str.extract(r"(\d+\.?\d*)").astype(int)
        df["date"] = (
            pd.to_datetime(df["date"]).dt.tz_localize("US/Eastern").dt.tz_convert("UTC")
        )

        return {"values": df.to_dict(orient="records")}
    except Exception as e:
        raise e
