function finalurl(){
    var url = new URL(window.location.href);
    var search_params = url.searchParams
    search_params.set('sort',document.getElementById("sort-list").value);
    url.search=search_params.toString();
    var newurl = url.toString()
    console.log(newurl)
    window.location.href = newurl;
}