# 内部流程自动化真实试点证据模板包

这组模板只服务 **AI 应用工程师 -> 内部流程自动化**，不扩到其他岗位，也不横向扩成通用试点管理模板。

## 这套模板解决什么

它解决的是“试点讲得动”和“试点证据留得下”之间的断层。

对内部流程自动化来说，真正要留下来的不是一句“试点成功了”，而是下面这些可复核证据：
- 试点前：为什么选这条流程、基线是多少、验收标准是什么
- 试点中：每次运行发生了什么、哪里触发人工介入、哪里走了 fallback
- 试点后：ROI、效率、错误率、人工介入率、审计覆盖、是否可以扩展

## 文件清单

- `pre-pilot-template.md`：试点前证据记录模板
- `during-pilot-template.md`：试点中运行证据模板
- `post-pilot-template.md`：试点后结果复盘模板
- `metrics-template.md`：核心指标定义与口径模板
- `execution-checklist.md`：试点执行说明与证据采集清单

## 推荐使用顺序

1. 先填 `pre-pilot-template.md`，把范围、基线、风险、验收条件定下来
2. 试点期间按批次或按天填 `during-pilot-template.md`
3. 试点结束后用 `post-pilot-template.md` 汇总结果
4. 计算指标时统一走 `metrics-template.md`
5. 执行前后都对照 `execution-checklist.md` 补齐证据

## 这套模板要留哪些证据

至少要留下：
- 输入样本或流程起点证据
- AI 初稿 / 自动输出
- 人工修改点
- fallback 触发点和原因
- 审计日志或留痕路径
- 最终提交结果
- 基线对比与试点结论

## 和现有闭环怎么接

这些模板不是孤立材料，而是可以直接接到现有闭环里：
- 试点前的范围和基线，可回填到推荐报告里的 `evaluation_plan` / `risk_analysis`
- 试点中的异常、人工介入和 fallback，可整理成 feedback 记录
- 试点后的 ROI 和复用价值，可写入 `feedback_case_map.roi_signal` / `reuse_score` / `should_deepen`
- 最终结论也可以继续落到 `feedback/reviews/ai-application-engineer/` 作为可复用样本

## 最小落库建议

如果要同步到 SQLite 方向优先级数据库，建议优先写这几个字段：
- `case_id`
- `direction_id`
- `success_failure`
- `failure_reason`
- `human_edits`
- `reuse_score`
- `roi_signal`
- `should_deepen`

## 使用原则

- 先做单流程小试点，不要一上来做多流程联动
- 先留证据，再谈扩展
- 先能复盘，再能规模化
- 试点失败也要留证据，因为失败样本同样能指导下一轮判断
