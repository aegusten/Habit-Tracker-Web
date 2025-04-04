document.addEventListener("DOMContentLoaded",function(){
  const cd=document.getElementById("chart-data");
  const cf=document.getElementById("chart-fields");
  const cm=document.getElementById("chart-method");
  if(!cd||!cf||!cm)return;
 
  const chartData=JSON.parse(cd.textContent||"[]");
  const fields=JSON.parse(cf.textContent||"[]");
  const method=JSON.parse(cm.textContent||'"chart"');
  const labels=chartData.map(r=>r.date);
 
  function checkFrontEndProgress(data){
    let consecutiveZero=0;
    for(let i=data.length-1; i>=0; i--){
      let cigs=data[i].cigarettes_per_day||0;
      if(+cigs===0) consecutiveZero++;
      else break;
    }
    let msgBox=document.getElementById("frontendProgressMsg");
    if(!msgBox)return;
    if(consecutiveZero>=5){
      msgBox.textContent="Front-end says: You have 5+ consecutive smoke-free days!";
      msgBox.classList.remove("d-none","alert-info");
      msgBox.classList.add("alert-success");
    } else if(consecutiveZero>0){
      msgBox.textContent=`Front-end says: You have ${consecutiveZero} consecutive smoke-free day(s). Keep going!`;
      msgBox.classList.remove("d-none","alert-success");
      msgBox.classList.add("alert-info");
    } else {
      msgBox.classList.add("d-none");
    }
  }
 
  const modal=document.getElementById("insightModal");
  if(!modal)return;
 
  modal.addEventListener("shown.bs.modal",()=>{
   checkFrontEndProgress(chartData);
 
   fields.forEach((field,index)=>{
    const label=field.replace(/_/g," ").replace(/\b\w/g,c=>c.toUpperCase());
    const values=chartData.map(row=>row[field]||0);

    if(method==="chart"||method==="both"){
     const chartCanvas=document.getElementById(`modalChart_${index+1}`);
     if(chartCanvas&&chartCanvas.dataset.rendered!=="true"){
      chartCanvas.dataset.rendered="true";
      const ctx=chartCanvas.getContext("2d");
      const grad=ctx.createLinearGradient(0,0,0,chartCanvas.height);
      grad.addColorStop(0,"rgba(64,128,255,0.4)");
      grad.addColorStop(1,"rgba(64,128,255,0)");
      new Chart(ctx,{
       type:"line",
       data:{
        labels:labels,
        datasets:[{
         label:label,
         data:values,
         borderColor:"rgba(64,128,255,1)",
         backgroundColor:grad,
         fill:true,
         tension:0.3
        }]
       },
       options:{
        responsive:true,
        maintainAspectRatio:false,
        plugins:{legend:{display:true}}
       }
      });
     }
    }
 
    if(method==="graph"||method==="both"){
     const graphCanvas=document.getElementById(`modalGraph_${index+1}`);
     if(graphCanvas&&graphCanvas.dataset.rendered!=="true"){
      graphCanvas.dataset.rendered="true";
      const ctx=graphCanvas.getContext("2d");
      new Chart(ctx,{
       type:"bar",
       data:{
        labels:labels,
        datasets:[{
         label:label,
         data:values,
         backgroundColor:"rgba(255,99,132,0.7)",
         borderColor:"rgba(255,99,132,1)",
         borderWidth:1
        }]
       },
       options:{
        responsive:true,
        maintainAspectRatio:false,
        plugins:{legend:{display:true}}
       }
      });
     }
    }
   });
  });
 });
 