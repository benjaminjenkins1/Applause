
/**
 * Send the page view POST and get the pvid
 */
document.addEventListener('DOMContentLoaded', function() {
  
  const path     = window.location.pathname;
  const referrer = document.referrer;
  const key = document.getElementById('applause-tag').dataset.key;

  let XHR = new XMLHttpRequest();
  let FD  = new FormData();

  FD.append('path', path);
  FD.append('referrer', referrer);
  FD.append('key', key);

  XHR.addEventListener('error', function() {
    console.log('Applause: Error sending page view info.');
  });

  XHR.open('POST', 'https://applauseapp.io/analytics/view');

  XHR.onreadystatechange = function() {
    if(this.readyState === XMLHttpRequest.DONE && this.status === 200) {
      console.log('Applause: Page view info sent successfully.');
      document.getElementById('applause-tag').dataset.pvid = parseInt(XHR.response);
    }
    else if(this.status != 200) {
      console.log('Applause: Error sending page view info. Status code: ' + this.status);
    }
  }

  XHR.send(FD);

});

window.addEventListener('beforeunload', (event) => {

  const e = document.getElementById('applause-tag');
  const path = window.location.pathname;
  const pvid = e.dataset.pvid;
  const key = e.dataset.key;

  let XHR = new XMLHttpRequest();
  let FD = new FormData();

  FD.append('path', path);
  FD.append('pvid', pvid);
  FD.append('key', key);

  XHR.addEventListener('error', function() {
    console.log('Applause: Error sending page leave info.');
  });

  XHR.open('PUT', 'https://applauseapp.io/analytics/view');

  XHR.onreadystatechange = function() {
    if(this.readyState === XMLHttpRequest.HEADERS_RECEIVED) {
      console.log('Applause: Sending page leave request.');
    }
  }

  XHR.send(FD);

});

