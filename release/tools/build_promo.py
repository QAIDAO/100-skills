#!/usr/bin/env python3
"""生成宣发展示页（单文件、自包含）；版本号取自 CHANGELOG。

用法：python3 -I release/tools/build_promo.py --out <dir>
写出 <dir>/index.html。题目数据取自 problems/*/*/problem.json 与 release/stats.json；
叙述文字为固定措辞。不读时钟、不联网。难度与 starter 取自 problem.json 的 track 字段。

呈现重心：每道题为什么值得做（研发决策）、要算什么（可观测量），
以及「经典基线」与「量子方法的角色」的对照。题库为「左列表 + 右详情」双栏，另有侧边目录；
这两处最初在 QAIDAO.github.io 上手改，已并回本生成器，站点页面只从这里复制。
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOMAINS = {  # 目录 → (中文名, 题板色类名)
    "biomedicine": ("生物医药", "d-bio"),
    "applied-materials": ("应用材料", "d-mat"),
    "model-dynamics": ("材料模型与动力学", "d-dyn"),
    "extensions": ("交叉方向与算法", "d-ext"),
}
PARTS = (
    ("system", "研究体系", "算的是什么"),
    ("observable", "可观测量", "用什么数回答"),
    ("classical_baseline", "经典基线", "经典能做到哪"),
    ("quantum_role", "量子方法的角色", "量子放在哪一步"),
    ("decision", "研发决策", "支撑什么判断"),
)
SPECIMEN = "M01"
LEVELS = ("热身", "进阶", "前沿")
WARM_DEMO = "C11"  # 「从热身题开始」里演示的 starter
TOC = (  # 侧边目录：锚点与名称
    ("top", "开篇"), ("why", "为什么值得做"), ("anatomy", "一道题长什么样"), ("start", "从热身题开始"),
    ("problems", "题库"), ("reference", "现有参照"), ("join", "怎么参与"),
)
REPO = "https://github.com/QAIDAO/100-skills"
BLOB = f"{REPO}/blob/main"
CRITERION_RE = re.compile(r"^\d+\. \*\*(.+?)\*\*：(.+)$")
# 「为什么值得做」：主题词为固定措辞，决策句取自各题 problem.json 原文。
STAKES = (
    ("固氮", "B01"),
    ("碳捕集", "M17"),
    ("PFAS 治理", "M21"),
    ("电池电解液", "M15"),
    ("药物筛选", "B12"),
    ("高温超导", "F01"),
)
PIPELINE = (
    ("提交", "按模板提交，CI 校验格式"),
    ("审核", "五条验收标准都有回应"),
    ("复现", "他人按记录独立重跑"),
    ("采纳", "记入这道题的现有参照"),
    ("skill", "同类方法积累后提炼，署名全部来源作者"),
)

GRAIN = (
    "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E"
    "%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' stitchTiles='stitch'/%3E"
    "%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .55 0'/%3E%3C/filter%3E"
    "%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E\")"
)

CSS = """
@font-face{font-family:"Subscripts";src:local("PingFangSC-Regular"),local("Helvetica Neue"),local("Arial");unicode-range:U+2070-209F}
:root{
  --canvas:#f6f2f9;--surface:#fffcfe;--ink:#271b38;--muted:#665877;--faint:#968aa6;
  --rule:#e2d9ec;--rule-strong:#cdbfdc;--accent:#7442c4;--accent-ink:#5a2fa3;--accent-soft:#efe6fb;
  --deep:#1b1229;--deep-2:#241838;--on-deep:#f1ebf7;--on-deep-muted:#b6a8c8;--on-deep-faint:#7f7192;
  --bio:#7442c4;--mat:#a8732a;--dyn:#4b6699;--ext:#ad4f7d;
  --bio-n:#c6a6f7;--mat-n:#e6c48f;--dyn-n:#a6badf;--ext-n:#eba9c9;
  --warm:#2f9e6e;--warm-soft:#e3f4ec;--warm-ink:#1d7a52;
  --grain-opacity:.05;
  --serif:"Subscripts","Songti SC","STSong","Noto Serif SC","Source Han Serif SC",ui-serif,Georgia,serif;
  --sans:-apple-system,BlinkMacSystemFont,"SF Pro Text","PingFang SC","Hiragino Sans GB","Noto Sans SC","Microsoft YaHei",sans-serif;
  --mono:ui-monospace,"SF Mono",SFMono-Regular,Menlo,Consolas,monospace;
  --r-chip:4px;--r-control:8px;--r-panel:16px;
  --ease:cubic-bezier(.16,1,.3,1);
}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
  --canvas:#110c18;--surface:rgba(255,255,255,.035);--ink:#ece6f4;--muted:#a898bb;--faint:#7d6f8f;
  --rule:rgba(255,255,255,.08);--rule-strong:rgba(255,255,255,.14);--accent:#c3a3f5;--accent-ink:#d6c0fa;--accent-soft:rgba(195,163,245,.12);
  --deep:#0a0710;--deep-2:#140e1e;--bio:#c6a6f7;--mat:#e6c48f;--dyn:#a6badf;--ext:#eba9c9;--grain-opacity:.07;
  --warm:#6fd3a5;--warm-soft:rgba(111,211,165,.12);--warm-ink:#8fe0ba}}
:root[data-theme="dark"]{
  --canvas:#110c18;--surface:rgba(255,255,255,.035);--ink:#ece6f4;--muted:#a898bb;--faint:#7d6f8f;
  --rule:rgba(255,255,255,.08);--rule-strong:rgba(255,255,255,.14);--accent:#c3a3f5;--accent-ink:#d6c0fa;--accent-soft:rgba(195,163,245,.12);
  --deep:#0a0710;--deep-2:#140e1e;--bio:#c6a6f7;--mat:#e6c48f;--dyn:#a6badf;--ext:#eba9c9;--grain-opacity:.07;
  --warm:#6fd3a5;--warm-soft:rgba(111,211,165,.12);--warm-ink:#8fe0ba}
*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-padding-top:72px}
body{margin:0;background:var(--canvas);color:var(--ink);font:16px/1.75 var(--sans);-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}
body:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:50;background-image:GRAIN;opacity:var(--grain-opacity);mix-blend-mode:multiply}
a{color:inherit}button,input{font:inherit;color:inherit}button{cursor:pointer;touch-action:manipulation}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px;border-radius:2px}
h1,h2,h3,p,ol,ul,dl,dd{margin:0}ol,ul{padding:0;list-style:none}
main *{min-width:0}
.wrap{max-width:1180px;margin:0 auto;padding:0 40px}
.kicker{font:500 12px/1.4 var(--mono);letter-spacing:.08em;color:var(--accent-ink);text-transform:uppercase}
.num{font-family:var(--mono);font-variant-numeric:tabular-nums}
.skip{position:absolute;left:12px;top:-60px;background:var(--deep);color:var(--on-deep);padding:8px 12px;border-radius:var(--r-control);z-index:60}.skip:focus{top:12px}
.d-bio{--d:var(--bio);--dn:var(--bio-n)}.d-mat{--d:var(--mat);--dn:var(--mat-n)}.d-dyn{--d:var(--dyn);--dn:var(--dyn-n)}.d-ext{--d:var(--ext);--dn:var(--ext-n)}

header{position:sticky;top:0;z-index:20;background:var(--canvas);border-bottom:1px solid var(--rule)}
.nav{height:60px;display:flex;align-items:center;gap:28px}
.brand{font:600 17px/1 var(--mono);text-decoration:none;letter-spacing:-.01em}.brand b{color:var(--accent);font-weight:600}
.navlinks{display:flex;gap:24px;font-size:14px;margin-left:auto}.navlinks a{text-decoration:none;color:var(--muted)}
.nav .contribute{font-size:14px;text-decoration:none;color:var(--accent-ink);font-weight:600}
@media (hover:hover){.navlinks a:hover{color:var(--ink)}.nav .contribute:hover{text-decoration:underline}}

.btn{display:inline-flex;align-items:center;gap:10px;padding:12px 22px;border-radius:var(--r-control);background:var(--ink);color:var(--canvas);text-decoration:none;font-size:15px;font-weight:600;border:0;transition:transform 120ms var(--ease)}
.btn:active{transform:scale(.97)}
.btn svg{width:16px;height:16px;transition:transform 160ms var(--ease)}
@media (hover:hover){.btn:hover svg{transform:translateX(3px)}}
.textlink{font-size:15px;color:var(--accent-ink);text-decoration:none;font-weight:600}
@media (hover:hover){.textlink:hover{text-decoration:underline}}

