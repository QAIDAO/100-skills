// 展示页浏览器检查。用法：node verify_promo.mjs <index.html> <输出目录>
// 需要环境变量 PLAYWRIGHT_MODULE（playwright 的 index.mjs 路径）；CHROME_PATH 可选，指定本机 Chrome。
// 写出 <输出目录>/checks.json 与各宽度截图；任一检查失败时退出码为 1。
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';

const [, , pagePath, outDir] = process.argv;
if (!pagePath || !outDir || !process.env.PLAYWRIGHT_MODULE) {
  console.error('用法：PLAYWRIGHT_MODULE=<playwright/index.mjs> node verify_promo.mjs <index.html> <输出目录>');
  process.exit(2);
}
const {chromium} = await import(pathToFileURL(process.env.PLAYWRIGHT_MODULE).href);
fs.mkdirSync(outDir, {recursive: true});
const browser = await chromium.launch({headless: true, ...(process.env.CHROME_PATH ? {executablePath: process.env.CHROME_PATH} : {})});
const checks = [];
const errors = [];
const check = (name, pass) => checks.push({name, pass: Boolean(pass)});
const url = pathToFileURL(path.resolve(pagePath)).href;
const current = page => page.locator('#mdbody .md-card .pid').innerText();
const rows = page => page.locator('.md-row');

