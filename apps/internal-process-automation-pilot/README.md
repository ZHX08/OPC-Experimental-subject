# 内部流程自动化试点控制台

这是 `AI 应用工程师 -> 内部流程自动化` 的第一版本地 UI。

## 这页能做什么

- 录入试点输入
- 一键运行试点评估
- 看到运行结果、缺口、风险和人审点
- 填人工确认
- 填反馈回写字段
- 填试点证据记录
- 保存本地回写包，供后续写入知识库 / feedback / SQLite 方向库

## 默认试点场景

- 场景：采购申请预审与分流
- system of record：OA 审批系统
- 次级系统：ERP 供应商主数据 / 工单系统
- 人审点：高风险字段确认 + 最终提交前复核
- 写回目标：OA 审批备注 + 试点证据回流包

## 启动方式

在仓库根目录运行：

```bash
python apps/internal-process-automation-pilot/server.py --port 8000
```

然后打开：

```text
http://127.0.0.1:8000
```

## 保存后会写到哪里

- 运行记录：`apps/internal-process-automation-pilot/data/runtime/`
- 反馈回写包：`feedback/reviews/ai-application-engineer/`
- 运行历史：`apps/internal-process-automation-pilot/data/runtime/runs.jsonl`

## 试点设计对应关系

这个 UI 直接对应：

- `verticals/recruiting/ai-application-engineer/sell-pack/internal-process-automation/real-pilot-design.md`
- `verticals/recruiting/ai-application-engineer/sell-pack/internal-process-automation/pilot-evidence/`
- `knowledge/cases/ai-application-engineer/internal-process-automation/pilot-design.md`

## 使用建议

先按下面顺序跑一遍：

1. 点“填入样例”
2. 点“运行试点评估”
3. 看缺字段、风险和写回路径
4. 填人工确认
5. 填 feedback 回写字段
6. 点“保存试点证据”

## 说明

这不是生产系统，只是第一版试点控制台。它的任务是把试点设计和证据记录跑通，而不是把 OA / ERP 真接上。
