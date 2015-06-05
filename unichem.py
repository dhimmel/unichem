import requests
import collections

id_to_source = {
    0: None,
    1: 'chembl',
    2: 'drugbank',
    3: 'pdb',
    4: 'iuphar',
    5: 'pubchem_dotf',
    6: 'kegg_ligand',
    7: 'chebi',
    8: 'nih_ncc',
    9: 'zinc',
    10: 'emolecules',
    11: 'ibm',
    12: 'atlas',
    13: 'ibm_patents',
    14: 'fdasrs',
    15: 'surechembl',
    17: 'pharmgkb',
    18: 'hmdb',
    20: 'selleck',
    21: 'pubchem_tpharma',
    22: 'pubchem',
    23: 'mcule',
    24: 'nmrshiftdb2',
    25: 'lincs',
    26: 'actor',
    27: 'recon',
    28: 'molport',
    29: 'nikkaji',
    31: 'bindingdb',
}

source_to_id = {v: k for k, v in id_to_source.items()}

def connectivity_query(search_url, target = None, B = 0, C = 0, D = 0, E = 0, F = 0, G = 0):
    """
    https://www.ebi.ac.uk/unichem/info/widesearchInfo
    """
    url = '{search_url}/{A}/{B}/{C}/{D}/{E}/{F}/{G}/{H}'.format(
        search_url = search_url,
        A = source_to_id[target], # Sources
        B = B, # Pattern
        C = C, # Component Mapping
        D = D, # Frequency Block
        E = E, # InChI Length Block
        F = F, # UniChem Labels
        G = G, # Assignment Status
        H = 1, # Data Structure
    )
    response = requests.get(url)
    try:
        response = response.json()
    except ValueError:
        print('cannot decode json:', url)
        return
    if 'error' in response:
        print('UniChem error:', response['error'])
        return
    for assignment in response.values():
        header = assignment.pop(0)
        for match in assignment:
            yield collections.OrderedDict(zip(header, match))

def key_search(inchikey, **kwargs):
    """Search by InChIKeys."""
    if inchikey.startswith('InChIKey='):
        prefix, inchikey = inchikey.split('=', 1)
    base_url = 'https://www.ebi.ac.uk/unichem/rest/key_search'
    search_url = '{base_url}/{StandardInChIKey}'.format(
        base_url = base_url,
        StandardInChIKey = inchikey)
    return connectivity_query(search_url, **kwargs)

def cpd_search(source, compound_id, **kwargs):
    """Search by source-specific identifiers."""
    base_url = 'https://www.ebi.ac.uk/unichem/rest/cpd_search'
    search_url = '{base_url}/{src_compound_id}/{src_id}'.format(
        base_url = base_url,
        src_compound_id = compound_id,
        src_id = source_to_id[source])
    return connectivity_query(search_url, **kwargs)
