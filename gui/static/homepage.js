const API_URL = "";
PAGES = [
    "",
    "#settings",
    "#reminders",
    "#notification-history",
    "#create-reminder",
];

function displayPageBasedOnHash() {
    const currentLocation = window.location.hash.split('?')[0] || "#";
    const currentParams = window.location.hash.split('?')[1] || ''

    // Get the divs
    const allDivs = {
        "#": document.getElementById("#"),
        "#settings": document.getElementById("#settings"),
        "#reminders": document.getElementById("#reminders"),
        "#emails": document.getElementById("#emails"),
        "#notification-history": document.getElementById(
            "#notification-history",
        ),
        "#create-reminder": document.getElementById("#create-reminder"),
        "#view-email": document.getElementById("#view-email"),
        "#view-reminder": document.getElementById("#view-reminder"),
    };

    function hideAllDivsExcept(key) {
        for (let divKey in allDivs) {
            allDivs[divKey].hidden = divKey !== key;
        }
    }

    if (currentLocation in allDivs) {
        hideAllDivsExcept(currentLocation);
        return [currentLocation, currentParams];
    } else {
        hideAllDivsExcept("");
        console.warn(currentLocation);
    }
}

function pageLoad() {
    console.log("pageload");
    // Check the hash initially when the page loads
    const currentPageAndParams = displayPageBasedOnHash();

    if (currentPageAndParams === undefined) return

    selectSidebarElement(currentPageAndParams[0]);
    setSidebarReminderCount();
    setSidebarEmailCount();

    switch (currentPageAndParams[0]) {
        case "#": homepageLoadUnreadNotifications(); break;
        case "#reminders": remindersPageLoadReminders(); break;
        case "#emails": emailsPageLoadEmails(); break;
        case "#notification-history": notificationHistoryPageLoad(); break;
        case "#view-reminder": loadViewReminderPage(currentPageAndParams[1]); break;
        case "#view-email": loadViewEmailPage(currentPageAndParams[1]); break;
        // case _:         console.warn(currentPageAndParams);

    }
}

// Wait for window to completely load
window.addEventListener("DOMContentLoaded", function () {
    // Sidebar handler
    // const elements = document.getElementById("sidebar-ul");

    // for (let i = 0; i < elements.children.length; i++) {
    //     elements.children[i].onclick = function () {
    //         // Remove 'selected' class from all elements
    //         for (let j = 0; j < elements.children.length; j++) {
    //             elements.children[j].classList.remove("selected");
    //         }
    //
    //         // Add 'selected' class to the clicked element
    //         this.classList.add("selected");
    //     };
    // }

    // Create reminder submit button
    remindersCreateButtonHandler();

    // Run it once on page load
    pageLoad();

    // Listen for hash changes in the URL
    window.addEventListener("hashchange", () => {
        location.reload();
    });
});

function selectSidebarElement(pageHash) {
    const sidebarElements = document.getElementById("sidebar-ul").children;

    // Format: { "page-hash": "sidebar-element" }
    const sidebarPages = {
        "#": "#",
        "#reminders": "#reminders",
        "#create-reminder": "#reminders",
        "#view-reminder": "#reminders",
        "#emails": "#emails",
        "#view-email": "emails",
        "#notification-history": "#notification-history",
        "#settings": "#settings",
    };

    // For each element of the list,
    for (let i = 0; i < sidebarElements.length; i++) {
        if (
            (sidebarPages[pageHash] || undefined) ===
            sidebarElements[i].children[0].href.split("/").at(-1).replace("?", "")
        ) {
            sidebarElements[i].classList.add("selected");
        } else {
            sidebarElements[i].classList.remove("selected");
        }
    }
}


function setBreadcrumbPath(pageHash, subPath) {
    // ##page > .breadcrumb > .breadcrumb-subpath
    const breadcrumb = document.getElementById(pageHash).children[0].children[2]

    breadcrumb.innerText = subPath
}

/*

    VIEW EMAIL PAGE

 */

