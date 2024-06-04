function createUnreadNotificationBox(title, description, image_path, timestamp) {

}




// Wait for window to completely load
window.addEventListener('DOMContentLoaded', function() {

    // Sidebar handler
    const elements = document.getElementById('sidebar-ul')

    for (let i = 0; i < elements.children.length; i++) {
            elements.children[i].onclick = function() {
                // Remove 'selected' class from all elements
                for (let j = 0; j < elements.children.length; j++) {
                    elements.children[j].classList.remove('selected');
                }

                // Add 'selected' class to the clicked element
                this.classList.add('selected');

            };
        }


    // Function to show the appropriate div based on the hash
    function showDivBasedOnHash() {

        // Get the divs
        const allDivs = {
            '#': document.getElementById("#"),
            '#settings': document.getElementById("#settings"),
            '#reminders': document.getElementById("#reminders"),
            "#notification-history": document.getElementById("#notification-history")
        }

        function hideAllDivsExcept(except) {
            for (let divKey in allDivs) {
                allDivs[divKey].hidden = divKey !== except;
            }
        }


        if (window.location.hash in allDivs) {
            hideAllDivsExcept(window.location.hash)
        } else {
            hideAllDivsExcept('#')
        }

    }

    // Check the hash initially when the page loads
    showDivBasedOnHash();

    // Listen for hash changes in the URL
    window.addEventListener("hashchange", showDivBasedOnHash);

});