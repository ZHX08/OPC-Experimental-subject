# AI 应用工程师 Schema Pack

这个目录只服务 **AI 应用工程师** 这个岗位，不扩到其他岗位。

## 简短评估

第一步已经形成了“业务流程闭环”的雏形：
- 有 JD 拆解思路
- 有简历 / 候选人评估方向
- 有推荐报告模板
- 有反馈回流意识

但它还不是“结构闭环”，主要缺口是：
- 缺少岗位级、可机器读取的 schema
- 缺少 AI 应用工程师特有字段：业务场景、技术栈、工程证据、上线 / 评测要求
- 缺少从 JD → 匹配评估 → 推荐报告 → feedback 的统一数据流

结论：**可以进入第二步**，而且第二步应该先做结构化 schema，再继续补内容。

## 本包包含

- `schemas/jd.schema.json`
- `schemas/match-evaluation.schema.json`
- `schemas/recommendation-report.schema.json`
- `schemas/feedback.schema.json`

## 设计原则

1. 只围绕 AI 应用工程师岗位建模
2. 强制保留工程证据链，而不是只写“感觉不错”
3. 强制保留评测、上线、fallback、反馈回流字段
4. 输出结构尽量能直接喂给检索、生成和复盘流程

## 使用顺序

1. 先录入 JD schema
2. 再做匹配评估 schema
3. 再生成推荐报告 schema
4. 最后把实际结果回写 feedback schema

## 字段设计重点

- 业务场景 / 产品阶段 / 成功标准
- Prompt / RAG / workflow / tool calling / deployment 证据
- 评测指标 / 失败场景 / fallback
- 试用期验证点 / 是否可上线

## 当前补齐情况

- 已补 `workflows/examples/ai-application-engineer/` 端到端样例链路
- 已将 feedback capture / store 显式接入 `workflows/definitions/recruiting-jd-to-shortlist.yaml`
- 现在可以直接沿着 `JD → 匹配评估 → 推荐报告 → feedback` 跑最小可用闭环
