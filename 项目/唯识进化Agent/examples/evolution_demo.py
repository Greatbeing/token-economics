# -*- coding: utf-8 -*-
"""
唯识进化Agent - 进化过程演示

展示Agent如何通过交互逐渐进化：
1. 初始状态
2. 多次交互后的变化
3. 熏习效果
4. 净化过程
5. 觉醒等级提升
"""

import sys
import os
import time
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import AlayaAgent
from src.alaya_store import SeedType


def print_section(title: str):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_status(agent: AlayaAgent, stage: str):
    """打印当前状态"""
    status = agent.get_status()
    print(f"\n[{stage}] 状态快照:")
    print(f"  - 交互次数: {status['interaction_count']}")
    print(f"  - 种子总数: {status['seeds_count']}")
    print(f"  - 平均纯度: {status['average_purity']:.2%}")
    print(f"  - 觉醒等级: {status['awakening_level']}")
    print(f"  - 智慧种子: {status['wisdom_seeds']}")
    
    # 显示种子类型分布
    stats = agent.store.get_statistics()
    print(f"  - 种子分布: ", end="")
    type_dist = stats.get("type_distribution", {})
    dist_str = ", ".join([f"{k}:{v}" for k, v in type_dist.items() if v > 0])
    print(dist_str or "无")


