"""
Run this script to create a file which will be processed in cNMF.py

several instructions:
1. the counting table shouldn't be normalized, since there is a normalization stage which different from our method
during the cNMF preparation process.

2. Only genes with a total count != 0 should be taken.
"""

# ------- SERVER EXTENSIONS ---------
lib =  r'/srv01/technion/shitay/Code/classifying_response_to_immunotherapy/utilities/droplet_dataset'
lib2 = r'/srv01/technion/shitay/Code/classifying_response_to_immunotherapy/utilities'
lib3 = r'/srv01/technion/shitay/Code/classifying_response_to_immunotherapy/data_analysis'
lib4 = r'/srv01/technion/shitay/Code/classifying_response_to_immunotherapy'
lib5 = r'/srv01/technion/shitay/Code/classifying_response_to_immunotherapy/scripts'
import sys
sys.path.append(lib)
sys.path.append(lib2)
sys.path.append(lib3)
sys.path.append(lib4)
sys.path.append(lib5)
# ------- SERVER EXTENSIONS ---------

import pickle
import numpy as np

# You should put a path of non_normalize cohort with immune and tumor cells without variance filter.
COHORT_PATH = r'/storage/md_keren/shitay/Data/droplet_seq/cohort/non_normalized/6.21/cohort_non_normalized_10.6.21.pkl'
OUTPUT_PATH = r'/storage/md_keren/shitay/outputs/cNMF/conversions/tumor_filtered_cNMF_10.6.21.txt'
CONVERT_TUMOR = True     # False for immune


if __name__ == '__main__':

    print(f'Starting data conversion for cNMF')
    cohort = pickle.load(open(COHORT_PATH, 'rb'))
    print(f'{COHORT_PATH} file has been loaded')
    if CONVERT_TUMOR:
        cohort = cohort.filter_cells_by_property('is_cancer', True)
        print(f'tumor cells only')
    else:
        cohort = cohort.filter_cells_by_property('is_immune', True)
        print(f'immune cells only')

    counts = cohort.counts
    cell_ids = [f'_'.join(v) for v in list(zip(cohort.samples, cohort.barcodes))]
    gene_ids = cohort.features
    gene_names = cohort.gene_names

    # drop all gene with count=0
    gene_indices = (np.sum(counts, axis=0)!=0)
    gene_names = [gene_names[i] for i in range(len(gene_names)) if gene_indices[i]]
    gene_ids = [gene_ids[i] for i in range(len(gene_names)) if gene_indices[i]]
    values = counts[:, gene_indices]
    print(values.shape)

    print(f'Saving output in {OUTPUT_PATH}')
    # build file and save it
    with open(OUTPUT_PATH, 'w') as writer:

        gene_file = ''
        for gene in gene_names:
            gene_file += '\t'+gene
        gene_file += '\n'
        writer.write(gene_file)

        cell_file = ''
        for c_idx in range(len(cell_ids)):
            cell_file += cell_ids[c_idx]+'\t'+'\t'.join(values[c_idx].astype(str).tolist())+'\n'
        writer.write(cell_file)