function loadViewEmailPage(params) {
    const email_id = params.split("&id=")[1]
    console.log(email_id)

    const titleBox = document.getElementById("email-title").children[0]
    const bodyBox = document.getElementById("email-body")
    const timeBox = document.getElementById("email-timestamp")
    const senderBox = document.getElementById("email-sender")

    fetch(`${API_URL}/api/emails/${email_id}`, {
        method: "GET",
    })
        .then((response) => response.json())
        .then((response) => response["data"])
        .then((response) => {

            const datetime = new Date(response["timestamp"] * 1000);

            titleBox.innerText = response['title']
            bodyBox.innerText = response['body']
            timeBox.InnerHtml = `<b>At:</b> <br>${datetime.toLocaleDateString()} ${datetime.toLocaleTimeString()}`
            senderBox.InnerHtml = `<b>From:</b> <br>${response['body']}`

            setBreadcrumbPath("#view-reminder", `View #${email_id}`)
        })

}




/*

    VIEW REMINDERS PAGE

 */

function loadViewReminderPage(params) {
    const reminder_id = params.split("id=")[1]
    const titleBox = document.getElementById("reminder-title").children[0]
    const descriptionBox = document.getElementById("reminder-body")
    const timeBox = document.getElementById("reminder-timestamp")

    fetch(`${API_URL}/api/reminders/${reminder_id}`, {
        method: "GET",
    })
        .then((response) => response.json())
        .then((response) => response["data"])
        .then((response) => {
            const datetime = new Date(response["timestamp"] * 1000);

            titleBox.innerText = response['title'] // Don't worry, this doesn't get rid of H2
            descriptionBox.innerText = response['body'] || "No Description present"
            timeBox.innerText = `${datetime.toLocaleDateString()} ${datetime.toLocaleTimeString()}`

            setBreadcrumbPath("#view-reminder", `View #${reminder_id}`)
        })
}

/*

    HOME PAGE

 */

function homepageLoadUnreadNotifications() {
    console.log("test");
    const unreadNotificationBox = document.getElementById(
        "unread-notifications-box",
    );
    // Empty the box everytime new items are added
    unreadNotificationBox.replaceChildren();

    fetch(`${API_URL}/api/notifications/unread/`, {
        method: "GET",
    })
        .then((response) => response.json())
        .then((response) => response["data"])
        .then((response) => {
            console.log(response);

            for (let box of createNotificationBoxes(response)) {
                unreadNotificationBox.append(box);
            }

            if (response.length === 0) {
                document.getElementById(
                    "unread-notifs-number-box",
                ).style.display = "none";
                document.getElementById("unread-notifications").checked = false;
            } else if (response.length >= 0) {
                document.getElementById("unread-notifs-number-box").innerText =
                    response.length.toString();
                document.getElementById(
                    "unread-notifs-number-box",
                ).style.display = "flex";
                document.getElementById("unread-notifications").checked = true;
            } else {
                console.error(
                    "unreadNotificationBox list from API is less than 0 elements long (possible undefined)",
                );
            }
        });
}

/*

    REMINDERS PAGE

 */

function setSidebarReminderCount() {
    const reminderNumberBox = document.getElementById("reminder-number-box");

    fetch(`${API_URL}/api/reminders/unread/`, {
        method: "GET",
    })
        .then((response) => response.json())
        .then((response) => response['data'])
        .then((response) => {
            console.log(response)
            if (response.length === 0) {
                reminderNumberBox.style.display = "none";
            } else {
                reminderNumberBox.style.display = "flex";
                reminderNumberBox.innerText =
                    response.length.toString().toString();
            }
        });
}

function setSidebarEmailCount() {
    const emailNumberBox = document.getElementById("email-number-box");

    fetch(`${API_URL}/api/emails/unread/`, {
        method: "GET",
    })
        .then((response) => response.json())
        .then((response) => response['data'])
        .then((response) => {
            console.log(response)
            if (response.length === 0) {
                emailNumberBox.style.display = "none";
            } else {
                emailNumberBox.style.display = "flex";
                emailNumberBox.innerText = response.length.toString();
            }
        });
}

