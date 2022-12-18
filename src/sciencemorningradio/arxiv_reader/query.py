from typing import Optional

def url_builder(search:Optional[dict]=None,ids:Optional[list]=None,
        start:Optional[int]=None,max_results:Optional[int]=None,
        sort_by:Optional[str]=None,sort_direction:Optional[int]=None)->str:
        
    elements = []

    if search is not None:
        elements.append(_build_search_string(search))
    
    if ids is not None:
        ids_string = ','.join(str(i) for i in ids)
        elements.append('id_list='+ids_string)

    if start is not None:
        elements.append(f"start={start}")

    if max_results is not None:
        elements.append(f"max_results={max_results}")

    return url_builder._base_url + '&'.join(elements)

url_builder._base_url = 'http://export.arxiv.org/api/query?'

def _build_search_string(search_parameters:dict):
    if any(search_field not in _build_search_string._search_fields 
            for search_field in search_parameters):
        raise ArgumentError(f"Invalid search field passed to url_builder in {search_parameters}")

    search_terms = [f'{_build_search_string._search_fields[field]}:{term}'
            for field,term in search_parameters.items()] 

    return 'search_query=' + '+AND+'.join(search_terms)

_build_search_string._search_fields = {'all':'all','id':'id','report number':'rn',
        'category':'cat','journal reference':'jr','comment':'co',
        'abstract':'abs','author':'au','title':'tl'}
