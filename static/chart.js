const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'bar', // グラフの種類
    data: {
        labels: {{ labels|safe }}, // Flaskから渡されるラベル
        datasets: [{
            label: '合計金額',
            data: {{ total_amounts|safe }}, // Flaskから渡されるデータ
            backgroundColor: 'rgba(75, 192, 192, 0.2)', // 背景色
            borderColor: 'rgba(75, 192, 192, 1)', // 枠線の色
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});
