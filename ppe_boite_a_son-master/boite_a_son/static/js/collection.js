function sendInfoToModalCollection(url){
    let csrfValue = document.querySelector('[name=csrfmiddlewaretoken]').value;
    fetch(url, {
        method:"POST",
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': csrfValue,
            "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify({'post_data_1' : COLLECTION_CHOOSEN}),
    }).then(response => response.json()).
    then(function(data){
    //clear table
    var table = document.getElementById("CollectionSelectedTable").getElementsByTagName('tbody')[0];
    while (table.hasChildNodes()) {
        table.removeChild(table.lastChild);
    }
    console.log("SAMPLES_CHOOSEN :", COLLECTION_CHOOSEN);
    for(let i=0; i<(JSON.parse(data["collections_selected"]).length); i++  ){
        pk = JSON.parse(data["collections_selected"])[i]["pk"]
        var refTable = document.getElementById("CollectionSelectedTable").getElementsByTagName('tbody')[0];
        var nouvelleLigne = refTable.insertRow(i);
        nouvelleLigne.classList.add("text-center");
        nouvelleLigne.classList.add("align-middle");


        var cellCheckbox = nouvelleLigne.insertCell(0);
        cellCheckbox.style.color = "var(--color)";
        var inputSelected = document.createElement("INPUT");
        inputSelected.classList.add("form-check-input");
        inputSelected.classList.add("row_selector");
        inputSelected.type = "checkbox";
        inputSelected.setAttribute("data-id",pk);
        inputSelected.checked = true;
        cellCheckbox.appendChild(inputSelected);


        var cellName = nouvelleLigne.insertCell(1);
        cellName.style.color = "var(--color)";
        var textName = document.createTextNode(JSON.parse(data["collections_selected"])[i]["fields"]["name"]);
        cellName.appendChild(textName);


        var cellAuthor = nouvelleLigne.insertCell(2);
        cellAuthor.style.color = "var(--color)";
        var textAuthor = document.createTextNode(JSON.parse(data["collections_artist"])[i]["fields"]["username"]);
        cellAuthor.appendChild(textAuthor);

    
        var cellNbSamples = nouvelleLigne.insertCell(3);
        cellNbSamples.style.color = "var(--color)";
        var nbSamples = document.createTextNode(JSON.parse(data["collections_selected"])[i]["fields"]["samples"].length);
        cellNbSamples.appendChild(nbSamples);

        var cellDescription = nouvelleLigne.insertCell(4);
        cellDescription.style.color = "var(--color)";
        cellDescription.classList.add("text-truncate");
        cellDescription.style.maxWidth = "100px";
        var description = document.createTextNode(JSON.parse(data["collections_selected"])[i]["fields"]["description"]);
        cellDescription.appendChild(description);

        
        var cellDate = nouvelleLigne.insertCell(5);
        cellDate.style.color = "var(--color)";
        var texte = JSON.parse(data["collections_selected"])[i]["fields"]["created_date"].split("T");
        texte = texte[0] + " " + texte[1].split(".")[0];
        var textDate = document.createTextNode(texte);
        cellDate.appendChild(textDate);
        
    }
    })
    .catch(err => {
    // gestion des erreurs
    });
}


function changeDataCollections(url){
    COLLECTION_CHOOSEN = []
    let csrfValue = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var checkboxesSamples = document.querySelectorAll('input[type=checkbox]:checked')
    for (var i = 0; i < checkboxesSamples.length; i++) {
        COLLECTION_CHOOSEN.push(checkboxesSamples[i].getAttribute("data-id"));        
    }   
    fetch(url, {
        method:"POST",
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': csrfValue,
            "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify({'post_data_2' : COLLECTION_CHOOSEN}),
    }).then(function (response){
        return response.json();
    }).
    then(function(data){
        if (data.type === "deleteFromMyCollections"){
            var collectionDiv  = document.querySelector('#myCollection');
            collectionDiv.innerHTML = data.collection_list;
            var toastEl = document.getElementById('deleteToMyCollectionToast');
            var cards = document.querySelectorAll("a[checked='true']");
            for (var i = 0; i < cards.length; i++) { 
                cards[i].setAttribute("checked", "false");
            }
            SHOW_EDIT_TAGS = false;
            render();
        }
        else{
            var toastEl = document.getElementById('addToMyCollectionToast');
        }
        toast = new bootstrap.Toast(toastEl);
        toast.show();
    })
    .catch(err => {
    // gestion des erreurs
     });
}