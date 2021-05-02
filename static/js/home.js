var users = [];
var loader= document.getElementsByClassName('loader-container')[0];
function makeCard(user) {
  return (
    '<div class="card">\
                <h1 class="user-name">' +
    user.name +
    " - " +
    user.blood +
    '</h1>\
                <p class="user-address">' +
    user.address +
    '</p>\
                <p class="user-address-pin">' +
    user.pin +
    '</p>\
                <div class="user-contact-button" uid="' +
    user.uid +
    '">Contact</div>\
                </div>'
  );
}

function loadData() {

  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("GET", "/api/users", true); // false for synchronous request
  xmlHttp.onload = function (e) {
    users = JSON.parse(xmlHttp.responseText);

    userHolder = document.getElementById("card-holder");
    userHolder.innerHTML = "";

    for (let i = 0; i < users.length; i++) {
      userHolder.innerHTML += makeCard(users[i]);
    }

    allElements = document.getElementsByClassName("user-contact-button");
    for (let i = 0; i < allElements.length; i++) {
      allElements[i].onclick = makeRequest;
    }


  };
  xmlHttp.send();
}

function makeRequest(e) {
  console.log(loader.style.visibility)
  loader.style.visibility = "visible";
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("POST", "/request", true); // false for synchronous request

  xmlHttp.onload = function (e) {
    loader.style.visibility="hidden"
    resp = JSON.parse(xmlHttp.responseText);
    if (!resp.status) {
      document.location = "/login";
    } else {
      alert(resp.message);
    }
  };
  xmlHttp.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xmlHttp.send("uid=" + e.srcElement.getAttribute("uid"));
}

function filterUsers() {
  let address = document.getElementById("filter-by-address").value;
  let pin = document.getElementById("filter-by-pin").value;
  let bg = document.getElementById("filter-by-bg").value;

  userHolder = document.getElementById("card-holder");
  userHolder.innerHTML = "";

  for (let i = 0; i < users.length; i++) {
    let user = users[i];
    if ((user.pin == pin || pin == "") && user.address.includes(address) && (bg == user.blood || bg == "")) {
      userHolder.innerHTML += makeCard(users[i]);
    }
  }

  allElements = document.getElementsByClassName("user-contact-button");
  for (let i = 0; i < allElements.length; i++) {
    allElements[i].onclick = makeRequest;
  }
}

document.getElementById("filter-submit").onclick = (e) => {
  filterUsers();
};

loadData();
