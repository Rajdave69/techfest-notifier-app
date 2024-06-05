const API_URL = ""

function showDivBasedOnHash() {
    if (window.location.hash === "") {
        window.location.hash = "#"
    }

        // Get the divs
        const allDivs = {
            '#': document.getElementById("#"),
            '#settings': document.getElementById("#settings"),
            '#reminders': document.getElementById("#reminders"),
            "#notification-history": document.getElementById("#notification-history"),
            '#create-reminder': document.getElementById("#create-reminder")
        }

        function hideAllDivsExcept(except) {
            for (let divKey in allDivs) {

                allDivs[divKey].hidden = divKey !== except;

            }
        }


        if (window.location.hash in allDivs) {
            hideAllDivsExcept(window.location.hash)
            return window.location.hash
        } else {
            hideAllDivsExcept('#')
        }

    }

function homepageLoadUnreadNotifications() {
        fetch(`API_URL`, {method: 'GET'})
        .then(r => {

        /*
        const r = [
            {'title': 'Title', 'content': 'Content', 'image': './static/placeholder_image.png', 'epoch': '123'},
            {'title': 'Title', 'content': 'Content', 'image': './static/placeholder_image.png', 'epoch': '123'},
            {'title': 'Title', 'content': 'Content', 'image': './static/placeholder_image.png', 'epoch': '123'},
            {'title': 'Title', 'content': 'Content', 'image': './static/placeholder_image.png', 'epoch': '123'},
            {'title': 'Title', 'content': 'Content', 'image': './static/placeholder_image.png', 'epoch': '123'},
        ]*/

            const unreadNotificationBox = document.getElementById('unread-notifications-box')

            for (let notification of r) {
                console.log(notification)
                // Create the unread-notification div
                const mainDiv = document.createElement('div')

                // Create the required items to be put in the div
                const image = document.createElement('img')
                const h3 = document.createElement('h3')
                const p = document.createElement('p')

                // Assign values to the divs
                mainDiv.setAttribute('class', 'notification-box');
                image.src = notification['image']
                h3.innerText = notification['title']
                p.innerText = notification['content']

                // Add all the new items to the main div, then add the main div to the page
                mainDiv.append(image, h3, p)
                unreadNotificationBox.append(mainDiv)
            }

            if (r.length === 0) {
                document.getElementById('unread-notifs-number-box').style.display = 'none';
                document.getElementById('unread-notifications').checked = false
            } else if (r.length >= 0) {
                document.getElementById('unread-notifs-number-box').innerText = r.length.toString()
                document.getElementById('unread-notifs-number-box').style.display = 'flex';
                document.getElementById('unread-notifications').checked = true

            } else {
                console.error("unreadNotificationBox list from API is less than 0 elements long (possible undefined)")
            }
        })
    }


function pageLoad() {
        // Check the hash initially when the page loads
        const currentPage = showDivBasedOnHash();

        if (currentPage === '#') {
            homepageLoadUnreadNotifications();
        }

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

    // Run it once on page load
    pageLoad();

    // Listen for hash changes in the URL
    window.addEventListener("hashchange", pageLoad);

});