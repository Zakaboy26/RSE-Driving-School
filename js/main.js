(function(){
const $=(s,r=document)=>r.querySelector(s),$$=(s,r=document)=>[...r.querySelectorAll(s)];
const shuffle=a=>{a=[...a];for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]]}return a};

// Mobile nav
const mb=$('.menu-btn'),ul=$('#nav-list');
if(mb)mb.addEventListener('click',()=>{const o=ul.classList.toggle('open');mb.setAttribute('aria-expanded',o)});

// Lightbox
const lb=$('#lb');
if(lb){const btns=$$('[data-lb]');let i=0;const img=$('img',lb),cap=$('#lb-cap');
const show=n=>{i=(n+btns.length)%btns.length;img.src=btns[i].dataset.lb;img.alt=btns[i].dataset.alt;cap.textContent=(i+1)+' of '+btns.length};
btns.forEach((b,n)=>b.addEventListener('click',()=>{show(n);lb.showModal()}));
$('#lb-prev').onclick=()=>show(i-1);$('#lb-next').onclick=()=>show(i+1);$('#lb-close').onclick=()=>lb.close();
lb.addEventListener('keydown',e=>{if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1)});
lb.addEventListener('click',e=>{if(e.target===lb)lb.close()})}

// Learning Centre search
const sf=$('#lc-search');
if(sf&&window.SEARCH_INDEX){const out=$('#results'),st=$('#result-status');
const run=()=>{const q=sf.value.trim().toLowerCase();out.innerHTML='';if(q.length<2){st.textContent='';return}
const hits=SEARCH_INDEX.filter(e=>(e.t+' '+e.k).toLowerCase().includes(q)).slice(0,25);
st.textContent=hits.length?hits.length+' result'+(hits.length>1?'s':'')+' found':'No results. Try a different word, or browse the categories below.';
hits.forEach(h=>{const li=document.createElement('li'),a=document.createElement('a');a.href=SITE_BASE+h.u;a.textContent=h.t;li.append(a,' ');const s=document.createElement('span');s.className='tag';s.textContent=h.c;li.append(s);out.append(li)})};
sf.addEventListener('input',run);$('#lc-form').addEventListener('submit',e=>{e.preventDefault();run()})}

// Dictionary filter
const df=$('#dict-filter');
if(df)df.addEventListener('input',()=>{const q=df.value.toLowerCase();let n=0;$$('#dict dt').forEach(dt=>{const dd=dt.nextElementSibling,m=(dt.textContent+dd.textContent).toLowerCase().includes(q);dt.hidden=dd.hidden=!m;if(m)n++});$('#dict-count').textContent=n+' term'+(n===1?'':'s')+' shown'});

// Flashcards
const fc=$('#fc');
if(fc){const all=$$('.qa').map(e=>({type:e.dataset.type,q:e.dataset.q,a:e.dataset.a,n:e.dataset.n}));
let deck=[],k=0,known=0;const q=$('#fc-q'),a=$('#fc-a'),rv=$('#fc-reveal'),st=$('#fc-stat'),row=$('#fc-rate');
const build=()=>{const t=$('#fc-type').value;deck=shuffle(all.filter(x=>t==='all'||x.type===t));k=0;known=0;draw()};
const draw=()=>{if(k>=deck.length){q.textContent='Round complete';a.hidden=true;rv.hidden=true;row.hidden=true;st.textContent='You marked '+known+' of '+deck.length+' as known. Shuffle to go again.';return}
const c=deck[k];q.textContent=c.q;a.textContent=c.a;a.hidden=true;rv.hidden=false;row.hidden=true;st.textContent='Card '+(k+1)+' of '+deck.length+' ('+c.type+' me)'};
rv.onclick=()=>{a.hidden=false;rv.hidden=true;row.hidden=false;$('#fc-known').focus()};
$('#fc-known').onclick=()=>{known++;k++;draw()};$('#fc-again').onclick=()=>{k++;draw()};
$('#fc-type').onchange=build;$('#fc-shuffle').onclick=build;build()}

// Quiz
const qz=$('#quiz');
if(qz&&window.QUIZ){let qs,i,score;const box=$('#quiz-box');
const start=()=>{qs=shuffle(QUIZ).map(x=>{const idx=shuffle(x.o.map((t,n)=>n));return{q:x.q,e:x.e,o:idx.map(n=>x.o[n]),c:idx.indexOf(0)}});i=0;score=0;ask()};
const ask=()=>{if(i>=qs.length){box.innerHTML='<h3>Your score: '+score+' / '+qs.length+'</h3><p>This quiz is unofficial and uses original practice questions. The real theory test needs a minimum of 43 out of 50 to pass.</p>';const b=document.createElement('button');b.className='btn';b.textContent='Try again';b.onclick=start;box.append(b);b.focus();return}
const c=qs[i];box.innerHTML='';const h=document.createElement('h3');h.textContent='Question '+(i+1)+' of '+qs.length;h.tabIndex=-1;const p=document.createElement('p');p.textContent=c.q;box.append(h,p);
const fb=document.createElement('div');fb.setAttribute('aria-live','polite');
c.o.forEach((t,n)=>{const b=document.createElement('button');b.className='opt';b.textContent=t;b.onclick=()=>{$$('.opt',box).forEach((o,m)=>{o.disabled=true;if(m===c.c)o.classList.add('good')});const ok=n===c.c;if(ok)score++;else b.classList.add('bad');fb.className='fb';fb.textContent=(ok?'Correct. ':'Not quite. ')+c.e;const nx=document.createElement('button');nx.className='btn sm';nx.textContent=i+1<qs.length?'Next question':'See my score';nx.onclick=()=>{i++;ask()};box.append(nx);nx.focus()};box.append(b)});box.append(fb);h.focus()};
start()}

// Back to top
const t=$('#top');if(t)window.addEventListener('scroll',()=>{t.hidden=scrollY<700});
})();
