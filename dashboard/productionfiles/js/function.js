function toggleTheme() {
    const lightThemeLink = document.getElementById('light-theme');
    const darkThemeLink = document.getElementById('dark-theme');

    lightThemeLink.toggleAttribute('disabled');
    darkThemeLink.toggleAttribute('disabled');
}
function redirectToAdmin() {
    var adminUrl = '/admin/';
    window.open(adminUrl, '_blank');
}