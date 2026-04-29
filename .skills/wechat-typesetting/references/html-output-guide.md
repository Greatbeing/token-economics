# WeChat HTML Output Guide

## 目录
- [Overview](#overview)
- [Base Template Structure](#base-template-structure)
- [Color Scheme Variables](#color-scheme-variables)
- [HTML Components Library](#html-components-library)
- [Image Placement Guidelines](#image-placement-guidelines)
- [Typography Guidelines for HTML](#typography-guidelines-for-html)
- [Mobile Optimization Checklist](#mobile-optimization-checklist)
- [WeChat Editor Compatibility](#wechat-editor-compatibility)
- [Example Output Format](#example-output-format)
- [Advanced Techniques](#advanced-techniques)

## Overview

This guide provides complete HTML template structure for generating WeChat-ready formatted articles. The HTML uses inline styles to ensure compatibility with all WeChat editors (135编辑器, 秀米, 96编辑器, etc.).

## Base Template Structure

```html
<section style="max-width: 750px; margin: 0 auto; padding: 20px 16px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif; font-size: 15px; color: #3f3f3f; line-height: 1.75; letter-spacing: 0.5px;">

  <!-- Main Title -->
  <h1 style="font-size: 24px; font-weight: bold; color: #1a1a1a; text-align: center; margin: 20px 0 30px 0; line-height: 1.4;">
    文章标题
  </h1>

  <!-- Subtitle or intro (optional) -->
  <p style="font-size: 14px; color: #666; text-align: center; margin: -20px 0 30px 0; font-style: italic;">
    副标题或引言
  </p>

  <!-- Introduction paragraph -->
  <p style="margin: 20px 0; text-align: justify;">
    引言段落内容...
  </p>

  <!-- Section 01 -->
  <div style="margin: 40px 0 10px 0;">
    <span style="display: inline-block; font-size: 18px; font-weight: bold; color: {{PRIMARY_COLOR}}; padding: 5px 15px; border-left: 4px solid {{PRIMARY_COLOR}};">
      01.
    </span>
  </div>

  <h2 style="font-size: 17px; font-weight: bold; color: #1a1a1a; margin: 15px 0;">
    第一部分标题
  </h2>

  <p style="margin: 15px 0; text-align: justify;">
    正文内容。可以使用 <strong style="color: {{PRIMARY_COLOR}};">加粗强调</strong> 来突出关键词。
  </p>

  <!-- Bullet points (if needed) -->
  <ul style="margin: 15px 0; padding-left: 20px;">
    <li style="margin: 8px 0; line-height: 1.75;">要点一</li>
    <li style="margin: 8px 0; line-height: 1.75;">要点二</li>
    <li style="margin: 8px 0; line-height: 1.75;">要点三</li>
  </ul>

  <!-- Image 1 (after first section) -->
  <div style="text-align: center; margin: 30px 0;">
    <img src="[IMAGE_PLACEHOLDER_1]" alt="图片描述" style="max-width: 100%; width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
    <p style="font-size: 12px; color: #999; text-align: center; margin-top: 10px;">
      图片说明文字
    </p>
  </div>

  <!-- Section 02 -->
  <div style="margin: 40px 0 10px 0;">
    <span style="display: inline-block; font-size: 18px; font-weight: bold; color: {{PRIMARY_COLOR}}; padding: 5px 15px; border-left: 4px solid {{PRIMARY_COLOR}};">
      02.
    </span>
  </div>

  <h2 style="font-size: 17px; font-weight: bold; color: #1a1a1a; margin: 15px 0;">
    第二部分标题
  </h2>

  <p style="margin: 15px 0; text-align: justify;">
    更多正文内容...
  </p>

  <!-- Highlight box (optional) -->
  <div style="background: {{ACCENT_COLOR}}; border-left: 4px solid {{PRIMARY_COLOR}}; padding: 15px 20px; margin: 20px 0; border-radius: 4px;">
    <p style="margin: 0; color: #3f3f3f; font-size: 14px;">
      💡 <strong>小贴士:</strong> 重要提示或补充信息放在这里
    </p>
  </div>

  <!-- Image 2 -->
  <div style="text-align: center; margin: 30px 0;">
    <img src="[IMAGE_PLACEHOLDER_2]" alt="图片描述" style="max-width: 100%; width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
  </div>

  <!-- Section 03 (if needed) -->
  <div style="margin: 40px 0 10px 0;">
    <span style="display: inline-block; font-size: 18px; font-weight: bold; color: {{PRIMARY_COLOR}}; padding: 5px 15px; border-left: 4px solid {{PRIMARY_COLOR}};">
      03.
    </span>
  </div>

  <h2 style="font-size: 17px; font-weight: bold; color: #1a1a1a; margin: 15px 0;">
    第三部分标题
  </h2>

  <p style="margin: 15px 0; text-align: justify;">
    最后部分内容...
  </p>

  <!-- Conclusion -->
  <div style="margin: 40px 0 20px 0; padding: 20px; background: #f8f8f8; border-radius: 8px; text-align: center;">
    <p style="margin: 0; font-size: 15px; color: #3f3f3f; line-height: 1.8;">
      总结性语句或结束语
    </p>
  </div>

  <!-- Footer CTA -->
  <div style="margin: 30px 0 0 0; padding: 20px; border-top: 1px solid #e0e0e0; text-align: center;">
    <p style="margin: 0; font-size: 14px; color: #666;">
      📌 更多相关内容,关注主页查看~
    </p>
  </div>

</section>
```

## Color Scheme Variables

Replace these placeholders with actual colors based on content type:

- `{{PRIMARY_COLOR}}` - Main accent color for headings, section numbers, emphasis
- `{{ACCENT_COLOR}}` - Light background color for highlight boxes (usually primary color at 10-15% opacity)

### Color Schemes by Content Type

#### Tech/Business (蓝色系)
```
PRIMARY_COLOR: #1E88E5
ACCENT_COLOR: #E3F2FD
```

#### Lifestyle/Food (莫兰迪色系)
```
PRIMARY_COLOR: #A8DADC
ACCENT_COLOR: #F1FAEE
```

#### Motivational/Energy (橙黄色系)
```
PRIMARY_COLOR: #FF6B35
ACCENT_COLOR: #FFF3E0
```

#### Education/Knowledge (青绿色系)
```
PRIMARY_COLOR: #00897B
ACCENT_COLOR: #E0F2F1
```

#### Luxury/Premium (紫金色系)
```
PRIMARY_COLOR: #7B1FA2
ACCENT_COLOR: #F3E5F5
```

#### Health/Wellness (绿色系)
```
PRIMARY_COLOR: #43A047
ACCENT_COLOR: #E8F5E9
```

## HTML Components Library

### 1. Quote Block

```html
<div style="border-left: 4px solid {{PRIMARY_COLOR}}; padding-left: 15px; margin: 20px 0; font-style: italic; color: #666;">
  <p style="margin: 5px 0;">引用文字或名言</p>
  <p style="margin: 5px 0; font-size: 13px; color: #999;">— 来源或作者</p>
</div>
```

### 2. Numbered List (Custom Style)

```html
<div style="margin: 20px 0;">
  <div style="display: flex; margin: 15px 0;">
    <div style="flex-shrink: 0; width: 28px; height: 28px; background: {{PRIMARY_COLOR}}; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; margin-right: 12px;">1</div>
    <div style="flex: 1;">
      <p style="margin: 0;">第一点内容</p>
    </div>
  </div>

  <div style="display: flex; margin: 15px 0;">
    <div style="flex-shrink: 0; width: 28px; height: 28px; background: {{PRIMARY_COLOR}}; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; margin-right: 12px;">2</div>
    <div style="flex: 1;">
      <p style="margin: 0;">第二点内容</p>
    </div>
  </div>
</div>
```

### 3. Tip Box (带图标)

```html
<div style="background: {{ACCENT_COLOR}}; border-left: 4px solid {{PRIMARY_COLOR}}; padding: 15px 20px; margin: 20px 0; border-radius: 4px;">
  <p style="margin: 0 0 10px 0; font-weight: bold; color: {{PRIMARY_COLOR}};">
    💡 温馨提示
  </p>
  <p style="margin: 0; color: #3f3f3f; font-size: 14px;">
    提示内容文字
  </p>
</div>
```

### 4. Two-Column Layout (Mobile-Friendly)

```html
<div style="display: flex; gap: 15px; margin: 20px 0; flex-wrap: wrap;">
  <div style="flex: 1; min-width: 200px; padding: 15px; background: #f8f8f8; border-radius: 8px;">
    <h3 style="margin: 0 0 10px 0; font-size: 16px; color: {{PRIMARY_COLOR}};">左侧标题</h3>
    <p style="margin: 0; font-size: 14px;">左侧内容</p>
  </div>
  <div style="flex: 1; min-width: 200px; padding: 15px; background: #f8f8f8; border-radius: 8px;">
    <h3 style="margin: 0 0 10px 0; font-size: 16px; color: {{PRIMARY_COLOR}};">右侧标题</h3>
    <p style="margin: 0; font-size: 14px;">右侧内容</p>
  </div>
</div>
```

### 5. Divider Line

```html
<div style="margin: 30px 0; text-align: center;">
  <div style="display: inline-block; width: 50px; height: 3px; background: {{PRIMARY_COLOR}};"></div>
</div>
```

### 6. Image with Caption

```html
<div style="text-align: center; margin: 30px 0;">
  <img src="[IMAGE_URL]" alt="描述" style="max-width: 100%; width: 100%; height: auto; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
  <p style="font-size: 12px; color: #999; text-align: center; margin-top: 10px; font-style: italic;">
    图片说明文字
  </p>
</div>
```

### 7. Call-to-Action Button

```html
<div style="text-align: center; margin: 30px 0;">
  <a href="[LINK_URL]" style="display: inline-block; padding: 12px 40px; background: {{PRIMARY_COLOR}}; color: white; text-decoration: none; border-radius: 25px; font-size: 15px; font-weight: bold; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
    点击查看更多
  </a>
</div>
```

### 8. Stats or Data Display

```html
<div style="display: flex; gap: 10px; margin: 25px 0; flex-wrap: wrap;">
  <div style="flex: 1; min-width: 100px; text-align: center; padding: 20px; background: {{ACCENT_COLOR}}; border-radius: 8px;">
    <div style="font-size: 28px; font-weight: bold; color: {{PRIMARY_COLOR}}; margin-bottom: 5px;">80%</div>
    <div style="font-size: 13px; color: #666;">用户满意度</div>
  </div>
  <div style="flex: 1; min-width: 100px; text-align: center; padding: 20px; background: {{ACCENT_COLOR}}; border-radius: 8px;">
    <div style="font-size: 28px; font-weight: bold; color: {{PRIMARY_COLOR}}; margin-bottom: 5px;">10万+</div>
    <div style="font-size: 13px; color: #666;">阅读量</div>
  </div>
  <div style="flex: 1; min-width: 100px; text-align: center; padding: 20px; background: {{ACCENT_COLOR}}; border-radius: 8px;">
    <div style="font-size: 28px; font-weight: bold; color: {{PRIMARY_COLOR}}; margin-bottom: 5px;">500+</div>
    <div style="font-size: 13px; color: #666;">分享次数</div>
  </div>
</div>
```

## Image Placement Guidelines

### Optimal Image Count: 2-3 images per article

**Image 1 Placement:**
- After introduction and first section
- Should illustrate the main topic or concept
- Suggested position: After Section 01 content

**Image 2 Placement:**
- Middle of article (after Section 02)
- Should support or visualize key points
- Helps break up text for better readability

**Image 3 Placement (optional):**
- Near conclusion or after final section
- Summary visual or call-to-action related
- Use only if article is longer (>1500 words)

### Image Specifications

- **Width**: 100% (responsive)
- **Max-width**: 750px for desktop
- **Format**: JPG or PNG
- **File size**: < 500KB for fast loading
- **Aspect ratio**: 16:9 or 4:3 recommended
- **Border radius**: 8px for modern look
- **Box shadow**: Subtle shadow for depth

### Image Placeholder Format

Use descriptive placeholders:
```html
[IMAGE_PLACEHOLDER_1: 展示产品使用场景的高清照片]
[IMAGE_PLACEHOLDER_2: 数据图表或信息图]
[IMAGE_PLACEHOLDER_3: 团队合影或活动现场]
```

## Typography Guidelines for HTML

### Font Families
Primary: `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif`

This ensures optimal rendering across iOS, Android, and desktop.

### Font Sizes
- Main Title (h1): 24px
- Section Headers (h2): 17px
- Body Text: 15px
- Captions/Annotations: 12-13px
- Subtitles: 14px

### Line Heights
- Headings: 1.3-1.4
- Body text: 1.75
- Captions: 1.5

### Letter Spacing
- Body text: 0.5px
- Headings: 0px (default)

## Mobile Optimization Checklist

- [ ] Max-width set to 750px with centering
- [ ] All images use `max-width: 100%` for responsiveness
- [ ] Font sizes are readable on small screens (minimum 14px)
- [ ] Padding/margins use relative units or appropriate px values
- [ ] Touch-friendly spacing between interactive elements
- [ ] Flex layouts use `flex-wrap: wrap` for mobile stacking
- [ ] No fixed widths except for containers

## WeChat Editor Compatibility

### Tested and Compatible With:
- ✅ 135编辑器 (135editor.com)
- ✅ 秀米编辑器 (xiumi.us)
- ✅ 96编辑器 (96weixin.com)
- ✅ i排版编辑器 (ipaiban.com)
- ✅ 微信公众号原生编辑器

### Copy-Paste Workflow:
1. Generate complete HTML code following this template
2. Copy the entire `<section>...</section>` block
3. Open WeChat editor in "HTML mode" or "Source code mode"
4. Paste the HTML
5. Switch back to visual mode
6. Replace image placeholders with actual images
7. Preview on mobile before publishing

## Example Output Format

When generating HTML for users, present it like this:

````markdown
## 格式化完成!

以下是您的文章HTML代码,可直接复制到微信编辑器使用:

```html
<section style="...">
  <!-- Your complete HTML here -->
</section>
```

### 使用说明:
1. 复制上方完整HTML代码
2. 在编辑器中切换到"HTML模式"或"源代码模式"
3. 粘贴代码
4. 切换回可视化模式
5. 替换图片占位符 [IMAGE_PLACEHOLDER_1] 等为实际图片
6. 手机预览后发布

### 配色方案:
- 主色调: #1E88E5 (科技蓝)
- 强调色: #E3F2FD (浅蓝背景)

### 建议配图 (2张):
1. [IMAGE_PLACEHOLDER_1: 产品功能演示截图]
2. [IMAGE_PLACEHOLDER_2: 用户使用场景照片]
````

## Advanced Techniques

### Gradient Headers

```html
<h1 style="font-size: 24px; font-weight: bold; background: linear-gradient(135deg, {{PRIMARY_COLOR}}, #667eea); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin: 20px 0;">
  渐变标题效果
</h1>
```

### Card-Style Sections

```html
<div style="background: white; border-radius: 12px; padding: 20px; margin: 20px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
  <h3 style="margin: 0 0 15px 0; color: {{PRIMARY_COLOR}}; font-size: 17px;">卡片标题</h3>
  <p style="margin: 0; color: #3f3f3f; line-height: 1.75;">卡片内容</p>
</div>
```

### Timeline Layout

```html
<div style="position: relative; padding-left: 30px; margin: 30px 0;">
  <div style="position: absolute; left: 0; top: 0; bottom: 0; width: 2px; background: {{PRIMARY_COLOR}};"></div>

  <div style="position: relative; margin-bottom: 25px;">
    <div style="position: absolute; left: -35px; top: 5px; width: 12px; height: 12px; background: {{PRIMARY_COLOR}}; border-radius: 50%; border: 2px solid white;"></div>
    <h4 style="margin: 0 0 8px 0; font-size: 16px; color: #1a1a1a;">2024年1月</h4>
    <p style="margin: 0; font-size: 14px; color: #666;">发生的事件描述</p>
  </div>

  <div style="position: relative; margin-bottom: 25px;">
    <div style="position: absolute; left: -35px; top: 5px; width: 12px; height: 12px; background: {{PRIMARY_COLOR}}; border-radius: 50%; border: 2px solid white;"></div>
    <h4 style="margin: 0 0 8px 0; font-size: 16px; color: #1a1a1a;">2024年6月</h4>
    <p style="margin: 0; font-size: 14px; color: #666;">另一个事件描述</p>
  </div>
</div>
```
