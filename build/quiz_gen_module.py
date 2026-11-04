# -*- coding: utf-8 -*-
"""Сборка quiz.html — тест «Какая религия вам ближе» (движок AutoCoder + UI Веротеки).

Вызывается из build.py: import quiz; quiz.build_quiz(SITE)
Данные: build/quiz-data.json (банк 262 традиций с link/axis/family/year/tags/description).
"""
import json, os
from pathlib import Path

BUILD = Path(os.environ.get("QUIZ_BUILD_DIR", Path(__file__).parent))

QUESTIONS_JS = r"""
var QUESTIONS = [
 {id:'axis_split', text:'Как тебе ближе взглянуть на устройство мира?',
  opts:[
   {t:'Мир управляется личным Творцом, отличным от мира', e:{a:{dvaita:2.4}}},
   {t:'Бог и мир в глубине одно; различия — лишь видимость', e:{a:{advaita:2.4}}},
   {t:'«Бог» — лишнее слово: есть пустота и поток причин', e:{a:{sunyata:2.4}}},
   {t:'Не хочу решать философию — мне ближе уклад и традиция', e:{t:{'региональные':1.8,'древние':0.9}}}
  ]},
 {id:'revelation', text:'Главный источник религиозной истины?',
  opts:[
   {t:'Откровение Бога в священном писании', e:{t:{'авраамические':2.0,'монотеизм':1.0},a:{dvaita:0.8}}},
   {t:'Вечный закон мироустройства (дхарма, дао)', e:{t:{'индуизм':1.2,'буддизм':1.0,'дхармические':1.0}}},
   {t:'Мудрость древних народов, живущая в обрядах', e:{t:{'древние':2.0,'Европа':0.8},f:{'Древние':0.6}}},
   {t:'Личный опыт и практика важнее писаний', e:{t:{'эзотерика':1.2,'недуальность':0.8},a:{advaita:0.5}}}
  ]},
 {id:'practice', text:'Какая практика отзывается больше?',
  opts:[
   {t:'Молитва и богослужение', e:{t:{'христианство':1.2,'ислам':1.2},a:{dvaita:0.6}}},
   {t:'Медитация и созерцание', e:{t:{'буддизм':1.2,'дзен':0.9,'йога':0.9},a:{advaita:0.5,sunyata:0.5}}},
   {t:'Ритуалы и праздники народного года', e:{t:{'региональные':2.0,'возрождённые':0.8}}},
   {t:'Йога, телесные и энергетические практики', e:{t:{'йога':1.6,'тантра':1.2,'индуизм':0.6}}}
  ]},
 {id:'rules', text:'Строгие правила и заповеди — это…',
  opts:[
   {t:'Опора: я следую традиции как она есть', e:{t:{'монотеизм':1.0,'право':1.5},a:{dvaita:0.6}}},
   {t:'Инструмент, но истина — за пределами правил', e:{t:{'философия':1.2},a:{advaita:0.8}}},
   {t:'Внешних правил мало — важен внутренний путь', e:{t:{'эзотерика':1.6,'мистицизм':1.0}}},
   {t:'Уклад общины важнее догм', e:{t:{'старообрядчество':1.4,'региональные':0.8}}}
  ]},
 {id:'mystic', text:'Мистический опыт — это…',
  opts:[
   {t:'Встреча с живым Богом', e:{t:{'суфизм':1.6,'мистицизм':0.8},a:{dvaita:0.8}}},
   {t:'Растворение в Едином', e:{t:{'тантра':0.8,'шиваизм':0.8},a:{advaita:1.2}}},
   {t:'Пробуждение: увидеть реальность как она есть', e:{t:{'дзен':1.6,'махаяна':1.0},a:{sunyata:1.0}}},
   {t:'Не про меня, интереснее история и культура', e:{t:{'древние':1.4,'история':0.8}}}
  ]},
 {id:'era', text:'Тебе ближе традиции…',
  opts:[
   {t:'Древние, восходящие к самым истокам', e:{e:{ancient:2.2},t:{'греко-римский мир':1.6,'Америки':1.4,'Европа':0.9}}},
   {t:'Средневековая классика: соборы, монастыри, суфии', e:{e:{medieval:2.2},t:{'суфизм':0.8}}},
   {t:'Нового времени: реформации и пробуждения', e:{e:{earlymodern:1.8,xix:1.2},t:{'протестантизм':1.4}}},
   {t:'XX–XXI века: новые учения и движения', e:{e:{xx:1.5,xxi:2.0},t:{'НРД':2.0}}}
  ]},
 {id:'scripture', text:'Как читать священные тексты?',
  opts:[
   {t:'Буквально: это история реальных событий', e:{t:{'монотеизм':0.8},a:{dvaita:0.8}}},
   {t:'Как метафоры, за которыми скрыт глубинный смысл', e:{t:{'эзотерика':1.0,'кашмирский шиваизм':0.8,'недуальный тантрический шиваизм':0.8},a:{advaita:0.6}}},
   {t:'Как указатели на путь, а не догмы', e:{t:{'дзен':1.0,'философия':0.8},a:{sunyata:0.8}}},
   {t:'Как культурный памятник эпохи', e:{t:{'древние':1.2,'история':1.0}}}
  ]},
 {id:'mode', text:'Как удобнее практиковать?',
  opts:[
   {t:'В общине, вместе с людьми', e:{t:{'христианство':1.0,'протестантизм':0.8,'региональные':0.8}}},
   {t:'Наедине с собой', e:{t:{'эзотерика':0.9,'недуальность':0.6},a:{advaita:0.5}}},
   {t:'В монастыре или ашраме, по уставу', e:{t:{'буддизм':1.2,'индуизм':0.8},e:{medieval:0.5}}},
   {t:'Свободно, без институтов', e:{t:{'НРД':1.6,'пародия':0.5,'Россия':0.8},a:{sunyata:0.4}}}
  ]},
 {id:'god', text:'Понятие «личный Бог» тебе…',
  opts:[
   {t:'Отзывается: есть Тот, к Кому обращаются в молитве', e:{t:{'монотеизм':1.5},a:{dvaita:1.2}}},
   {t:'Тесно: Абсолют шире любой личности', e:{t:{'философия':0.8,'индуизм':0.6},a:{advaita:1.4}}},
   {t:'Лишнее: есть путь, ум и прозрение', e:{t:{'буддизм':1.4,'дзен':0.8},a:{sunyata:1.2}}},
   {t:'Второстепенно: важнее, как жить', e:{t:{'региональные':1.2,'древние':0.6}}}
  ]},
 {id:'after', text:'Что после смерти?',
  opts:[
   {t:'Суд, рай и ад', e:{t:{'монотеизм':1.2,'христианство':0.8,'ислам':0.8},a:{dvaita:0.8}}},
   {t:'Перерождения до освобождения', e:{t:{'индуизм':1.4,'буддизм':1.2,'джайнизм':0.8}}},
   {t:'Возвращение к единому началу мира', e:{t:{'тантра':0.6},a:{advaita:1.0}}},
   {t:'Неизвестно — живём сейчас', e:{t:{'НРД':0.8,'пародия':0.6},a:{sunyata:0.5}}}
  ]},
 {id:'humor', text:'Парадоксы и смех в духовной жизни — это…',
  opts:[
   {t:'Часть пути: истина играет и улыбается', e:{t:{'кашмирский шиваизм':1.8,'Каширский шиваизм':1.6,'недуальный тантрический шиваизм':1.4,'дзен':1.2},a:{advaita:0.5}}},
   {t:'Дело серьёзное, спасение требует строгости', e:{t:{'монотеизм':0.8,'право':0.8},a:{dvaita:0.6}}},
   {t:'Знак, что ум зашёл в тупик; нужен прямой взгляд', e:{t:{'дзен':1.4},a:{sunyata:0.7}}},
   {t:'Мне важнее красота обряда и храма', e:{t:{'региональные':1.0,'возрождённые':0.8}}}
  ]},
 {id:'nature', text:'Мир и природа — это…',
  opts:[
   {t:'Творение, доверенное человеку', e:{t:{'монотеизм':1.0},a:{dvaita:1.0}}},
   {t:'Проявление божественного', e:{t:{'индуизм':1.2,'тантра':0.6},a:{advaita:0.9}}},
   {t:'Поток взаимозависимых событий без хозяина', e:{t:{'буддизм':1.0},a:{sunyata:1.0}}},
   {t:'Дом предков: жить с ним в ладу', e:{t:{'региональные':1.8,'древние':1.0,'Африка':0.6,'Китай':0.6}}}
  ]},
 {id:'church', text:'Старые церкви и институты — это…',
  opts:[
   {t:'Дом и опора: предание веков', e:{t:{'христианство':1.0,'право':0.6},e:{medieval:0.6}}},
   {t:'Нужна реформа: вернуться к первоисточнику', e:{t:{'протестантизм':1.8},e:{earlymodern:0.8}}},
   {t:'Институты не обязательны для веры', e:{t:{'НРД':1.2,'эзотерика':0.8}}},
   {t:'Древние дохристианские пути ближе', e:{t:{'древние':2.0,'возрождённые':1.0}}}
  ]},
 {id:'ethics', text:'Основа морали?',
  opts:[
   {t:'Воля Божья и заповеди', e:{t:{'монотеизм':1.2,'авраамические':1.0},a:{dvaita:0.8}}},
   {t:'Закон причины и следствия (карма)', e:{t:{'индуизм':1.2,'джайнизм':0.8,'буддизм':0.8}}},
   {t:'Сострадание ко всем живым существам', e:{t:{'махаяна':1.4,'буддизм':1.0},a:{sunyata:0.7}}},
   {t:'Свобода и ответственность личности', e:{t:{'НРД':1.0,'США':0.8},a:{advaita:0.5}}}
  ]},
 {id:'flavor', text:'Если выбирать направление внутри индуизма/дхармы, тебе ближе…',
  opts:[
   {t:'Бхакти: любовь и преданность Богу', e:{t:{'бхакти':3.0,'вишнуизм':2.2}}},
   {t:'Тантра: энергия, ритуал, работа с телом', e:{t:{'тантра':3.0,'шактизм':2.2}}},
   {t:'Джняна: знание и недвойственность', e:{t:{'философия':1.5,'кашмирский шиваизм':1.8,'недуальность':1.6,'Каширский шиваизм':1.0},a:{advaita:0.8}}},
   {t:'Шива как центр всего', e:{t:{'шиваизм':2.6,'кашмирский шиваизм':1.2}}}
  ]},
 {id:'abraham_flavor', text:'Если выбрать авраамическую семью, что ближе?',
  opts:[
   {t:'Христианство во всех его формах', e:{t:{'христианство':2.6}}},
   {t:'Ислам: единобожие и предание', e:{t:{'ислам':2.6,'суннизм':1.0}}},
   {t:'Иудаизм и его традиция', e:{t:{'иудаизм':2.8}}},
   {t:'Радикальные и рыцарские ордена (тамплиеры, ассасины…)', e:{t:{'спорный статус':2.0,'тарикаты':1.5}}}
  ]}
];
""".strip()

