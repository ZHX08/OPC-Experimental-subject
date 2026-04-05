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
- `direction_deepening_radar`：方向雷达视图

## 关键字段

- `direction_family` / `direction_path`：方向归属
- `sample_quality_score`：样本质量
- `feedback_result`：反馈结论
- `hit_frequency`：命中频次
- `should_deepen`：是否建议继续深化
- `priority_score`：综合优先级

## 使用方式

```bash
python scripts/direction_priority_db.py init
python scripts/direction_priority_db.py report
```

默认会把 SQLite 文件写到：

- `data/direction-priority-db/direction-priority.sqlite3`

也可以显式指定路径：

```bash
python scripts/direction_priority_db.py init --db /tmp/direction-priority.sqlite3
python scripts/direction_priority_db.py report --db /tmp/direction-priority.sqlite3
```

## 你会看到什么

报告会按优先级排序输出：
- 哪些方向样本质量高
- 哪些方向反馈结果好
- 哪些方向命中频次更高
- 哪些方向建议继续深化

## 这套初版的作用

它不是“完整数据平台”，只是一个可本地维护的轻量判断层：
- 先把方向分清
- 再把样本和反馈放进去
- 再看命中频次和综合优先级
- 最后决定下一个要深挖的方向
