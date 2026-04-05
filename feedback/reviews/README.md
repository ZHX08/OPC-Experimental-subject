# Feedback Reviews

放人工修改、最终版本、采用结果与评分。

## AI 应用工程师

- `feedback-loop-sample.md`：企业知识工作台，推荐通过
- `feedback-case-02-support-copilot-success.md`：客服 Copilot，推荐通过
- `feedback-case-03-sales-proposal-failure.md`：销售提案生成，不推荐
- `feedback-case-04-internal-workflow-success.md`：内部流程自动化，推荐通过

## 数据闭环

这些记录已经被同步映射到 `data/direction-priority-db/seed.sql` 里的 `feedback_case_map`，可直接回流到方向优先级数据库。

上游如果要做真实试点，也可以先用 `verticals/recruiting/ai-application-engineer/sell-pack/internal-process-automation/pilot-evidence/` 里的试点前 / 中 / 后模板，把证据整理好再转成 feedback 记录。

## 新的本地试点回写路径

- 本地 UI：`apps/internal-process-automation-pilot/`
- 运行记录：`apps/internal-process-automation-pilot/data/runtime/`
- 回写包：`feedback/reviews/ai-application-engineer/`
- 下一步如果要进 SQLite：把回写包整理成 `case_id / direction_id / success_failure / human_edits / reuse_score / roi_signal / should_deepen` 再桥接到 `scripts/direction_priority_db.py`
