function showToast(message, type = 'success', duration = 3000) {
    let backgroundColor;
    switch (type) {
        case 'success':
            backgroundColor = '#00b09b'; 
            break;
        case 'error':
            backgroundColor = '#ff4d4d'; 
            break;
        case 'warning':
            backgroundColor = '#6a0dad'; 
            break;
        default:
            backgroundColor = '#00b09b'; 
    }

    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.style.position = 'fixed';
        toastContainer.style.top = '15px';
        toastContainer.style.right = '20px';
        toastContainer.style.zIndex = '1000';
        document.body.appendChild(toastContainer);
    }

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.textContent = message;
    toast.style.backgroundColor = backgroundColor; 
    toast.style.color = '#fff'; 
    toast.style.padding = '10px 20px';
    toast.style.marginBottom = '10px';
    toast.style.borderRadius = '5px';
    toast.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.2)';
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.5s';

    if (window.innerWidth < 600) { 
        toast.style.fontSize = '14px'; 
        toast.style.padding = '8px 16px'; 
        toast.style.right = '10px'; 
    } else {
        toast.style.fontSize = '16px'; 
    }

    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '1';
    }, 10); 

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => {
            toastContainer.removeChild(toast);
            if (toastContainer.children.length === 0) {
                document.body.removeChild(toastContainer);
            }
        }, 500); 
    }, duration);
}
