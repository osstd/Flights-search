const preloader = document.querySelector("[data-preloader]");

window.addEventListener("load", function () {
  preloader.classList.add("loaded");
  document.body.classList.add("loaded");
});

function loadingH() {
  var loader = document.getElementById("loading");
  loader.style.display = "block";

  var form = document.getElementById("form");
  form.style.display = "none";

  var alert = document.getElementById("alert");
  alert.style.display = "none";
}
