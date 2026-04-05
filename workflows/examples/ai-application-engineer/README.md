# AI 应用工程师端到端样例链路

> 这组样例只覆盖 **AI 应用工程师**，不扩到其他岗位。
>
> 目标是补齐一条最小可用闭环：**JD 样本 → 简历样本 → 匹配评估 → 推荐报告 → feedback 回流记录**。

## 文件顺序

1. `jd.sample.json`：岗位 JD 样本，直接对齐 AI 应用工程师 JD schema
2. `resume.sample.md`：候选人简历样本，突出真实上线、评测和反馈闭环
3. `match-evaluation.sample.json`：基于 JD 和简历的匹配评估
4. `recommendation-report.sample.json`：进入推荐阶段的报告
5. `../../../feedback/reviews/ai-application-engineer/feedback-loop-sample.md`：人工修改 + 最终采用 + 回流记录

## 已补案例

- `case-01`：当前根目录下的原始样例，推荐通过
- `case-02`：客服 Copilot / 工单总结，推荐通过
- `case-03`：销售提案生成，失败样例
- `case-04`：内部流程自动化，推荐通过

## 这条链路想证明什么

- AI 应用工程师不是“会调模型 API”就够了
- 推荐判断必须看：业务场景、工程证据、评测方法、上线状态、fallback、反馈回流
- feedback step 不是附录，而是 workflow 的一部分

## 对应工作流

这套样例配合 `workflows/definitions/recruiting-jd-to-shortlist.yaml` 使用：
- JD 进入拆解
- 再做候选人匹配评估
- 再生成推荐报告
- 最后显式捕获反馈并回写

## 使用提示

- 这套样例只用于招聘链路的最小闭环验证
- 不要把它泛化成多岗位模板
- 不要把里面的业务场景扩成别的职业方向
- 新增案例集中放在 `cases/` 目录，便于横向比较
