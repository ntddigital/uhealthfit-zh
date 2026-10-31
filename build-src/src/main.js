/* 優健堂 UHealthFit × WiseQuest — 全站互動 */
(function(){
  // 手機選單
  var mb=document.querySelector('.menu-btn'), mm=document.querySelector('.mobile-menu');
  if(mb&&mm){mb.addEventListener('click',function(){var o=mm.classList.toggle('open');mb.setAttribute('aria-expanded',o?'true':'false');});}

  // 外站購買連結：沿用廣告來源參數、記錄事件（GA4 / Meta Pixel 若存在）
  // 訪客若從廣告或帶 UTM 的連結進站，把來源參數與點擊編號存在本次瀏覽，
  // 前往商店時原樣帶過去，讓 Shopify、GA4、Meta、Google Ads 能把訂單歸回原本的廣告。
  // 沒有廣告來源時不加任何參數：us. 與 zh. 共用同一個 GA4 資源與 _ga cookie，
  // 自製 utm_source 反而會把 Google 自然搜尋、YouTube 等原始來源蓋掉。
  var page=document.body.getAttribute('data-page')||'site';
  var AD_KEYS=['utm_source','utm_medium','utm_campaign','utm_content','utm_term','utm_id','fbclid','gclid','gbraid','wbraid','msclkid','ttclid'];
  var adParams={};
  try{
    var q=new URLSearchParams(location.search), fresh={}, hasFresh=false;
    AD_KEYS.forEach(function(k){var v=q.get(k); if(v){fresh[k]=v; hasFresh=true;}});
    if(hasFresh){ sessionStorage.setItem('uhf_ad_params',JSON.stringify(fresh)); adParams=fresh; }
    else { adParams=JSON.parse(sessionStorage.getItem('uhf_ad_params')||'{}')||{}; }
  }catch(e){ adParams={}; }
  function shopHref(href){
    var u=new URL(href), keys=Object.keys(adParams);
    if(keys.length){
      AD_KEYS.forEach(function(k){u.searchParams.delete(k);});
      keys.forEach(function(k){u.searchParams.set(k,adParams[k]);});
    }
    return u.toString();
  }
  document.querySelectorAll('a[href^="https://zh.uhealthfit.com"]').forEach(function(a){
    try{
      a.href=shopHref(a.href);
      a.setAttribute('rel','noopener'); a.setAttribute('target','_blank'); // 另開新分頁，保留本站
      a.addEventListener('click',function(){
        var label=a.getAttribute('data-product')||page;
        if(window.gtag){gtag('event','begin_checkout_redirect',{product:label,page:page});}
        // Meta 只收到「前往商店」這個動作，不帶產品或頁面名稱，避免被視為健康相關資料
        if(window.fbq){fbq('trackCustom','ShopRedirect');}
      });
    }catch(e){}
  });

  // 產品頁固定購買列：主購買按鈕沒有完整出現在畫面上時顯示（手機首屏只露出一半也算）
  var bar=document.querySelector('.buybar'), mainBtn=document.querySelector('.buybox .btn-primary');
  if(bar&&mainBtn){
    document.body.classList.add('has-buybar');
    var checkBar=function(){
      var r=mainBtn.getBoundingClientRect(), vh=window.innerHeight||document.documentElement.clientHeight;
      var seen=Math.max(0,Math.min(r.bottom,vh)-Math.max(r.top,0))/(r.height||1);
      bar.classList.toggle('show',seen<0.9);
    };
    window.addEventListener('scroll',checkBar,{passive:true});
    window.addEventListener('resize',checkBar);
    window.addEventListener('load',checkBar);
    checkBar();
  }

  // 部落格篩選
  var chips=document.querySelectorAll('.chip[data-f]');
  if(chips.length){
    chips.forEach(function(c){c.addEventListener('click',function(){
      chips.forEach(function(x){x.classList.remove('on');});c.classList.add('on');
      var f=c.getAttribute('data-f');
      document.querySelectorAll('.post-card[data-series]').forEach(function(p){p.style.display=(f==='all'||p.getAttribute('data-series')===f)?'':'none';});
    });});
  }

  // 測驗
  var quiz=document.getElementById('quiz');
  if(quiz){
    var steps=[].slice.call(quiz.querySelectorAll('.qstep')), i=0, score={eye:0,dental:0,sleep:0,digestive:0,skin:0,vitality:0}, answers=[];
    var prog=quiz.querySelector('.qprog i'), result=quiz.querySelector('.qresult'), back=quiz.querySelector('.qback');
    function show(n){steps.forEach(function(s,k){s.classList.toggle('on',k===n);});prog.style.width=((n)/steps.length*100)+'%';if(back)back.style.visibility=n>0?'visible':'hidden';}
    quiz.querySelectorAll('.qopts button').forEach(function(b){b.addEventListener('click',function(){
      var w=JSON.parse(b.getAttribute('data-w')||'{}');answers[i]=w;
      i++; if(i<steps.length){show(i);} else {finish();}
    });});
    if(back){back.addEventListener('click',function(){if(i>0){i--;answers.length=i;show(i);}});}
    function finish(){
      Object.keys(score).forEach(function(k){score[k]=0;});
      answers.forEach(function(w){Object.keys(w).forEach(function(k){score[k]+=w[k];});});
      var ranked=Object.keys(score).sort(function(a,b){return score[b]-score[a];});
      var top=ranked[0], second=ranked[1];
      steps.forEach(function(s){s.classList.remove('on');});prog.style.width='100%';
      result.querySelectorAll('[data-r]').forEach(function(el){el.style.display=el.getAttribute('data-r')===top?'':'none';});
      result.querySelectorAll('[data-r2]').forEach(function(el){el.style.display=el.getAttribute('data-r2')===second?'':'none';});
      var hid=result.querySelector('input[name="quiz_result"]'); if(hid){hid.value=top+'|'+second;}
      var eb=(top==='eye')?'eye-care':'body-balance';
      result.querySelectorAll('[data-eb]').forEach(function(el){el.style.display=el.getAttribute('data-eb')===eb?'':'none';});
      var lm=result.querySelector('input[name="lead_magnet"]'); if(lm){lm.value=eb;}
      result.classList.add('on'); if(back)back.style.visibility='hidden';
      result.scrollIntoView({behavior:'smooth',block:'start'});
      if(window.gtag){gtag('event','quiz_complete',{result:top});}
    }
    show(0);
  }

  // Klaviyo 名單訂閱（client API，公開金鑰）：測驗電子書、免費下載頁、文章內區塊、小視窗共用
  var LM_KEY='uhf_lm_done';
  function lmDone(){try{return JSON.parse(localStorage.getItem(LM_KEY)||'{}')||{};}catch(e){return {};}}
  function markLm(k){try{var d=lmDone();d[k]=1;localStorage.setItem(LM_KEY,JSON.stringify(d));}catch(e){}}
  var kforms=[].slice.call(document.querySelectorAll('form[data-klaviyo-list]'));
  kforms.forEach(function(form){
    form.addEventListener('submit',function(ev){
      ev.preventDefault();
      var input=form.querySelector('input[type=email]'), email=input.value.trim();
      if(!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)){ toast('請輸入正確的 Email'); input.focus(); return; }
      var company=form.getAttribute('data-klaviyo-company'), list=form.getAttribute('data-klaviyo-list');
      var lmPage=form.getAttribute('data-lm'), place=form.getAttribute('data-lm-place')||'';
      var props={source:'uhealthfit-site/'+page}, lmKey='', ebook=null;
      if(lmPage){ // 免費下載品（7 天護眼、節氣月曆）：各自的 List 觸發各自的 Flow
        lmKey=lmPage; props.lead_magnet=lmKey; props.lead_magnet_place=place;
      } else { // 測驗電子書
        var r=form.querySelector('input[name="quiz_result"]'); if(r&&r.value){props.quiz_result=r.value;}
        var lmIn=form.querySelector('input[name="lead_magnet"]'), ebooks={}; lmKey=lmIn?lmIn.value:'';
        try{ebooks=JSON.parse(form.getAttribute('data-ebooks')||'{}');}catch(e){}
        ebook=ebooks[lmKey]||null; if(ebook){props.lead_magnet=lmKey;}else{lmKey='';}
      }
      var body={data:{type:'subscription',attributes:{custom_source:'uhealthfit-site '+page+(place?' '+place:''),profile:{data:{type:'profile',attributes:{email:email,properties:props}}}},relationships:{list:{data:{type:'list',id:list}}}}};
      var btn=form.querySelector('button'); btn.disabled=true;
      fetch('https://a.klaviyo.com/client/subscriptions/?company_id='+encodeURIComponent(company),{method:'POST',headers:{'Content-Type':'application/json','revision':'2024-10-15'},body:JSON.stringify(body)})
      .then(function(res){ if(res.status===202||res.ok){done();} else {throw new Error('status '+res.status);} })
      .catch(function(){ btn.disabled=false; toast('暫時無法送出，請稍後再試，或來信 service@uhealthfit.com'); });
      function done(){
        // 同一頁上同一個下載品的表單（頁首、頁尾、小視窗）一起換成「已收到」
        var same=lmPage?kforms.filter(function(f){return f.getAttribute('data-lm')===lmPage;}):[form];
        same.forEach(function(f){
          f.style.display='none'; var ok=f.parentNode.querySelector('.email-ok');
          if(ok){ok.style.display='block';var dl=ok.querySelector('.ebook-dl');if(dl){if(ebook){dl.href=ebook.url;}else if(!lmPage){dl.style.display='none';}}}
        });
        if(lmPage){ markLm(lmPage); document.body.classList.add('lm-submitted'); }
        if(ebook){ // 觸發 Klaviyo「Requested Quiz Ebook」事件，由 Flow 寄出對應的電子書
          var ev={data:{type:'event',attributes:{properties:{ebook:lmKey,ebook_title:ebook.title,ebook_url:ebook.url,quiz_result:props.quiz_result||''},metric:{data:{type:'metric',attributes:{name:'Requested Quiz Ebook'}}},profile:{data:{type:'profile',attributes:{email:email,properties:props}}}}}};
          fetch('https://a.klaviyo.com/client/events/?company_id='+encodeURIComponent(company),{method:'POST',headers:{'Content-Type':'application/json','revision':'2024-10-15'},body:JSON.stringify(ev)}).catch(function(){});
        }
        if(window.gtag){gtag('event','generate_lead',{method:lmPage?('lead_magnet_'+(place||'page')):'quiz_email',lead_magnet:lmKey||'none'});}
        if(window.fbq){fbq('track','Lead');} // 不傳下載品類別給 Meta，類別只留在 GA4 與 Klaviyo
      }
    });
  });

  // 免費下載頁：手機上表單不在畫面內時，底部出現「免費下載」按鈕，點了捲回表單
  var lps=document.querySelector('.lp-sticky');
  if(lps){
    var lpForms=[].slice.call(document.querySelectorAll('.lp .lm-form'));
    var chkLp=function(){
      var vh=window.innerHeight||document.documentElement.clientHeight;
      var vis=lpForms.some(function(f){var r=f.getBoundingClientRect();return f.style.display!=='none'&&r.bottom>0&&r.top<vh;});
      lps.classList.toggle('show',!vis&&!document.body.classList.contains('lm-submitted')&&window.scrollY>240);
    };
    window.addEventListener('scroll',chkLp,{passive:true}); window.addEventListener('resize',chkLp); chkLp();
    lps.addEventListener('click',function(e){
      e.preventDefault(); var f=lpForms[0]; if(!f) return;
      f.scrollIntoView({behavior:'smooth',block:'center'});
      setTimeout(function(){var i=f.querySelector('input');if(i){i.focus({preventScroll:true});}},600);
    });
  }

  // 免費下載小視窗：每次瀏覽最多一次；捲到 55% 或停留 30 秒才出現；測驗頁、下載頁、已領過的人不出現
  var pops=[].slice.call(document.querySelectorAll('.lm-pop'));
  if(pops.length&&page!=='quiz'&&!document.querySelector('main.lp')){
    var inl=document.querySelector('.lm-inline[data-lm-key]');
    var popKey=inl?inl.getAttribute('data-lm-key'):'solar-calendar-2027';
    var pop=pops.filter(function(p){return p.getAttribute('data-lm-key')===popKey;})[0];
    var seen=false; try{seen=!!sessionStorage.getItem('uhf_pop_seen');}catch(e){}
    if(pop&&!seen&&!lmDone()[popKey]){
      var opened=false, tm;
      var openPop=function(){
        if(opened||document.body.classList.contains('lm-submitted')) return; opened=true; clearTimeout(tm);
        try{sessionStorage.setItem('uhf_pop_seen','1');}catch(e){}
        pop.hidden=false; requestAnimationFrame(function(){pop.classList.add('show');});
        if(window.gtag){gtag('event','lead_magnet_popup_view',{lead_magnet:popKey});}
      };
      var closePop=function(){pop.classList.remove('show');setTimeout(function(){pop.hidden=true;},250);};
      pop.querySelector('.lm-pop-x').addEventListener('click',closePop);
      document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!pop.hidden){closePop();}});
      tm=setTimeout(openPop,30000);
      var onPopScroll=function(){var h=document.documentElement;if((window.scrollY+window.innerHeight)/h.scrollHeight>0.55){openPop();window.removeEventListener('scroll',onPopScroll);}};
      window.addEventListener('scroll',onPopScroll,{passive:true});
    }
  }
  // 系列頁頁首輪播：箭頭、圓點、滑動、約 6 秒自動切換（滑鼠移入或觸控時暫停）
  document.querySelectorAll('.slides').forEach(function(box){
    var track=box.querySelector('.slides-track'), dots=[].slice.call(box.querySelectorAll('.slides-dots button')), n=track.children.length;
    if(n<2) return;
    var idx=0, t, timer, paused=false;
    var still=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    function preload(i){[].forEach.call(track.children[i].querySelectorAll('img[loading=lazy]'),function(img){img.loading='eager';});}
    function mark(){dots.forEach(function(d,i){if(i===idx){d.setAttribute('aria-current','true');}else{d.removeAttribute('aria-current');}});}
    function go(i){idx=(i+n)%n; preload(idx); preload((idx+1)%n); mark(); track.scrollTo({left:idx*track.clientWidth});}
    function play(){clearInterval(timer); if(!still){timer=setInterval(function(){if(!paused&&!document.hidden){go(idx+1);}},6000);}}
    box.querySelector('.slides-prev').addEventListener('click',function(){go(idx-1);play();});
    box.querySelector('.slides-next').addEventListener('click',function(){go(idx+1);play();});
    dots.forEach(function(d,i){d.addEventListener('click',function(){go(i);play();});});
    box.addEventListener('mouseenter',function(){paused=true;});
    box.addEventListener('mouseleave',function(){paused=false;});
    box.addEventListener('focusin',function(){paused=true;});
    box.addEventListener('focusout',function(){paused=false;});
    track.addEventListener('touchstart',function(){paused=true;},{passive:true});
    track.addEventListener('touchend',function(){setTimeout(function(){paused=false;},4000);},{passive:true});
    track.addEventListener('scroll',function(){clearTimeout(t);t=setTimeout(function(){idx=Math.round(track.scrollLeft/track.clientWidth);mark();},150);});
    window.addEventListener('resize',function(){track.scrollTo({left:idx*track.clientWidth,behavior:'auto'});});
    window.addEventListener('load',function(){preload(1);});
    play();
  });

  function toast(msg){var t=document.querySelector('.toast');if(!t){t=document.createElement('div');t.className='toast';document.body.appendChild(t);}t.textContent=msg;t.classList.add('show');setTimeout(function(){t.classList.remove('show');},3200);}
})();
