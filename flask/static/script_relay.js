document.addEventListener("DOMContentLoaded", () => {

  setInterval(relaySwitchPage, (500));
  // Select all input elements on the page
  const inputs = document.querySelectorAll('input');

  // Function to handle input changes
  function handleInputChange(event) {
    const name = event.target.name;
    const checked = event.target.checked;
    const etat_switch = document.querySelectorAll('h3');
    for (let i = 0; i < etat_switch.length; i++) {
      let mainString = etat_switch[i].id
      if (mainString.includes(name)) {
        if(checked === true){
          etat_switch[i].textContent = 'Etat open'
        }else{
          etat_switch[i].textContent = 'Etat close'
        }
      }  
    }
    const jsonObject = {};
    jsonObject[name] = checked
    $.getJSON('/flask/relaySwitch', {
      result:JSON.stringify(jsonObject)
    }, function(data, status, xhr) {
        myObj = data.result
    });
  }

  // Add event listener to each input element
  inputs.forEach(input => {
      input.addEventListener('input', handleInputChange);
  });
});

function relaySwitchPage() {
  $.getJSON('/flask/relaySwitchPage', {
  }, function(data, status, xhr) {
    if (data.result != null) {
      myObj = JSON.parse(data.result);
    }
  });
}

  //document.getElementById("relaySwitch").checked = true;