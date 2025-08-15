## 什么是 Dify

Dify 是一款开源的大语言模型(LLM) 应用开发平台。它融合了后端即服务（Backend as Service）和 LLMOps 的理念，使开发者可以快速搭建生产级的生成式 AI 应用。即使你是非技术人员，也能参与到 AI 应用的定义和数据运营过程中。

由于 Dify 内置了构建 LLM 应用所需的关键技术栈，包括对数百个模型的支持、直观的 Prompt 编排界面、高质量的 RAG 引擎、稳健的 Agent 框架、灵活的流程编排，并同时提供了一套易用的界面和 API。这为开发者节省了许多重复造轮子的时间，使其可以专注在创新和业务需求上。

## 为什么使用 Dify？
你或许可以把 LangChain 这类的开发库（Library）想象为有着锤子、钉子的工具箱。与之相比，Dify 提供了更接近生产需要的完整方案，Dify 好比是一套脚手架，并且经过了精良的工程设计和软件测试。

重要的是，Dify 是开源的，它由一个专业的全职团队和社区共同打造。你可以基于任何模型自部署类似 Assistants API 和 GPTs 的能力，在灵活和安全的基础上，同时保持对数据的完全控制。

## Dify 主要特点、优势和功能
### Dify 的特点和优势
Dify 提供安全数据通道、高可靠索引检索、友好提示词开发、多模型切换、推理观测、日志记录、数据标注、模型训练、微调、简化AI研发、定制化Agent自动化、AI工作流编排等优势，实现数据安全、开发高效、模型优化、自动化智能及工作流管理，助力开发者构建强大、灵活的AI应用。

### Dify 基本功能组成

|类别|	内容|
|---|---|
|LLM 推理引擎	|Dify Runtime (自 v0.4 移除了 LangChain)
|支持的商业模型	|10+，包括 OpenAI和 Anthropic <br>主流新模型可在 48 小时内接入|
|支持的 MaaS 厂商	|7 家：Hugging Face, Replicate, AWS Bedrock, NVIDIA, GroqCloud, together.ai, OpenRouter|
|支持的本地模型推理运行时	|6 种：Xoribits（推荐）、OpenLLM、LocalAI、ChatGLM、Ollama、NVIDIA TIS|
|OpenAI 接口标准模型集成	|无限支持|
|多模态能力	|ASR 模型、富文本模型（最高支持 GPT-4o 规格）|
|内置应用类型	|文本生成、聊天机器人、代理、工作流、对话流|
|Prompt-as-a-Service 编排	|广受好评的可视化编排界面，可集中修改 Prompt 并预览效果|
|编排模式	|简单编排、代理编排、流程编排|
|Prompt 变量类型	|字符串、单选枚举|
|外部 API 支持	|文件（2024 Q3 上线）|
|代理工作流特性	|行业领先的可视化工作流编排界面，实时编辑节点调试、模块化 DSL、原生代码运行时|
|支持的节点	|LLM、知识检索、问题分类器、IF/ELSE、代码、模板、HTTP 请求、工具|
|RAG 特性	|行业首个可视化知识库管理界面，支持片段预览和召回测试|
|索引方法	|关键词、文本向量、LLM 辅助问题-片段模型|
|检索方法	|关键词、文本相似度匹配、混合搜索、多路径检索、重排序模型|
|召回优化	|重排序模型|
|ETL 能力	|自动清理 TXT、Markdown、PDF、HTML、DOC、CSV 格式数据；支持非结构化服务|
|知识库同步	|同步 Notion 文档、网页作为知识库|
|支持的向量数据库	|Qdrant（推荐）、Weaviate、Zilliz/Milvus、Pgvector、Pgvector-rs、Chroma、OpenSearch、TiDB、腾讯向量、Oracle、Relyt、Analyticdb、Couchbase|
|代理技术	|ReAct、函数调用|
|工具支持	|调用 OpenAI 插件标准工具、直接加载 OpenAPI 规范 API 为工具|
|内置工具	|40+ 工具（截至 2024 Q2）|
|日志记录	|支持，基于日志的注释|
|注释回复	|基于人工标注的问答，用于基于相似性的回复；可导出为数据格式以微调模型|
|内容审核	|OpenAI 内容审核或外部 API|
|团队协作	|工作区、多成员管理|
|API 规范	|RESTful，覆盖大多数功能|
|部署方式	|Docker、Helm|

## 如何启动 Dify

点击右侧运行和调试按钮，点击运行，等待片刻，点击调试，即可看到效果。

<img src="/img/1.png">

此时，点击右侧web预览，选择80端口即可进入Dify界面。

<img src="/img/2.png">

<img src="/img/3.png">

## 向Dify中接入大模型
Dify 是基于大语言模型的 AI 应用开发平台，初次使用时你需要先在 Dify 的 **设置 -- 模型供应商** 页面内添加并配置所需要的模型。

<img src="/img/4.png">

<img src="/img/5.png">

Dify 已支持多家主流模型供应商，包括 OpenAI 的 GPT 系列、Anthropic 的 Claude 系列等。不同模型的能力和参数各异，用户可根据具体应用场景选择合适的供应商。在使用 Dify 的模型能力前，需从各模型厂商官网获取 API Key。

### 以火山方舟为例，接入DeepSeek V3大模型

点击 **添加模型**，选择模型类型为 **LLM**，输入模型名称，选择鉴权方式，输入模型 API Key

<img src="/img/6.png">

输入需要接入的推理点，点击 **保存** 即可。

<img src="/img/7.png">

此时，外部供应商的模型就已经接入成功

<img src="/img/8.png">

### 以火山方舟为例，接入豆包的嵌入模型
点击 **添加模型**，选择 **外部模型** 为**Text Embedding**，输入模型名称，选择鉴权方式，输入模型 API Key，并输入推理点

<img src="/img/10.png">


### 接入本地 Ollama 模型

>添加上一节中的文本嵌入模型dengcao/Qwen3-Embedding-8B:Q5_K_M

点击 **添加模型**，选择模型类型为 **Text Embedding**，输入模型名称
**dengcao/Qwen3-Embedding-8B:Q5_K_M**，输入本地URL **http://127.0.0.1:11434** ，点击 **保存** 即可。

<img src="/img/9.png">
