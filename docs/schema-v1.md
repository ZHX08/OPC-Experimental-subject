# 垂直行业 AI 知识库系统 Schema v1

## 1. 系统目标
把某个行业的知识、模板、案例、流程，变成可被 AI 稳定调用的生产系统。

核心能力：
1. 检索
2. 生成
3. 反馈回流
4. 持续优化

---

## 2. 四层结构

### 2.1 知识层
回答：AI 知道什么。

#### 基础知识库
- 行业术语
- 角色定义
- 标准流程
- 常见问题
- 风险边界
- 方法论

建议字段：
- `id`
- `title`
- `category`
- `tags`
- `content`
- `source`
- `applicable_scenarios`
- `confidence`
- `updated_at`

#### 案例知识库
- 成功案例
- 失败案例
- 典型问题
- 处理路径
- 结果与复盘

建议字段：
- `id`
- `name`
- `industry`
- `customer_type`
- `problem`
- `actions`
- `result`
- `lessons`
- `reusable`

#### 模板知识库
- 方案模板
- 报告模板
- 话术模板
- SOP 模板
- 表单模板
- Prompt 模板

建议字段：
- `id`
- `name`
- `scenario`
- `input_requirements`
- `output_format`
- `example`
- `version`

---

### 2.2 结构化数据层
回答：AI 应该按什么字段取数。

建议拆成：
- 客户画像表
- 任务定义表
- 标签表
- 风险规则表
- 输出规范表

典型字段：
- `customer_type`
- `company_size`
- `pain_points`
- `task_name`
- `required_inputs`
- `risk_level`
- `needs_human_review`

---

### 2.3 工作流层
回答：AI 怎么做事。

一个标准工作流包含：
- 触发条件
- 输入
- 检索范围
- 模板调用规则
- 输出要求
- 风险检查
- 人工确认点

标准结构：
```yaml
name: customer-demand-to-plan
trigger: 用户提交客户需求
inputs:
  - customer_profile
  - dialogue_history
  - business_goal
retrieve:
  - knowledge/base
  - knowledge/cases
  - templates/plans
steps:
  - extract_intent
  - classify_customer
  - retrieve_examples
  - draft_output
  - risk_check
  - final_format
outputs:
  - summary
  - detailed_plan
  - risk_notes
human_review: true
```

---

### 2.4 反馈层
回答：AI 如何越用越准。

每次使用后记录：
- 原始输入
- AI 输出
- 用户修改稿
- 最终稿
- 是否采用
- 结果评分
- 失败原因

建议字段：
- `task_type`
- `input_snapshot`
- `ai_output`
- `edited_output`
- `final_output`
- `accepted`
- `score`
- `failure_reason`
- `notes`

---

## 3. 最小闭环
1. 用户提交任务
2. 系统检索相关知识/案例/模板
3. AI 按工作流生成结果
4. 用户修改
5. 最终结果回流为知识资产

---

## 4. 第一版只做三件事
1. 智能检索问答
2. 高频任务生成器
3. 反馈回流

不做：
- 多行业大一统
- 超长链自治 Agent
- 复杂权限系统
- 花哨自动化

---

## 5. 推荐 MVP 切法
先选一个行业，再选一个任务。

示例：
- 猎头：JD 拆解 / 推荐报告生成
- 财税：客户咨询问答 / 资料清单生成
- 咨询：需求诊断 / 方案初稿生成
- 电商：客服问答 / 商品卖点生成

---

## 6. 护城河定义
真正的壁垒不是向量库本身，而是：

`公开模型 + 私有知识 + 结构化流程 + 业务反馈`

这四个组合起来，才是 OPC 能长期积累的生产系统。
