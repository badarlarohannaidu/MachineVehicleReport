document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');

    form.addEventListener('submit', function(event) {
        // Prevent the default form submission
        event.preventDefault();

        // Gather all form inputs
        const machineName = document.getElementById('name').value.trim();
        const date = document.querySelector('input[type="date"]').value;
        const shift = document.querySelector('input[name="shift"]:checked');
        const unitStart = parseInt(document.getElementById('smu').value, 10);
        const unitEnd = parseInt(document.getElementById('emu').value, 10);
        const location = document.getElementById('location').value.trim();
        const nature = document.getElementById('nature').value.trim();
        const startTime = document.getElementById('start-time').value;
        const endTime = document.getElementById('end-time').value;
        const quant=document.getElementById('quantity').value;
        const quantunits=document.querySelector('input[name="quanunits"]:checked');;
        let valid = true;

        // Validate time inputs
        // if (startTime && endTime && startTime >= endTime) {
        //     alert('Start time must be before end time');
        //     valid = false;
        // }

        // Calculate total units used
        const totalUnits = unitEnd - unitStart;
        if (totalUnits < 0) {
            alert('Ending Measuring Unit must be greater than or equal to Starting Measuring Unit');
            valid = false;
        }
        if(quant!=0){
            if(quantunits){}
            else{ alert('Put proper units for quanity');
                valid=false;}
        }
        if (valid) {
            // Form data is valid, proceed with form submission
            alert('Form submitted successfully');
            form.submit(); // Continue with form submission
        }
    });
});
