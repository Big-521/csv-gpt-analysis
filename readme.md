# CSV 智能可视化分析 + GPT 解读

## 项目简介
本项目实现了一个基于 **FastAPI** 和 **Streamlit** 的 CSV 数据智能可视化分析工具。用户可以上传 CSV 文件，系统会自动生成数据统计信息、可视化图表，并调用 **Qwen（通义千问）** 模型生成中文数据分析报告。

## 功能特性
- **CSV 文件上传**：支持上传任意 CSV 文件。
- **数据预览**：展示前五行数据。
- **统计信息**：
  - 数据行数和列名
  - 每列非空值统计
  - 数值列描述性统计
  - 分类列唯一值数量
- **自动图表生成**：
  - 数值列：直方图
  - 分类列：柱状图
- **智能分析总结**：调用 Qwen 模型生成 3-5 句中文分析报告。
- **可视化界面**：基于 Streamlit 的简洁前端。

## 项目结构
```
project_root/
│
├── test1.py        # FastAPI 后端主文件
├── ui_app.py        # Streamlit 前端主文件
├── README.md       # 项目说明文档
└── requirements.txt # 依赖包
```

## 安装依赖
使用 Python 3.10+ 环境，安装所需依赖：
```bash
pip install fastapi uvicorn pandas matplotlib openai streamlit requests
```

## 环境变量
- `DASHSCOPE_API_KEY`：Qwen API Key，用于调用通义千问模型。

## 后端启动
```bash
uvicorn test1:app --reload --host 0.0.0.0 --port 8000
```

## 前端启动
```bash
streamlit run ui_app.py
```

## 使用方法
1. 打开前端网页。
2. 上传 CSV 文件。
3. 查看数据预览、统计信息、图表和 GPT 分析报告。

## FAQ
**Q: 上传 CSV 文件失败怎么办？**
- 确认文件后缀为 `.csv`。
- 确认后端 FastAPI 服务已启动。

**Q: GPT 分析报告为空？**
- 检查 `DASHSCOPE_API_KEY` 是否正确。
- 确认网络可以访问 Qwen API。

## 技术栈
- 后端：FastAPI + Pandas + Matplotlib + OpenAI Qwen API
- 前端：Streamlit

## 项目优化方向
- 支持更多文件格式（Excel、JSON）
- 增加图表交互功能
- 支持多语言分析报告