ENGINE_JS = r"""
var AXES=['dvaita','advaita','sunyata'];
function mulberry32(seed){var a=seed>>>0;return function(){a|=0;a=(a+0x6D2B79F5)|0;var t=Math.imul(a^(a>>>15),1|a);t=(t+Math.imul(t^(t>>>7),61|t))^t;return((t^(t>>>14))>>>0)/4294967296;};}
function romanToInt(s){var map={I:1,V:5,X:10,L:50,C:100,D:500,M:1000};var r=0;s=s.toUpperCase();for(var i=0;i<s.length;i++){var c=map[s.charAt(i)];var n=map[s.charAt(i+1)];if(!c)continue;r+=(n&&n>c)?-c:c;}return r;}
function parseEras(year){var out=[];function push(e){if(e&&out.indexOf(e)===-1)out.push(e);}if(!year)return out;var s=String(year);if(/до\s*н\.?\s*э/i.test(s))push('ancient');var romanRe=/\b([IVXLC]+)\s*(?:в\.|век|тыс)/gi;var m;while((m=romanRe.exec(s))){var c=romanToInt(m[1]);if(c<=5)push('ancient');else if(c<=15)push('medieval');else if(c<=18)push('earlymodern');else if(c===19)push('xix');else if(c===20)push('xx');else push('xxi');}var yrRe=/\b(\d{1,4})\b/g;while((m=yrRe.exec(s))){var y=parseInt(m[1],10);if(y<=500)push('ancient');else if(y<=1450)push('medieval');else if(y<=1800)push('earlymodern');else if(y<=1900)push('xix');else if(y<=2000)push('xx');else push('xxi');}return out;}
function createGame(seed){return{seed:(seed>>>0)||1,answers:[]};}
function jitters(state,n){var r=mulberry32(state.seed^0x9E3779B9);var out=new Array(n);for(var i=0;i<n;i++)out[i]=r()*0.06;return out;}
function zeroPts(){return{axis:{dvaita:0,advaita:0,sunyata:0},family:{},tag:{},era:{ancient:0,medieval:0,earlymodern:0,xix:0,xx:0,xxi:0}};}
function addEffect(pts,e){if(!e)return;var k,v;for(k in e.a||{}){v=e.a[k];if(v>2)v=2;pts.axis[k]=(pts.axis[k]||0)+v;}for(k in e.f||{}){v=e.f[k];if(v>2)v=2;pts.family[k]=(pts.family[k]||0)+v;}for(k in e.t||{}){v=e.t[k];if(v>2)v=2;pts.tag[k]=(pts.tag[k]||0)+v;}for(k in e.e||{}){v=e.e[k];if(v>2)v=2;pts.era[k]=(pts.era[k]||0)+v;}}
function clonePts(p){return{axis:{dvaita:p.axis.dvaita,advaita:p.axis.advaita,sunyata:p.axis.sunyata},family:JSON.parse(JSON.stringify(p.family)),tag:JSON.parse(JSON.stringify(p.tag)),era:JSON.parse(JSON.stringify(p.era))};}
function qIndex(QS){var m={};for(var i=0;i<QS.length;i++)m[QS[i].id]=QS[i];return m;}
var SCALE=2.2;function scaleEff(e){if(!e)return null;var o={a:{},f:{},t:{},e:{}};var k;for(k in e.a||{})o.a[k]=e.a[k]*SCALE;for(k in e.f||{})o.f[k]=e.f[k]*SCALE;for(k in e.t||{})o.t[k]=e.t[k]*SCALE;for(k in e.e||{})o.e[k]=e.e[k]*SCALE;return o;}
function pointsFor(state,QS){var pts=zeroPts();var idx=qIndex(QS);for(var i=0;i<state.answers.length;i++){var a=state.answers[i];var q=idx[a.q];if(!q||!q.opts[a.o])continue;addEffect(pts,scaleEff(q.opts[a.o].e));}return pts;}
function scoreItem(item,pts,jit){var s=0.6;var pa=pts.axis||{};if(item.axis){var own=pa[item.axis]||0;var other=Math.max(pa.dvaita||0,pa.advaita||0,pa.sunyata||0);s+=1.45*own-0.85*Math.max(0,other-own);}else{var avg=((pa.dvaita||0)+(pa.advaita||0)+(pa.sunyata||0))/3;s+=0.5*avg;}s+=1.05*(pts.family[item.family]||0);var tsum=0;var tags=item.tags||[];for(var i=0;i<tags.length;i++)tsum+=(pts.tag[tags[i]]||0);s+=1.6*Math.log(1+tsum);var eras=item.eras||[];for(var j=0;j<eras.length;j++){s+=0.5*(pts.era[eras[j]]||0)*(j===0?1:0.6);}return s+(jit||0);}
function scores(state,data,QS){var pts=pointsFor(state,QS);var jit=jitters(state,data.items.length);var out=new Array(data.items.length);for(var i=0;i<data.items.length;i++)out[i]=scoreItem(data.items[i],pts,jit[i]);return out;}
function sortedOrder(sc){var order=[];for(var i=0;i<sc.length;i++)order.push(i);order.sort(function(a,b){return sc[b]-sc[a];});return order;}
function marginOf(sc){var order=sortedOrder(sc);var s1=sc[order[0]],s2=sc[order[1]];return(s1-s2)/(Math.abs(s1)+Math.abs(s2)+1e-9);}
function discriminate(q,leaderIdx,data,pts,jit){var gains=[];var argmax={};for(var li=0;li<leaderIdx.length;li++){var i=leaderIdx[li];var item=data.items[i];var best=-1e9,bestOpt=-1;for(var o=0;o<q.opts.length;o++){var p2=clonePts(pts);addEffect(p2,q.opts[o].e);var s=scoreItem(item,p2,jit[i]);if(s>best){best=s;bestOpt=o;}}gains.push(best);argmax[bestOpt]=(argmax[bestOpt]||0)+1;}var mean=0;for(var g=0;g<gains.length;g++)mean+=gains[g];mean/=gains.length;var vr=0;for(var g2=0;g2<gains.length;g2++)vr+=(gains[g2]-mean)*(gains[g2]-mean);var stdev=Math.sqrt(vr/gains.length);var distinct=0;for(var k in argmax)distinct++;return stdev+0.2*distinct;}
function nextQuestion(state,data,QS){if(state.answers.length===0)return QS[0].id;if(state.answers.length>=14)return null;var used={};for(var i=0;i<state.answers.length;i++)used[state.answers[i].q]=true;var sc=scores(state,data,QS);var order=sortedOrder(sc);var leaders=order.slice(0,Math.min(40,order.length));var pts=pointsFor(state,QS);var jit=jitters(state,data.items.length);var best=null,bestDisc=0;for(var q=0;q<QS.length;q++){var question=QS[q];if(used[question.id])continue;var d=discriminate(question,leaders,data,pts,jit);if(d>bestDisc){bestDisc=d;best=question.id;}}if(bestDisc<=0.05)return null;return best;}
function finished(state,data,QS){var n=state.answers.length;if(n===0)return{done:false,reason:'start'};if(n>=10&&n<14){var sc=scores(state,data,QS);var margin=marginOf(sc);if(margin>0.045)return{done:true,reason:'confident'};}if(n>=14)return{done:true,reason:'max'};if(n>=8&&!nextQuestion(state,data,QS))return{done:true,reason:'no-questions'};return{done:false};}
function result(state,data,QS){var sc=scores(state,data,QS);var order=sortedOrder(sc);var winner=order[0];var runners=[];var seen={};seen[data.items[winner].title]=true;for(var i=1;i<order.length&&runners.length<3;i++){var it=data.items[order[i]];if(seen[it.title])continue;seen[it.title]=true;runners.push(order[i]);}return{winner:winner,runners:runners,scores:sc,order:order};}
var QuizEngine={createGame:createGame,nextQuestion:nextQuestion,finished:finished,result:result,parseEras:parseEras};
"""

