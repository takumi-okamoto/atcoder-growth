import streamlit as st

import user_data as ud
import graph


def main() -> None:
    st.title('ABC の各コンテストでn 完するのにかかった時間の可視化')
    st.markdown('[Source code](https://github.com/takumi-okamoto/atcoder-growth)')
    st.markdown('製作: [kmmtkm](https://x.com/ayumu_togu)')

    user_name = st.text_input(label='user name', value='kmmtkm')

    with st.spinner('データ取得中'):
        fig = graph.make_fig(ud.abc_ac_time(1, 386, user_name))
    if fig is None:
        st.warning('user name を確認してください')
    else:
        st.plotly_chart(fig)


if __name__ == '__main__':
    main()
