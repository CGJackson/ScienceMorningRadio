import toga
from toga.style.pack import COLUMN, ROW, Pack

import sciencemorningradio.gui.feed_display as feed_display

def run_screen(app):

    menu = build_side_menu(app)

    feed_list_display = toga.ScrollContainer(content=app.feed_list)

    screen = toga.SplitContainer()
    screen.content = [(menu,1),(feed_list_display,2)]

    return screen

def build_side_menu(app):

    menu = toga.Box("Side Menu",style=Pack(direction=COLUMN))

    menu_options = [("New Feed", lambda button: None),
                    ("New search", lambda button: None),
                    ("Settings", lambda button: None)]

    for option_name,callback in menu_options:
        button = toga.Button(text=option_name,
                on_press=callback,
                style=Pack(width=200,padding=5))
        menu.add(button)
        
    return menu
