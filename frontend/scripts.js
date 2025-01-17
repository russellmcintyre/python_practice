document.getElementById('username-form').addEventListener('submit', async (event) => {
    event.preventDefault();
  
    const username = document.getElementById('username').value;
    const apiUrl = 'https://<your-backend-url>/analyze';
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username }),
    });
  
    const data = await response.json();
    if (data.error) {
      alert(data.error);
      return;
    }
  
    // Update totals
    document.getElementById('weekly-total').innerText = `Weekly Earnings: $${data.weekly_total}`;
    document.getElementById('monthly-total').innerText = `Monthly Earnings: $${data.monthly_total}`;
  
    // Render chart
    renderChart(data.weekday_analysis);
  });
  
  function renderChart(data) {
    const ctx = document.getElementById('earnings-chart').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        datasets: [{
          label: 'Earnings ($)',
          data: Object.values(data),
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
        }],
      },
      options: {
        scales: {
          y: { beginAtZero: true },
        },
      },
    });
  }
  