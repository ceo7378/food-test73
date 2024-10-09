<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>月間廃棄数量グラフ</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <h1>月間廃棄数量グラフ</h1>
    <canvas id="myChart"></canvas>
    <script>
        const ctx = document.getElementById('myChart').getContext('2d');
        const myChart = new Chart(ctx, {
            type: 'bar', // グラフの種類
            data: {
                labels: {{ months|tojson }}, // 月ごとのラベル
                datasets: [{
                    label: '廃棄数量',
                    data: {{ quantities|tojson }}, // 廃棄数量データ
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
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
    </script>
</body>
</html>
