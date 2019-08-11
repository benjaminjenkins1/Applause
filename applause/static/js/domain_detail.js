

var toggleKeyDetails = function(uuid) {
  let key_li = document.getElementById(uuid);
  let code = key_li.querySelector("code");
  let form = key_li.querySelector("form");
  let button = key_li.querySelector("button");
  if(code.hasAttribute("hidden")){
    code.removeAttribute("hidden");
    form.removeAttribute("hidden");
    button.innerText = "less";
  }
  else {
    code.setAttribute("hidden", true);
    form.setAttribute("hidden", true);
    button.innerText = "more";
  }
}