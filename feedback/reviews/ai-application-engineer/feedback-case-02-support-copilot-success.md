# AI 应用工程师反馈回流样例 - case 02

## 1. 任务背景
- 任务类型：AI 应用工程师推荐报告回流
- 目标岗位：AI 应用工程师（客服 Copilot）
- 关联 JD：`jd-aie-20260405-002`
- 关联候选人：`cand-wang-qi-002`
- 关联报告：`rep-aie-20260405-002`
- Workflow stage：`recommendation_report`
- 目的：把客服 Copilot 的推荐判断沉淀成可复用样本

## 2. AI 初稿摘要
- 推荐决策：`recommend`
- 理由：候选人具备客服 Copilot、工单摘要和知识检索项目经验。
- 主要判断：技术链路完整，但对高风险工单升级、监控告警和 SLA 约束写得不够强。

## 3. 人工修改点
- 把“技术完整”改成“有生产证据、升级流转和回滚机制”
- 补上客服/质检/主管三个角色的协同方式
- 把“会做 RAG”改成“能控制高风险回答和人工升级”

## 4. 最终输出摘要
- 推荐决策：`recommend`
- 原因：候选人能把客服 Copilot 做到稳定运行，并且有抽样复核、升级流转和回流样例。
- 结论：通过，进入下一轮面试

## 5. 反馈记录（结构化样例）
```json
{
  "id": "fb-aie-20260405-002",
  "task_type": "ai_application_engineer_recommendation",
  "jd_id": "jd-aie-20260405-002",
  "candidate_id": "cand-wang-qi-002",
  "report_id": "rep-aie-20260405-002",
  "workflow_stage": "recommendation_report",
  "accepted": true,
  "score": 8.8,
  "failure_reason": "",
  "notes": "人工把评估重点拉回到上线证据、升级阈值和 fallback，而不是只看技术栈。"
}
```
