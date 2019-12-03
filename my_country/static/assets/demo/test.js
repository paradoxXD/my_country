test = {
    initlounge: function(new_data,new_label){
    

        
      // charts
      gradientChartOptionsConfigurationWithTooltipPurple = {
        maintainAspectRatio: false,
        legend: {
          display: false
        },
        bezierCurve: false,
        tooltips: {
          backgroundColor: '#f5f5f5',
          titleFontColor: '#333',
          bodyFontColor: '#666',
          bodySpacing: 4,
          xPadding: 12,
          mode: "nearest",
          intersect: 0,
          position: "nearest"
        },
        responsive: true,
        scales: {
          yAxes: [{
            barPercentage: 1.6,
            gridLines: {
              drawBorder: false,
              color: 'rgba(29,140,248,0.0)',
              zeroLineColor: "transparent",
            },
            ticks: {
              // suggestedMin: 60,
              // suggestedMax: 125,
              padding: 20,
              fontColor: "#9a9a9a"
            }
          }],
  
          xAxes: [{
            barPercentage: 1.6,
            gridLines: {
              drawBorder: false,
              color: 'rgba(225,78,202,0.1)',
              zeroLineColor: "transparent",
            },
            ticks: {
              padding: 20,
              fontColor: "#9a9a9a"
            }
          }]
        }
      };
        
      
      var chart_labels = new_label;
      var week_data = new_data;

      
      var ctx = document.getElementById("chartBig2").getContext('2d');

      var gradientStroke = ctx.createLinearGradient(0, 230, 0, 50);

      gradientStroke.addColorStop(1, 'rgba(72,72,176,0.1)');
      gradientStroke.addColorStop(0.4, 'rgba(72,72,176,0.0)');
      gradientStroke.addColorStop(0, 'rgba(119,52,169,0)'); //purple colors

      var config = {
        type: 'line',
        data: {
          labels: chart_labels,
          datasets: [{
            label: "Stock Price",
            fill: true,
            backgroundColor: gradientStroke,
            lineTension: 0,
            borderColor: '#d346b1',
            borderWidth: 2,
            borderDash: [],
            borderDashOffset: 0.0,
            pointBackgroundColor: '#d346b1',
            pointBorderColor: 'rgba(255,255,255,0)',
            pointHoverBackgroundColor: '#d346b1',
            pointBorderWidth: 20,
            pointHoverRadius: 4,
            pointHoverBorderWidth: 15,
            pointRadius: 4,
            data: week_data,
          },{
            label: "Predicted Price",
            fill: true,
            backgroundColor: gradientStroke,
            lineTension: 0,
            borderColor: '#ff8a76',
            borderWidth: 2,
            borderDash: [],
            borderDashOffset: 0.0,
            pointBackgroundColor: '#ff8a76',
            pointBorderColor: 'rgba(255,255,255,0)',
            pointHoverBackgroundColor: '#ff8a76',
            pointBorderWidth: 20,
            pointHoverRadius: 4,
            pointHoverBorderWidth: 15,
            pointRadius: 4,
            data: [10,10,10,10,10,10,10],
          }]
        },
        options: gradientChartOptionsConfigurationWithTooltipPurple
    };
    var myChartData = new Chart(ctx, config);



    this.update_data = function(new_data,sql_label,Predicted){
      week_data = new_data;
      var data = myChartData.config.data;
      data.datasets[0].data = week_data;
      data.datasets[1].data = Predicted;
      data.labels = sql_label;
      myChartData.update();
    }

  
    this.update_point_size= function(size){
      var data = myChartData.config.data;
      data.datasets[0].pointRadius = size;
    }

    this.update_point_size_pre= function(size){
      var data = myChartData.config.data;
      data.datasets[1].pointRadius = size;
    }


  }
}