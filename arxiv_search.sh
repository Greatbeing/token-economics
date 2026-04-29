#!/bin/bash

# arXiv论文搜索脚本
# 用于检索climate resilience基础设施相关论文

TOKEN="R7Vpy-Ln2dXdthRNkHXjLSF2BNEZ65O0nh-Wr36rWOc"
BASE_URL="https://data.rag.ac.cn/arxiv"

# 搜索关键词
QUERY="climate resilience infrastructure"

echo "正在搜索: $QUERY"

# 搜索论文
curl -X GET "$BASE_URL/search?q=$QUERY&token=$TOKEN" \
  -H "Content-Type: application/json" \
  -o arxiv_search_results.json

echo "搜索完成，结果已保存到 arxiv_search_results.json"
