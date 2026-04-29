# -*- coding: utf-8 -*-
"""
唯识进化Agent - 基础使用示例

展示Agent的基本用法：
1. 创建Agent实例
2. 进行对话交互
3. 查看状态和统计
4. 添加知识种子
5. 手动触发反思和净化
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import AlayaAgent


def main():
    """基础使用示例"""
    
    print("=" * 60)
    print("唯识进化Agent - 基础使用示例")
    print("=" * 60)
    
    # 1. 创建Agent实例
    print("\n[1] 创建Agent实例...")
    agent = AlayaAgent(
        config_path="config/default.yaml",
        name="Alaya",
        data_dir="./data/demo"
    )
    print(f"✓ Agent已创建: {agent}")
    
    # 2. 添加一些初始知识
    print("\n[2] 添加初始知识种子...")
    knowledge_seeds = [
        ("Python是一种高级编程语言，强调代码可读性", 0.8),
        ("人工智能是研究使计算机展示智能的学科", 0.7),
        ("机器学习是AI的一个子领域，通过数据学习模式", 0.7),
        ("唯识论是佛教哲学，强调心识的变现功能", 0.6),
    ]
    for content, importance in knowledge_seeds:
        seed_id = agent.add_knowledge(content, importance)
        print(f"  - 添加: {content[:30]}... → {seed_id[:8]}")
    
    # 3. 进行对话交互
    print("\n[3] 进行对话交互...")
    interactions = [
        "你好，请介绍一下你自己",
        "什么是人工智能？",
        "你能教我Python吗？",
        "唯识论和AI有什么关系？",
        "你今天感觉怎么样？"
    ]
    
    for user_input in interactions:
        response = agent.interact(user_input)
        print(f"\n  用户: {user_input}")
        print(f"  Agent: {response}")
    
    # 4. 查看Agent状态
    print("\n[4] 查看Agent状态...")
    status = agent.get_status()
    print(f"\n  Agent名称: {status['name']}")
    print(f"  交互次数: {status['interaction_count']}")
    print(f"  种子数量: {status['seeds_count']}")
    print(f"  平均纯度: {status['average_purity']:.2%}")
    print(f"  觉醒等级: {status['awakening_level']}")
    print(f"  觉醒评分: {status['awakening_score']:.2%}")
    print(f"  智慧种子: {status['wisdom_seeds']}")
    print(f"  创伤种子: {status['trauma_seeds']}")
    
    # 5. 详细交互模式
    print("\n[5] 详细交互模式...")
    detailed = agent.interact_detailed("请解释一下什么是机器学习")
    print(f"\n  意图识别: {detailed['sensory_analysis']['intent']}")
    print(f"  情感分析: {detailed['sensory_analysis']['sentiment']}")
    print(f"  激活种子: {len(detailed['activated_seeds'])}")
    print(f"  决策行动: {detailed['decision']['action']}")
    print(f"  置信度: {detailed['decision']['confidence']:.2%}")
    print(f"  结果评分: {detailed['evaluation']['outcome']:.2%}")
    
    # 6. 手动触发反思
    print("\n[6] 手动触发反思...")
    reflection = agent.reflect()
    print(f"  对齐度: {reflection.get('alignment_rate', 0):.2%}")
    print(f"  建议: {reflection.get('suggestions', [])}")
    
    # 7. 手动触发净化
    print("\n[7] 手动触发净化...")
    purify_results = agent.purify()
    print(f"  净化种子数: {len(purify_results)}")
    for result in purify_results[:3]:
        print(f"    - {result.original_seed_id[:8]}: {result.action}")
    
    # 8. 查看觉醒报告
    print("\n[8] 觉醒报告:")
    report = agent.get_awakening_report()
    print(report)
    
    # 9. 保存状态
    print("\n[9] 保存Agent状态...")
    if agent.save():
        print("  ✓ 状态已保存")
    else:
        print("  ✗ 保存失败")
    
    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
