// Varible pour la boucle de mise à jour
var update_time = 1000; // 1 seconde

var myObj = null

var voltage = 0.0;
var voltage_gauge = 11.0;
var current = 0.0;
var power = 0.0;

var temp = -50.0;
var humi = 0.0;


var value_precision = 2;

var min_gauge = 11;
var max_gauge  = 14;
var anim_gauge = 32;

var min_Temp = -50;
var max_Temp  = 150;
var min_Humi = 0;
var max_Humi  = 100;

document.addEventListener("DOMContentLoaded", () => {
  drawChart();
});

function createGaugeOptions(labels, zones, divison, subDivisions) {
  return {
    colorStart: "#6fadcf",
    colorStop: void 0,
    gradientType: 0,
    strokeColor: "#e0e0e0",
    generateGradient: true,
    percentColors: [[0.0, "#a9d70b"], [0.50, "#f9c802"], [1.0, "#ff0000"]],
    pointer: {
      length: 0.6,
      strokeWidth: 0.035,
      iconScale: 1.0,
      color: '#ffffff'
    },
    staticLabels: {
      font: "10px sans-serif",
      labels: labels,
      fractionDigits: 0,
      color: '#ffffff'
    },
    staticZones: zones,
    renderTicks: {
      divisions: divison,
      divWidth: 1.1,
      divLength: 0.3,
      divColor: "#333333",
      subDivisions: subDivisions,
      subLength: 0.2,
      subWidth: 0.6,
      subColor: "#666666"
    },
    angle: 0.15,
    lineWidth: 0.44,
    radiusScale: 1.0,
    fontSize: 30,
    limitMax: false,
    limitMin: false,
    highDpiSupport: true
  };
}

