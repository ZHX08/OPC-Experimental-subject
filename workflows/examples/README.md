# Workflow Examples

放真实任务样例与输入输出示例。

## 已补样例

- `customer-demand-to-plan.yaml`：客户需求到计划输出
- `ai-application-engineer/`：AI 应用工程师端到端样例链路
  - `cases/`：同一岗位下的多组对照样例，包含成功与失败案例

## AI 应用工程师样例链路

这条样例链路只服务 **AI 应用工程师**，不向其他岗位泛化。

推荐顺序：
1. `workflows/examples/ai-application-engineer/jd.sample.json`
2. `workflows/examples/ai-application-engineer/resume.sample.md`
3. `workflows/examples/ai-application-engineer/match-evaluation.sample.json`
4. `workflows/examples/ai-application-engineer/recommendation-report.sample.json`
5. `feedback/reviews/ai-application-engineer/feedback-loop-sample.md`

补充阅读：
- `workflows/examples/ai-application-engineer/cases/README.md`
- `feedback/reviews/ai-application-engineer/README.md`

它对应的 workflow 现在已经显式包含 feedback capture / store 步骤，用来把人工修改和最终采用结果回写。
