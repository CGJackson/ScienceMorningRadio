import asyncio

import toga
from sciencemorningradio.arxiv_reader import Query,SearchFields,SortBy,SortDirection
from sciencemorningradio.playlists import Feed
import sciencemorningradio.gui.main_screen as main_screen
from toga.style.pack import COLUMN, Pack


def build_new_feed_form(app):

    def create_new_feed(button: toga.Button):
        query = Query(search={SearchFields.all: search_input.value},max_results=10,sort_by=SortBy.lastUpdatedDate)
        feed = Feed(name=name_input.value, feed_data=query)
        asyncio.create_task(feed.update())
        app.feed_list.append(feed)
        app.main_window.content = main_screen.run_screen(app)

    name_label = toga.Label("Name")
    name_input = toga.TextInput()

    search_label = toga.Label("Search")
    search_input = toga.TextInput()

    create_feed_button = toga.Button(
        "Create Feed",
        on_press=create_new_feed,
        style=Pack(margin_top=10),
    )

    form = toga.Box(style=Pack(direction=COLUMN, margin=10))
    form.add(name_label)
    form.add(name_input)
    form.add(search_label)
    form.add(search_input)
    form.add(create_feed_button)

    app.main_window.content = form

