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
    response = JSON.parse(response);
    if (response.count >= 1) {
      if (response.count > 1) {
        document.getElementById('order-count-'+product).innerHTML = response.count + '×';
      }

      if (document.getElementById(product).className.indexOf('ordered') == -1) {
        document.getElementById(product).className += ' ordered';
      }

      document.getElementById('product-cancel-'+product).style.display = 'block';

      order_table = document.getElementById('order-table');
      tr_id = 'ordered-item-' + product;
      tr = document.getElementById(tr_id);
      if (tr == undefined) {
        tr = document.createElement('tr');
        tr.id = 'ordered-item-' + product;
        td_food = document.createElement('td');
        td_food.innerHTML = response.name;
        td_cost = document.createElement('td');
        td_cost.id = 'product-cost-'+product;
        td_cost.innerHTML = response.cost*response.count + ' ₽';
        tr.appendChild(td_food);
        tr.appendChild(td_cost);
        order_table.appendChild(tr);
      } else {
        td_cost = document.getElementById('product-cost-'+product);
        td_cost.innerHTML = response.cost*response.count + ' ₽';
      }

      old_cost = document.getElementById('total-cost');
      if (old_cost != undefined) {
        old_cost_num = old_cost.innerHTML.match(/\d+/)[0]*1;
        old_cost.parentNode.removeChild(old_cost);
      } else {
        old_cost_num = 0;
      }

      new_cost = document.createElement('tr');
      new_cost.id = 'total-cost';
      td_empty = document.createElement('td');
      td_cost = document.createElement('td');
      span_cost = document.createElement('span');
      span_cost.innerHTML = (old_cost_num + response.cost) + ' ₽';
      td_cost.appendChild(span_cost);
      new_cost.appendChild(td_empty);
      new_cost.appendChild(td_cost);
      order_table.appendChild(new_cost);
    }
  });
}

function cancel_order(menu, product) {
  ajax.post('/cancel', {menu: menu, product: product}, function(response) {
    response = JSON.parse(response);
    document.getElementById('order-count-'+product).innerHTML = '';
    document.getElementById(product).className = document.getElementById(product).className.replace(/ordered/g, '');
    document.getElementById('product-cancel-'+product).style.display = 'none';
  });
}

window.onload = function () {
  var scrolledElement = document.querySelector('#sales-receipt');
  var top = scrolledElement.offsetTop;
  var listener = function () {
    var y = window.pageYOffset;

    if (y >= top) {
      scrolledElement.classList.add('fixed');
    } else {
      scrolledElement.classList.remove('fixed');
    }
  };
  window.addEventListener('scroll', listener, false);
}
