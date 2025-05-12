// Varible pour la boucle de mise à jour
var update_time = 1000; // 1 seconde

var myObj = null

var voltage = 0.0;
var voltage_gauge = 11.0;
var current = 0.0;
var power = 0.0;

var value_precision = 2;

var min_gauge = 11;
var max_gauge  = 14;
var anim_gauge = 32;

document.addEventListener("DOMContentLoaded", () => {
  drawChart();
});


// Pour les gauge et la mise à jour des variables du multimètre
function drawChart() {

  // Variable pour les options des gauges 
  var opts = {
    // color configs
    colorStart: "#6fadcf",
    colorStop: void 0,
    gradientType: 0,
    strokeColor: "#e0e0e0",
    generateGradient: true,
    percentColors: [[0.0, "#a9d70b" ], [0.50, "#f9c802"], [1.0, "#ff0000"]],
    // customize pointer
    pointer: {
      length: 0.6,
      strokeWidth: 0.035,
      iconScale: 1.0,
      color: '#ffffff'
    },
    // static labels
    staticLabels: {
      font: "10px sans-serif",
      labels: [11, 12, 13, 14],
      fractionDigits: 0,
      color: '#ffffff'

    },
    // static zones
    staticZones: [
      {strokeStyle: "#FF0000", min: 11, max: 11.9},
      {strokeStyle: "#FFDD00", min: 11.9, max: 12.4},
      {strokeStyle: "#30B32D", min: 12.4, max: 14.0},
    ],
    // render ticks
    renderTicks: {
      divisions: 6,
      divWidth: 1.1,
      divLength: 0.3,
      divColor: "#333333",
      subDivisions: 5,
      subLength: 0.2,
      subWidth: 0.6,
      subColor: "#666666"
    },
    // the span of the gauge arc
    angle: 0.15,
    // line thickness
    lineWidth: 0.44,
    // radius scale
    radiusScale: 1.0,
    // font size
    fontSize: 30,
    // if false, max value increases automatically if value > maxValue
    limitMax: false,
    // if true, the min value of the gauge will be fixed
    limitMin: false,
    // High resolution support
    highDpiSupport: true
  };


  var target_01 = document.getElementById('chart_Tension_01'); 
  var gauge_01 = new Gauge(target_01).setOptions(opts);
  gauge_01.maxValue = max_gauge;
  gauge_01.setMinValue(min_gauge); 
  gauge_01.animationSpeed = anim_gauge

  var target_02 = document.getElementById('chart_Tension_02'); 
  var gauge_02 = new Gauge(target_02).setOptions(opts);
  gauge_02.maxValue = max_gauge;
  gauge_02.setMinValue(min_gauge); 
  gauge_02.animationSpeed = anim_gauge

  var target_03 = document.getElementById('chart_Tension_03'); 
  var gauge_03 = new Gauge(target_03).setOptions(opts);
  gauge_03.maxValue = max_gauge;
  gauge_03.setMinValue(min_gauge); 
  gauge_03.animationSpeed = anim_gauge

  var target_04 = document.getElementById('chart_Tension_04'); 
  var gauge_04 = new Gauge(target_04).setOptions(opts);
  gauge_04.maxValue = max_gauge;
  gauge_04.setMinValue(min_gauge); 
  gauge_04.animationSpeed = anim_gauge


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