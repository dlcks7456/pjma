function pie_chart(id, labels, data, color, label){
  var ctx = document.getElementById(id);
  var myChart = new Chart(ctx, {
      type : 'pie',
      data : {
        labels: labels,
        datasets: [{
          label: label,
          data: data,
          backgroundColor: color,
          hoverOffset: 4
        }]
      }
  });
}


function bar_chart(id, labels, data, color, label){
  var ctx = document.getElementById(id);
  var myChart = new Chart(ctx, {
      type : 'bar',
      data : {
        labels: labels,
        datasets: [{
          label: label,
          data: data,
          backgroundColor: color
        }]
      },
      options: {
        maintainAspectRatio: false,
      }
  });
}

function month_qc_line(id, data1, data2, data3){
    var ctx = document.getElementById(id);
    var data = {
      labels: ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
      type: 'scatter',
      datasets: [{
        type: 'bar',
        label: 'project',
        data: data3,
        backgroundColor: 'rgba(54, 162, 235, 0.3)',
        borderColor: 'rgba(54, 162, 235)',
        borderWidth: 1
      }, {
        type: 'line',
        label: 'Test QC',
        data: data1,
        backgroundColor: 'rgba(153, 102, 255, 0.4)',
        borderColor: 'rgba(153, 102, 255, 0.4)'
      }, {
        type: 'line',
        label: 'Live QC',
        data: data2,
        backgroundColor: 'rgba(255, 99, 132, 0.4)',
        borderColor: 'rgba(255, 99, 132, 0.4)'
      }]
    };
    var mixedChart = new Chart(ctx, {
        type: 'scatter',
        data: data,
        options: {
            title: {
                display: true,
                text: 'Monthly QC (by start)'
            }
        }
    });
}


function month_sample_bar(id, data, total){
    var ctx = document.getElementById(id);
    var data = {
      labels: ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'],
      type: 'scatter',
      datasets: [{
        type: 'bar',
        label: total,
        data: data,
        backgroundColor: 'rgba(75, 192, 192, 0.3)',
        borderColor: 'rgba(75, 192, 192)',
        borderWidth: 1
      }]
    };
    var mixedChart = new Chart(ctx, {
        type: 'scatter',
        data: data,
        options: {
            title: {
                display: true,
                text: 'Monthly Total Sample'
            }
        }
    });
}