/* 首屏：标题 + 题板（100 题排成 10×10） */
.hero{padding:72px 0 88px;border-bottom:1px solid var(--rule)}
.hero-grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.02fr);gap:64px;align-items:center}
.hero h1{font:600 clamp(38px,4.8vw,62px)/1.16 var(--serif);margin:18px 0 24px}
.hero h1 .num{font-weight:600;color:var(--accent)}
.lead{font-size:17px;color:var(--muted);max-width:32em}
.lead strong{color:var(--ink);font-weight:600}
.cta-row{display:flex;align-items:center;gap:24px;margin-top:32px;flex-wrap:wrap}
.figures{display:grid;grid-template-columns:repeat(3,auto);justify-content:start;margin-top:44px;border-top:1px solid var(--rule)}
.figures div{padding:16px 28px 0 0;margin-right:28px;border-right:1px solid var(--rule)}
.figures div:last-child{border-right:0;margin-right:0}
.figures b{display:block;font:600 30px/1.1 var(--mono);font-variant-numeric:tabular-nums;letter-spacing:-.02em}
.figures span{display:block;font-size:13px;color:var(--muted);margin-top:6px}

.board{position:relative;background:var(--deep);border:1px solid rgba(255,255,255,.07);color:var(--on-deep);border-radius:var(--r-panel);padding:28px 28px 24px;overflow:hidden;box-shadow:0 1px 0 rgba(255,255,255,.06) inset,0 24px 60px rgba(27,18,41,.28)}
.board:before{content:"";position:absolute;inset:0;background-image:GRAIN;opacity:.18;mix-blend-mode:screen;pointer-events:none}
.board-head{position:relative;display:flex;justify-content:space-between;align-items:baseline;gap:16px;margin-bottom:18px}
.board-head b{font:600 16px/1.4 var(--serif)}
.board-head span{font:500 12px/1 var(--mono);color:var(--on-deep-muted)}
.cells{position:relative;display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:6px}
.cell{aspect-ratio:1;display:grid;place-items:center;border:1px solid color-mix(in srgb,var(--dn) 55%,transparent);background:color-mix(in srgb,var(--dn) 7%,transparent);border-radius:5px;padding:0;font:600 10px/1 var(--mono);color:color-mix(in srgb,var(--dn) 88%,white);letter-spacing:-.02em;transition:transform 140ms var(--ease),background-color 140ms var(--ease);animation:rise .6s var(--ease) both;animation-delay:calc(var(--i) * 7ms)}
.cell:active{transform:scale(.92)}
@media (hover:hover){.cell:hover{transform:scale(1.12);background:color-mix(in srgb,var(--dn) 30%,transparent);position:relative;z-index:1}}
@keyframes rise{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.legend{position:relative;display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:18px;font-size:12px;color:var(--on-deep-muted)}
.legend span{display:inline-flex;align-items:center;gap:7px}
.legend i{width:9px;height:9px;border-radius:2px;background:var(--dn)}
.cell.warm{position:relative}
.cell.warm:after{content:"";position:absolute;top:3px;right:3px;width:5px;height:5px;border-radius:50%;background:var(--warm)}
.legend .warm-key i{width:7px;height:7px;border-radius:50%;background:var(--warm)}
.board-foot{position:relative;margin-top:18px;padding-top:16px;border-top:1px solid rgba(255,255,255,.1);font-size:14px;color:var(--on-deep-muted)}
.board-foot b{color:var(--on-deep);font-weight:600}

section{padding:96px 0 104px;scroll-margin-top:60px;border-bottom:1px solid var(--rule)}
.section-head{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:48px;align-items:end;margin-bottom:44px}
.section-head h2{font:600 clamp(28px,3.4vw,42px)/1.2 var(--serif);margin-top:12px}
.section-head p{color:var(--muted);max-width:36em}

/* 为什么值得做 */
.stakes{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));border-top:1px solid var(--rule-strong)}
.stake{display:flex;flex-direction:column;gap:12px;padding:26px 28px 28px 0;border-bottom:1px solid var(--rule);text-align:left;background:transparent;border-left:0;border-right:0;border-top:0;transition:transform 120ms var(--ease)}
.stake:active{transform:scale(.985)}
.stake:nth-child(3n+2),.stake:nth-child(3n+3){padding-left:28px;border-left:1px solid var(--rule)}
.stake .theme{font:600 30px/1.2 var(--serif);color:var(--d)}
.stake .why{font-size:16px;line-height:1.75}
.stake .src{margin-top:auto;display:flex;gap:10px;align-items:baseline;font-size:13px;color:var(--muted)}
.stake .src .num{color:var(--d);font-weight:600}
.stake .go{font-size:13px;font-weight:600;color:var(--accent-ink)}
@media (hover:hover){.stake:hover .go{text-decoration:underline}}

/* 一道题长什么样 */
.anatomy{display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);gap:64px;align-items:start}
.anatomy ol li{display:grid;grid-template-columns:40px minmax(0,1fr);gap:4px 12px;padding:14px 0;border-top:1px solid var(--rule)}
.anatomy ol li:last-child{border-bottom:1px solid var(--rule)}
.anatomy ol .num{grid-column:1;grid-row:1/3;font-size:13px;color:var(--accent);font-weight:600;padding-top:3px}
.anatomy ol b{grid-column:2;grid-row:1;font-weight:600}.anatomy ol span:not(.num){grid-column:2;grid-row:2;font-size:14px;color:var(--muted)}
.anatomy .after{margin-top:22px;font-size:15px;color:var(--muted)}
.specimen{background:var(--surface);border:1px solid var(--rule);border-radius:var(--r-panel);padding:26px 28px 22px;box-shadow:0 1px 2px rgba(39,27,56,.05),0 18px 40px rgba(39,27,56,.07)}
.specimen-head{display:flex;justify-content:space-between;align-items:baseline;gap:16px;padding-bottom:14px;border-bottom:1px solid var(--rule)}
.specimen-head h3{font:600 19px/1.45 var(--serif)}
.specimen-head h3 .num{color:var(--accent)}
.tag-open{flex:none;font:600 11px/1 var(--mono);letter-spacing:.06em;color:var(--accent-ink);background:var(--accent-soft);padding:6px 8px;border-radius:var(--r-chip)}

.ledger{display:grid}
.part{display:grid;grid-template-columns:132px minmax(0,1fr);gap:16px;padding:12px 0;border-bottom:1px solid var(--rule)}
.part:last-child{border-bottom:0}
.part dt{display:flex;gap:8px;align-items:baseline}
.part dt .idx,.versus .idx,.pline .idx{font:600 12px/1.2 var(--mono);color:var(--accent)}
.part dt .name,.versus .name{font-size:14px;font-weight:600}
.part dd{font-size:15px;line-height:1.7}
.versus-cap{font:500 11px/1 var(--mono);letter-spacing:.08em;color:var(--faint);padding-top:14px;text-transform:uppercase}
.versus{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);border-bottom:1px solid var(--rule)}
.versus .side{padding:12px 0}
.versus .side:first-child{padding-right:20px}
.versus .side+.side{padding-left:20px;border-left:1px solid var(--rule)}
.versus .label{display:flex;flex-wrap:wrap;column-gap:8px;align-items:baseline;margin-bottom:4px}
.versus .label .name{white-space:nowrap}
.versus .label .hint{font-size:12px;color:var(--faint)}
.versus p{font-size:15px;line-height:1.7}

