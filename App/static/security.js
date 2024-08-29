const ws = new WebSocket(URI.URI);

var code_input = [];
var code_string = "_ _ _ _";


        ws.onopen = () => {
            console.log("Connected to the WebSocket server");
            ws.send(`{"operation":"reload","page":"${document.getElementById("page").getAttribute("data-page")}"}`);
        };
        
        function SendCommandMessage(room,value) {
            console.log(`{"operation":"client_update_blinds", "page":"blinds","num_entities":0,"num_server_entities":1,"entities":[{"entity":"${room}-blind-command", "value":${value}}]}`)

            ws.send(`{"operation":"client_update_blinds", "page":"blinds","num_entities":0,"num_server_entities":1,"entities":[{"entity":"${room}-blind-command", "value":${value}}]}`)
        }


function ShowMenu() {
    var items = document.getElementsByClassName('menu')
    for(var i = 0; i < items.length; i++) {
        items[i].style.visibility = 'visible'
    }
    items = document.getElementsByClassName('lock')
    for(var i = 0; i < items.length; i++) {
        items[i].style.visibility = 'hidden'
    }
}

function KeyPress(input) {
    if (input == 'enter' && code_input.length >= 4) {
        ShowMenu()
        if (code_input == code) {
            code_input = []
            
        }
    }
    else {
    if (input == 'del' || input == 'enter') {
        if (input == 'del') {
            code_input = []
        }
    }
    else {
        code_input = code_input.concat(input)
    }
    var empty_list = ['_','_','_','_']

    

    for(var i = 0; i < code_input.length; i++) {
        empty_list[i] = code_input[i]
    }
    code_string = `${empty_list[0]} ${empty_list[1]} ${empty_list[2]} ${empty_list[3]}`
    //console.log(number)
    document.getElementById('keypad-text-input').textContent = code_string
    console.log(code_input)
    console.log(code_string)
    }
}

ws.onmessage = (event) => {
    const obj = JSON.parse(event.data);
    if (obj.page == "security") {
        const num_entities = obj.num_entities;
        for (let i = 0; i < num_entities; i++) {
            const entity = obj.entities[i].entity;
            const value = obj.entities[i].state;
            //console.log(`${entity}-icon`);
            //console.log(document.getElementById(`${entity}-icon`).style);
            console.log(entity)
            document.getElementById(`${entity}`).value = value
            UpdateAllBlinds()
            console.log(`${entity} is set to ${value}`);
        }
    } 
    
};