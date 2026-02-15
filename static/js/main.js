document.addEventListener("DOMContentLoaded", function() {
    console.log("CyberGuard Toolkit Loaded");

    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Auto-dismiss alerts
    setTimeout(function() {
        let alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(alert => {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // START BINARY RAIN
    createBinaryRain();
});

function createBinaryRain() {
    const container = document.getElementById('binary-rain');
    if (!container) return;

    // --- DENSITY SETTING ---
    // 30 = Clean, Spread out look
    const densityModifier = 30; 
    const streamCount = Math.floor(window.innerWidth / densityModifier);

    container.innerHTML = ''; // Clear previous

    for (let i = 0; i < streamCount; i++) {
        const stream = document.createElement('div');
        stream.classList.add('binary-stream');
        
        // Random binary string
        let binaryString = "";
        const length = Math.floor(Math.random() * 25) + 10; 
        for (let j = 0; j < length; j++) {
            if (Math.random() > 0.8) {
                binaryString += " "; // Gaps
            } else {
                binaryString += Math.random() > 0.5 ? "1" : "0";
            }
        }
        stream.innerText = binaryString;

        // Positioning
        stream.style.left = (i * densityModifier) + 'px'; 
        stream.style.fontSize = (Math.floor(Math.random() * 6) + 16) + 'px'; 
        
        // --- SPEED SETTING ---
        // 8s-15s = Very Slow and Atmospheric
        const duration = (Math.random() * 7 + 8) + 's'; 
        const delay = (Math.random() * 5) + 's';
        
        stream.style.animationDuration = duration;
        stream.style.animationDelay = delay;
        
        // Varied Opacity
        stream.style.opacity = Math.random() * 0.5 + 0.3; 

        container.appendChild(stream);
    }
}

// Re-calc rain on resize
window.addEventListener("resize", () => {
    createBinaryRain();
});

// Clipboard Helper
function copyToClipboard(elementId) {
    var copyText = document.getElementById(elementId);
    if(copyText) {
        copyText.select();
        copyText.setSelectionRange(0, 99999);
        navigator.clipboard.writeText(copyText.value).then(() => {
            const btn = document.activeElement;
            if(btn) {
                const originalText = btn.innerHTML;
                btn.innerHTML = '<i class="bi bi-check-lg"></i>';
                btn.classList.add('btn-success');
                btn.classList.remove('btn-outline-primary', 'btn-outline-info');
                
                setTimeout(() => { 
                    btn.innerHTML = originalText; 
                    btn.classList.remove('btn-success');
                    btn.classList.add('btn-outline-info'); 
                }, 2000);
            }
        }).catch(err => {
            console.error('Failed to copy: ', err);
        });
    }
}