/* 题库 */
.toolbar{display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap;padding-bottom:16px;border-bottom:1px solid var(--rule-strong)}
.filters{display:flex;gap:4px;flex-wrap:wrap}
.filters button{display:inline-flex;align-items:center;gap:7px;border:0;background:transparent;padding:8px 12px;border-radius:var(--r-control);font-size:14px;color:var(--muted);transition:transform 120ms var(--ease)}
.filters button:active{transform:scale(.97)}
.filters button i{width:8px;height:8px;border-radius:2px;background:var(--d)}
.filters button .num{font-size:12px;color:var(--faint)}
.filters button[aria-pressed="true"]{background:var(--ink);color:var(--canvas)}
.filters button[aria-pressed="true"] .num{color:inherit;opacity:.7}
@media (hover:hover){.filters button[aria-pressed="false"]:hover{color:var(--ink);background:var(--accent-soft)}}
.filters .flabel{align-self:center;font:500 11px/1 var(--mono);letter-spacing:.08em;color:var(--faint);padding:0 6px 0 2px}
.filters.levels{flex-basis:100%;order:3;padding-top:2px}
.lvl{font:600 11px/1 var(--mono);letter-spacing:.04em;padding:5px 7px;border-radius:var(--r-chip);color:var(--muted);background:var(--accent-soft);white-space:nowrap}
.lvl[data-level="热身"]{color:var(--warm-ink);background:var(--warm-soft)}
.lvl[data-level="前沿"]{color:var(--faint);background:transparent;box-shadow:inset 0 0 0 1px var(--rule-strong)}
.search{display:flex;align-items:center;gap:8px;min-width:300px;border:1px solid var(--rule-strong);border-radius:var(--r-control);padding:7px 12px;background:var(--surface)}
.search input{border:0;background:transparent;outline:none;width:100%;font-size:14px}
.search svg{flex:none;width:16px;height:16px;color:var(--faint)}
.count{font-size:13px;color:var(--muted)}
.pid{font:600 15px/1.6 var(--mono);color:var(--d)}
.ptitle{display:block;font:600 19px/1.5 var(--serif)}
.pmeta{display:flex;align-items:center;gap:7px;font-size:13px;color:var(--faint);margin-top:2px}
.pmeta i{width:7px;height:7px;border-radius:2px;background:var(--d)}
.pmeta .bg:before{content:"·";margin-right:7px}
.psection{padding:16px 0 4px;border-top:1px solid var(--rule)}
.versus+.psection{border-top:0}
.pcap{font:500 11px/1 var(--mono);letter-spacing:.08em;color:var(--faint);text-transform:uppercase;margin-bottom:10px}
.criteria{counter-reset:c;display:grid;gap:8px}
.criteria li{counter-increment:c;display:grid;grid-template-columns:22px 92px minmax(0,1fr);gap:10px;font-size:14px;line-height:1.65}
.criteria li:before{content:counter(c);font:600 12px/1.65 var(--mono);color:var(--accent)}
.criteria b{font-weight:600}
.pnote{font-size:13px;color:var(--muted);margin-top:10px}
.reftitle{font-weight:600;font-size:14px}
.refsum{font-size:14px;color:var(--muted);margin-top:4px;line-height:1.7}
.pactions{display:flex;gap:24px;flex-wrap:wrap;align-items:center;padding-top:14px;font-size:14px;border-top:1px solid var(--rule);margin-top:14px}
.pactions a{color:var(--accent-ink);font-weight:600;text-decoration:none}
@media (hover:hover){.pactions a:hover{text-decoration:underline}}

