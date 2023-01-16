from typing import Tuple

import src.sciencemorningradio.arxiv_reader as arxiv_reader
import src.sciencemorningradio.playlists.playlist as playlist

def playlist_from_search(search_query:arxiv_reader.Query,
        properties_to_read:Tuple(str)) -> playlist.Playlist:
    articles, _ = search_query.run()
    return playlist.Playlist(articles,properties_to_read)