UI_JS = r"""
(function(){
 var DATA=window.QUIZ_DATA;
 for(var ei=0;ei<DATA.items.length;ei++)DATA.items[ei].eras=QuizEngine.parseEras(DATA.items[ei].year);
 var QS=null;
 try{QS=JSON.parse(document.getElementById('quiz-questions').textContent);}catch(e){}
 var state=null,current=null;
 var elStep=document.getElementById('q-step');
 var elText=document.getElementById('q-text');
 var elOpts=document.getElementById('q-opts');
 var elQ=document.getElementById('quiz-question');
 var elR=document.getElementById('quiz-result');
 var elIntro=document.getElementById('quiz-intro');
 var AXIS_RU={dvaita:'двайта',advaita:'адвайта',sunyata:'пустотные'};
 function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
 function start(){state=QuizEngine.createGame((Date.now()%2147483647)||1);elIntro.style.display='none';elR.style.display='none';elQ.style.display='';next();}
 function next(){
  var qid=QuizEngine.nextQuestion(state,DATA,QS);
  var fin=QuizEngine.finished(state,DATA,QS);
  if(fin.done||!qid){showResult();return;}
  var q=null;for(var i=0;i<QS.length;i++)if(QS[i].id===qid)q=QS[i];
  if(!q){showResult();return;}
  current=q;
  elStep.textContent='Вопрос '+(state.answers.length+1);
  elText.textContent=q.text;
  elOpts.innerHTML='';
  for(var o=0;o<q.opts.length;o++){
   var b=document.createElement('button');
   b.className='q-opt';b.type='button';
   b.textContent=q.opts[o].t;
   (function(idx,btn){btn.onclick=function(){pick(idx);};})(o,b);
   elOpts.appendChild(b);
  }
 }
 function pick(o){if(!current)return;state.answers.push({q:current.id,o:o});current=null;next();}
 function itemCard(it,main){
  var badges='';
  if(it.family)badges+='<span class="q-badge">'+esc(it.family)+'</span>';
  if(it.year)badges+='<span class="q-badge">'+esc(it.year)+'</span>';
  if(it.axis&&AXIS_RU[it.axis])badges+='<span class="q-badge q-badge-ax">'+AXIS_RU[it.axis]+'</span>';
  var h='<div class="q-res'+(main?' q-res-main':'')+'">';
  if(main)h+='<div class="q-res-label">Тебе ближе:</div>';
  h+='<h3 class="q-res-title">'+esc(it.title)+'</h3>';
  h+='<div class="q-badges">'+badges+'</div>';
  if(it.description)h+='<p class="q-res-desc">'+esc(it.description)+'</p>';
  h+='<a class="q-btn q-btn-primary" target="_blank" rel="noopener" href="'+esc(it.link)+'">Читать статью в Веротеке →</a>';
  return h+'</div>';
 }
 function showResult(){
  elQ.style.display='none';
  var r=QuizEngine.result(state,DATA,QS);
  var w=DATA.items[r.winner];
  var h=itemCard(w,true);
  if(r.runners&&r.runners.length){
   h+='<div class="q-res-label" style="margin-top:18px">Также присмотрись:</div>';
   for(var i=0;i<r.runners.length;i++)h+=itemCard(DATA.items[r.runners[i]],false);
  }
  h+='<button class="q-btn q-btn-ghost" id="q-restart" type="button">Пройти ещё раз</button>';
  elR.innerHTML=h;elR.style.display='';
  document.getElementById('q-restart').onclick=start;
 }
 document.getElementById('q-start').onclick=start;
 window.__quizStart=start;
})();
"""

