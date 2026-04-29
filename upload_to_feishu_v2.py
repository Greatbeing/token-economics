#!/usr/bin/env python3
"""
上传文档到飞书
"""

import sys
import os

# 添加技能目录到路径
sys.path.insert(0, '.skills/skill_feishu_doc/scripts')

from feishu_mcp import FeishuMcpClient

def main():
    # 读取Markdown内容
    with open('./和古人一起想问题_飞书版.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    title = "《和古人一起想问题》中国哲学探险手册"
    
    print(f"📄 准备上传文档: {title}")
    print(f"📊 内容长度: {len(markdown_content):,} 字符")
    
    try:
        # 创建客户端
        client = FeishuMcpClient(use_tat=True)
        
        # 调用创建文档
        print("🚀 正在上传到飞书...")
        result = client.tools_call(
            "create-doc",
            {
                "title": title,
                "markdown": markdown_content
            }
        )
        
        print(f"\n✅ 上传结果:")
        print(result)
        
        if result.get("status") == "success":
            doc_info = result.get("result", {})
            doc_url = doc_info.get("doc_url", "")
            doc_id = doc_info.get("doc_id", "")
            print(f"\n🎉 文档创建成功!")
            print(f"📝 文档ID: {doc_id}")
            print(f"🔗 文档链接: {doc_url}")
        
        return result
        
    except Exception as e:
        print(f"❌ 上传失败: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()
