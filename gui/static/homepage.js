function createUnreadNotificationBox(title, description, image_path, timestamp) {

}




// Wait for window to completely load
window.addEventListener('DOMContentLoaded', function() {

    const elements = document.getElementsByClassName('nav-item')

    for (let i = 0; i < elements.length; i++) {
        elements[i].onclick = () => {
            elements[i].classList.add('selected')
            console.log(`${elements[i].innerText}`);
        }
    }

});



