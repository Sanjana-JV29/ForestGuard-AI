const ctx = document.getElementById('myChart');

if (ctx) {

    // ============================================
    // GET VALUES FROM HTML INPUTS
    // ============================================

    const temp =
        parseFloat(document.querySelector('input[name="temp"]')?.value) || 0;

    const humidity =
        parseFloat(document.querySelector('input[name="RH"]')?.value) || 0;

    const wind =
        parseFloat(document.querySelector('input[name="wind"]')?.value) || 0;

    const rain =
        parseFloat(document.querySelector('input[name="rain"]')?.value) || 0;

    // ============================================
    // CREATE CHART
    // ============================================

    new Chart(ctx, {

        type: 'bar',

        data: {

            labels: [

                'Temperature',

                'Humidity',

                'Wind Speed',

                'Rainfall'
            ],

            datasets: [{

                label: 'Environmental Conditions Analysis',

                data: [

                    temp,

                    humidity,

                    wind,

                    rain
                ],

                backgroundColor: [

                    'rgba(255, 99, 132, 0.7)',

                    'rgba(54, 162, 235, 0.7)',

                    'rgba(255, 206, 86, 0.7)',

                    'rgba(75, 192, 192, 0.7)'
                ],

                borderColor: [

                    'rgba(255, 99, 132, 1)',

                    'rgba(54, 162, 235, 1)',

                    'rgba(255, 206, 86, 1)',

                    'rgba(75, 192, 192, 1)'
                ],

                borderWidth: 2,

                borderRadius: 10
            }]
        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    labels: {

                        color: 'white',

                        font: {

                            size: 14
                        }
                    }
                }
            },

            scales: {

                x: {

                    ticks: {

                        color: 'white',

                        font: {

                            size: 13
                        }
                    },

                    grid: {

                        color: 'rgba(255,255,255,0.1)'
                    }
                },

                y: {

                    beginAtZero: true,

                    ticks: {

                        color: 'white',

                        font: {

                            size: 13
                        }
                    },

                    grid: {

                        color: 'rgba(255,255,255,0.1)'
                    }
                }
            }
        }
    });
}