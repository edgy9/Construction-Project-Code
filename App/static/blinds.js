
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
            const SittingRoomBlindCommandSlider = document.getElementById('sitting-room-blind-command');
            const SittingRoomBlindStateSlider = document.getElementById('sitting-room-blind-state');
            const SittingRoomBlindCommandLine = document.getElementById('sitting-room-blind-command-line');
            const SittingRoomBlindStateLine = document.getElementById('sitting-room-blind-state-line');
            const SittingRoomBlindRoller = document.getElementById('sitting-room-blind-roller');
            const SittingRoomBlindRollerInner = document.getElementById('sitting-room-blind-roller-inner');

            function UpdateBlinds() {
                const SittingRoomSliderContainer = document.getElementById('sitting-room-slider-container').getBoundingClientRect();
                const SittingRoomSVGContainer = document.getElementById('sitting-room-svg-container').getBoundingClientRect();
                const SittingRoomBlindCommandRect = SittingRoomBlindCommandSlider.getBoundingClientRect();
                const SittingRoomBlindStateRect = SittingRoomBlindStateSlider.getBoundingClientRect();


            /*                       ------- Set Slider Stuff -------                       */


                SittingRoomBlindCommandSlider.style.width = SittingRoomSliderContainer.height + "px"
                SittingRoomBlindStateSlider.style.width = SittingRoomSliderContainer.height + "px"

            /*                       ------- Set Command Line Stuff -------                       */

                const SittingRoomBlindCommandLineY1 = window.innerHeight * 0.28;
                const SittingRoomBlindCommandLineY2 = window.innerHeight * 0.28 + ((100 - SittingRoomBlindCommandSlider.valueAsNumber) / SittingRoomBlindCommandSlider.max * SittingRoomBlindCommandRect.height);
                const SittingRoomBlindCommandLineX = ((SittingRoomSVGContainer.width * 0.5)+12) + "px"

                SittingRoomBlindCommandLine.setAttribute('y1', SittingRoomBlindCommandLineY1);
                SittingRoomBlindCommandLine.setAttribute('y2', SittingRoomBlindCommandLineY2);
                SittingRoomBlindCommandLine.setAttribute('x1', SittingRoomBlindCommandLineX);
                SittingRoomBlindCommandLine.setAttribute('x2', SittingRoomBlindCommandLineX);

            /*                       ------- Set State Line Stuff -------                       */

            const SittingRoomBlindStateLineY1 = window.innerHeight * 0.30;
            const SittingRoomBlindStateLineY2 = window.innerHeight * 0.30 + ((100 - SittingRoomBlindStateSlider.valueAsNumber) / SittingRoomBlindStateSlider.max * SittingRoomBlindStateRect.height);
            const SittingRoomBlindStateLineX = ((SittingRoomSVGContainer.width * 0.5)+12) + "px"

            SittingRoomBlindStateLine.setAttribute('y1', SittingRoomBlindStateLineY1);
            SittingRoomBlindStateLine.setAttribute('y2', SittingRoomBlindStateLineY2);
            SittingRoomBlindStateLine.setAttribute('x1', SittingRoomBlindStateLineX);
            SittingRoomBlindStateLine.setAttribute('x2', SittingRoomBlindStateLineX);
            
            /*                       ------- Set Roller Circles Stuff -------                       */
            const SittingRoomBlindRollerY = window.innerHeight * 0.28;
            const SittingRoomBlindRollerX = ((SittingRoomSVGContainer.width * 0.5)-5) + "px";
            

            SittingRoomBlindRoller.setAttribute('cx', SittingRoomBlindRollerX);
            SittingRoomBlindRoller.setAttribute('cy', SittingRoomBlindRollerY);
            SittingRoomBlindRollerInner.setAttribute('cx', SittingRoomBlindRollerX);
            SittingRoomBlindRollerInner.setAttribute('cy', SittingRoomBlindRollerY);
            
            }
            SittingRoomBlindCommandSlider.addEventListener('input', UpdateBlinds);
            SittingRoomBlindStateSlider.addEventListener('input', UpdateBlinds);

            window.addEventListener('resize', UpdateBlinds);
            window.addEventListener('load', UpdateBlinds);
            
        });