for (const [width, height] of [[1440, 1000], [768, 1024], [390, 844]]) {
  const page = await browser.newPage({viewport: {width, height}});
  page.on('pageerror', e => errors.push(`${width}: ${e.message}`));
  await page.emulateMedia({reducedMotion: 'reduce', colorScheme: 'light'});
  await page.goto(url);
  check(`${width} 无横向滚动`, await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  const ids = await rows(page).evaluateAll(rs => rs.map(r => r.dataset.id));
  const total = await page.evaluate(() => JSON.parse(document.getElementById('data').textContent).length);
  check(`${width} 列表列出全部 ${total} 题且不重复`, total >= 84 && ids.length === total && new Set(ids).size === total);
  await rows(page).nth(1).click();
  await page.waitForTimeout(350);
  check(`${width} 点题目后详情显示该题`, (await current(page)) === ids[1]);
  if (width < 980) {
    check(`${width} 手机端详情以全屏面板弹出`, await page.locator('#mddetail.sheet-open').count() === 1);
    await page.screenshot({path: path.join(outDir, `sheet-${width}.png`)});
    await page.locator('#mdclose').click();
    await page.waitForTimeout(350);
    check(`${width} 「返回列表」关闭面板`, await page.locator('#mddetail.sheet-open').count() === 0);
  }
  check(`${width} 打开详情后仍无横向滚动`, await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  await page.screenshot({path: path.join(outDir, `page-${width}.png`), fullPage: false});
  await page.close();
}

const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
page.on('pageerror', e => errors.push(`interact: ${e.message}`));
await page.emulateMedia({reducedMotion: 'reduce', colorScheme: 'light'});
await page.goto(url);
const data = await page.evaluate(() => JSON.parse(document.getElementById('data').textContent));
const tally = key => Object.entries(data.reduce((c, p) => { const k = key(p); c[k] = (c[k] || 0) + 1; return c; }, {}));
for (const [domain, n] of tally(p => p.area)) {
  await page.locator(`[data-domain="${domain}"]`).click();
  check(`筛选 ${domain} 得到 ${n} 题`, (await rows(page).count()) === n);
}
await page.locator('[data-domain="all"]').click();
const levelOf = Object.fromEntries(data.map(p => [p.id, p.track.level]));
for (const [level, n] of tally(p => p.track.level)) {
  await page.locator(`[data-level-filter="${level}"]`).click();
  const shown = await rows(page).evaluateAll(rs => rs.map(r => r.dataset.id));
  check(`难度筛选 ${level} 得到 ${n} 题`, shown.length === n && shown.every(id => levelOf[id] === level));
}
await page.locator('[data-level-filter="all"]').click();
const warmCount = data.filter(p => p.track.level === '热身').length;
check('列表行标出全部热身题', warmCount > 0 && (await page.locator('.md-lv').evaluateAll(es => es.filter(e => e.textContent === '热身').length)) === warmCount);
check('题板标出全部热身题', (await page.locator('.cell.warm').count()) === warmCount);
check('「从热身题开始」列出全部热身题', (await page.locator('.warm-item').count()) === warmCount);
await page.locator('#onlyref').check();
check('「只看有参照」只列有参照的题', (await rows(page).count()) === data.filter(p => p.has_reference).length);
await page.locator('#onlyref').uncheck();

await page.locator('#q').fill('M01');
check('搜索 M01 得到 1 题', (await rows(page).count()) === 1);
const card = page.locator('#mdbody .md-card');
check('详情显示五段题面', await card.innerText().then(t => ['研究体系', '可观测量', '经典基线', '量子方法的角色', '研发决策'].every(k => t.includes(k))));
check('详情显示 5 条验收标准与现有参照', (await card.locator('.criteria li').count()) === 5 && await card.locator('.reftitle').innerText().then(t => t.length > 4));
check('详情显示难度标签', (await card.locator('.lvl').innerText()) === levelOf['M01']);
check('题目链接指向 GitHub 并预填 issue', await card.evaluate(r => r.querySelector('[data-link="problem"]').href.startsWith('https://github.com/') && decodeURIComponent(r.querySelector('[data-link="issue"]').href).includes('[题目] M01')));
await card.screenshot({path: path.join(outDir, 'detail-1440.png')});
await page.locator('#q').fill('');
await rows(page).first().click();
const first = await current(page);
await page.locator('#mdbody [data-step="1"]').click();
const second = await current(page);
check('「下一题」切到下一道', second !== first && second === await rows(page).nth(1).getAttribute('data-id'));
await page.evaluate(() => document.activeElement?.blur());
await page.keyboard.press('ArrowUp');
check('键盘 ↑ 切回上一道', (await current(page)) === first);
check('所有链接都是页内锚点或 https 外链（不依赖本地文件）', await page.evaluate(() => [...document.querySelectorAll('a[href]')].every(a => { const h = a.getAttribute('href'); return h.startsWith('#') || h.startsWith('https://'); })));
check('题板格数等于题目数', (await page.locator('.cell').count()) === data.length);
await page.locator('.cell[data-open="M01"]').click();
await page.waitForTimeout(400);
check('点题板格子打开对应题目并滚到题库', (await current(page)) === 'M01' && await page.evaluate(() => { const t = document.getElementById('problems').getBoundingClientRect().top; return t > -200 && t < innerHeight; }));
await page.locator('.stake[data-open="B01"]').click();
await page.waitForTimeout(300);
check('「为什么值得做」可直达对应题目', (await current(page)) === 'B01');
await page.locator('[data-level-filter="前沿"]').click();
await page.locator('.warm-item[data-open="C11"]').click();
await page.waitForTimeout(300);
check('热身题列表可直达题目，并清除难度筛选', (await current(page)) === 'C11' && (await page.locator('[data-level-filter="all"]').getAttribute('aria-pressed')) === 'true');
check('有 starter 的题在详情里给出 starter 链接', await card.evaluate(r => [...r.querySelectorAll('.pactions a')].some(a => a.href.endsWith('/tree/main/starters/C11'))));
await page.locator('#q').fill('不存在的题目xyz');
check('无结果时显示空状态', (await page.locator('#mdlist .empty').count()) === 1);
await page.locator('#q').fill('');
check('清空搜索后详情恢复显示', (await page.locator('#mdbody .md-card').count()) === 1);

const toc = page.locator('#sidenav');
check('侧边目录覆盖所有章节', await toc.locator('ol a').evaluateAll(as => as.every(a => document.getElementById(a.getAttribute('href').slice(1)))) && (await toc.locator('ol a').count()) >= 7);
await toc.locator('.sn-toggle').click();
check('目录按钮展开目录', await page.locator('#sidenav.open').count() === 1);
await toc.locator('ol a[href="#join"]').click();
await page.waitForTimeout(400);
check('点目录项跳到对应章节并收起', await page.locator('#sidenav.open').count() === 0 && await page.evaluate(() => { const t = document.getElementById('join').getBoundingClientRect().top; return t >= -10 && t < innerHeight / 2; }));

const light = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
await page.emulateMedia({colorScheme: 'dark'});
const dark = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
check('深色模式切换背景', light !== dark);
await page.evaluate(() => document.getElementById('problems').scrollIntoView());
await page.screenshot({path: path.join(outDir, 'dark-1440.png')});
await page.close();

const deep = await browser.newPage({viewport: {width: 1600, height: 1000}});
deep.on('pageerror', e => errors.push(`deep: ${e.message}`));
await deep.emulateMedia({reducedMotion: 'reduce', colorScheme: 'light'});
await deep.goto(url + '#p-F16');
await deep.waitForTimeout(300);
check('深链 #p-F16 直接打开该题', (await current(deep)) === 'F16');
check('深链打开的题在列表里可见', await deep.evaluate(() => { const r = document.getElementById('row-F16').getBoundingClientRect(); return r.top >= 0 && r.bottom <= innerHeight; }));
check('宽屏侧边目录常驻且不出按钮', await deep.locator('#sidenav .sn-toggle').isHidden() && await deep.locator('#sidenav nav').isVisible());
await deep.screenshot({path: path.join(outDir, 'wide-1600.png')});
await deep.close();
await browser.close();

check('无 JS 错误', errors.length === 0);
fs.writeFileSync(path.join(outDir, 'checks.json'), JSON.stringify({checks, errors}, null, 2));
console.log(JSON.stringify({passed: checks.filter(c => c.pass).length, total: checks.length, errors}));
if (checks.some(c => !c.pass)) process.exitCode = 1;
