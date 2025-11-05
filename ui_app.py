import streamlit as st
import pandas as pd
import requests
import base64

# 设置网页页面标题和显示模式
st.set_page_config(page_title="📊 CSV 智能可视化分析", layout="wide")
st.title("📊 CSV 智能可视化分析 + GPT 解读")

# 前端调用的 后端接口地址
API_URL = "http://127.0.0.1:8000/upload_csv"

# 处理 CSV 文件上传
uploaded_file = st.file_uploader("上传 CSV 文件进行分析", type=["csv"])

if uploaded_file:
    with st.spinner("正在上传并分析数据..."):
        files = {"file": (uploaded_file.name,
                          uploaded_file.getvalue(), "text/csv")}
        response = requests.post(API_URL, files=files)

    if response.status_code != 200:
        st.error("❌ 上传失败：" + response.json().get("error", "未知错误"))
    else:
        data = response.json()

        # 展示返回的数据
        st.subheader("✅ 数据预览")
        preview_df = pd.DataFrame(data["preview"])
        st.dataframe(preview_df, use_container_width=True)
        # 数据统计部分
        summary = data["summary"]
        with st.expander("查看详细统计信息"):
            st.write(f"**行数**：{summary['rows']}")
            st.write(f"**列名**：{summary['columns']}")
            st.write("**每列非空统计：**")
            st.json(summary["column_non_null_count"])
            st.write("**数值列统计：**")
            st.json(summary["numeric_stats"])
            st.write("**分类列唯一值数量：**")
            st.json(summary["categorical_unique_values"])
            # 自动图表展示
        st.subheader("📈 自动生成图表")
        charts = data["charts"]
        for name, base64_img in charts.items():
            st.write(f"**{name}**")
            img_bytes = base64.b64decode(base64_img.split(",")[1])
            st.image(img_bytes, use_container_width=True)
        # GPT 数据分析总结
        st.subheader("🧠 智能分析总结")
        st.info(data["analysis_report"])
