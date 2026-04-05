INSERT INTO direction_catalog (direction_id, direction_family, direction_name, direction_path, description, status, created_at, updated_at) VALUES
  ('dir-aie-knowledge', 'AI 应用工程师', '企业内部知识工作台', 'AI 应用工程师/企业内部知识工作台', '面向销售、客服和运营的内部知识检索与问答方向。', 'active', '2026-04-05T12:00:00+08:00', '2026-04-05T12:00:00+08:00'),
  ('dir-aie-support', 'AI 应用工程师', '客服 Copilot', 'AI 应用工程师/客服 Copilot', '面向售后客服、工单处理和回复建议的方向。', 'active', '2026-04-05T12:00:00+08:00', '2026-04-05T12:00:00+08:00'),
  ('dir-aie-sales', 'AI 应用工程师', '销售提案生成', 'AI 应用工程师/销售提案生成', '面向销售提案草稿、产品对比和下一步计划生成的方向。', 'active', '2026-04-05T12:00:00+08:00', '2026-04-05T12:00:00+08:00'),
  ('dir-aie-workflow', 'AI 应用工程师', '内部流程自动化', 'AI 应用工程师/内部流程自动化', '面向采购、法务、审批和内部流转自动化的方向。', 'active', '2026-04-05T12:00:00+08:00', '2026-04-05T12:00:00+08:00');

INSERT INTO sample_case (case_id, direction_id, case_code, case_title, case_status, sample_quality_score, feedback_result, hit_frequency, should_deepen, source_path, notes, created_at, updated_at) VALUES
  ('case-01', 'dir-aie-knowledge', 'case-01-enterprise-knowledge', '企业内部知识工作台', 'success', 8.4, 'passed', 12, 1, 'workflows/examples/ai-application-engineer/jd.sample.json', '根目录原始样例。', '2026-04-05T12:00:00+08:00', '2026-04-05T12:00:00+08:00'),
  ('case-02', 'dir-aie-support', 'case-02-support-copilot', '客服 Copilot / 工单总结', 'success', 8.7, 'passed', 9, 1, 'workflows/examples/ai-application-engineer/cases/case-02-support-copilot-success/', '覆盖客服与售后场景。', '2026-04-05T12:00:00+08:00', '2026-04-05T12:00:00+08:00'),
  ('case-03', 'dir-aie-sales', 'case-03-sales-proposal', '销售提案生成', 'failure', 5.3, 'rejected', 2, 0, 'workflows/examples/ai-application-engineer/cases/case-03-sales-proposal-failure/', '典型不推荐样例。', '2026-04-05T12:00:00+08:00', '2026-04-05T12:00:00+08:00'),
  ('case-04', 'dir-aie-workflow', 'case-04-internal-workflow', '内部流程自动化', 'success', 9.0, 'passed', 7, 1, 'workflows/examples/ai-application-engineer/cases/case-04-internal-workflow-success/', '系统集成和审批流方向。', '2026-04-05T12:00:00+08:00', '2026-04-05T12:00:00+08:00');

