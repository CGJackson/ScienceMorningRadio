import toga
import sciencemorningradio.playlists as playlists

def display_feed(feed: playlists.Feed):
    block = toga.Box()

    block.add(toga.Label(str(feed.feed_data)))
    
    return block
