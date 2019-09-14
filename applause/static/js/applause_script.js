
/**
 * Send the page view POST and get the pvid for the page
 */
document.addEventListener('DOMContentLoaded', function() {
  
  const path     = window.location.pathname;
  const referrer = document.referrer;
  const key = document.getElementById('applause-script').dataset.key;

  let XHR = new XMLHttpRequest();
  let FD  = new FormData();

  FD.append('path', path);
  FD.append('referrer', referrer);
  FD.append('key', key);

  XHR.open('POST', 'https://applauseapp.io/analytics/view');

  XHR.onreadystatechange = function() {
    if(this.readyState === XMLHttpRequest.DONE && this.status === 200) {
      console.log('Applause: Page view info sent successfully.');
      document.getElementById('applause-script').dataset.pvid = parseInt(XHR.response);
    }
    else if(this.status != 200) {
      console.log('Applause: Error sending page view info. Status code: ' + this.status);
    }
  }

  XHR.send(FD);

});

/**
 * Helper function for inserting an element after another
 */
function insertAfter(el, referenceNode) {
  referenceNode.parentNode.insertBefore(el, referenceNode.nextSibling);
}

/**
 * Get the total claps and this user's claps
 * returns an object
 */
function getClaps() {

  const path = window.location.pathname;
  const key = document.getElementById('applause-script').dataset.key;

  let XHR = new XMLHttpRequest();
  let FD  = new FormData();

  FD.append('path', path);
  FD.append('key', key);

  XHR.open('GET', 'https://applauseapp.io/analytics/clap');

  XHR.onreadystatechange = function() {
    if(this.readyState === XMLHttpRequest.DONE && this.status === 200) {
      console.log('Applause: Got claps successfully.');
      // we need to keep track of the total times the user has clapped and make sure it is no more than 50 times
      // total claps - user claps = initial claps
      let c = document.getElementById('applause-counter');
      claps = JSON.parse(XHR.response);
      c.setAttribute('data-initial_claps', claps.total - claps.user);
      c.innerText = claps.total;
    }
    else if(this.status != 200) {
      console.log('Applause: Error getting claps for this page. Status code: ' + this.status);
    }
  }

  XHR.send(FD);

}

/**
 * Update the server with the number of times this user has clapped
 */
function updateClaps() {

  let c = document.getElementById('applause-counter');
  
  const path = window.location.pathname;
  const key = document.getElementById('applause-script').dataset.key;
  const num_claps = parseInt(c.innerText) - parseInt(c.dataset.initial_claps);

  let XHR = new XMLHttpRequest();
  let FD  = new FormData();

  FD.append('path', path);
  FD.append('key', key);
  FD.append('num_claps', num_claps);

  XHR.open('PUT', 'https://applauseapp.io/analytics/clap');

  XHR.onreadystatechange = function() {
    if(this.readyState === XMLHttpRequest.DONE && this.status === 200) {
      console.log('Applause: Updated claps successfully.');
    }
    else if(this.status != 200) {
      console.log('Applause: Error updating claps for this page. Status code: ' + this.status);
    }
  }

  XHR.send(FD);
}

/**
 * Add the Clap button immedaetely after the script
 */
document.addEventListener('DOMContentLoaded', function() {
  
  const clap_white_url = 'https://static.applauseapp.io/images/clap_white.svg';
  const clap_black_url = 'https://static.applauseapp.io/images/clap_black.svg';
  const clap_pop_url = 'https://static.applauseapp.io/images/clap_pop.svg';
  // Clap SVG icons by Adrien Coquet from the Noun Project
  const clap_css_url = 'https://static.applauseapp.io/css/clap.css';

  let button = document.createElement('div');
  let anim = document.createElement('div');
  let counter = document.createElement('div');
  let total = document.createElement('div');
  let stylesheet = document.createElement('link');

  const script = document.getElementById('applause-script');
  
  button.setAttribute('id', 'applause-button');
  anim.setAttribute('id', 'applause-anim');
  counter.setAttribute('id', 'applause-counter');

  stylesheet.setAttribute('rel', 'stylesheet');
  stylesheet.setAttribute('href', 'https://static.applauseapp.io/css/clap.css');

  insertAfter(button, script);

  button.appendChild(anim);
  button.appendChild(counter);
  button.appendChild(total);

  insertAfter(stylesheet, button);

  // get the total claps and user claps
  getClaps();
  

  // Add event listener for clap button click
  document.getElementById('applause-button').addEventListener('click', function() {
    
    let e = document.getElementById('applause-anim');
    e.classList.add('applause-anim-active');
    setTimeout(function() {
      document.getElementById('applause-anim').classList.remove('applause-anim-active');
    }, 100);
    let c = document.getElementById('applause-counter');
    // ensure that the number of claps the user has added is no more than 50
    user_claps = parseInt(c.innerText) - parseInt(c.dataset.initial_claps);
    if(user_claps <= 50) {
      c.innerText = parseInt(c.innerText) + 1;
      updateClaps(user_claps + 1);
    }

  });

});



