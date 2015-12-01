var toggle = {

  hide : function(obj) {
    if (typeof obj == 'undefined' || typeof obj.className == 'undefined') {
      return false;
    }

    if (obj.className.indexOf('hidden') == -1) {
      obj.className = obj.className + ' hidden';
    }

    return true;
  },

  show : function(obj) {
    if (typeof obj == 'undefined' || typeof obj.className == 'undefined') {
      return false;
    }

    obj.className = obj.className.replace(/hidden/g, '');
    return true;
  }

};

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
  ajax.send(url, callback, 'POST', query.join('&'), sync);
};

function draw_add_order(product_id, name, cost, count, menu_id, total, rest) {
  if (count <= 0) {
    return False;
  }

  if (count > 1) {
    document.getElementById('order-count-'+product_id).innerHTML = count + '×';
  }

  if (document.getElementById(product_id).className.indexOf('ordered') == -1) {
    document.getElementById(product_id).className += ' ordered';
  }

  old_cost = document.getElementById('total-cost');
  if (old_cost != undefined) {
    old_cost_num = old_cost.innerHTML.match(/\d+/)[0]*1;
    old_cost.parentNode.removeChild(old_cost);
  } else {
    old_cost_num = 0;
  }

  order_table = document.getElementById('order-table');
  tr_id = 'ordered-item-' + product_id;
  tr = document.getElementById(tr_id);

  if (tr == undefined) { // new item, add it
    tr = document.createElement('tr');
    tr.id = 'ordered-item-' + product_id;

    td_op = document.createElement('td');
    td_op.style.minWidth = '20px';
    button_minus = document.createElement('img');
    button_minus.id = 'product-cancel-'+product_id;
    button_minus.className = product_id+'-cancel';
    button_minus.style.verticalAlign = 'middle';
    button_minus.style.cursor = 'pointer';
    button_minus.setAttribute('onclick', 'cancel_order(\''+menu_id+'\', \''+product_id+'\')');
    button_minus.src = '/static/img/minus.png';
    button_minus.width = 16;

    td_op.appendChild(button_minus);

    if (count > 1) {
      food_count = count + '×';
    } else {
      food_count = '';
    }

    td_food = document.createElement('td');
    td_food.width = '100%';
    td_food.className = 'td-food';
    td_food.id = 'td-food-' + product_id;
    td_food.innerHTML = '<div class="td-food-inner">' + food_count + name + '</div>';

    td_cost = document.createElement('td');
    td_cost.id = 'product-cost-'+product_id;
    td_cost.innerHTML = cost*count + ' ₽';
    td_cost.style.minWidth = '50px';

    tr.appendChild(td_op);
    tr.appendChild(td_food);
    tr.appendChild(td_cost);
    order_table.appendChild(tr);
  } else {
    td_cost = document.getElementById('product-cost-'+product_id);
    td_cost.innerHTML = cost*count + ' ₽';

    if (count > 1) {
      food_count = count + '×';
    } else {
      food_count = '';
    }

    td_food = document.getElementById('td-food-' + product_id);
    td_food.innerHTML = '<div class="td-food-inner">' + food_count + name + '</div>';
  }

  new_cost = document.createElement('tr');
  new_cost.id = 'total-cost';
  td_empty = document.createElement('td');
  td_empty.setAttribute('colspan', '2');
  td_cost = document.createElement('td');
  span_cost = document.createElement('span');
  span_cost.innerHTML = total + '&nbsp;₽';
  td_cost.appendChild(span_cost);
  new_cost.appendChild(td_empty);
  new_cost.appendChild(td_cost);
  order_table.appendChild(new_cost);
  order_label = document.getElementById('order-label');
  toggle.show(order_label);

  view_delivery_cost(rest);

  return false;
}

