import json
import time

import requests
import pandas as pd

import contest_data as cd


ABC = cd.create_dataframe(cd.get_contest_data())
ABC = ABC.rename(columns={'id': 'contest_id'})
ABC = ABC[ABC.contest_id.str.startswith('abc')]


def get_user_data(user_name: str, start_epoch_time: int) -> list[dict]:
    url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={user_name}&from_second={start_epoch_time}"
    response = requests.get(url)
    return json.loads(response.text)


def create_dataframe(user_data: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(user_data)[['epoch_second', 'contest_id', 'problem_id', 'result']]
    return df


def ac_in_the_contest(contest_num, submit_time):
    start_time = ABC.iloc[contest_num-1, 1]
    end_time = ABC.iloc[contest_num-1, 1] + ABC.iloc[contest_num-1, 2]
    return start_time <= submit_time <= end_time


def modify_contest_num(contest_num: int):
    if contest_num >= 316:
        contest_num -= 1
    return contest_num


def abc_ac_time(
    start_contest_num: int, end_contest_num: int,
    user_name: str,
) -> pd.DataFrame:
    start_contest_num = modify_contest_num(start_contest_num)
    end_contest_num = modify_contest_num(end_contest_num)
    start_epoch_time = ABC.iloc[start_contest_num-1, 1]

    end_epoch_time = ABC.iloc[end_contest_num-1, 1] + ABC.iloc[end_contest_num-1, 2]
    user_data_list = []
    while (_user_data_list := get_user_data(user_name, start_epoch_time)):
        user_data_list += _user_data_list
        start_epoch_time = user_data_list[-1]['epoch_second']
        if start_epoch_time > end_epoch_time:
            break
        time.sleep(1)

    if not user_data_list:
        return pd.DataFrame()

    df = create_dataframe(user_data_list)
    df = df[df.contest_id.str.startswith('abc')]
    df = df[df.result == 'AC']
    df = df[df.apply(lambda x: ac_in_the_contest(
        modify_contest_num(int(x[1][3:])), x[0]
    ), axis=1)]
    df = df.groupby('problem_id').min()
    df.sort_values('epoch_second', inplace=True)
    df.reset_index(inplace=True)

    df = pd.merge(df, ABC, on='contest_id')
    df['AC_time'] = df['epoch_second'] - df['start_epoch_second']

    df = df[['contest_id', 'AC_time']].groupby('contest_id')['AC_time'].apply(list)
    df = df.to_frame().reset_index()
    df = pd.merge(df, ABC[['contest_id', 'start_epoch_second']])

    return df
