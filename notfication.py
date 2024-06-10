from win11toast import toast



def notification_toast_handler(thing: dict):
    print(thing)
    if thing['arguments'] == "http:Mark as Read":
        mark_as_read(notification_id)
    elif thing['arguments'] == "http:Open":
        window.load_url("") # TODO URL WITH NOTIF ID




def send_reminder_notification():
    from win11toast import toast

    buttons = [
        'Mark as Read',       
        'Open'
    ]

    icon = {

    'src': 'https://unsplash.it/64?image=669',
    'placement': 'appLogoOverride'
    }


    toast('Hello', 'Hello from Python', icon=icon, buttons=buttons, on_click=notification_toast_handler, on_dismissed=lambda X: X)

send_reminder_notification()
