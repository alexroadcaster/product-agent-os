/* Adapted from designbookmark.com/motion-src/sidebar-collapse/side.js and
   shared/motion.js. Same unit-mass springs, four Euler substeps, delays and
   label travel. Product navigation has no showcase autoplay/theme messages. */
(() => {
  const root=document.documentElement, side=document.querySelector('.sidebar');
  const nav=document.querySelector('#nav'), toggle=document.querySelector('#sidebar-toggle');
  const brand=side.querySelector('.brand'), media=matchMedia('(prefers-reduced-motion: reduce)');
  const pairs={width:[260,24],rotation:[300,22],highlight:[380,28],label:[300,26]};
  for(const key of Object.keys(pairs)){
    const parsed=getComputedStyle(root).getPropertyValue(`--sidebar-spring-${key}`).trim().split(/\s+/).map(Number);
    if(parsed.length===2&&parsed.every(Number.isFinite))pairs[key]=parsed;
  }
  const spring=(x,key)=>({x,v:0,t:x,k:pairs[key][0],c:pairs[key][1]});
  const width=spring(216,'width'), rotation=spring(0,'rotation'), highlight=spring(0,'highlight');
  const clamp=x=>Math.max(0,Math.min(1,x));
  let expanded=true, labels=[], pill, frame=0, last=0, tooltipTarget=null;
  const tip=document.createElement('div');tip.id='sidebar-tooltip';tip.className='sidebar-tooltip';tip.role='tooltip';tip.hidden=true;document.body.append(tip);
  const moving=s=>Math.abs(s.x-s.t)>.005||Math.abs(s.v)>.01;
  function hideTip(){tooltipTarget?.removeAttribute('aria-describedby');tooltipTarget=null;tip.hidden=true;}
  function showTip(target){
    if(expanded||!target)return;hideTip();tooltipTarget=target;
    tip.textContent=target.getAttribute('aria-label');target.setAttribute('aria-describedby',tip.id);tip.hidden=false;
    const box=target.getBoundingClientRect(), edge=side.getBoundingClientRect();
    tip.style.left=`${edge.right+8}px`;tip.style.top=`${Math.max(8,Math.min(innerHeight-tip.offsetHeight-64,box.top+(box.height-tip.offsetHeight)/2))}px`;
  }
  function paint(){
    root.style.setProperty('--sidebar-width',`${width.x.toFixed(3)}px`);
    toggle.firstElementChild.style.transform=`rotate(${(180*rotation.x).toFixed(3)}deg)`;
    side.querySelector('.brand-mark').style.opacity=clamp(1-rotation.x*2);
    for(const label of labels){const opacity=clamp(label.s.x);label.el.style.opacity=opacity;label.el.style.transform=`translateX(${(1-opacity)*-10}px)`;}
    if(pill)pill.style.transform=`translateY(${highlight.x.toFixed(3)}px)`;
  }
  function snap(){
    cancelAnimationFrame(frame);frame=0;
    for(const s of [width,rotation,highlight,...labels.map(l=>l.s)]){s.x=s.t;s.v=0;}
    for(const l of labels)l.delay=0;
    paint();
  }
  function tick(now){
    const dt=Math.min((now-last)/1000,1/30);last=now;
    for(const l of labels)if(l.delay>0){l.delay-=dt;if(l.delay<=0)l.s.t=expanded?1:0;}
    const springs=[width,rotation,highlight,...labels.map(l=>l.s)];
    for(let i=0;i<4;i++)for(const s of springs){const h=dt/4;s.v+=(-s.k*(s.x-s.t)-s.c*s.v)*h;s.x+=s.v*h;}
    paint();frame=0;
    if(springs.some(moving)||labels.some(l=>l.delay>0))frame=requestAnimationFrame(tick);
    else snap();
  }
  function wake(){if(media.matches){for(const l of labels)l.s.t=expanded?1:0;snap();return;}if(!frame){last=performance.now();frame=requestAnimationFrame(tick);}}
  function targetHighlight(immediate=false){
    const selected=nav.querySelector('.nav-link.active');if(!selected||!pill)return;
    highlight.t=selected.getBoundingClientRect().top-nav.getBoundingClientRect().top+nav.scrollTop;
    pill.style.height=`${selected.offsetHeight}px`;
    if(immediate){highlight.x=highlight.t;highlight.v=0;}
  }
  function refresh(first=false){
    hideTip();
    // The existing renderer replaces the nav. Rebind only those labels, keeping
    // the component's spring state and collapsed selection across routes.
    const old=new Map(labels.map(l=>[l.key,l]));
    nav.querySelectorAll('.nav-link').forEach(link=>{
      const text=[...link.childNodes].filter(n=>n.nodeType===Node.TEXT_NODE).map(n=>n.textContent).join('').trim();
      if(text){const span=document.createElement('span');span.className='sidebar-label';span.textContent=text;
        [...link.childNodes].filter(n=>n.nodeType===Node.TEXT_NODE).forEach(n=>n.remove());link.append(span);}
      link.setAttribute('aria-label',link.textContent.trim());
    });
    side.querySelector('.project-picker>span:nth-child(2)').classList.add('sidebar-label');
    side.querySelector('.project-picker>span:last-child').classList.add('sidebar-label');
    side.querySelector('.project-picker').setAttribute('aria-label',`Выбрать проект: ${side.querySelector('.project-picker strong').textContent}`);
    side.querySelector('.sidebar-foot>span:last-child').classList.add('sidebar-label');
    side.querySelectorAll('.nav-group-label').forEach(el=>el.classList.add('sidebar-label'));
    labels=[...side.querySelectorAll('.sidebar-label')].map((el,i)=>{const key=el.closest('[data-section]')?.dataset.section||`label-${i}`;return {el,key,s:old.get(key)?.s||spring(expanded?1:0,'label'),delay:old.get(key)?.delay||0};});
    pill=document.createElement('span');pill.className='sidebar-highlight';pill.setAttribute('aria-hidden','true');nav.prepend(pill);
    targetHighlight(first);paint();wake();
  }
  function setExpanded(value){
    expanded=value;hideTip();side.dataset.collapsed=String(!value);
    toggle.setAttribute('aria-expanded',String(value));toggle.setAttribute('aria-label',value?'Свернуть меню':'Развернуть меню');toggle.title=toggle.getAttribute('aria-label');
    brand.tabIndex=value?0:-1;brand.setAttribute('aria-hidden',String(!value));
    width.t=value?216:64;rotation.t=value?0:1;
    labels.forEach((l,i)=>{l.delay=value?.06+i*.04:0;if(!value)l.s.t=0;});wake();
  }
  toggle.addEventListener('click',()=>setExpanded(!expanded));
  side.addEventListener('pointerover',e=>showTip(e.target.closest('.nav-link,.project-picker')));
  side.addEventListener('pointerout',e=>{if(!tooltipTarget?.contains(e.relatedTarget)&&!tooltipTarget?.contains(document.activeElement))hideTip();});
  side.addEventListener('focusin',e=>showTip(e.target.closest('.nav-link,.project-picker')));
  side.addEventListener('focusout',hideTip);
  nav.addEventListener('scroll',()=>{const focused=nav.contains(document.activeElement)?document.activeElement.closest('.nav-link'):null;if(focused)showTip(focused);else hideTip();});
  document.addEventListener('keydown',e=>{if(e.key==='Escape')hideTip();});
  addEventListener('resize',()=>{hideTip();targetHighlight(true);paint();if(side.contains(document.activeElement))showTip(document.activeElement.closest('.nav-link,.project-picker'));});
  media.addEventListener('change',()=>{if(media.matches){for(const l of labels)l.s.t=expanded?1:0;snap();}});
  const previousRender=render;
  render=function(...args){const result=previousRender(...args);refresh();return result;};
  window.DESIGN_SIDEBAR={springs:pairs,get settled(){return !frame;},get framePending(){return !!frame;},get expanded(){return expanded;}};
  refresh(true);
})();
