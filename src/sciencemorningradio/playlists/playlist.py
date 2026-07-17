import datetime
import weakref
from typing import Tuple,List
import sciencemorningradio.arxiv_reader as arxiv_reader
from sciencemorningradio.article import Article

class PlaylistStatus():
    pass

class PlaylistOK(PlaylistStatus):
    pass

class PlaylistError(PlaylistStatus):
    def __init__(self,error:Exception):
        self.error = error

class PlaylistUpdating(PlaylistStatus):
    def __init__(self,**kwargs):
        self.data = kwargs

class Playlist():
    def __init__(self,name: str,articles: List[Article],read_attributes: Tuple[str]=("title","authors","abstract")):
        self.name:str = name
        self.articles: List[Article] = articles
        self.read_attributes = read_attributes
        self.status: PlaylistStatus = PlaylistOK()
        self._references = weakref.WeakSet()
    
    def register_reference(self,reference):
        self._references.add(reference)

    def update_references(self):
        for reference in self._references:
            reference.refresh()

class Feed(Playlist):
    def __init__(self,name: str,feed_data: arxiv_reader.Query,read_attributes: Tuple[str]=None):
        if read_attributes is None:
            super().__init__(name,[])
        else:
            super().__init__(name,[],read_attributes)
        self.feed_data = feed_data
        self.last_updated = datetime.datetime.fromtimestamp(0)

    async def update(self):
        """
        Updates the current list of articles to the latest available from
        arXive.org. If arXiv.org would not have been updated since the last
        update, it has no effect
        """
        if self.last_updated.date() < datetime.datetime.now().date():
            old_last_updated = self.last_updated
            old_articles = self.articles
            self.status = PlaylistUpdating()
            self.update_references()
            try:
                self.articles, query_data = await self.feed_data.run()
                self.last_updated = query_data["updated"]
            except Exception as e:
                self.status = PlaylistError(e)
                self.last_updated = old_last_updated
                self.articles = old_articles
            else:
                self.status = PlaylistOK()
            finally:
                self.update_references()
