const {chromium}=require('C:/Users/yundo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url');const fs=require('fs');const path=require('path');
(async()=>{
 const dir=path.resolve(process.argv[2],'lds_viewer');
 const exe=['C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe','C:/Program Files/Google/Chrome/Application/chrome.exe'].find(fs.existsSync);
 const browser=await chromium.launch({headless:true,executablePath:exe});
 const page=await browser.newPage({viewport:{width:1700,height:1450}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(path.join(dir,'index.html')).href);
 await page.locator('#frame').evaluate(img=>img.decode());
 await page.locator('#next').click();if(await page.locator('#number').inputValue()!=='2')throw Error('Next failed');
 await page.keyboard.press('ArrowLeft');if(await page.locator('#number').inputValue()!=='1')throw Error('Previous failed');
 await page.locator('#zoom').click();if(!await page.locator('#frame').evaluate(img=>img.classList.contains('expanded')))throw Error('Zoom failed');
 await page.locator('#zoom').click();
 const groups=JSON.parse(fs.readFileSync(path.join(dir,'manifest.json'),'utf8'));
 for (const index of [...new Set([0,groups.length-1])]){
  await page.locator('#search').selectOption(String(index));
  await page.locator('#number').fill(String(groups[index].frames.length));await page.locator('#number').press('Tab');
  await page.locator('#frame').evaluate(img=>img.decode());
  await page.screenshot({path:path.join(dir,`preview_search_${index}.png`),fullPage:true});
 }
 await browser.close();if(errors.length)throw Error(errors.join('\n'));
 console.log(JSON.stringify({verified:true,searches:groups.length}));
})().catch(e=>{console.error(e);process.exit(1)});
