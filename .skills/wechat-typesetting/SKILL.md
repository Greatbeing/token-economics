---
name: wechat-typesetting
description: Professional WeChat Official Account typesetting and formatting guide with HTML output. Use this skill when creating or formatting WeChat public account articles, designing article layouts, choosing color schemes, optimizing readability, or helping users improve their WeChat content presentation. Automatically generates beautifully formatted HTML output with intelligent color selection based on content type and 2-3 contextual images.
---

# WeChat Official Account Typesetting

## Overview

Transform WeChat articles from text dumps into professional, reader-friendly HTML content. This skill provides systematic typesetting guidelines covering typography, color schemes, spacing, visual hierarchy, and image usage - all optimized for mobile reading and attention retention. **Outputs production-ready HTML that can be directly copied into WeChat editors.**

## When to Use This Skill

Activate this skill when users request help with:
- Formatting WeChat public account articles (outputs HTML)
- Choosing color schemes and fonts for WeChat content
- Improving article readability and visual appeal
- Designing article layouts and structure
- Converting plain text to formatted WeChat articles
- Creating style guides for WeChat accounts
- Optimizing content for mobile reading

## Output Format

**IMPORTANT:** When formatting articles, always output HTML code that follows the WeChat HTML Template structure detailed in `references/html-output-guide.md`. The HTML should be:
- Copy-paste ready for WeChat editors (135编辑器, 秀米, etc.)
- Mobile-optimized with proper viewport settings
- Intelligently color-coded based on article content type
- Include 2-3 contextual images with proper sizing

## Core Typesetting Principles

### 1. Purpose-Driven Design

Typesetting serves three critical functions:

**Rescue Fragmented Attention**
- Readers have 3-second attention spans (subway, restroom, work breaks)
- Clean layouts enable "painless reading"
- Avoid: Rainbow colors + dense text = instant bounce

**Visual Navigation System**
- Guide readers to key points instantly
- Hierarchical headings act as roadmap signposts
- Keyword highlighting enables 3-second information capture

**Visual Brand Identity**
- Consistent typesetting = recognizable brand signature
- Just like Coca-Cola's red/black or Zhihu's blue/white
- Maintain style for 3+ months to establish brand imprint

### 2. Style Consistency Formula

```
Style = Title Format + Primary Color + Text Format + Image Style + Header/Footer Guide
```

**Critical Rule:** Stick to ONE style for 3+ months. Switching styles (literary today, cyberpunk tomorrow) causes follower loss.

## Typography Specifications

### Font Size Guidelines

```
12px  → Annotations, source citations
14px  → Compact elegant style (literary accounts)
15px  → Safe default (never wrong)
16px  → Larger text (less refined visually)
17px  → Section headers

Note: Add +2px for elderly audiences
```

**Recommendation:** Use 14px or 15px for body text to balance readability and aesthetics.

### Spacing for Breathing Room

**Character Spacing:** 1-1.5px (avoid QR code compression)

**Line Spacing:** 1.5-1.75x (intimate but not invasive)

**Paragraph Spacing:**
- Between paragraphs → 1 blank line
- Between sections → 2 lines above + 1 line below

**Side Margins:** 8-16px (edge whitespace reduces reading pressure)

### Alignment Principles

- **Body text** → Justified alignment (no ragged right edge)
- **Short text/annotations** → Center alignment (instant premium feel)

## Color Strategy

### Golden Rule: 1 Primary + ≤2 Supporting Colors

Using consistent primary color increases reading continuity. Rainbow text creates fragmentation and chaos.

### Color Psychology

**Energetic & Positive**
- Orange, Yellow
- Use for: Motivational, uplifting content

**Professional & Business**
- Blue, Gray, Red
- Use for: Corporate, formal content

**Fresh & Artistic**
- Morandi palette (low saturation YYDS!)
- Use for: Lifestyle, aesthetic content

### Body Text Color

**Recommended:** #595959 or #3f3f3f (softer than pure black #000000)

