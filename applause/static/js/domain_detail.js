

var toggleKeyDetails = function(uuid) {
  let key_li = document.getElementById(uuid);
  let pre = key_li.querySelector("pre");
  let form = key_li.querySelector("form");
  let button = key_li.querySelector("button");
  if(pre.hasAttribute("hidden")){
    pre.removeAttribute("hidden");
    form.removeAttribute("hidden");
    button.innerText = "less";
  }
  else {
    pre.setAttribute("hidden", true);
    form.setAttribute("hidden", true);
    button.innerText = "more";
  }
}