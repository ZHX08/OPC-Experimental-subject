# AI 应用工程师 Feedback Index

只放 **AI 应用工程师** 相关的人工修改和回流样例。

## 清单

- `feedback-loop-sample.md`
- `feedback-case-02-support-copilot-success.md`
- `feedback-case-03-sales-proposal-failure.md`
- `feedback-case-04-internal-workflow-success.md`

## 说明

这些记录对应 `workflows/examples/ai-application-engineer/cases/` 里的案例，重点保留：
- AI 初稿
- 人工修改点
- 最终采用结论
- 失败原因 / 改进动作

其中 `feedback-case-04-internal-workflow-success.md` 也被用于
`verticals/recruiting/ai-application-engineer/sell-pack/internal-process-automation/` 的客户沟通样板。

## SQLite 映射

同一组反馈样例已经写入 `data/direction-priority-db/feedback_case_map`，字段包含：
- `case_id`
- `direction_id`
- `success_failure`
- `failure_reason`
- `human_edits`
- `reuse_score`
- `roi_signal`
- `should_deepen`