/* 题库：左列表 + 右详情 */
.md{display:grid;grid-template-columns:minmax(300px,380px) minmax(0,1fr);gap:28px;align-items:start;padding-top:18px}
.md-index{position:sticky;top:76px;display:flex;flex-direction:column;max-height:calc(100vh - 92px);border:1px solid var(--rule);border-radius:var(--r-panel);background:var(--surface);overflow:hidden}
.md-bar{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 14px;border-bottom:1px solid var(--rule)}
.md-bar .count{padding:0;margin:0}
.md-reftoggle{display:inline-flex;align-items:center;gap:6px;font-size:13px;color:var(--muted);cursor:pointer;white-space:nowrap}
.md-reftoggle input{accent-color:var(--accent);margin:0}
.md-scroll{overflow-y:auto;overscroll-behavior:contain;padding:0 0 10px}
.md-group{position:sticky;top:0;z-index:1;display:flex;align-items:center;gap:8px;padding:10px 14px 6px;font:600 12px/1 var(--sans);color:var(--ink);background:linear-gradient(var(--surface),var(--surface)),var(--canvas)}
.md-group i{width:8px;height:8px;border-radius:2px;background:var(--d)}
.md-group .num{font:500 11px/1 var(--mono);color:var(--faint)}
.md-row{display:grid;grid-template-columns:40px minmax(0,1fr) 8px;gap:10px;align-items:center;width:100%;text-align:left;border:0;background:transparent;padding:8px 14px;cursor:pointer;color:var(--ink);border-left:3px solid transparent;font:inherit}
.md-row .pid{font:600 12px/1.4 var(--mono);color:var(--d);padding:0}
.md-t{display:flex;flex-direction:column;min-width:0}
.md-title{font-size:14px;line-height:1.45;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.md-sub{font-size:12px;line-height:1.4;color:var(--faint);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.md-dot{width:7px;height:7px;border-radius:50%}
.md-row.has-ref .md-dot{background:var(--d);opacity:.65}
.md-row.on{background:var(--accent-soft);border-left-color:var(--d)}
.md-row.on .md-title{font-weight:600}
@media (hover:hover){.md-row:not(.on):hover{background:color-mix(in srgb,var(--accent-soft) 55%,transparent)}}
.md-row:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
.md-scroll .empty{padding:20px 14px;font-size:14px;color:var(--muted)}
.md-detail{position:sticky;top:76px;max-height:calc(100vh - 92px);overflow-y:auto;overscroll-behavior:contain;border:1px solid var(--rule);border-radius:var(--r-panel);background:var(--surface)}
.md-sheethead{display:none}
.md-card{padding:22px 26px 22px}
.md-dhead{padding-bottom:14px;border-bottom:1px solid var(--rule-strong)}
.md-dtop{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.md-dtop .pid{font:600 15px/1.4 var(--mono);color:var(--d);padding:0}
.md-dtop .pmeta{margin:0}
.md-ref{margin-left:auto;font-size:12px;color:var(--muted);border:1px solid var(--rule-strong);border-radius:999px;padding:2px 10px}
.md-ref.yes{color:var(--d);border-color:color-mix(in srgb,var(--d) 45%,transparent)}
.md-dhead .ptitle{font-size:24px;line-height:1.4;margin:8px 0 12px}
.md-nav{display:flex;gap:8px}
.md-nav button{border:1px solid var(--rule-strong);background:transparent;color:var(--ink);border-radius:var(--r-control);padding:6px 12px;font-size:13px;cursor:pointer}
.md-nav button:disabled{opacity:.4;cursor:default}
@media (hover:hover){.md-nav button:not(:disabled):hover{background:var(--accent-soft)}}
.md-card .ledger{margin-top:4px}
.md-card .pactions{margin-top:18px}
@media (max-width:980px){
  .md{grid-template-columns:1fr}
  .md-index{position:static;max-height:none;overflow:visible}
  .md-scroll{overflow:visible}
  .md-group{top:60px}
  .md-detail{position:fixed;inset:0;z-index:40;max-height:none;border:0;border-radius:0;background:var(--canvas);transform:translateY(100%);transition:transform .28s var(--ease);visibility:hidden}
  .md-detail.sheet-open{transform:none;visibility:visible}
  .md-sheethead{display:flex;position:sticky;top:0;z-index:2;padding:10px 12px;background:var(--canvas);border-bottom:1px solid var(--rule)}
  .md-close{border:0;background:transparent;color:var(--accent-ink);font:600 15px/1 var(--sans);padding:8px 4px;cursor:pointer}
  .md-card{padding:18px 16px 40px}
  .md-dhead .ptitle{font-size:20px}
  .md-card .versus{grid-template-columns:1fr}
  .md-card .versus .side+.side{padding-left:0;border-left:0;border-top:1px solid var(--rule)}
  .md-card .part{grid-template-columns:1fr;gap:4px}
  .md-card .criteria li{grid-template-columns:22px minmax(0,1fr)}
  .md-card .criteria li span{grid-column:2}
  html.md-lock,html.md-lock body{overflow:hidden}
  #sidenav{z-index:30}
}
@media (prefers-reduced-motion:reduce){.md-detail{transition:none}}
.md-row{grid-template-columns:40px minmax(0,1fr) auto 8px}
.md-lv{font:600 10px/1 var(--mono);padding:4px 6px;border-radius:var(--r-chip);color:var(--warm-ink);background:var(--warm-soft)}
.md-lv:empty{display:none}
.md-dtop .lvl{flex:none}

/* 侧边快速导航 */
#sidenav{position:fixed;z-index:30;font:14px/1.4 var(--sans)}
#sidenav ol{list-style:none;margin:0;padding:0}
#sidenav a{display:flex;align-items:center;gap:10px;padding:7px 10px;border-radius:var(--r-control);color:var(--muted);text-decoration:none;transition:color .2s,background .2s}
#sidenav a:hover{color:var(--ink);background:var(--accent-soft)}
#sidenav a .n{font:500 11px/1 var(--mono);color:var(--faint);width:18px;flex:none}
#sidenav a.on{color:var(--accent-ink);font-weight:600}
#sidenav a.on .n{color:var(--accent)}
#sidenav .sn-title{font:500 11px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--faint);padding:0 10px 10px}
#sidenav .sn-bar{position:absolute;left:0;top:28px;bottom:0;width:2px;background:var(--rule);border-radius:2px}
#sidenav .sn-bar i{display:block;width:100%;height:0;background:var(--accent);border-radius:2px}
#sidenav .sn-toggle{display:none}
/* 宽屏：常驻左侧 */
@media (min-width:1500px){
  #sidenav{top:50%;transform:translateY(-50%);left:max(20px,calc((100vw - 1180px)/2 - 190px));width:170px}
  #sidenav nav{position:relative;padding-left:12px}
}
/* 窄屏：右下角按钮展开 */
@media (max-width:1499px){
  #sidenav{right:20px;bottom:20px}
  #sidenav .sn-toggle{display:inline-flex;align-items:center;gap:8px;margin-left:auto;height:44px;padding:0 16px;border-radius:999px;border:1px solid var(--rule-strong);background:var(--surface);color:var(--ink);font:500 14px/1 var(--sans);cursor:pointer;box-shadow:0 8px 24px -12px rgba(39,27,56,.45);backdrop-filter:blur(8px)}
  #sidenav{display:flex;flex-direction:column;align-items:flex-end;gap:10px}
  #sidenav nav{order:-1;width:220px;padding:14px 8px 10px;border-radius:var(--r-panel);border:1px solid var(--rule);background:var(--canvas);box-shadow:0 18px 40px -18px rgba(39,27,56,.5);opacity:0;transform:translateY(8px);pointer-events:none;transition:opacity .2s,transform .2s var(--ease);position:relative}
  #sidenav.open nav{opacity:1;transform:none;pointer-events:auto}
  #sidenav .sn-bar{display:none}
}
@media (prefers-reduced-motion:reduce){#sidenav *{transition:none!important}}

/* 从热身题开始 */
.start{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.05fr);gap:64px;align-items:start}
.steps li{display:grid;grid-template-columns:40px minmax(0,1fr);gap:4px 12px;padding:16px 0;border-top:1px solid var(--rule)}
.steps li:last-of-type{border-bottom:1px solid var(--rule)}
.steps .num{grid-row:1/3;font-size:13px;color:var(--warm-ink);font-weight:600;padding-top:3px}
.steps b{font-weight:600}.steps span:not(.num){grid-column:2;font-size:15px;color:var(--muted)}
.start pre{margin-top:28px}
.start pre .ok{color:var(--warm)}.start pre .dim{color:var(--on-deep-faint)}
.warmlist{border-top:1px solid var(--rule-strong)}
.warm-item{display:grid;grid-template-columns:52px minmax(0,1fr) auto;gap:4px 16px;align-items:baseline;width:100%;text-align:left;background:transparent;border:0;border-bottom:1px solid var(--rule);padding:16px 0;transition:transform 120ms var(--ease)}
.warm-item:active{transform:scale(.99)}
.warm-item .num{font-weight:600;color:var(--d)}
.warm-item .wt{font:600 16px/1.5 var(--serif)}
.warm-item .wbg{grid-column:2;font-size:13px;color:var(--faint)}
.warm-item .wst{grid-row:1/3;grid-column:3;align-self:center;font:600 11px/1 var(--mono);padding:6px 8px;border-radius:var(--r-chip);color:var(--muted);box-shadow:inset 0 0 0 1px var(--rule-strong);white-space:nowrap}
.warm-item .wst.ready{color:var(--warm-ink);background:var(--warm-soft);box-shadow:none}
@media (hover:hover){.warm-item:hover .wt{color:var(--accent-ink)}}
.warm-foot{margin-top:18px;font-size:14px;color:var(--muted)}
.warm-foot a{color:var(--accent-ink);font-weight:600;text-decoration:none}
@media (hover:hover){.warm-foot a:hover{text-decoration:underline}}

/* 现有参照 */
.split{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(0,1fr);gap:64px;align-items:start}
.story h3{font:600 28px/1.4 var(--serif);margin:12px 0 16px}
.story p{color:var(--muted);max-width:34em}.story p+p{margin-top:12px}
.facts li{position:relative;padding:14px 0 14px 22px;border-top:1px solid var(--rule);font-size:15px}
.facts li:last-child{border-bottom:1px solid var(--rule)}
.facts li:before{content:"";position:absolute;left:2px;top:25px;width:7px;height:7px;border-radius:50%;background:var(--accent)}

/* 你的贡献会去哪里 */
.join{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:40px}
.join li{border-top:1px solid var(--rule-strong);padding-top:18px}
.join .num{display:block;font-size:13px;color:var(--accent);font-weight:600}
.join h3{font:600 21px/1.4 var(--serif);margin:8px 0 8px}
.join p{font-size:15px;color:var(--muted)}
code{font:13px var(--mono);background:var(--accent-soft);padding:1px 6px;border-radius:var(--r-chip);overflow-wrap:anywhere}
pre{margin:40px 0 0;background:var(--deep);color:var(--on-deep);border-radius:var(--r-control);padding:16px 20px;overflow-x:auto;font-size:14px}
pre code{background:none;padding:0;color:inherit}
.pipeline{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));position:relative;margin-top:64px}
.pipeline:before{content:"";position:absolute;left:6px;right:6px;top:6px;height:1px;background:var(--rule-strong)}
.pipeline li{position:relative;padding:28px 16px 0 0}
.pipeline li:before{content:"";position:absolute;left:0;top:0;width:13px;height:13px;border-radius:50%;background:var(--canvas);border:1px solid var(--rule-strong)}
.pipeline li:last-child:before{background:var(--accent);border-color:var(--accent);box-shadow:0 0 0 5px var(--accent-soft)}
.pipeline b{display:block;font:600 18px/1.4 var(--serif)}
.pipeline li:last-child b{color:var(--accent-ink);font-family:var(--mono)}
.pipeline span{display:block;font-size:14px;color:var(--muted);margin-top:4px}
.credit{margin-top:48px;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:0 48px}
.credit li{padding:14px 0;border-top:1px solid var(--rule);font-size:15px;color:var(--muted)}
.credit li b{color:var(--ink);font-weight:600}

/* 收尾 */
.closing{position:relative;background:var(--deep);color:var(--on-deep);padding:96px 0 72px;overflow:hidden}
.closing:before{content:"";position:absolute;inset:0;background-image:GRAIN;opacity:.16;mix-blend-mode:screen;pointer-events:none}
.closing .wrap{position:relative}
.closing h2{font:600 clamp(32px,4.2vw,52px)/1.2 var(--serif);max-width:15em}
.closing .lead{color:var(--on-deep-muted);margin-top:20px}
.closing .btn{background:var(--on-deep);color:var(--deep);margin-top:32px}
.closing .fine{margin-top:64px;padding-top:24px;border-top:1px solid rgba(255,255,255,.1);font-size:13px;color:var(--on-deep-faint);max-width:52em}
.closing .fine p+p{margin-top:8px}.closing .fine a{color:var(--on-deep-muted)}

[hidden]{display:none!important}
@media (max-width:980px){
  .wrap{padding:0 28px}.hero-grid,.anatomy,.start{grid-template-columns:1fr;gap:48px}
  .section-head{grid-template-columns:1fr;gap:12px}.split{grid-template-columns:1fr;gap:40px}
  .stakes{grid-template-columns:repeat(2,minmax(0,1fr))}
  .stake:nth-child(n){padding:24px 24px 26px 0;border-left:0}
  .stake:nth-child(2n){padding-left:24px;border-left:1px solid var(--rule)}
  .pipeline{grid-template-columns:1fr}.pipeline:before{right:auto;bottom:6px;width:1px;height:auto}
  .pipeline li{padding:0 0 22px 32px}.credit{grid-template-columns:1fr}
}
@media (max-width:640px){
  .wrap{padding:0 16px}.navlinks{display:none}.nav .contribute{margin-left:auto}
  .hero{padding:44px 0 60px}.lead{font-size:16px}
  .board{padding:20px 16px 18px}.cells{gap:4px}.cell{font-size:9px;border-radius:3px}
  .figures{grid-template-columns:repeat(3,minmax(0,1fr))}.figures div{margin-right:0;padding:14px 10px 0 0;border-right:0}.figures b{font-size:24px}
  section{padding:64px 0 72px}
  .stakes{grid-template-columns:1fr}.stake:nth-child(n){padding:22px 0;border-left:0}.stake .theme{font-size:26px}
  .specimen{padding:20px 18px 18px}
  .part{grid-template-columns:1fr;gap:4px}
  .versus{grid-template-columns:1fr}.versus .side+.side{padding-left:0;border-left:0;border-top:1px dashed var(--rule)}.versus .side:first-child{padding-right:0}
  .search{min-width:0;width:100%}
  .warm-item{grid-template-columns:44px minmax(0,1fr)}.warm-item .wst{grid-row:auto;grid-column:2;justify-self:start;margin-top:6px}
  .criteria li{grid-template-columns:22px minmax(0,1fr)}.criteria li span{grid-column:2}
  .join{grid-template-columns:1fr;gap:28px}
  .closing{padding:64px 0 56px}
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*:before,*:after{transition:none!important;animation:none!important}}
""".replace("GRAIN", GRAIN)

JS = """
const problems = JSON.parse(document.getElementById('data').textContent);
const DOMAINS = JSON.parse(document.getElementById('domains').textContent);
const REPO = JSON.parse(document.getElementById('repo').textContent);
const ORDER = ['biomedicine','applied-materials','model-dynamics','extensions'];
let domain = 'all', level = 'all', query = '', onlyRef = false, current = null, hits = [];
const listEl = document.getElementById('mdlist'), count = document.getElementById('count');
const detail = document.getElementById('mddetail'), body = document.getElementById('mdbody');
const tpl = document.getElementById('detail-tpl');
const mobile = window.matchMedia('(max-width:980px)');
const byId = Object.fromEntries(problems.map(p => [p.id, p]));

function matches(p) {
  if (domain !== 'all' && p.area !== domain) return false;
  if (level !== 'all' && p.track.level !== level) return false;
  if (onlyRef && !p.has_reference) return false;
  if (!query) return true;
  return [p.id, p.title, p.subdomain, p.system, p.observable, p.classical_baseline, p.quantum_role, p.decision].join(' ').toLowerCase().includes(query);
}
function fill(root, key, value) { root.querySelectorAll(`[data-f="${key}"]`).forEach(el => { el.textContent = value || '—'; }); }

function renderList() {
  hits = problems.filter(matches);
  const frag = document.createDocumentFragment();
  for (const area of ORDER) {
    const group = hits.filter(p => p.area === area);
    if (!group.length) continue;
    const h = document.createElement('div');
    h.className = 'md-group ' + DOMAINS[area][1];
    h.innerHTML = '<i></i><span></span><span class="num"></span>';
    h.children[1].textContent = DOMAINS[area][0]; h.children[2].textContent = group.length;
    frag.append(h);
    for (const p of group) {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'md-row ' + DOMAINS[p.area][1];
      b.id = 'row-' + p.id; b.dataset.id = p.id; b.setAttribute('role', 'option');
      b.innerHTML = '<span class="pid"></span><span class="md-t"><span class="md-title"></span><span class="md-sub"></span></span><span class="md-lv"></span><span class="md-dot" aria-hidden="true"></span>';
      b.querySelector('.pid').textContent = p.id;
      b.querySelector('.md-title').textContent = p.title;
      b.querySelector('.md-sub').textContent = p.subdomain || '';
      if (p.track.level === '热身') b.querySelector('.md-lv').textContent = '热身';
      if (p.has_reference) { b.classList.add('has-ref'); b.title = '有参照记录'; }
      b.addEventListener('click', () => select(p.id, {open: true, focus: false}));
      frag.append(b);
    }
  }
  listEl.replaceChildren(frag);
  if (!hits.length) {
    const e = document.createElement('p'); e.className = 'empty';
    e.textContent = '没有找到匹配的题目。试试题号、体系或方法名，比如 Hubbard、VQE、退火。';
    listEl.append(e);
  }
  count.textContent = `共 ${hits.length} 题`;
  if (!current || !hits.some(p => p.id === current)) {
    if (hits.length) select(hits[0].id, {open: false, scroll: false, hash: false});
    else { current = null; body.replaceChildren(); }
  } else markActive(false);
}

function markActive(scroll) {
  listEl.querySelectorAll('.md-row').forEach(r => {
    const on = r.dataset.id === current;
    r.classList.toggle('on', on); r.setAttribute('aria-selected', String(on));
    if (on && scroll) reveal(r);
  });
}
// 只滚动列表自身，不带动整页（scrollIntoView 会把页面也滚过题库标题）
function reveal(row) {
  const box = listEl.getBoundingClientRect(), r = row.getBoundingClientRect();
  const head = listEl.querySelector('.md-group')?.offsetHeight || 0;
  // 列表在吸顶之前可能伸出视口，按它在视口里可见的那一段计算
  const top = Math.max(box.top, 60) + head, bottom = Math.min(box.bottom, innerHeight - 16);
  if (r.top < top) listEl.scrollTop -= top - r.top;
  else if (r.bottom > bottom) listEl.scrollTop += r.bottom - bottom;
}

function renderDetail(p) {
  const node = tpl.content.firstElementChild.cloneNode(true);
  node.classList.add(DOMAINS[p.area][1]);
  for (const key of ['id', 'title', 'observable', 'system', 'classical_baseline', 'quantum_role', 'decision']) fill(node, key, p[key]);
  fill(node, 'meta', `${DOMAINS[p.area][0]} · ${p.subdomain || ''}`);
  fill(node, 'bg', p.track.background);
  fill(node, 'level', p.track.level);
  node.querySelector('.lvl').dataset.level = p.track.level;
  fill(node, 'ref', p.has_reference ? '有参照记录' : '仅文献整理');
  if (p.has_reference) node.querySelector('.md-ref').classList.add('yes');
  const ref = p.reference;
  fill(node, 'ref_title', ref ? `本项目最新一轮研究：${ref.title}` : '本题暂无本项目的执行记录，从文献出发。');
  fill(node, 'ref_summary', ref ? ref.summary : '题面里的文献来源和五段拆解就是起点。');
  const ol = node.querySelector('[data-list="criteria"]');
  for (const [label, text] of p.criteria) {
    const li = document.createElement('li');
    const b = document.createElement('b'); b.textContent = label;
    const span = document.createElement('span'); span.textContent = text;
    li.append(b, span); ol.append(li);
  }
  node.querySelector('[data-link="problem"]').href = `${REPO}/blob/main/problems/${p.area}/${p.id}/PROBLEM.md`;
  node.querySelector('[data-link="issue"]').href = `${REPO}/issues/new?template=problem.yml&title=${encodeURIComponent(`[题目] ${p.id}: `)}`;
  if (p.track.starter) {
    const a = document.createElement('a');
    a.href = `${REPO}/tree/main/${p.track.starter.path}`; a.target = '_blank'; a.rel = 'noopener';
    a.textContent = `运行 starter（${p.track.starter.path}）`;
    node.querySelector('.pactions').prepend(a);
  }
  const i = hits.findIndex(x => x.id === p.id);
  node.querySelectorAll('[data-step]').forEach(btn => {
    const j = i + Number(btn.dataset.step);
    btn.disabled = j < 0 || j >= hits.length;
    btn.addEventListener('click', () => step(Number(btn.dataset.step)));
  });
  body.replaceChildren(node);
  detail.scrollTop = 0;
}

function select(id, opts = {}) {
  const p = byId[id]; if (!p) return;
  current = id;
  renderDetail(p);
  markActive(opts.scroll !== false);
  if (opts.hash !== false) history.replaceState(null, '', '#p-' + id);
  if (mobile.matches && opts.open) openSheet(true);
}
function step(d) {
  const i = hits.findIndex(x => x.id === current), j = i + d;
  if (j >= 0 && j < hits.length) select(hits[j].id, {open: false});
}
function openSheet(open) {
  detail.classList.toggle('sheet-open', open);
  document.documentElement.classList.toggle('md-lock', open && mobile.matches);
}
document.getElementById('mdclose').addEventListener('click', () => openSheet(false));

function setDomain(value) {
  domain = value;
  document.querySelectorAll('[data-domain]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.domain === value)));
}
function setLevel(value) {
  level = value;
  document.querySelectorAll('[data-level-filter]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.levelFilter === value)));
}
// 首屏题板 / 其他入口：直接打开某题
function openProblem(id) {
  if (!byId[id]) return;
  if (!hits.some(p => p.id === id)) { setDomain('all'); setLevel('all'); query = ''; document.getElementById('q').value = ''; onlyRef = false; document.getElementById('onlyref').checked = false; renderList(); }
  document.getElementById('problems').scrollIntoView({block: 'start'});
  select(id, {open: true});
}
document.querySelectorAll('[data-domain]').forEach(btn => btn.addEventListener('click', () => { setDomain(btn.dataset.domain); renderList(); listEl.scrollTop = 0; }));
document.querySelectorAll('[data-level-filter]').forEach(btn => btn.addEventListener('click', () => { setLevel(btn.dataset.levelFilter); renderList(); listEl.scrollTop = 0; }));
document.querySelectorAll('[data-open]').forEach(btn => btn.addEventListener('click', () => openProblem(btn.dataset.open)));
document.getElementById('q').addEventListener('input', e => { query = e.target.value.trim().toLowerCase(); renderList(); listEl.scrollTop = 0; });
document.getElementById('onlyref').addEventListener('change', e => { onlyRef = e.target.checked; renderList(); });
// 键盘：在题库区域内 ↑/↓ 或 j/k 切换
document.addEventListener('keydown', e => {
  if (e.target.closest && e.target.closest('input,textarea')) return;
  if (e.key === 'Escape') { openSheet(false); return; }
  const sec = document.getElementById('problems').getBoundingClientRect();
  if (sec.bottom < 0 || sec.top > innerHeight) return;
  if (e.key === 'ArrowDown' || e.key === 'j') { e.preventDefault(); step(1); }
  else if (e.key === 'ArrowUp' || e.key === 'k') { e.preventDefault(); step(-1); }
});
mobile.addEventListener('change', () => { if (!mobile.matches) openSheet(false); });

renderList();
function fromHash(){ const m0 = location.hash.match(/^#p-([A-Za-z][0-9]+)$/); if (m0 && byId[m0[1].toUpperCase()]) openProblem(m0[1].toUpperCase()); }
window.addEventListener('hashchange', fromHash);
fromHash();
"""

SIDENAV_JS = """
(function(){
  var root=document.getElementById('sidenav'); if(!root) return;
  var links=[].slice.call(root.querySelectorAll('ol a'));
  var secs=links.map(function(a){return document.getElementById(a.getAttribute('href').slice(1))});
  var bar=root.querySelector('.sn-bar i'), btn=root.querySelector('.sn-toggle');
  function update(){
    var cur=0;
    secs.forEach(function(s,i){ if(s && s.getBoundingClientRect().top<=Math.max(180,innerHeight*.3)) cur=i; });
    if(window.innerHeight+window.scrollY>=document.documentElement.scrollHeight-4) cur=secs.length-1;
    links.forEach(function(a,i){ a.classList.toggle('on',i===cur); if(i===cur) a.setAttribute('aria-current','true'); else a.removeAttribute('aria-current'); });
    var max=document.documentElement.scrollHeight-window.innerHeight;
    if(bar) bar.style.height=(max>0?Math.min(100,window.scrollY/max*100):0)+'%';
  }
  var ticking=false;
  window.addEventListener('scroll',function(){ if(!ticking){ticking=true;requestAnimationFrame(function(){update();ticking=false;});} },{passive:true});
  window.addEventListener('resize',update); update();
  function setOpen(o){ root.classList.toggle('open',o); btn.setAttribute('aria-expanded',o?'true':'false'); }
  btn.addEventListener('click',function(e){ e.stopPropagation(); setOpen(!root.classList.contains('open')); });
  links.forEach(function(a){ a.addEventListener('click',function(){ setOpen(false); }); });
  document.addEventListener('click',function(e){ if(!root.contains(e.target)) setOpen(false); });
  document.addEventListener('keydown',function(e){ if(e.key==='Escape') setOpen(false); });
})();
"""

ARROW = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SEARCH = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><circle cx="7" cy="7" r="4.6" stroke="currentColor" stroke-width="1.4"/><path d="M10.5 10.5L14 14" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>'


def esc(text: object) -> str:
    return html.escape(str(text or ""), quote=True)


def load_problems() -> list[dict]:
    rows = []
    for domain in DOMAINS:
        for path in sorted((ROOT / "problems" / domain).glob("*/problem.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            row = {k: data.get(k) for k in (
                "id", "title", "area", "subdomain", "system", "observable",
                "classical_baseline", "quantum_role", "decision", "has_reference", "track",
            )}
            row["criteria"] = criteria((path.parent / "PROBLEM.md").read_text(encoding="utf-8"))
            row["reference"] = reference(path.parent / "REFERENCE.md")
            rows.append(row)
    return rows


def plain(text: str) -> str:
    """Markdown 行内标记转纯文本：链接留文字，去掉粗体与代码标记。"""
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return re.sub(r"\*\*|`", "", text).strip()


def criteria(problem_md: str) -> list[list[str]]:
    section = problem_md.split("## 什么算解", 1)[1].split("## 现有参照", 1)[0]
    return [[m.group(1), plain(m.group(2))] for m in map(CRITERION_RE.match, section.splitlines()) if m]


def reference(path: Path) -> dict | None:
    """REFERENCE.md 的报告标题与首个正文段落，原文提取；不足 12 字的短行视为小标题跳过。"""
    if not path.is_file():
        return None
    title, paragraphs, current = "", [], []
    for line in path.read_text(encoding="utf-8").splitlines() + [""]:
        if not title:
            if line.startswith("# "):
                title = plain(line[2:])
            continue
        if not line.strip() or line.startswith(("#", ">", "|", "<!--", "```", "- ", "* ")):
            if current:
                paragraphs.append(plain(" ".join(current)))
                current = []
            continue
        current.append(line.strip())
    body = next((t for t in paragraphs if len(t) >= 12), paragraphs[0] if paragraphs else "")
    return {"title": title, "summary": body}


def embed(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True).replace("</", "<\\/")


def part_row(index: int, value: str | None = None, field: str | None = None) -> str:
    _key, name, _hint = PARTS[index]
    content = f'<dd data-f="{field}"></dd>' if field else f"<dd>{esc(value)}</dd>"
    return f'<div class="part"><dt><span class="idx">0{index + 1}</span><span class="name">{esc(name)}</span></dt>{content}</div>'


def versus(classical: str | None = None, quantum: str | None = None, templated: bool = False) -> str:
    def side(index: int, value: str | None) -> str:
        key, name, hint = PARTS[index]
        body = f'<p data-f="{key}"></p>' if templated else f"<p>{esc(value)}</p>"
        return (f'<div class="side"><div class="label"><span class="idx">0{index + 1}</span>'
                f'<span class="name">{esc(name)}</span><span class="hint">{esc(hint)}</span></div>{body}</div>')
    return f'<p class="versus-cap">同一问题，两种做法</p><div class="versus">{side(2, classical)}{side(3, quantum)}</div>'


def board(problems: list[dict], total: int) -> str:
    cells = "".join(
        f'<button type="button" class="cell {DOMAINS[p["area"]][1]}{" warm" if p["track"]["level"] == "热身" else ""}" '
        f'style="--i:{i}" data-open="{esc(p["id"])}" title="{esc(p["id"])} {esc(p["title"])}（{esc(p["track"]["level"])}）" '
        f'aria-label="{esc(p["id"])} {esc(p["title"])}，{esc(p["track"]["level"])}">{esc(p["id"])}</button>'
        for i, p in enumerate(problems)
    )
    legend = "".join(f'<span class="{cls}"><i></i>{esc(label)}</span>' for label, cls in DOMAINS.values())
    legend += '<span class="warm-key"><i></i>热身题</span>'
    return f"""<div class="board" aria-label="题板：{total} 道开放题">
<div class="board-head"><b>{total} 道题，全部开放</b><span>点亮 0 / {total}</span></div>
<div class="cells">{cells}</div>
<div class="legend">{legend}</div>
<p class="board-foot">每一格是一道题，点一格直接打开它。<b>第一份被采纳的解法，会是这里亮起的第一格。</b></p>
</div>"""


def stakes(by_id: dict[str, dict]) -> str:
    items = []
    for theme, pid in STAKES:
        p = by_id[pid]
        items.append(
            f'<button type="button" class="stake {DOMAINS[p["area"]][1]}" data-open="{esc(pid)}">'
            f'<span class="theme">{esc(theme)}</span><span class="why">{esc(p["decision"])}</span>'
            f'<span class="src"><span class="num">{esc(pid)}</span><span>{esc(p["title"])}</span></span>'
            f'<span class="go">看这道题</span></button>'
        )
    return f'<div class="stakes">{"".join(items)}</div>'


def specimen(p: dict) -> str:
    return f"""<article class="specimen" aria-label="例题 {esc(p['id'])}">
<div class="specimen-head"><h3><span class="num">{esc(p['id'])}</span> {esc(p['title'])}</h3><span class="tag-open">开放</span></div>
<dl class="ledger">{part_row(0, p['system'])}{part_row(1, p['observable'])}</dl>
{versus(p['classical_baseline'], p['quantum_role'])}
<dl class="ledger">{part_row(4, p['decision'])}</dl>
</article>"""


def warmup(problems: list[dict], stats: dict) -> str:
    warm = [p for p in problems if p["track"]["level"] == "热身"]
    items = "".join(
        f'<li><button type="button" class="warm-item {DOMAINS[p["area"]][1]}" data-open="{esc(p["id"])}">'
        f'<span class="num">{esc(p["id"])}</span><span class="wt">{esc(p["title"])}</span>'
        f'<span class="wbg">{esc(p["track"]["background"])}</span>'
        + (f'<span class="wst ready">starter 可运行</span>' if p["track"].get("starter") else '<span class="wst">starter 待认领</span>')
        + "</button></li>"
        for p in warm
    )
    demo = next(p for p in warm if p["id"] == WARM_DEMO)["track"]["starter"]
    levels = stats["levels"]
    return f"""<section id="start"><div class="wrap">
<div class="section-head"><div><p class="kicker">First steps</p><h2>第一次参与，从一道热身题开始</h2></div>
<p>{len(warm)} 道热身题输入公开、笔记本就能跑。带 starter 的题，一条命令就能复现现有参照的数字；复现之后，再往前走一小步。其余题按难度分为进阶 {levels.get("进阶", 0)} 道、前沿 {levels.get("前沿", 0)} 道，在题库里可以筛选。</p></div>
<div class="start">
<div>
<ol class="steps">
<li><span class="num">01</span><b>装环境</b><span>Python 3.10+，依赖固定版本，只用 CPU。</span></li>
<li><span class="num">02</span><b>复现参照</b><span>脚本下载公开输入、校验哈希，跑完后逐项对照参照数字并打 ✓。</span></li>
<li><span class="num">03</span><b>往前一步，提交</b><span>从 starter 的「下一步」挑一个方向；结果不论好坏，用脚手架建目录提交。</span></li>
</ol>
<pre><code>uv pip install -r starters/requirements.txt
python {esc(demo["path"])}/run.py
<span class="dim">…</span>
<span class="ok">✓</span> AMI[rbf] = 0.7353419233（参照 0.735342）
<span class="ok">✓</span> AMI[quantum] = 0.7107767887（参照 0.710777）
全部落在容差内：你已经复现了现有参照。</code></pre>
</div>
<div>
<ul class="warmlist">{items}</ul>
<p class="warm-foot">给标着「待认领」的题写 starter，本身就是一份很好的第一份贡献。<a href="{BLOB}/starters/README.md" target="_blank" rel="noopener">入门轨道说明</a> · <a href="{BLOB}/solutions/B16/qaidao-vqe-shot-budget/SOLUTION.md" target="_blank" rel="noopener">一份入门示例解法</a></p>
</div>
</div>
</div></section>"""


def problem_template() -> str:
    return f"""<template id="detail-tpl"><article class="md-card">
<div class="md-dhead">
<div class="md-dtop"><span class="pid" data-f="id"></span><span class="pmeta"><i></i><span data-f="meta"></span><span class="bg" data-f="bg"></span></span><span class="lvl" data-f="level"></span><span class="md-ref" data-f="ref"></span></div>
<h3 class="ptitle" data-f="title"></h3>
<div class="md-nav"><button type="button" data-step="-1" aria-label="上一题">↑ 上一题</button><button type="button" data-step="1" aria-label="下一题">下一题 ↓</button></div>
</div>
<dl class="ledger">{part_row(0, field='system')}{part_row(1, field='observable')}{part_row(4, field='decision')}</dl>
{versus(templated=True)}
<div class="psection"><p class="pcap">什么算解</p><ol class="criteria" data-list="criteria"></ol>
<p class="pnote">负结果同样接受，只要过程可复现、结论有依据。</p></div>
<div class="psection"><p class="pcap">现有参照</p><p class="reftitle" data-f="ref_title"></p><p class="refsum" data-f="ref_summary"></p></div>
<div class="pactions"><a data-link="problem" href="#" target="_blank" rel="noopener">在 GitHub 查看完整题面</a><a data-link="issue" href="#" target="_blank" rel="noopener">开 issue 讨论这道题</a><a href="{BLOB}/CONTRIBUTING.md" target="_blank" rel="noopener">提交解法</a></div>
</article></template>"""


def sidenav() -> str:
    links = "".join(f'<li><a href="#{anchor}"><span class="n">0{i}</span>{esc(name)}</a></li>' for i, (anchor, name) in enumerate(TOC))
    return f"""<aside id="sidenav" aria-label="快速跳转">
<nav><div class="sn-title">目录</div><span class="sn-bar" aria-hidden="true"><i></i></span><ol>{links}</ol></nav>
<button class="sn-toggle" type="button" aria-expanded="false" aria-controls="sidenav"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M2 4h12M2 8h12M2 12h8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" fill="none"/></svg>目录</button>
</aside>"""


def release_version() -> str:
    """当前版本号取自 CHANGELOG.md 的第一个 `## vX.Y.Z` 标题。"""
    match = re.search(r"^## (v\d+\.\d+\.\d+)", (ROOT / "CHANGELOG.md").read_text(encoding="utf-8"), re.MULTILINE)
    return match.group(1) if match else ""


def page(problems: list[dict], stats: dict, version: str) -> str:
    domains = stats["domains"]
    total, with_ref = stats["total_problems"], stats["with_reference"]
    by_id = {p["id"]: p for p in problems}
    filters = [f'<button type="button" data-domain="all" aria-pressed="true">全部<span class="num">{total}</span></button>'] + [
        f'<button type="button" class="{cls}" data-domain="{d}" aria-pressed="false"><i></i>{esc(label)}<span class="num">{domains[d]["problems"]}</span></button>'
        for d, (label, cls) in DOMAINS.items()
    ]
    level_filters = ['<span class="flabel">难度</span>', '<button type="button" data-level-filter="all" aria-pressed="true">全部</button>'] + [
        f'<button type="button" data-level-filter="{lv}" aria-pressed="false">{lv}<span class="num">{stats["levels"].get(lv, 0)}</span></button>'
        for lv in LEVELS
    ]
    pipeline = "".join(f"<li><b>{esc(a)}</b><span>{esc(b)}</span></li>" for a, b in PIPELINE)
    anatomy = "".join(
        f'<li><span class="num">0{i + 1}</span><b>{esc(name)}</b><span>{esc(hint)}</span></li>'
        for i, (_k, name, hint) in enumerate(PARTS)
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>100-skills 开放题</title>
<meta name="description" content="{total} 道还开放着的量子计算与科学计算研究题：固氮、碳捕集、PFAS 治理、电池、药物、高温超导。挑一道，提交你的解法。">
<style>{CSS}</style>
</head>
<body>
<a class="skip" href="#problems">跳到题库</a>
<header><div class="wrap nav">
<a class="brand" href="#top">100<b>-</b>skills</a>
<nav class="navlinks" aria-label="页面导航"><a href="#why">为什么值得做</a><a href="#start">从热身题开始</a><a href="#problems">题库</a><a href="#reference">现有参照</a><a href="#join">怎么参与</a></nav>
<a class="contribute" href="{BLOB}/CONTRIBUTING.md" target="_blank" rel="noopener">参与贡献</a>
</div></header>
<main id="top">
<div class="hero"><div class="wrap hero-grid">
<div>
<p class="kicker">Open problems · {version}</p>
<h1><span class="num">{total}</span> 道还开放着的科学计算题</h1>
<p class="lead">固氮、碳捕集、PFAS 治理、电池、药物、高温超导……每一道题都卡在一个<strong>真实的研发判断</strong>上：经典方法做到了哪一步，量子方法能不能补上。挑一道，提交你的解法；被采纳的解法会记入这道题的参照，并在沉淀出的 skill 里署名。</p>
<div class="cta-row"><a class="btn" href="#problems">挑一道题{ARROW}</a><a class="textlink" href="#start">第一次参与？从热身题开始</a></div>
<div class="figures">
<div><b>{total}</b><span>道开放题</span></div>
<div><b>{len(domains)}</b><span>个领域</span></div>
<div><b>{with_ref}</b><span>道有参照记录</span></div>
</div>
</div>
{board(problems, total)}
</div></div>

<section id="why"><div class="wrap">
<div class="section-head"><div><p class="kicker">Why it matters</p><h2>每道题背后，是一个等着被做出的判断</h2></div>
<p>下面是其中 6 道题的「研发决策」原文。算对了，就能少走一条错的研发路线；算出来行不通，同样是有价值的答案。</p></div>
{stakes(by_id)}
</div></section>

<section id="anatomy"><div class="wrap anatomy">
<div><p class="kicker">Problem anatomy</p>
<div class="section-head" style="display:block;margin-bottom:28px"><h2>一道题长什么样</h2></div>
<ol>{anatomy}</ol>
<p class="after">每道题还给出五条「什么算解」：模型对应、可观测量与不确定度、同模型经典对照、可复现性与成本、对研发决策的支撑。负结果同样接受。</p>
</div>
{specimen(by_id[SPECIMEN])}
</div></section>

{warmup(problems, stats)}

<section id="problems"><div class="wrap">
<div class="section-head"><div><p class="kicker">Problem set</p><h2>题库</h2></div>
<p>按领域列出全部 {total} 题，可按难度筛选；点任意一题即可查看五段拆解、经典与量子的对照、验收标准和现有参照，也可用 ↑ ↓ 键逐题浏览。</p></div>
<div class="toolbar"><div class="filters" role="group" aria-label="按领域筛选">{''.join(filters)}</div>
<div class="filters levels" role="group" aria-label="按难度筛选">{''.join(level_filters)}</div>
<label class="search">{SEARCH}<input id="q" type="search" placeholder="搜索题号、体系或方法：Hubbard、VQE、退火" aria-label="搜索题目"></label></div>
<div class="md">
<div class="md-index" aria-label="题目列表">
<div class="md-bar"><p class="count" id="count" aria-live="polite"></p>
<label class="md-reftoggle"><input type="checkbox" id="onlyref">只看有参照</label></div>
<div class="md-scroll" id="mdlist" role="listbox" aria-label="题目"></div>
</div>
<div class="md-detail" id="mddetail" aria-live="polite">
<div class="md-sheethead"><button type="button" class="md-close" id="mdclose" aria-label="返回列表">← 返回列表</button></div>
<div id="mdbody"></div>
</div>
</div>
</div></section>

<section id="reference"><div class="wrap">
<div class="section-head"><div><p class="kicker">Reference runs</p><h2>你不是从零开始</h2></div>
<p>{total} 道题中有 {with_ref} 道附有我们已完成的计算与模拟记录，成功和失败都摆出来。参照不代表最优解，它告诉你从哪里接着做、哪条路已经试过。</p></div>
<div class="split">
<div class="story"><p class="kicker">C08 · RNA 二级结构与假结</p><h3>能量最低的解，不一定是对的解</h3>
<p>在一个真实的 33 核苷酸适配体上，最低目标分的解确实能找到，但它比真实结构多出两对不存在的配对；真实结构也在可行空间里，得分却低得多。</p>
<p>问题出在能量模型本身，换更强的求解器也解决不了。这样的负结果同样写进参照，能帮后来者少走弯路。</p></div>
<ul class="facts">
<li>所有参照都在经典计算机上执行，不包含真机结果。</li>
<li>按项目当前记录，原应用目标完成数为 0，这些题目都还开放着；我们不声称量子优势。</li>
<li>原始数据与第三方数据集不随题库发布，每题的 evidence.json 记录来源文件的 SHA-256。</li>
</ul>
</div>
</div></section>

<section id="join"><div class="wrap">
<div class="section-head"><div><p class="kicker">Contribute</p><h2>你的解法会去哪里</h2></div>
<p>想先聊思路，或觉得某道题的标准需要细化，直接开 issue。负结果和部分结果同样欢迎。</p></div>
<ol class="join">
<li><span class="num">01</span><h3>挑一道题</h3><p>第一次参与先挑热身题。读它的 PROBLEM.md：五段题面、五条验收标准和现有参照都在里面。</p></li>
<li><span class="num">02</span><h3>建目录、写解法</h3><p>脚手架建好 <code>solutions/&lt;题号&gt;/&lt;名字&gt;-&lt;短名&gt;/</code>，填写 SOLUTION.md 与 solution.json。只做一小部分也欢迎。</p></li>
<li><span class="num">03</span><h3>校验后开 PR</h3><p>本地跑一遍校验器，用 <code>git commit -s</code> 签名提交，CI 会再检查一次。</p></li>
</ol>
<pre><code>python3 -I release/tools/new_solution.py C11 你的名字-短名
python3 -I release/tools/check_submissions.py --root .</code></pre>
<ol class="pipeline" aria-label="从提交到 skill">{pipeline}</ol>
<ul class="credit">
<li><b>记入参照。</b>被采纳的解法记入这道题的现有参照，后来的人从你停下的地方接着做。</li>
<li><b>署名进 skill。</b>同一类方法积累到足够多的采纳解法后提炼为 skill，署名全部来源解法的作者。</li>
<li><b>负结果同样算数。</b>一条在给定预算下走不通的路线，写清楚了，就是别人不必再走的弯路。</li>
<li><b>公开可复用。</b>题面与文档 CC BY 4.0，代码 Apache-2.0，任何人都能在你的工作上继续。</li>
</ul>
</div></section>
</main>

<footer class="closing"><div class="wrap">
<p class="kicker" style="color:var(--on-deep-muted)">Start here</p>
<h2>挑一道题，成为点亮第一格的人</h2>
<p class="lead">{total} 道题都还开放着。可以从一道热身题复现参照开始，开个 issue 聊聊思路，或者直接提交一份解法。</p>
<a class="btn" href="#problems">去题库{ARROW}</a>
<div class="fine">
<p>题面与文档采用 CC BY 4.0，代码采用 Apache-2.0，贡献需要 DCO 签名。题面目前只有中文，英文版会在下一个版本补上。详见 <a href="{BLOB}/CONTRIBUTING.md" target="_blank" rel="noopener">CONTRIBUTING.md</a>。</p>
<p>社区沉淀出的 skill 也会内置到晓梦 Agent，让更多研发团队可以直接调用。</p>
</div>
</div></footer>
{problem_template()}
<script type="application/json" id="data">{embed(problems)}</script>
<script type="application/json" id="domains">{embed(DOMAINS)}</script>
<script type="application/json" id="repo">{embed(REPO)}</script>
<script>{JS}</script>
{sidenav()}
<script>{SIDENAV_JS}</script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    out = Path(parser.parse_args().out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    stats = json.loads((ROOT / "release" / "stats.json").read_text(encoding="utf-8"))
    (out / "index.html").write_text(page(load_problems(), stats, release_version()), encoding="utf-8")


if __name__ == "__main__":
    main()
