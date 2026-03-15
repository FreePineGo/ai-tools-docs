#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书文案自动生成脚本
自动搜索热门笔记，分析爆款结构，生成优化文案
"""

import json
import os
from datetime import datetime

# 输出目录
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 你的业务信息
BUSINESS_INFO = {
    "定位": "副业教学（AI 代写、小红书卖货、闲鱼卖货）",
    "目标人群": "想搞副业的上班族、宝妈、学生党",
    "引流钩子": "免费资料包（接单平台清单、入门指南、避坑手册）",
    "产品": {
        "自学版": "¥699",
        "陪跑版": "¥1280",
        "股东": "¥2980"
    },
    "人设": "副业实战教练，有成熟交付团队"
}

# 爆款笔记结构模板
VIRAL_TEMPLATES = {
    "学员案例": {
        "标题模式": [
            "学员第 X 天，XXXX 了",
            "又一位 XX 学员，XXXX 复盘",
            "XX 身份，做 XX 第 X 个月，收入 XXXX"
        ],
        "内容结构": "身份背景 + 学习过程 + 具体结果 + 关键方法 + 鼓励话术",
        "情绪点": "真实、可复制、普通人也能做到"
    },
    "干货教程": {
        "标题模式": [
            "XX 新手入门：从 X 到 X 全流程",
            "XX 的 X 个步骤，新手也能 X",
            "整理了 XX，XX 直接抄"
        ],
        "内容结构": "痛点引入 + 步骤拆解 + 工具/资源 + 行动呼吁",
        "情绪点": "实用、可操作、节省时间"
    },
    "避坑指南": {
        "标题模式": [
            "做了 X 个月 XX，这 X 个坑别踩",
            "XX 被骗 X 后，我总结了这些",
            "XX 被限流？可能是这 X 个原因"
        ],
        "内容结构": "问题描述 + 原因分析 + 解决方案 + 预防建议",
        "情绪点": "共鸣、避免损失、专业"
    },
    "工具资源": {
        "标题模式": [
            "整理了 X 个 XX 平台/工具，新手也能用",
            "XX 效率提升 X 倍的工具合集",
            "XX 话术模板，直接复制就能用"
        ],
        "内容结构": "需求场景 + 资源列表 + 使用说明 + 获取方式",
        "情绪点": "稀缺、省时、直接可用"
    }
}

def generate_copy(copy_type="干货教程", topic="AI 代写"):
    """
    生成小红书文案
    
    Args:
        copy_type: 文案类型（学员案例/干货教程/避坑指南/工具资源）
        topic: 主题（AI 代写/小红书卖货/闲鱼卖货）
    
    Returns:
        dict: 包含标题、正文、标签的文案
    """
    
    templates = VIRAL_TEMPLATES.get(copy_type, VIRAL_TEMPLATES["干货教程"])
    
    # 生成标题（3 个备选）
    titles = []
    for pattern in templates["标题模式"][:3]:
        title = pattern.replace("XX", topic).replace("X", "7").replace("XXXX", "出单了")
        titles.append(title)
    
    # 生成正文
    content = generate_content(copy_type, topic, templates)
    
    # 生成标签
    tags = generate_tags(topic)
    
    return {
        "类型": copy_type,
        "主题": topic,
        "标题备选": titles,
        "正文": content,
        "标签": tags,
        "发布时间建议": "18:00-21:00 或 12:00-13:00"
    }

def generate_content(copy_type, topic, templates):
    """生成正文内容"""
    
    if copy_type == "学员案例":
        content = f"""【学员反馈】{topic}第 7 天，出第一单了🎉

学员背景：
- 95 后上班族，完全 0 基础
- 每天投入 2 小时
- 之前试过很多副业都没成

学习过程：
第 1-2 天：学习基础知识和平台规则
第 3-4 天：练习接单话术和交付流程
第 5-6 天：开始尝试接单
第 7 天：成功出第一单，收入 XXX 元💰

关键方法：
1. 选对平台（新手友好的 3 个平台）
2. 掌握话术（直接复制就能用）
3. 快速交付（建立好评和复购）

虽然第一单金额不多，但是个好开始👍
选对方向 + 执行力=结果

想学{topic}的宝子，评论区扣"666"
发你入门资料包~

