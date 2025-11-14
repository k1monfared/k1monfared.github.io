/**
 * Theme Toggle - Light/Dark Mode Switcher
 * NOTE: This script only creates the button. The theme is applied via inline script in <head>
 */

(function() {
    // Helper: Save theme to both localStorage and cookie
    function saveTheme(theme) {
        // Always save to cookie (works with file:// protocol)
        document.cookie = `theme=${theme};path=/;max-age=31536000;SameSite=Lax`; // 1 year

        // Try localStorage if available
        try {
            localStorage.setItem('theme', theme);
            console.log('Saved to localStorage:', theme);
        } catch (e) {
            console.log('localStorage not available, using cookie only');
        }
    }

    // Create and add theme toggle button
    function createThemeToggle() {
        const button = document.createElement('button');
        button.className = 'theme-toggle';
        button.setAttribute('aria-label', 'Toggle theme');
        button.setAttribute('title', 'Toggle light/dark mode');

        button.addEventListener('click', toggleTheme);

        document.body.appendChild(button);
    }

    // Toggle between light and dark themes
    function toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        console.log('Toggling theme from', currentTheme, 'to', newTheme);

        document.documentElement.setAttribute('data-theme', newTheme);
        saveTheme(newTheme);

        console.log('Theme saved. localStorage:', localStorage.getItem('theme'));
        console.log('Cookie:', document.cookie);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', createThemeToggle);
    } else {
        createThemeToggle();
    }
})();
