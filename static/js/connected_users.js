var changebutton = document.getElementById("change-button");
var loader = document.getElementsByClassName("loader-container")[0];

function change(e) {
  loader.style.visibility = "visible";
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("POST", "/changestatus", true); // false for synchronous request

  xmlHttp.onload = function (e) {
    loader.style.visibility = "hidden";
    resp = JSON.parse(xmlHttp.responseText);
    if (!resp.status) {
      document.location = "/login";
    } else {
      alert(resp.message);

      location.reload();
    }
  };
  xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xmlHttp.send("canDonate=" + e);
}
