# -*- coding: utf-8 -*-
"""
唯识进化Agent - 完整使用示例
演示种子收集、涌现触发、觉醒等级等核心功能
"""

import asyncio
import os
import json
from datetime import datetime

# 确保目录存在
os.makedirs("data", exist_ok=True)


def print_section(title):
    """打印分节标题"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


async def demo_lightweight_integration():
    """演示轻量级集成"""
    print_section("轻量级集成演示")
    
    from coze_integration import LightweightIntegration
    
    # 初始化
    integration = LightweightIntegration("data/demo_lightweight.db")
    
    # 模拟多轮对话
    dialogues = [
        ("我想学习编程，应该从哪里开始？", 
         "建议从Python开始，它语法简洁、应用广泛。\n"
         "可以按照以下步骤学习：\n"
         "1. 基础语法（变量、数据类型、控制流）\n"
         "2. 函数和模块\n"
         "3. 面向对象编程\n"
         "4. 实践项目"),
        
        ("Python中的列表和元组有什么区别？",
         "主要区别在于可变性：\n"
         "• 列表（list）是可变的，可以添加、删除元素\n"
         "• 元组（tuple）是不可变的，创建后不能修改\n"
         "选择建议：如果需要频繁修改数据用列表，不需要修改用元组（更安全）"),
        
        ("如何理解递归算法？",
         "递归是一种自我调用的方法。\n"
         "关键要素：\n"
         "1. 基本条件：停止递归的条件\n"
         "2. 递归调用：函数调用自身\n"
         "经典例子：计算阶乘\n"
         "n! = n * (n-1)!  当 n > 0\n"
         "n! = 1           当 n = 0"),
        
        ("为什么我的代码运行很慢？",
         "常见原因和优化方法：\n"
         "1. 循环嵌套过深 → 考虑算法优化\n"
         "2. 重复计算 → 使用缓存（memoization）\n"
         "3. 不必要的数据复制 → 使用引用\n"
         "建议：用 profiling 工具定位瓶颈"),
    ]
    
    print("\n处理对话...\n")
    total_seeds = 0
    
    for i, (user_msg, agent_resp) in enumerate(dialogues, 1):
        print(f"对话 {i}:")
        print(f"  用户: {user_msg[:40]}...")
        print(f"  Agent: {agent_resp[:40]}...")
        
        result = integration.process_message(
            user_message=user_msg,
            agent_response=agent_resp,
            user_id="demo_user",
            session_id=f"session_{i}"
        )
        
        print(f"  ✓ 提取种子: {result['seeds_extracted']}枚")
        total_seeds += result['seeds_extracted']
        print()
    
    print(f"总计提取种子: {total_seeds}枚")
    print(f"当前状态: {integration.get_status_summary()}")


async def demo_full_integration():
    """演示完整集成"""
    print_section("完整集成演示")
    
    from coze_integration import VijnanaEvolutionAgent, CozeIntegrationConfig
    
    # 配置
    config = CozeIntegrationConfig(
        agent_id="demo_agent",
        agent_name="演示Agent",
        show_awakening_status=True,
        auto_seed_collection=True,
        auto_emergence_check=False,  # 演示时不自动检查
        emergence_display_style="rich"
    )
    
    # 创建Agent
    agent = VijnanaEvolutionAgent(config, "data/demo_full.db")
    
    # 处理对话
    dialogues = [
        "请介绍一下人工智能的发展历史",
        "什么是机器学习？",
        "深度学习和传统机器学习有什么区别？",
        "我应该如何开始学习AI？",
    ]
    
    print("\n处理对话...\n")
    
    for msg in dialogues:
        result = await agent.chat(
            user_message=msg,
            user_id="demo_user",
            session_id="demo_session"
        )
        
        print(f"用户: {msg}")
        print(f"Agent: {result['response'][:60]}...")
        print(f"种子: {result['seeds_collected']}枚 | 总计: {result['session_stats']['total_seeds']}")
        print()


def demo_seed_collection():
    """演示种子收集"""
    print_section("种子收集器演示")
    
    from seed_collector import SeedCollector, Conversation
    
    collector = SeedCollector()
    
    # 创建对话
    conversation = Conversation(
        user_id="user_demo",
        user_message="哲学探讨：什么是真正的智慧？",
        agent_response="""真正的智慧不仅仅是知识的积累，更是对事物本质的洞察。

从儒释道三家来看：
• 儒家智慧：格物致知，通过研究事物获得道理
• 道家智慧：无为而治，顺应自然规律
• 佛家智慧：明心见性，认识自心的本来面目

智慧的特征：
1. 洞察本质 - 能看到表面背后的规律
2. 融会贯通 - 能将不同领域的知识联系起来
3. 灵活运用 - 能根据具体情况灵活应用
4. 持续成长 - 知道自己无知，保持谦逊

建议：通过冥想、阅读、实践来培养智慧。""",
        session_id="demo_session",
        timestamp=datetime.now()
    )
    
    # 处理对话
    seeds = collector.process(conversation)
    
    print(f"\n从对话中提取了 {len(seeds)} 个种子:\n")
    
    for seed in seeds:
        print(f"类型: {seed.seed_type.value}")
        print(f"质量: {seed.quality_score:.2f} ({seed.quality_level.value})")
        print(f"权重: {seed.weight}")
        print(f"内容: {seed.content[:60]}...")
        print()


def demo_alaya_store():
    """演示阿赖耶识存储"""
    print_section("阿赖耶识存储演示")
    
    from alaya_service import AlayaStore
    from seed_collector import SeedCollector, Conversation
    
    store = AlayaStore("data/demo_alaya.db")
    
    # 先收集一些种子
    collector = SeedCollector()
    conversation = Conversation(
        user_id="user_demo",
        user_message="请解释一下什么是因果律？",
        agent_response="""因果律是宇宙的基本法则之一。