function view_delivery_cost(rest) {
  delivery_info = document.getElementById('delivery-info');
  toggle.show(delivery_info);

  if (rest > 0 && rest < 1500) {
    document.getElementById('sum-order-cost-total').innerHTML = rest;
    els = document.getElementsByClassName('sum-order-label');
    for (el in els) {
      if (els[el].id == 'total-delivery') {
        toggle.show(els[el]);
      } else {
        toggle.hide(els[el]);
      }
    }

    // order cost
    els = document.getElementsByClassName('sum-delivery-label');
    for (el in els) {
      if (els[el].id == 'not-free-delivery-container') {
        toggle.show(els[el]);
      } else {
        toggle.hide(els[el]);
      }
    }

    if (rest <= 500) {
      document.getElementById('delivery-cost-cheap').innerHTML = 100;
      els = document.getElementsByClassName('delivery-cost');
      for (el in els) {
        if (els[el].id == 'cheap-delivery') {
          toggle.show(els[el]);
        } else {
          toggle.hide(els[el]);
        }
      }
    } else {
      if (rest < 1500) {
        document.getElementById('delivery-cost-expensive').innerHTML = 200;
        els = document.getElementsByClassName('delivery-cost');
        for (el in els) {
          if (els[el].id == 'expensive-delivery') {
            toggle.show(els[el]);
          } else {
            toggle.hide(els[el]);
          }
        }
      } else {
        if (rest >= 1500) {
          els = document.getElementsByClassName('sum-delivery-label');
          for (el in els) {
            toggle.hide(els[el]);
          }
        }
      }
    }
  } else {
    if (rest <= 0) {
      total_delivery = document.getElementById('total-delivery');
      toggle.hide(total_delivery);
      els = document.getElementsByClassName('sum-delivery-label');
      for (el in els) {
        if (els[el].id == 'free-delivery-container') {
          toggle.show(els[el]);
        } else {
          toggle.hide(els[el]);
        }
      }
    } else {
      delivery_info = document.getElementById('delivery-info');
      toggle.hide(delivery_info);
    }
  }
}

function send_order(menu, product) {
  ajax.post('/order', {menu: menu, product: product}, function(response) {
    response = JSON.parse(response);
    draw_add_order(product, response.name, response.cost, response.count, response.menu, response.total, response.rest);
  }, 'async');
}

function cancel_order(menu, product) {
  ajax.post('/cancel', {menu: menu, product: product}, function(response) {
    response = JSON.parse(response);
    order_table = document.getElementById('order-table');
    tr_id = 'ordered-item-' + product;
    tr = document.getElementById(tr_id);
    if (tr != undefined) {
      if (response.count == 0) {
        tr.parentNode.removeChild(tr);
        document.getElementById(product).className = document.getElementById(product).className.replace(/ordered/g, '');
        if (response.total == 0) {
          order_label = document.getElementById('order-label');
          toggle.hide(order_label);
        }
      } else {
        td_cost = document.getElementById('product-cost-'+product);
        td_cost.innerHTML = response.cost*response.count + ' ₽';
        td_count = document.getElementById('product-count-'+product);
        if (response.count > 1) {
          food_count = response.count + '×';
        } else {
          food_count = '';
        }

        td_food = document.getElementById('td-food-' + product);
        td_food.innerHTML = '<div class="td-food-inner">' + food_count + response.name + '</div>';
      }
    }

    old_cost = document.getElementById('total-cost');
    if (old_cost != undefined) {
      old_cost_num = old_cost.innerHTML.match(/\d+/)[0]*1;
      old_cost.parentNode.removeChild(old_cost);
    } else {
      old_cost_num = 0;
    }

    if(response.total > 0) {
      new_cost = document.createElement('tr');
      new_cost.id = 'total-cost';
      td_empty = document.createElement('td');
      td_empty.setAttribute('colspan', '2');
      td_cost = document.createElement('td');
      span_cost = document.createElement('span');
      span_cost.innerHTML = response.total + ' ₽';
      td_cost.appendChild(span_cost);
      new_cost.appendChild(td_empty);
      new_cost.appendChild(td_cost);
      order_table.appendChild(new_cost);
    }

    view_delivery_cost(response.rest);
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

  if (typeof ordered_products == "undefined") {
    ordered_products = [];
  }

  for (op in ordered_products) {
    draw_add_order(ordered_products[op].id,
                   ordered_products[op].name,
                   ordered_products[op].cost,
                   ordered_products[op].count,
                   ordered_products[op].menu_id,
                   ordered_products[op].total,
                   ordered_products[op].rest);
  }
}
