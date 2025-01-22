from flask import Flask, render_template_string, jsonify
import psutil

# Initialize Flask app
app = Flask(__name__)

# Fetch system metrics for CPU and memory
def get_system_metrics():
    metrics = {}

    # CPU utilization
    metrics['cpu_utilization'] = psutil.cpu_percent(interval=0.1)

    # Memory utilization
    mem = psutil.virtual_memory()
    metrics['memory_utilization'] = mem.percent
    metrics['memory_total'] = mem.total // (1024 ** 2)  # Convert to MB
    metrics['memory_used'] = mem.used // (1024 ** 2)    # Convert to MB

    return metrics

# Serve the webpage
@app.route('/')
def index():
    # Inline HTML Template
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>System Monitor</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            .card {
                border: 1px solid #ccc;
                padding: 15px;
                margin-bottom: 10px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            .title {
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            .utilization-bar {
                background-color: #f0f0f0;
                border-radius: 5px;
                overflow: hidden;
                margin: 5px 0;
            }
            .utilization-bar div {
                height: 20px;
                line-height: 20px;
                color: white;
                text-align: center;
            }
            .cpu-bar {
                background-color: #4caf50;
            }
            .memory-bar {
                background-color: #2196f3;
            }
        </style>
    </head>
    <body>
        <h1>System Monitor</h1>
        <div id="system-metrics"></div>
        <script>
            async function fetchMetrics() {
                const response = await fetch('/metrics');
                const metrics = await response.json();

                const container = document.getElementById('system-metrics');
                container.innerHTML = '';

                // CPU Metrics
                const cpuCard = document.createElement('div');
                cpuCard.className = 'card';
                cpuCard.innerHTML = `
                    <div class="title">CPU Utilization</div>
                    <div>${metrics.cpu_utilization}%</div>
                    <div class="utilization-bar">
                        <div class="cpu-bar" style="width: ${metrics.cpu_utilization}%;"></div>
                    </div>
                `;
                container.appendChild(cpuCard);

                // Memory Metrics
                const memoryCard = document.createElement('div');
                memoryCard.className = 'card';
                memoryCard.innerHTML = `
                    <div class="title">Memory Utilization</div>
                    <div>${metrics.memory_used} / ${metrics.memory_total} MB (${metrics.memory_utilization}%)</div>
                    <div class="utilization-bar">
                        <div class="memory-bar" style="width: ${metrics.memory_utilization}%;"></div>
                    </div>
                `;
                container.appendChild(memoryCard);
            }

            setInterval(fetchMetrics, 2000); // Refresh every 2 seconds
            fetchMetrics();
        </script>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/metrics')
def metrics():
    return jsonify(get_system_metrics())

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