QUIZ_CSS = """
.q-wrap{max-width:640px;margin:0 auto;}
.q-intro{padding:26px 22px;}
.q-intro h2{margin:0 0 10px;font-size:1.5rem;}
.q-intro p{color:var(--muted);margin:0 0 18px;}
.q-card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:22px;box-shadow:0 1px 3px rgba(0,0,0,.05);}
.q-step{font-size:.78rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:6px;}
.q-qtext{font-size:1.18rem;font-weight:600;margin:0 0 16px;}
.q-opt{display:block;width:100%;text-align:left;background:var(--card);border:1px solid var(--border);border-radius:12px;padding:13px 15px;margin:8px 0;font-size:.98rem;cursor:pointer;transition:border-color .15s,background .15s,transform .06s;font-family:inherit;color:var(--fg);}
.q-opt:hover{border-color:var(--accent);background:rgba(79,70,229,.05);}
.q-opt:active{transform:scale(.995);}
.q-btn{display:inline-block;border:none;border-radius:12px;padding:12px 20px;font-size:1rem;cursor:pointer;font-family:inherit;text-decoration:none;}
.q-btn-primary{background:linear-gradient(135deg,#4f46e5,#8b5cf6);color:#fff;width:100%;text-align:center;margin-top:12px;}
.q-btn-primary:hover{opacity:.92;}
.q-btn-ghost{background:transparent;border:1px solid var(--border);color:var(--fg);width:100%;margin-top:16px;}
.q-res{border:1px solid var(--border);border-radius:14px;padding:16px 18px;margin:10px 0;background:var(--card);}
.q-res-main{border-color:#4f46e5;box-shadow:0 2px 10px rgba(79,70,229,.10);}
.q-res-label{font-size:.8rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);}
.q-res-title{margin:6px 0 8px;font-size:1.25rem;}
.q-res-main .q-res-title{font-size:1.45rem;}
.q-badges{margin:0 0 10px;display:flex;flex-wrap:wrap;gap:6px;}
.q-badge{display:inline-block;background:rgba(79,70,229,.08);border:1px solid rgba(79,70,229,.18);color:#4f46e5;border-radius:999px;padding:2px 10px;font-size:.8rem;}
.q-badge-ax{background:rgba(139,92,246,.08);border-color:rgba(139,92,246,.2);color:#7c3aed;}
.q-res-desc{color:var(--muted);font-size:.95rem;line-height:1.5;margin:0 0 6px;}
@media (max-width:640px){.q-card{padding:16px;border-radius:14px;}.q-qtext{font-size:1.08rem;}.q-opt{padding:12px 13px;font-size:.95rem;}}
"""

