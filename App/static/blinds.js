
const ws = new WebSocket("ws://192.168.1.130:6789");
        ws.onopen = () => {
            console.log("Connected to the WebSocket server");
            ws.send(`{"reload":1,"page":"blinds"}`);
        };
        
        ws.onmessage = (event) => {
            const obj = JSON.parse(event.data);
            const num_entities = obj.num_entities;
            if (num_entities == 1) {
                    const entity = obj.entities[0].entity;
                    const value = obj.entities[0].state;
                    
                    document.getElementById(`${entity}`).value= value
                    console.log(entity);
                    console.log(value);
                    
            }
            
            else {
                for (let i = 0; i < num_entities; i++) {
                    const entity = obj.entities[i].entity;
                    const value = obj.entities[i].state;
                    //console.log(`${entity}-icon`);
                    //console.log(document.getElementById(`${entity}-icon`).style);
                    document.getElementById(`${entity}`).value= value
                    console.log(value);
                }
            }
            
            
            
            
            
        };

        function toggleLight(entity) {
            let state = 0
            if (document.getElementById(`${entity}-state`).innerText == "On") {state = 0}else {state = 1};
            ws.send(`{"num_entities":0,"num_server_entities":1,"entities":[{"entity":"${entity}","state":${state}}],"reload":0,"page":"${document.getElementById("page").getAttribute("data-page")}"}`);
        }
        document.addEventListener('DOMContentLoaded', () => {
            const slider1 = document.getElementById('sitting-room-blind-command');
            const slider2 = document.getElementById('sitting-room-blind-state');
            const line1 = document.getElementById('line1');
            const line2 = document.getElementById('line2');

            function UpdateBlinds() {
                console.log("updating");
                const containerRect = document.getElementById('test').getBoundingClientRect();
                const slider1Rect = slider1.getBoundingClientRect();
                const slider2Rect = slider2.getBoundingClientRect();

                const slider1Y = window.innerHeight * 0.25 + ((100 - slider1.valueAsNumber) / slider1.max * slider1Rect.height);
                
                const slider2X = slider2Rect.left + slider2.valueAsNumber / slider2.max * slider2Rect.width;
                const slider2Y = slider2Rect.top + slider2Rect.height / 2;
                
                console.log(slider1Y)
                line1.setAttribute('y2', slider1Y);
                line2.setAttribute('x2', slider2X);
                line2.setAttribute('y2', slider2Y);
            }

            slider1.addEventListener('input', UpdateBlinds);
            slider2.addEventListener('input', UpdateBlinds);

            window.addEventListener('resize', UpdateBlinds);
            window.addEventListener('load', UpdateBlinds);
        });