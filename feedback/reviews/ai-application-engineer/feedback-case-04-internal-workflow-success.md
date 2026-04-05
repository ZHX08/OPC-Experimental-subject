# AI 应用工程师反馈回流样例 - case 04

## 1. 任务背景
- 任务类型：AI 应用工程师推荐报告回流
- 目标岗位：AI 应用工程师（内部流程自动化）
- 关联 JD：`jd-aie-20260405-004`
- 关联候选人：`cand-liu-ming-004`
- 关联报告：`rep-aie-20260405-004`
- Workflow stage：`recommendation_report`
- 目的：沉淀内部系统集成方向的成功样例

## 2. AI 初稿摘要
- 推荐决策：`recommend`
- 理由：候选人有工作流和系统集成经验。
- 主要判断：初稿对监控、回滚和审计的强调还不够强。

## 3. 人工修改点
- 强化“内部流程自动化”所需要的审计、回滚和监控
- 把“有工作流经验”改成“有稳定上线和可运营证据”
- 补充用户数、请求量和试点结果

## 4. 最终输出摘要
- 推荐决策：`recommend`
- 原因：候选人在内部系统集成、流程编排和兜底方面证据完整。
- 结论：通过，进入下一轮面试

## 5. 反馈记录（结构化样例）
```json
{
  "id": "fb-aie-20260405-004",
  "task_type": "ai_application_engineer_recommendation",
  "jd_id": "jd-aie-20260405-004",
  "candidate_id": "cand-liu-ming-004",
  "report_id": "rep-aie-20260405-004",
  "case_id": "case-04",
  "direction_id": "dir-aie-workflow",
  "success_failure": "success",
  "failure_reason": "",
  "human_edits": "人工把这条线的关键词从‘工作流能力’修正为‘可审计、可回滚、可监控的上线系统’。",
  "reuse_score": 0.91,
  "roi_signal": "审批和流转时间下降",
  "should_deepen": 1,
  "workflow_stage": "recommendation_report",
  "accepted": true,
  "score": 9.1,
  "notes": "内部流程自动化是当前最强样板。"
}
```
