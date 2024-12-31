import pandas as pd
import numpy as np
import plotly.graph_objects as go


def make_fig(abc_ac_time: pd.DataFrame) -> go.Figure | None:
    if len(abc_ac_time) == 0:
        return None
    contest_ids = abc_ac_time.contest_id.apply(lambda x: int(x[3:])).to_list()

    ac_times = []
    for i in range(len(abc_ac_time)):
        ac_times.append(abc_ac_time.iloc[i, 1])
        ac_times[-1] += [None]*(8-len(ac_times[-1]))

    ac_times = np.array(ac_times)
    ac_times = ac_times.T

    # コンテストIDを基準にデータをまとめる
    hover_texts = []
    for j, contest_id in enumerate(contest_ids):
        hover_text = f'contest id: {contest_id}<br>'
        for i, ac_time in enumerate(ac_times):
            if ac_time[j] is not None:  # None をスキップ
                hover_text += f'{i+1}完: {ac_time[j]} sec<br>'
        hover_texts.append(hover_text)

    # グラフ作成
    fig = go.Figure()

    # すべてのトレースを一括で追加
    for i, ac_time in enumerate(ac_times):
        fig.add_trace(go.Scatter(
            x=contest_ids,
            y=ac_time,
            mode='lines+markers',
            name=f'{i+1}完'
        ))

    # カスタムツールチップを設定
    fig.update_traces(hovertemplate='%{text}<extra></extra>', text=hover_texts)

    fig.update_xaxes(title='ABC xxx')
    fig.update_yaxes(title='sec')

    return fig
