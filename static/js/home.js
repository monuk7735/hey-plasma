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
    user.address +
    '</p>\
                <p class="user-address-pin">' +
    user.pin +
    '</p>\
                <a href="#" class="user-contact-button">Contact</a>\
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
  };
  xmlHttp.send();
}

function filterUsersBy(type, target) {}

loadData();
