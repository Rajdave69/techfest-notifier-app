const API_URL = "";
PAGES = ["", "#settings", "#reminders", "#notification-history", "#create-reminder"];

function showDivBasedOnHash() {
    let currentLocation = window.location.hash || "#";

    // Get the divs
    const allDivs = {
        "#": document.getElementById("#"),
        "#settings": document.getElementById("#settings"),
        "#reminders": document.getElementById("#reminders"),
        "#notification-history": document.getElementById("#notification-history"),
        "#create-reminder": document.getElementById("#create-reminder"),
    };

    function hideAllDivsExcept(key) {
        for (let divKey in allDivs) {
            console.log(divKey, key, divKey !== key);

            allDivs[divKey].hidden = divKey !== key;
        }
    }

    if (currentLocation in allDivs) {
        console.log("test", currentLocation);
        hideAllDivsExcept(currentLocation);
        return currentLocation;
    } else {
        hideAllDivsExcept("");
        console.warn(currentLocation);
    }
}

function homepageLoadUnreadNotifications() {
    console.log("test");
    const unreadNotificationBox = document.getElementById("unread-notifications-box");
    unreadNotificationBox.replaceChildren();

    fetch(`${API_URL}`, {
        method: "GET",
    })
        .then((response) => response.json())
        .then((r) => {
            // const r = [
            //     {'title': 'Title', 'content': 'Content', 'image': './static/placeholder_image.png', 'epoch': '123'},
            //     {'title': 'Title', 'content': 'Content', 'image': './static/placeholder_image.png', 'epoch': '123'},
            //     {'title': 'Title', 'content': 'Content', 'image': './static/placeholder_image.png', 'epoch': '123'},
            //     {'title': 'Title', 'content': 'Content', 'image': './static/placeholder_image.png', 'epoch': '123'},
            //     {'title': 'Title', 'content': 'Content', 'image': './static/placeholder_image.png', 'epoch': '123'},
            // ]

            for (let notification of r) {
                console.log(notification);
                // Create the unread-notification div
                const mainDiv = document.createElement("div");

                // Create the required items to be put in the div
                const image = document.createElement("img");
                const h3 = document.createElement("h3");
                const p = document.createElement("p");

                // Assign values to the divs
                mainDiv.setAttribute("class", "notification-box");
                image.src = notification["image"];
                h3.innerText = notification["title"];
                p.innerText = notification["content"];

                // Add all the new items to the main div, then add the main div to the page
                mainDiv.append(image, h3, p);
                unreadNotificationBox.append(mainDiv);
            }

            if (r.length === 0) {
                document.getElementById("unread-notifs-number-box").style.display = "none";
                document.getElementById("unread-notifications").checked = false;
            } else if (r.length >= 0) {
                document.getElementById("unread-notifs-number-box").innerText = r.length.toString();
                document.getElementById("unread-notifs-number-box").style.display = "flex";
                document.getElementById("unread-notifications").checked = true;
            } else {
                console.error("unreadNotificationBox list from API is less than 0 elements long (possible undefined)");
            }
        });
}

function remindersPageLoadReminders() {
    const remindersTableBody = document.getElementById("reminders-table").children[0];
    while (remindersTableBody.rows.length > 1) {
        remindersTableBody.deleteRow(1);
    }

    fetch(`${API_URL}/api/reminders/`, {
        method: "GET",
    })
        .then((response) => response.json())
        .then((r) => {
            console.log(r);
            // const r = [
            //     {'title': 'test', 'description': 'also eeetest', 'time': '1717701680', 'id': '123'}
            // ]
            for (let element of r["data"]) {
                // Create a table row
                let tr = document.createElement("tr");

                // Create table data cells for title, description, and time
                let title = document.createElement("td");
                let description = document.createElement("td");
                let time = document.createElement("td");
                const deleteButton = document.createElement("td");

                // Set the text content for the cells
                title.innerText = element["title"];
                description.innerText = element["description"];
                const dateObj = new Date(element["time"] * 1000);
                time.innerText = `${dateObj.toLocaleDateString()}  ${dateObj.toLocaleTimeString()}`;

                // Set class for the delete button
                deleteButton.setAttribute("class", "table-delete-button");
                deleteButton.setAttribute("id", `reminder-${element["id"]}`);

                // Create an SVG element with the appropriate namespace
                const deleteButtonSVG = document.createElementNS("http://www.w3.org/2000/svg", "svg");

                // Set necessary attributes for the SVG element
                deleteButtonSVG.setAttribute("viewBox", "0 0 20 20");
                deleteButtonSVG.setAttribute("fill", "currentColor");
                deleteButtonSVG.setAttribute("aria-hidden", "true");
                deleteButtonSVG.setAttribute("height", "1em");
                deleteButtonSVG.setAttribute("width", "1em");

                // Create path elements with the correct namespace
                const svgPath1 = document.createElementNS("http://www.w3.org/2000/svg", "path");
                svgPath1.setAttribute("d", "M8.75 1A2.75 2.75 0 0 0 6 3.75v.443c-.795.077-1.584.176-2.365.298a.75.75 0 1 0 .23 1.482l.149-.022.841 10.518A2.75 2.75 0 0 0 7.596 19h4.807a2.75 2.75 0 0 0 2.742-2.53l.841-10.52.149.023a.75.75 0 0 0 .23-1.482A41.03 41.03 0 0 0 14 4.193V3.75A2.75 2.75 0 0 0 11.25 1h-2.5ZM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4ZM8.58 7.72a.75.75 0 0 0-1.5.06l.3 7.5a.75.75 0 1 0 1.5-.06l-.3-7.5Zm4.34.06a.75.75 0 1 0-1.5-.06l-.3 7.5a.75.75 0 1 0 1.5.06l.3-7.5Z");
                svgPath1.setAttribute("fill-rule", "evenodd");
                svgPath1.setAttribute("clip-rule", "evenodd");

                deleteButtonSVG.append(svgPath1);
                deleteButton.append(deleteButtonSVG);
                // Add the text "Delete" after the SVG
                deleteButton.append(" Delete");

                // Add a click event listener to the delete button cell
                deleteButton.addEventListener("click", remindersDeleteButtonHandler);

                tr.append(title, description, time, deleteButton);
                remindersTableBody.append(tr);
            }
        });
}

