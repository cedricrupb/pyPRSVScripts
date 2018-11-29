"""
    A scripts to transform a C program with PeSCo (https://github.com/cedricrupb/cpachecker)
"""
import os
import subprocess
from subprocess import PIPE
from os.path import join, isdir, isfile
import logging
import argparse
from tqdm import tqdm
import json
from utils import load_constants


__CONSTANTS__ = load_constants()
__PESCO_PATH__ = __CONSTANTS__['pesco_path']
__SV_COMP_BASE_PATH__ = __CONSTANTS__['sv_benchmark_path']


def graphId(s):
    global __SV_COMP_BASE_PATH__
    s = s.replace(__SV_COMP_BASE_PATH__, "")
    s = s.replace("/", "_")
    s = s.replace(".", "_")
    return s


def checkIfEmpty(path):
    if not isfile(path):
        return True

    return os.stat(path).st_size == 0


def generate(path_to_source, timeout=900):
    global __PESCO_PATH__

    pesco_path = __PESCO_PATH__
    output_path = join(pesco_path, "output", graphId(path_to_source)+".dfs")

    if not isdir(pesco_path):
        raise ValueError("Unknown pesco path %s" % pesco_path)
    if not (isfile(path_to_source) and (path_to_source.endswith('.i') or path_to_source.endswith('.c'))):
        raise ValueError('path_to_source is no valid filepath. [%s]' % path_to_source)

    proc = subprocess.run(
                            [pesco_path,
                             "-graphgen",
                             "-heap", "1000m",
                             "-setprop", "graphGen.output="+output_path,
                             ],
                            check=False, stdout=PIPE, stderr=PIPE,
                            timeout=timeout
                            )

    if proc.returncode != 0 or checkIfEmpty(output_path):
        logging.error(proc.args)
        logging.error(proc.stdout.decode('utf-8'))
        logging.error(proc.stderr.decode('utf-8'))
        raise ValueError("Something went wrong while processing: %s" % path_to_source)

    return output_path


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    parser.add_argument("-t", "--timelimit", type=int)
    parser.add_argument("output_list", type=str)

    args = parser.parse_args()

    if not isfile(args.input_file):
        raise ValueError("Unknown input path: %s" % args.input_file)

    Input = []
    with open(args.input_file, "r") as inp:
        for line in inp:
            Input.append(line)

    logging.info("Start processing %d programs" % len(Input))
    Output = []
    Fail = []

    timelimt = 900
    if args.timelimit:
        timelimit = args.timelimit

    for f in tqdm(Input):
        try:
            output = generate(f, timelimit)
            Output.append(output)
        except ValueError:
            Fail.append(f)

    with open(args.output_list, "w") as o:
        json.dump({
            'success': Output,
            'fail': Fail
        }, o, indent=4)
