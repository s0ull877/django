function ShowRoles() {
    document.getElementById("all-roles").classList.toggle("show");
}

function filterFunction() {
    var filter, a, i;
    div = document.getElementsByClassName("all-roles")
    console.log(div)
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
        if (a[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}