function showToastCreated(){
     var toastEl = document.getElementById('addToast');
     toast = new bootstrap.Toast(toastEl);
     toast.show();
 }

 function sendInfoToModal(url){ 
    let csrfValue = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(url, {
        method:"POST",
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': csrfValue,
            "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify({'post_data_1' : SAMPLE_CHOOSEN}),
    }).then(response => response.json()).
    then(function(data){
    //clear table
    var table = document.getElementById("SampleSelectedTable").getElementsByTagName('tbody')[0];
    while (table.hasChildNodes()) {
        table.removeChild(table.lastChild);
    }
    for(let i=0; i<(JSON.parse(data["samples_selected"]).length); i++  ){
        pk = JSON.parse(data["samples_selected"])[i]["pk"]
        var refTable = document.getElementById("SampleSelectedTable").getElementsByTagName('tbody')[0];
        var nouvelleLigne = refTable.insertRow(i);
        nouvelleLigne.classList.add("text-center");
        nouvelleLigne.classList.add("align-middle");

        var cellule1 = nouvelleLigne.insertCell(0);
        cellule1.style.color = "var(--color)";
        var inputSelected = document.createElement("INPUT");
        inputSelected.classList.add("form-check-input");
        inputSelected.classList.add("row_selector");
        inputSelected.type = "checkbox";
        inputSelected.setAttribute("data-id",pk);
        inputSelected.checked = true;
        cellule1.appendChild(inputSelected);

        var cellAudio = nouvelleLigne.insertCell(1);
        cellAudio.style.color = "var(--color)";
        var audioSelected = document.createElement("AUDIO");
        audioSelected.volume = "1";
        audioSelected.controls = true;
        audioSelected.preload = "metadata";
        audioSelected.classList.add("player");
        audioSelected.style.maxWidth = "200px";
        var sourceAudio = document.createElement("SOURCE");
        sourceAudio.src = JSON.parse(data["samples_url"])[i];
        audioSelected.appendChild(sourceAudio);
        cellAudio.appendChild(audioSelected);

        var cellName = nouvelleLigne.insertCell(2);
        cellName.style.color = "var(--color)";
        var textName = document.createTextNode(JSON.parse(data["samples_selected"])[i]["fields"]["name"]);
        cellName.appendChild(textName);

        var cellAuthor = nouvelleLigne.insertCell(3);
        cellAuthor.style.color = "var(--color)";
        var textAuthor = document.createTextNode(JSON.parse(data["samples_artist"])[i]["fields"]["username"]);
        cellAuthor.appendChild(textAuthor);

        var cellTags = nouvelleLigne.insertCell(4);
        cellTags.style.color = "var(--color)";
        var tag = document.createElement("SPAN");
        tag.classList.add("badge");
        console.log(JSON.parse(data["samples_tag"])[i]);
        tag.style.backgroundColor = JSON.parse(data["samples_tag"])[i]["fields"]["color"];
        tag.innerHTML = JSON.parse(data["samples_tag"])[i]["fields"]["name"];
        cellTags.appendChild(tag);


        var cellDate = nouvelleLigne.insertCell(5);
        cellDate.style.color = "var(--color)";
        var texte = JSON.parse(data["samples_selected"])[i]["fields"]["created_date"].split("T");
        texte = texte[0] + " " + texte[1].split(".")[0];
        var textDate = document.createTextNode(texte);
        cellDate.appendChild(textDate);
    }
    })
    .catch(err => {
    // gestion des erreurs
     });
}


function changeDataServer(url){
    SAMPLE_CHOOSEN = []
    let csrfValue = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var checkboxesSamples = document.querySelectorAll('input[type=checkbox]:checked')
    for (var i = 0; i < checkboxesSamples.length; i++) {
        SAMPLE_CHOOSEN.push(checkboxesSamples[i].getAttribute("data-id"));        
    }   
    fetch(url, {
        method:"POST",
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': csrfValue,
            "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify({'post_data_2' : SAMPLE_CHOOSEN}),
    }).then(response => response.json()).
    then(function(data){
        if (data.type === "deleteFromMySamples"){
            var sampleDiv  = document.querySelector('#mySamplesList');
            sampleDiv.innerHTML = data.sample_list;
            var toastEl = document.getElementById('deleteToMySampleToast');
            var cards = document.querySelectorAll("a[checked='true']");
            for (var i = 0; i < cards.length; i++) { 
                cards[i].setAttribute("checked", "false");
            }
            SHOW_EDIT_TAGS = false;
            render();
            }
        else{
            var toastEl = document.getElementById('addToMySampleToast');
        }
        toast = new bootstrap.Toast(toastEl);
        toast.show();
    })
    .catch(err => {
    // gestion des erreurs
     });
}

function changeMacro(){
    divsMicro = document.getElementsByClassName("micro");
    for(var i=0; i<divsMicro.length; i++) {
        divsMicro[i].classList.add("d-none");
    }
    divsMacro = document.getElementsByClassName("macro");
    for(var i=0; i<divsMacro.length; i++) {
        divsMacro[i].classList.remove("d-none");
    }
    document.getElementById("filter_macro").checked = true;
    document.getElementById("btnradio2").classList.remove("btn-active");
    document.getElementById("btnradio1").classList.add("btn-active")
};

function changeMicro(){
    divsMacro = document.getElementsByClassName("macro");
    for(var i=0; i<divsMacro.length; i++) {
        divsMacro[i].classList.add("d-none");
    }
    divsMicro = document.getElementsByClassName("micro");
    for(var i=0; i<divsMicro.length; i++) {
        divsMicro[i].classList.remove("d-none");
    }
    document.getElementById("filter_macro").checked = false;
    document.getElementById("btnradio1").classList.remove("btn-active");
    document.getElementById("btnradio2").classList.add("btn-active")
};

function selectCard(id, user=null){
    var item=document.getElementById(id);
    if (item.getAttribute("checked") === "false"){
        item.style.border= "3px solid ghostwhite";
        item.style.borderRadius= "7px";
        item.setAttribute("checked",true);}
    else{
        item.classList.remove("select");
        item.style.border= "none";
        item.setAttribute("checked",false);
    }
    if (typeof SHOW_EDIT_TAGS !== "undefined"){
        var cards = document.querySelectorAll("a[checked='true']");
        for (var i = 0; i < cards.length; i++) { 
                if (user===cards[i].getAttribute("author")){
                    SHOW_EDIT_TAGS = true;
                }
                else {
                    SHOW_EDIT_TAGS = false;
                    break;
                }
            }
        if(cards.length===0){
            SHOW_EDIT_TAGS = false;
        }
    }
    render();
}


(function () {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('.needs-validation')

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
            }

            form.classList.add('was-validated')
        }, false)
        })
    })()