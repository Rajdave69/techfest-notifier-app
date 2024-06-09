from win11toast import toast


def send_reminder_notification():
    from win11toast import toast

    buttons = [
        {'activationType': 'protocol', 'arguments': 'C:\Windows\Media\Alarm01.wav', 'content': 'Play'},
        {'activationType': 'protocol', 'arguments': 'file:///C:/Windows/Media', 'content': 'Open Folder'}
    ]

    toast('Hello', 'Click a button', buttons=buttons)


send_reminder_notification()
