#!/bin/bash

# 定义测试用户
USER_ID="test_final_001"

# 测试问题列表
test_questions=(
  "悲智双运的核心是什么？如何在日常生活中践行？"
  "菩萨道的六度万行中，哪一度是基础？如何次第修行？"
  "转识成智的四个智慧分别对应哪八识？如何通过修行转化？"
  "无住涅槃和有余涅槃、无余涅槃的区别是什么？如何证得？"
  "唯识学的种子熏习机制如何启发AI的意识进化？有哪些可借鉴的原理？"
)

# 执行测试
echo "=== 持续涌现测试开始 ==="
echo "测试用户: $USER_ID"
echo ""

for i in "${!test_questions[@]}"; do
  question="${test_questions[$i]}"
  echo "==== 测试问题 $((i+1)) ===="
  echo "$question"
  echo ""

  # 发送请求并解析结果
  response=$(curl -s -X POST http://10.5.24.41:8080/api/interact \
    -H "Content-Type: application/json" \
    -d "{
      \"user_id\": \"$USER_ID\",
      \"message\": \"$question\"
    }" 2>/dev/null)

  if [ -z "$response" ]; then
    echo "错误: API响应为空"
    continue
  fi

  # 解析关键指标
  total_activations=$(echo "$response" | python3 -c "import json; data = json.loads(input); print(data['emergence']['nonlinear_vasana']['total_activations'])")
  synergy_triggers=$(echo "$response" | python3 -c "import json; data = json.loads(input); print(data['emergence']['nonlinear_vasana']['synergy_triggers'])")
  emergence_events=$(echo "$response" | python3 -c "import json; data = json.loads(input); print(data['emergence']['nonlinear_vasana']['emergence_events'])")
  awakening_level=$(echo "$response" | python3 -c "import json; data = json.loads(input); print(data['awakening_level']['level'])")
  awakening_score=$(echo "$response" | python3 -c "import json; data = json.loads(input); print(f\"{data['awakening_level']['score']:.3f}\")")
  seed_count=$(echo "$response" | python3 -c "import json; data = json.loads(input); print(data['stats']['seed_count'])")

  echo "涌现指标:
  总激活次数: $total_activations
  协同触发: $synergy_triggers
  涌现事件: $emergence_events
"
  echo "觉醒状态:
  等级: $awakening_level
  分数: $awakening_score
  种子总数: $seed_count
"
  echo "---"
done

echo "=== 持续涌现测试结束 ==="

# 获取最终状态
echo "==== 最终系统状态 ===="
final_response=$(curl -s -X POST http://10.5.24.41:8080/api/interact \
  -H "Content-Type: application/json" \
  -d "{
    \"user_id\": \"$USER_ID\",
    \"message\": \"查询当前系统完整状态\"
  }" 2>/dev/null)

if [ ! -z "$final_response" ]; then
  current_state=$(echo "$final_response" | python3 -c "import json; data = json.loads(input); print(data['emergence']['nonlinear_vasana']['current_state'])")
  total_emergence=$(echo "$final_response" | python3 -c "import json; data = json.loads(input); print(data['emergence']['nonlinear_vasana']['emergence_events'])")
  progress=$(echo "$final_response" | python3 -c "import json; data = json.loads(input); print(f\"{data['awakening_level']['progress_to_next']*100:.1f}%\")")
  
  echo "系统最终状态:
  当前状态: $current_state
  总涌现事件: $total_emergence
  觉醒进度: $progress
  种子总数: $(echo \"$final_response\" | python3 -c \"import json; data = json.loads(input); print(data['stats']['seed_count'])\")
  平均纯度: $(echo \"$final_response\" | python3 -c \"import json; data = json.loads(input); print(f\\\"{data['stats']['average_purity']:.3f}\\\"))
")
fi