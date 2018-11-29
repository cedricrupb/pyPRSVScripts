""" Script to scan sv-benchmark (https://github.com/sosy-lab/sv-benchmarks) directory for tasks"""
from glob import glob
from utils import load_constants
import argparse
import logging

__CONSTANTS__ = load_constants()
__SV_COMP_BASE_PATH__ = __CONSTANTS__['sv_benchmark_path']

if __name__ == "__main__":

    global __SV_COMP_BASE_PATH__
    prefix = __SV_COMP_BASE_PATH__

    parser = argparse.ArgumentParser()
    parser.add_argument("output")

    args = parser.parse_args()

    L = []

    logging.info("Start to scan directory %s" % prefix)
    L.extend("%s/%s" % (prefix, "*/*.i"))
    L.extend("%s/%s" % (prefix, "*/*.c"))

    with open(args.output, "w") as o:
        for p in L:
            p = p.replace(prefix, "")
            o.write("%s\n" % p)
