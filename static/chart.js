{% extends "base.html" %}
{% block title %}月間廃棄数量グラフ{% endblock %}
{% block content %}
<h1>月間廃棄数量グラフ</h1>
<!-- データ確認用の表示 -->
<p>Months: {{ months|tojson }}</p>
<p>Quantities: {{ quantities|tojson }}</p>
<canvas id="myChart" style="width: 100%; height: 400px;"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    const ctx = document.getElementById('myChart').getContext('2d');
    // デバッグ用コンソールログ
    console.log("Months:", {{ months| tojson }});
    console.log("Quantities:", {{ quantities| tojson }});
    // データがある場合のみグラフを描画
    if ({{ quantities | length }} > 0) {
        const myChart = new Chart(ctx, {
            type: 'bar', // グラフの種類
            data: {
                labels: {{ months| tojson }}, // 月ごとのラベル
    datasets: [{
        label: '廃棄数量',
        data: {{ quantities| tojson }}, // 廃棄数量データ
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
        } else {
        console.log("廃棄数量データがありません。");
    }
</script>
{% endblock %}