const monthNames = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
  "Jullet", "Août", "Septembre", "Octobre", "Novembre", "D&eacute;cembre"
];

var year;
var month;
var jour;

document.addEventListener("DOMContentLoaded", () => {
  updateDataRaspberry();
  setInterval(myTimer, (1000));
  setInterval(updateDataRaspberry, 5000);
});

function myTimer() {
  now = new Date();
  year = now.getFullYear();
  month = now.getMonth();

  jour    = ('0'+now.getDate()   ).slice(-2);

  document.getElementById("current_date").innerHTML = jour + "   " + monthNames[month] + "   " + year;
  document.getElementById("current_time").innerHTML = now.toLocaleTimeString();
}


function updateDataRaspberry() {
  $.getJSON('/flask/updateDataRaspberry', {
    name: "data",
  }, function(data, status, xhr) {
    $("#val_systmeStatus").text(data.status)

    $("#val_Temp").text(data.temp + "°C")
    $("#val_Usage").text(data.usage + "%")
    $("#val_Core").text(data.core + "V")

    $("#val_RamTotal").text(data.ram[0] + "%")
    $("#val_RamUsed").text(data.ram[1] + "G")
    $("#val_RamFree").text(data.ram[2] + "G")
    $("#val_RamTotal").text(data.ram[2] + "G")

    $("#val_DiskPerc").text(data.disk[3] + "%")
    $("#val_DiskUsed").text(data.disk[2] + "G")
    $("#val_DiskFree").text(data.disk[2] + "G")
    $("#val_DiskTotal").text(data.disk[0] + "G")     
  });
}

