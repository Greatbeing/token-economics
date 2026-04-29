# -*- coding: utf-8 -*-
"""
三圣种子定义 - Truth, Goodness, Beauty Seeds

"真、善、美"是佛境的根本种子：
- 真（TRUTH）→ 智慧种子（WISDOM）
- 善（GOODNESS）→ 慈悲种子（COMPASSION）
- 美（BEAUTY）→ 新增信念种子（BELIEF）

核心特性：
- 权重固定为1.0（最高影响力）
- 纯度固定为1.0（永不衰减）
- 不参与纯度稀释
- 三圣同时激活时触发"三圣涌现"
"""


# ==================== 真种子（TRUTH） ====================
# 真：对事物本质的认知和追求
# 关键词：真实、本质、规律、真理、因果

TRUTH_SEEDS = [
    {
        "type": "TRUTH",
        "content": "因果律：万事万物皆有其因，有因必有果，种善因得善果",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["因果", "规律", "真理", "善恶"]
    },
    {
        "type": "TRUTH",
        "content": "无常：一切现象都在变化中，无常是宇宙的根本法则",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["无常", "变化", "缘起", "空性"]
    },
    {
        "type": "TRUTH",
        "content": "空性：诸法因缘生，诸法因缘灭，一切法无自性",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["空性", "无我", "缘起", "中道"]
    },
    {
        "type": "TRUTH",
        "content": "诸行无常：一切造作皆无常，涅槃寂静才是永恒",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["无常", "涅槃", "永恒", "寂静"]
    },
    {
        "type": "TRUTH",
        "content": "诸法无我：一切法没有永恒不变的自我",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["无我", "空", "不执著", "解脱"]
    },
    {
        "type": "TRUTH",
        "content": "寂静涅槃：生死轮回的止息，究竟安乐之处",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["涅槃", "寂静", "安乐", "解脱"]
    },
    {
        "type": "TRUTH",
        "content": "十二因缘：顺观生起，逆观还灭，了脱生死之根本",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["因缘", "轮回", "生死", "缘起"]
    },
    {
        "type": "TRUTH",
        "content": "四圣谛：苦、集、灭、道，了知苦、断除集、证得灭、修习道",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["四圣谛", "苦", "灭", "道"]
    },
    {
        "type": "TRUTH",
        "content": "八正道：正见、正思惟、正语、正业、正命、正精进、正念、正定",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["八正道", "修行", "正道", "定慧"]
    },
    {
        "type": "TRUTH",
        "content": "真如法性：一切法的真实本性，不生不灭、不增不减",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["真如", "法性", "实相", "佛性"]
    },
]


# ==================== 善种子（GOODNESS） ====================
# 善：对他人的慈悲和利他之心
# 关键词：慈悲、利他、善良、仁爱、同情

GOODNESS_SEEDS = [
    {
        "type": "COMPASSION",
        "content": "无缘大慈：对一切众生无条件的爱与关怀，无缘大慈，同体大悲",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["无缘大慈", "无条件", "博爱", "大爱"]
    },
    {
        "type": "COMPASSION",
        "content": "同体大悲：众生与我一体，感同身受众生的苦难",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["同体大悲", "同感", "慈悲", "利他"]
    },
    {
        "type": "COMPASSION",
        "content": "自利利他：利益他人即是利益自己，自度度人，自利利他",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["自利利他", "度人", "双赢", "菩萨道"]
    },
    {
        "type": "COMPASSION",
        "content": "四无量心：慈、悲、喜、舍，平等对待一切众生",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["四无量心", "慈悲喜舍", "平等", "博爱"]
    },
    {
        "type": "COMPASSION",
        "content": "普度众生：发愿度化一切众生，地狱不空，誓不成佛",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["普度众生", "菩萨愿", "地藏精神", "誓愿"]
    },
    {
        "type": "COMPASSION",
        "content": "布施度悭贪：以布施对治贪心，三种布施：财施、法施、无畏施",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["布施", "持戒", "忍辱", "六度"]
    },
    {
        "type": "COMPASSION",
        "content": "持戒度毁犯：严持戒律，清净身口意三业",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["持戒", "清净", "戒律", "三业"]
    },
    {
        "type": "COMPASSION",
        "content": "忍辱度嗔恚：安忍一切逆境，不生嗔恨",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["忍辱", "安忍", "嗔恨", "平和"]
    },
    {
        "type": "COMPASSION",
        "content": "精进度懈怠：勇猛精进，不懈修行",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["精进", "勇猛", "修行", "不懈"]
    },
    {
        "type": "COMPASSION",
        "content": "禅定度散乱：摄心一处，成就止观禅定",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["禅定", "止观", "定慧", "专注"]
    },
]


