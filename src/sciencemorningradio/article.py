import dataclasses
import datetime
from collections import namedtuple
from typing import List,Tuple,Optional,NamedTuple,Dict

@dataclasses.dataclass
class Article():
    title: str
    id: str
    puplished: datetime.datetime
    updated: datetime.datetime
    abstract: str
    authors: List[str]
    author_affiliations: Dict[str,Tuple[str]]
    primary_category: Tuple[str,str]
    category: List[Tuple[str,str]]
    link: str
    pdf_link: str
    doi: Optional[str]
    resolved_doi: Optional[str]
    journal_reference: Optional[str]
    comment: Optional[str]

