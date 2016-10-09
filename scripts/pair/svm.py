#!/usr/bin/env python

import os
import sys
import time

import pandas as pd
import numpy as np

from runtimes import get_runtime_dataframe, get_runtime_pivot_tables
from util import *

def add_to_classifier(X, Y):
    X = None
    Y = None
    return (X, Y)

def make_matrix(results_file, output_file):
    df = load_as_X(results_file, aggregate_samples='meanstd', cut_off_nan=True)
    df.to_csv(output_file, index=False)

if __name__ == '__main__':
    pd.set_option('display.max_rows', 10)
    pd.set_option('display.max_columns', 5)
    pd.set_option('display.width', 160)

    ## Settings:
    MATRIX_FILE = 'matrix_X_uncore_shared.csv'
    TO_BUILD = ['L3-SMT'] # 'L3-SMT-cores'
    CLASSIFIER_CUTOFF = 1.15

    X = pd.DataFrame()
    Y = pd.Series()

    runtimes = get_runtime_dataframe(sys.argv[1])

    for config, table in get_runtime_pivot_tables(runtimes):
        if config in TO_BUILD:
            for (A, values) in table.iterrows():
                for (i, normalized_runtime) in enumerate(values):
                    B = table.columns[i]

                    classification = 'Y' if normalized_runtime > CLASSIFIER_CUTOFF else 'N'
                    results_path = os.path.join(sys.argv[1], config, "{}_vs_{}".format(A, B))
                    matrix_file = os.path.join(results_path, MATRIX_FILE)

                    if os.path.exists(os.path.join(results_path, 'completed')):
                        if not os.path.exists(matrix_file):
                            print "No matrix file found, run the scripts/pair/matrix.py script first!"
                            sys.exit(1)
                        df = pd.read_csv(matrix_file, index_col=False)

                        Y = pd.concat([Y, pd.Series([classification for _ in range(0, df.shape[0])])])
                        X = pd.concat([X, df])
                    else:
                        print "Exclude unfinished directory {}".format(results_path)

    X['Y'] = Y
    print X.shape
    X.to_csv(os.path.join(sys.argv[1], 'wekka_xy_L3-SMT_uncore_shared.csv'), index=False)