def build_quiz(site_dir):
    site = Path(site_dir)
    data = json.loads((BUILD / "quiz-data.json").read_text(encoding="utf-8"))
    import html as _html
    qjs = _html.escape(QUESTIONS_JS.replace("</", "<\\/"), quote=False).replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')
    # безопаснее: положить QUESTIONS как JS-литерал без экранирования, но внутри <script type="application/json"> экранируем только </script>
    qjson = json.dumps([{"id": q["id"], "text": q["text"], "opts": [{"t": o["t"], "e": o["e"]} for o in q["opts"]]} for q in json.loads(_QUESTIONS_JSON)], ensure_ascii=False).replace("</", "<\\/")
    datajs = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    page = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Тест: Какая религия вам ближе? - Веротека</title>
<meta property="og:title" content="Тест: Какая религия вам ближе? — Веротека">
<meta property="og:description" content="Адаптивный тест по банку традиций Веротеки: 10–14 вопросов — и ссылка на твою статью.">
<link rel="stylesheet" href="assets/style.css">
<style>{QUIZ_CSS}</style>
</head>
<body>
<header class="topbar">
  <a class="brand" href="index.html">Веротека</a>
  <nav class="topnav">
    <a href="az.html">А-Я</a>
    <a href="tags.html">Теги</a>
    <a href="axis.html">Ось</a>
    <a href="quiz.html">Тест</a>
    <a href="ru/09_ref/about/about.html">О проекте</a>
  </nav>
  <input id="searchbox" type="search" placeholder="Поиск..." autocomplete="off">
  <button id="themeToggle" title="Тёмная/светлая тема">&#127769;</button>
