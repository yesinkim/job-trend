import streamlit as st

from utils.query import get_data, load_model
from views import default_view, search_view, side_vector_search

st.set_page_config(
    page_title="JobTrend",
    page_icon=":chart_with_upwards_trend:",
    initial_sidebar_state="expanded",
    layout="centered",
    menu_items={
        "Report a bug": "https://github.com/heehehe/job-trend/issues",
        "About": "# JobTrend",
    },
)


def main():
    st.title("JOB TREND for EVERYBODY")
    if not st.session_state.get("view_function"):
        st.session_state["view_function"] = default_view

    with st.spinner("Get data..."):
        df = get_data()

    job_names = df["job_name"].unique().tolist()
    tech_stacks = df["tech_stacks"].explode().unique().tolist()
    companies = df["company_name"].unique().tolist()

    # 사이드바
    with st.sidebar:
        st.title(":technologist: Search the JobTrend")
        tab1, tab2 = st.tabs([":mag: Search", ":sparkles: AI Search"])

    # 탭1: 일반 검색
    with tab1:
        job_name_selected = st.multiselect(
            "Select job name", ["All"] + job_names, "All"
        )
        tech_stacks_selected = st.multiselect(
            "Select tech stacks", ["All"] + tech_stacks, "All"
        )
        deadline_date = st.date_input("Select a deadline")
        check_ongoing = st.checkbox("Exclude ongoing")

        if st.button(":mag: Search!", key="search_button", use_container_width=True):
            st.session_state["view_function"] = search_view  # search_view로 뷰 변경
        print(f"{job_name_selected=}, {tech_stacks_selected=}, {deadline_date=}")

    # 탭 2: 벡터 검색
    with tab2:
        model = load_model()
        side_vector_search(model)
        if st.button(
            ":sparkles: Clear History!", key="vector_search_button", use_container_width=True
        ):
            st.session_state["chat_session"] = model.start_chat(history=[])

    # 메인화면
    st.subheader("Overview", divider="grey")
    m1, m2, m3, m4, m5 = st.columns(5)
    m2.metric("**Count of Jobs**", len(job_names))
    m3.metric("**Count of Tech Stacks**", len(tech_stacks))
    m4.metric("**Total Companies**", len(companies))

    # view 분기
    with st.spinner("Loading..."):
        if st.session_state["view_function"] == search_view:
            search_view(
                df,
                job_name_selected,
                tech_stacks_selected,
                deadline_date,
                check_ongoing,
            )
        else:
            default_view(df)

    # default view가 아닐 때 홈버튼 생성
    if st.session_state["view_function"] in [search_view]:
        st.markdown("")

        _, center, _ = st.columns(3)
        with center:
            if st.button(":house: Home", type="primary", use_container_width=True):
                st.session_state["view_function"] = default_view


if __name__ == "__main__":
    main()
