# workbuddy-skills

WorkBuddy Skills Collection — 个人 AI 技能仓库

## 技能列表

| 技能名称 | 版本 | 描述 | 安装命令 |
|----------|------|------|----------|
| stock-limit-60ma | v1.0.0 | 筛选当日涨停且股价上穿 60 日均线的股票，适用于短线选股、打板策略、趋势跟踪 | `skhub install stock-limit-60ma` |

## 目录结构

```
workbuddy-skills/
├── README.md
└── skills/
    └── stock-limit-60ma/
        ├── SKILL.md
        ├── README.md
        ├── _meta.json
        ├── scripts/
        │   └── filter_limit_60ma.py
        └── references/
```

## 安装方式

### 方式一：skhub CLI 安装

```bash
skhub install https://github.com/lisa20150928/workbuddy-skills/raw/main/skills/stock-limit-60ma
```

### 方式二：手动安装

1. 下载对应技能目录
2. 解压到 `~/.workbuddy/skills/`
3. 重启 WorkBuddy 即可使用

## 作者

[lisa20150928](https://github.com/lisa20150928)
