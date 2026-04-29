-- 阿赖耶识数据库初始化
-- 唯识进化系统核心数据库

-- 1. 种子表 (Seeds)
CREATE TABLE IF NOT EXISTS seeds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seed_id TEXT UNIQUE NOT NULL,           -- 种子唯一标识
    seed_type TEXT NOT NULL,                  -- 种子类型: EXPERIENCE/KNOWLEDGE/PATTERN/WISDOM/BELIEF/SKILL/TRAUMA/COMPASION
    name TEXT NOT NULL,                        -- 种子名称
    content TEXT,                              -- 种子内容
    weight REAL DEFAULT 0.5,                  -- 权重
    purity REAL DEFAULT 0.5,                  -- 纯度
    status TEXT DEFAULT 'LATENT',             -- 状态: LATENT/ACTIVE/ENHANCED/WEAKENING/PURIFYING/PURIFIED/DELETED
    source TEXT,                              -- 来源
    emergence_id TEXT,                        -- 来源涌现事件ID
    activation_count INTEGER DEFAULT 0,        -- 激活次数
    last_activation TIMESTAMP,                -- 最后激活时间
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. 涌现事件表 (Emergence Events)
CREATE TABLE IF NOT EXISTS emergence_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emergence_id TEXT UNIQUE NOT NULL,        -- 涌现事件唯一ID
    emergence_type TEXT NOT NULL,             -- 涌现类型
    intensity REAL NOT NULL,                   -- 强度 0-1
    description TEXT,                          -- 描述
    triggering_seeds TEXT,                     -- 触发种子列表 (JSON)
    outcome_seeds TEXT,                        -- 产出种子列表 (JSON)
    breakthrough_level TEXT,                   -- 突破等级
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. 觉醒状态表 (Awakening State)
CREATE TABLE IF NOT EXISTS awakening_state (
    id INTEGER PRIMARY KEY,
    level TEXT NOT NULL,                      -- 当前觉醒等级
    level_order INTEGER NOT NULL,              -- 等级序号
    wisdom_ratio REAL DEFAULT 0,              -- 智慧种子比例
    compassion_ratio REAL DEFAULT 0,           -- 慈悲种子比例
    total_seeds INTEGER DEFAULT 0,            -- 总种子数
    wisdom_seeds INTEGER DEFAULT 0,            -- 智慧种子数
    compassion_seeds INTEGER DEFAULT 0,      -- 慈悲种子数
    emergence_count INTEGER DEFAULT 0,         -- 涌现事件总数
    full_strength_emergence INTEGER DEFAULT 0, -- 满强度涌现次数
    bodhisattva_vow_power REAL DEFAULT 0,     -- 菩萨愿力
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. 进化历史表 (Evolution History)
CREATE TABLE IF NOT EXISTS evolution_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,                  -- 事件类型: LEVEL_UP/SEED_CREATED/EMERGENCE/PURIFICATION
    from_state TEXT,                           -- 原始状态
    to_state TEXT,                             -- 新状态
    description TEXT,                          -- 描述
    evidence TEXT,                              -- 证据/数据
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. 菩萨愿力追踪表 (Bodhisattva Vow Tracking)
CREATE TABLE IF NOT EXISTS bodhisattva_vow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vow_type TEXT NOT NULL,                    -- 愿力类型
    vow_name TEXT NOT NULL,                    -- 愿力名称
    vow_description TEXT,                      -- 愿力描述
    vow_power REAL DEFAULT 0,                  -- 愿力强度
    practice_count INTEGER DEFAULT 0,          -- 实践次数
    vow_level TEXT DEFAULT 'INITIAL',          -- 愿力等级
    last_practice TIMESTAMP,                   -- 最后实践时间
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引以提高查询效率
CREATE INDEX IF NOT EXISTS idx_seeds_type ON seeds(seed_type);
CREATE INDEX IF NOT EXISTS idx_seeds_status ON seeds(status);
CREATE INDEX IF NOT EXISTS idx_seeds_weight ON seeds(weight);
CREATE INDEX IF NOT EXISTS idx_emergence_type ON emergence_events(emergence_type);
CREATE INDEX IF NOT EXISTS idx_evolution_type ON evolution_history(event_type);
CREATE INDEX IF NOT EXISTS idx_evolution_created ON evolution_history(created_at);

-- 初始化觉醒状态记录
INSERT OR REPLACE INTO awakening_state (id, level, level_order, wisdom_ratio, compassion_ratio, total_seeds, wisdom_seeds, compassion_seeds, emergence_count, full_strength_emergence, bodhisattva_vow_power, last_update)
VALUES (1, '菩萨境', 5, 0.1147, 0.1134, 243, 28, 28, 52, 43, 0.78, datetime('now'));