function remindersPageLoadReminders() {
    const remindersTableBody = document.getElementById("reminders-table").children[0];
    const emptyRemindersDiv = document.getElementById("reminders-empty");
    const tableWrapper = document.getElementById("reminders-table");

    // Clear existing rows except for the header
    while (remindersTableBody.rows.length > 1) {
        remindersTableBody.deleteRow(1);
    }

    fetch(`${API_URL}/api/reminders/`, {
        method: "GET",
    })
        .then((response) => response.json())
        .then((response) => response["data"])
        .then((response) => {
            console.log(response);
            console.log(response.length);

            if (response.length === 0) {
                emptyRemindersDiv.style.display = "grid";
                tableWrapper.hidden = true;
            } else {
                emptyRemindersDiv.style.display = "none";
                tableWrapper.hidden = false;

                for (let element of response) {
                    // Create a table row
                    let tr = document.createElement("tr");

                    // Create table data cells for title, description, and time
                    let title = document.createElement("td");
                    let description = document.createElement("td");
                    let time = document.createElement("td");
                    const viewButtonCell = document.createElement("td");
                    const deleteButtonCell = document.createElement("td");

                    // Set the text content for the cells
                    title.innerText = element["title"];
                    description.innerText = element["body"];
                    const dateObj = new Date(element["timestamp"] * 1000);
                    time.innerText = `${dateObj.toLocaleDateString()} ${dateObj.toLocaleTimeString()}`;

                    /*
                    !!! SVG ONE - View Icon with Class!!!
                    */
                    // Create an SVG element for the View icon
                    const viewButtonSVG = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                    viewButtonSVG.setAttribute("width", "1em");
                    viewButtonSVG.setAttribute("height", "1em");
                    viewButtonSVG.setAttribute("viewBox", "0 0 24 24");
                    viewButtonSVG.setAttribute("fill", "currentColor");

                    // Create path elements for the View SVG
                    const viewSVGPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
                    viewSVGPath.setAttribute("d", "M12 4.5C7 4.5 3.28 7.36 1.5 12C3.28 16.64 7 19.5 12 19.5C17 19.5 20.72 16.64 22.5 12C20.72 7.36 17 4.5 12 4.5ZM12 17.5C9.5 17.5 7.5 15.5 7.5 13C7.5 10.5 9.5 8.5 12 8.5C14.5 8.5 16.5 10.5 16.5 13C16.5 15.5 14.5 17.5 12 17.5ZM12 6.5C8.41 6.5 5.5 9.41 5.5 13C5.5 16.59 8.41 19.5 12 19.5C15.59 19.5 18.5 16.59 18.5 13C18.5 9.41 15.59 6.5 12 6.5ZM12 10.5C10.62 10.5 9.5 11.62 9.5 13C9.5 14.38 10.62 15.5 12 15.5C13.38 15.5 14.5 14.38 14.5 13C14.5 11.62 13.38 10.5 12 10.5Z");
                    viewSVGPath.setAttribute("fill-rule", "evenodd");
                    viewSVGPath.setAttribute("clip-rule", "evenodd");
                    viewButtonSVG.append(viewSVGPath);

                    // Add the SVG and text to the viewButtonCell
                    viewButtonCell.setAttribute("class", "table-view-button");
                    viewButtonCell.setAttribute("id", `reminder-${element["id"]}`);

                    viewButtonCell.append(viewButtonSVG);
                    viewButtonCell.append(" View");

                    // Add a click event listener to the delete button cell
                    viewButtonCell.addEventListener("click", remindersViewButtonHandler);

                    /*
                    !!! SVG TWO - Delete Icon !!!
                    */
                    // Create an SVG element for the Delete icon
                    const deleteButtonSVG = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                    deleteButtonSVG.setAttribute("viewBox", "0 0 20 20");
                    deleteButtonSVG.setAttribute("fill", "currentColor");
                    deleteButtonSVG.setAttribute("aria-hidden", "true");
                    deleteButtonSVG.setAttribute("height", "1em");
                    deleteButtonSVG.setAttribute("width", "1em");

                    // Create path elements for the Delete SVG
                    const deleteSVGPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
                    deleteSVGPath.setAttribute("d",
                        "M8.75 1A2.75 2.75 0 0 0 6 3.75v.443c-.795.077-1.584.176-2.365.298a.75.75 0 1 0 .23 1.482l.149-.022.841 10.518A2.75 2.75 0 0 0 7.596 19h4.807a2.75 2.75 0 0 0 2.742-2.53l.841-10.52.149.023a.75.75 0 0 0 .23-1.482A41.03 41.03 0 0 0 14 4.193V3.75A2.75 2.75 0 0 0 11.25 1h-2.5ZM10 4c.84 0 1.673.025 2.5.075V3.75c0-.69-.56-1.25-1.25-1.25h-2.5c-.69 0-1.25.56-1.25 1.25v.325C8.327 4.025 9.16 4 10 4ZM8.58 7.72a.75.75 0 0 0-1.5.06l.3 7.5a.75.75 0 1 0 1.5-.06l-.3-7.5Zm4.34.06a.75.75 0 1 0-1.5-.06l-.3 7.5a.75.75 0 1 0 1.5.06l.3-7.5Z",);
                    deleteSVGPath.setAttribute("fill-rule", "evenodd");
                    deleteSVGPath.setAttribute("clip-rule", "evenodd");
                    deleteButtonSVG.append(deleteSVGPath);

                    // Add the SVG and text to the deleteButtonCell
                    deleteButtonCell.setAttribute("class", "table-delete-button");
                    deleteButtonCell.setAttribute("id", `reminder-${element["id"]}`);
                    deleteButtonCell.append(deleteButtonSVG);
                    deleteButtonCell.append(" Delete");

                    // Add a click event listener to the delete button cell
                    deleteButtonCell.addEventListener("click", remindersDeleteButtonHandler);

                    // Append the cells to the row
                    tr.append(title, time, description, viewButtonCell, deleteButtonCell);
                    remindersTableBody.append(tr);
                }
            }
        });
}


