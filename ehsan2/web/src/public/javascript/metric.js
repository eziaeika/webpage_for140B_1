document.addEventListener("DOMContentLoaded", (event) => {
  var dataURL =
    "https://data.seattle.gov/resource/4xy5-26gy.json?$order=date%20desc&$limit=1";

  function showError(err) {
    console.log(err);
  }

  function update(data) {
    var theCount = data[0].fremont_bridge;
    var theUsers = document.querySelector("#users");
    theUsers.setAttribute("data-count", theCount);
  }

  fetch(dataURL)
    .then((response) => response.json())
    .then(update)
    .catch(showError);
});