**Emphasis Color:** Use primary brand color + bold (e.g., #FF0000)

**Critical Rule:** ≤3 highlighted items per screen. Everything highlighted = nothing highlighted!

### Color Resources

Reference `references/color-resources.md` for recommended color palette websites.

## Image Guidelines

### Cover Image Specifications

**Primary image:** 900×383px (2.35:1 golden ratio)
**Secondary image:** 200×200px (1:1 square)

### Techniques

- Add borders → Focus viewer attention
- Center + enlarge → Emphasize key points
- Emotion transmission → Laugh/cry/surprise emojis grab eyeballs

### Four Principles for In-Article Images

1. **No blurriness** (HD is baseline!)
2. **No copyright violations** (beware legal letters!)
3. **No style clashes** (maintain consistency!)
4. **Optimal quantity** (2-3 images/article recommended for balance)

### AI Image Tools

See `references/ai-tools.md` for AI-powered cover generation and image creation resources.

## Typesetting Tools

### Recommended Editors

1. **135 Editor** - All-around champion (author's favorite)
   - https://www.135editor.com/

2. **Xiumi Editor** - Fresh style & layout master
   - https://xiumi.us/

3. **96 Editor** - Free user's blessing
   - https://bj.96weixin.com/

4. **iPaiban Editor** - Black tech player essential
   - https://x.ipaiban.com/

5. **Yiban Assistant** - WeChat backend "cheat code"
   - https://yiban.io/

6. **Native WeChat Editor** - Minimalist choice
   - https://mp.weixin.qq.com/

Detailed tool comparison available in `references/tools-comparison.md`.

## Quality Checklist

Before publishing, ask these three soul-searching questions:

1. **Can readers find key points in 3 seconds?**
2. **Does it hurt to look at on mobile screen?**
3. **Does the entire style feel unified like one person wrote it?**

**Ultimate Principle:** Typesetting serves readers, not self-gratification!

## Workflow for Creating WeChat Articles

### Step 1: Analyze Content & Choose Color Scheme

**Automatic Color Selection Based on Content Type:**

Analyze the article content and select appropriate color scheme:

- **Tech/Business** → Blue scheme (#1E88E5, #2C73D2, #E3F2FD)
- **Lifestyle/Food** → Morandi scheme (#A8DADC, #E5989B, #F1FAEE)
- **Motivational/Energy** → Orange/Yellow scheme (#FF6B35, #FFE66D, #FFF3E0)
- **Education/Knowledge** → Teal scheme (#00897B, #4DB6AC, #E0F2F1)
- **Luxury/Premium** → Purple/Gold scheme (#7B1FA2, #BA68C8, #F3E5F5)
- **Health/Wellness** → Green scheme (#43A047, #81C784, #E8F5E9)

Use `scripts/color_selector.py` to programmatically determine the best color scheme.

### Step 2: Structure Content with HTML

Apply HTML structure following the template in `assets/base-template.html`:
- Semantic HTML5 tags (section, article, header)
- Main title with appropriate heading level
- Section numbers (01., 02., etc.) in styled divs
- Bold section headers with color accents
- Paragraph breaks every 3-5 lines
- Strategic whitespace using margin/padding

### Step 3: Apply Color & Emphasis

- Highlight ≤3 key points per section using `<strong>` with primary color
- Use primary color consistently for headings and accents
- Apply text color (#3f3f3f) for readability
- Add emoji for emotional emphasis (sparingly)

### Step 4: Insert & Optimize Images

- Add 2-3 images using `<img>` tags with:
  - Proper width (100% with max-width: 600px)
  - Centered alignment
  - Border radius for modern look
  - Alt text for accessibility
- Suggest relevant placeholder image descriptions
- Images should be contextually relevant to surrounding content

### Step 5: Generate Final HTML

Output complete HTML code following this structure:

```html
<section style="...">
  <!-- Title -->
  <h1 style="...">Article Title</h1>

  <!-- Intro -->
  <p style="...">Introduction text...</p>

  <!-- Section 01 -->
  <div class="section-number" style="...">01.</div>
  <h2 style="...">Section Title</h2>
  <p style="...">Content...</p>

  <!-- Image 1 -->
  <div style="text-align: center; margin: 30px 0;">
    <img src="[IMAGE_PLACEHOLDER_1]" alt="..." style="...">
    <p style="font-size: 12px; color: #999; text-align: center;">Image caption</p>
  </div>

  <!-- More sections and images -->

  <!-- Footer CTA -->
  <div style="...">
    📌 Call to action text
  </div>
</section>
```

See `references/html-output-guide.md` for complete template and styling details.

## Common Mistakes to Avoid

1. **Rainbow chaos** - Using 5+ colors destroys coherence
2. **Wall of text** - No spacing = instant reader fatigue
3. **Highlight overload** - Too many emphasized words = no emphasis
4. **Inconsistent style** - Switching fonts/colors mid-article
5. **Giant font sizes** - 18px+ body text lacks refinement
6. **Missing visual breaks** - No images or section dividers
7. **Center-aligning body text** - Hard to read on mobile
8. **Ignoring mobile preview** - Always check phone display before publishing

## Resources

### scripts/
- `color_selector.py` - Automatically determine color scheme based on article content keywords

### references/
Contains detailed supplementary information:
- `html-output-guide.md` - Complete HTML template structure and styling guide
- `color-resources.md` - Color palette websites and tools
- `ai-tools.md` - AI image generation for covers and illustrations
- `tools-comparison.md` - Detailed comparison of WeChat editors
- `examples.md` - Real-world before/after formatting examples

### assets/
- `base-template.html` - Complete WeChat HTML template with inline styles
- `template-tech.html` - Technology/Business style example
- `template-lifestyle.html` - Lifestyle/Food style example
- `template-motivational.html` - Motivational/Energy style example

Use these templates as starting points. The HTML is designed to work in all major WeChat editors (135编辑器, 秀米, etc.).
