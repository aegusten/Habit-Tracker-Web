document.addEventListener("DOMContentLoaded", function () {
  const chartData = JSON.parse(document.getElementById("chart-data").textContent || "[]");
  const fields = JSON.parse(document.getElementById("chart-fields").textContent || "[]");

  const labels = chartData.map(row => row.date);
  const selectedFields = (fields.length === 1) ? fields : [fields[0]];

  const datasets = selectedFields.map(field => ({
    label: field.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
    data: chartData.map(row => row[field] || 0),
    borderColor: 'rgba(75, 192, 192, 1)',
    backgroundColor: 'rgba(75, 192, 192, 0.2)',
    tension: 0.2,
    fill: true
  }));

  const habitChartCanvas = document.getElementById("habitChart");
  if (habitChartCanvas) {
    const ctx = habitChartCanvas.getContext("2d");
    new Chart(ctx, {
      type: "line",
      data: { labels, datasets },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: false },
          x: { ticks: { autoSkip: true, maxTicksLimit: 10 } }
        }
      }
    });
  }

  setTimeout(() => {
    document.querySelectorAll(".alert").forEach(alert => {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    });
  }, 4000);
});
