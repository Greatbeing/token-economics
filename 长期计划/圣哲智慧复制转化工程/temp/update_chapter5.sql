UPDATE chapter_progress 
SET status = 'completed',
    completed_at = '2026-04-02',
    word_count = 7600,
    feedback_summary = '儿童参与感强化完成：儿童提问9次（达标≥8），质疑反驳6次（达标≥4），立场选择2次（达标≥2），新增生活共鸣点（学校午餐分配、数学作业经历、带课外书争议）3个，总字数约7600字。思想剧场增加儿童深度辩论回合，强化主动思考与生活经验联系。'
WHERE chapter_title = '第五章 什么是"好"的规则？';