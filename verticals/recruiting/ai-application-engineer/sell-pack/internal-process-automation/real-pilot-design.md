# 内部流程自动化真实试点设计

> 只围绕 **AI 应用工程师 -> 内部流程自动化**。这不是“通用工作流 demo”，而是一条可以直接进入 shadow mode 的真实试点设计。

## 1. 试点场景

### 场景名称
**采购申请预审与分流**

### 为什么先做这条流程
- 申请单重复、字段多、来回确认多
- 规则相对固定，适合先做 shadow mode
- 能清楚量化：处理时长、返工率、人工介入率、回写成功率
- 有明确的系统 of record，容易定义审计和回写边界

### 试点范围
- 只做一个入口：采购申请表单 / 审批单
- 只做一个系统 of record：OA 审批系统
- 只做一个主回写路径：OA 审批备注 / 任务流转
- 只做一个人工确认点：高风险字段与最终提交前复核
- 只做一个试点模式：shadow mode 起步，先不自动提交

## 2. system of record

### 业务真源头
- **OA 审批系统**：最终审批状态、责任人、单据流转的真源头
- **ERP 供应商主数据**：供应商信息、预算科目、基础校验的参考源
- **工单系统**：如果异常需要退回或升级，作为异常流转的记录点

### 试点控制台的角色
- 本地 UI 不是 system of record
- 本地 UI 只负责：录入试点输入、生成 AI 初稿、收集人审、生成回写包、留痕
- 真正的业务状态仍然以 OA / ERP 为准

## 3. 人审点

### 人审点 1：字段完整性确认
检查是否缺少：
- 申请金额
- 供应商名称
- 预算科目
- 申请部门
- 申请用途

### 人审点 2：高风险字段确认
必须人工确认：
- 金额
- 供应商
- 合同条款
- 审批结论
- 超预算或例外说明

### 人审点 3：最终提交前复核
确认：
- AI 初稿是否覆盖全部关键字段
- fallback 是否已经准备好
- 审计记录是否完整
- 是否允许回写到 OA

## 4. 回写路径

### 主路径
1. 用户在本地 UI 填入试点输入
2. AI 生成预审结果
3. 人工确认修改点
4. 保存试点证据
5. 生成反馈回写包
6. 写入 `feedback/reviews/ai-application-engineer/`
7. 后续可整理到 `data/direction-priority-db/` 作为方向优先级输入

### 业务回写
- 试点结果最终要回写到 OA 审批备注或任务流转记录
- 如果是 shadow mode，先只写备注，不自动改变审批状态
- 如果后续转小范围试点，再考虑和 OA / ERP API 对接

## 5. 失败时怎么兜底

- 低置信度：只出草稿，不自动提交
- 缺关键字段：退回补充，不进入回写
- 接口异常：保留草稿和审计记录
- 高风险字段：默认人工确认后才允许继续

## 6. 试点成功标准

至少要看到下面几项：
- 平均整理时长下降
- 人工来回确认次数下降
- 审计记录完整
- fallback 可用
- 业务方愿意把它当成可运营流程，而不是一次性 demo

## 7. 对应证据模板

建议按下面顺序留证据：
1. `pilot-evidence/pre-pilot-template.md`
2. `pilot-evidence/during-pilot-template.md`
3. `pilot-evidence/post-pilot-template.md`
4. `pilot-evidence/metrics-template.md`
5. `pilot-evidence/execution-checklist.md`

## 8. 对应的落地组件

- 本地 UI：`apps/internal-process-automation-pilot/`
- 客户沟通包：`sell-sheet.md` / `case-study.md` / `pricing-pilot.md`
- 风险边界：`risk-boundary.md`
- 反馈样本：`feedback/reviews/ai-application-engineer/`

## 9. 试点一句话

> 先用 shadow mode 把采购申请预审、人工确认、回写和审计跑通，再决定要不要扩到更多流程。
