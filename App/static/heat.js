document.addEventListener("DOMContentLoaded", function() {
    
    const svg = document.getElementById('kitchen-scale-svg');


    function getColorFromTemp(percentage) {
        //console.log(percentage)
        const startColor = { r: 0, g: 0, b: 255 }; // Blue
        const endColor = { r: 255, g: 0, b: 0 }; // Red
    
        const r = Math.round(startColor.r + (endColor.r - startColor.r) * (percentage / 250));
        const g = Math.round(startColor.g + (endColor.g - startColor.g) * (percentage / 250));
        const b = Math.round(startColor.b + (endColor.b - startColor.b) * (percentage / 250));
    
        return `rgb(${r}, ${g}, ${b})`;
    }
    function getShadedColorFromTemp(percentage) {
        //console.log(percentage)
        const startColor = { r: 0, g: 0, b: 255 }; // Blue
        const endColor = { r: 255, g: 0, b: 0 }; // Red
    
        const r = Math.round(startColor.r + (endColor.r - startColor.r) * (percentage / 250));
        const g = Math.round(startColor.g + (endColor.g - startColor.g) * (percentage / 250));
        const b = Math.round(startColor.b + (endColor.b - startColor.b) * (percentage / 250));
    
        return `rgba(${r}, ${g}, ${b}, 0.5)`;
    }

    
    
    window.onload = function() {
        
        
        

        const drawScaleLine = (unadjustedAngle) => {
            angle = unadjustedAngle + 240;
            const x1 = radius + (radius - 14) * Math.cos((angle - 90) * Math.PI / 180);
            const y1 = radius + (radius - 14) * Math.sin((angle - 90) * Math.PI / 180);
            const x2 = radius + (radius - 26) * Math.cos((angle - 90) * Math.PI / 180);
            const y2 = radius + (radius - 26) * Math.sin((angle - 90) * Math.PI / 180);
            
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', x1);
            line.setAttribute('y1', y1);
            line.setAttribute('x2', x2);
            line.setAttribute('y2', y2);
            line.setAttribute('stroke', getShadedColorFromTemp(unadjustedAngle));
            line.setAttribute('stroke-width', '4');
    
            svg.appendChild(line);
        };

        
    
        function drawScale() {
            for (let i = 0; i < 25; i++) {
                drawScaleLine(i * 10);
            }
        }
    
        drawScale();
    
    };
    
    
    
    
    
    
    const knob = document.getElementById('knob');
    const circle = document.getElementById('circle');
    const container = document.querySelector('.slider-container');
    const radius = container.clientWidth / 2;
    const knobRadius = knob.clientWidth / 2;


    const removeDrawnScale = () => {
        let svg = document.getElementById("tempscale");
        while (svg) {
            svg.parentNode.removeChild(svg);
            svg = document.getElementById("tempscale");
    }
    }
    const drawScaleLine = (scaledangle) => {
        let finalAngle = 0;
        if (scaledangle > 240) {
            finalAngle = scaledangle - 240;
        }
        else if (scaledangle < 120) {
            finalAngle = scaledangle + 120
        }
        else return;
        removeDrawnScale();
        for (let i = 0; i < finalAngle; i++) {
            let adjustedangle = i - 120
            const x1 = radius + (radius - 14) * Math.cos((adjustedangle - 90) * Math.PI / 180);
            const y1 = radius + (radius - 14) * Math.sin((adjustedangle - 90) * Math.PI / 180);
            const x2 = radius + (radius - 26) * Math.cos((adjustedangle - 90) * Math.PI / 180);
            const y2 = radius + (radius - 26) * Math.sin((adjustedangle - 90) * Math.PI / 180);
            
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', x1);
            line.setAttribute('y1', y1);
            line.setAttribute('x2', x2);
            line.setAttribute('y2', y2);
            line.setAttribute('stroke', getColorFromTemp(i));
            line.setAttribute('stroke-width', '4');
            line.setAttribute('id', 'tempscale')

            svg.appendChild(line);
        }
        
    };
    


    const setKnobPosition = (angle) => {
        if (angle > 120 && angle < 240){return};
        const x = radius + (radius - 30) * Math.cos((angle - 90) * Math.PI / 180);
        const y = radius + (radius - 30) * Math.sin((angle - 90) * Math.PI / 180);
        knob.style.left = `${x}px`; // Adjust for knob's width
        knob.style.top = `${y}px`;  // Adjust for knob's height
        knob.style.transform = `translate(-50%, -100%) rotate(${angle}deg)`;
    };

    const updateKnobPosition = (event) => {
        const rect = container.getBoundingClientRect();
        const centerX = rect.left + radius;
        const centerY = rect.top + radius;

        const x = event.clientX - centerX;
        const y = event.clientY - centerY;

        let angle = (Math.atan2(y, x) * (180 / Math.PI)) + 90;
        if (angle < 0) {angle = 360 + angle}

        let scaledangle = angle;
        
        console.log(scaledangle)
        //console.log(scaledangle)
        //scaledangle = 180 - scaledangle
        //console.log(angle, scaledangle)
        //angle = angle + 90;
        if (angle < 0) angle += 360;

        setKnobPosition(scaledangle);
        //console.log('Slider angle:', angle); // Logs the slider angle
        drawScaleLine(scaledangle)
    };
    

    // Add event listener to the whole circle container
    circle.addEventListener('mousedown', (event) => {
        updateKnobPosition(event);
        document.addEventListener('mousemove', updateKnobPosition);
    });

    document.addEventListener('mouseup', () => {
        document.removeEventListener('mousemove', updateKnobPosition);
    });

    // Initialize knob position at the top
    setKnobPosition(0);
});