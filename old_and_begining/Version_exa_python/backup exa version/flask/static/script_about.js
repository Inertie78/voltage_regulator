document.addEventListener("DOMContentLoaded", () => {
  // Envoi à socket un message pour faire une mise à jour des valeurs 
  socket.send("up_PI");
  // Reçois les valeurs du socket
  socket.on('message', function(msg) {
    if (msg != null) {
      if(msg.includes("cpu_")){
        myObj = JSON.parse(msg);
        $("#val_systmeStatus").text(myObj.sys_stat)
    
        $("#val_Temp").text(myObj.cpu_temp.toFixed(2) + " °C")
        $("#val_Usage").text(myObj.cpu_usage.toFixed(2) + " %")
        $("#val_Core").text(myObj.cpu_volt.toFixed(2) + " V")
    
        $("#val_RamPercent").text(myObj.porcent_disk_ussed.toFixed(2) + " %")
        $("#val_RamUsed").text(myObj.disk_ussed.toFixed(2)+ " G")
        $("#val_RamFree").text(myObj.disk_free.toFixed(2) + " G")
        $("#val_RamTotal").text(myObj.disk_total.toFixed(2) + " G")
    
        $("#val_DiskPerc").text(myObj.porcent_ram_ussed.toFixed(2) + " %")
        $("#val_DiskUsed").text(myObj.ram_ussed.toFixed(2) + " G")
        $("#val_DiskFree").text(myObj.ram_free.toFixed(2) + " G")
        $("#val_DiskTotal").text(myObj.ram_total.toFixed(2) + " G")   
      }
    }
  });

  document.getElementById('raspberryReboot').addEventListener('click', function() {
    $.getJSON('/flask/raspberryReboot', {
    }, function(data, status, xhr) {
        myObj = data.result
    });
  });

  document.getElementById('raspberryShutdown').addEventListener('click', function() {
    $.getJSON('/flask/raspberryShutdown', {
    }, function(data, status, xhr) {
        myObj = data.result
    });
  });
});