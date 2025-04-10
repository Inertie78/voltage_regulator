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

  var dataTension = google.visualization.arrayToDataTable([
    ['Label', 'Value'],
    ['Tens', 11]
  ]);
FULL_CHARGE_TENSION = 12.8
CYCLE_CHARGE_TENSION = 12.4
MIN_CHARGE_TENSION = 11.9
  var optionsTension = {
    width: 150, height: 150,
    min: 11, max: 14,
    redFrom: 11.5, redTo: 11.9,
    yellowFrom: 11.9, yellowTo: 12.4,
    greenFrom: 12.4, greenTo: 12.8,
    majorTicks: ['11', '12', '13', '14'],
    minorTicks: 10
  };

  var formatTension = new google.visualization.NumberFormat({
    suffix: ' V',
    fractionDigits: 1
  });

  
  formatTension.format(dataTension, 1);
  chartTension_01.draw(dataTension, optionsTension);
  chartTension_02.draw(dataTension, optionsTension);
  chartTension_03.draw(dataTension, optionsTension);
  chartTension_04.draw(dataTension, optionsTension);

  setInterval(function () {
    socket.send("up_bat");
    socket.on('message', function(msg) {
      if (msg != null) {
        if(msg.includes("bat_")){
          formatTension.format(dataTension, 1);
          myObj = JSON.parse(msg);
          var voltage = Number(myObj.bat_psu_voltage_01).toFixed(3)
          $("#shunt_voltage_01").text( voltage + " V");
          dataTension.setValue(0, 1, voltage);
          chartTension_01.draw(dataTension, optionsTension);
          $("#current_01").text( Number(myObj.bat_current_01).toFixed(3) + " A");
          $("#power_01").text( Number(myObj.bat_power_01).toFixed(3) + " W");
          
          voltage = Number(myObj.bat_psu_voltage_02).toFixed(3)
          $("#shunt_voltage_02").text( voltage + " V");
          dataTension.setValue(0, 1, voltage);
          chartTension_02.draw(dataTension, optionsTension);
          $("#current_02").text( Number(myObj.bat_current_02).toFixed(3) + " A");
          $("#power_02").text( Number(myObj.bat_power_02).toFixed(3) + " W");

          voltage = Number(myObj.bat_psu_voltage_03).toFixed(3)
          $("#shunt_voltage_03").text( voltage + " V");
          dataTension.setValue(0, 1, voltage);
          chartTension_03.draw(dataTension, optionsTension);
          $("#current_03").text( Number(myObj.bat_current_03).toFixed(3) + " A");
          $("#power_03").text( Number(myObj.bat_power_03).toFixed(3) + " W");
          
          voltage = Number(myObj.bat_psu_voltage_04).toFixed(3)
          $("#shunt_voltage_04").text( voltage + " V");
          dataTension.setValue(0, 1, voltage);
          chartTension_04.draw(dataTension, optionsTension);
          $("#current_04").text( Number(myObj.bat_current_04).toFixed(3) + " A");
          $("#power_04").text( Number(myObj.bat_power_04).toFixed(3) + " W");
        }
      }
    });

      
      

      
      
      

      


  }, (1000));
}
