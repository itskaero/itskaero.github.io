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
 const el=document.createElement("div");
 if(type==="merit"){
   [["3,473+ candidates",9,22],["preferences",35,17],["quotas",15,53],["seats",41,61],["marks",60,27],["allocate()",70,61]].forEach((x,i)=>{let c=document.createElement("div");c.className="data-chip"+(i===5?" hot":"");c.textContent=x[0];c.style.left=x[1]+"%";c.style.top=x[2]+"%";c.style.animationDelay=(-i*.35)+"s";el.appendChild(c)});
   [[18,31,70,35],[43,28,22,31],[49,66,25,-18],[60,40,18,31]].forEach(x=>{let l=document.createElement("div");l.className="network-line";l.style.left=x[0]+"%";l.style.top=x[1]+"%";l.style.width=x[2]+"%";l.style.transform=`rotate(${x[3]}deg)`;el.appendChild(l)});
   for(let i=0;i<9;i++){let b=document.createElement("div");b.className="bar";b.style.left=(10+i*8)+"%";b.style.height=(25+((i*17)%70))+"px";el.appendChild(b)}
 }else if(type==="nabz"){
   let c=document.createElement("div");c.className="rx-card";c.innerHTML="<small>PATIENT</small><br><strong>AHMAD R.</strong><br><br><small>RX</small><div class='rx-rule'></div><div class='rx-rule' style='width:60%'></div><div class='urdu'>مریض کو ہدایات</div><div class='rx-stamp'>LOCAL<br>FIRST</div>";el.appendChild(c);
 }else if(type==="micro"){
   let grid=document.createElement("div");grid.className="micro-grid";[45,72,55,90,62,78,50].forEach((h,i)=>{let s=document.createElement("span");s.style.setProperty("--h",h+"%");s.style.animationDelay=(-i*.2)+"s";grid.appendChild(s)});el.appendChild(grid);
 }else{
   [["AUTH",16,25],["DATA",42,18],["AUDIT",67,32],["SQL",28,62],["BUILD",63,67]].forEach((x,i)=>{let c=document.createElement("div");c.className="data-chip"+(i===4?" hot":"");c.textContent=x[0];c.style.left=x[1]+"%";c.style.top=x[2]+"%";el.appendChild(c)});
 }
 return el;
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

showProject("meritnama",false);