</header>
<div id="searchresults"></div>
<main class="wide">
<div class="q-wrap">
<section id="quiz-intro" class="q-card q-intro">
  <h2>Какая религия вам ближе?</h2>
  <p>10–14 вопросов, каждый следующий зависит от твоих ответов. В конце — традиция из банка Веротеки ({data['count']} религий, конфессий, сект и эзотерических учений) и ссылка на статью о ней.</p>
  <button id="q-start" class="q-btn q-btn-primary" type="button">Начать тест</button>
</section>
<section id="quiz-question" class="q-card" style="display:none">
  <div class="q-step" id="q-step"></div>
  <div class="q-qtext" id="q-text"></div>
  <div id="q-opts"></div>
</section>
<section id="quiz-result" style="display:none"></section>
</div>
</main>
<script type="application/json" id="quiz-data">{datajs}</script>
<script type="application/json" id="quiz-questions">{qjson}</script>
<script>{ENGINE_JS}
window.QUIZ_DATA=JSON.parse(document.getElementById('quiz-data').textContent);
{UI_JS}</script>
</body>
</html>"""
    (site / "quiz.html").write_text(page, encoding="utf-8")
    print("quiz.html: items=%d questions=14" % data["count"])


# JSON-источник вопросов (тот же массив, что QUESTIONS_JS, машиночитаемо)
import re as _re
_QUESTIONS_JSON = None  # заполняется ниже

def _questions_from_js():
    """Извлечь QUESTIONS из QUESTIONS_JS как Python-объект (через json5-подобный парс)"""
    import json
    src = QUESTIONS_JS
    src = src[src.index('['):src.rindex(']') + 1]
    # JS-объект -> JSON: ключи без кавычек
    src = _re.sub(r'([{,]\s*)([A-Za-z_А-Яа-яЁё][\w]*)\s*:', r'\1"\2":', src)
    src = src.replace("'", '"')
    return json.loads(src)

_QUESTIONS_JSON = json.dumps(_questions_from_js(), ensure_ascii=False)
