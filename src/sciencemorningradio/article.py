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

    def get_readable_string(self,attr_name:string) -> str:
        data = getattr(self,attr_name)
        if data is None:
            raise ArticleMissingAttributeError(
                f"The article {title} does not have a {attr_name} listed")
        if type(data) is str:
            return data
        if type(data) is datetime.datetime:
            if data.day % 10 == 1:
                day_suffix = "st"
            elif data.day % 10 == 2:
                day_suffix = "nd"
            else:
                day_suffix = "st"
            return data.strfttime(f"%d{day_suffix} %B %Y")
        if attr == "authors":
            return " ".join(data)
        if attr == "primary_category":
            return data[0]
        if attr == "categories":
            return " ".join([category[0] for category in data])
        if attr == "author_affiliations":
            auth_aff_strings = []
            for auth, affs in data.items():
                aff_strings = " ".join(affs)
                auth_aff_strings.append(f"{auth} {aff_strings}")
            return " ".join(auth_aff_strings)

        raise NotImplementedError(f"readable string for {attr} not implemented")

class ArticleMissingAttributeError(RuntimeError):
    pass
