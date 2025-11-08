"""
StructLang认知结构分析系统 - Streamlit前端
"""
import streamlit as st
import requests
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# API配置
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


# ============ 工具函数 ============

def get_topics():
    """获取话题列表"""
    try:
        response = requests.get(f"{API_BASE_URL}/topics/")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"获取话题失败: {str(e)}")
        return []


def analyze_question(question, topic_id):
    """分析问题"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/analysis/",
            json={"question": question, "topic_id": topic_id}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"分析失败: {str(e)}")
        return None


def submit_feedback(pattern_id, result, detail, rating):
    """提交反馈"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/feedbacks/",
            json={
                "pattern_id": pattern_id,
                "strategy_used": "已使用策略",
                "result": result,
                "result_detail": detail,
                "rating": rating
            }
        )
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"提交反馈失败: {str(e)}")
        return False


def get_cases(topic_id=None, verified=None):
    """获取案例列表"""
    try:
        params = {}
        if topic_id is not None:
            params["topic_id"] = topic_id
        if verified is not None:
            params["verified"] = verified

        response = requests.get(f"{API_BASE_URL}/cases/", params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"获取案例失败: {str(e)}")
        return []


def verify_case(case_id):
    """验证案例"""
    try:
        response = requests.put(f"{API_BASE_URL}/cases/{case_id}/verify")
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"验证失败: {str(e)}")
        return False


# ============ 页面函数 ============

def main_page():
    """主页 - 问题分析"""
    st.title("🧠 StructLang认知结构分析系统")
    st.markdown("---")

    # 获取话题列表
    topics = get_topics()
    if not topics:
        st.warning("暂无话题，请先初始化数据")
        return

    # 选择话题
    topic_options = {topic["name"]: topic["id"] for topic in topics}
    selected_topic = st.selectbox("选择话题", list(topic_options.keys()))
    topic_id = topic_options[selected_topic]

    # 输入问题
    st.subheader("📝 描述你的问题")
    question = st.text_area(
        "请详细描述你遇到的问题：",
        height=150,
        placeholder="例如：我想在公司申请晋升，但老板态度模糊，总说'再看看'..."
    )

    # 分析按钮
    if st.button("🔍 开始分析", type="primary"):
        if not question:
            st.warning("请先输入问题描述")
            return

        with st.spinner("AI正在分析中..."):
            result = analyze_question(question, topic_id)

        if result:
            # 显示分析结果
            st.success("分析完成！")

            # 结构标注
            st.subheader("📊 结构分析")
            analysis = result["analysis"]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("主体结构", analysis["structure"]["subject"])
            with col2:
                st.metric("客体结构", analysis["structure"]["object"])
            with col3:
                st.metric("结构键", analysis["structure"]["structure_key"])

            # 意图向量
            st.subheader("🎯 意图向量")
            intent = analysis["intent"]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("时间维度", f"{intent['time']}/10")
                st.progress(intent["time"] / 10)
            with col2:
                st.metric("利益维度", f"{intent['benefit']}/10")
                st.progress(intent["benefit"] / 10)
            with col3:
                st.metric("风险维度", f"{intent['risk']}/10")
                st.progress(intent["risk"] / 10)

            # AI推理
            with st.expander("💡 AI推理过程"):
                st.write(analysis["reasoning"])

            # 策略推荐
            recommendations = result["recommendations"]
            if recommendations:
                st.subheader("💡 策略推荐")

                for i, rec in enumerate(recommendations, 1):
                    with st.expander(
                        f"策略 {i}: {rec['structure_key']} "
                        f"(成功率: {rec['success_rate']:.1%}, "
                        f"意图距离: {rec['intent_distance']})"
                    ):
                        st.markdown(f"**策略内容:**\n{rec['strategy']}")
                        st.markdown(f"**推理依据:**\n{rec['reasoning']}")

                        if rec["risk_warning"]:
                            st.warning(f"⚠️ 风险提示: {rec['risk_warning']}")

                        # 反馈区域
                        st.markdown("---")
                        st.markdown("**使用后反馈:**")

                        feedback_key = f"feedback_{i}"
                        result_option = st.radio(
                            "结果",
                            ["成功", "部分成功", "失败"],
                            key=f"result_{feedback_key}",
                            horizontal=True
                        )

                        detail = st.text_input(
                            "详细说明（可选）",
                            key=f"detail_{feedback_key}"
                        )

                        rating = st.slider(
                            "评分",
                            1, 5, 3,
                            key=f"rating_{feedback_key}"
                        )

                        if st.button("提交反馈", key=f"submit_{feedback_key}"):
                            if submit_feedback(
                                rec["pattern_id"],
                                result_option,
                                detail,
                                rating
                            ):
                                st.success("反馈已提交，感谢！")
            else:
                st.info(result["message"])