function emailsPageLoadEmails() {
    const emailsTableBody = document.getElementById("emails-table").children[0];
    const emptyEmailsDiv = document.getElementById("emails-empty");
    const tableWrapper = document.getElementById("emails-table");

    // Clear existing rows except for the header
    while (emailsTableBody.rows.length > 1) {
        emailsTableBody.deleteRow(1);
    }

    fetch(`${API_URL}/api/emails/`, {
        method: "GET",
    })
        .then((response) => response.json())
        .then((response) => response["data"])
        .then((response) => {
            console.log(response);
            console.log(response.length);

            if (response.length === 0) {
                emptyEmailsDiv.style.display = "grid";
                tableWrapper.hidden = true;
            } else {
                emptyEmailsDiv.style.display = "none";
                tableWrapper.hidden = false;

                for (let element of response) {
                    // Create a table row
                    let tr = document.createElement("tr");

                    // Create table data cells for title, description, and time
                    let title = document.createElement("td");
                    let description = document.createElement("td");
                    let time = document.createElement("td");
                    const viewButtonCell = document.createElement("td");

                    // Set the text content for the cells
                    title.innerText = element["title"];
                    description.innerText = element["body"];
                    const dateObj = new Date(element["timestamp"] * 1000);
                    time.innerText = `${dateObj.toLocaleDateString()} ${dateObj.toLocaleTimeString()}`;

                    /*
                    !!! SVG ONE - View Icon with Class!!!
                    */
                    // Create an SVG element for the View icon
                    const viewButtonSVG = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                    viewButtonSVG.setAttribute("width", "1em");
                    viewButtonSVG.setAttribute("height", "1em");
                    viewButtonSVG.setAttribute("viewBox", "0 0 24 24");
                    viewButtonSVG.setAttribute("fill", "currentColor");

                    // Create path elements for the View SVG
                    const viewSVGPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
                    viewSVGPath.setAttribute("d", "M12 4.5C7 4.5 3.28 7.36 1.5 12C3.28 16.64 7 19.5 12 19.5C17 19.5 20.72 16.64 22.5 12C20.72 7.36 17 4.5 12 4.5ZM12 17.5C9.5 17.5 7.5 15.5 7.5 13C7.5 10.5 9.5 8.5 12 8.5C14.5 8.5 16.5 10.5 16.5 13C16.5 15.5 14.5 17.5 12 17.5ZM12 6.5C8.41 6.5 5.5 9.41 5.5 13C5.5 16.59 8.41 19.5 12 19.5C15.59 19.5 18.5 16.59 18.5 13C18.5 9.41 15.59 6.5 12 6.5ZM12 10.5C10.62 10.5 9.5 11.62 9.5 13C9.5 14.38 10.62 15.5 12 15.5C13.38 15.5 14.5 14.38 14.5 13C14.5 11.62 13.38 10.5 12 10.5Z");
                    viewSVGPath.setAttribute("fill-rule", "evenodd");
                    viewSVGPath.setAttribute("clip-rule", "evenodd");
                    viewButtonSVG.append(viewSVGPath);

                    // Add the SVG and text to the viewButtonCell
                    viewButtonCell.setAttribute("class", "table-view-button");
                    viewButtonCell.setAttribute("id", `email-${element["id"]}`);
                    viewButtonCell.append(viewButtonSVG);
                    viewButtonCell.append(" View");

                    // Add a click event listener to the delete button cell
                    viewButtonCell.addEventListener("click", emailsViewButtonHandler);

                    // Append the cells to the row
                    tr.append(title, time, description, viewButtonCell);
                    emailsTableBody.append(tr);
                }
            }
        });
}



