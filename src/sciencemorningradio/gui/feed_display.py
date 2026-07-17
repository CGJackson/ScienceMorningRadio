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

    block = toga.Box(style=Pack(padding=10, background_color=status_color))
    block.add(toga.Label(str(feed.feed_data)))
    if isinstance(feed.status, PlaylistUpdating):
        block.add(toga.Label("Updating..."))
    elif isinstance(feed.status, PlaylistError):
        block.add(toga.Label(f"Error: {feed.status.error}"))

    return block
