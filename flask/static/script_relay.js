// Varible pour la boucle de mise à jour
var update_time = 1000; // 1 seconde

// Au chargement de la page
document.addEventListener('DOMContentLoaded', (event) => {
  

  // Select all input elements on the page
  const inputs = document.querySelectorAll('input');

  // Add event listener to each input element
  inputs.forEach(input => {
      input.addEventListener('input', handleInputChange);
  });

  updatePage();
  
});

// Function to handle input changes
function handleInputChange(event) {
  const name = event.target.name;
  const checked = event.target.checked;
  let etat_switch = {};

  if(name.includes("au_")){
    if(name === 'au_ob'){
      $("#au_pr").prop('checked', false);
      $("#au_co").prop('checked', false);
      $("#au_ma").prop('checked', false);
      etat_switch[name] = checked;
      Object.assign(etat_switch, { name: checked });
      Object.assign(etat_switch, { "au_pr": false });
      Object.assign(etat_switch, { "au_co": false });
      Object.assign(etat_switch, { "au_ma": false });
    }else if(name === 'au_pr'){
      $("#au_co").prop('checked', false);
      $("#au_ob").prop('checked', false);
      $("#au_ma").prop('checked', false);
      etat_switch[name] = checked;
      Object.assign(etat_switch, { "au_co": false });
      Object.assign(etat_switch, { "au_ob": false });
      Object.assign(etat_switch, { "au_ma": false });
    }else if(name === 'au_co'){
      $("#au_pr").prop('checked', false);
      $("#au_ob").prop('checked', false);
      $("#au_ma").prop('checked', false);
      etat_switch[name] = checked;
      Object.assign(etat_switch, { "au_pr": false });
      Object.assign(etat_switch, { "au_ob": false });
      Object.assign(etat_switch, { "au_ma": false });
    }else if(name === 'au_ma'){
      $("#au_pr").prop('checked', false);
      $("#au_ob").prop('checked', false);
      $("#au_co").prop('checked', false);
      etat_switch[name] = checked;
      Object.assign(etat_switch, { "au_pr": false });
      Object.assign(etat_switch, { "au_ob": false });
      Object.assign(etat_switch, { "au_co": false });

      $("#rs_01").prop('checked', true);
      $("#rs_02").prop('checked', true);
      $("#rs_03").prop('checked', false);
      $("#rs_04").prop('checked', false);

      Object.assign(etat_switch, { "rs_01": true });
      Object.assign(etat_switch, { "rs_02": true });
      Object.assign(etat_switch, { "rs_03": false });
      Object.assign(etat_switch, { "rs_04": false });
    }
    
    if($("#au_co").prop("checked") === false && $("#au_pr").prop("checked") === false && $("#au_ma").prop("checked") === false && $("#au_ob").prop("checked") === false){
      $("#au_ob").prop('checked', true);
      Object.assign(etat_switch, { "au_ob": true });
      Object.assign(etat_switch, { "au_pr": false });
      Object.assign(etat_switch, { "au_co": false });
      Object.assign(etat_switch, { "au_ma": false });
    }
    
  }else{
    etat_switch[name] = checked;
  }

  textEtatChexbox(name, checked);
  // Envoie les valeurs au socket
  const jsonString = JSON.stringify(etat_switch);
  socket.send(jsonString);
}

// Function qui change le text de l'état du relais entre ouvert ou fermé
function textEtatChexbox(name, checked) {
  const etat_text = document.querySelectorAll('h3');
  for (let i = 0; i < etat_text.length; i++) {
    let mainString = etat_text[i].id
    if (mainString.includes(name)) {
      if(checked === true){
        etat_text[i].textContent = 'Etat close'
      }else{
        etat_text[i].textContent = 'Etat open'
      }
    }  
  }

}


// Function pour mettre à jour les varibles de la page toute les seconde
function updatePage() {
  setInterval(function () {
    // Envoi à socket un message pour faire une mise à jour des valeurs 
    socket.send("up_relay");
    // Reçois les valeurs du socket
    socket.on('message', function(msg) {
      if (msg != null) {
        if(msg.includes("rs_0")){
          myObj = JSON.parse(msg);
          if (Object.keys(myObj).length > 1){
            const etat_switch = document.querySelectorAll('input');
            const etat_text = document.querySelectorAll('h3');
            for (let i = 0; i < etat_switch.length; i++) {
              etat_switch[i].checked = myObj[etat_switch[i].name]
              textEtatChexbox(etat_switch[i].name, etat_switch[i].checked);
            }
            
          }
          $("#etatSyteme").text(myObj["message"])
        }
      }
    });
  }, (update_time));
}

