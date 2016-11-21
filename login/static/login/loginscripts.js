function enterField(el){
    if (el.value == "User Name"){
        el.value = "";
        el.style.color = "black";
        el.style.fontStyle = "normal";
    } else if (el.value == ""){
        el.value = "User Name";
        el.style.color = "grey";
        el.style.fontStyle = "italic";
    }
}

function exitField(el){
    if (el.value == ""){
        el.value = "User Name";
        el.style.color = "grey";
        el.style.fontStyle = "italic";
    } else{
        el.style.color = "black";
        el.style.fontStyle = "normal";
    }
}

function enterPassField(el){ 
    if ((el.value == "Password" || el.value == "Confirm Password")&& (el.type != "password")){
        el.type = "password";
        el.value = "";
        el.style.color = "black";
        el.style.fontStyle = "normal";
    }
}

function exitPassField(el){
    if (el.value == ""){
        if (el.name == "PassWord")
            el.value = "Password";
        else   
            el.value = "Confirm Password";
        el.type = "text";
        el.style.color = "grey";
        el.style.fontStyle = "italic";
    } 
}