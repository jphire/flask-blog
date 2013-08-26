(function() {
  window.add_tag = function(e) {
    var a_elem, amount, choice, div, elem, i_elem, tag, option, td_elem, td_elem_remove, tr_elem, val, _i, _len;
    choice = $('#post_tag_id').get(0);
    val = choice.value;
    div = document.createElement('div');
    div.setAttribute("id", val + "_hidden");
    elem = document.createElement('input');
    tr_elem = document.createElement('tr');
    tr_elem.id = val;
    td_elem = document.createElement('td');
    td_elem_remove = document.createElement('td');
    a_elem = document.createElement('a');
    i_elem = document.createElement('i');
    i_elem.setAttribute("class", "icon-remove");
    for (_i = 0, _len = choice.length; _i < _len; _i++) {
      option = choice[_i];
      if (option.value === val && option.innerHTML !== "Choose tag") {
        td_elem.innerHTML = option.innerHTML + ", " + amount + " g</br>";
        a_elem.href = "#";
        a_elem.setAttribute("class", "nav-link");
        a_elem.setAttribute("onclick", "remove_tag_element(" + val + ")");
        material = val;
        elem.type = "hidden";
        elem.name = "new_materials[" + material + "]";
        elem.value = amount;
        $('#recipe_materials').append(tr_elem);
        $('#recipe_materials').append(div);
        $(div).append(elem);
        $(tr_elem).append(td_elem);
        $(tr_elem).append(td_elem_remove);
        $(td_elem_remove).append(a_elem);
        $(a_elem).append(i_elem);
      }
    }
    console.log(div);
    return console.log(amount);
  };

}).call(this);