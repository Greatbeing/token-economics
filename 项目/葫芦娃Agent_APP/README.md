# 葫芦娃 Agent APP

> 你的圣哲思维教练 - 整合东西方圣哲智慧，帮助你在真实场景中练习思维成长。

## 项目概述

葫芦娃是一个基于扣子(Coze)平台开发的AI Agent，核心能力包括：
- 🤝 **圣哲思维匹配**：根据问题智能匹配最适合的圣哲视角
- 🎯 **思维练习系统**：在真实场景中练习圣哲思维
- 🌱 **种子追踪成长**：记录思维种子，追踪觉醒等级
- 📊 **成长报告**：可视化展示思维成长历程

## 核心功能

### 1. 圣哲思维模型库
整合9大圣哲思维：
- 孔子·仁学思维
- 庄子·逍遥思维
- 老子·无为思维
- 佛陀·四谛思维
- 孟子·心性思维
- 王阳明·心学思维
- 苏格拉底·产婆术
- 亚里士多德·实践智慧
- 鬼谷子·权衡思维

### 2. 觉醒等级体系
| 等级 | 名称 | 描述 |
|------|------|------|
| L1 | 迷途者 | 遇到问题习惯焦虑 |
| L2 | 觉醒者 | 开始用圣哲思维思考 |
| L3 | 修行者 | 能运用多种思维框架 |
| L4 | 明智者 | 思维灵活，快速匹配 |
| L5 | 圣哲境 | 内化为本能，智慧涌现 |

### 3. 种子系统
每完成一次练习，根据得分获得种子。种子积累触发智慧涌现，等级提升。

## 项目结构

```
./项目/葫芦娃Agent_APP/
├── docs/                          # 文档目录
│   ├── 产品定位.md                 # 产品定位文档
│   ├── Agent人设.md                # Agent人设设计
│   ├── 对话流程.md                 # 对话流程设计
│   ├── 技能整合方案.md             # 技能整合方案
│   └── 扣子平台配置指南.md         # 扣子平台配置
├── src/                           # 源代码目录
│   ├── main.py                    # 主入口模块
│   ├── sage_matcher.py            # 圣哲思维匹配器
│   ├── practice_generator.py     # 练习题生成器
│   ├── seed_tracker.py            # 种子追踪器
│   └── awakening_display.py       # 觉醒展示器
├── prompts/                       # 提示词目录
│   └── coze_system_prompt.md      # 扣子系统提示词
└── README.md                      # 项目说明

```

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 测试运行
```bash
cd src
python main.py
```

### 3. 扣子平台部署
1. 在扣子平台创建新Bot
2. 导入Agent人设和提示词
3. 配置知识库
4. 发布到飞书/微信

详见 [扣子平台配置指南](./docs/扣子平台配置指南.md)

## 核心模块说明

### SageMatcher - 圣哲思维匹配器
```python
from sage_matcher import SageMatcher

matcher = SageMatcher()
result = matcher.match_thought("室友总是影响我，很生气")
# 返回：{'model': '仁学思维', 'sage': '孔子', 'confidence': 0.85, ...}
```

### PracticeGenerator - 练习题生成器
```python
from practice_generator import generate_practice

practice = generate_practice("仁学思维")
# 返回练习题，包含场景和问题列表
```

### SeedTracker - 种子追踪器
```python
from seed_tracker import SeedTracker

tracker = SeedTracker("user_123")
tracker.add_seed("仁学思维")  # 添加种子
tracker.get_status()  # 获取状态
```

### AwakeningDisplay - 觉醒展示器
```python
from awakening_display import AwakeningDisplay

display = AwakeningDisplay(tracker)
print(display.display_full_report())  # 生成成长报告
```

## 整合资源

本项目整合了以下现有项目：
- **圣哲思维引擎**：提供思维模型库和练习题
- **唯识进化Agent**：提供种子追踪和等级进化机制
- **80万字圣哲知识库**：提供圣哲知识支持

详见 [技能整合方案](./docs/技能整合方案.md)

## 设计原则

1. **不说教，用引导代替告诉**
2. **每次都给出具体练习**
3. **记录成长，追踪觉醒**
4. **用鼓励代替批评**

## 联系方式

如有问题或建议，请联系开发团队。

---

🌿 葫芦娃 - 你的圣哲思维教练
