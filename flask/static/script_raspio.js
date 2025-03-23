document.addEventListener("DOMContentLoaded", () => {

  setInterval(relaySwitchPage, (500));
  // Select all input elements on the page
  const inputs = document.querySelectorAll('input');

  // Function to handle input changes
  function handleInputChange(event) {
    console.log(`Input changed: ${event.target.name} = ${event.target.checked}`);
    const jsonObject = {};
    jsonObject[event.target.name] = event.target.checked
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