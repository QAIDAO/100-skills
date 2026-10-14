#!/usr/bin/env python3
"""生成 v0.1.0 宣发展示页（单文件、自包含）。

用法：python3 -I release/tools/build_promo.py --out <dir>
写出 <dir>/index.html。题目数据取自 problems/*/*/problem.json 与 release/stats.json；
叙述文字为固定措辞。不读时钟、不联网。

呈现重心：每道题为什么值得做（研发决策）、要算什么（可观测量），
以及「经典基线」与「量子方法的角色」的对照。
"""

from __future__ import annotations

import argparse
import html
import json
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
  --deep:#0a0710;--deep-2:#140e1e;--bio:#c6a6f7;--mat:#e6c48f;--dyn:#a6badf;--ext:#eba9c9;--grain-opacity:.07}}
:root[data-theme="dark"]{
  --canvas:#110c18;--surface:rgba(255,255,255,.035);--ink:#ece6f4;--muted:#a898bb;--faint:#7d6f8f;
  --rule:rgba(255,255,255,.08);--rule-strong:rgba(255,255,255,.14);--accent:#c3a3f5;--accent-ink:#d6c0fa;--accent-soft:rgba(195,163,245,.12);
  --deep:#0a0710;--deep-2:#140e1e;--bio:#c6a6f7;--mat:#e6c48f;--dyn:#a6badf;--ext:#eba9c9;--grain-opacity:.07}
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

/* 首屏：标题 + 84 格题板 */
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
.cells{position:relative;display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:5px}
.cell{aspect-ratio:1;display:grid;place-items:center;border:1px solid color-mix(in srgb,var(--dn) 55%,transparent);background:color-mix(in srgb,var(--dn) 7%,transparent);border-radius:5px;padding:0;font:600 10px/1 var(--mono);color:color-mix(in srgb,var(--dn) 88%,white);letter-spacing:-.02em;transition:transform 140ms var(--ease),background-color 140ms var(--ease);animation:rise .6s var(--ease) both;animation-delay:calc(var(--i) * 7ms)}
.cell:active{transform:scale(.92)}
@media (hover:hover){.cell:hover{transform:scale(1.12);background:color-mix(in srgb,var(--dn) 30%,transparent);position:relative;z-index:1}}
@keyframes rise{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.legend{position:relative;display:flex;flex-wrap:wrap;gap:6px 18px;margin-top:18px;font-size:12px;color:var(--on-deep-muted)}
.legend span{display:inline-flex;align-items:center;gap:7px}
.legend i{width:9px;height:9px;border-radius:2px;background:var(--dn)}
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
.search{display:flex;align-items:center;gap:8px;min-width:300px;border:1px solid var(--rule-strong);border-radius:var(--r-control);padding:7px 12px;background:var(--surface)}
.search input{border:0;background:transparent;outline:none;width:100%;font-size:14px}
.search svg{flex:none;width:16px;height:16px;color:var(--faint)}
.count{font-size:13px;color:var(--muted);padding:14px 0 6px}
.problem{border-bottom:1px solid var(--rule);scroll-margin-top:72px}
.phead{display:grid;grid-template-columns:64px minmax(0,1fr) auto 20px;gap:20px;align-items:start;width:100%;text-align:left;background:transparent;border:0;padding:22px 0;transition:transform 120ms var(--ease)}
.phead:active{transform:scale(.995)}
.pid{font:600 15px/1.6 var(--mono);color:var(--d);padding-top:2px}
.ptitle{display:block;font:600 19px/1.5 var(--serif)}
.pmeta{display:flex;align-items:center;gap:7px;font-size:13px;color:var(--faint);margin-top:2px}
.pmeta i{width:7px;height:7px;border-radius:2px;background:var(--d)}
.pline{display:grid;grid-template-columns:auto minmax(0,1fr);gap:10px;align-items:baseline;margin-top:8px;font-size:15px}
.pline .idx{background:var(--accent-soft);padding:2px 6px;border-radius:var(--r-chip);font-size:11px;white-space:nowrap}
.pline.why{color:var(--muted)}
.pstate{padding-top:4px}
.pstate .ref{font-size:12px;color:var(--muted);white-space:nowrap}
.chev{width:20px;height:20px;margin-top:4px;color:var(--faint);transition:transform 200ms var(--ease)}
.problem.open .chev{transform:rotate(180deg);color:var(--accent)}
@media (hover:hover){.phead:hover .ptitle{color:var(--accent-ink)}.phead:hover .chev{color:var(--accent)}}
.pbody{display:grid;grid-template-rows:0fr;transition:grid-template-rows 240ms var(--ease)}
.problem.open .pbody{grid-template-rows:1fr}
.pinner{overflow:hidden}
.pcontent{margin:0 0 26px 84px;padding:4px 24px 18px;background:var(--surface);border:1px solid var(--rule);border-radius:var(--r-panel)}
.pactions{display:flex;gap:24px;flex-wrap:wrap;align-items:center;padding-top:14px;font-size:14px}
.pactions a{color:var(--accent-ink);font-weight:600;text-decoration:none}
@media (hover:hover){.pactions a:hover{text-decoration:underline}}
.pactions span{color:var(--muted);margin-right:auto}
.problem.flash .phead{animation:flash 1.2s var(--ease)}
@keyframes flash{from{background:var(--accent-soft)}to{background:transparent}}
.more{display:inline-flex;margin:28px 0 0;padding:11px 22px;border:1px solid var(--rule-strong);background:transparent;border-radius:var(--r-control);font-size:14px;font-weight:600;transition:transform 120ms var(--ease)}
.more:active{transform:scale(.97)}
.empty{padding:40px 0;color:var(--muted)}

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
  .wrap{padding:0 28px}.hero-grid,.anatomy{grid-template-columns:1fr;gap:48px}
  .section-head{grid-template-columns:1fr;gap:12px}.split{grid-template-columns:1fr;gap:40px}
  .stakes{grid-template-columns:repeat(2,minmax(0,1fr))}
  .stake:nth-child(n){padding:24px 24px 26px 0;border-left:0}
  .stake:nth-child(2n){padding-left:24px;border-left:1px solid var(--rule)}
  .pipeline{grid-template-columns:1fr}.pipeline:before{right:auto;bottom:6px;width:1px;height:auto}
  .pipeline li{padding:0 0 22px 32px}.credit{grid-template-columns:1fr}
  .pcontent{margin-left:0}
}
@media (max-width:640px){
  .wrap{padding:0 16px}.navlinks{display:none}.nav .contribute{margin-left:auto}
  .hero{padding:44px 0 60px}.lead{font-size:16px}
  .board{padding:20px 16px 18px}.cells{gap:3px}.cell{font-size:8px;border-radius:3px}
  .figures{grid-template-columns:repeat(3,minmax(0,1fr))}.figures div{margin-right:0;padding:14px 10px 0 0;border-right:0}.figures b{font-size:24px}
  section{padding:64px 0 72px}
  .stakes{grid-template-columns:1fr}.stake:nth-child(n){padding:22px 0;border-left:0}.stake .theme{font-size:26px}
  .specimen{padding:20px 18px 18px}
  .part{grid-template-columns:1fr;gap:4px}
  .versus{grid-template-columns:1fr}.versus .side+.side{padding-left:0;border-left:0;border-top:1px dashed var(--rule)}.versus .side:first-child{padding-right:0}
  .search{min-width:0;width:100%}
  .phead{grid-template-columns:minmax(0,1fr) 20px;gap:6px 12px}
  .pid{grid-column:1;padding-top:0}.phead .pmain{grid-column:1/-1;grid-row:2}.pstate{grid-column:1;grid-row:3;padding-top:0}
  .chev{grid-column:2;grid-row:1}
  .pcontent{padding:2px 16px 16px}
  .join{grid-template-columns:1fr;gap:28px}
  .closing{padding:64px 0 56px}
}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*:before,*:after{transition:none!important;animation:none!important}}
""".replace("GRAIN", GRAIN)

JS = """
const problems = JSON.parse(document.getElementById('data').textContent);
const DOMAINS = JSON.parse(document.getElementById('domains').textContent);
const PAGE = 12;
let domain = 'all', query = '', shown = PAGE;
const list = document.getElementById('plist'), count = document.getElementById('count'), more = document.getElementById('more');
const tpl = document.getElementById('problem-tpl');
function matches(p) {
  if (domain !== 'all' && p.area !== domain) return false;
  if (!query) return true;
  return [p.id, p.title, p.subdomain, p.system, p.observable, p.classical_baseline, p.quantum_role, p.decision].join(' ').toLowerCase().includes(query);
}
function fill(root, key, value) { root.querySelectorAll(`[data-f="${key}"]`).forEach(el => { el.textContent = value || '—'; }); }
function setOpen(node, open) {
  node.classList.toggle('open', open);
  node.querySelector('.phead').setAttribute('aria-expanded', String(open));
  node.querySelector('.pbody').inert = !open;
}
function build(p) {
  const node = tpl.content.firstElementChild.cloneNode(true);
  const head = node.querySelector('.phead'), body = node.querySelector('.pbody');
  node.dataset.id = p.id; node.id = `p-${p.id}`; node.classList.add(DOMAINS[p.area][1]);
  head.id = `h-${p.id}`; body.id = `b-${p.id}`;
  head.setAttribute('aria-controls', body.id); body.setAttribute('aria-labelledby', head.id);
  for (const key of ['id', 'title', 'observable', 'system', 'classical_baseline', 'quantum_role', 'decision']) fill(node, key, p[key]);
  fill(node, 'meta', `${DOMAINS[p.area][0]} · ${p.subdomain || ''}`);
  fill(node, 'ref', p.has_reference ? '有参照记录' : '仅文献整理');
  fill(node, 'refnote', p.has_reference ? '本项目已有执行记录，可以从那里接着做。' : '暂无执行记录，从文献出发。');
  node.querySelector('[data-link="problem"]').href = `../../problems/${p.area}/${p.id}/PROBLEM.md`;
  body.inert = true;
  head.addEventListener('click', () => setOpen(node, !node.classList.contains('open')));
  return node;
}
function render() {
  const hits = problems.filter(matches);
  list.replaceChildren(...hits.slice(0, shown).map(build));
  if (!hits.length) {
    const empty = document.createElement('li'); empty.className = 'empty';
    empty.textContent = '没有找到匹配的题目。试试题号、体系或方法名，比如 Hubbard、VQE、退火。';
    list.append(empty);
  }
  count.textContent = hits.length > shown ? `共 ${hits.length} 题，先显示 ${shown} 题` : `共 ${hits.length} 题`;
  more.hidden = hits.length <= shown;
}
function setDomain(value) {
  domain = value;
  document.querySelectorAll('[data-domain]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.domain === value)));
}
function openProblem(id) {
  setDomain('all'); query = ''; document.getElementById('q').value = ''; shown = problems.length; render();
  const node = document.getElementById(`p-${id}`);
  if (!node) return;
  setOpen(node, true);
  node.classList.remove('flash'); void node.offsetWidth; node.classList.add('flash');
  node.scrollIntoView({block: 'start'});
  node.querySelector('.phead').focus({preventScroll: true});
}
document.querySelectorAll('[data-domain]').forEach(btn => btn.addEventListener('click', () => { setDomain(btn.dataset.domain); shown = PAGE; render(); }));
document.querySelectorAll('[data-open]').forEach(btn => btn.addEventListener('click', () => openProblem(btn.dataset.open)));
document.getElementById('q').addEventListener('input', e => { query = e.target.value.trim().toLowerCase(); shown = PAGE; render(); });
more.addEventListener('click', () => { shown = problems.length; render(); });
render();
"""

ARROW = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
CHEVRON = '<svg class="chev" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M5 8l5 5 5-5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
SEARCH = '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true"><circle cx="7" cy="7" r="4.6" stroke="currentColor" stroke-width="1.4"/><path d="M10.5 10.5L14 14" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/></svg>'


def esc(text: object) -> str:
    return html.escape(str(text or ""), quote=True)


def load_problems() -> list[dict]:
    rows = []
    for domain in DOMAINS:
        for path in sorted((ROOT / "problems" / domain).glob("*/problem.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            rows.append({k: data.get(k) for k in (
                "id", "title", "area", "subdomain", "system", "observable",
                "classical_baseline", "quantum_role", "decision", "has_reference",
            )})
    return rows


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
        f'<button type="button" class="cell {DOMAINS[p["area"]][1]}" style="--i:{i}" data-open="{esc(p["id"])}" '
        f'title="{esc(p["id"])} {esc(p["title"])}" aria-label="{esc(p["id"])} {esc(p["title"])}">{esc(p["id"])}</button>'
        for i, p in enumerate(problems)
    )
    legend = "".join(f'<span class="{cls}"><i></i>{esc(label)}</span>' for label, cls in DOMAINS.values())
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


def problem_template() -> str:
    return f"""<template id="problem-tpl"><li class="problem">
<button type="button" class="phead" aria-expanded="false">
<span class="pid" data-f="id"></span>
<span class="pmain"><span class="ptitle" data-f="title"></span><span class="pmeta"><i></i><span data-f="meta"></span></span>
<span class="pline"><span class="idx">02 算什么</span><span data-f="observable"></span></span>
<span class="pline why"><span class="idx">05 为了什么</span><span data-f="decision"></span></span></span>
<span class="pstate"><span class="ref" data-f="ref"></span></span>
{CHEVRON}
</button>
<div class="pbody" role="region"><div class="pinner"><div class="pcontent">
<dl class="ledger">{part_row(0, field='system')}</dl>
{versus(templated=True)}
<div class="pactions"><span data-f="refnote"></span><a data-link="problem" href="#">完整题面与验收标准</a><a href="../../CONTRIBUTING.md">提交解法</a></div>
</div></div></div>
</li></template>"""


def page(problems: list[dict], stats: dict) -> str:
    domains = stats["domains"]
    total, with_ref = stats["total_problems"], stats["with_reference"]
    by_id = {p["id"]: p for p in problems}
    filters = [f'<button type="button" data-domain="all" aria-pressed="true">全部<span class="num">{total}</span></button>'] + [
        f'<button type="button" class="{cls}" data-domain="{d}" aria-pressed="false"><i></i>{esc(label)}<span class="num">{domains[d]["problems"]}</span></button>'
        for d, (label, cls) in DOMAINS.items()
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
<nav class="navlinks" aria-label="页面导航"><a href="#why">为什么值得做</a><a href="#problems">题库</a><a href="#reference">现有参照</a><a href="#join">怎么参与</a></nav>
<a class="contribute" href="../../CONTRIBUTING.md">参与贡献</a>
</div></header>
<main id="top">
<div class="hero"><div class="wrap hero-grid">
<div>
<p class="kicker">Open problems · v0.1.0</p>
<h1><span class="num">{total}</span> 道还开放着的科学计算题</h1>
<p class="lead">固氮、碳捕集、PFAS 治理、电池、药物、高温超导……每一道题都卡在一个<strong>真实的研发判断</strong>上：经典方法做到了哪一步，量子方法能不能补上。挑一道，提交你的解法；被采纳的解法会记入这道题的参照，并在沉淀出的 skill 里署名。</p>
<div class="cta-row"><a class="btn" href="#problems">挑一道题{ARROW}</a><a class="textlink" href="#why">先看看为什么值得做</a></div>
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

<section id="problems"><div class="wrap">
<div class="section-head"><div><p class="kicker">Problem set</p><h2>题库</h2></div>
<p>每一行告诉你这道题算什么、为了什么；点开看经典基线与量子方法的对照。完整题面、验收标准和现有参照在每道题的题面文件里。</p></div>
<div class="toolbar"><div class="filters" role="group" aria-label="按领域筛选">{''.join(filters)}</div>
<label class="search">{SEARCH}<input id="q" type="search" placeholder="搜索题号、体系或方法：Hubbard、VQE、退火" aria-label="搜索题目"></label></div>
<p class="count" id="count" aria-live="polite"></p>
<ol class="plist" id="plist"></ol>
<button type="button" class="more" id="more">显示全部 {total} 题</button>
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
<li><span class="num">01</span><h3>挑一道题</h3><p>读它的 PROBLEM.md：五段题面、五条验收标准和现有参照都在里面。</p></li>
<li><span class="num">02</span><h3>按模板提交</h3><p>把解法放进 <code>solutions/&lt;题号&gt;/&lt;名字&gt;-&lt;短名&gt;/</code>，包括 SOLUTION.md 与 solution.json。</p></li>
<li><span class="num">03</span><h3>校验后开 PR</h3><p>本地跑一遍校验器，用 <code>git commit -s</code> 签名提交，CI 会再检查一次。</p></li>
</ol>
<pre><code>python3 -I release/tools/check_submissions.py --root .</code></pre>
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
<p class="lead">{total} 道题都还开放着。先读题面，开个 issue 聊聊思路，或者直接提交一份解法。</p>
<a class="btn" href="#problems">去题库{ARROW}</a>
<div class="fine">
<p>题面与文档采用 CC BY 4.0，代码采用 Apache-2.0，贡献需要 DCO 签名。题面目前只有中文，英文版会在下一个版本补上。详见 <a href="../../CONTRIBUTING.md">CONTRIBUTING.md</a>。</p>
<p>社区沉淀出的 skill 也会内置到晓梦 Agent，让更多研发团队可以直接调用。</p>
</div>
</div></footer>
{problem_template()}
<script type="application/json" id="data">{embed(problems)}</script>
<script type="application/json" id="domains">{embed(DOMAINS)}</script>
<script>{JS}</script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    out = Path(parser.parse_args().out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    stats = json.loads((ROOT / "release" / "stats.json").read_text(encoding="utf-8"))
    (out / "index.html").write_text(page(load_problems(), stats), encoding="utf-8")


if __name__ == "__main__":
    main()
