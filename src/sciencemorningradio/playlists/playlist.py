import asyncio
import datetime
import weakref
from typing import Tuple,List
import sciencemorningradio.arxiv_reader as arxiv_reader
from sciencemorningradio.article import Article
from sciencemorningradio.playlists.read_playlist import read_playlist

class PlaylistStatus():
    pass

class PlaylistOK(PlaylistStatus):
    pass

class PlaylistError(PlaylistStatus):
    def __init__(self,error:Exception):
        self.error = error

class PlaylistUpdating(PlaylistStatus):
    def __init__(self,request:asyncio.Task,**kwargs):
        self.request = request
        self.data = kwargs

class Playlist():
    def __init__(self,name: str,articles: List[Article],read_attributes: Tuple[str]=("title","authors","abstract")):
        self.name:str = name
        self.articles: List[Article] = articles
        self.read_attributes = read_attributes
        self.status: PlaylistStatus = PlaylistOK()
        self._references = weakref.WeakKeyDictionary()
    
    def register_reference(self,reference,behavior):
        self._references[reference] = behavior

    def update_references(self):
        for (reference, behavior) in self._references.items():
            behavior(reference,self)
            

    def read(self,engine,**kwargs):
        """
        Uses text to speach engine engine to read out loud the article 
        attributes spesified by the playlist
        """
        read_playlist(engine,self)

class Feed(Playlist):
    def __init__(self,name: str,feed_data: arxiv_reader.Query,read_attributes: Tuple[str]=None):
        if read_attributes is None:
            super().__init__(name,[])
        else:
            super().__init__(name,[],read_attributes)
        self.feed_data = feed_data
        self.last_updated = datetime.datetime.fromtimestamp(0)
        self.update()

    def update(self):
        """
        Updates the current list of articles to the latest available from
        arXive.org. If arXiv.org would not have been updated since the last
        update, it has no effect
        """

        async def update_internal():
            try:
                new_articles, query_data = await self.feed_data.run()
                self.articles.extend(new_articles)
                self.last_updated = query_data["updated"]
            except Exception as e:
                self.status = PlaylistError(e)
                self.last_updated = old_last_updated
                self.articles = old_articles
            else:
                self.status = PlaylistOK()
            finally:
                self.update_references()

        if self.last_updated.date() < datetime.datetime.now().date():
            old_last_updated = self.last_updated
            old_articles = self.articles
            self.status = PlaylistUpdating(asyncio.create_task(update_internal()))
            self.update_references()

    async def read(self,engine,timeout:float=5,**kwargs):
        """
        Uses text to speach engine engine to read out loud the article 
        attributes spesified by the playlist
        """
        if isinstance(self.status, PlaylistUpdating):
            try:
                await asyncio.wait_for(self.status.request, timeout=timeout)
            except asyncio.TimeoutError as te:
                self.status = PlaylistError(te)

        if isinstance(self.status, PlaylistError):
            raise RuntimeError(f"Cannot read feed {self.name} because an error occurred: {self.status.error}")

        super().read(engine)






