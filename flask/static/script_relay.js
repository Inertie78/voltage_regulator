document.addEventListener('DOMContentLoaded', (event) => {
  socket.send("up_relay");
  socket.on('message', function(msg) {
    if (msg != null) {
      if(msg.includes("rs_0")){
        myObj = JSON.parse(msg);
        if (Object.keys(myObj).length > 1){
          const etat_switch = document.querySelectorAll('input');
          const etat_text = document.querySelectorAll('h3');
          for (let i = 0; i < etat_switch.length; i++) {
            etat_switch[i].checked = myObj[etat_switch[i].name]
          }
        }
      }
    }
  });

  // Select all input elements on the page
  const inputs = document.querySelectorAll('input');

  // Function to handle input changes
  function handleInputChange(event) {
    const name = event.target.name;
    const checked = event.target.checked;
    let etat_switch = {};

    if(name.includes("au_")){
      if(name === 'au_ob'){
        $("#au_pr").prop('checked', false);
        $("#au_co").prop('checked', false);
        etat_switch[name] = checked;
        Object.assign(etat_switch, { "au_pr": false });
        Object.assign(etat_switch, { "au_co": false });
      }else if(name === 'au_pr'){
        $("#au_co").prop('checked', false);
        $("#au_ob").prop('checked', false);
        etat_switch[name] = checked;
        Object.assign(etat_switch, { "au_co": false });
        Object.assign(etat_switch, { "au_ob": false });
      }else if(name === 'au_co'){
        $("#au_pr").prop('checked', false);
        $("#au_ob").prop('checked', false);
        etat_switch[name] = checked;
        Object.assign(etat_switch, { "au_pr": false });
        Object.assign(etat_switch, { "au_ob": false });
      }
      
    }else{
      const etat_text = document.querySelectorAll('h3');
      for (let i = 0; i < etat_text.length; i++) {
        let mainString = etat_text[i].id
        if (mainString.includes(name)) {
          if(checked === true){
            etat_text[i].textContent = 'Etat open'
          }else{
            etat_text[i].textContent = 'Etat close'
          }
        }  
      }
      etat_switch[name] = checked;
    }

    
    etat_switch[name] = checked;
    const jsonString = JSON.stringify(etat_switch);
    socket.send(jsonString);
  }

  // Add event listener to each input element
  inputs.forEach(input => {
      input.addEventListener('input', handleInputChange);
  });
});

function activateCheckbox(clickedCheckbox) {
  const checkboxes = document.querySelectorAll('input[type="checkbox"]');
  checkboxes.forEach(checkbox => {
      checkbox.checked = false;
  });
  clickedCheckbox.checked = true;
}