INSERT INTO case_asset (asset_id, case_id, asset_type, asset_path, asset_quality_score, accepted, created_at) VALUES
  ('asset-01-jd', 'case-01', 'jd', 'workflows/examples/ai-application-engineer/jd.sample.json', 8.4, 1, '2026-04-05T12:00:00+08:00'),
  ('asset-01-resume', 'case-01', 'resume', 'workflows/examples/ai-application-engineer/resume.sample.md', 8.4, 1, '2026-04-05T12:00:00+08:00'),
  ('asset-01-match', 'case-01', 'match', 'workflows/examples/ai-application-engineer/match-evaluation.sample.json', 8.4, 1, '2026-04-05T12:00:00+08:00'),
  ('asset-01-report', 'case-01', 'report', 'workflows/examples/ai-application-engineer/recommendation-report.sample.json', 8.4, 1, '2026-04-05T12:00:00+08:00'),
  ('asset-01-feedback', 'case-01', 'feedback', 'feedback/reviews/ai-application-engineer/feedback-loop-sample.md', 8.4, 1, '2026-04-05T12:00:00+08:00'),
  ('asset-02-jd', 'case-02', 'jd', 'workflows/examples/ai-application-engineer/cases/case-02-support-copilot-success/jd.sample.json', 8.7, 1, '2026-04-05T12:00:00+08:00'),
  ('asset-02-resume', 'case-02', 'resume', 'workflows/examples/ai-application-engineer/cases/case-02-support-copilot-success/resume.sample.md', 8.7, 1, '2026-04-05T12:00:00+08:00'),
  ('asset-02-match', 'case-02', 'match', 'workflows/examples/ai-application-engineer/cases/case-02-support-copilot-success/match-evaluation.sample.json', 8.7, 1, '2026-04-05T12:00:00+08:00'),
  ('asset-02-report', 'case-02', 'report', 'workflows/examples/ai-application-engineer/cases/case-02-support-copilot-success/recommendation-report.sample.json', 8.7, 1, '2026-04-05T12:00:00+08:00'),
  ('asset-02-feedback', 'case-02', 'feedback', 'feedback/reviews/ai-application-engineer/feedback-case-02-support-copilot-success.md', 8.7, 1, '2026-04-05T12:00:00+08:00'),
  ('asset-03-jd', 'case-03', 'jd', 'workflows/examples/ai-application-engineer/cases/case-03-sales-proposal-failure/jd.sample.json', 5.3, 0, '2026-04-05T12:00:00+08:00'),
  ('asset-03-resume', 'case-03', 'resume', 'workflows/examples/ai-application-engineer/cases/case-03-sales-proposal-failure/resume.sample.md', 5.3, 0, '2026-04-05T12:00:00+08:00'),
  ('asset-03-match', 'case-03', 'match', 'workflows/examples/ai-application-engineer/cases/case-03-sales-proposal-failure/match-evaluation.sample.json', 5.3, 0, '2026-04-05T12:00:00+08:00'),
  ('asset-03-report', 'case-03', 'report', 'workflows/examples/ai-application-engineer/cases/case-03-sales-proposal-failure/recommendation-report.sample.json', 5.3, 0, '2026-04-05T12:00:00+08:00'),
  ('asset-03-feedback', 'case-03', 'feedback', 'feedback/reviews/ai-application-engineer/feedback-case-03-sales-proposal-failure.md', 5.3, 0, '2026-04-05T12:00:00+08:00'),
  ('asset-04-jd', 'case-04', 'jd', 'workflows/examples/ai-application-engineer/cases/case-04-internal-workflow-success/jd.sample.json', 9.0, 1, '2026-04-05T12:00:00+08:00'),
  ('asset-04-resume', 'case-04', 'resume', 'workflows/examples/ai-application-engineer/cases/case-04-internal-workflow-success/resume.sample.md', 9.0, 1, '2026-04-05T12:00:00+08:00'),
  ('asset-04-match', 'case-04', 'match', 'workflows/examples/ai-application-engineer/cases/case-04-internal-workflow-success/match-evaluation.sample.json', 9.0, 1, '2026-04-05T12:00:00+08:00'),
  ('asset-04-report', 'case-04', 'report', 'workflows/examples/ai-application-engineer/cases/case-04-internal-workflow-success/recommendation-report.sample.json', 9.0, 1, '2026-04-05T12:00:00+08:00'),
  ('asset-04-feedback', 'case-04', 'feedback', 'feedback/reviews/ai-application-engineer/feedback-case-04-internal-workflow-success.md', 9.0, 1, '2026-04-05T12:00:00+08:00');

INSERT INTO direction_hit_log (hit_id, direction_id, case_id, hit_source, hit_count, query_text, recorded_at, notes) VALUES
  ('hit-01', 'dir-aie-knowledge', 'case-01', 'workflow_examples', 12, '企业内部知识工作台 / AI 应用工程师', '2026-04-05T12:00:00+08:00', '知识工作台样本被多次引用。'),
  ('hit-02', 'dir-aie-support', 'case-02', 'workflow_examples', 9, '客服 Copilot / AI 应用工程师', '2026-04-05T12:00:00+08:00', '客服场景受到较高关注。'),
  ('hit-03', 'dir-aie-sales', 'case-03', 'workflow_examples', 2, '销售提案生成 / AI 应用工程师', '2026-04-05T12:00:00+08:00', '作为失败对照样例保留。'),
  ('hit-04', 'dir-aie-workflow', 'case-04', 'workflow_examples', 7, '内部流程自动化 / AI 应用工程师', '2026-04-05T12:00:00+08:00', '流程自动化方向被稳定引用。');

