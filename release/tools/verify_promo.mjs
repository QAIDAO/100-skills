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

for (const [width, height] of [[1440, 1000], [768, 1024], [390, 844]]) {
  const page = await browser.newPage({viewport: {width, height}});
  page.on('pageerror', e => errors.push(`${width}: ${e.message}`));
  await page.emulateMedia({reducedMotion: 'reduce', colorScheme: 'light'});
  await page.goto(url);
  check(`${width} 无横向滚动`, await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  check(`${width} 初始显示 12 道题`, (await page.locator('.problem').count()) === 12);
  await page.locator('#more').click();
  const ids = await page.locator('.problem').evaluateAll(rows => rows.map(r => r.dataset.id));
  check(`${width} 全部 84 题可达且不重复`, ids.length === 84 && new Set(ids).size === 84);
  check(`${width} 展开后仍无横向滚动`, await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth));
  await page.screenshot({path: path.join(outDir, `page-${width}.png`), fullPage: false});
  await page.close();
}

const page = await browser.newPage({viewport: {width: 1440, height: 1000}});
page.on('pageerror', e => errors.push(`interact: ${e.message}`));
await page.emulateMedia({reducedMotion: 'reduce', colorScheme: 'light'});
await page.goto(url);
for (const [domain, n] of [['biomedicine', 26], ['applied-materials', 24], ['model-dynamics', 19], ['extensions', 15]]) {
  await page.locator(`[data-domain="${domain}"]`).click();
  await page.locator('#more').click({timeout: 1000}).catch(() => {});
  check(`筛选 ${domain} 得到 ${n} 题`, (await page.locator('.problem').count()) === n);
}
await page.locator('[data-domain="all"]').click();
await page.locator('#q').fill('M01');
check('搜索 M01 得到 1 题', (await page.locator('.problem').count()) === 1);
const row = page.locator('.problem').first();
check('题目行直接显示「算什么」与「为了什么」', await row.locator('.phead').innerText().then(t => t.includes('算什么') && t.includes('为了什么')));
check('收起时详情不可聚焦', await row.locator('.pbody').evaluate(el => el.inert === true));
await row.locator('.phead').click();
await page.waitForTimeout(300);
check('点开后显示五段题面', await row.innerText().then(t => ['研究体系', '算什么', '经典基线', '量子方法的角色', '为了什么'].every(k => t.includes(k))));
check('点开后 aria-expanded 为 true', (await row.locator('.phead').getAttribute('aria-expanded')) === 'true');
await row.screenshot({path: path.join(outDir, 'problem-open-1440.png')});
await row.locator('.phead').focus();
await page.keyboard.press('Enter');
check('键盘 Enter 收起题目', (await row.locator('.phead').getAttribute('aria-expanded')) === 'false' && await row.locator('.pbody').evaluate(el => el.inert === true));
check('题板共 84 格', (await page.locator('.cell').count()) === 84);
await page.locator('#q').fill('');
await page.locator('.cell[data-open="M01"]').click();
await page.waitForTimeout(400);
check('点题板格子打开对应题目并滚到视野内', await page.evaluate(() => {
  const node = document.getElementById('p-M01');
  const top = node?.getBoundingClientRect().top ?? -1;
  return Boolean(node?.classList.contains('open')) && top >= 0 && top < innerHeight;
}));
await page.locator('.stake[data-open="B01"]').click();
await page.waitForTimeout(400);
check('「为什么值得做」可直达对应题目', await page.evaluate(() => document.getElementById('p-B01')?.classList.contains('open')));
await page.locator('#q').fill('不存在的题目xyz');
check('无结果时显示空状态', (await page.locator('.empty').count()) === 1);
const light = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
await page.emulateMedia({colorScheme: 'dark'});
await page.locator('#q').fill('');
const dark = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
check('深色模式切换背景', light !== dark);
await page.screenshot({path: path.join(outDir, 'dark-1440.png')});
await page.close();
await browser.close();

check('无 JS 错误', errors.length === 0);
fs.writeFileSync(path.join(outDir, 'checks.json'), JSON.stringify({checks, errors}, null, 2));
console.log(JSON.stringify({passed: checks.filter(c => c.pass).length, total: checks.length, errors}));
if (checks.some(c => !c.pass)) process.exitCode = 1;
