
/**
 * Send the page view POST and get the pvid
 */
document.addEventListener('DOMContentLoaded', function() {
  
  let path     = window.location.pathname;
  let referrer = document.referrer;
  let key = document.getElementById('applause-tag').dataset.key;

  let XHR = new XMLHTTPRequest();
  let FD  = new FormData();

  FD.append('path', path);
  FD.append('referrer', referrer);
  FD.append('key', key);

  XHR.addEventListener('load', function() {
    console.log('Page view info sent successfully');
  });

  XHR.addEventListener('error', function() {
    console.log('Error sending page view info');
  });

  XHR.open('POST', 'http://benjen.me:5000/analytics/view');

  XHR.send(FD);

});


