// TeleAcolhe - JavaScript do Formul\u00e1rio Multi-Etapas

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('symptomsForm');
    const steps = document.querySelectorAll('.form-step');
    const progressSteps = document.querySelectorAll('.progress-step');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const submitBtn = document.getElementById('submitBtn');
    const progressBar = document.querySelector('.progress-indicator');
    
    let currentStep = 1;
    const totalSteps = steps.length;
    
    // Inicializa os \u00edcones do Feather
    feather.replace();
    
    // Fun\u00e7\u00e3o para mostrar a etapa atual
    function showStep(stepNumber) {
        steps.forEach((step, index) => {
            if (index + 1 === stepNumber) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });
        
        // Atualiza o indicador de progresso
        progressSteps.forEach((step, index) => {
            if (index + 1 <= stepNumber) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });
        
        // Atualiza aria-valuenow para acessibilidade
        if (progressBar) {
            progressBar.setAttribute('aria-valuenow', stepNumber);
        }
        
        // Controla a visibilidade dos bot\u00f5es
        if (stepNumber === 1) {
            prevBtn.style.display = 'none';
        } else {
            prevBtn.style.display = 'inline-flex';
        }
        
        if (stepNumber === totalSteps) {
            nextBtn.style.display = 'none';
            submitBtn.style.display = 'inline-flex';
        } else {
            nextBtn.style.display = 'inline-flex';
            submitBtn.style.display = 'none';
        }
        
        // Rola para o topo do formul\u00e1rio
        form.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Foca no primeiro campo da etapa
        const firstInput = steps[stepNumber - 1].querySelector('input, select, textarea');
        if (firstInput) {
            setTimeout(() => firstInput.focus(), 300);
        }
        
        // Atualiza os \u00edcones
        feather.replace();
    }
    
    // Fun\u00e7\u00e3o para validar a etapa atual
    function validateStep(stepNumber) {
        const currentStepElement = steps[stepNumber - 1];
        const inputs = currentStepElement.querySelectorAll('input, select, textarea');
        let isValid = true;
        
        inputs.forEach(input => {
            const errorMessage = input.parentElement.querySelector('.error-message');
            
            // Limpa mensagens de erro anteriores
            if (errorMessage) {
                errorMessage.textContent = '';
            }
            
            // Valida campos obrigat\u00f3rios
            if (input.hasAttribute('required')) {
                if (input.type === 'radio') {
                    const radioGroup = currentStepElement.querySelectorAll(`input[name="${input.name}"]`);
                    const isChecked = Array.from(radioGroup).some(radio => radio.checked);
                    
                    if (!isChecked) {
                        isValid = false;
                        if (errorMessage) {
                            errorMessage.textContent = 'Por favor, selecione uma op\u00e7\u00e3o.';
                        }
                    }
                } else if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('error');
                    if (errorMessage) {
                        errorMessage.textContent = 'Este campo \u00e9 obrigat\u00f3rio.';
                    }
                } else {
                    input.classList.remove('error');
                }
                
                // Valida\u00e7\u00f5es espec\u00edficas
                if (input.type === 'number' && input.value) {
                    const value = parseInt(input.value);
                    const min = parseInt(input.getAttribute('min'));
                    const max = parseInt(input.getAttribute('max'));
                    
                    if (value < min || value > max) {
                        isValid = false;
                        input.classList.add('error');
                        if (errorMessage) {
                            errorMessage.textContent = `Por favor, insira um valor entre ${min} e ${max}.`;
                        }
                    }
                }
                
                // Valida textarea m\u00ednimo
                if (input.tagName === 'TEXTAREA' && input.value.trim().length < 10) {
                    isValid = false;
                    input.classList.add('error');
                    if (errorMessage) {
                        errorMessage.textContent = 'Por favor, forne\u00e7a uma descri\u00e7\u00e3o mais detalhada (m\u00ednimo 10 caracteres).';
                    }
                }
            }
        });
        
        return isValid;
    }
    
    // Evento do bot\u00e3o "Pr\u00f3ximo"
    nextBtn.addEventListener('click', function() {
        if (validateStep(currentStep)) {
            if (currentStep < totalSteps) {
                currentStep++;
                showStep(currentStep);
            }
        } else {
            // Foca no primeiro campo com erro
            const errorInput = steps[currentStep - 1].querySelector('.error, input:invalid');
            if (errorInput) {
                errorInput.focus();
            }
        }
    });
    
    // Evento do bot\u00e3o "Voltar"
    prevBtn.addEventListener('click', function() {
        if (currentStep > 1) {
            currentStep--;
            showStep(currentStep);
        }
    });
    
    // Contador de caracteres para textarea de sintomas
    const symptomsTextarea = document.getElementById('symptoms');
    const charCount = document.getElementById('charCount');
    
    if (symptomsTextarea && charCount) {
        symptomsTextarea.addEventListener('input', function() {
            charCount.textContent = this.value.length;
        });
    }
    
    // Valida\u00e7\u00e3o em tempo real
    const allInputs = form.querySelectorAll('input, select, textarea');
    allInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const errorMessage = this.parentElement.querySelector('.error-message');
            
            if (this.hasAttribute('required') && !this.value.trim() && this.type !== 'radio') {
                this.classList.add('error');
                if (errorMessage) {
                    errorMessage.textContent = 'Este campo \u00e9 obrigat\u00f3rio.';
                }
            } else {
                this.classList.remove('error');
                if (errorMessage) {
                    errorMessage.textContent = '';
                }
            }
        });
        
        // Remove erro ao come\u00e7ar a digitar
        input.addEventListener('input', function() {
            this.classList.remove('error');
            const errorMessage = this.parentElement.querySelector('.error-message');
            if (errorMessage) {
                errorMessage.textContent = '';
            }
        });
    });
    
    // Valida\u00e7\u00e3o final ao submeter
    form.addEventListener('submit', function(e) {
        let allValid = true;
        
        for (let i = 1; i <= totalSteps; i++) {
            if (!validateStep(i)) {
                allValid = false;
                currentStep = i;
                showStep(currentStep);
                break;
            }
        }
        
        if (!allValid) {
            e.preventDefault();
            alert('Por favor, preencha todos os campos obrigat\u00f3rios corretamente.');
        } else {
            // Mostra feedback de carregamento
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<svg class="animate-spin" style="width: 18px; height: 18px;" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Analisando...';
        }
    });
    
    // Permite navega\u00e7\u00e3o com Enter (exceto em textarea)
    form.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
            e.preventDefault();
            if (currentStep < totalSteps) {
                nextBtn.click();
            } else {
                submitBtn.click();
            }
        }
    });
    
    // Inicializa na primeira etapa
    showStep(currentStep);
});
