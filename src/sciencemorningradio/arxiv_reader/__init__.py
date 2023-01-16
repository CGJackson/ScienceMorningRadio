from dataclasses import dataclass
from enum import Enum
import src.sciencemorningradio.arxiv_reader.query as query

class SortBy(Enum):
    relevance
    lastUpdatedDate
    submittedDate

class SortDirections(Enum):
    ascending=1
    descending=-1

class SearchFields(Enum):
    all
    id
    report_number
    category
    journal_reference
    comment
    abstract
    title

@dataclass
class Query():
    """
    Stores the data about a query to the arxiv API
    """
    search:Optional[Dict[SearchFields,str]]=None,
    ids:Optional[List[str]]=None,
    start:Optional[int]=None,
    max_results:Optional[int]=None,
    sort_by:Optional[SortBy]=None,
    sort_direction:Optional[SortDirection]=None

    def run(self)
        return get_articles(search={field.name:data 
                                for field,data in self.search.items()},
                            ids=self.ids
                            start=self.start
                            max_results=self.max_results
                            sort_by=self.sort_by.name
                            sort_direction=self.sort_direction.value)
