# RichEditor / BD-Note

RichEditor 是一个面向写作、学习和办公场景的智能富文本编辑器项目，也是中国软件杯参赛项目。项目采用前后端分离架构：前端使用 Vue 3 + Vite + Tiptap 构建编辑器界面，后端使用 Flask 提供用户、文档、模板、AI、OCR 和本地知识库问答接口，数据存储使用 MongoDB。

仓库中还保留了比赛材料：

- `37014328文档.pdf`：项目说明文档
- `37014328演示.pptx`：项目演示文稿

## 项目功能

### 账号与文档管理

- 用户注册、登录、找回密码
- 文档创建、读取、保存、删除
- 文档重命名、标签修改、按标题搜索和按时间/标题/标签排序
- 当前文档定位、文档创建热力图
- 文档分享码生成、共享状态切换、通过分享码获取共享文档
- 文档导出为模板、从模板创建新文档

### 富文本编辑

编辑器基于 Tiptap，支持常见排版能力：

- 标题、段落、粗体、斜体、下划线、删除线、上下标
- 有序列表、无序列表、任务列表
- 字体、字号、文字颜色、背景高亮
- 左对齐、居中、右对齐、两端对齐
- 引用块、代码块、水平线、链接、图片
- 表格插入、增删行列、表头切换、单元格合并/拆分
- 代码高亮，支持 HTML、CSS、JavaScript、TypeScript、Python、Java、JSON、C 等语言
- 右侧自动生成内容大纲，并显示字符统计
- 浏览器打印方式导出 PDF

### AI 辅助写作

后端通过 `erniebot` 调用文心一言相关能力，前端以流式方式展示结果，当前代码中包含：

- 选中文本摘要
- 文本润色
- 文本续写
- 文本翻译
- 一键排版
- Markdown 表格生成
- Mermaid/UML 内容生成
- Markmap 思维导图内容提炼
- 基于本地知识库的 AI 对话

### OCR、语音与知识库

- 图片 OCR：上传图片后使用 PaddleOCR 识别中文文本
- 语音识别入口：前端已实现浏览器录音上传流程，后端当前返回的是示例文本
- 本地知识库：支持上传 `txt`、`pdf`、`xlsx`、`xls`、`docx`、`doc` 文件
- 知识库问答：使用 LangChain 加载文件，`text2vec-base-chinese` 生成向量，Chroma 持久化后进行相似文档检索，再结合大模型回答问题

## 技术栈

### 前端

- Vue 3
- Vite
- TypeScript / JavaScript
- Pinia
- Vue Router
- Tiptap
- Element Plus
- PrimeVue
- Tailwind CSS / DaisyUI
- ECharts、Cal Heatmap、ScrollReveal

### 后端

- Python 3.9
- Flask
- Flask-CORS
- MongoDB / PyMongo
- PaddleOCR
- OpenCV
- LangChain
- Chroma
- HuggingFace Embeddings
- text2vec-base-chinese
- erniebot

## 目录结构

```text
RichEditor-main/
├── backend/                 # Flask 后端
│   ├── app.py               # 后端入口与 API 路由
│   ├── auth.py              # 登录、注册、找回密码
│   ├── document.py          # 文档、模板、分享、热力图逻辑
│   ├── db_config.py         # MongoDB 连接配置
│   ├── models.py            # 用户、文档、模板等模型定义
│   ├── redisUtil.py         # Redis 工具文件
│   ├── environment.yml      # 旧开发环境记录，不需要新建 conda 环境
│   └── models/Embeddings/   # 本地 text2vec embedding 模型
├── frontend/                # Vue 前端
│   ├── src/
│   │   ├── views/           # 首页、登录页、编辑器页
│   │   ├── components/      # 首页、登录、编辑器组件
│   │   ├── hooks/           # 认证、文档、分享等组合逻辑
│   │   ├── store/           # Pinia 状态管理
│   │   ├── utils/           # Axios 请求封装
│   │   └── assets/          # 图片、图标、字体等静态资源
│   ├── package.json
│   └── vite.config.js
├── 37014328文档.pdf
├── 37014328演示.pptx
└── README.md
```

## 运行前准备

本项目不要求重新创建 conda 环境。直接使用你本机已有的 Python 3.9 环境、conda 环境或 venv 都可以，只要安装后端依赖即可。

需要提前准备：

- Node.js，建议 18+
- Python，建议 3.9
- MongoDB，本地默认地址为 `mongodb://localhost:27017/`
- 可用的文心一言 / AI Studio token
- Git LFS，或已经下载好的 `text2vec-base-chinese` 模型权重

后端默认数据库为 `richEditorDB`，代码会使用以下集合：

- `User`
- `Document`
- `Template`

如果 `backend/models/Embeddings/text2vec-base-chinese/pytorch_model.bin` 只有一百多字节，说明它只是 Git LFS 指针文件，不是真正的模型权重。需要先执行：

```powershell
git lfs install
git lfs pull
```

或者手动把完整的 `text2vec-base-chinese` 模型文件放回该目录，否则本地知识库向量化功能无法正常运行。

## 启动后端

进入后端目录：

```powershell
cd backend
```

使用已有 Python 环境安装依赖。下面是根据当前代码整理出的核心依赖，具体版本可参考 `backend/environment.yml`：

```powershell
pip install flask flask-cors pymongo numpy opencv-python erniebot paddleocr paddlepaddle langchain-community langchain-text-splitters chromadb sentence-transformers pypdf unstructured python-docx docx2txt openpyxl
```

如果你的机器使用 GPU 版 PaddlePaddle，可以按自己的 CUDA 版本安装 `paddlepaddle-gpu`，不要同时混装 CPU/GPU 版本。

当前 `backend/app.py` 中保留了比赛开发时的本机路径：

```python
sys.path.append("E:\\vue_flask\\RichEditor")
```

换机器运行时，建议删除这一行，或改成当前项目根目录。也可以在 PowerShell 里临时设置 `PYTHONPATH` 后启动：

```powershell
$env:PYTHONPATH = "$PWD\..;$PWD"
python app.py
```

后端默认运行在：

```text
http://localhost:5000
```

## 启动前端

打开新的终端，进入前端目录：

```powershell
cd frontend
```

安装依赖：

```powershell
npm install
```

启动开发服务器：

```powershell
npm run dev
```

前端默认会运行在 Vite 输出的本地地址，通常是：

```text
http://localhost:5173
```

前端请求地址写在 `frontend/src/utils/requests.ts` 中，目前固定为：

```ts
http://localhost:5000
```

因此本地运行时请先保证 Flask 后端已经启动。

## 常用页面

- `/home`：项目首页
- `/login`：登录、注册、找回密码
- `/editor`：富文本编辑器主界面

## 注意事项

- `backend/environment.yml` 是旧环境记录，可以用来查版本，但 README 不建议通过它新建 conda 环境。
- `backend/app.py` 中当前直接写入了 `erniebot.access_token`，正式使用时建议改成环境变量读取，避免泄露密钥。
- OCR、知识库构建和 Paddle 相关依赖较大，第一次运行可能需要较长初始化时间。
- 知识库向量会持久化到后端运行目录下的 `data/docs_<uid>`。
- 上传图片和知识库文件会写入后端运行目录下的 `static/images/<uid>` 和 `static/libs/<uid>`。
- 语音识别后端目前是演示返回值，真实 ASR 逻辑在 `backend/app.py` 中保留了注释代码入口。

## 构建前端

如需生成前端生产构建：

```powershell
cd frontend
npm run build
```

构建产物会输出到 `frontend/dist`。
