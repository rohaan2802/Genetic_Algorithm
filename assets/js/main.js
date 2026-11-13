(function(){
  var root=document.documentElement;
  var themeBtn=document.getElementById('theme-toggle');
  function setTheme(t){
    root.setAttribute('data-theme',t);
    try{localStorage.setItem('ga-theme',t)}catch(e){}
    if(themeBtn) themeBtn.setAttribute('aria-label',t==='dark'?'Switch to light theme':'Switch to dark theme');
    var m=document.querySelector('meta[name="theme-color"]');
    if(m)m.setAttribute('content',t==='dark'?'#14161c':'#f5f1ef');
  }
  var saved=null;
  try{saved=localStorage.getItem('ga-theme')}catch(e){}
  setTheme(saved||root.getAttribute('data-theme')||'dark');
  if(themeBtn) themeBtn.addEventListener('click',function(){
    setTheme(root.getAttribute('data-theme')==='dark'?'light':'dark');
  });

  var menuBtn=document.getElementById('menu-toggle'),links=document.getElementById('nav-links');
  function closeMenu(){if(!links||!menuBtn)return;links.classList.remove('open');menuBtn.setAttribute('aria-expanded','false')}
  if(menuBtn&&links){
    menuBtn.addEventListener('click',function(){
      var o=links.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded',o);
    });
    links.addEventListener('click',function(event){if(event.target.closest('a')) closeMenu()});
    document.addEventListener('keydown',function(event){
      if(event.key==='Escape'&&links.classList.contains('open')){closeMenu();menuBtn.focus()}
    });
  }
  window.addEventListener('resize',function(){
    if(window.innerWidth>999) closeMenu();
  });

  var navA=links?[].slice.call(links.querySelectorAll('a')):[];
  var secs=navA.map(function(a){return document.querySelector(a.getAttribute('href'))}).filter(Boolean);
  if('IntersectionObserver' in window){
    var spy=new IntersectionObserver(function(es){
      es.forEach(function(en){
        if(en.isIntersecting){
          navA.forEach(function(a){
            var on=a.getAttribute('href')==='#'+en.target.id;
            a.classList.toggle('active',on);
            if(on)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');
          });
        }
      });
    },{rootMargin:'-45% 0px -50% 0px'});
    secs.forEach(function(s){spy.observe(s)});
    var rv=new IntersectionObserver(function(es){
      es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');rv.unobserve(en.target)}});
    },{rootMargin:'0px 0px -8% 0px'});
    document.querySelectorAll('.reveal').forEach(function(el){rv.observe(el)});
  }else{
    document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in')});
  }

  document.addEventListener('click',function(e){
    var b=e.target.closest('.btn');if(!b)return;
    var r=b.getBoundingClientRect(),s=Math.max(r.width,r.height),sp=document.createElement('span');
    sp.className='ripple';sp.style.width=sp.style.height=s+'px';
    sp.style.left=(e.clientX-r.left-s/2)+'px';sp.style.top=(e.clientY-r.top-s/2)+'px';
    b.appendChild(sp);setTimeout(function(){sp.remove()},650);
  });

  var top=document.getElementById('to-top');
  function syncTop(){
    if(!top)return;
    var y=window.scrollY||document.documentElement.scrollTop||0;
    var show=y>200;
    top.classList.toggle('show',show);
    top.tabIndex=show?0:-1;
    top.setAttribute('aria-hidden',show?'false':'true');
  }
  ['scroll','touchmove','wheel','resize'].forEach(function(ev){
    window.addEventListener(ev,syncTop,{passive:true});
  });
  if(window.visualViewport) window.visualViewport.addEventListener('resize',syncTop);
  setInterval(syncTop,400);
  syncTop();
  if(top) top.addEventListener('click',function(e){
    e.preventDefault();
    var prev=root.style.scrollBehavior;
    root.style.scrollBehavior='auto';
    if(window.scrollTo) window.scrollTo(0,0);
    root.scrollTop=0;
    if(document.body) document.body.scrollTop=0;
    var dest=document.getElementById('top');
    if(dest&&dest.scrollIntoView) dest.scrollIntoView({block:'start',behavior:'auto'});
    root.style.scrollBehavior=prev;
  });

  document.querySelectorAll('.code-wrap').forEach(function(w){
    var b=w.querySelector('.copy'),pre=w.querySelector('pre');
    if(!b||!pre)return;
    b.addEventListener('click',function(){
      var c=pre.querySelector('code');var txt=(c||pre).innerText;
      (navigator.clipboard?navigator.clipboard.writeText(txt):Promise.reject()).then(function(){
        b.textContent='Copied!';
      },function(){b.textContent='Press Ctrl+C'});
      setTimeout(function(){b.textContent='Copy'},1600);
    });
  });

  var shots=[].slice.call(document.querySelectorAll('.shot'));
  var groups=[].slice.call(document.querySelectorAll('.gallery-group'));
  var chips=[].slice.call(document.querySelectorAll('.chip'));
  var q=document.getElementById('search'),empty=document.getElementById('no-results');
  var cat='all';
  function filter(){
    var term=(q&&q.value||'').trim().toLowerCase(),n=0;
    shots.forEach(function(s){
      var ok=(cat==='all'||s.dataset.cat===cat)&&(!term||s.textContent.toLowerCase().indexOf(term)>-1);
      s.classList.toggle('hide',!ok);if(ok)n++;
    });
    groups.forEach(function(group){group.hidden=!group.querySelector('.shot:not(.hide)')});
    if(empty) empty.style.display=n?'none':'block';
  }
  chips.forEach(function(c){c.addEventListener('click',function(){
    cat=c.dataset.filter;chips.forEach(function(x){x.setAttribute('aria-pressed',x===c?'true':'false')});filter();
  })});
  if(q) q.addEventListener('input',filter);

  function attachHScroll(el){
    if(!el||el.closest('.h-scroll-host'))return;
    var host=document.createElement('div');
    host.className='h-scroll-host';
    el.parentNode.insertBefore(host,el);
    host.appendChild(el);
    var bar=document.createElement('div');
    bar.className='h-scroll-bar';
    bar.setAttribute('aria-hidden','true');
    var thumb=document.createElement('div');
    thumb.className='h-scroll-thumb';
    bar.appendChild(thumb);
    host.appendChild(bar);
    function sync(){
      var sw=el.scrollWidth,cw=el.clientWidth,sl=el.scrollLeft;
      var overflow=sw>cw+2;
      host.classList.toggle('has-h-scroll',overflow);
      if(!overflow)return;
      var tw=bar.clientWidth,th=Math.max(28,tw*cw/sw),max=Math.max(0,tw-th);
      var x=(sw-cw)>0?max*sl/(sw-cw):0;
      thumb.style.width=th+'px';
      thumb.style.transform='translateX('+x+'px)';
    }
    el.addEventListener('scroll',sync,{passive:true});
    window.addEventListener('resize',sync);
    if(window.visualViewport) window.visualViewport.addEventListener('resize',sync);
    bar.addEventListener('pointerdown',function(e){
      e.preventDefault();
      var rect=bar.getBoundingClientRect();
      function at(clientX){
        var tw=bar.clientWidth,th=thumb.offsetWidth,max=Math.max(0,tw-th);
        var x=clientX-rect.left-th/2;
        if(x<0)x=0;if(x>max)x=max;
        var sw=el.scrollWidth,cw=el.clientWidth;
        el.scrollLeft=(sw-cw)*x/max;
      }
      at(e.clientX);
      function move(ev){at(ev.clientX)}
      function up(){
        document.removeEventListener('pointermove',move);
        document.removeEventListener('pointerup',up);
      }
      document.addEventListener('pointermove',move);
      document.addEventListener('pointerup',up);
    });
    sync();
    setTimeout(sync,400);
    setTimeout(sync,1200);
    return sync;
  }
  var hScrollSyncs=[];
  document.querySelectorAll('.table-wrap, pre.code, pre.tree').forEach(function(el){
    var s=attachHScroll(el);if(s)hScrollSyncs.push(s);
  });
  window.addEventListener('load',function(){hScrollSyncs.forEach(function(s){s()})});

  var lb=document.getElementById('lightbox');
  if(!lb)return;
  var lbImg=lb.querySelector('img');
  var lbCap=lb.querySelector('.lb-caption')||lb.querySelector('p');
  var lbCount=lb.querySelector('.lb-count');
  var originalLink=lb.querySelector('.lb-original');
  var idx=0,lastFocus=null,lockY=0;
  var scale=1,tx=0,ty=0,pinching=false,swiping=false,pinchOccurred=false;
  var sx=0,sy=0,lastX=0,lastY=0,startDist=0,startScale=1;

  function visible(){return shots.filter(function(s){return !s.classList.contains('hide')})}
  function applyZoom(){
    if(!lbImg)return;
    if(scale<=1.001&&!tx&&!ty){lbImg.style.transform='';return}
    lbImg.style.transform='translate('+tx+'px,'+ty+'px) scale('+scale+')';
  }
  function resetZoom(){
    scale=1;tx=0;ty=0;pinching=false;swiping=false;pinchOccurred=false;
    if(lbImg)lbImg.style.transform='';
  }
  function headingOf(s){
    var cap=s.querySelector('figcaption');
    if(!cap)return '';
    var node=cap.childNodes[0];
    return node&&node.textContent?node.textContent.trim():cap.textContent.trim();
  }
  function show(i){
    var v=visible();if(!v.length)return;
    idx=(i+v.length)%v.length;
    var s=v[idx],im=s.querySelector('img');
    var src=s.dataset.full||(im&&im.getAttribute('src'))||'';
    lbImg.src=src;
    lbImg.alt=im?im.alt:'';
    if(originalLink){originalLink.href=src;originalLink.setAttribute('aria-label','Open original image in a new tab')}
    var title=headingOf(s);
    if(lbCap)lbCap.textContent=title;
    if(lbCount)lbCount.textContent=(idx+1)+'/'+v.length;
    else if(lbCap)lbCap.textContent=(idx+1)+'/'+v.length+(title?' — '+title:'');
    lb.setAttribute('aria-label',title+' ('+(idx+1)+' of '+v.length+')');
    resetZoom();
  }
  function lockScroll(){
    lockY=window.scrollY||document.documentElement.scrollTop||0;
    document.body.style.overflow='hidden';
    document.documentElement.style.overflow='hidden';
    document.body.style.position='fixed';
    document.body.style.top='-'+lockY+'px';
    document.body.style.left='0';
    document.body.style.right='0';
    document.body.style.width='100%';
  }
  function unlockScroll(){
    document.body.style.overflow='';
    document.documentElement.style.overflow='';
    document.body.style.position='';
    document.body.style.top='';
    document.body.style.left='';
    document.body.style.right='';
    document.body.style.width='';
    if(window.scrollTo)window.scrollTo(0,lockY);
  }
  function open(s){
    lastFocus=document.activeElement;
    var v=visible();
    var i=v.indexOf(s);if(i<0)i=0;
    show(i);
    lb.classList.add('open');
    lb.setAttribute('aria-hidden','false');
    lockScroll();
    var c=lb.querySelector('.close');if(c)c.focus();
  }
  function close(){
    if(!lb.classList.contains('open'))return;
    lb.classList.remove('open');
    lb.setAttribute('aria-hidden','true');
    resetZoom();
    unlockScroll();
    if(lastFocus&&lastFocus.focus)lastFocus.focus();
  }
  shots.forEach(function(s){
    var b=s.querySelector('button');
    if(b)b.addEventListener('click',function(){open(s)});
  });
  var cl=lb.querySelector('.close'),pv=lb.querySelector('.prev'),nx=lb.querySelector('.next');
  if(cl)cl.addEventListener('click',function(e){e.stopPropagation();close()});
  if(pv)pv.addEventListener('click',function(e){e.stopPropagation();show(idx-1)});
  if(nx)nx.addEventListener('click',function(e){e.stopPropagation();show(idx+1)});
  lb.addEventListener('click',function(e){
    if(e.target===lb||e.target.classList.contains('lb-meta'))close();
  });
  document.addEventListener('keydown',function(e){
    if(!lb.classList.contains('open'))return;
    if(e.key==='Escape'){e.preventDefault();close()}
    else if(e.key==='ArrowRight'){e.preventDefault();show(idx+1)}
    else if(e.key==='ArrowLeft'){e.preventDefault();show(idx-1)}
    else if(e.key==='Home'){e.preventDefault();show(0)}
    else if(e.key==='End'){e.preventDefault();show(visible().length-1)}
    else if(e.key==='Tab'){
      var f=[].slice.call(lb.querySelectorAll('button, a[href]')).filter(function(el){return el.offsetParent!==null});
      if(!f.length)return;
      var i=f.indexOf(document.activeElement);e.preventDefault();
      f[(i+(e.shiftKey?-1:1)+f.length)%f.length].focus();
    }
  });
  function distOf(touches){
    var a=touches[0],b=touches[1];
    return Math.hypot(a.clientX-b.clientX,a.clientY-b.clientY);
  }
  lb.addEventListener('touchstart',function(e){
    if(e.touches.length>=2){
      pinching=true;pinchOccurred=true;swiping=false;
      startDist=distOf(e.touches);startScale=scale;
    }else if(e.touches.length===1){
      var t=e.touches[0];sx=lastX=t.clientX;sy=lastY=t.clientY;swiping=true;
    }
  },{passive:true});
  lb.addEventListener('touchmove',function(e){
    if(pinching&&e.touches.length>=2&&startDist>0){
      scale=Math.min(5,Math.max(1,startScale*distOf(e.touches)/startDist));
      if(scale<=1.001){scale=1;tx=0;ty=0}
      applyZoom();
    }else if(scale>1.02&&e.touches.length===1){
      var t=e.touches[0];
      tx+=t.clientX-lastX;ty+=t.clientY-lastY;
      lastX=t.clientX;lastY=t.clientY;
      applyZoom();
      swiping=false;
    }
  },{passive:true});
  lb.addEventListener('touchend',function(e){
    if(pinching){
      if(e.touches.length<2)pinching=false;
      if(scale<1.05)resetZoom();
      if(e.touches.length===0)pinchOccurred=false;
      return;
    }
    if(pinchOccurred){if(e.touches.length===0)pinchOccurred=false;return}
    if(!swiping||!e.changedTouches.length||scale>1.05){swiping=false;return}
    var t=e.changedTouches[0],dx=t.clientX-sx,dy=t.clientY-sy;
    swiping=false;
    if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)*1.3)show(idx+(dx<0?1:-1));
    else if(dy>90&&Math.abs(dy)>Math.abs(dx)*1.5)close();
  },{passive:true});
})();
