const projects={
meritnama:{title:"MERITNAMA",sub:"medical induction intelligence",kicker:"01 / PROBLEM",body:"Medical induction data was scattered, manual and difficult to interpret. The system was a black box. I wanted to understand it.",stack:"Python · JavaScript · PostgreSQL · Docker",open:"https://itskaero.github.io/meritnama/",github:"https://github.com/itskaerox/meritnama",type:"merit",next:"NABZ",nextCopy:"Clinical documentation was slow, manual and unfriendly. So I built something better.",nextLink:"https://itskaero.github.io/nabz/",detail:"A residency induction system is more than a list. It is marks, preferences, quotas, seats and rules interacting with each other.",steps:["The induction process was difficult to reason about.","I broke the system into candidates, preferences, quotas, seats and rules.","Patterns appeared when the data was structured and compared across cycles.","The pieces became calculators, analytics and a seat-allocation simulator.","The result: a tool for understanding where you stand and how an induction may play out."]},
nabz:{title:"NABZ",sub:"clinical workflow & prescriptions",kicker:"02 / PROBLEM",body:"Clinical documentation was slow, manual and unfriendly. I wanted a local-first workflow that respected the way doctors actually work.",stack:"HTML · CSS · JavaScript · PWA",open:"https://itskaero.github.io/nabz/",github:"https://github.com/itskaerox/nabz",type:"nabz",next:"ANTIBIOTIGRAM",nextCopy:"Antibiotic information is easier to use when susceptibility patterns can be seen, not just read.",nextLink:"https://itskaero.github.io/antibiotigram/",detail:"A prescription is a tiny document with a lot of friction hidden inside it.",steps:["Writing and explaining prescriptions takes repeated manual work.","I separated the workflow into patient, prescription and instructions.","Bilingual output and reusable structures made the pieces fit.","The pieces became a local-first prescription workflow.","The result: a clinical tool built around the workflow, not around the software."]},
antibiome:{title:"ANTIBIOME",sub:"culture surveillance & local guidelines",kicker:"03 / PROBLEM",body:"Cultures were happening, resistance patterns were changing, but the information needed to become a useful local picture. Antibiome was built to surveil cultures and help guide local antibiotic guidelines.",stack:"Python · JavaScript · Data · Clinical systems",open:"https://itskaero.github.io/antibiome/",github:"https://github.com/itskaerox/antibiome",type:"micro",next:"ANTIBIOTIGRAM",nextCopy:"From local microbiology to a visual way of thinking about antibiotics.",nextLink:"https://itskaero.github.io/antibiotigram/",detail:"The useful thing is not merely storing culture reports. It is seeing what is happening locally.",steps:["Cultures generate data, but isolated reports hide the larger pattern.","I started structuring organisms, specimens and susceptibility results.","The pattern is a local resistance picture that can change over time.","That picture can feed practical local antibiotic guidance.","The result: surveillance designed around the question clinicians actually ask."]},
antibiotigram:{title:"ANTIBIOTIGRAM",sub:"antibiotic susceptibility visualizer",kicker:"04 / QUESTION",body:"Antibiotic information can become a wall of tables. I wanted to make the relationships easier to see and reason about.",stack:"JavaScript · HTML · CSS · Clinical visualization",open:"https://itskaero.github.io/antibiotigram/",github:"https://github.com/itskaerox/antibiotigram",type:"micro",next:"ANTIBIOME",nextCopy:"The visual question led back to the underlying local microbiology.",nextLink:"https://itskaero.github.io/antibiome/",detail:"An antibiogram is data, but the point is the decision hidden inside the data.",steps:["Tables make susceptibility hard to scan quickly.","I turned organisms, antibiotics and susceptibility into visual relationships.","Patterns become visible instead of requiring every cell to be read.","The visualization becomes a way to ask better clinical questions.","The result: a more visual interface to antibiotic susceptibility."]},
nigheban:{title:"NIGHEBAN",sub:"system experiment",kicker:"05 / EXPERIMENT",body:"An evolving experiment in building the infrastructure around a useful system. Not everything starts with a finished product.",stack:"Python · JavaScript · SQL",open:"https://itskaero.github.io/nigheban/",github:"https://github.com/itskaerox/nigheban",type:"system",next:"BAHAWALPURNAMA",nextCopy:"Another local question is taking shape.",nextLink:"https://github.com/itskaerox/bahawalpurnama",detail:"Some projects are useful precisely because they are unfinished.",steps:["There was a system I wanted to understand and improve.","I started by separating the moving parts and their data.","The architecture became the experiment.","The build is still evolving rather than pretending to be complete.","That is okay. Some questions need more than one version."]},
bahawalpurnama:{title:"BAHAWALPURNAMA",sub:"local information / building…",kicker:"06 / BUILDING",body:"A new experiment around local information, data and the place I know. Still being assembled.",stack:"Early build · data · web",open:"https://github.com/itskaerox/bahawalpurnama",github:"https://github.com/itskaerox/bahawalpurnama",type:"local",next:"MERITNAMA",nextCopy:"Back to where the archive began.",nextLink:"https://itskaero.github.io/meritnama/",detail:"A local question is taking shape.",steps:["Something local is fragmented or hard to find.","The first step is figuring out what the pieces actually are.","Patterns should emerge from the data rather than assumptions.","Then the interface can make the useful part visible.","For now: building."]}};

