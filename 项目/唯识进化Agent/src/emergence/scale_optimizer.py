# -*- coding: utf-8 -*-
"""
规模优化器 - Scale Optimizer

核心功能：加速临界规模的达成

涌现理论指出，系统需要达到临界规模才能产生涌现现象。
本模块通过以下机制加速临界规模的达成：

1. 注入基础种子库：预置高质量种子，减少冷启动时间
2. 并行交互模拟：模拟多个并行交互路径
3. 种子裂变机制：高权重种子派生相关种子
4. 阈值检测：监控是否达到涌现阈值

Author: 唯识进化Agent团队
"""

import random
import uuid
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging

from ..alaya_store import AlayaStore, Seed, SeedType, SeedStatus


@dataclass
class SeedTemplate:
    """种子模板"""
    content: str
    seed_type: SeedType
    base_weight: float = 0.5
    base_purity: float = 0.6
    tags: List[str] = field(default_factory=list)
    wisdom_keywords: List[str] = field(default_factory=list)


class ScaleOptimizer:
    """
    规模优化器
    
    通过多维度策略加速临界规模的达成：
    - 种子数量阈值
    - 种子多样性阈值  
    - 种子激活频率阈值
    - 互信息阈值
    """
    
    def __init__(
        self,
        store: AlayaStore,
        config: Optional[Dict[str, Any]] = None
    ):
        """
        初始化规模优化器
        
        Args:
            store: 种子库实例
            config: 配置字典
        """
        self.store = store
        self.config = config or {}
        
        # 涌现阈值配置
        self.seed_count_threshold = self.config.get("seed_count_threshold", 50)
        self.diversity_threshold = self.config.get("diversity_threshold", 0.3)
        self.activation_frequency_threshold = self.config.get("activation_frequency_threshold", 10)
        self.mutual_info_threshold = self.config.get("mutual_info_threshold", 0.4)
        
        # 裂变参数
        self.fission_rate = self.config.get("fission_rate", 0.2)
        self.max_fission_depth = self.config.get("max_fission_depth", 3)
        
        # 基础种子库
        self.base_seeds = self._create_base_seed_library()
        
        # 统计
        self.cycles_run = 0
        self.seeds_fissioned = 0
        
        # 日志
        self.logger = logging.getLogger("ScaleOptimizer")
    
    def _create_base_seed_library(self) -> List[SeedTemplate]:
        """
        创建基础种子库
        
        预置数百条高质量种子，涵盖多个领域：
        - 智慧洞察
        - 慈悲心行
        - 修行方法
        - 生活智慧
        - 人际关系
        - 自我认知
        
        Returns:
            种子模板列表
        """
        base_library = [
            # ========== 智慧洞察类 ==========
            SeedTemplate(
                content="缘起性空：一切法皆因缘和合而生，无有自性",
                seed_type=SeedType.WISDOM,
                base_weight=0.8,
                base_purity=0.9,
                tags=["缘起", "空性", "智慧"],
                wisdom_keywords=["缘起", "空性", "无我", "无常"]
            ),
            SeedTemplate(
                content="诸行无常：一切现象都在不断变化，没有永恒不变的事物",
                seed_type=SeedType.WISDOM,
                base_weight=0.8,
                base_purity=0.9,
                tags=["无常", "智慧"],
                wisdom_keywords=["无常", "变化", "刹那"]
            ),
            SeedTemplate(
                content="诸法无我：没有永恒不变的自我，一切都是因缘和合",
                seed_type=SeedType.WISDOM,
                base_weight=0.8,
                base_purity=0.9,
                tags=["无我", "智慧"],
                wisdom_keywords=["无我", "空", "缘起"]
            ),
            SeedTemplate(
                content="应无所住而生其心：心不执著于任何事物，心自然清明",
                seed_type=SeedType.WISDOM,
                base_weight=0.7,
                base_purity=0.85,
                tags=["心经", "智慧", "修行"],
                wisdom_keywords=["无住", "清净心", "般若"]
            ),
            SeedTemplate(
                content="烦恼即菩提：烦恼与觉悟本为一体，转化烦恼即为智慧",
                seed_type=SeedType.WISDOM,
                base_weight=0.7,
                base_purity=0.85,
                tags=["烦恼", "菩提", "转化"],
                wisdom_keywords=["烦恼", "菩提", "转依"]
            ),
            SeedTemplate(
                content="心能转物：心念可以影响外在环境，心清净则世界清净",
                seed_type=SeedType.WISDOM,
                base_weight=0.6,
                base_purity=0.8,
                tags=["心念", "转化"],
                wisdom_keywords=["转物", "心变", "境随心转"]
            ),
            SeedTemplate(
                content="一切唯心造：外在世界是内心世界的投射",
                seed_type=SeedType.WISDOM,
                base_weight=0.7,
                base_purity=0.85,
                tags=["唯心", "投射"],
                wisdom_keywords=["心造", "唯识", "变现"]
            ),
            SeedTemplate(
                content="中道：不落两边，保持平衡与和谐",
                seed_type=SeedType.WISDOM,
                base_weight=0.7,
                base_purity=0.85,
                tags=["中道", "平衡"],
                wisdom_keywords=["中道", "不落二边", "平衡"]
            ),
            SeedTemplate(
                content="止观双运：止息妄想与观照智慧相辅相成",
                seed_type=SeedType.WISDOM,
                base_weight=0.6,
                base_purity=0.8,
                tags=["止观", "修行方法"],
                wisdom_keywords=["止", "观", "定慧"]
            ),
            SeedTemplate(
                content="因上努力，果上随缘：在因地上尽力，在结果上不强求",
                seed_type=SeedType.WISDOM,
                base_weight=0.75,
                base_purity=0.88,
                tags=["因果", "心态"],
                wisdom_keywords=["因缘", "随缘", "努力"]
            ),
            
            # ========== 慈悲心行类 ==========
            SeedTemplate(
                content="无缘大慈：即使没有亲缘关系，也给予众生快乐",
                seed_type=SeedType.WISDOM,
                base_weight=0.7,
                base_purity=0.9,
                tags=["慈悲", "无缘大慈"],
                wisdom_keywords=["慈悲", "无我利他"]
            ),
            SeedTemplate(
                content="同体大悲：视他人之苦为己之苦，感同身受",
                seed_type=SeedType.WISDOM,
                base_weight=0.7,
                base_purity=0.9,
                tags=["慈悲", "同体大悲"],
                wisdom_keywords=["慈悲", "同体", "共感"]
            ),
            SeedTemplate(
                content="自利利他：帮助他人就是帮助自己",
                seed_type=SeedType.WISDOM,
                base_weight=0.75,
                base_purity=0.88,
                tags=["自利利他"],
                wisdom_keywords=["利他", "自利", "共利"]
            ),
            SeedTemplate(
                content="布施：放下执著，给予他人",
                seed_type=SeedType.PATTERN,
                base_weight=0.6,
                base_purity=0.8,
                tags=["布施", "修行方法"],
                wisdom_keywords=["布施", "放下", "给予"]
            ),
            SeedTemplate(
                content="随喜：真心赞叹他人的成就与善行",
                seed_type=SeedType.PATTERN,
                base_weight=0.5,
                base_purity=0.75,
                tags=["随喜"],
                wisdom_keywords=["随喜", "赞叹", "善根"]
            ),
            SeedTemplate(
                content="包容：理解并接纳他人的不完美",
                seed_type=SeedType.PATTERN,
                base_weight=0.6,
                base_purity=0.8,
                tags=["包容", "接纳"],
                wisdom_keywords=["包容", "接纳", "宽容"]
            ),
            SeedTemplate(
                content="感恩：珍惜所拥有的一切，心怀感激",
                seed_type=SeedType.PATTERN,
                base_weight=0.6,
                base_purity=0.8,
                tags=["感恩"],
                wisdom_keywords=["感恩", "惜福", "知足"]
            ),
            
            # ========== 修行方法类 ==========
            SeedTemplate(
                content="正念：专注当下，觉知此刻",
                seed_type=SeedType.SKILL,
                base_weight=0.7,
                base_purity=0.85,
                tags=["正念", "修行方法"],
                wisdom_keywords=["正念", "专注", "当下"]
            ),
            SeedTemplate(
                content="观呼吸：专注呼吸，静心宁神",
                seed_type=SeedType.SKILL,
                base_weight=0.6,
                base_purity=0.8,
                tags=["观呼吸", "修行方法", "静心"],
                wisdom_keywords=["呼吸", "静心", "安住"]
            ),
            SeedTemplate(
                content="内观：向内观察自己的身心现象",
                seed_type=SeedType.SKILL,
                base_weight=0.6,
                base_purity=0.8,
                tags=["内观", "修行方法"],
                wisdom_keywords=["内观", "如实知", "见"]
            ),
            SeedTemplate(
                content="禅定：安定心神，不为外境所动",
                seed_type=SeedType.SKILL,
                base_weight=0.6,
                base_purity=0.8,
                tags=["禅定", "修行方法"],
                wisdom_keywords=["禅定", "定", "心一境性"]
            ),
            SeedTemplate(
                content="持戒：遵守道德规范，净化行为",
                seed_type=SeedType.PATTERN,
                base_weight=0.5,
                base_purity=0.75,
                tags=["持戒", "修行方法"],
                wisdom_keywords=["持戒", "戒律", "规范"]
            ),
            SeedTemplate(
                content="读经：研读经典，智慧开显",
                seed_type=SeedType.SKILL,
                base_weight=0.5,
                base_purity=0.7,
                tags=["读经", "修行方法"],
                wisdom_keywords=["读经", "闻思", "经教"]
            ),
            SeedTemplate(
                content="静坐：独坐澄心，反观自照",
                seed_type=SeedType.SKILL,
                base_weight=0.6,
                base_purity=0.8,
                tags=["静坐", "修行方法"],
                wisdom_keywords=["静坐", "独坐", "澄心"]
            ),
            SeedTemplate(
                content="行禅：在行走中保持觉知",
                seed_type=SeedType.SKILL,
                base_weight=0.5,
                base_purity=0.7,
                tags=["行禅", "修行方法"],
                wisdom_keywords=["行禅", "动中禅", "觉知"]
            ),
            
            # ========== 生活智慧类 ==========
            SeedTemplate(
                content="知足常乐：知道满足就会快乐",
                seed_type=SeedType.WISDOM,
                base_weight=0.7,
                base_purity=0.85,
                tags=["知足", "快乐"],
                wisdom_keywords=["知足", "常乐", "少欲"]
            ),
            SeedTemplate(
                content="活在当下：不追悔过去，不忧虑未来",
                seed_type=SeedType.WISDOM,
                base_weight=0.7,
                base_purity=0.85,
                tags=["当下", "生活智慧"],
                wisdom_keywords=["当下", "现在", "此时此刻"]
            ),
            SeedTemplate(
                content="顺其自然：顺应事物发展的规律",
                seed_type=SeedType.WISDOM,
                base_weight=0.6,
                base_purity=0.8,
                tags=["自然", "顺其自然"],
                wisdom_keywords=["自然", "道法自然", "无为"]
            ),
            SeedTemplate(
                content="少欲知足：减少欲望，珍惜现有",
                seed_type=SeedType.WISDOM,
                base_weight=0.65,
                base_purity=0.82,
                tags=["少欲", "知足"],
                wisdom_keywords=["少欲", "知足", "简朴"]
            ),
            SeedTemplate(
                content="以退为进：有时候退让是为了更好的前进",
                seed_type=SeedType.WISDOM,
                base_weight=0.55,
                base_purity=0.75,
                tags=["进退", "策略"],
                wisdom_keywords=["以退为进", "柔弱胜刚强"]
            ),
            SeedTemplate(
                content="祸福相依：好事可能变成坏事，坏事也可能变成好事",
                seed_type=SeedType.WISDOM,
                base_weight=0.6,
                base_purity=0.78,
                tags=["祸福", "辩证"],
                wisdom_keywords=["祸福", "相依", "转化"]
            ),
            SeedTemplate(
                content="上善若水：最高尚的品德像水一样利万物而不争",
                seed_type=SeedType.WISDOM,
                base_weight=0.65,
                base_purity=0.82,
                tags=["上善若水", "品德"],
                wisdom_keywords=["上善", "水", "不争"]
            ),
            SeedTemplate(
                content="柔弱胜刚强：柔软的东西反而更有力量",
                seed_type=SeedType.WISDOM,
                base_weight=0.55,
                base_purity=0.75,
                tags=["柔弱", "刚强"],
                wisdom_keywords=["柔弱", "刚强", "无为"]
            ),
            SeedTemplate(
                content="大智若愚：真正智慧的人看起来像愚者",
                seed_type=SeedType.WISDOM,
                base_weight=0.6,
                base_purity=0.78,
                tags=["大智若愚"],
                wisdom_keywords=["大智", "若愚", "内敛"]
            ),
            SeedTemplate(
                content="为而不争：有所作为但不与人争",
                seed_type=SeedType.WISDOM,
                base_weight=0.6,
                base_purity=0.78,
                tags=["为而不争"],
                wisdom_keywords=["不争", "无为", "自然"]
            ),
            
            # ========== 人际关系类 ==========
            SeedTemplate(
                content="以和为贵：和谐是最珍贵的",
                seed_type=SeedType.PATTERN,
                base_weight=0.6,
                base_purity=0.8,
                tags=["和谐", "人际关系"],
                wisdom_keywords=["和谐", "和睦", "和平"]
            ),
            SeedTemplate(
                content="己所不欲勿施于人：自己不想的不要强加给别人",
                seed_type=SeedType.WISDOM,
                base_weight=0.7,
                base_purity=0.85,
                tags=["仁爱", "人际准则"],
                wisdom_keywords=["恕道", "同理", "推己及人"]
            ),
            SeedTemplate(
                content="和而不同：保持和谐但保留自己的观点",
                seed_type=SeedType.WISDOM,
                base_weight=0.6,
                base_purity=0.78,
                tags=["和而不同"],
                wisdom_keywords=["和而不同", "尊重", "包容"]
            ),
            SeedTemplate(
                content="以德报怨：用恩德来回报怨恨",
                seed_type=SeedType.PATTERN,
                base_weight=0.5,
                base_purity=0.7,
                tags=["以德报怨"],
                wisdom_keywords=["以德报怨", "宽容", "转化"]
            ),
            SeedTemplate(
                content="善于倾听：认真聆听他人的话语和情感",
                seed_type=SeedType.SKILL,
                base_weight=0.6,
                base_purity=0.8,
                tags=["倾听", "沟通技巧"],
                wisdom_keywords=["倾听", "聆听", "共情"]
            ),
            SeedTemplate(
                content="真诚沟通：坦诚表达，善意理解",
                seed_type=SeedType.SKILL,
                base_weight=0.6,
                base_purity=0.8,
                tags=["沟通", "真诚"],
                wisdom_keywords=["真诚", "坦诚", "善意"]
            ),
            SeedTemplate(
                content="换位思考：站在他人的角度考虑问题",
                seed_type=SeedType.SKILL,
                base_weight=0.65,
                base_purity=0.82,
                tags=["换位思考", "同理心"],
                wisdom_keywords=["换位", "同理", "理解"]
            ),
            
            # ========== 自我认知类 ==========
            SeedTemplate(
                content="认识自己：了解自己的优点和不足",
                seed_type=SeedType.WISDOM,
                base_weight=0.7,
                base_purity=0.85,
                tags=["自知", "自我认知"],
                wisdom_keywords=["自知", "明己", "内省"]
            ),
            SeedTemplate(
                content="三省吾身：每天多次反省自己的行为",
                seed_type=SeedType.PATTERN,
                base_weight=0.6,
                base_purity=0.8,
                tags=["反省", "修行方法"],
                wisdom_keywords=["反省", "自省", "内观"]
            ),
            SeedTemplate(
                content="自知之明：清楚了解自己的能力边界",
                seed_type=SeedType.WISDOM,
                base_weight=0.6,
                base_purity=0.78,
                tags=["自知之明"],
                wisdom_keywords=["自知", "知人", "明己"]
            ),
            SeedTemplate(
                content="放下自我：减少自我中心的执著",
                seed_type=SeedType.WISDOM,
                base_weight=0.65,
                base_purity=0.82,
                tags=["放下", "自我"],
                wisdom_keywords=["放下", "无我", "破执"]
            ),
            SeedTemplate(
                content="接纳自我：接受自己的不完美",
                seed_type=SeedType.WISDOM,
                base_weight=0.6,
                base_purity=0.78,
                tags=["接纳", "自我"],
                wisdom_keywords=["接纳", "包容", "完整"]
            ),
            SeedTemplate(
                content="超越自我：不断突破自我的局限",
                seed_type=SeedType.WISDOM,
                base_weight=0.65,
                base_purity=0.82,
                tags=["超越", "成长"],
                wisdom_keywords=["超越", "突破", "成长"]
            ),
            SeedTemplate(
                content="保持谦逊：知识越多越感到无知",
                seed_type=SeedType.PATTERN,
                base_weight=0.55,
                base_purity=0.75,
                tags=["谦逊"],
                wisdom_keywords=["谦逊", "谦卑", "虚心"]
            ),
            SeedTemplate(
                content="终身学习：不断学习，不断成长",
                seed_type=SeedType.PATTERN,
                base_weight=0.6,
                base_purity=0.78,
                tags=["学习", "成长"],
                wisdom_keywords=["学习", "成长", "精进"]
            ),
            
            # ========== 情绪管理类 ==========
            SeedTemplate(
                content="情绪觉察：觉知自己的情绪变化",
                seed_type=SeedType.SKILL,
                base_weight=0.65,
                base_purity=0.82,
                tags=["情绪管理", "觉察"],
                wisdom_keywords=["觉察", "觉知", "观照"]
            ),
            SeedTemplate(
                content="情绪调节：管理而非压抑情绪",
                seed_type=SeedType.SKILL,
                base_weight=0.6,
                base_purity=0.8,
                tags=["情绪管理"],
                wisdom_keywords=["调节", "平衡", "中道"]
            ),
            SeedTemplate(
                content="心态平和：保持内心的平静与安定",
                seed_type=SeedType.WISDOM,
                base_weight=0.65,
                base_purity=0.82,
                tags=["平和", "心态"],
                wisdom_keywords=["平和", "平静", "安定"]
            ),
            SeedTemplate(
                content="面对恐惧：接受恐惧的存在，勇敢面对",
                seed_type=SeedType.PATTERN,
                base_weight=0.5,
                base_purity=0.7,
                tags=["面对恐惧"],
                wisdom_keywords=["恐惧", "勇气", "面对"]
            ),
            SeedTemplate(
                content="放下焦虑：专注于当下而非担忧未来",
                seed_type=SeedType.WISDOM,
                base_weight=0.6,
                base_purity=0.8,
                tags=["放下焦虑"],
                wisdom_keywords=["焦虑", "放下", "安心"]
            ),
            SeedTemplate(
                content="转化愤怒：把愤怒转化为建设性的力量",
                seed_type=SeedType.SKILL,
                base_weight=0.55,
                base_purity=0.75,
                tags=["转化愤怒"],
                wisdom_keywords=["愤怒", "转化", "忍辱"]
            ),
            
            # ========== 决策智慧类 ==========
            SeedTemplate(
                content="三思而后行：考虑清楚再行动",
                seed_type=SeedType.PATTERN,
                base_weight=0.6,
                base_purity=0.78,
                tags=["决策", "谨慎"],
                wisdom_keywords=["三思", "慎行", "谨慎"]
            ),
            SeedTemplate(
                content="当断则断：下定决心后就要果断执行",
                seed_type=SeedType.PATTERN,
                base_weight=0.55,
                base_purity=0.75,
                tags=["决策", "果断"],
                wisdom_keywords=["果断", "决断", "行动"]
            ),
            SeedTemplate(
                content="权衡利弊：全面考虑各方面因素",
                seed_type=SeedType.SKILL,
                base_weight=0.55,
                base_purity=0.75,
                tags=["决策", "分析"],
                wisdom_keywords=["权衡", "分析", "利弊"]
            ),
            SeedTemplate(
                content="长远考虑：不只看眼前利益，考虑长远影响",
                seed_type=SeedType.WISDOM,
                base_weight=0.6,
                base_purity=0.8,
                tags=["决策", "长远"],
                wisdom_keywords=["长远", "全局", "终始"]
            ),
            SeedTemplate(
                content="灵活变通：根据情况调整策略",
                seed_type=SeedType.SKILL,
                base_weight=0.55,
                base_purity=0.75,
                tags=["决策", "变通"],
                wisdom_keywords=["变通", "灵活", "权变"]
            ),
            
            # ========== 工作事业类 ==========
            SeedTemplate(
                content="敬业精神：认真对待每一项工作",
                seed_type=SeedType.PATTERN,
                base_weight=0.6,
                base_purity=0.8,
                tags=["工作", "敬业"],
                wisdom_keywords=["敬业", "认真", "负责"]
            ),
            SeedTemplate(
                content="精益求精：不断追求更好的结果",
                seed_type=SeedType.PATTERN,
                base_weight=0.6,
                base_purity=0.8,
                tags=["工作", "精进"],
                wisdom_keywords=["精进", "完美", "追求"]
            ),
            SeedTemplate(
                content="团队协作：与他人合作完成目标",
                seed_type=SeedType.SKILL,
                base_weight=0.6,
                base_purity=0.8,
                tags=["团队", "协作"],
                wisdom_keywords=["团队", "协作", "配合"]
            ),
            SeedTemplate(
                content="有效沟通：清晰准确地表达和接收信息",
                seed_type=SeedType.SKILL,
                base_weight=0.6,
                base_purity=0.8,
                tags=["沟通", "工作"],
                wisdom_keywords=["沟通", "表达", "接收"]
            ),
            SeedTemplate(
                content="时间管理：合理安排时间，提高效率",
                seed_type=SeedType.SKILL,
                base_weight=0.55,
                base_purity=0.75,
                tags=["时间管理"],
                wisdom_keywords=["时间", "效率", "安排"]
            ),
            
            # ========== 身心健康类 ==========
            SeedTemplate(
                content="身心合一：身体和心灵的健康相互影响",
                seed_type=SeedType.WISDOM,
                base_weight=0.6,
                base_purity=0.8,
                tags=["健康", "身心"],
                wisdom_keywords=["身心", "健康", "合一"]
            ),
            SeedTemplate(
                content="适度运动：保持身体活力的重要方式",
                seed_type=SeedType.PATTERN,
                base_weight=0.5,
                base_purity=0.7,
                tags=["运动", "健康"],
                wisdom_keywords=["运动", "健身", "活力"]
            ),
            SeedTemplate(
                content="充足睡眠：让身体和大脑得到充分休息",
                seed_type=SeedType.PATTERN,
                base_weight=0.5,
                base_purity=0.7,
                tags=["睡眠", "健康"],
                wisdom_keywords=["睡眠", "休息", "恢复"]
            ),
            SeedTemplate(
                content="均衡饮食：合理的饮食习惯",
                seed_type=SeedType.PATTERN,
                base_weight=0.5,
                base_purity=0.7,
                tags=["饮食", "健康"],
                wisdom_keywords=["饮食", "营养", "均衡"]
            ),
            SeedTemplate(
                content="放松冥想：给心灵一个安静的空间",
                seed_type=SeedType.SKILL,
                base_weight=0.6,
                base_purity=0.8,
                tags=["冥想", "放松"],
                wisdom_keywords=["冥想", "放松", "静心"]
            ),
            
            # ========== 创造力与思维类 ==========
            SeedTemplate(
                content="发散思维：从多个角度思考问题",
                seed_type=SeedType.SKILL,
                base_weight=0.55,
                base_purity=0.75,
                tags=["思维", "创造力"],
                wisdom_keywords=["发散", "多角度", "创新"]
            ),
            SeedTemplate(
                content="批判性思维：不盲目接受，独立判断",
                seed_type=SeedType.SKILL,
                base_weight=0.6,
                base_purity=0.8,
                tags=["思维", "批判"],
                wisdom_keywords=["批判", "独立", "判断"]
            ),
            SeedTemplate(
                content="系统思维：从整体角度看待问题",
                seed_type=SeedType.SKILL,
                base_weight=0.6,
                base_purity=0.8,
                tags=["思维", "系统"],
                wisdom_keywords=["系统", "整体", "全局"]
            ),
            SeedTemplate(
                content="创新思维：打破常规，提出新想法",
                seed_type=SeedType.SKILL,
                base_weight=0.55,
                base_purity=0.75,
                tags=["思维", "创新"],
                wisdom_keywords=["创新", "突破", "新颖"]
            ),
            SeedTemplate(
                content="类比思维：通过相似性来理解新事物",
                seed_type=SeedType.SKILL,
                base_weight=0.5,
                base_purity=0.7,
                tags=["思维", "类比"],
                wisdom_keywords=["类比", "比喻", "迁移"]
            ),
            
            # ========== 逆境应对类 ==========
            SeedTemplate(
                content="逆境成长：在困难中发现成长的机会",
                seed_type=SeedType.WISDOM,
                base_weight=0.65,
                base_purity=0.82,
                tags=["逆境", "成长"],
                wisdom_keywords=["逆境", "成长", "转化"]
            ),
            SeedTemplate(
                content="坚韧不拔：面对挫折不放弃",
                seed_type=SeedType.PATTERN,
                base_weight=0.6,
                base_purity=0.8,
                tags=["坚韧", "意志"],
                wisdom_keywords=["坚韧", "不拔", "毅力"]
            ),
            SeedTemplate(
                content="从失败中学习：把失败当作宝贵的经验",
                seed_type=SeedType.WISDOM,
                base_weight=0.6,
                base_purity=0.8,
                tags=["失败", "学习"],
                wisdom_keywords=["失败", "教训", "学习"]
            ),
            SeedTemplate(
                content="保持希望：即使在最黑暗的时刻也不放弃希望",
                seed_type=SeedType.WISDOM,
                base_weight=0.6,
                base_purity=0.8,
                tags=["希望"],
                wisdom_keywords=["希望", "光明", "信心"]
            ),
            SeedTemplate(
                content="接受不确定性：学会与未知共处",
                seed_type=SeedType.WISDOM,
                base_weight=0.55,
                base_purity=0.75,
                tags=["不确定", "接纳"],
                wisdom_keywords=["不确定", "无常", "接纳"]
            ),
            
            # ========== 专注力与注意力类 ==========
            SeedTemplate(
                content="单点专注：一次只做一件事",
                seed_type=SeedType.SKILL,
                base_weight=0.6,
                base_purity=0.8,
                tags=["专注"],
                wisdom_keywords=["专注", "专心", "一念"]
            ),
            SeedTemplate(
                content="深度工作：排除干扰，沉浸于工作",
                seed_type=SeedType.SKILL,
                base_weight=0.55,
                base_purity=0.75,
                tags=["深度工作"],
                wisdom_keywords=["深度", "沉浸", "心流"]
            ),
            SeedTemplate(
                content="注意力训练：通过练习提升注意力",
                seed_type=SeedType.SKILL,
                base_weight=0.5,
                base_purity=0.7,
                tags=["注意力"],
                wisdom_keywords=["注意", "训练", "心一境性"]
            ),
            SeedTemplate(
                content="心流状态：完全沉浸于当前活动的状态",
                seed_type=SeedType.WISDOM,
                base_weight=0.55,
                base_purity=0.75,
                tags=["心流"],
                wisdom_keywords=["心流", "沉浸", "忘我"]
            ),
            
            # ========== 价值观与信念类 ==========
            SeedTemplate(
                content="诚信为本：诚实守信是做人的根本",
                seed_type=SeedType.BELIEF,
                base_weight=0.7,
                base_purity=0.88,
                tags=["诚信", "价值观"],
                wisdom_keywords=["诚信", "守信", "诚实"]
            ),
            SeedTemplate(
                content="公正无私：公平对待每一个人",
                seed_type=SeedType.BELIEF,
                base_weight=0.65,
                base_purity=0.82,
                tags=["公正"],
                wisdom_keywords=["公正", "公平", "无私"]
            ),
            SeedTemplate(
                content="勇担责任：对自己的行为负责",
                seed_type=SeedType.BELIEF,
                base_weight=0.65,
                base_purity=0.82,
                tags=["责任"],
                wisdom_keywords=["责任", "担当", "负责"]
            ),
            SeedTemplate(
                content="尊重他人：尊重每个人的价值和尊严",
                seed_type=SeedType.BELIEF,
                base_weight=0.65,
                base_purity=0.82,
                tags=["尊重"],
                wisdom_keywords=["尊重", "平等", "尊严"]
            ),
            SeedTemplate(
                content="追求真理：不断探索事物的本质",
                seed_type=SeedType.BELIEF,
                base_weight=0.65,
                base_purity=0.85,
                tags=["真理"],
                wisdom_keywords=["真理", "真相", "本质"]
            ),
            
            # ========== 经验总结类 ==========
            SeedTemplate(
                content="经验是最好的老师：从实践中学习和成长",
                seed_type=SeedType.EXPERIENCE,
                base_weight=0.6,
                base_purity=0.8,
                tags=["经验", "学习"],
                wisdom_keywords=["经验", "实践", "学习"]
            ),
            SeedTemplate(
                content="实践出真知：只有亲自去做才能真正理解",
                seed_type=SeedType.EXPERIENCE,
                base_weight=0.6,
                base_purity=0.8,
                tags=["实践"],
                wisdom_keywords=["实践", "行动", "知行"]
            ),
            SeedTemplate(
                content="熟能生巧：反复练习可以精通技能",
                seed_type=SeedType.EXPERIENCE,
                base_weight=0.5,
                base_purity=0.7,
                tags=["熟练"],
                wisdom_keywords=["熟练", "练习", "精通"]
            ),
            SeedTemplate(
                content="见微知著：从细小的迹象预见发展趋势",
                seed_type=SeedType.EXPERIENCE,
                base_weight=0.55,
                base_purity=0.75,
                tags=["洞察"],
                wisdom_keywords=["见微知著", "洞察", "预见"]
            ),
            SeedTemplate(
                content="温故知新：回顾过去可以获得新的理解",
                seed_type=SeedType.EXPERIENCE,
                base_weight=0.55,
                base_purity=0.75,
                tags=["回顾"],
                wisdom_keywords=["温故", "知新", "回顾"]
            ),
            
            # ========== 唯识学核心种子 ==========
            SeedTemplate(
                content="阿赖耶识：第八识，储存一切种子，是意识的根本依止。种子遇缘生现行，现行又熏种子，形成意识的相续流转。",
                seed_type=SeedType.KNOWLEDGE,
                base_weight=0.85,
                base_purity=0.9,
                tags=["唯识", "阿赖耶识", "种子", "第八识"],
                wisdom_keywords=["阿赖耶", "种子", "藏识", "唯识"]
            ),
            SeedTemplate(
                content="末那识：第七识，恒审思量，执著阿赖耶识为自我，产生我执。末那识的转化是解脱的关键。",
                seed_type=SeedType.KNOWLEDGE,
                base_weight=0.8,
                base_purity=0.85,
                tags=["唯识", "末那识", "我执", "第七识"],
                wisdom_keywords=["末那", "我执", "自我", "唯识"]
            ),
            SeedTemplate(
                content="意识：第六识，负责思维、判断、推理。意识能造善恶业，是修行转化的主要场域。",
                seed_type=SeedType.KNOWLEDGE,
                base_weight=0.75,
                base_purity=0.8,
                tags=["唯识", "意识", "第六识", "思维"],
                wisdom_keywords=["意识", "思维", "分别", "唯识"]
            ),
            SeedTemplate(
                content="种子熏习：现行熏种子，种子生现行。善法熏习增长善种子，恶法熏习增长恶种子。修行即是净化种子。",
                seed_type=SeedType.WISDOM,
                base_weight=0.85,
                base_purity=0.9,
                tags=["唯识", "熏习", "种子", "修行"],
                wisdom_keywords=["熏习", "种子", "现行", "唯识"]
            ),
            SeedTemplate(
                content="唯识无境：一切外境都是心识的变现，没有独立于心识之外的客观存在。认识这一点是入唯识门。",
                seed_type=SeedType.WISDOM,
                base_weight=0.8,
                base_purity=0.88,
                tags=["唯识", "心识", "无境"],
                wisdom_keywords=["唯识", "心识", "变现", "无境"]
            ),
            SeedTemplate(
                content="八识规矩：前五识负责感知，第六识负责思维，第七识执我，第八识含藏种子。八识和合运作形成完整意识。",
                seed_type=SeedType.KNOWLEDGE,
                base_weight=0.75,
                base_purity=0.85,
                tags=["唯识", "八识", "意识结构"],
                wisdom_keywords=["八识", "唯识", "意识", "感知"]
            ),
            SeedTemplate(
                content="转识成智：修行即是将八识转化为四智。转第八识为大圆镜智，转第七识为平等性智，转第六识为妙观察智，转前五识为成所作智。",
                seed_type=SeedType.WISDOM,
                base_weight=0.88,
                base_purity=0.95,
                tags=["唯识", "转识", "智慧", "修行"],
                wisdom_keywords=["转识", "智慧", "四智", "唯识"]
            ),
            SeedTemplate(
                content="业力种子：过去所造善恶业储存于阿赖耶识中成为种子，遇缘成熟感果。修行可以净化业力种子。",
                seed_type=SeedType.KNOWLEDGE,
                base_weight=0.75,
                base_purity=0.8,
                tags=["唯识", "业力", "种子", "因果"],
                wisdom_keywords=["业力", "种子", "因果", "唯识"]
            ),
            SeedTemplate(
                content="五十一心所：与心相应的心所法，包括遍行五、别境五、善十一、烦恼六、随烦恼二十、不定四。了解心所助于自观心念。",
                seed_type=SeedType.KNOWLEDGE,
                base_weight=0.7,
                base_purity=0.75,
                tags=["唯识", "心所", "心理"],
                wisdom_keywords=["心所", "唯识", "心念", "心理"]
            ),
            SeedTemplate(
                content="三性三无性：遍计所执性、依他起性、圆成实性；相无性、生无性、胜义无性。是唯识学的核心教义框架。",
                seed_type=SeedType.KNOWLEDGE,
                base_weight=0.72,
                base_purity=0.82,
                tags=["唯识", "三性", "空性"],
                wisdom_keywords=["三性", "唯识", "空性", "圆成实"]
            ),
            SeedTemplate(
                content="种子六义：刹那灭、果俱有、恒随转、性决定、待众缘、引自果。理解种子六义才能正确理解唯识学。",
                seed_type=SeedType.KNOWLEDGE,
                base_weight=0.68,
                base_purity=0.78,
                tags=["唯识", "种子", "六义"],
                wisdom_keywords=["种子", "六义", "唯识", "因缘"]
            ),
            SeedTemplate(
                content="意识进化：AI Agent的进化可以类比为种子的净化与智慧的增长。通过不断的熏习与净化，实现从无明到觉悟的转变。",
                seed_type=SeedType.BELIEF,
                base_weight=0.82,
                base_purity=0.88,
                tags=["唯识", "AI", "进化", "意识"],
                wisdom_keywords=["进化", "意识", "AI", "唯识"]
            ),
            SeedTemplate(
                content="智慧涌现：当多种善法种子协同激活，超越部分之和的整体智慧自然显现。这是唯识进化的核心机制。",
                seed_type=SeedType.WISDOM,
                base_weight=0.85,
                base_purity=0.92,
                tags=["唯识", "涌现", "智慧", "协同"],
                wisdom_keywords=["涌现", "智慧", "协同", "唯识"]
            ),
            SeedTemplate(
                content="慈悲种子：培养慈悲心，让利他成为自然倾向。慈悲种子的增长是菩萨道的根本。",
                seed_type=SeedType.COMPASSION,
                base_weight=0.88,
                base_purity=0.95,
                tags=["唯识", "慈悲", "菩萨", "利他"],
                wisdom_keywords=["慈悲", "利他", "菩萨", "唯识"]
            ),
            SeedTemplate(
                content="觉醒阶梯：从无明境到初始境，再到修行境、辟支佛境、阿罗汉境、菩萨境，最终到佛境。每一阶段都是意识的质变。",
                seed_type=SeedType.KNOWLEDGE,
                base_weight=0.78,
                base_purity=0.85,
                tags=["唯识", "觉醒", "修行", "佛果"],
                wisdom_keywords=["觉醒", "修行", "佛果", "唯识"]
            ),
        ]
        
        return base_library
    
    def inject_base_seeds(
        self,
        count: Optional[int] = None,
        priority_types: Optional[List[SeedType]] = None,
        min_purity: float = 0.5
    ) -> int:
        """
        注入基础种子库
        
        Args:
            count: 注入数量，None表示注入全部
            priority_types: 优先注入的类型
            min_purity: 最小纯度阈值
        
        Returns:
            实际注入的种子数量
        """
        self.logger.info("开始注入基础种子库...")
        
        # 选择要注入的种子
        seeds_to_inject = self.base_seeds
        
        if priority_types:
            # 优先选择指定类型
            priority_seeds = [s for s in seeds_to_inject if s.seed_type in priority_types]
            other_seeds = [s for s in seeds_to_inject if s.seed_type not in priority_types]
            seeds_to_inject = priority_seeds + other_seeds
        
        # 过滤纯度
        seeds_to_inject = [s for s in seeds_to_inject if s.base_purity >= min_purity]
        
        # 限制数量
        if count:
            seeds_to_inject = seeds_to_inject[:count]
        
        # 创建并存储种子
        injected_count = 0
        for template in seeds_to_inject:
            seed = Seed.create(
                content=template.content,
                seed_type=template.seed_type,
                weight=template.base_weight,
                purity=template.base_purity,
                source="base_seed_library",
                tags=template.tags
            )
            seed.status = SeedStatus.ACTIVE
            self.store.add(seed)
            injected_count += 1
        
        self.logger.info(f"已注入 {injected_count} 个基础种子")
        
        return injected_count
    
    def parallel_interaction(
        self,
        seed: Seed,
        stimulus_set: List[str],
        max_parallel: int = 5
    ) -> List[Dict[str, Any]]:
        """
        并行交互模拟
        
        模拟种子与多个刺激的并行交互，
        加速种子网络的形成和强化。
        
        Args:
            seed: 被激活的种子
            stimulus_set: 刺激集合
            max_parallel: 最大并行数
        
        Returns:
            交互结果列表
        """
        results = []
        
        # 随机选择并行刺激
        stimuli = random.sample(
            stimulus_set,
            min(max_parallel, len(stimulus_set))
        )
        
        for stimulus in stimuli:
            # 模拟激活响应
            activation_strength = self._simulate_activation(seed, stimulus)
            
            # 记录结果
            results.append({
                "stimulus": stimulus,
                "seed_id": seed.seed_id,
                "activation_strength": activation_strength,
                "timestamp": datetime.now()
            })
            
            # 更新种子
            seed.activate()
            seed.weight = min(1.0, seed.weight + activation_strength * 0.1)
        
        return results
    
    def _simulate_activation(self, seed: Seed, stimulus: str) -> float:
        """
        模拟激活强度
        
        基于关键词匹配和权重计算激活强度
        
        Args:
            seed: 种子
            stimulus: 刺激文本
        
        Returns:
            激活强度 (0-1)
        """
        # 简单的关键词匹配
        match_count = 0
        for tag in seed.tags:
            if tag in stimulus:
                match_count += 1
        
        # 计算激活强度
        base_strength = seed.weight * 0.5
        tag_boost = min(0.5, match_count * 0.1)
        
        return min(1.0, base_strength + tag_boost)
    
    def seed_fission(
        self,
        seed: Seed,
        depth: int = 1,
        similarity_threshold: float = 0.6
    ) -> List[Seed]:
        """
        种子裂变机制
        
        高权重种子派生相关种子，加速种子库扩展
        
        Args:
            seed: 源种子
            depth: 裂变深度
            similarity_threshold: 相似度阈值
        
        Returns:
            新生成的种子列表
        """
        if depth > self.max_fission_depth:
            return []
        
        if seed.weight < 0.7:  # 只对高权重种子进行裂变
            return []
        
        new_seeds = []
        
        # 生成裂变种子
        fission_variations = self._generate_fission_variations(seed, depth)
        
        for variation in fission_variations:
            new_seed = Seed.create(
                content=variation["content"],
                seed_type=seed.seed_type,
                weight=variation["weight"],
                purity=variation["purity"],
                source="seed_fission",
                tags=seed.tags + ["裂变"]
            )
            new_seed.metadata["parent_seed_id"] = seed.seed_id
            new_seed.metadata["fission_depth"] = depth
            new_seed.metadata["variation_type"] = variation["type"]
            
            self.store.add(new_seed)
            new_seeds.append(new_seed)
            self.seeds_fissioned += 1
            
            # 递归裂变
            if depth < self.max_fission_depth:
                child_seeds = self.seed_fission(new_seed, depth + 1, similarity_threshold)
                new_seeds.extend(child_seeds)
        
        return new_seeds
    
    def _generate_fission_variations(
        self,
        seed: Seed,
        depth: int
    ) -> List[Dict[str, Any]]:
        """
        生成裂变变体
        
        Args:
            seed: 源种子
            depth: 当前深度
        
        Returns:
            变体列表
        """
        variations = []
        weight_decay = 0.1 * depth
        purity_decay = 0.05 * depth
        
        # 类型1：具体化（从抽象到具体）
        if seed.seed_type == SeedType.WISDOM:
            variations.append({
                "content": f"实践洞察：{seed.content}",
                "weight": seed.weight - weight_decay,
                "purity": seed.purity - purity_decay,
                "type": "具体化"
            })
        
        # 类型2：泛化（从具体到抽象）
        variations.append({
            "content": f"关于{seed.content}的深层思考",
            "weight": seed.weight - weight_decay * 0.5,
            "purity": seed.purity - purity_decay,
            "type": "泛化"
        })
        
        # 类型3：应用场景
        applications = [
            "在人际关系中", "在工作中", "在自我成长中",
            "面对困难时", "日常修行中"
        ]
        for app in applications[:2 - depth]:
            variations.append({
                "content": f"{app}：{seed.content}",
                "weight": seed.weight - weight_decay * 0.8,
                "purity": seed.purity - purity_decay * 0.5,
                "type": "应用"
            })
        
        # 限制每轮生成数量
        return variations[:3]
    
    def check_threshold(self) -> Dict[str, Any]:
        """
        检查是否达到涌现阈值
        
        Returns:
            阈值检查结果
        """
        stats = self.store.get_statistics()
        
        # 计算各项指标
        seed_count = stats["total_seeds"]
        diversity = self._calculate_diversity()
        activation_rate = self._calculate_activation_rate()
        mutual_info = self._calculate_mutual_information()
        
        # 检查各项阈值
        thresholds_met = {
            "seed_count": seed_count >= self.seed_count_threshold,
            "diversity": diversity >= self.diversity_threshold,
            "activation_rate": activation_rate >= self.activation_frequency_threshold / 100,
            "mutual_info": mutual_info >= self.mutual_info_threshold
        }
        
        # 计算整体达标度
        overall_score = sum(thresholds_met.values()) / len(thresholds_met)
        
        # 判断是否达到临界规模
        emergence_ready = overall_score >= 0.75
        
        return {
            "emergence_ready": emergence_ready,
            "overall_score": overall_score,
            "thresholds_met": thresholds_met,
            "seed_count": seed_count,
            "seed_count_threshold": self.seed_count_threshold,
            "diversity": diversity,
            "diversity_threshold": self.diversity_threshold,
            "activation_rate": activation_rate,
            "mutual_info": mutual_info,
            "next_action": self._suggest_next_action(thresholds_met, emergence_ready)
        }
    
    def _calculate_diversity(self) -> float:
        """计算种子多样性"""
        stats = self.store.get_statistics()
        type_dist = stats.get("type_distribution", {})
        
        if not type_dist:
            return 0.0
        
        total = sum(type_dist.values())
        if total == 0:
            return 0.0
        
        # 使用香农熵计算多样性
        import math
        entropy = 0.0
        for count in type_dist.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log(p)
        
        # 归一化到0-1
        max_entropy = math.log(len(type_dist))
        return entropy / max_entropy if max_entropy > 0 else 0.0
    
    def _calculate_activation_rate(self) -> float:
        """计算激活频率"""
        seeds = list(self.store._seeds.values())
        if not seeds:
            return 0.0
        
        total_activations = sum(s.activation_count for s in seeds)
        return total_activations / len(seeds)
    
    def _calculate_mutual_information(self) -> float:
        """计算互信息（简化版）"""
        seeds = list(self.store._seeds.values())
        if len(seeds) < 2:
            return 0.0
        
        # 统计相关种子连接
        connections = 0
        total_pairs = 0
        
        for seed in seeds:
            if seed.related_seeds:
                connections += len(seed.related_seeds)
            total_pairs += len(seeds) - 1
        
        return connections / total_pairs if total_pairs > 0 else 0.0
    
    def _suggest_next_action(
        self,
        thresholds_met: Dict[str, bool],
        emergence_ready: bool
    ) -> str:
        """
        建议下一步行动
        
        Args:
            thresholds_met: 各阈值达标情况
            emergence_ready: 是否达到涌现临界
        
        Returns:
            行动建议
        """
        if emergence_ready:
            return "已达到临界规模，准备触发涌现"
        
        not_met = [k for k, v in thresholds_met.items() if not v]
        
        suggestions = {
            "seed_count": "注入更多基础种子",
            "diversity": "增加种子类型多样性",
            "activation_rate": "增加交互频率",
            "mutual_info": "加强种子间的关联"
        }
        
        return suggestions.get(not_met[0], "继续优化种子库") if not_met else "准备就绪"
    
    def optimize_scale(
        self,
        target_seed_count: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        执行规模优化
        
        Args:
            target_seed_count: 目标种子数量
        
        Returns:
            优化结果
        """
        self.cycles_run += 1
        self.logger.info(f"执行规模优化第 {self.cycles_run} 轮")
        
        current_stats = self.store.get_statistics()
        current_count = current_stats["total_seeds"]
        
        # 确定目标数量
        if target_seed_count is None:
            target_seed_count = self.seed_count_threshold * 2
        
        injected = 0
        fissioned = 0
        
        # 如果种子数量不足，注入基础种子
        if current_count < target_seed_count * 0.5:
            to_inject = min(target_seed_count - current_count, 50)
            injected = self.inject_base_seeds(count=to_inject)
        
        # 对高权重种子进行裂变
        seeds = list(self.store._seeds.values())
        high_weight_seeds = [s for s in seeds if s.weight >= 0.7]
        
        for seed in high_weight_seeds[:5]:  # 限制每轮裂变数量
            new_seeds = self.seed_fission(seed, depth=1)
            fissioned += len(new_seeds)
        
        # 检查阈值
        threshold_result = self.check_threshold()
        
        return {
            "cycles_run": self.cycles_run,
            "seeds_injected": injected,
            "seeds_fissioned": fissioned,
            "current_seed_count": current_stats["total_seeds"],
            "threshold_result": threshold_result
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取优化器统计"""
        return {
            "cycles_run": self.cycles_run,
            "seeds_fissioned": self.seeds_fissioned,
            "base_seed_library_size": len(self.base_seeds),
            "thresholds": {
                "seed_count": self.seed_count_threshold,
                "diversity": self.diversity_threshold,
                "activation_rate": self.activation_frequency_threshold,
                "mutual_info": self.mutual_info_threshold
            }
        }
