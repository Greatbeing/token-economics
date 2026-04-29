#!/bin/bash
export IMA_CLIENT_ID="8a5569cf6c06596689989612bc913c41"
export IMA_API_KEY="CAamgRX6n8sCOOGqfqkG42WOuMElWF1G2YS33uaxz4Av0qkUEENChLbH6Tq5ARgO5TLM4g4TXw=="
export KB_ID="BvDIS0KXLBD2OVnwpPJQQUig3Pem2kbl8cCRqTNWkTE="

UPLOAD_DIR="战略思想库"
SUCCESS_COUNT=0
FAIL_COUNT=0

upload_file() {
  local file_path="$1"
  local file_name=$(basename "$file_path")
  local file_size=$(wc -c < "$file_path")
  
  echo ">>> 处理: $file_name (${file_size} bytes)"
  
  # 检查重名
  CHECK_RESULT=$(curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/check_repeated_names" \
    -H "ima-openapi-clientid: $IMA_CLIENT_ID" \
    -H "ima-openapi-apikey: $IMA_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"knowledge_base_id\": \"$KB_ID\", \"params\": [{\"name\": \"$file_name\", \"media_type\": 7}]}")
  
  if echo "$CHECK_RESULT" | grep -q '"is_repeated":true'; then
    echo "    [跳过] 文件已存在: $file_name"
    return 1
  fi
  
  # 创建上传凭证
  RESULT=$(curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/create_media" \
    -H "ima-openapi-clientid: $IMA_CLIENT_ID" \
    -H "ima-openapi-apikey: $IMA_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"file_name\": \"$file_name\", \"file_size\": $file_size, \"content_type\": \"text/markdown\", \"knowledge_base_id\": \"$KB_ID\", \"file_ext\": \"md\"}")
  
  MEDIA_ID=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data'].get('media_id','') if d.get('data') else '')")
  
  if [ -z "$MEDIA_ID" ]; then
    echo "    [失败] 创建凭证失败: $RESULT"
    return 1
  fi
  
  SECRET_ID=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['cos_credential'].get('secret_id','') if d.get('data') else '')")
  SECRET_KEY=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['cos_credential'].get('secret_key','') if d.get('data') else '')")
  TOKEN=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['cos_credential'].get('token','') if d.get('data') else '')")
  BUCKET=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['cos_credential'].get('bucket_name','') if d.get('data') else '')")
  REGION=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['cos_credential'].get('region','') if d.get('data') else '')")
  COS_KEY=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['cos_credential'].get('cos_key','') if d.get('data') else '')")
  START_TIME=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['cos_credential'].get('start_time','') if d.get('data') else '')")
  EXPIRED_TIME=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['cos_credential'].get('expired_time','') if d.get('data') else '')")
  
  # 上传到COS
  node .skills/skill_ima-skill/knowledge-base/scripts/cos-upload.cjs \
    --file "$file_path" \
    --secret-id "$SECRET_ID" \
    --secret-key "$SECRET_KEY" \
    --token "$TOKEN" \
    --bucket "$BUCKET" \
    --region "$REGION" \
    --cos-key "$COS_KEY" \
    --content-type "text/markdown" \
    --start-time "$START_TIME" \
    --expired-time "$EXPIRED_TIME" 2>&1 | head -1
  
  # 添加到知识库
  ADD_RESULT=$(curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/add_knowledge" \
    -H "ima-openapi-clientid: $IMA_CLIENT_ID" \
    -H "ima-openapi-apikey: $IMA_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"media_type\": 7, \"media_id\": \"$MEDIA_ID\", \"title\": \"$file_name\", \"knowledge_base_id\": \"$KB_ID\", \"file_info\": {\"cos_key\": \"$COS_KEY\", \"file_size\": $file_size, \"file_name\": \"$file_name\"}}")
  
  if echo "$ADD_RESULT" | grep -q '"code":0'; then
    echo "    [成功] $file_name"
    return 0
  else
    echo "    [失败] $ADD_RESULT"
    return 1
  fi
}

# 文件列表
FILES=(
  "战略思想库/raw/素材说明.md"
  "战略思想库/wiki/INDEX.md"
  "战略思想库/wiki/主题分类/以少胜多.md"
  "战略思想库/wiki/主题分类/全胜思想.md"
  "战略思想库/wiki/主题分类/战略与战术.md"
  "战略思想库/wiki/主题分类/治军之道.md"
  "战略思想库/wiki/主题分类/知己知彼.md"
  "战略思想库/wiki/主题分类/集中兵力原则.md"
  "战略思想库/wiki/人物档案/克劳塞维茨.md"
  "战略思想库/wiki/人物档案/孙子.md"
  "战略思想库/wiki/人物档案/拿破仑.md"
  "战略思想库/wiki/人物档案/曹操.md"
  "战略思想库/wiki/人物档案/曾国藩.md"
  "战略思想库/wiki/人物档案/毛泽东.md"
  "战略思想库/wiki/人物档案/隆美尔.md"
  "战略思想库/wiki/人物档案/韩信.md"
  "战略思想库/wiki/经典案例/井陉之战.md"
  "战略思想库/wiki/经典案例/四渡赤水.md"
  "战略思想库/wiki/经典案例/赤壁之战.md"
)

echo "=== 开始批量上传 $((${#FILES[@]})) 个文件 ==="
echo ""

for file in "${FILES[@]}"; do
  if upload_file "$file"; then
    ((SUCCESS_COUNT++))
  else
    ((FAIL_COUNT++))
  fi
  echo ""
done

echo "=== 上传完成 ==="
echo "成功: $SUCCESS_COUNT"
echo "失败: $FAIL_COUNT"