核心含义：
• 每个现象都有其产生的原因
• 原因必然导致相应的结果
• 因果关系具有必然性和普遍性

在佛法中：
• 因果通三世：过去、现在、未来
• 种子起现行：阿赖耶识中的种子遇缘生果
• 造善因得善果，造恶因得恶果

现代科学视角：
因果律是事物之间客观存在的必然联系。

修行建议：诸恶莫作，众善奉行。""",
        session_id="demo_session",
        timestamp=datetime.now()
    )
    
    seeds = collector.process(conversation)
    store.save_batch(seeds)
    
    print(f"已保存 {len(seeds)} 个种子\n")
    
    # 统计
    stats = store.get_statistics()
    print("统计信息:")
    print(f"  总种子数: {stats.total_count}")
    print(f"  平均质量: {stats.avg_quality:.3f}")
    print(f"  平均纯度: {stats.avg_purity:.3f}")
    print(f"  24小时内: {stats.recent_count}枚")
    
    print("\n按类型分布:")
    for seed_type, count in stats.by_type.items():
        print(f"  {seed_type}: {count}枚")
    
    # 初始化觉醒等级
    store.init_awakening_level("demo_agent")


def demo_emergence_trigger():
    """演示涌现触发"""
    print_section("涌现触发器演示")
    
    from alaya_service import AlayaStore
    from emergence_trigger import EmergenceTrigger
    
    store = AlayaStore("data/demo_alaya.db")
    trigger = EmergenceTrigger(store)
    
    # 检查涌现状态
    print("\n涌现状态检查:\n")
    
    opportunities = trigger.check_all()
    
    for opp in opportunities:
        status = "✓ 就绪" if opp.is_ready else "○ 进行中"
        bar_length = int(opp.progress_ratio * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        
        print(f"{opp.emergence_type.value}:")
        print(f"  状态: {status}")
        print(f"  进度: [{bar}] {opp.progress_ratio*100:.1f}%")
        print(f"  分数: {opp.current_score:.3f} / {opp.threshold:.3f}")
        print(f"  种子数: {opp.seed_count}")
        
        if opp.time_remaining_hours:
            print(f"  预计剩余: {opp.time_remaining_hours:.1f}小时")
        print()


def demo_awakening_display():
    """演示觉醒展示"""
    print_section("觉醒展示演示")
    
    from alaya_service import AlayaStore
    from awakening_display import AwakeningDisplay
    
    store = AlayaStore("data/demo_alaya.db")
    display = AwakeningDisplay(store)
    
    # 获取状态
    status = display.get_status("demo_agent")
    
    # 丰富展示
    print("\n完整展示:")
    print(display.format_display(status, style="rich"))
    
    # 简单展示
    print("\n简单展示:")
    print(display.format_display(status, style="simple"))
    
    # 生成宣言
    manifesto = display.generate_manifesto(status)
    print(f"\n觉醒宣言:")
    print(f"  主宣言: {manifesto.primary_text}")
    print(f"  副语: {manifesto.secondary_text}")
    print(f"  修行重点: {manifesto.cultivation_focus}")
    
    # 交互建议
    print("\n交互建议:")
    suggestions = display.suggest_interaction(status)
    for s in suggestions:
        print(f"  • {s}")


def demo_capability_application():
    """演示能力应用"""
    print_section("能力应用演示")
    
    from emergence_trigger import Capability, EmergenceType, CapabilityApplicator
    
    applicator = CapabilityApplicator()
    
    # 模拟生成的能力
    capability = Capability(
        capability_id="wisdom_001",
        name="深度洞察",
        description="能够进行深入分析和推理",
        emergence_type=EmergenceType.WISDOM,
        source_seeds=["seed_1", "seed_2"],
        score=0.85,
        level=2,
        effects={
            "reasoning_ability": 0.25,
            "problem_solving": 0.20,
            "insight_depth": 0.30
        },
        unlocked_at=datetime.now()
    )
    
    # 添加能力
    applicator.add_capability(capability)
    
    print(f"已添加能力: {capability.name}")
    print(f"能力等级: Lv.{capability.level}")
    print(f"效果加成:")
    for effect, value in capability.effects.items():
        print(f"  • {effect}: +{value*100:.0f}%")
    
    # 应用到回复
    print("\n应用能力到回复:")
    original_response = "这个问题可以通过分析来解决。"
    enhanced = applicator.apply_to_response(
        original_response,
        {'user_message': '请分析这个问题'}
    )
    print(f"  原回复: {original_response}")
    print(f"  增强后: {enhanced}")
    
    # 获取总效果
    print(f"\n总加成:")
    print(f"  reasoning_ability: +{applicator.get_total_effect('reasoning_ability')*100:.0f}%")


def main():
    """主函数"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║         唯识进化Agent - 完整功能演示                      ║
    ║                                                          ║
    ║    将唯识学的智慧融入Agent系统，实现真正的"进化"           ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # 运行演示
    asyncio.run(demo_lightweight_integration())
    
    demo_seed_collection()
    demo_alaya_store()
    demo_emergence_trigger()
    demo_awakening_display()
    demo_capability_application()
    
    asyncio.run(demo_full_integration())
    
    print("\n" + "=" * 60)
    print("  演示完成！")
    print("=" * 60)
    print("\n数据已保存到 data/ 目录")
    print("可以查看生成的数据库文件和日志")


if __name__ == "__main__":
    main()