function remindersDeleteButtonHandler(item) {
    const id = item.target.id.replace("reminder-", "");

    fetch(`${API_URL}`, {
        method: "post",
        body: { id: id },
    }).then((r) => {
        console.log(r);
        location.reload(); // TODO TEST
    });
}

function pageLoad() {
    console.log("pageload");
    // Check the hash initially when the page loads
    const currentPage = showDivBasedOnHash();

    selectSidebarElement(currentPage);
    setSidebarReminderCount();

    if (currentPage === "#") {
        console.log("uwu");
        homepageLoadUnreadNotifications();
    } else if (currentPage === "#reminders") {
        remindersPageLoadReminders();
    } else {
        console.warn(currentPage);
    }
}

// Wait for window to completely load
window.addEventListener("DOMContentLoaded", function () {
    // Sidebar handler
    const elements = document.getElementById("sidebar-ul");

    for (let i = 0; i < elements.children.length; i++) {
        elements.children[i].onclick = function () {
            // Remove 'selected' class from all elements
            for (let j = 0; j < elements.children.length; j++) {
                elements.children[j].classList.remove("selected");
            }

            // Add 'selected' class to the clicked element
            this.classList.add("selected");
        };
    }

    // Create reminder submit button
    createReminderSubmitButton();

    // Run it once on page load
    pageLoad();

    // Listen for hash changes in the URL
    window.addEventListener("hashchange", pageLoad);
});

function selectSidebarElement(pageHash) {
    const sidebarElements = document.getElementById("sidebar-ul");

    for (let i = 0; i < sidebarElements.children.length; i++) {
        console.log(sidebarElements.children[i].children[0].href);

        if (sidebarElements.children[i].children[0].href.endsWith(pageHash)) {
            sidebarElements.children[i].children[0].click();
        }
    }
}

function createReminderSubmitButton() {
    document.getElementById("create-reminder-submit-button").onclick = () => {
        const nameElement = document.getElementById("get-reminder-name");
        const timeElement = document.getElementById("get-reminder-time");
        const imageElement = document.getElementById("get-reminder-image");
        const descriptionElement = document.getElementById("get-reminder-description");

        if (nameElement.value === "" || timeElement.value === "") {
            console.log("undefined things");
            return;
        }

        const imageRegex = /(http(s?):)([/|.|\\w|\\s|-])*\\.(?:jpg|png)/;

        if (!imageRegex.test(imageElement.value) && imageElement.value !== "") {
            alert("Invalid Image URL. Only JPG and PNG allowed");
            imageElement.value = "";
            return;
        }

        // Check if epoch given is smaller than current epoch
        if (Date.parse(timeElement.value) <= Date.parse(new Date().toString())) {
            alert("Time cannot be earlier than current time");
            timeElement.value = "";
            return;
        }

        fetch(`${API_URL}`, {
            method: "POST",
            body: {
                name: nameElement.value,
                time: Date.parse(timeElement.value),
                image: imageElement.value,
                description: descriptionElement.value,
            },
        }).then((r) => {
            nameElement.value = "";
            timeElement.value = "";
            imageElement.value = "";
            descriptionElement.value = "";

            window.location.hash = "#reminders";
            alert("Reminder Successfully created");
        });
    };
}

function setSidebarReminderCount() {
    const reminderNumberBox = document.getElementById("reminder-number-box");

    fetch(`${API_URL}/api/reminders/`, {
        method: "GET",
    })
        .then((response) => response.json())
        .then((response) => {
            if (response["data"].length === 0) {
                reminderNumberBox.style.display = "none";
            } else {
                reminderNumberBox.style.display = "flex";
                reminderNumberBox.innerText = response["data"].length.toString();
            }
        });
}
