from abc import abstractmethod
import argparse
import sys
import os

import numpy as np

from pathlib import Path
from sympy import false

from yacos.essential import Engine
from yacos.essential import Goal

from yacos.info.ncc import Inst2Vec
from yacos.info import compy
from yacos.info.compy.extractors import LLVMDriver

class IR2vecExtractor:
    """ Extract IR2vec """
    @staticmethod
    def extract_representation(bench_dir, sequence_str):
        """Extract IR2vec representation from a 
        """
        Engine.compile(benchmark_directory=bench_dir,
                       sequence=sequence_str,
                       compiler='opt')
        
        driver = LLVMDriver([])
        builder = compy.LLVMIR2VecBuilder(driver)
        info = builder.ir_to_info(os.path.join(bench_dir,
                                               'a.out_o.bc'))
        repr = info.moduleInfo.ir2vec
        return repr

class HistogramExtractor:
    keys = ['ret',
            'br',
            'switch',
            'indirectbr',
            'invoke',
            'callbr',
            'resume',
            'catchswitch',
            'catchret',
            'cleanupret',
            'unreachable',
            'fneg',
            'add',
            'fadd',
            'sub',
            'fsub',
            'mul',
            'fmul',
            'udiv',
            'sdiv',
            'fdiv',
            'urem',
            'srem',
            'frem',
            'shl',
            'lshr',
            'ashr',
            'and',
            'or',
            'xor',
            'extractelement',
            'insertelement',
            'sufflevector',
            'extractvalue',
            'insertvalue',
            'alloca',
            'load',
            'store',
            'fence',
            'cmpxchg',
            'atomicrmw',
            'getelementptr',
            'trunc',
            'zext',
            'sext',
            'fptrunc',
            'fpext',
            'fptoui',
            'fptosi',
            'uitofp',
            'sitofp',
            'ptrtoint',
            'inttoptr',
            'bitcast',
            'addrspacecast',
            'icmp',
            'fcmp',
            'phi',
            'select',
            'freeze',
            'call',
            'var_arg',
            'landingpad',
            'catchpad',
            'cleanuppad']
    @classmethod
    def _program_representation(cls, functionInfos):
        """calculate program representation."""
        values = []
        for data in functionInfos:
            values.append([data.instructions[key] for key in cls.keys])

        return [sum(x) for x in zip(*values)]
    
    @classmethod
    def extract_representation(cls, bench_dir,
                               sequence_str):
        Engine.compile(benchmark_directory=bench_dir,
                       sequence=sequence_str,
                       compiler='opt')
        driver = LLVMDriver([])
        builder = compy.LLVMHistogramBuilder(driver)
        info = builder.ir_to_info(os.path.join(bench_dir,
                                               'a.out_o.bc'))
        repr = cls._program_representation(info.functionInfos)
        return repr

class Inst2vecExtractor:
    @staticmethod
    def extract_representation(bench_dir, sequence_str):
        '''inst2vec={}
        Inst2Vec.prepare_benchmark(bench_dir)
        rep = Inst2Vec.extract(data_type="index")
        Inst2Vec.remove_data_directory()
        for bench, indexes in rep.items():
            inst2vec[bench] = indexes
        
        embeddings = Inst2Vec.embeddings
        for bench,indexes in inst2vec.items():
            vals = [list(embeddings[idx]) for idx in indexes]
        print(vals[0][0:5])
        repr = vals
        '''
        print('Not implemented yet',file=sys.stderr)
        exit(0)

class SpeedupExtractor:
    _baseline = '-O0'
    _number_runs = 1
    @classmethod 
    def set_baseline(cls, baseline):
        cls._baseline=baseline
    @classmethod
    def set_exec_number(cls, num):
        if num < 1 or int(num) != num:
            raise Exception("The number of executions must be an integer greater or equal 1")
        cls._number_runs = num

    @classmethod
    def get_sepeedup(cls, 
                     bench_dir,
                     sequence_str,
                     working_set=0):
        """
        Compile and execut the program with sequence argument and the baseline level O0
        (you can change the beseline method set_baseline)
        Calculates the speedup of sequence and baseline
        bench_dir: str
            directory of one benchmark ready to compile and run with Yacos 
            (with makefile.opt, configure.sh and execute.sh)
        sequence_str : string
            The optimization sequence string
        working_set: str
        """
        goal = Goal.prepare_goal(['runtime'],[1])
        #Engine.compile(benchmark_directory=bench_dir,
        #               sequence=cls._baseline,
        #               compiler='opt')
        #g_b = Engine.only_evaluate(goals=goal,
        #                           benchmark_directory=bench_dir,
        #                           working_set=working_set)
        goal_baseline = Engine.evaluate(goals=goal,
                                        sequence=cls._baseline,
                                        compiler='opt',
                                        benchmark_directory=bench_dir)
        goal_seq = Engine.evaluate(goals=goal,
                                   sequence=sequence_str,
                                   compiler='opt',
                                   benchmark_directory=bench_dir)
        return goal_baseline/goal_seq