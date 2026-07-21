import toga
from toga.style.pack import COLUMN, ROW, Pack

from sciencemorningradio.gui.new_feed import build_new_feed_form
import sciencemorningradio.gui.feed_display as feed_display
import sciencemorningradio.gui.playlist_screen as playlist_screen

import sys

def run_screen(app):

    menu = build_side_menu(app)

    feed_list_display_internal = toga.Box(
        children=[build_feed_menu(app, feed) for feed in app.feed_list],
        style=Pack(direction=COLUMN),
    )

    feed_list_display = toga.ScrollContainer(content=feed_list_display_internal)

    screen = toga.SplitContainer()
    screen.content = [(menu,1),(feed_list_display,2)]

    return screen

def build_side_menu(app):

    menu = toga.Box("Side Menu",style=Pack(direction=COLUMN))

    menu_options = [("New Feed", lambda button: build_new_feed_form(app)),
                    ("New search", lambda button: None),
                    ("Settings", lambda button: None)]

    for option_name,callback in menu_options:
        button = toga.Button(text=option_name,
                on_press=callback,
                style=Pack(width=200,margin=5))
        menu.add(button)
        
    return menu

def build_feed_menu(app,feed):

    feed_view = toga.Box("Feed Menu",style=Pack(direction=COLUMN))

    feed_view.add(feed_display.display_feed(feed))

    menu = toga.Box("Menu buttons",style=Pack(direction=ROW))
    menu_options = [("View", lambda button: playlist_screen.go_to_playlist_screen(app, feed)),
                    ("Play", lambda button: feed.read(app.tts_engine)),
                    ("Update", lambda button: feed.update()),
                    ("Delete", lambda button: delete_feed_handler(app, feed))]

    for option_name,callback in menu_options:
        button = toga.Button(text=option_name,
                on_press=callback,
                style=Pack(width=80,margin=5))
        menu.add(button)

    feed_view.add(menu)

    return feed_view

def delete_feed_handler(app, feed): # TODO add confirmation dialog
    app.feed_list.remove(feed)
    go_to_main_screen(app)

def go_to_main_screen(app):
    app.main_window.content = run_screen(app)
