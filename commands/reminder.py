import click
import time
from time import strftime, localtime
import requests

API_URL = "http://127.0.0.1:30711"


def validate_timestamp(ctx, param, timestamp: int):
    if timestamp is None:
        return None
    if timestamp < 0:
        raise click.BadParameter("Please provide a valid timestamp.")
    return timestamp


def validate_image_url(ctx, param, image_url: str):
    if image_url is None:
        return None
    if not image_url.startswith("http") and not image_url.startswith("https"):
        raise click.BadParameter("Please provide a valid image URL.")
    image_formats = ("image/png", "image/jpeg", "image/jpg")
    r = requests.head(image_url)
    if not r.headers["content-type"] in image_formats:
        raise click.BadParameter("Please provide a valid image URL.")
    return image_url


@click.group(chain=True)
def reminder():
    pass


@reminder.command()
@click.option("--name", help="Name of the reminder.", required=True)
@click.option("--description", help="Description of the reminder.")
@click.option("--image", help="Image URL of the reminder.", callback=validate_image_url)
@click.option(
    "--time",
    help="Timestamp of the reminder.",
    default=int(time.time()),
    callback=validate_timestamp,
)
def create(name: str, description: str, image: str, time: int):
    try:
        response = requests.post(
            f"{API_URL}/api/reminders/create/",
            json={
                "name": name,
                "timestamp": time,
                "description": description,
                "image_url": image,
            },
        )
    except requests.exceptions.ConnectionError:
        raise click.ClickException(
            "Could not connect to the API. Please make sure the API is running."
        )

    assert (
        response.status_code == 200
    ), f"Failed to create reminder with status code: {response.status_code}."
    click.echo("Reminder created successfully.")


@reminder.command()
@click.option("--id", help="ID of the reminder to delete.", required=True)
def delete(id: str):
    try:
        response = requests.post(f"{API_URL}/api/reminders/delete/", json={"id": id})
    except requests.exceptions.ConnectionError:
        raise click.ClickException(
            "Could not connect to the API. Please make sure the API is running."
        )

    assert (
        response.status_code == 200
    ), f"Failed to delete reminder with status code: {response.status_code}."
    click.echo("Reminder deleted successfully.")


@reminder.command()
def list():
    try:
        response = requests.get(f"{API_URL}/api/reminders/")
    except requests.exceptions.ConnectionError:
        raise click.ClickException(
            "Could not connect to the API. Please make sure the API is running."
        )

    assert (
        response.status_code == 200
    ), f"Failed to list reminders with status code: {response.status_code}."
    reminders = response.json()
    reminders = reminders["data"]
    if len(reminders) == 0:
        click.echo("No Reminders.")
        return

    for reminder in reminders:
        readable_time = strftime(
            "%Y-%m-%d %H:%M:%S", localtime(reminder["timestamp"])
        )  # Assuming timestamp is in seconds, raises OSError when in milliseconds.
        click.echo(
            f"ID: {reminder['id']}, Name: {reminder['title']}, Description: {reminder['description']}, Timestamp: {readable_time}"
        )
        click.echo("")
