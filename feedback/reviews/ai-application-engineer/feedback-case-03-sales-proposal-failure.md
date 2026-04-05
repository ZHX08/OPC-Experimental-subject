# AI 应用工程师反馈回流样例 - case 03

## 1. 任务背景
- 任务类型：AI 应用工程师推荐报告回流
- 目标岗位：AI 应用工程师（销售提案生成）
- 关联 JD：`jd-aie-20260405-003`
- 关联候选人：`cand-chen-che-003`
- 关联报告：`rep-aie-20260405-003`
- Workflow stage：`recommendation_report`
- 目的：记录一个典型失败样例

## 2. AI 初稿摘要
- 推荐决策：`谨慎推荐`
- 理由：候选人理解销售场景，也会维护 prompt 模板。
- 主要判断：把 prompt 与文案整理能力放得太高，低估了工程与上线证据的缺失。

## 3. 人工修改点
- 直接把结论从“谨慎推荐”改成“不推荐”
- 强调候选人缺少可验证的生产系统、接口集成和评测闭环
- 把“能做提案草稿”与“能做 AI 应用工程师”明确拆开

## 4. 最终输出摘要
- 推荐决策：`reject`
- 原因：缺少上线、工程和回流证据，和岗位核心要求不匹配。
- 结论：不推进面试，建议转向内容 / prompt 运营岗位

## 5. 反馈记录（结构化样例）
```json
{
  "id": "fb-aie-20260405-003",
  "task_type": "ai_application_engineer_recommendation",
  "jd_id": "jd-aie-20260405-003",
  "candidate_id": "cand-chen-che-003",
  "report_id": "rep-aie-20260405-003",
  "workflow_stage": "recommendation_report",
  "accepted": false,
  "score": 4.9,
  "failure_reason": "缺少上线、工程实现和评测闭环证据。",
  "notes": "这个案例说明：prompt 能力本身不能替代 AI 应用工程能力。"
}
```