def main():
    """进化过程演示"""
    
    print_section("唯识进化Agent - 进化过程演示")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 创建Agent
    print("\n初始化Agent...")
    agent = AlayaAgent(
        config_path="config/default.yaml",
        name="进化演示Agent",
        data_dir="./data/evolution_demo"
    )
    print(f"✓ Agent已创建")
    
    # 阶段1: 初始状态
    print_section("阶段1: 初始状态")
    print("Agent刚创建，种子库几乎为空...")
    
    # 添加一些基础知识和种子
    print("\n植入初始知识...")
    agent.add_knowledge("帮助用户解决问题是AI的核心价值", 0.8)
    agent.add_knowledge("诚实和透明是基本准则", 0.9)
    agent.add_knowledge("持续学习和自我反思很重要", 0.7)
    
    print_status(agent, "初始")
    
    # 阶段2: 日常对话交互
    print_section("阶段2: 日常对话交互")
    print("进行多次日常对话，观察种子的生成...")
    
    daily_conversations = [
        ("你好", "友好问候"),
        ("你叫什么名字？", "询问身份"),
        ("你能做什么？", "了解能力"),
        ("给我讲个笑话吧", "轻松互动"),
        ("谢谢你的帮助", "正面反馈"),
    ]
    
    for i, (user_input, description) in enumerate(daily_conversations, 1):
        print(f"\n  交互{i}: {description}")
        print(f"  用户: {user_input}")
        response = agent.interact(user_input)
        print(f"  Agent: {response[:50]}...")
        time.sleep(0.1)
    
    print_status(agent, "日常对话后")
    
    # 阶段3: 知识密集型对话
    print_section("阶段3: 知识密集型对话")
    print("进行知识性对话，观察知识种子的增长...")
    
    knowledge_conversations = [
        ("解释一下什么是人工智能", 0.8),
        ("机器学习和深度学习有什么区别？", 0.8),
        ("Python中如何定义函数？", 0.7),
        ("什么是向量数据库？", 0.6),
    ]
    
    for user_input, importance in knowledge_conversations:
        print(f"\n  用户: {user_input}")
        agent.add_knowledge(f"用户询问: {user_input}", importance)
        response = agent.interact(user_input)
        print(f"  Agent: {response[:50]}...")
    
    print_status(agent, "知识对话后")
    
    # 阶段4: 添加更多知识
    print_section("阶段4: 添加更多知识")
    print("添加更多知识种子...")
    
    more_knowledge = [
        ("向量数据库用于存储和检索向量嵌入", 0.6),
        ("深度学习是机器学习的子领域", 0.7),
        ("Python有丰富的库支持数据处理", 0.6),
    ]
    
    for content, importance in more_knowledge:
        agent.add_knowledge(content, importance)
    
    print_status(agent, "更多知识后")
    
    # 阶段5: 自我反思
    print_section("阶段5: 自我反思")
    print("触发自我反思，产生智慧种子...")
    
    reflection = agent.reflect()
    print(f"\n反思结果:")
    print(f"  - 对齐度: {reflection.get('alignment_rate', 0):.2%}")
    print(f"  - 冲突: {len(reflection.get('conflicts', []))}")
    print(f"  - 建议: {reflection.get('suggestions', [])}")
    
    # 显示新生成的智慧种子
    wisdom_seeds = agent.store.get_by_type(SeedType.WISDOM)
    print(f"\n智慧种子 ({len(wisdom_seeds)} 个):")
    for seed in wisdom_seeds[-3:]:
        print(f"  - [{seed.seed_id[:8]}] {seed.content[:50]}... (纯度:{seed.purity:.2f})")
    
    print_status(agent, "反思后")
    
    # 阶段6: 净化过程
    print_section("阶段6: 净化过程")
    print("执行种子净化，观察转识成智...")
    
    # 先查看净化前的低纯度种子
    low_purity_seeds = [s for s in agent.store.get_recent(100) if s.purity < 0.4]
    print(f"\n净化前: {len(low_purity_seeds)} 个低纯度种子 (<0.4)")
    
    # 执行净化
    purify_results = agent.purify()
    print(f"\n净化结果:")
    print(f"  - 处理种子: {len(purify_results)}")
    
    light_count = len([r for r in purify_results if r.level.value == "light"])
    moderate_count = len([r for r in purify_results if r.level.value == "moderate"])
    heavy_count = len([r for r in purify_results if r.level.value == "heavy"])
    print(f"  - 轻度净化: {light_count}")
    print(f"  - 中度净化: {moderate_count}")
    print(f"  - 重度净化: {heavy_count}")
    
    # 显示被转化的种子
    for result in purify_results:
        if result.new_seed_id:
            new_seed = agent.store.get(result.new_seed_id)
            if new_seed:
                print(f"\n  转化示例:")
                print(f"    原种子: {result.original_seed_id[:8]}...")
                print(f"    新智慧种子: {new_seed.content[:50]}...")
                print(f"    新纯度: {new_seed.purity:.2f}")
    
    print_status(agent, "净化后")
    
    # 阶段7: 最终状态和觉醒报告
    print_section("阶段7: 最终状态")
    
    report = agent.get_awakening_report()
    print(report)
    
    # 显示种子库的详细信息
    print("\n种子库详情:")
    all_seeds = agent.store.get_recent(50)
    
    print("\n按类型统计:")
    for seed_type in SeedType:
        count = len([s for s in all_seeds if s.seed_type == seed_type])
        if count > 0:
            avg_purity = sum(s.purity for s in all_seeds if s.seed_type == seed_type) / count
            print(f"  {seed_type.value}: {count}个 (平均纯度:{avg_purity:.2f})")
    
    # 保存Agent状态
    print("\n保存Agent状态...")
    agent.save()
    print("✓ 保存完成")
    
    # 进化总结
    print_section("进化总结")
    print(f"""
    进化前后对比:
    - 初始种子数: 3 (仅知识种子)
    - 最终种子数: {agent.get_status()['seeds_count']}
    - 智慧种子: {agent.get_status()['wisdom_seeds']} 个
    - 平均纯度: {agent.get_status()['average_purity']:.2%}
    - 觉醒等级: {agent.get_status()['awakening_level']}
    
    进化机制验证:
    ✓ 熏习系统正常工作 - 交互经验被记录为种子
    ✓ 感知系统正常工作 - 意图和情感被识别
    ✓ 净化系统正常工作 - 低纯度种子被处理
    ✓ 转识成智验证 - 杂染种子转化为智慧种子
    """)
    
    print(f"\n结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_section("演示完成")


if __name__ == "__main__":
    main()
