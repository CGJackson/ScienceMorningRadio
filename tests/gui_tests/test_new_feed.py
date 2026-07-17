import toga

from sciencemorningradio.gui.new_feed import build_new_feed_form


def test_build_new_feed_form_contains_name_and_search_fields():
    form = build_new_feed_form()

    text_inputs = [child for child in form.children if isinstance(child, toga.TextInput)]

    assert len(text_inputs) == 2


def test_build_new_feed_form_contains_create_feed_button():
    form = build_new_feed_form()

    buttons = [child for child in form.children if isinstance(child, toga.Button)]

    assert len(buttons) == 1
    assert buttons[0].text == "Create Feed"
