import click
from time import strftime, localtime
import requests

API_URL = "http://127.0.0.1:30711"


@click.group(chain=True)
def notification():
    pass


@notification.command()
@click.option("--title", help="Title of the notification.", required=True)
@click.option("--description", help="Description of the notification.")
def send(title: str, description: str):
    try:
        response = requests.post(
            f"{API_URL}/api/send-notification/",
            json={
                "title": title,
                "body": description,
            },
        )
    except requests.exceptions.ConnectionError:
        raise click.ClickException(
            "Could not connect to the API. Please make sure the API is running."
        )

    assert (
        response.status_code == 200
    ), f"Failed to create notification with status code: {response.status_code}."
    click.echo("Notification successfully sent.")


@notification.command()
def list():
    try:
        response = requests.get(f"{API_URL}/api/notifications/")
    except requests.exceptions.ConnectionError:
        raise click.ClickException(
            "Could not connect to the API. Please make sure the API is running."
        )

    assert (
        response.status_code == 200
    ), f"Failed to list notifications with status code: {response.status_code}."

    notifications = response.json()
    notifications = notifications["data"]
    if len(notifications) == 0:
        click.echo("No Notifications.")
        return

    for notification in notifications:
        readable_time = strftime(
            "%Y-%m-%d %H:%M:%S", localtime(notification["timestamp"])
        )  # Assuming timestamp is in seconds, raises OSError when in milliseconds.
        click.echo(f"ID: {notification['id']}")
        click.echo(f"Type: {notification['type']}")
        click.echo(f"Read: {notification['read']}")
        click.echo(f"Title: {notification['title']}")
        click.echo(f"Description: {notification['body']}")
        click.echo(f"Sender: {notification['sender']}")
        click.echo(f"Image URL: {notification['image_url']}")
        click.echo(f"Timestamp: {readable_time}")
        click.echo("")


@notification.command()
def list_unread():
    try:
        response = requests.get(f"{API_URL}/api/notifications/")
    except requests.exceptions.ConnectionError:
        raise click.ClickException(
            "Could not connect to the API. Please make sure the API is running."
        )

    assert (
        response.status_code == 200
    ), f"Failed to list notifications with status code: {response.status_code}."

    notifications = response.json()
    notifications = notifications["data"]
    if len(notifications) == 0:
        click.echo("No Notifications.")
        return

    for notification in notifications:
        readable_time = strftime(
            "%Y-%m-%d %H:%M:%S", localtime(notification["timestamp"])
        )  # Assuming timestamp is in seconds, raises OSError when in milliseconds.
        click.echo(f"ID: {notification['id']}")
        click.echo(f"Type: {notification['type']}")
        click.echo(f"Title: {notification['title']}")
        click.echo(f"Description: {notification['body']}")
        click.echo(f"Sender: {notification['sender']}")
        click.echo(f"Image URL: {notification['image_url']}")
        click.echo(f"Timestamp: {readable_time}")
        click.echo("")
