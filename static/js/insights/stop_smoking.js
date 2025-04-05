document.addEventListener("DOMContentLoaded", function(){
  const cdEl = document.getElementById("modal-chart-data");
  const cfEl = document.getElementById("modal-chart-fields");
  const cmEl = document.getElementById("modal-chart-method");
  const upEl = document.getElementById("modal-user-prefs");
  if(!cdEl || !cfEl || !cmEl || !upEl) return;
  const chartData = JSON.parse(cdEl.textContent || "[]");
  const fields = JSON.parse(cfEl.textContent || "[]");
  const method = JSON.parse(cmEl.textContent || '"chart"');
  const userPrefs = JSON.parse(upEl.textContent || "{}");
  const modal = document.getElementById("insightModal");
  if(!modal) return;
  let graphInstance = null;
  let chartInstance = null;
  function labelify(str) {
    return str.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
  }
  modal.addEventListener("shown.bs.modal", () => {
    const fieldTogglesEls = document.querySelectorAll(".fieldToggle");
    const graphTypeEls = document.querySelectorAll(".graphTypeChoice");
    const chartTypeEls = document.querySelectorAll(".chartTypeChoice");
    function getSelectedFields() {
      let arr = [];
      fieldTogglesEls.forEach(chk => {
        if(chk.checked) arr.push(chk.dataset.fieldName);
      });
      return arr;
    }
    function buildDatasetsForTime(selected) {
      const dateLabels = chartData.map(r => r.date);
      const datasets = selected.map(fn => {
        const dataArr = chartData.map(row => parseFloat(row[fn] || 0));
        return { label: labelify(fn), data: dataArr };
      });
      return { labels: dateLabels, datasets };
    }
    function buildPieData(selected) {
      if(!chartData.length) return { labels: [], data: [] };
      const lastRow = chartData[chartData.length - 1];
      const labels = [];
      const data = [];
      selected.forEach(f => {
        labels.push(labelify(f));
        data.push(parseFloat(lastRow[f] || 0));
      });
      return { labels, data };
    }
    function updateGraph() {
      const sel = getSelectedFields();
      if(!sel.length) { if(graphInstance) graphInstance.destroy(); return; }
      let userGraph = "auto";
      graphTypeEls.forEach(r => { if(r.checked) userGraph = r.value; });
      if(graphInstance) graphInstance.destroy();
      if(userGraph === "pie") {
        const pd = buildPieData(sel);
        graphInstance = new Chart(document.getElementById("graphCanvas").getContext("2d"), {
          type: "pie",
          data: {
            labels: pd.labels,
            datasets: [{
              label: "Distribution",
              data: pd.data,
              backgroundColor: ["#ffd54f", "#fff176", "#ffecb3", "#ffe082", "#ffe57f", "#fff9c4"],
              borderColor: "#ffca28"
            }]
          },
          options: { responsive: true, maintainAspectRatio: false }
        });
      } else {
        let finalType = (userGraph === "auto") ? "bar" : userGraph;
        const tdata = buildDatasetsForTime(sel);
        tdata.datasets.forEach(ds => {
          ds.backgroundColor = "rgba(255,193,7,0.6)";
          ds.borderColor = "rgba(255,193,7,1)";
          ds.borderWidth = 1;
        });
        graphInstance = new Chart(document.getElementById("graphCanvas").getContext("2d"), {
          type: finalType,
          data: { labels: tdata.labels, datasets: tdata.datasets },
          options: { responsive: true, maintainAspectRatio: false }
        });
      }
    }
    function updateChart() {
      const sel = getSelectedFields();
      if(!sel.length) { if(chartInstance) chartInstance.destroy(); return; }
      let userChart = "auto";
      chartTypeEls.forEach(r => { if(r.checked) userChart = r.value; });
      if(chartInstance) chartInstance.destroy();
      let finalType = (userChart === "auto") ? "line" : (userChart === "bar" ? "bar" : userChart);
      const tdata = buildDatasetsForTime(sel);
      let colorList = ["rgba(0,123,255,0.4)", "rgba(40,167,69,0.4)", "rgba(255,193,7,0.4)", "rgba(220,53,69,0.4)"];
      tdata.datasets.forEach((ds, i) => {
        ds.backgroundColor = colorList[i % colorList.length];
        ds.borderColor = colorList[i % colorList.length].replace("0.4", "1");
        ds.borderWidth = 1;
        ds.fill = (finalType === "line");
        ds.tension = 0.3;
      });
      chartInstance = new Chart(document.getElementById("chartCanvas").getContext("2d"), {
        type: finalType,
        data: { labels: tdata.labels, datasets: tdata.datasets },
        options: { responsive: true, maintainAspectRatio: false }
      });
      let sum = 0, count = 0;
      sel.forEach(f => {
        chartData.forEach(r => {
          sum += parseFloat(r[f] || 0);
          count++;
        });
      });
      let avg = (count > 0) ? (sum / count).toFixed(2) : "0";
      document.getElementById("chartSummary").textContent = `Total: ${sum}, Avg: ${avg}`;
    }
    document.querySelectorAll(".fieldToggle").forEach(chk => {
      chk.addEventListener("change", () => { updateGraph(); updateChart(); });
    });
    document.querySelectorAll(".graphTypeChoice").forEach(radio => {
      radio.addEventListener("change", updateGraph);
    });
    document.querySelectorAll(".chartTypeChoice").forEach(radio => {
      radio.addEventListener("change", updateChart);
    });
    updateGraph();
    updateChart();
  });
});
