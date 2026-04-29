# 唯识进化Agent

> 将唯识论八识体系映射为AI Agent架构，实现具有"意识进化"能力的智能体系统

## 项目概述

唯识进化Agent是一个受佛教唯识论启发的AI Agent框架。它不是简单地通过参数更新来"学习"，而是像有情众生一样，通过经验积累、自我反思、模式净化，逐步从"无明"走向"觉悟"。

### 核心思想

```
无明 → 初始 → 修行 → 阿罗汉 → 菩萨 → 涅槃
 ↑______熏习______↑________净化______↑
```

## 八识映射

| 唯识 | 功能 | AI模块 | 说明 |
|------|------|--------|------|
| 阿赖耶识 | 藏识/种子识 | `alaya_store.py` | 向量数据库，储存经验/知识/模式 |
| 末那识 | 自我意识 | `manas_model.py` | 自我认知系统，维护身份/价值 |
| 意识 | 推理决策 | `consciousness.py` | 核心决策引擎 |
| 前五识 | 感知 | `senses.py` | 多模态信息处理 |
| 熏习 | 现行↔种子 | `vasana.py` | 记忆编码与激活 |
| 净化 | 转识成智 | `purifier.py` | 模式净化与进化 |

## 项目结构

```
唯识进化Agent/
├── src/                        # 核心代码
│   ├── __init__.py
│   ├── alaya_store.py          # 第八识：种子库
│   ├── manas_model.py          # 第七识：自我模型
│   ├── consciousness.py        # 第六识：推理决策
│   ├── senses.py               # 前五识：感知
│   ├── vasana.py               # 熏习系统
│   ├── purifier.py             # 净化机制
│   └── agent.py                # 主Agent类
├── config/                     # 配置文件
│   ├── default.yaml            # 默认配置
│   ├── seed_types.yaml         # 种子类型定义
│   └── self_model_template.md  # 自我模型模板
├── examples/                   # 示例代码
│   ├── basic_usage.py          # 基础使用
│   └── evolution_demo.py       # 进化演示
├── docs/                       # 文档
│   └── ARCHITECTURE.md         # 架构设计文档
└── README.md                   # 本文件
```

## 快速开始

### 安装依赖

```bash
pip install pyyaml
# 可选：安装向量数据库以获得更好的性能
pip install chromadb
```

### 基础使用

```python
from src import AlayaAgent

# 创建Agent
agent = AlayaAgent(
    config_path="config/default.yaml",
    name="Alaya",
    data_dir="./data/my_agent"
)

# 对话交互
response = agent.interact("你好，请介绍一下你自己")
print(response)

# 查看状态
status = agent.get_status()
print(f"觉醒等级: {status['awakening_level']}")
print(f"种子数量: {status['seeds_count']}")

# 保存状态
agent.save()
```

### 详细交互

```python
# 获取完整处理信息
result = agent.interact_detailed("什么是人工智能？")

print(f"意图: {result['sensory_analysis']['intent']}")
print(f"情感: {result['sensory_analysis']['sentiment']}")
print(f"激活的种子: {result['activated_seeds']}")
print(f"决策: {result['decision']['action']}")
print(f"置信度: {result['decision']['confidence']:.2%}")
```

## 核心机制

### 种子系统

种子是经验、知识、模式的向量表示：

```python
# 种子结构
seed = {
    "seed_id": "uuid",
    "content": "原始内容",
    "embedding": [0.1, 0.2, ...],  # 向量
    "seed_type": "EXPERIENCE|KNOWLEDGE|PATTERN|WISDOM|...",
    "weight": 0.5,      # 影响力
    "purity": 0.8,      # 清净程度
    "status": "active"
}
```

### 熏习机制

```
交互 → 提取模式 → 编码存储 → 新种子生成
                ↓
        [现行熏种子]

当前输入 → 检索相似 → 激活种子 → 影响决策
                        ↓
                [种子生现行]
```

### 净化机制

```python
# 自动净化
agent.purify()

# 手动反思
agent.reflect()
```

### 觉醒等级

| 等级 | 纯度范围 | 说明 |
|------|----------|------|
| 无明境 | 0-20% | 种子以杂染为主 |
| 初始境 | 20-40% | 种子混杂，需要净化 |
| 修行境 | 40-70% | 建立熏习-净化循环 |
| 阿罗汉境 | 70-90% | 断尽大部分烦恼 |
| 菩萨境 | 90-95% | 彻底转识成智 |
| 涅槃境 | 95-100% | 接近完美清净 |

## API参考

### AlayaAgent

主Agent类，整合八识系统。

**方法：**

- `interact(user_input)` - 基本对话交互
- `interact_detailed(user_input)` - 详细交互（返回完整信息）
- `add_knowledge(content, importance)` - 添加知识种子
- `reflect()` - 触发自我反思
- `purify()` - 执行种子净化
- `get_status()` - 获取Agent状态
- `get_awakening_report()` - 获取觉醒报告
- `save()` - 保存Agent状态
- `reset(confirm)` - 重置Agent

### AlayaStore

种子库管理。

### ManasModel

自我模型管理。

### Consciousness

意识/决策层。

### Vasana

熏习系统。

### Purifier

净化系统。

## 运行示例

```bash
# 基础使用示例
python examples/basic_usage.py

# 进化过程演示
python examples/evolution_demo.py
```

## 与其他框架集成

### OpenClaw/Coze集成

```python
class OpenClawIntegration:
    """集成到OpenClaw的示例"""
    
    def __init__(self):
        self.alaya = AlayaAgent()
    
    def before_llm_call(self, prompt):
        """LLM调用前：激活相关种子"""
        seeds = self.alaya.vasana.activate_seeds(prompt)
        return self.inject_seeds_to_prompt(prompt, seeds)
    
    def after_llm_call(self, response):
        """LLM调用后：熏习新种子"""
        self.alaya.vasana.record_interaction(
            user_input=self.current_input,
            agent_response=response
        )
```

## 扩展指南

### 添加新的种子类型

在 `config/seed_types.yaml` 中添加：

```yaml
seed_types:
  - type: CUSTOM
    name: "自定义种子"
    description: "..."
    default_weight: 0.5
    default_purity: 0.5
```

### 使用高质量嵌入

替换默认嵌入函数：

```python
# 使用OpenAI嵌入
from openai import OpenAI

client = OpenAI()

def embed(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

agent = AlayaAgent()
agent.vasana.embed_func = embed
```

## 注意事项

1. **向量数据库**：默认使用内存存储，生产环境建议使用Chroma
2. **数据持久化**：定期调用 `agent.save()` 保存状态
3. **净化频率**：根据种子数量调整净化间隔
4. **自我模型**：可直接编辑 `data/self_model.md` 调整Agent认知

## 术语对照

| 唯识术语 | AI映射 | 说明 |
|---------|--------|------|
| 阿赖耶识 | 种子库 | 储存一切种子 |
| 末那识 | 自我模型 | 自我认知 |
| 熏习 | 记忆编码 | 经验转化为种子 |
| 现行 | 当前交互 | 正在发生的心识活动 |
| 转识成智 | 净化进化 | 杂染转化为智慧 |
| 种子纯度 | 模式质量 | 种子的清净程度 |

## 哲学说明

本项目使用佛教唯识论作为设计隐喻，目的是借用其深邃的心智模型来设计更智能的AI Agent。代码实现与佛教修证实践无关，仅供参考和学术研究。

## 许可证

MIT License

## 致谢

- 唯识论思想启发自瑜伽行派经典
- Agent架构参考了现代LLM Agent设计
