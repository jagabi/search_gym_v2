const {chromium} = require('C:/Users/yundo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('fs');
const {pathToFileURL} = require('url');
const dir = 'C:/Users/yundo/Desktop/search_gym_v2/analysis/visuals/lds_actions/';
(async()=>{
  const executablePath = ['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','C:/Program Files/Google/Chrome/Application/chrome.exe'].find(p=>fs.existsSync(p));
  const browser = await chromium.launch({headless:true, executablePath});
  const page = await browser.newPage({viewport:{width:1700,height:1400},deviceScaleFactor:1});
  const errors=[]; page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(dir+'index.html').href);
  await page.locator('#frame').evaluate(img=>img.decode());
  await page.locator('#next').click();
  if(await page.locator('#number').inputValue()!=='2') throw Error('Next failed');
  await page.keyboard.press('ArrowLeft');
  if(await page.locator('#number').inputValue()!=='1') throw Error('Back failed');
  for(const action of [27,67,127]){
    await page.locator('#number').fill(String(action));
    await page.locator('#number').press('Tab');
    await page.locator('#frame').evaluate(img=>img.decode());
    await page.screenshot({path:dir+'preview_'+action+'.png',fullPage:true});
  }
  if(errors.length) throw Error(errors.join('\n'));
  const svgPage=await browser.newPage();
  await svgPage.goto(pathToFileURL(dir+'action_127.svg').href);
  const overflow=await svgPage.locator('text').evaluateAll(ts=>ts.map(t=>({s:t.textContent,b:t.getBBox()})).filter(t=>t.b.x<0||t.b.x+t.b.width>1700));
  console.log(JSON.stringify({viewer:'passed',actions:127,textOverflow:overflow.map(t=>t.s)}));
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
