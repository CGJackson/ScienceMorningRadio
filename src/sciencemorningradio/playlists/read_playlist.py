import pyttsx3 as tts
from src.sciencemorningradio.article import ArticleMissingAttributeError

def read_playlist(engine:tts.Engine, playlist):
    """
    Uses text to speach engine engine to read out loud the article 
    attributes spesified by the playlist
    """
    for article in playlist.articles:
        read_article(engine,article,playlist.read_properties)


def read_article(engine:tts.Engine,article,properties_to_read)
    """
    uses text to speach engine engine to read out loud the attributes 
    properties_to_read form article
    """
    for read_property in properties_to_read:
        try:
            text = article.get_readable_string(read_property)
            engine.say(text)
        except ArticleMissingAttributeError:
            continue
    engine.runAndWait()


