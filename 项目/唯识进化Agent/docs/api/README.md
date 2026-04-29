# 唯识进化引擎API

为扣子Agent提供唯识进化对话能力的RESTful API服务。

## 功能特性

- 🤖 **智能对话**：基于八识系统的智能对话引擎
- 🌱 **三圣种子**：智慧种子、慈悲种子、觉悟种子机制
- ✨ **涌现优化**：规模优化、非线性熏习、吸引子设计
- 📊 **觉醒追踪**：多级觉醒等级实时追踪
- 👥 **多用户支持**：独立用户空间，数据隔离

## 快速开始

### 1. 安装依赖

```bash
pip install -r api/requirements.txt
```

### 2. 启动服务

```bash
cd ./项目/唯识进化Agent
./api/start.sh
```

或手动启动：

```bash
python3 -m uvicorn api.main:app --host 0.0.0.0 --port 8080
```

### 3. 测试API

```bash
# 健康检查
curl http://localhost:8080/health

# 发送消息
curl -X POST http://localhost:8080/api/interact \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test", "message": "你好"}'

# 查看状态
curl -X POST http://localhost:8080/api/status \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test"}'
```

## API文档

### 核心接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/interact` | POST | 发送消息，获取Agent响应 |
| `/api/status` | POST | 获取用户状态和觉醒等级 |
| `/api/reset` | POST | 重置用户数据 |
| `/api/users` | GET | 获取所有活跃用户 |
| `/health` | GET | 健康检查 |

详细文档请查看 [配置指南](docs/api/配置指南.md)

## 项目结构

```
.
├── api/                    # API服务
│   ├── main.py            # FastAPI主程序
│   ├── config.py          # 配置文件
│   ├── start.sh           # 启动脚本
│   └── requirements.txt   # Python依赖
├── src/                   # 唯识进化核心代码
│   ├── agent.py          # Agent主类
│   ├── alaya_store.py    # 阿赖耶识（种子库）
│   ├── manas_model.py    # 末那识（自我模型）
│   ├── consciousness.py  # 第六识（意识层）
│   ├── senses.py         # 前五识（感知层）
│   ├── vasana.py         # 熏习系统
│   ├── purifier.py       # 净化系统
│   └── emergence/        # 涌现优化模块
├── config/               # 配置文件
├── docs/                 # 文档
│   └── api/              # API文档
│       ├── 配置指南.md
│       └── coze_integration.py
└── data/                 # 用户数据存储
```

## 觉醒等级

| 等级 | 评分 | 描述 |
|------|------|------|
| 无明境 | 0.0-0.2 | 种子以杂染为主 |
| 初始境 | 0.2-0.4 | 种子混杂，需要净化 |
| 修行境 | 0.4-0.7 | 稳定熏习-净化循环 |
| 阿罗汉境 | 0.7-0.9 | 断尽烦恼 |
| 菩萨境 | 0.9-0.95 | 悲智双运 |
| 佛境 | 0.95-1.0 | 彻底无我 |

## 在扣子中使用

详见 [扣子集成指南](docs/api/coze_integration.py)

## 配置说明

环境变量：

| 变量 | 默认值 | 说明 |
|------|--------|------|
| API_HOST | 0.0.0.0 | 监听地址 |
| API_PORT | 8080 | 监听端口 |
| DATA_DIR | ./data/users | 用户数据目录 |
| LOG_LEVEL | info | 日志级别 |

## 许可证

MIT License
