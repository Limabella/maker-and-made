const fs=require('fs'),path=require('path');
const rootFlag=process.argv.indexOf('--skill-root');
const skillRoot=path.resolve(rootFlag>=0?process.argv[rootFlag+1]:path.join(__dirname,'..')); 
const flag=n=>{const i=process.argv.indexOf('--'+n);return i<0?null:process.argv[i+1];};
const input=flag('input'),out=flag('output');
if(!input||!out)throw Error('Usage: node render-calendar.cjs --input calendar.json --output month.png [--modules NODE_MODULES] [--chrome CHROME_PATH] [--font FONT_PATH]');
const config=JSON.parse(fs.readFileSync(input,'utf8'));
const mode=JSON.parse(fs.readFileSync(path.join(skillRoot,'references','mode.json'),'utf8')).mode;
const {year,month}=config;
if(!Number.isInteger(year)||year<1900||year>2200||!Number.isInteger(month)||month<1||month>12)throw Error('Invalid calendar year/month');
if(!config.asOf||!config.bannerPath)throw Error('asOf and bannerPath are required');
const last=new Date(Date.UTC(year,month,0)).getUTCDate(),first=new Date(Date.UTC(year,month-1,1)).getUTCDay();
const rows=Math.ceil((first+last)/7),prefix=`${year}-${String(month).padStart(2,'0')}`;
const esc=s=>String(s??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const uri=p=>{const ext=path.extname(p).toLowerCase(),mime={'.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp'}[ext];if(!mime)throw Error('Unsupported banner format '+ext);return 'data:'+mime+';base64,'+fs.readFileSync(p).toString('base64');};
const groups={market:config.marketEvents||[],culture:config.cultureEvents||[]};
for(const [group,events]of Object.entries(groups))for(const event of events){
 const day=Number(event.date?.slice(-2));
 if(!event.date?.startsWith(prefix+'-')||!/^\d{4}-\d{2}-\d{2}$/.test(event.date)||day<1||day>last)throw Error('Event outside requested month: '+event.date);
 if(!event.title||!event.time||!event.point)throw Error('Event needs title/time/point');
 if(!['confirmed','tentative','example','check'].includes(event.status))throw Error('Invalid event status: '+event.title);
 if(event.status==='confirmed'&&!/^https?:\/\//.test(event.source||''))throw Error('Confirmed event requires source URL: '+event.title);
 if(event.status==='tentative'&&!/예정|잠정|확인/.test(event.title+' '+event.time))throw Error('Tentative event must be labelled');
 if(event.status==='example'&&!/예시/.test(event.time))throw Error('Example meeting must say 예시');
 if(event.status==='check'&&!/확인일/.test(event.title))throw Error('Ranking check must say 확인일');
 if(!Number.isInteger(event.stars??0)||(event.stars??0)<0||(event.stars??0)>3)throw Error('Stars must be 0–3');
 if(group==='culture'&&(event.stars??0)!==0)throw Error('Market influence stars belong only to market events');
}
const banner=uri(path.resolve(config.bannerPath)),franklin=mode==='culture'?null:uri(path.join(skillRoot,'assets','bfr-n.png'));
const goethe=mode==='culture'?uri(path.join(skillRoot,'assets','gth-n.png')):null;
const monthName=['JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER'][month-1];
const title=mode==='culture'?config.cultureTitle:config.marketTitle;
if(!title)throw Error('Provide a concise month-specific title');
const quote=config.quote||(mode==='culture'?{text:'한 권을 읽고,\n한 문장을 나눠요.',attribution:'MaAM · 함께 읽는 '+month+'월'}:{text:'고통 + 성찰 = 발전',attribution:'— 레이 달리오 · 『원칙』 (번역)'});
const speech=`<div class="speech"><div class="quote-text">${esc(quote.text).replaceAll('\n','<br>')}</div><small>${esc(quote.attribution)}</small></div>`;
function calendar(group){
 let cells='';
 for(let i=0;i<rows*7;i++){
  const day=i-first+1,inside=day>=1&&day<=last;
  const events=inside?groups[group].filter(e=>e.date===prefix+'-'+String(day).padStart(2,'0')):[];
  cells+=`<div class="day ${events.length>=3?'dense':''} ${inside?'':'empty'} ${i%7===0?'sun':i%7===6?'sat':''}">${inside?`<div class="date">${String(day).padStart(2,'0')}</div>${events.map(e=>`<div class="event"><div class="event-title">${e.stars?`<b class="stars">${'★'.repeat(e.stars)}</b>`:''}${esc(e.title)}</div><div class="time">${esc(e.time)}</div><div class="point">${esc(e.point)}</div></div>`).join('')}`:''}</div>`;
 }
 return `<section class="calendar"><div class="weekdays">${['일 SUN','월 MON','화 TUE','수 WED','목 THU','금 FRI','토 SAT'].map(t=>'<span>'+t+'</span>').join('')}</div><div class="grid">${cells}</div></section>`;
}
const mascot=`<img class="bot" src="${config.mascotPath?uri(path.resolve(config.mascotPath)):(mode==='culture'?goethe:franklin)}" alt="${esc(config.mascotName||(mode==='culture'?'GTH-N':'BFR-N'))}">`;
const brand=mode==='market'?'MaAM Market Brief':mode==='culture'?'MaAM Culture & Books':'MaAM Dual';
const band=`<div class="month-line"><h1>${esc(title)}</h1>${speech}${mascot}</div>`;
const body=mode==='dual'?`<div class="dual"><div class="shared-line">${band}</div><div class="dual-panel">${calendar('market')}</div><div class="dual-panel">${calendar('culture')}</div></div>`:band+calendar(mode);
const fallbackHome=process.env.USERPROFILE||process.env.HOME;
const modules=flag('modules')||process.env.MAAM_NODE_MODULES||path.join(fallbackHome,'.cache','codex-runtimes','codex-primary-runtime','dependencies','node','node_modules');
const {chromium}=require(path.join(modules,'playwright'));
const chrome=flag('chrome')||process.env.MAAM_CHROME_PATH||(process.platform==='win32'?'C:/Program Files/Google/Chrome/Application/chrome.exe':null);
const font=flag('font')||process.env.MAAM_FONT_PATH||(process.platform==='win32'?'C:/Windows/Fonts/NotoSansKR-VF.ttf':null);
if(!font||!fs.existsSync(font))throw Error('Pass --font with Noto Sans KR font path');
const fontUri='data:font/ttf;base64,'+fs.readFileSync(font).toString('base64');
const dual=mode==='dual';
const css=`
@font-face{font-family:MaamSans;src:url(${fontUri}) format('truetype');font-weight:100 900}
*{box-sizing:border-box}body{margin:0;background:white;font-family:MaamSans,sans-serif;color:#34463f}
#canvas{width:${dual?7680:3840}px;padding:${dual?'84px':'44px 64px 24px'};${dual?'border:12px solid #161a18;':''}background:white}
.brand{height:60px;font-size:${dual?38:32}px;font-weight:500;letter-spacing:1px;color:#31594f}
.photo{height:${Math.round((dual?7488:3712)/config.bannerAspectRatio)}px;position:relative;overflow:hidden}.photo-img{width:100%;height:100%;object-fit:cover;object-position:${esc(config.bannerPosition||'center 51%')}}
.stamp{position:absolute;bottom:${dual?68:34}px;left:${dual?100:50}px;display:flex;align-items:flex-end;gap:${dual?42:28}px;color:white;text-shadow:0 2px 6px #0003}
.stamp b{font-size:${dual?340:210}px;font-weight:500;line-height:.95;letter-spacing:-8px}.stamp span{font-size:${dual?60:38}px;letter-spacing:6px;margin-bottom:15px}.stamp small{display:block;font-size:${dual?100:65}px;letter-spacing:6px;margin-top:12px}
.month-line{height:400px;position:relative;background:white}.month-line h1{position:absolute;top:78px;left:0;margin:0;font-size:86px;font-weight:600;line-height:1.4;letter-spacing:-1.5px;max-width:2100px;word-break:keep-all}
.bot{position:absolute;right:44px;bottom:16px;width:220px;height:330px;object-fit:contain;filter:drop-shadow(-8px 12px 10px #8774564d)}
.speech{position:absolute;right:340px;bottom:85px;width:1140px;padding:32px 40px;background:#fffef8;border:2px solid #d2c4a9;border-radius:40px;box-shadow:0 4px 18px #203c2214;font-size:54px;line-height:1.55;font-weight:400;letter-spacing:-1px;color:#2e5147;word-break:keep-all}
.speech small{display:block;font-size:34px;line-height:1.5;letter-spacing:0;margin-top:18px;color:#7d826e}
.speech:before{content:'';position:absolute;right:-36px;bottom:58px;border-top:23px solid transparent;border-bottom:9px solid transparent;border-left:37px solid #d2c4a9;transform:rotate(9deg)}
.speech:after{content:'';position:absolute;right:-32px;bottom:60px;border-top:21px solid transparent;border-bottom:8px solid transparent;border-left:35px solid #fffef8;transform:rotate(9deg)}
.calendar{border-top:2px solid #7b9388;border-bottom:2px solid #7b9388}.weekdays{display:grid;grid-template-columns:repeat(7,1fr);height:57px;text-align:center;align-items:center;background:#f4f6f2;font-size:32px;font-weight:700;color:#466559}
.weekdays span:first-child,.sun .date{color:#a04d3e}.weekdays span:last-child,.sat .date{color:#3d728a}
.grid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));grid-template-rows:repeat(${rows},var(--row-height,440px))}
.day{padding:14px 17px;border-top:1px solid #cbd3cd;border-right:1px solid #cbd3cd;overflow:hidden;min-width:0}.day:nth-child(7n){border-right:0}.empty{background:#fafbf9}
.date{font-size:48px;line-height:1.4;font-weight:500;margin-bottom:12px}.event{padding:4px 0 7px;margin-bottom:10px}.event-title{font-size:40px;font-weight:700;line-height:1.5;word-break:keep-all;letter-spacing:-.6px;color:#314c42}
.time{font-size:28px;line-height:1.35;margin:3px 0;color:#7c8981}.point{font-size:30px;line-height:1.35;word-break:keep-all;letter-spacing:-.5px;color:#5d7066}.stars{color:#9f834b;margin-right:8px;white-space:nowrap}
.dense .date{font-size:36px;margin-bottom:6px}.dense .event{padding:0;margin-bottom:2px}.dense .event-title{font-size:36px}.dense .time,.dense .point{font-size:24px;line-height:1.2}.dense .time{margin:2px 0}
.dual{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 64px;margin-top:160px}.shared-line{grid-column:1/-1}.dual-panel{min-width:0}
.bottom-space{height:${dual?175:58}px}
`;
(async()=>{
 const browser=await chromium.launch({headless:true,...(chrome?{executablePath:chrome}:{})});
 try{
  const page=await browser.newPage({viewport:{width:dual?7680:3840,height:2160}});
  await page.setContent(`<html lang="ko"><head><meta charset="utf-8"><style>${css}</style></head><body><main id="canvas"><div class="brand">${brand}</div><div class="photo"><img class="photo-img" src="${banner}"><div class="stamp"><b>${String(month).padStart(2,'0')}</b><span>${monthName}<small>${year}</small></span></div></div>${body}<div class="bottom-space"></div></main></body></html>`);
  await page.evaluate(()=>document.fonts.ready);await page.locator('img').evaluateAll(xs=>Promise.all(xs.map(x=>x.decode())));
  await page.evaluate(()=>{
   const band=document.querySelector('.month-line'),title=band.querySelector('h1'),bubble=band.querySelector('.speech');
   const needed=Math.max(400,title.offsetHeight+156,bubble.offsetHeight+140);band.style.height=needed+'px';
   const days=[...document.querySelectorAll('.day')];let maximum=440;
   for(const day of days){const end=day.lastElementChild;if(end)maximum=Math.max(maximum,Math.ceil(end.getBoundingClientRect().bottom-day.getBoundingClientRect().top+18));}
   document.querySelector('#canvas').style.setProperty('--row-height',maximum+'px');
  });
  const qa=await page.evaluate(()=>{
   const overflow=[...document.querySelectorAll('.day,.event-title,.time,.point,.quote-text,.speech small')].filter(e=>e.scrollHeight>e.clientHeight+2||e.scrollWidth>e.clientWidth+2).map(e=>e.textContent);
   const title=document.querySelector('h1').getBoundingClientRect(),bubble=document.querySelector('.speech').getBoundingClientRect();
   return {width:document.querySelector('#canvas').offsetWidth,height:document.querySelector('#canvas').offsetHeight,days:document.querySelectorAll('.date').length,bots:document.querySelectorAll('.bot').length,events:document.querySelectorAll('.event').length,overflow,titleSpeechOverlap:title.right>bubble.left&&title.left<bubble.right&&title.bottom>bubble.top&&title.top<bubble.bottom};
  });
  if(qa.overflow.length||qa.titleSpeechOverlap)throw Error('Layout needs editing: '+JSON.stringify(qa));
  fs.mkdirSync(path.dirname(path.resolve(out)),{recursive:true});
  await page.locator('#canvas').screenshot({path:path.resolve(out)});
  fs.writeFileSync(path.resolve(out)+'.qa.json',JSON.stringify({mode,year,month,rows,asOf:config.asOf,...qa},null,2));
  const notes=`# ${brand} · ${year}-${String(month).padStart(2,'0')}\n\n편집 기준: ${config.asOf}. 해외 일정의 현지 날짜·한국 시간 구분은 각 항목에 표시. 예시 모임과 순위 확인일은 편집 일정. ★는 예상 시장 영향 범위이며 방향·수익률을 뜻하지 않음.\n\n`+Object.entries(groups).map(([g,es])=>'## '+g+'\n\n'+es.map(e=>'- '+e.date+' | '+e.title+' | '+e.time+' | '+e.point+' | '+e.status+(e.source?' | [출처]('+e.source+')':'')).join('\n')).join('\n\n')+(config.pending?.length?'\n\n## 날짜 확인 대기\n\n'+config.pending.map(e=>'- '+(typeof e==='string'?e:JSON.stringify(e))).join('\n'):'')+(quote.source?'\n\n명언 출처: '+quote.source:'');
  fs.writeFileSync(path.resolve(out)+'.sources.md',notes);
  console.log(JSON.stringify({output:path.resolve(out),mode,year,month,rows,...qa},null,2));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
