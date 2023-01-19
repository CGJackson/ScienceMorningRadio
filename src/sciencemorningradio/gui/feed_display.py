import toga

def display_feed(feed):
    block = toga.Box()

    block.add(toga.Label(str(feed.feed_data)))
    
    return block
