document.addEventListener("DOMContentLoaded", () => {
  socket.send("up_bat");
  socket.on('message', function(msg) {
    if (msg != null) {
      if(msg.includes("bat_")){
        myObj = JSON.parse(msg);
        $("#bus_voltage_01").text(myObj.bat_bus_voltage_01.toFixed(4) + " V");
        $("#shunt_voltage_01").text(myObj.bat_shunt_voltage_01.toFixed(4) + " V");
        $("#current_01").text(myObj.bat_current_01.toFixed(4) + " A");
        $("#power_01").text(myObj.bat_power_01.toFixed(4) + " W");
        
        $("#bus_voltage_02").text(myObj.bat_bus_voltage_02.toFixed(4) + " V");
        $("#shunt_voltage_02").text(myObj.bat_shunt_voltage_02.toFixed(4) + " V");
        $("#current_02").text(myObj.bat_current_02.toFixed(4) + " A");
        $("#power_02").text(myObj.bat_power_02.toFixed(4) + " W");

        $("#bus_voltage_03").text(myObj.bat_bus_voltage_03.toFixed(4) + " V");
        $("#shunt_voltage_03").text(myObj.bat_shunt_voltage_03.toFixed(4) + " V");
        $("#current_03").text(myObj.bat_current_03.toFixed(4) + " A");
        $("#power_03").text(myObj.bat_power_03.toFixed(4) + " W");
        
        $("#bus_voltage_04").text(myObj.bat_bus_voltage_04.toFixed(4) + " V");
        $("#shunt_voltage_04").text(myObj.bat_shunt_voltage_04.toFixed(4) + " V");
        $("#current_04").text(myObj.bat_current_04.toFixed(4) + " A");
        $("#power_04").text(myObj.bat_power_04.toFixed(4) + " W");
      }
    }
  });
});