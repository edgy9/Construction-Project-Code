 console
const ws = new WebSocket(URI.URI);
        ws.onopen = () => {
            console.log("Connected to the WebSocket server");
            ws.send(`{"operation":"reload","page":"blinds"}`);
        };
        
        function SendCommandMessage(room,value) {
            console.log(`{"operation":"client_update_blinds", "page":"blinds","num_entities":0,"num_server_entities":1,"entities":[{"entity":"${room}-blind-command", "value":${value}}]}`)

            ws.send(`{"operation":"client_update_blinds", "page":"blinds","num_entities":0,"num_server_entities":1,"entities":[{"entity":"${room}-blind-command", "value":${value}}]}`)
        }


   
        document.addEventListener('DOMContentLoaded', () => {
            const SittingRoomBlindCommandSlider = document.getElementById(`sitting-room-blind-command`);
            const SittingRoomBlindStateSlider = document.getElementById(`sitting-room-blind-state`);
            const SittingRoomOuterSection = document.getElementById('sitting-room-main-blind-container');
            const SittingRoomInnerSection = document.getElementById('sitting-room-blind-container');
            const SkylightBlindCommandSlider = document.getElementById(`skylight-blind-command`);
            const SkylightBlindStateSlider = document.getElementById(`skylight-blind-state`);
            const SkylightOuterSection = document.getElementById('skylight-main-blind-container');
            const SkylightInnerSection = document.getElementById('skylight-blind-container');
            const KitchenBlindCommandSlider = document.getElementById(`kitchen-blind-command`);
            const KitchenBlindStateSlider = document.getElementById(`kitchen-blind-state`);
            const KitchenOuterSection = document.getElementById('kitchen-main-blind-container');
            const KitchenInnerSection = document.getElementById('kitchen-blind-container');

           
            function UpdateBlind(room) {
                DrawBlindLine(room)


            }
            function DrawBlindLine(room) {
                const BlindCommandSlider = document.getElementById(`${room}-blind-command`);
                const BlindStateSlider = document.getElementById(`${room}-blind-state`);
                const BlindCommandLine = document.getElementById(`${room}-blind-command-line`);
                const BlindStateLine = document.getElementById(`${room}-blind-state-line`);
                const BlindRoller = document.getElementById(`${room}-blind-roller`);
                const BlindRollerInner = document.getElementById(`${room}-blind-roller-inner`);
                const SliderContainer = document.getElementById(`${room}-slider-container`).getBoundingClientRect();
                const SVGContainer = document.getElementById(`${room}-svg-container`).getBoundingClientRect();
                const BlindCommandRect = BlindCommandSlider.getBoundingClientRect();
                const BlindStateRect = BlindStateSlider.getBoundingClientRect();
                
            /*                       ------- Set Slider Stuff -------                       */


                BlindCommandSlider.style.width = (SliderContainer.height - 25) + "px"
                BlindStateSlider.style.width = (SliderContainer.height - 25) + "px"

            /*                       ------- Set State Line Stuff -------                       */

            const BlindStateLineY1 = window.innerHeight * 0.28;
            const BlindStateLineY2 = window.innerHeight * 0.317 + ((100 - BlindStateSlider.valueAsNumber) / 100 * BlindStateRect.height);
            const BlindStateLineX = ((SVGContainer.width * 0.5)+12) + "px"

            BlindStateLine.setAttribute('y1', BlindStateLineY1);
            BlindStateLine.setAttribute('y2', BlindStateLineY2);
            BlindStateLine.setAttribute('x1', BlindStateLineX);
            BlindStateLine.setAttribute('x2', BlindStateLineX);
            
            /*                       ------- Set Command Line Stuff -------                       */

                const BlindCommandLineY1 = window.innerHeight * 0.28;
                const BlindCommandLineY2 = window.innerHeight * 0.317 + ((100 - BlindCommandSlider.valueAsNumber) / 100 * BlindCommandRect.height);
                const BlindCommandLineX = ((SVGContainer.width * 0.5)+12) + "px"

                BlindCommandLine.setAttribute('y1', BlindCommandLineY1);
                BlindCommandLine.setAttribute('y2', BlindCommandLineY2);
                BlindCommandLine.setAttribute('x1', BlindCommandLineX);
                BlindCommandLine.setAttribute('x2', BlindCommandLineX);

            
            
            /*                       ------- Set Roller Circles Stuff -------                       */
            const BlindRollerY = window.innerHeight * 0.28;
            const BlindRollerX = ((SVGContainer.width * 0.5)-5) + "px";
            

            BlindRoller.setAttribute('cx', BlindRollerX);
            BlindRoller.setAttribute('cy', BlindRollerY);
            BlindRollerInner.setAttribute('cx', BlindRollerX);
            BlindRollerInner.setAttribute('cy', BlindRollerY);
            //console.log("there")
            
            }


            function UpdateAllBlinds() {
                UpdateBlind("sitting-room")
                UpdateBlind("kitchen")
                UpdateBlind("skylight")
                //console.log("updating all blinds")


            }
            function InputUpdate(room) {

                SendCommandMessage(room,document.getElementById(`${room}-blind-command`).valueAsNumber)
                UpdateBlind(room)
            }
            SittingRoomBlindCommandSlider.addEventListener('input', () => InputUpdate("sitting-room"));
            KitchenBlindCommandSlider.addEventListener('input', () => InputUpdate("kitchen"));
            SkylightBlindCommandSlider.addEventListener('input', () => InputUpdate("skylight"));
            

            
            //window.addEventListener('resize', print);
            //.onresize = resizedelay(UpdateAllBlinds, 500)
            //window.addEventListener('resize', debounce(UpdateAllBlinds, 600, true));

    
            window.addEventListener('resize', UpdateAllBlinds);
            window.addEventListener('load', UpdateAllBlinds);
            //document.addEventListener('fullscreenchange', UpdateAllBlinds);
            //document.addEventListener('webkitfullscreenchange', UpdateAllBlinds);
            //document.addEventListener('mozfullscreenchange', UpdateAllBlinds);
            //document.addEventListener('MSFullscreenChange', UpdateAllBlinds);
            

            ws.onmessage = (event) => {
                const obj = JSON.parse(event.data);
                if (obj.page == "blinds") {
                    const num_entities = obj.num_entities;
                    for (let i = 0; i < num_entities; i++) {
                        const entity = obj.entities[i].entity;
                        const value = obj.entities[i].state;
                        //console.log(`${entity}-icon`);
                        //console.log(document.getElementById(`${entity}-icon`).style);
                        slider = document.getElementById(`${entity}`)
                        slider.value = value
                        slider.style.display = 'none';
                        slider.offsetHeight; // trigger reflow
                        slider.style.display = '';
                        UpdateAllBlinds()
                        console.log(`${entity} is set to ${value}`);
                    }
                } 
            };
            
            const SectionClick = (event, device) => {
                const container = document.getElementById(`${device}-blind-container`);
                const rect = container.getBoundingClientRect();
        
                const y = event.clientY - rect.top;
                const boxHeight = (rect.bottom - rect.top);
                const ratio = Math.abs(((y / boxHeight) * 100) - 100);
                if (ratio < 6) {
                    SendCommandMessage(device, 0);
                }
                else if (ratio > 84) {
                    SendCommandMessage(device, 100);
                }
                else {
                    innerY = y - (0.16 * boxHeight);
                    innerBoxHeight = (0.78 * boxHeight);
                    innerRatio = Math.round(Math.abs(((innerY / innerBoxHeight) * 100) - 100));
                    SendCommandMessage(device, innerRatio)
                }
            };
            

            SittingRoomOuterSection.addEventListener('mousedown', (event) => {
                SectionClick(event, 'sitting-room');
                
            });
            SittingRoomInnerSection.addEventListener('mousedown', (event) => {
                SectionClick(event, 'sitting-room');
                
            });
            KitchenOuterSection.addEventListener('mousedown', (event) => {
                SectionClick(event, 'kitchen');
                
            });
            KitchenInnerSection.addEventListener('mousedown', (event) => {
                SectionClick(event, 'kitchen');
                
            });
            SkylightOuterSection.addEventListener('mousedown', (event) => {
                SectionClick(event, 'skylight');
                
            });
            SkylightInnerSection.addEventListener('mousedown', (event) => {
                SectionClick(event, 'skylight');
                
            });

        });

        
     