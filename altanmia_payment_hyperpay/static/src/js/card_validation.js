function formats(ele,e){
    if(ele.value.length<19){
        ele.value= ele.value.replace(/\W/gi, '').replace(/(.{4})/g, '$1 ');
        return true;
    }else{
        return false;
    }
}

function formatsCVV(ele,e){
    if(ele.value.length<4){
        return true;
    }else{
        return false;
    }
}

function numberValidation(e){
    e.target.value = e.target.value.replace(/[^\d ]/g,'');
    return false;
}