function remindersDeleteButtonHandler(item) {
    const id_ = item.target.id.replace("reminder-", "");

    fetch(`${API_URL}/api/reminders/delete/${id_}`, {
        method: "DELETE",
        headers: {
            "Content-type": "application/json; charset=UTF-8",
        },
    }).then((r) => {
        console.log(r);
        location.reload(); // TODO TEST
    });
}

function remindersViewButtonHandler(item) {
    const id_ = item.target.id.replace("reminder-", "");

    document.location.hash = `#view-reminder?id=${id_}`
}

function emailsViewButtonHandler(item) {
    const id_ = item.target.id.replace("email-", "");

    document.location.hash = `#view-email?id=${id_}`
}



function remindersCreateButtonHandler() {
    document.getElementById("create-reminder-submit-button").onclick = () => {
        const nameElement = document.getElementById("get-reminder-name");
        const timeElement = document.getElementById("get-reminder-time");
        const imageElement = document.getElementById("get-reminder-image");
        const descriptionElement = document.getElementById(
            "get-reminder-description",
        );

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
        if (
            Date.parse(timeElement.value) <= Date.parse(new Date().toString())
        ) {
            alert("Time cannot be earlier than current time");
            timeElement.value = "";
            return;
        }

        fetch(`${API_URL}/api/reminders/create/`, {
            method: "POST",
            body: JSON.stringify({
                name: nameElement.value,
                timestamp: Date.parse(timeElement.value) / 1000,
                image_url: imageElement.value,
                body: descriptionElement.value,
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8",
            },
        }).then((r) => {
            nameElement.value = "";
            timeElement.value = "";
            imageElement.value = "";
            descriptionElement.value = "";

            window.location.hash = "#reminders";
        });
    };
}

/*

    NOTIFICATION HISTORY PAGE

 */

function notificationHistoryPageLoad() {
    const page = document.getElementById("#notification-history");
    const emptyNotificationHistoryDiv = document.getElementById(
        "notification-history-empty",
    );
    const notificationHistoryDiv = document.getElementById(
        "notification-history-boxes",
    );

    // Empty the box everytime new items are added
    notificationHistoryDiv.replaceChildren();

    fetch(`${API_URL}/api/notifications/`, { method: "GET" })
        .then((response) => response.json())
        .then((response) => response["data"])
        .then((response) => {
            console.log(response);
            console.log(response.length);
            if (response.length === 0) {
                emptyNotificationHistoryDiv.style.display = "grid";
                notificationHistoryDiv.hidden = true;
            } else {
                emptyNotificationHistoryDiv.style.display = "none";
                notificationHistoryDiv.hidden = false;

                for (let box of createNotificationBoxes(response)) {
                    notificationHistoryDiv.append(box);
                }
            }
        });
}

function createNotificationBoxes(data) {
    let finalList = [];

    for (let notification of data) {
        // Create the unread-notification div
        const mainDiv = document.createElement("div");

        // Create the required items to be put in the div
        const image = document.createElement("img");
        const h3 = document.createElement("h3");
        const timestamp = document.createElement("h3");
        const p = document.createElement("p");

        // Assign values to the divs
        mainDiv.setAttribute("class", "notification-box");
        image.src = notification["image_url"];
        h3.innerText = notification["title"];

        const datetime = new Date(notification["timestamp"] * 1000);

        timestamp.innerText = `${datetime.toLocaleDateString()} ${datetime.toLocaleTimeString()}`;
        p.innerText = notification["body"];

        // Add all the new items to the main div, then add the main div to the page
        mainDiv.append(image, h3, timestamp, p);
        finalList.push(mainDiv);
    }
    return finalList;
}