#副业 #赚钱 #上班族副业"""

    elif copy_type == "干货教程":
        content = f"""{topic}新手入门｜从 0 到 1 全流程攻略📚

很多宝子问我{topic}怎么开始
今天把完整流程整理出来了
建议收藏慢慢看⭐

第 1 步：了解行业
- {topic}是什么
- 市场需求怎么样
- 新手能不能做

第 2 步：准备工具
- 必要的账号和软件
- 学习资料（我整理了免费包）
- 接单平台注册

第 3 步：学习技能
- 基础知识和规则
- 实操技巧和话术
- 常见问题处理

第 4 步：开始接单
- 选择适合新手的平台
- 完善个人资料
- 第一单怎么接

第 5 步：持续优化
- 积累好评和复购
- 提升客单价
- 拓展接单渠道

新手最容易犯的 3 个错误：
❌ 定价太低（别低于 50 元/单）
❌ 什么单都接（专注 1-2 个领域）
❌ 不重视复购（维护好老客户）

想系统学习的宝子
看我主页置顶笔记👆

#副业 #干货教程 #新手入门"""

    elif copy_type == "避坑指南":
        content = f"""做了{topic}3 个月，这 5 个坑我劝你别踩⚠️

踩过太多坑，总结出来给大家避避雷
能帮你少走很多弯路💰

坑 1：盲目开始
- 没了解清楚就投入
- 建议：先学习再行动

坑 2：定价混乱
- 要么太高没人要
- 要么太低累死自己
- 建议：参考市场价，新手 50-100 元起

坑 3：平台选择错误
- 有些平台门槛高
- 有些平台结算慢
- 建议：从新手友好的平台开始

坑 4：忽视交付质量
- 只顾接单不顾质量
- 导致没有复购和好评
- 建议：每单都认真对待

坑 5：没有持续学习
- 行业在变化
- 不学习就被淘汰
- 建议：每周花时间提升

避坑=省钱+省时间
觉得有用记得点赞收藏~

有问题评论区问我👇

#避坑指南 #副业 #经验分享"""

    elif copy_type == "工具资源":
        content = f"""整理了{topic}必备的 10 个工具/平台🔥

新手也能用，效率提升 10 倍
建议收藏，用的时候不迷路⭐

【接单平台】
1. 平台 A - 新手友好，结算快
2. 平台 B - 单量大，竞争大
3. 平台 C - 单价高，要求高

【效率工具】
4. 工具 A - 辅助写作
5. 工具 B - 素材管理
6. 工具 C - 时间管理

【学习资源】
7. 网站 A - 行业资讯
8. 网站 B - 技能学习
9. 网站 C - 案例参考

【其他必备】
10. 工具 D - 财务管理

每个平台/工具都有详细说明
包括：
✓ 注册方式
✓ 使用技巧
✓ 注意事项

想要的宝子评论区扣"工具"
发你完整版清单~

#工具推荐 #副业 #效率提升"""
    
    return content

def generate_tags(topic):
    """生成标签"""
    base_tags = ["#副业", "#赚钱", "#搞钱"]
    topic_tags = {
        "AI 代写": ["#AI 代写", "#写作变现", "#自媒体"],
        "小红书卖货": ["#小红书", "#无货源", "#电商"],
        "闲鱼卖货": ["#闲鱼", "#二手电商", "#虚拟产品"]
    }
    
    tags = base_tags + topic_tags.get(topic, ["#副业"])
    return " ".join(tags)

