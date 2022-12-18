import urllib.request as urlrequest
import urllib.parse
from typing import Optional,List,Dict

import feedparser

from sciencemorningradio.article import Article

# Opensearch metadata such as totalResults, startIndex, 
# and itemsPerPage live in the opensearch namespase.
# Some entry metadata lives in the arXiv namespace.
# This is a hack to expose both of these namespaces in
# feedparser v4.1
#feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
#feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'


def url_builder(search:Optional[Dict[str,str]]=None,
        ids:Optional[List[str]]=None,start:Optional[int]=None,
        max_results:Optional[int]=None,sort_by:Optional[str]=None,
        sort_direction:Optional[int]=None)->str:
        
    elements = []

    if search is not None:
        elements.append(_build_search_string(search))
    
    if ids is not None:
        ids_string = ','.join(urllib.parse.quote_plus(i,safe='.') for i in ids)
        elements.append('id_list='+ids_string)

    if start is not None:
        elements.append(f"start={start}")

    if max_results is not None:
        elements.append(f"max_results={max_results}")

    return url_builder._base_url + '&'.join(elements)

url_builder._base_url = 'http://export.arxiv.org/api/query?'

def _build_search_string(search_parameters:Dict[str,str]):
    if any(search_field not in _build_search_string._search_fields 
            for search_field in search_parameters):
        raise ArgumentError(f"Invalid search field passed to url_builder in {search_parameters}")

    search_terms = [
            f'{_build_search_string._search_fields[field]}:{urllib.parse.quote_plus(term)}'
            for field,term in search_parameters.items()] 

    return 'search_query=' + '+AND+'.join(search_terms)

_build_search_string._search_fields = {'all':'all','id':'id','report number':'rn',
        'category':'cat','journal reference':'jr','comment':'co',
        'abstract':'abs','author':'au','title':'tl'}


def get_articles(search:Optional[Dict[str,str]]=None,
        ids:Optional[List[str]]=None,start:Optional[int]=None,
        max_results:Optional[int]=None,sort_by:Optional[str]=None,
        sort_direction:Optional[int]=None)->List[Article]:
        
        query_url = url_builder(search,ids,start,max_results,
                                sort_by,sort_direction)

        with urlrequest.urlopen(query_url) as responce:
            text = responce.read()

        parsed_responce, metadata = parse_query(text)
        return parsed_responce, metadata


def parse_query(responce_text):
    feed = feedparser.parse(responce_text)
    return ([_feed_entry_to_article(entry) for entry in feed],
            {'title':feed.feed.title,
             'updated':datetime.fromisoformat(feed.feed.updated)})


def _feed_entry_to_article(feed_entry) -> Article:

    published_date = datetime.fromisoformat(feed_entry.published)
    updated_date = datetime.fromisoformat(feed_entry.updated)

    affiliations = {}
    for author in feed_entry.authors:
        try:
            affiliations[author.name]=author.arxiv_affiliation
        except AttributeError:
            affiliations[author.name]=None

    links = {('main' if link.rel == 'alternate' else link.title):link.href 
            for link in feed_entry.links}
    try:
        journal_ref = feed_entry.arxiv_journal_ref
    except AttributeError:
        journal_ref = None

    try:
        comment = feed_entry.comment
    except AttributeError:
        comment = None

    return Article(title=feed_entry.title,
                   id=feed_entry.id.split('/abs/'),
                   published=published_date,
                   updated=updated_date,
                   authors=[author.name for author in feed_entry.author],
                   author_affiliations = affiliations,
                   primary_category=(feed_entry.arxiv_primary_category.term,
                                     feed_entry.arxiv_primary_category.scheme),
                   categories=[(cat.term,cat.scheme) for cat in feed_entry.categories],
                   link=links['main'],
                   pdf_link=links['pdf'],
                   doi=feed_entry.arxiv_doi,
                   resolved_doi=links.get('doi',None),
                   journal_reference=journal_ref,
                   comment=comment)




        # see 
        # https://static.arxiv.org/static/arxiv.marxdown/0.1/help/api/examples/python_arXiv_parsing_example.txt
        # for example
