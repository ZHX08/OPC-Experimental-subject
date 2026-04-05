# AI 应用工程师反馈回流样例

> 这份记录对应 `workflows/examples/ai-application-engineer/` 里的样例链路。
>
> 它展示的是**推荐报告之后的回流**：把人工修改、最终采用结果、失败模式和改进动作写回去。

## 1. 任务背景
- 任务类型：AI 应用工程师推荐报告回流
- 目标岗位：AI 应用工程师
- 关联 JD：`jd-aie-20260405-001`
- 关联候选人：`cand-zhang-cheng-001`
- 关联报告：`rep-aie-20260405-001`
- Workflow stage：`recommendation_report`
- 目的：把人工修改后的判断沉淀成可复用反馈样本

## 2. AI 初稿摘要
- 推荐决策：`recommend`
- 理由：候选人具备 RAG、Prompt、workflow 和基础工程能力，做过企业知识助手与销售方案生成助手。
- 主要判断：技术栈与项目类型匹配，但对上线证据、评测方法和成本边界的强调还不够强。

## 3. 人工修改点
- 把“技术全面”改成“有上线证据、评测意识和反馈闭环”
- 把“能做 RAG”改成“能说明 chunking / rerank / 命中率 / feedback 回流”
- 补充“是否上线、多少用户在用、是否稳定运行”
- 补充“成本、延迟、fallback、人工确认点”

## 4. 最终输出摘要
- 推荐决策：`recommend`
- 原因：候选人能做 AI 应用工程落地，且有较完整的评测与回流意识；需要在后续面试继续确认线上规模和稳定性。
- 结论：通过，进入面试/客户沟通下一步

## 5. 反馈记录（结构化样例）
```json
{
  "id": "fb-aie-20260405-001",
  "task_type": "ai_application_engineer_recommendation",
  "jd_id": "jd-aie-20260405-001",
  "candidate_id": "cand-zhang-cheng-001",
  "report_id": "rep-aie-20260405-001",
  "workflow_stage": "recommendation_report",
  "input_snapshot": {
    "jd_version": "1.0",
    "candidate_version": "resume-v1",
    "report_version": "1.0",
    "key_signals": [
      "企业知识助手已稳定运行",
      "有抽样评测和人工复核",
      "有反馈回流和兜底意识"
    ],
    "source_materials": [
      "workflows/examples/ai-application-engineer/jd.sample.json",
      "workflows/examples/ai-application-engineer/resume.sample.md",
      "workflows/examples/ai-application-engineer/match-evaluation.sample.json",
      "workflows/examples/ai-application-engineer/recommendation-report.sample.json"
    ]
  },
  "ai_output_snapshot": {
    "decision": "recommend",
    "summary": "候选人具备 AI 应用工程落地经验，能做 RAG、workflow、评测和反馈闭环，但对上线规模和成本控制的强调不足。",
    "score": 8.2,
    "notable_risks": [
      "上线规模证据不够量化",
      "复杂部署经验需要追问",
      "成本控制细节需进一步确认"
    ]
  },
  "human_edit_snapshot": {
    "edited_sections": [
      "headline.summary",
      "match_overview.overall_assessment",
      "risk_analysis.risks",
      "evaluation_plan.feedback_loop"
    ],
    "change_summary": "把“技术栈匹配”改成“证据链匹配”，把评估重点从概念转为上线、评测、fallback 和回流。",
    "reason": "AI 初稿更关注技术术语，人工补上了证据链和可上线性。"
  },
  "final_outcome": {
    "result": "passed",
    "reason": "推荐结果通过，但要在面试中继续验证上线规模、评测方法和复杂部署能力。",
    "offer_status": "none",
    "onboarding_status": "not_started",
    "client_feedback": "候选人项目背景与岗位方向一致，愿意继续推进。",
    "candidate_feedback": "愿意补充项目 demo、评测和回流样本。"
  },
  "accepted": true,
  "score": 8.6,
  "failure_modes": [
    "初稿对上线证据和成本边界强调不足",
    "容易把“会做 RAG”误当成“能稳定上线”"
  ],
  "improvement_actions": [
    "强制输出业务目标、工程证据和评测方式",
    "在推荐报告里单独写 fallback 与成本边界",
    "回流记录中保存人工修改理由"
  ],
  "lessons": [
    "AI 应用工程师评估不能只看技术栈，必须看证据链。",
    "feedback step 要进入 workflow，而不是事后附录。",
    "同一份样例应该能同时支持评估、推荐和复盘。"
  ],
  "collector": "recruiting-opc",
  "collected_at": "2026-04-05T11:45:00+08:00",
  "version": "1.0"
}
```

## 6. 可回流的规则
- 如果候选人没有上线证据，推荐等级自动降一级
- 如果没有评测和反馈记录，报告必须标注“证据不足”
- 如果无法说明 fallback / 兜底方案，进入终面前必须补问
- 如果人工修改集中在“证据链”，下次 prompt 要强制输出证据项
