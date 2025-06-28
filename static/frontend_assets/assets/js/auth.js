// Login Form Handling
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Basic validation
            if (!email || !password) {
                alert('Please fill in all fields');
                return;
            }
            
            // In a real application, you would send this to your authentication server
            console.log('Login attempt with:', { email, password });
            
            // Simulate successful login
            alert('Login successful! Redirecting to dashboard...');
            
            // Redirect to dashboard (in a real app, this would be handled after server validation)
            // window.location.href = 'dashboard.html';
        });
    }
});