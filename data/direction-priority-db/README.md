# Direction Priority DB

这是一个本地 SQLite 方案，用来判断 **哪些方向应该继续深化**。

## 目标

把“方向是否值得继续加码”从口头判断，变成能落库、能检索、能统计的本地数据。

## 适用范围

当前初版只围绕 **AI 应用工程师** 的几个纵向方向：
- 企业内部知识工作台
- 客服 Copilot
- 销售提案生成
- 内部流程自动化

## 数据表

- `direction_catalog`：方向目录
- `sample_case`：案例级样本
- `case_asset`：案例文件映射
- `direction_hit_log`：命中/检索频次明细
- `direction_review`：方向级复盘与是否建议深化
- `feedback_case_map`：反馈记录与案例 / 方向的映射
- `direction_deepening_radar`：方向雷达视图，已带入反馈闭环摘要
- `case_feedback_bridge`：单条反馈的明细桥接视图

## 关键字段

- `direction_family` / `direction_path`：方向归属
- `sample_quality_score`：样本质量
- `feedback_result`：反馈结论
- `hit_frequency`：命中频次
- `should_deepen`：是否建议继续深化
- `priority_score`：综合优先级
- `reuse_score`：反馈复用价值
- `roi_signal`：反馈对应的价值信号

## 试点证据接入

对于 **AI 应用工程师 / 内部流程自动化**，新的试点证据模板可以作为 `feedback_case_map` 的上游输入：

- 试点前基线与验收标准 → 帮助确认 `roi_signal` 是否可信
- 试点中人工介入 / fallback / 审计日志 → 帮助写清 `failure_reason` / `human_edits`
- 试点后 ROI / 效率 / 错误率 / 扩展判断 → 帮助计算 `reuse_score` 和 `should_deepen`

也就是说，这套模板不是单独存档，而是为了让方向优先级数据库更容易判断“值不值得继续加码”。

## 使用方式

```bash
python scripts/direction_priority_db.py init
python scripts/direction_priority_db.py report
python scripts/direction_priority_db.py feedback
```

默认会把 SQLite 文件写到：

- `data/direction-priority-db/direction-priority.sqlite3`

也可以显式指定路径：

```bash
python scripts/direction_priority_db.py init --db /tmp/direction-priority.sqlite3
python scripts/direction_priority_db.py report --db /tmp/direction-priority.sqlite3
python scripts/direction_priority_db.py feedback --db /tmp/direction-priority.sqlite3
```

## 你会看到什么

`report` 会按优先级输出：
- 哪些方向样本质量高
- 哪些方向反馈结果好
- 哪些方向命中频次更高
- 哪些方向的反馈复用价值更高
- 哪些方向建议继续深化

`feedback` 会输出：
- case_id / direction_id / success_failure 映射
- failure_reason / human_edits
- reuse_score / roi_signal / should_deepen

## 这套初版的作用

它不是“完整数据平台”，只是一个可本地维护的轻量判断层：
- 先把方向分清
- 再把样本和反馈放进去
- 再看命中频次、复用价值和综合优先级
- 最后决定下一个要深挖的方向
