

var toggleKeyDetails = function(uuid) {
  let key_li = document.getElementById(uuid);
  let code = key_li.querySelector("code")
  let form = key_li.querySelector("form");
  if(code.hasAttribute("hidden")){
    code.removeAttribute("hidden");
    form.removeAttribute("hidden");
  }
  else {
    code.setAttribute("hidden", true);
    form.setAttribute("hidden", true);
  }
}