const $=s=>document.querySelector(s), $$=s=>document.querySelectorAll(s);
let currentKey="meritnama";

function sceneFor(type){
  const wrap=document.createElement("div");
  wrap.className="project-assembly";
  const grid=document.createElement("div"); grid.className="assembly-grid"; wrap.appendChild(grid);

  const targetMap={
    merit:{label:"ALLOCATION SYSTEM", points:[[38,38],[50,25],[62,38],[62,62],[50,75],[38,62],[50,50]]},
    nabz:{label:"PRESCRIPTION", points:[[36,32],[64,32],[64,68],[36,68],[50,50]]},
    micro:{label:"LOCAL RESISTANCE", points:[[30,40],[45,27],[65,40],[58,67],[38,67],[50,50]]},
    system:{label:"SYSTEM", points:[[35,35],[65,35],[65,65],[35,65],[50,50]]},
    local:{label:"LOCAL DATA", points:[[32,42],[48,28],[68,43],[58,68],[38,68],[50,50]]}
  };
  const cfg=targetMap[type]||targetMap.system;
  const starts=[
    [8,12],[23,82],[78,13],[92,72],[11,56],[72,88],
    [52,8],[87,43],[28,18],[60,94],[4,87],[94,18]
  ];
  for(let i=0;i<12;i++){
    const f=document.createElement("i");
    f.className="fragment"+(i%4===0?" hot":"");
    const t=cfg.points[i%cfg.points.length];
    f.style.setProperty("--sx",starts[i][0]+"%");
    f.style.setProperty("--sy",starts[i][1]+"%");
    f.style.setProperty("--tx",t[0]+"%");
    f.style.setProperty("--ty",t[1]+"%");
    f.style.setProperty("--r",((i*47)%140-70)+"deg");
    f.style.setProperty("--delay",(i*.055)+"s");
    wrap.appendChild(f);
  }
  const target=document.createElement("div"); target.className="target"; wrap.appendChild(target);
  const dot=document.createElement("div"); dot.className="target-dot"; wrap.appendChild(dot);
  const label=document.createElement("div"); label.className="target-label"; label.textContent=cfg.label; wrap.appendChild(label);
  const note=document.createElement("div"); note.className="scene-note"; note.textContent="FRAGMENTS → PATTERN → TOOL"; wrap.appendChild(note);
  return wrap;
}
function showProject(key,scroll=true){
 currentKey=key; const p=projects[key];
 $("#case-kicker").textContent=p.kicker;$("#case-title").textContent=p.title;$("#case-sub").textContent=p.sub;$("#case-body").textContent=p.body;$("#case-stack").textContent=p.stack;
 $("#case-open").href=p.open;$("#case-github").href=p.github;$("#case-number").textContent=String(Object.keys(projects).indexOf(key)+1).padStart(2,"0")+" / 06";
 $("#scene").replaceChildren(sceneFor(p.type));
 $("#detail-title").textContent=p.detail;$("#detail-text").textContent=p.steps[0];
 $("#next-title").textContent=p.next;$("#next-copy").textContent=p.nextCopy;$("#next-link").href=p.nextLink;
 $$(".tl").forEach((b,i)=>b.classList.toggle("active",i===0)); renderTimeline(0);
 if(scroll) $("#case-study").scrollIntoView({behavior:"smooth"});
}

