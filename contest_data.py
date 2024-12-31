import json
import requests
import pandas as pd


def get_contest_data() -> list[dict]:
    url = "https://kenkoooo.com/atcoder/resources/contests.json"
    response = requests.get(url)
    return json.loads(response.text)


def create_dataframe(contest_data: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(contest_data)[['id', 'start_epoch_second', 'duration_second']]

    return df
