
const ws = new WebSocket("ws://192.168.1.130:6789");
        ws.onopen = () => {
            console.log("Connected to the WebSocket server");
            ws.send(`{"reload":1,"page":"${document.getElementById("page").getAttribute("data-page")}"}`);
        };
        ws.onclose = (event) => {
            ws.send(`colese`);
            console.log('The connection has been closed successfully.');
            };
        ws.onmessage = (event) => {
            const obj = JSON.parse(event.data);
            const num_entities = obj.num_entities;
            if (obj.page == "energy") {
        
                for (let i = 0; i < num_entities; i++) {
                    const entity = obj.entities[i].entity;
                    const value = obj.entities[i].state;
                    //console.log(`${entity}-icon`);
                    //console.log(document.getElementById(`${entity}-icon`).style);
                    //console.log(entity);
                    document.getElementById(`${entity}`).textContent = value
                    //
                    
                    //console.log(state);
                }
                
            }
            else if (obj.page == document.getElementById("page").getAttribute("data-page")) {
                if (num_entities == 1) {
                    const entity = obj.entities[0].entity;
                    const state = obj.entities[0].state;
                    
                    document.getElementById(`${entity}-icon`).style= state ? "background-color: yellow" : "background-color: rgb(95,95,95)" ;
                    document.getElementById(`${entity}-state`).innerText= state ? "On" : "Off" ;
                    //console.log(entity);
                    //console.log(state);
                    
                }
                
                else {
                    for (let i = 0; i < num_entities; i++) {
                        const entity = obj.entities[i].entity;
                        const state = obj.entities[i].state;
                        //console.log(`${entity}-icon`);
                        //console.log(document.getElementById(`${entity}-icon`).style);
                        document.getElementById(`${entity}-icon`).style= state ? "background-color: yellow" : "background-color: rgb(95,95,95)" ;
                        document.getElementById(`${entity}-state`).innerText= state ? "On" : "Off" ;
                        //console.log(entity);
                        //console.log(state);
                    }
                }
            }
            
            
            
            
        };

        function toggleLight(entity) {
            let state = 0
            if (document.getElementById(`${entity}-state`).innerText == "On") {state = 0}else {state = 1};
            ws.send(`{"num_entities":0,"num_server_entities":1,"entities":[{"entity":"${entity}","state":${state}}],"reload":0,"page":"${document.getElementById("page").getAttribute("data-page")}"}`);
        }
       