def case_management_page():
    """案例管理页面"""
    st.title("📚 案例管理")
    st.markdown("---")

    # 获取话题
    topics = get_topics()
    if not topics:
        st.warning("暂无话题")
        return

    # 筛选选项
    col1, col2 = st.columns(2)
    with col1:
        topic_options = {topic["name"]: topic["id"] for topic in topics}
        topic_options["全部"] = None
        selected_topic = st.selectbox("话题", list(topic_options.keys()))
        topic_id = topic_options[selected_topic]

    with col2:
        verified_options = {"全部": None, "已验证": 1, "未验证": 0}
        selected_verified = st.selectbox("验证状态", list(verified_options.keys()))
        verified = verified_options[selected_verified]

    # 获取案例
    cases = get_cases(topic_id, verified)

    if not cases:
        st.info("暂无案例")
        return

    # 显示案例
    st.subheader(f"共 {len(cases)} 个案例")

    for case in cases:
        with st.expander(
            f"{case['structure_key']} - "
            f"{'✅ 已验证' if case['verified'] else '⏳ 待验证'}"
        ):
            st.markdown(f"**描述:** {case['description']}")
            st.markdown(f"**结果:** {case['outcome']}")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**意图向量:**")
                st.write(f"- 时间: {case['intent_time']}/10")
                st.write(f"- 利益: {case['intent_benefit']}/10")
                st.write(f"- 风险: {case['intent_risk']}/10")

            with col2:
                if case["verified"] == 0:
                    if st.button("验证此案例", key=f"verify_{case['id']}"):
                        if verify_case(case["id"]):
                            st.success("已验证！")
                            st.rerun()


def statistics_page():
    """统计页面"""
    st.title("📈 系统统计")
    st.markdown("---")

    try:
        # 获取所有数据
        topics = get_topics()
        cases = get_cases()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("话题数量", len(topics))

        with col2:
            verified_cases = [c for c in cases if c["verified"] == 1]
            st.metric("已验证案例", len(verified_cases))

        with col3:
            unverified_cases = [c for c in cases if c["verified"] == 0]
            st.metric("待验证案例", len(unverified_cases))

        # 按话题统计
        st.subheader("📊 各话题案例分布")
        for topic in topics:
            topic_cases = [c for c in cases if c["topic_id"] == topic["id"]]
            st.write(f"**{topic['name']}:** {len(topic_cases)} 个案例")

    except Exception as e:
        st.error(f"加载统计数据失败: {str(e)}")


# ============ 主应用 ============

def main():
    """主应用"""
    st.set_page_config(
        page_title="StructLang分析系统",
        page_icon="🧠",
        layout="wide"
    )

    # 侧边栏导航
    st.sidebar.title("导航")
    page = st.sidebar.radio(
        "选择页面",
        ["问题分析", "案例管理", "系统统计"]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 关于")
    st.sidebar.info(
        "StructLang认知结构分析系统\n\n"
        "基于StructLang方法论，通过AI辅助分析人际互动问题，"
        "提供基于认知结构的策略推荐。"
    )

    # 路由
    if page == "问题分析":
        main_page()
    elif page == "案例管理":
        case_management_page()
    elif page == "系统统计":
        statistics_page()


if __name__ == "__main__":
    main()
