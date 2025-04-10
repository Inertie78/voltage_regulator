var myObj = null
document.addEventListener("DOMContentLoaded", () => {
  google.charts.load('current', { 'packages': ['gauge'] });
  google.charts.setOnLoadCallback(drawChart);

});

function drawChart() {

  var chartTension_01 = new google.visualization.Gauge(document.getElementById("chart_Tension_01"));
  var chartTension_02 = new google.visualization.Gauge(document.getElementById("chart_Tension_02"));
  var chartTension_03 = new google.visualization.Gauge(document.getElementById("chart_Tension_03"));
  var chartTension_04 = new google.visualization.Gauge(document.getElementById("chart_Tension_04"));

  var dataTension_01 = google.visualization.arrayToDataTable([
    ['Label', 'Value'],
    ['Tens', 0]
  ]);

  var dataTension_02 = google.visualization.arrayToDataTable([
    ['Label', 'Value'],
    ['Tens', 0]
  ]);

  var dataTension_03 = google.visualization.arrayToDataTable([
    ['Label', 'Value'],
    ['Tens', 0]
  ]);

  var dataTension_04 = google.visualization.arrayToDataTable([
    ['Label', 'Value'],
    ['Tens', 0]
  ]);

  var optionsTension = {
    width: 150, height: 150,
    min: 7, max: 14,
    redFrom: 11.4, redTo: 11.9,
    yellowFrom: 11.9, yellowTo: 12.4,
    greenFrom: 12.4, greenTo: 12.8,
    majorTicks: ['7', '8', '9', '10', '11', '12', '13', '14'],
    minorTicks: 5
  };

  var formatTension = new google.visualization.NumberFormat({
    suffix: ' V',
    fractionDigits: 1
  });

  
  formatTension.format(dataTension_01, 1);
  chartTension_01.draw(dataTension_01, optionsTension);
  formatTension.format(dataTension_02, 1);
  chartTension_02.draw(dataTension_02, optionsTension);
  formatTension.format(dataTension_03, 1);
  chartTension_03.draw(dataTension_03, optionsTension);
  formatTension.format(dataTension_04, 1);
  chartTension_04.draw(dataTension_04, optionsTension);

  setInterval(function () {
    socket.send("up_bat");
    socket.on('message', function(msg) {
      if (msg != null) {
        if(msg.includes("bat_")){
          myObj = JSON.parse(msg);
          var voltage = Number(myObj.bat_psu_voltage_01).toFixed(3)
          formatTension.format(dataTension_01, 1);
          $("#shunt_voltage_01").text( voltage + " V");
          dataTension_01.setValue(0, 1, voltage);
          chartTension_01.draw(dataTension_01, optionsTension);
          $("#current_01").text( Number(myObj.bat_current_01).toFixed(3) + " A");
          $("#power_01").text( Number(myObj.bat_power_01).toFixed(3) + " W");
          
          voltage = Number(myObj.bat_psu_voltage_02).toFixed(3)
          formatTension.format(dataTension_02, 1);
          $("#shunt_voltage_02").text( voltage + " V");
          dataTension_02.setValue(0, 1, voltage);
          chartTension_02.draw(dataTension_02, optionsTension);
          $("#current_02").text( Number(myObj.bat_current_02).toFixed(3) + " A");
          $("#power_02").text( Number(myObj.bat_power_02).toFixed(3) + " W");

          voltage = Number(myObj.bat_psu_voltage_03).toFixed(3)
          formatTension.format(dataTension_03, 1);
          $("#shunt_voltage_03").text( voltage + " V");
          dataTension_03.setValue(0, 1, voltage);
          chartTension_03.draw(dataTension_03, optionsTension);
          $("#current_03").text( Number(myObj.bat_current_03).toFixed(3) + " A");
          $("#power_03").text( Number(myObj.bat_power_03).toFixed(3) + " W");
          
          voltage = Number(myObj.bat_psu_voltage_04).toFixed(3)
          formatTension.format(dataTension_04, 1);
          $("#shunt_voltage_04").text( voltage + " V");
          dataTension_04.setValue(0, 1, voltage);
          chartTension_04.draw(dataTension_04, optionsTension);
          $("#current_04").text( Number(myObj.bat_current_04).toFixed(3) + " A");
          $("#power_04").text( Number(myObj.bat_power_04).toFixed(3) + " W");
        }
      }
    });
  }, (1000));
}