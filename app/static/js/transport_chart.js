let chartInstance = null;

function loadChart(view = 'monthly') {
  fetch(`/transport_chart_data?view=${view}`)
    .then(res => res.json())
    .then(data => {
      const ctx = document.getElementById('transportChart').getContext('2d');
      if (chartInstance) chartInstance.destroy();

      chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: data.labels,
          datasets: [
            {
              label: 'Revenue (DIN)',
              data: data.fee_values,
              backgroundColor: 'rgba(54, 162, 235, 0.9)',
              yAxisID: 'y'
            },
            {
              label: 'Quantity delivered (kg)',
              data: data.amount_values,
              type: 'bar',
              borderColor: 'rgba(255, 159, 64, 1)',
              backgroundColor: 'rgba(255, 159, 64, 0.7)',
              yAxisID: 'y2'
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
          },
          scales: {
            y: {
              beginAtZero: true,
              position: 'left',
              title: { display: true, text: 'Revenue' }
            },
            y2: {
              beginAtZero: true,
              position: 'right',
              grid: { drawOnChartArea: false },
              title: { display: true, text: 'Quantity delivered' }
            },
            x: {
              title: { display: true, text: view === "monthly" ? 'Month' : 'Last week' }
            }
          }
        }
      });
    });
}

document.getElementById('chartViewSelector').addEventListener('change', (e) => {
  loadChart(e.target.value);
});

loadChart();