INSERT INTO direction_review (review_id, direction_id, review_date, sample_quality_avg, feedback_result, hit_frequency, should_deepen, priority_score, reason, next_action, created_at) VALUES
  ('review-01', 'dir-aie-knowledge', '2026-04-05', 8.4, 'passed', 12, 1, 8.6, '知识工作台方向样本质量高，反馈通过率高，命中频次也高。', '继续补真实知识库、RAG 和 fallback 的案例。', '2026-04-05T12:00:00+08:00'),
  ('review-02', 'dir-aie-support', '2026-04-05', 8.7, 'passed', 9, 1, 8.8, '客服 Copilot 方向证据链完整，且和真实业务协作场景贴合。', '继续补客服升级、监控和告警样本。', '2026-04-05T12:00:00+08:00'),
  ('review-03', 'dir-aie-sales', '2026-04-05', 5.3, 'rejected', 2, 0, 4.9, '销售提案方向更容易混淆 prompt 能力与工程能力，暂不建议优先深化。', '保留失败样例，等待更多生产证据再决定。', '2026-04-05T12:00:00+08:00'),
  ('review-04', 'dir-aie-workflow', '2026-04-05', 9.0, 'passed', 7, 1, 9.1, '内部流程自动化方向工程证据强，适合继续作为重点方向。', '继续补 ERP / OA / 审批流的集成案例。', '2026-04-05T12:00:00+08:00');

INSERT INTO feedback_case_map (feedback_id, case_id, direction_id, task_type, workflow_stage, success_failure, failure_reason, human_edits, reuse_score, roi_signal, should_deepen, linked_jd_id, linked_candidate_id, linked_report_id, source_path, recorded_at, notes) VALUES
  ('fb-aie-20260405-001', 'case-01', 'dir-aie-knowledge', 'ai_application_engineer_recommendation', 'recommendation_report', 'success', '', '把技术匹配改成证据链匹配，补上线规模、成本边界和 fallback。', 0.82, '内部知识检索提效', 1, 'jd-aie-20260405-001', 'cand-zhang-cheng-001', 'rep-aie-20260405-001', 'feedback/reviews/ai-application-engineer/feedback-loop-sample.md', '2026-04-05T11:45:00+08:00', '知识工作台样本说明证据链的重要性。'),
  ('fb-aie-20260405-002', 'case-02', 'dir-aie-support', 'ai_application_engineer_recommendation', 'recommendation_report', 'success', '', '补高风险工单升级、监控告警和 SLA 约束，而不是只看技术栈。', 0.79, '客服工单提效', 1, 'jd-aie-20260405-002', 'cand-wang-qi-002', 'rep-aie-20260405-002', 'feedback/reviews/ai-application-engineer/feedback-case-02-support-copilot-success.md', '2026-04-05T11:46:00+08:00', '客服场景强调升级流转和 fallback。'),
  ('fb-aie-20260405-003', 'case-03', 'dir-aie-sales', 'ai_application_engineer_recommendation', 'recommendation_report', 'failure', '缺少上线、工程实现和评测闭环证据。', '把 prompt 能力与工程能力拆开，不能把提案文案当成 AI 应用工程。', 0.28, '不宜作为内部流程自动化样板', 0, 'jd-aie-20260405-003', 'cand-chen-che-003', 'rep-aie-20260405-003', 'feedback/reviews/ai-application-engineer/feedback-case-03-sales-proposal-failure.md', '2026-04-05T11:47:00+08:00', '失败样例提醒要区分内容能力和工程能力。'),
  ('fb-aie-20260405-004', 'case-04', 'dir-aie-workflow', 'ai_application_engineer_recommendation', 'recommendation_report', 'success', '', '强化审计、回滚、监控和可运营证据，把 workflow 说成可上线系统。', 0.91, '审批和流转时间下降', 1, 'jd-aie-20260405-004', 'cand-liu-ming-004', 'rep-aie-20260405-004', 'feedback/reviews/ai-application-engineer/feedback-case-04-internal-workflow-success.md', '2026-04-05T11:48:00+08:00', '内部流程自动化是当前最强可卖样板。');
