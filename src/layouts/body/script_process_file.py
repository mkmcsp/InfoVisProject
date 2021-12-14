import pandas as pd
import numpy as np


def process_file(file_nodes, file_edges):
    genes = pd.read_csv(file_nodes, sep='\t')
    genes = genes.replace('-', np.nan)
    genes = genes[['OFFICIAL SYMBOL', 'CATEGORY VALUES', 'SUBCATEGORY VALUES']]
    interactions = pd.read_csv(file_edges, sep='\t', dtype='string')
    interactions = interactions[['Official Symbol Interactor A', 'Official Symbol Interactor B']]
    return genes, interactions
