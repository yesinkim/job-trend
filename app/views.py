import pandas as pd
import streamlit as st

from utils.graph import job_graph_pie, sunburst_chart, top_stack_bar


def show_default_chart(df):
    """Top n개의 bar chart와 직종의 비율을 pie chart로 나타내는 함수"""
    # Chart
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(
            top_stack_bar(df["tech_stacks"], top_n=20), use_container_width=True
        )
    with c2:
        st.plotly_chart(job_graph_pie(df["job_name"], 0.5), use_container_width=True)


def default_view(df):
    st.plotly_chart(sunburst_chart(df), use_container_width=True)

    show_default_chart(df)


def search_view(
    df, job_name_selected, tech_stacks_selected, deadline_date, check_ongoing
):
    st.subheader("🗃 Result", divider="grey")
    filtered_df = df.copy()

    if job_name_selected != (["All"]):
        filtered_df = filtered_df[
            filtered_df["job_name"].apply(
                lambda x: any(tech in x for tech in job_name_selected)
            )
        ]
    if tech_stacks_selected != (["All"]):
        filtered_df = filtered_df[
            filtered_df["tech_stacks"].apply(
                lambda x: any(tech in x for tech in tech_stacks_selected)
            )
        ]
    if deadline_date and not filtered_df.empty:
        deadline_filter_date = pd.Timestamp(deadline_date)
        if check_ongoing:
            filtered_df = filtered_df[
                (pd.to_datetime(filtered_df["deadline"]) <= deadline_filter_date)
                & pd.notnull(filtered_df["deadline"])
            ]
        else:
            filtered_df = filtered_df[
                (pd.to_datetime(filtered_df["deadline"]) <= deadline_filter_date)
                | pd.isna(filtered_df["deadline"])
            ]

    with st.expander(":bar_chart: Chart", expanded=True):
        show_default_chart(filtered_df)

    if not tech_stacks_selected:
        st.warning("테크스택을 선택해주세요.")
    elif not job_name_selected:
        st.warning("직무를 선택해주세요.")
    elif filtered_df.empty:
        st.warning("검색되는 결과가 없습니다.")
    else:
        st.dataframe(
            data=filtered_df,
            column_config={"url": st.column_config.LinkColumn()},
            use_container_width=True,
            hide_index=True,
        )


def vector_search_view():
    pass
