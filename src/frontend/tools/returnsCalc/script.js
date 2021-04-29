google.charts.load('44', {
  callback: calc,
  packages: ['corechart']
});

// Standard Normal variate using Box-Muller transform.
// returns a gaussian random function with the given mean and stdev.
function gaussian(mean, stdev) {
  var y2;
  var use_last = false;
  return function() {
    var y1;
    if (use_last) {
      y1 = y2;
      use_last = false;
    } else {
      var x1, x2, w;
      do {
        x1 = 2.0 * Math.random() - 1.0;
        x2 = 2.0 * Math.random() - 1.0;
        w = x1 * x1 + x2 * x2;
      } while (w >= 1.0);
      w = Math.sqrt((-2.0 * Math.log(w)) / w);
      y1 = x1 * w;
      y2 = x2 * w;
      use_last = true;
    }

    return mean + stdev * y1;
  }
}

function calc() {
  var expectedReturn = parseFloat(document.getElementById("expectedReturn").value);
  var stdDeviation = parseFloat(document.getElementById("stdDeviation").value);
  var years = parseInt(document.getElementById("years").value);
  var value = parseFloat(document.getElementById("value").value);

  var dataInput = [];
  var returnsInput = [];
  var high = value;
  var low = value;
  var gaussianFunction = gaussian(expectedReturn, stdDeviation);
  var percentReturn = 0;
  for (var i = 0; i <= years; ++i) {
    var curr = [];
    curr.push(i);
    curr.push(value);
    curr.push(high);
    curr.push(low);
    dataInput.push(curr);

    var currReturns = [];
    currReturns.push(i);
    currReturns.push(percentReturn);
    returnsInput.push(currReturns);

    // Next year
    percentReturn = gaussianFunction();
    value = value * (1 + percentReturn);
    high = Math.max(high, value);
    low = Math.min(low, value);
  }

  var data = new google.visualization.DataTable();
  data.addColumn('number', 'Year');
  data.addColumn('number', 'Value');
  data.addColumn('number', 'High');
  data.addColumn('number', 'Low');

  data.addRows(dataInput);


  var returnsData = new google.visualization.DataTable();
  returnsData.addColumn('number', 'Year');
  returnsData.addColumn('number', 'returnsInput');

  returnsData.addRows(returnsInput);

  var options = {
    hAxis: {
      title: 'Year'
    },
    vAxis: {
      title: 'Value'
    },
    backgroundColor: '#f1f8e9'
  };

  var returnsOptions = {
    hAxis: {
      title: 'Year'
    },
    vAxis: {
      title: 'Return'
    },
    backgroundColor: '#f1f8e9'
  };
  var chart = new google.visualization.LineChart(document.getElementById('NominalGraph'));
  chart.draw(data, options);
  var returnsChart = new google.visualization.LineChart(document.getElementById('ReturnsGraph'));
  returnsChart.draw(returnsData, returnsOptions);
}