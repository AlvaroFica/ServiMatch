let currentStep = 1;

function nextStep(step) {
    document.getElementById('step-' + currentStep).classList.remove('active');
    currentStep = step + 1;
    document.getElementById('step-' + currentStep).classList.add('active');
}

function prevStep(step) {
    document.getElementById('step-' + currentStep).classList.remove('active');
    currentStep = step - 1;
    document.getElementById('step-' + currentStep).classList.add('active');
}

document.addEventListener("DOMContentLoaded", function() {
    // Mostrar el primer paso al cargar la página
    document.getElementById('step-1').classList.add('active');
});
