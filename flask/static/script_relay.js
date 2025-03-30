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
    let etat_switch = {};
    etat_switch[name] = checked;
    const jsonString = JSON.stringify(etat_switch);
    socket.send(jsonString);
  }



  // Add event listener to each input element
  inputs.forEach(input => {
      input.addEventListener('input', handleInputChange);
  });
});

//document.getElementById("relaySwitch").checked = true;