function renderTimeline(i){
 const p=projects[currentKey], out=$("#timeline-output");
 out.innerHTML="";
 if(i===0){let x=document.createElement("div");x.className="bigword";x.textContent="WHY?";out.appendChild(x)}
 if(i===1){let x=document.createElement("div");x.className="grid-points";out.appendChild(x)}
 if(i===2){let x=document.createElement("div");x.className="orbit";out.appendChild(x);for(let n=0;n<7;n++){let q=document.createElement("i");q.className="network-node";q.style.left=(25+Math.random()*50)+"%";q.style.top=(20+Math.random()*60)+"%";out.appendChild(q)}}
 if(i===3){let x=document.createElement("div");x.className="assembled";out.appendChild(x)}
 if(i===4){let x=document.createElement("div");x.className="result";[32,62,48,79,55].forEach(h=>{let q=document.createElement("i");q.style.setProperty("--h",h+"%");x.appendChild(q)});out.appendChild(x)}
 $("#detail-eyebrow").textContent=["THE PROBLEM","TAKE IT APART","FIND THE PATTERN","BUILD SOMETHING","THE RESULT"][i];
 $("#detail-text").textContent=p.steps[i];
}

$$(".node-card").forEach(n=>n.addEventListener("click",()=>showProject(n.dataset.project)));
$$(".filters button").forEach(b=>b.addEventListener("click",()=>{$$(".filters button").forEach(x=>x.classList.remove("active"));b.classList.add("active");const f=b.dataset.filter;$$(".node-card").forEach(n=>n.classList.toggle("hidden",f!=="all"&&!n.dataset.tags.split(" ").includes(f)))}));
$$(".tl").forEach((b,i)=>b.addEventListener("click",()=>{$$(".tl").forEach(x=>x.classList.remove("active"));b.classList.add("active");renderTimeline(i)}));

const observer=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)e.target.classList.add("visible")}),{threshold:.12});
$$(".process-step").forEach(x=>observer.observe(x));

const hero=$(".hero"), title=$(".hero h1");
hero.addEventListener("pointermove",e=>{if(matchMedia("(pointer:fine)").matches){let r=hero.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;title.style.transform=`translate(${x*8}px,${y*6}px)`}});
hero.addEventListener("pointerleave",()=>title.style.transform="");

const dot=$(".cursor-dot"),ring=$(".cursor-ring");
window.addEventListener("pointermove",e=>{dot.style.left=e.clientX+"px";dot.style.top=e.clientY+"px";ring.animate({left:e.clientX+"px",top:e.clientY+"px"},{duration:160,fill:"forwards"})});
$$("a,button").forEach(el=>{el.addEventListener("mouseenter",()=>{ring.style.width="50px";ring.style.height="50px"});el.addEventListener("mouseleave",()=>{ring.style.width="34px";ring.style.height="34px"})});


