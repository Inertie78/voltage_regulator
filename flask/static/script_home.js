const monthNames = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
  "Jullet", "Août", "Septembre", "Octobre", "Novembre", "D&eacute;cembre"
];

var year;
var month;
var jour;


var socket = io(adress);

document.addEventListener("DOMContentLoaded", (event) => {
  socket.on('connect', function() {
    socket.send('User has connected!');
  });

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