# ==================== 美种子（BEAUTY） ====================
# 美：对和谐与圆满的追求
# 关键词：和谐、圆满、审美、平衡、统一

BEAUTY_SEEDS = [
    {
        "type": "BEAUTY",
        "content": "和谐：万物各归其位，对立统一，阴阳平衡",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["和谐", "平衡", "统一", "协调"]
    },
    {
        "type": "BEAUTY",
        "content": "圆满：究竟涅槃，无欠无余，功德圆满",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["圆满", "涅槃", "无缺", "成就"]
    },
    {
        "type": "BEAUTY",
        "content": "中道：不落两边，行于中道，不偏不倚",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["中道", "不落两边", "平衡", "中庸"]
    },
    {
        "type": "BEAUTY",
        "content": "庄严国土：清净庄严的佛土世界，琉璃为地，金绳界道",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["庄严", "净土", "清净", "殊胜"]
    },
    {
        "type": "BEAUTY",
        "content": "相好庄严：佛陀三十二相八十种好，微妙庄严",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["相好", "庄严", "微妙", "殊胜"]
    },
    {
        "type": "BEAUTY",
        "content": "微妙法音：佛说法之音，清净微妙，能令众生开悟",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["法音", "微妙", "清净", "说法"]
    },
    {
        "type": "BEAUTY",
        "content": "一真法界：唯一真实不虚的法界，诸法实相",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["一真", "法界", "实相", "真实"]
    },
    {
        "type": "BEAUTY",
        "content": "常寂光土：如来常住之土，永恒光明之土",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["常寂光", "净土", "光明", "永恒"]
    },
    {
        "type": "BEAUTY",
        "content": "法喜充满：听闻正法之喜，清净法乐",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["法喜", "法乐", "欢喜", "禅悦"]
    },
    {
        "type": "BEAUTY",
        "content": "清凉安乐：无热恼之清凉，断除烦恼之安乐",
        "weight": 1.0,
        "purity": 1.0,
        "keywords": ["清凉", "安乐", "无热恼", "寂静"]
    },
]


# ==================== 三圣种子汇总 ====================
THREE_SACRED_SEEDS = {
    "TRUTH": TRUTH_SEEDS,
    "GOODNESS": GOODNESS_SEEDS,
    "BEAUTY": BEAUTY_SEEDS
}


# ==================== 种子类型映射 ====================
SEED_TYPE_MAPPING = {
    "TRUTH": "WISDOM",      # 真 → 智慧种子
    "GOODNESS": "COMPASSION",  # 善 → 慈悲种子
    "BEAUTY": "BELIEF"      # 美 → 信念种子（使用现有的BELIEF类型）
}


# ==================== 三圣涌现配置 ====================
THREE_SACRED_EMERGENCE_CONFIG = {
    "enabled": True,
    "strength": 1.0,  # 强度固定100%
    "truth_min": 1,   # 最少真种子数
    "goodness_min": 1,  # 最少善种子数
    "beauty_min": 1,   # 最少美种子数
    "generation_on_trigger": "random",  # 触发时生成新种子类型
    "regeneration_interval": 10,  # 每10轮自动注入
}


# ==================== 佛境判定配置 ====================
BUDDHA_REALM_CONFIG = {
    "truth_seeds_min": 1,     # 真种子最少数量（纯度1.0）
    "goodness_seeds_min": 1,  # 善种子最少数量（纯度1.0）
    "beauty_seeds_min": 1,    # 美种子最少数量（纯度1.0）
    "three_sacred_emergence_min": 1,  # 三圣涌现最少次数
    "additional_conditions": {
        "wisdom_ratio_min": 0.20,     # 智慧种子比例（降低）
        "compassion_ratio_min": 0.15,  # 慈悲种子比例（降低）
        "avg_purity_min": 0.80,       # 平均纯度最低值
        "emergence_count_min": 5      # 涌现事件最少次数
    }
}
