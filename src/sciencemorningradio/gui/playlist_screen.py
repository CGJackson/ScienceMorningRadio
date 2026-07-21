import toga
from toga.style.pack import COLUMN, ROW, Pack

import sciencemorningradio.gui.article_display as article_display
import sciencemorningradio.gui.main_screen as main_screen
import sciencemorningradio.playlists as playlists

import sys

def run_screen(app, playlist):

    menu = build_side_menu(app,playlist)

    article_list_display_internal = toga.Box(
        children=[article_display.display_article(article) for article in playlist.articles],
        style=Pack(direction=COLUMN),
    )

    article_list_display = toga.ScrollContainer(content=article_list_display_internal)

    screen = toga.SplitContainer()
    screen.content = [(menu,1),(article_list_display,2)]

    return screen

def build_side_menu(app,playlist):

    menu = toga.Box("Side Menu",style=Pack(direction=COLUMN))

    last_updated_label = toga.Label(f"Last updated: {playlist.last_updated}")

    menu.add(last_updated_label)


    menu_options = [("Play", lambda button: playlists.read_playlist(playlist))]

    if hasattr(playlist, "update"):
        def update_list_and_screen():
            playlist.update()
            app.main_window.content = run_screen(app,playlist)
        menu_options.append(("Update", lambda button: update_list_and_screen()))

    menu_options.append(("Back", lambda button: main_screen.go_to_main_screen(app)))

    for option_name,callback in menu_options:
        button = toga.Button(text=option_name,
                on_press=callback,
                style=Pack(width=200,margin=5))
        menu.add(button)
        
    return menu

def go_to_playlist_screen(app,playlist):
    app.main_window.content = run_screen(app,playlist)
