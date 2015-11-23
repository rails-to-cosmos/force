var ajax = {};
ajax.x = function() {
  if (typeof XMLHttpRequest !== 'undefined') {
    return new XMLHttpRequest();
  }
  var versions = [
    "MSXML2.XmlHttp.6.0",
    "MSXML2.XmlHttp.5.0",
    "MSXML2.XmlHttp.4.0",
    "MSXML2.XmlHttp.3.0",
    "MSXML2.XmlHttp.2.0",
    "Microsoft.XmlHttp"
  ];

  var xhr;
  for(var i = 0; i < versions.length; i++) {
    try {
      xhr = new ActiveXObject(versions[i]);
      break;
    } catch (e) {
    }
  }
  return xhr;
};

ajax.send = function(url, callback, method, data, sync) {
  var x = ajax.x();
  x.open(method, url, sync);
  x.onreadystatechange = function() {
    if (x.readyState == 4) {
      callback(x.responseText)
    }
  };
  if (method == 'POST') {
    x.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  }
  x.send(data)
};

ajax.get = function(url, data, callback, sync) {
  var query = [];
  for (var key in data) {
    query.push(encodeURIComponent(key) + '=' + encodeURIComponent(data[key]));
  }
  ajax.send(url + (query.length ? '?' + query.join('&') : ''), callback, 'GET', null, sync)
};

ajax.post = function(url, data, callback, sync) {
  var query = [];
  for (var key in data) {
    query.push(encodeURIComponent(key) + '=' + encodeURIComponent(data[key]));
  }
  ajax.send(url, callback, 'POST', query.join('&'), sync)
};

function send_order(menu, product) {
  ajax.post('/order', {menu: menu, product: product}, function(response) {
    if (response >= 1) {
      if (response > 1) {
        document.getElementById('order-count-'+product).innerHTML = response + '×';
      }

      if (document.getElementById(product).className.indexOf('ordered') == -1) {
        document.getElementById(product).className += ' ordered';
      }
      document.getElementById('product-cancel-'+product).style.display = 'block';
    }
  });
}

function cancel_order(menu, product) {
  ajax.post('/cancel', {menu: menu, product: product}, function(response) {
    if (response == 0) {
      document.getElementById('order-count-'+product).innerHTML = '';
      document.getElementById(product).className = document.getElementById(product).className.replace(/ordered/g, '');
      document.getElementById('product-cancel-'+product).style.display = 'none';
    }
  });
}
