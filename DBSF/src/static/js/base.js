function checkbox(){
    if(document.getElementById("checkbox-menu").checked){
        // Make logo disappear
        document.getElementById("logo").style.display = "none";

        // move hamburger
        document.getElementById("dropdown-menu").style.paddingLeft = "17vw";

        // update grid ratio
        document.getElementById("navbar").style.gridTemplateColumns = "0.6fr 0.4fr 1fr 1fr";

        // update grid ratio for body
        document.getElementById("base-body").style.gridTemplateColumns = "14fr 86fr";
    }else{
        // make logo appear
        document.getElementById("logo").style.display = "flex";

        // move back hamburger
        document.getElementById("dropdown-menu").style.paddingLeft = "1.5vw";

        // update grid ratio
        document.getElementById("navbar").style.gridTemplateColumns = "0.2fr 0.8fr 1fr 1fr";

        // update grid ratio for body
        document.getElementById("base-body").style.gridTemplateColumns = "0fr 1fr";
    }
}