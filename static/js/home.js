var users = [];

function makeCard(user) {
  return (
    '<div class="card">\
                <h1 class="user-name">' +
    user.name +
    " - " +
    user.blood +
    '</h1>\
                <p class="user-address">' +
    user.city +
    ", " +
    user.state +
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
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("POST", "/request", true); // false for synchronous request

  xmlHttp.onload = function (e) {
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

function filterUsersBy(type, target) {}

loadData();
