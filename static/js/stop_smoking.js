document.addEventListener("DOMContentLoaded", function () {
  const chartData = JSON.parse(document.getElementById("chart-data").textContent || "[]");
  const fields = JSON.parse(document.getElementById("chart-fields").textContent || "[]");
  const method = JSON.parse(document.getElementById("chart-method").textContent || '"chart"');
  const labels = chartData.map(row => row.date);

  const insightModal = document.getElementById("insightModal");
  if (!insightModal) return;

  insightModal.addEventListener("shown.bs.modal", () => {
    fields.forEach((field, index) => {
      const label = field.replace(/_/g, " ").replace(/\b\w/g, l => l.toUpperCase());
      const values = chartData.map(row => row[field] || 0);

      if (method === "chart" || method === "both") {
        const chartCanvas = document.getElementById(`modalChart_${index + 1}`);
        if (chartCanvas && chartCanvas.dataset.rendered !== "true") {
          chartCanvas.dataset.rendered = "true";
          const ctx = chartCanvas.getContext("2d");

          const gradient = ctx.createLinearGradient(0, 0, 0, chartCanvas.height);
          gradient.addColorStop(0, "rgba(75, 192, 192, 0.4)");
          gradient.addColorStop(1, "rgba(75, 192, 192, 0)");

          new Chart(ctx, {
            type: "line",
            data: {
              labels,
              datasets: [{
                label,
                data: values,
                borderColor: "rgba(54, 162, 235, 1)",
                backgroundColor: gradient,
                fill: true,
                tension: 0.3
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: { legend: { display: true } }
            }
          });
        }
      }

      if (method === "graph" || method === "both") {
        const graphCanvas = document.getElementById(`modalGraph_${index + 1}`);
        if (graphCanvas && graphCanvas.dataset.rendered !== "true") {
          graphCanvas.dataset.rendered = "true";
          const ctx = graphCanvas.getContext("2d");

          new Chart(ctx, {
            type: "bar",
            data: {
              labels,
              datasets: [{
                label,
                data: values,
                backgroundColor: "rgba(255, 99, 132, 0.6)",
                borderColor: "rgba(255, 99, 132, 1)",
                borderWidth: 1
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: { legend: { display: true } }
            }
          });
        }
      }
    });
  });
});
