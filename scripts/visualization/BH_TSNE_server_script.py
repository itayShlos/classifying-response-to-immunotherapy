"""
Running BH_TSNE.
Conclusion was to use variance 0.315 (~4K genes)
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
import numpy as np
import pickle
from os.path import join
from sklearn.decomposition import PCA
from bhtsne import tsne
from utilities.general_helpers import create_folder



OUTPUT_DIR = r'/storage/md_keren/shitay/outputs/TSNE/cohort_26.6.21/'

# in use only in 'run_bh_tsne' function
FILE_NAME = r'immune_cells_bhtsne_26.6.21.pkl'
PERPLEXITY = 130.0    # default=30.0

# cohort should be normalized and variance filtered
COHORT_PATH = r'/storage/md_keren/shitay/Data/droplet_seq/cohort/normalized/6.21/immune_cells_26.6.21_4k_genes.pkl'


def run_bh_tsne():
    print("Running TSNE")
    print(f'File {COHORT_PATH}')
    # print(f'ARG {sys.argv[1]}')

    cohort = pickle.load(open(COHORT_PATH, 'rb'))
    print(f"Counts shape {cohort.counts.shape}")

    PCs = PCA(n_components=10).fit_transform(cohort.counts)

    print(f"PCs shape {PCs.shape}")

    # cells_embedded = TSNE(n_components=2, perplexity=perplexity, random_state=21).fit_transform()
    cells_embedded = tsne(PCs, perplexity=PERPLEXITY)

    print(f"TSNE output size {cells_embedded.shape}")
    create_folder(OUTPUT_DIR)
    pickle.dump((cells_embedded), open(join(OUTPUT_DIR, FILE_NAME), 'wb'))


def run_bh_tsne_all_perplexity():
    PERPLEXITY = [10.0, 30.0, 50.0, 70.0, 90.0, 110.0, 130.0, 150.0]
    # PERPLEXITY = [30.0,  90.0, 10.0, 50.0, 70.0, 110.0, 130.0, 150.0]   # order changed
    print("run_bh_tsne_all_perplexity")
    print(f'File {COHORT_PATH}')
    # print(f'ARG {sys.argv[1]}')

    cohort = pickle.load(open(COHORT_PATH, 'rb'))
    cohort = cohort.filter_cells_by_property('is_immune', True)
    print(f"Counts shape {cohort.counts.shape}")

    PCs = PCA(n_components=10).fit_transform(cohort.counts)

    print(f"PCs shape {PCs.shape}")

    for perplexity in PERPLEXITY:
        print(f"Running TSNE Using perplexity {perplexity}")
        cells_embedded = tsne(PCs, perplexity=perplexity)
        print(f"TSNE output size {cells_embedded.shape}")
        pickle.dump((cells_embedded), open(join(OUTPUT_DIR, f'perplexity_{perplexity}.pkl'), 'wb'))



if __name__ == '__main__':
    # run_bh_tsne()
    run_bh_tsne_all_perplexity()


