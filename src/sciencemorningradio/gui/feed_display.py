import toga
from toga.style.pack import Pack

import sciencemorningradio.playlists as playlists
from sciencemorningradio.playlists.playlist import PlaylistError, PlaylistUpdating


def display_feed(feed: playlists.Feed):
    if isinstance(feed.status, PlaylistError):
        status_color = "red"
    elif isinstance(feed.status, PlaylistUpdating):
        status_color = "orange"
    else:
        status_color = "white"

    block = toga.Box(style=Pack(margin=10, background_color=status_color,direction="column"))
    block.add(toga.Label(str(feed.feed_data)))
    if isinstance(feed.status, PlaylistUpdating):
        block.add(toga.Label("Updating...",id="feed status"))
    elif isinstance(feed.status, PlaylistError):
        block.add(toga.Label(f"Error: {feed.status.error}"))

    feed.register_reference(block,update_feed_display)

    return block

def update_feed_display(block: toga.Box, feed: playlists.Feed):
    if isinstance(feed.status, PlaylistError):
        status_color = "red"
    elif isinstance(feed.status, PlaylistUpdating):
        status_color = "orange"
    else:
        status_color = "white"

    block.style.background_color = status_color

    # Remove any existing status labels before adding a new one
    try:
        current_status_labels = next(child for child in block.children if isinstance(child, toga.Label) and child.id == "feed status")
    except StopIteration:
        pass
    else:
        block.remove(current_status_labels)

    match feed.status:
        case PlaylistUpdating():
            block.add(toga.Label("Updating...",id="feed status"))
        case PlaylistError():
            block.add(toga.Label(f"Error: {feed.status.error}",id="feed status"))


