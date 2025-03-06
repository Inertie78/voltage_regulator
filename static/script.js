const monthNames = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
  "Jullet", "Août", "Septembre", "Octobre", "Novembre", "D&eacute;cembre"
];

var year;
var month;
var jour;

document.addEventListener("DOMContentLoaded", () => {

  google.charts.load('current', { 'packages': ['gauge'] });
  google.charts.setOnLoadCallback(drawChart);

  setInterval(myTimer, (1000));
});

function myTimer() {
  now = new Date();
  year = now.getFullYear();
  month = now.getMonth();

  jour    = ('0'+now.getDate()   ).slice(-2);

  document.getElementById("current_date").innerHTML = jour + "   " + monthNames[month] + "   " + year;
  document.getElementById("current_time").innerHTML = now.toLocaleTimeString();
}

function drawChart() {

  var chartTension = new google.visualization.Gauge(document.getElementById("chart_Tension"));
  var chartTemp = new google.visualization.Gauge(document.getElementById("chart_Temp"));

  var dataTension = google.visualization.arrayToDataTable([
    ['Label', 'Value'],
    ['Tens', 0]
  ]);

  var dataTemp = google.visualization.arrayToDataTable([
    ['Label', 'Value'],
    ['Temp', 0]
  ]);

  var optionsTension = {
    width: 100, height: 100,
    redFrom: 80, redTo: 100,
    yellowFrom: 0, yellowTo: 50,
    greenFrom: 50, greenTo: 80,
    majorTicks: ['5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'],
    minorTicks: 10
  };

  var formatTension = new google.visualization.NumberFormat({
    suffix: ' V',
    fractionDigits: 1
  });
  formatTension.format(dataTension, 1);

  var optionsTemp = {
    width: 100, height: 100,
    redFrom: 30, redTo: 100,
    yellowFrom: 0, yellowTo: 25,
    greenFrom: 25, greenTo: 30,
    majorTicks: ['0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100'],
    minorTicks: 10
  };

  var formatTemp = new google.visualization.NumberFormat({
    suffix: ' C',
    fractionDigits: 1
  });
  formatTemp.format(dataTemp, 1);

  chartTension.draw(dataTension, optionsTension);
  chartTemp.draw(dataTemp, optionsTemp);

  setInterval(function () {
    if(dataGPIO != null){
      dataTension.setValue(0, 1, dataGPIO.h);
      formatHumid.format(dataTension, 1);
      chartHumid.draw(dataTension, optionsTension);
    }
  }, (1000));

  setInterval(function () {
    if(dataGPIO != null){
      dataTemp.setValue(0, 1, dataGPIO.t);
      formatTemp.format(dataTemp, 1);
      chartTemp.draw(dataTemp, optionsTemp);
    }
  }, (1000));
}

function RefreshGraph(jsonTable) {
  var dataTemp = [];
  var dataTens = [];

  var options = {
    zoomEnabled: true,
    theme: "dark2",
    title: {
      text: "Grapigue"
    },
    axisX: {
      title: "Time"
    },
    axisY: {
      title: "Temp C",
      titleFontColor: "#6D78AD",
      lineColor: "#6D78AD",
      gridThickness: 0,
      lineThickness: 1
    },
    legend: {
      verticalAlign: "top",
      fontSize: 22,
      fontColor: "dimGrey"
    },
    data: [{
      type: "line",
      xValueType: "dateTime",
      xValueFormatString: "hh:mm T",
      showInLegend: true,
      name: "Temp",
      dataPoints: dataTemp
    }, {
      type: "line",
      xValueType: "dateTime",
      xValueFormatString: "hh:mm T",
      showInLegend: true,
      name: "Tension",
      axisYType: "secondary",
      dataPoints: dataTens
    }]
  };

  var chart = $("#chartContainer").CanvasJSChart(options);

  for (var i=0; i < jsonTable.length; i++) {
    if(typeof jsonTable[i]['e'] != "undefined"){
      var timeValues = jsonTable[i]['e'];
      const [hours, minutes] = timeValues.split(':');
      const dateCaptu = new Date(year, month, jour, +hours, +minutes);

      
      dataTemp.push({
        x: new Date(dateCaptu),
        y: parseFloat(jsonTable[i]['t'])
      });
      dataTens.push({
        x: new Date(dateCaptu),
        y: parseFloat(jsonTable[i]['h'])
      });
    }
  }

  $("#chartContainer").CanvasJSChart().render();
}