/* v3: real fragment assembly driven by scroll */
(function initAssembly(){
  const section=document.querySelector("[data-assembly]");
  if(!section)return;
  const stage=section.querySelector(".assembly-stage");
  const svg=section.querySelector("#assembly-svg");
  const fragments=[...section.querySelectorAll("[data-fragment]")];
  const edges=[...section.querySelectorAll("[data-edge]")];
  const nodes=[...section.querySelectorAll("[data-node]")];
  const labels=[...section.querySelectorAll(".assembly-labels text")];
  const steps=[...section.querySelectorAll(".assembly-step")];
  const percent=section.querySelector("#assembly-percent");
  const status=section.querySelector("#assembly-status");
  const replay=section.querySelector("#replay-assembly");
  const reduced=window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const targets=[
    [-120,-70],[0,-140],[120,-70],[120,70],[0,140],[-120,70],[0,0],
    [-60,-105],[60,-105],[60,35],[-60,35],[0,70]
  ];
  const starts=[
    [-255,-135],[-120,205],[235,-155],[-270,80],[220,190],[-205,165],
    [250,30],[-20,-205],[145,215],[-250,-15],[190,-20],[-95,220]
  ];
  const rotations=[-35,28,72,-20,48,-60,32,-18,55,-42,20,-75];

  function ease(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2}
  function lerp(a,b,t){return a+(b-a)*t}
  function draw(raw){
    const p=Math.max(0,Math.min(1,raw));
    const ep=ease(p);
    fragments.forEach((f,i)=>{
      const delay=i*.025;
      const local=Math.max(0,Math.min(1,(ep-delay)/(1-delay)));
      const x=lerp(starts[i][0],targets[i][0],local);
      const y=lerp(starts[i][1],targets[i][1],local);
      const r=lerp(rotations[i],0,local);
      f.setAttribute("transform",`translate(${x} ${y}) rotate(${r})`);
      f.style.opacity=String(1-Math.max(0,local-.72)*2.2);
    });
    edges.forEach((e,i)=>{
      const on=Math.max(0,Math.min(1,(p-(.52+i*.025))/.35));
      const len=e.getTotalLength();
      e.style.strokeDasharray=len;
      e.style.strokeDashoffset=len*(1-on);
      e.style.opacity=String(on);
    });
    nodes.forEach((n,i)=>{
      const on=Math.max(0,Math.min(1,(p-.75-i*.02)/.25));
      n.style.opacity=String(on);
      n.style.transform=`scale(${.65+.35*on})`;
      n.style.transformOrigin="center";
    });
    labels.forEach((l,i)=>{
      const on=Math.max(0,Math.min(1,(p-.84-i*.04)/.16));
      l.style.opacity=String(on);
    });
    const pct=Math.round(p*100);
    percent.textContent=String(pct).padStart(2,"0")+"%";
    status.textContent=p<.22?"DISASSEMBLED":p<.52?"INVESTIGATING":p<.82?"ASSEMBLING":"BUILT";
    steps.forEach((s,i)=>s.classList.toggle("active",i===Math.min(4,Math.floor(p*5))));
    stage.classList.toggle("assembled",p>.96);
  }

  let raf=0;
  function update(){
    cancelAnimationFrame(raf);
    raf=requestAnimationFrame(()=>{
      const r=section.getBoundingClientRect();
      const travel=Math.max(1,section.offsetHeight-window.innerHeight);
      const p=Math.max(0,Math.min(1,(-r.top+window.innerHeight*.12)/travel));
      draw(p);
    });
  }
  window.addEventListener("scroll",update,{passive:true});
  window.addEventListener("resize",update);

  replay.addEventListener("click",()=>{
    if(reduced){draw(1);return}
    const start=performance.now();
    function loop(now){
      const t=Math.min(1,(now-start)/1500);
      draw(t);
      if(t<1)requestAnimationFrame(loop);
    }
    requestAnimationFrame(loop);
  });

  draw(reduced?1:0);
})();

showProject("meritnama",false);
