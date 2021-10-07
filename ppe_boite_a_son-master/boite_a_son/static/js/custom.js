function get_selected_rows(btn_required_selected)
{
    var selected_rows = [];
    var checkedrows = document.querySelectorAll("a[checked='true']");
    for (var i = 0; i < checkedrows.length; i++) { 
        selected_rows.push(checkedrows[i].getAttribute("data-id"));
        }

    for (var i =0;i<btn_required_selected.length;i++)
    {
        button_id = btn_required_selected[i];
        if (selected_rows.length > 0)
        {
            document.getElementById(button_id).classList.remove('d-none');
        }
        else
        {
            document.getElementById(button_id).classList.add('d-none');
        }
    }
    return selected_rows;
}

function set_href(typename,query_string)
{
    var Item = document.querySelectorAll("."+typename+"-item");
    for (var i = 0; i < Item.length; i++) 
        {
        id = Item[i].getAttribute("data-id")
        Item[i].setAttribute("href","add"+typename+"/"+id+"?"+query_string);
        }
    document.getElementById(typename+"-delete").setAttribute("href","clear"+typename+"?"+query_string);
}

function init_table_ui(id,render)
{
    var elements = document.getElementsByClassName("row_selector");
    for (var i = 0; i < elements.length; i++) {
        elements[i].addEventListener('click', render, false);
    }
}

function post(path, params, method='post') {

    // The rest of this code assumes you are not using a library.
    // It can be made less verbose if you use one.
    const form = document.createElement('form');
    form.method = method;
    form.action = path;
    
    for (const key in params) {
        if (params.hasOwnProperty(key)) {
        const hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = key;
        hiddenField.value = params[key];
    
        form.appendChild(hiddenField);
        }
    }
    
    document.body.appendChild(form);
    form.submit();
}

function readFile(file) {
    const temporaryFileReader=new FileReader();

    return new Promise((resolve, reject) => {
        temporaryFileReader.onerror=() => {
            temporaryFileReader.abort();
            reject(new DOMException("Problem parsing input file."));
        };

        temporaryFileReader.onload=() => {
            resolve(temporaryFileReader.result);
        };
        temporaryFileReader.readAsArrayBuffer(file);
    });
}

function getStringifyBuffers(urlList){
    return new Promise((resolve, reject)=>{
        var result=[];
        urlList.forEach(async function (sample) {
            var file = await fetch("https://vlmboiteason.s3.amazonaws.com/static/media/"+sample.file
                ).then(response => response.blob()
                ).then(blobFile => new File([blobFile], "test.wav", {type: "audio/wav"}))
            var buffer = new Uint16Array(await readFile(file));
            var ser_buffer = '';
            buffer.forEach(charCode => {
                ser_buffer+=String.fromCharCode(charCode);
            });
            result.push(ser_buffer);
            if (result.length==urlList.length) {
                resolve(result);
            }
        })
    })
}

function str2ab(str) {
    var buf = new ArrayBuffer(str.length*2); // 2 bytes for each char
    var bufView = new Uint16Array(buf);
    for (var i=0, strLen=str.length; i < strLen; i++) {
        bufView[i] = str.charCodeAt(i);
    }
    return buf;
}

function storageAvailable(type) {
    try {
        var storage = window[type],
            x = '__storage_test__';
        storage.setItem(x, x);
        storage.removeItem(x);
        return true;
    }
    catch(e) {
        return e instanceof DOMException && (
            // everything except Firefox
            e.code === 22 ||
            // Firefox
            e.code === 1014 ||
            // test name field too, because code might not be present
            // everything except Firefox
            e.name === 'QuotaExceededError' ||
            // Firefox
            e.name === 'NS_ERROR_DOM_QUOTA_REACHED') &&
            // acknowledge QuotaExceededError only if there's something already stored
            storage.length !== 0;
    }
}