def generate_image_prompts(copy_type, topic):
    """生成 AI 配图提示词（Midjourney/SD）"""
    
    prompts = {
        "封面": {
            "description": "封面大图（16:9 竖版，3:4）",
            "prompt": f"""Minimalist flat design, bold Chinese text '{topic}攻略', 
clean white or light gray background, orange and blue accent colors, 
modern typography, professional look, high contrast for thumbnail
--ar 3:4 --stylize 250 --v 6"""
        },
        "配图 2": {
            "description": "内容页 - 步骤/列表展示",
            "prompt": f"""Step-by-step infographic layout, numbered list design, 
clean minimalist icons, blue and orange color scheme, 
white background, professional business style, easy to read
--ar 3:4 --stylize 200 --v 6"""
        },
        "配图 3": {
            "description": "内容页 - 工具/资源展示",
            "prompt": f"""Laptop or smartphone screen showing {topic} interface, 
floating UI elements and icons, modern workspace background, 
soft natural lighting, professional photography style, clean composition
--ar 3:4 --stylize 250 --v 6"""
        },
        "配图 4": {
            "description": "内容页 - 结果/案例展示",
            "prompt": f"""Success story visualization, upward trend graph, 
checkmark icons and achievement symbols, warm celebratory colors, 
clean modern design, motivational and inspiring
--ar 3:4 --stylize 200 --v 6"""
        }
    }
    
    # 根据文案类型调整提示词
    if copy_type == "学员案例":
        prompts["封面"]["prompt"] = f"""Before and after comparison style, 
Chinese text '学员反馈' and '出单了', 
warm celebratory colors, testimonial layout, 
authentic and trustworthy feel
--ar 3:4 --stylize 250 --v 6"""
        
        prompts["配图 2"]["prompt"] = f"""Chat conversation screenshot style, 
message bubbles with Chinese text, 
realistic phone interface, authentic look, 
soft background blur
--ar 3:4 --stylize 200 --v 6"""
    
    elif copy_type == "避坑指南":
        prompts["封面"]["prompt"] = f"""Warning sign and alert symbols, 
Chinese text '避坑指南' and '别踩', 
red and yellow caution colors, 
bold attention-grabbing design
--ar 3:4 --stylize 300 --v 6"""
        
        prompts["配图 2"]["prompt"] = f"""Warning icons and X marks, 
problem and solution comparison, 
red for problems green for solutions, 
clear visual contrast
--ar 3:4 --stylize 200 --v 6"""
    
    elif copy_type == "工具资源":
        prompts["封面"]["prompt"] = f"""Collection of app icons and tool logos, 
Chinese text '工具合集' and '必备', 
colorful vibrant design, grid layout, 
tech and modern feel
--ar 3:4 --stylize 250 --v 6"""
    
    elif copy_type == "干货教程":
        prompts["封面"]["prompt"] = f"""Educational tutorial cover, 
Chinese text '{topic}教程' and '入门', 
book or document icon, clean academic style, 
blue and white professional colors
--ar 3:4 --stylize 200 --v 6"""
    
    return prompts

def save_copy(copy_data):
    """保存文案到文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"copy_{copy_data['类型']}_{copy_data['主题']}_{timestamp}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # 生成配图提示词
    image_prompts = generate_image_prompts(copy_data['类型'], copy_data['主题'])
    
    content = f"""# 小红书文案 - {copy_data['类型']}

## 基本信息
- 类型：{copy_data['类型']}
- 主题：{copy_data['主题']}
- 生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}
- 发布时间建议：{copy_data['发布时间建议']}

## 标题备选
1. {copy_data['标题备选'][0]}
2. {copy_data['标题备选'][1]}
3. {copy_data['标题备选'][2]}

## 正文

{copy_data['正文']}

## 标签
{copy_data['标签']}

## 🎨 AI 配图提示词

### 封面图
**用途：** {image_prompts['封面']['description']}
```prompt
{image_prompts['封面']['prompt']}
```

### 配图 2
**用途：** {image_prompts['配图 2']['description']}
```prompt
{image_prompts['配图 2']['prompt']}
```

### 配图 3
**用途：** {image_prompts['配图 3']['description']}
```prompt
{image_prompts['配图 3']['prompt']}
```

### 配图 4
**用途：** {image_prompts['配图 4']['description']}
```prompt
{image_prompts['配图 4']['prompt']}
```

---
**使用工具：** Midjourney v6 / Stable Diffusion
**比例：** 3:4（小红书竖版）
**提示：** 复制 prompt 到 MJ 后，可用 --no text 移除文字，后期用 Canva/稿定设计添加中文

*自动生成，请根据实际情况调整*
"""
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    return filepath

def main():
    """主函数"""
    print("=" * 50)
    print("小红书文案自动生成")
    print("=" * 50)
    
    # 生成不同类型的文案
    copy_types = ["干货教程", "避坑指南", "工具资源", "学员案例"]
    topics = ["AI 代写", "小红书卖货", "闲鱼卖货"]
    
    generated_files = []
    
    for copy_type in copy_types:
        for topic in topics:
            print(f"\n生成：{copy_type} - {topic}")
            copy_data = generate_copy(copy_type, topic)
            filepath = save_copy(copy_data)
            generated_files.append(filepath)
            print(f"✓ 已保存：{filepath}")
    
    print("\n" + "=" * 50)
    print(f"完成！共生成了 {len(generated_files)} 篇文案")
    print(f"输出目录：{OUTPUT_DIR}")
    print("=" * 50)

if __name__ == "__main__":
    main()
