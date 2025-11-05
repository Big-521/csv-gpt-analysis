# 导入依赖
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
import io
from openai import OpenAI
import os
import matplotlib.pyplot as plt
import base64
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
matplotlib.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题
# FastAPI：用于创建 Web API 服务。
# File、UploadFile：FastAPI 内置的文件上传功能支持。
# JSONResponse：返回 JSON 格式的响应。
# pandas：用于处理 CSV 数据。
# io：Python 内置模块，用来处理内存中的二进制数据流。

# 创建应用对象
app = FastAPI()

# 配置 Qwen（通义千问）客户端
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 将 matplotlib 图表转成 Base64


def fig_to_base64():
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    plt.close()
    buf.seek(0)
    return "data:image/png;base64," + base64.b64encode(buf.read()).decode("utf-8")


# 定义上传接口


@app.post("/upload_csv")
async def upload_csv(file: UploadFile = File(...)):
    try:
        # 文件格式检查
        if not file.filename or not file.filename.endswith(".csv"):
            return JSONResponse(content={"error": "请上传 CSV 文件"}, status_code=400)
        # 读取 CSV 内容
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))

        # ======== 数据统计 ========
        summary = {
            # 基本信息统计
            "rows": len(df),
            "columns": list(df.columns),
            # 每列非空值数量
            "column_non_null_count": df.count().to_dict(),
            # 数值列的描述性统计
            "numeric_stats": df.describe(include=["number"]).to_dict(),
            # 字符串列的唯一值个数
            "categorical_unique_values": {
                col: df[col].nunique() for col in df.select_dtypes(include="object").columns
            }
        }

        # ===== 图表生成 =====
        charts = {}

        # 数值列 → 更清晰的直方图
        numeric_cols = df.select_dtypes(include="number").columns
        for col in numeric_cols:
            plt.figure(figsize=(5, 4))               # 统一设置大小
            df[col].dropna().hist(bins=30)           # 增加分箱数量
            plt.title(f"{col} - 分布直方图")
            plt.xlabel(col)
            plt.ylabel("频数")
            plt.tight_layout()                       # 自动调整布局
            charts[f"{col}_hist"] = fig_to_base64()

        # 分类列 → 更美观稳定的柱状图
        categorical_cols = df.select_dtypes(include="object").columns
        for col in categorical_cols:
            plt.figure(figsize=(6, 4))
            df[col].value_counts().head(15).plot(kind="bar")  # 限制最多显示15类，避免过密
            plt.title(f"{col} - 分类频数柱状图")
            plt.xlabel(col)
            plt.ylabel("出现次数")
            plt.xticks(rotation=45, ha="right")      # 处理过长标签
            plt.tight_layout()
            charts[f"{col}_bar"] = fig_to_base64()

        # GPT 自动生成中文分析报告
        prompt = f"""
        请根据以下 CSV 数据统计信息，生成一段中文的数据分析总结报告（3-5句话）：
        统计信息：{summary}
        """

        response = client.chat.completions.create(
            model="qwen-plus",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )

        gpt_content = response.choices[0].message.content
        gpt_summary = gpt_content.strip() if gpt_content else ""

        return {
            "filename": file.filename,
            "preview": df.head(5).to_dict(orient="records"),
            "summary": summary,
            "analysis_report": gpt_summary,
            "charts": charts
        }
    # 异常处理
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