// Pour les gauge et la mise à jour des variables du multimètre
function drawChart() {
  
  var opts_voltage = createGaugeOptions(
    [11, 12, 13, 14],
    [
      {strokeStyle: "#FF0000", min: 11, max: 11.9},
      {strokeStyle: "#FFDD00", min: 11.9, max: 12.4},
      {strokeStyle: "#30B32D", min: 12.4, max: 14}
    ],
    6, 
    5
  );

  var opts_temp = createGaugeOptions(
    [-50, -25, 0, 25, 50, 75, 100, 125, 150],
    [
      {strokeStyle: "#2600ffff", min: -50, max: 0},
      {strokeStyle: "#00ff22ff", min: 0, max: 90},
      {strokeStyle: "#ff0000ff", min: 90, max: 150}
    ],
    8, 
    5
  );

  var opts_humi = createGaugeOptions(
    [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    [
      {strokeStyle: "#d9ff00ff", min: 0, max: 30},
      {strokeStyle: "#00ff00ff", min: 30, max: 70},
      {strokeStyle: "#30B32D", min: 70, max: 100}
    ],
    10, 
    10
  );
 

  var target_01 = document.getElementById('chart_Tension_01'); 
  var gauge_01 = new Gauge(target_01).setOptions(opts_voltage);
  gauge_01.maxValue = max_gauge;
  gauge_01.setMinValue(min_gauge); 
  gauge_01.animationSpeed = anim_gauge

  var target_02 = document.getElementById('chart_Tension_02'); 
  var gauge_02 = new Gauge(target_02).setOptions(opts_voltage);
  gauge_02.maxValue = max_gauge;
  gauge_02.setMinValue(min_gauge); 
  gauge_02.animationSpeed = anim_gauge

  var target_03 = document.getElementById('chart_Tension_03'); 
  var gauge_03 = new Gauge(target_03).setOptions(opts_voltage);
  gauge_03.maxValue = max_gauge;
  gauge_03.setMinValue(min_gauge); 
  gauge_03.animationSpeed = anim_gauge

  var target_04 = document.getElementById('chart_Tension_04'); 
  var gauge_04 = new Gauge(target_04).setOptions(opts_voltage);
  gauge_04.maxValue = max_gauge;
  gauge_04.setMinValue(min_gauge); 
  gauge_04.animationSpeed = anim_gauge

  var target_Tremp = document.getElementById('chart_Temp'); 
  var gauge_Temp = new Gauge(target_Tremp).setOptions(opts_temp);
  gauge_Temp.maxValue = max_Temp;
  gauge_Temp.setMinValue(min_Temp); 
  gauge_Temp.animationSpeed = anim_gauge

  var target_Humi = document.getElementById('chart_Humi'); 
  var gauge_Humi = new Gauge(target_Humi).setOptions(opts_humi);
  gauge_Humi.maxValue = max_Humi;
  gauge_Humi.setMinValue(min_Humi); 
  gauge_Humi.animationSpeed = anim_gauge


  // Pour mettre à jour des valeurs de la page et des gauges toute les seconde
  setInterval(function () {
    // Envoi à socket un message pour faire une mise à jour des valeurs 
    socket.send("up_bat");
    // Reçois les valeurs du socket
    socket.on('message', function(msg) {
      if (msg != null) {
        if(msg.includes("bat_")){
          // Transforme le message en dictionaire
          myObj = JSON.parse(msg);

          // Met à jour la gauge N°1
          voltage = Number(myObj.bat_psu_voltage_01).toFixed(value_precision);
          voltage_gauge = voltage;
          current = Number(myObj.bat_current_01).toFixed(value_precision);
          power = Number(myObj.bat_power_01).toFixed(value_precision);
          checkValue();

          gauge_01.set(voltage_gauge);
          $("#psu_voltage_01").text( voltage + " V");
          $("#current_01").text(current + " A");
          $("#power_01").text(power + " W");
          
          // Met à jour la gauge N°2
          voltage = Number(myObj.bat_psu_voltage_02).toFixed(value_precision);
          voltage_gauge = voltage;
          current = Number(myObj.bat_current_02).toFixed(value_precision);
          power = Number(myObj.bat_power_02).toFixed(value_precision);
          checkValue();

          gauge_02.set(voltage_gauge);
          $("#psu_voltage_02").text( voltage + " V");
          $("#current_02").text( current + " A");
          $("#power_02").text( power + " W");

          // Met à jour la gauge N°3
          voltage = Number(myObj.bat_psu_voltage_03).toFixed(value_precision);
          voltage_gauge = voltage;
          current = Number(myObj.bat_current_03).toFixed(value_precision);
          power = Number(myObj.bat_power_03).toFixed(value_precision);
          checkValue();

          gauge_03.set(voltage_gauge);
          $("#psu_voltage_03").text( voltage + " V");
          $("#current_03").text( current + " A");
          $("#power_03").text( power + " W");
          
          // Met à jour la gauge N°4
          voltage = Number(myObj.bat_psu_voltage_04).toFixed(value_precision);
          voltage_gauge = voltage;
          current = Number(myObj.bat_current_04).toFixed(value_precision);
          power = Number(myObj.bat_power_04).toFixed(value_precision);
          checkValue();

          gauge_04.set(voltage_gauge);
          $("#psu_voltage_04").text( voltage + " V");
          $("#current_04").text( current + " A");
          $("#power_04").text( power + " W");
          
          // Met à jour la gauge température
          temp = Number(myObj.temp).toFixed(value_precision);
          value_gauge = temp;

          gauge_Temp.set(value_gauge);
          $("#temp_value").text( temp + " °C");

          // Met à jour la gauge humidité
          humi = Number(myObj.humi).toFixed(value_precision);
          value_gauge = humi;

          gauge_Humi.set(value_gauge);
          $("#humi_value").text( humi + " %");


          if(myObj["au_ob"] === true){
            $("#selectMode").text('Observateur')
          }else if(myObj["au_pr"] === true){
            $("#selectMode").text('Protection')
          }else if(myObj["au_co"] === true){
            $("#selectMode").text('Consomation')
          }else if(myObj["au_ma"] === true){
            $("#selectMode").text('Manuel')
          }
          $("#etatSyteme").text(myObj["message"])
        }
      }
    });
  }, (update_time));
}

function checkValue() {
  if(voltage < 1.0){
    voltage = 0.0.toFixed(value_precision);
    voltage_gauge = min_gauge.toFixed(value_precision);
    current = 0.0.toFixed(value_precision);
    power = 0.0.toFixed(value_precision);
  } else if (voltage > 14) {
    voltage_gauge = max_gauge.toFixed(value_precision);
  } 
}