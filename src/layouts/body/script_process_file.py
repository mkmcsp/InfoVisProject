import io

import pandas as pd
import numpy as np


def process_file(file_nodes, file_edges):
    genes = pd.read_csv(io.StringIO(file_nodes.decode('utf-8')), sep='\t')
    genes = genes.replace('-', np.nan)
    genes = genes[['OFFICIAL SYMBOL', 'CATEGORY VALUES', 'SUBCATEGORY VALUES']]
    interactions = pd.read_csv(io.StringIO(file_edges.decode('utf-8')), sep='\t', dtype='string')
    interactions = interactions[['Official Symbol Interactor A', 'Official Symbol Interactor B']]
    return genes, interactions
