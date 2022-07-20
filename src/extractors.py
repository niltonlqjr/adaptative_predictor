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

class ExecutionGoalExtractor:
    _number_runs = 1
    _goal_list = ['runtime']
    _weight_list = ['1']
    @classmethod
    def set_number_runs(cls, 
                        num):
        """Set the number of runs used to extract the goal (default: 1)
        Parameters
        num: int
            Number of executions for extract the goal
        """

        if num < 1 or int(num) != num:
            raise Exception("The number of executions must be an integer greater or equal 1")
        cls._number_runs = num

    @classmethod
    def set_goal(cls,
                 goal_list,
                 weight_list):
        """Set the goal list and weight for each goal
        Parameters:
            goal_list: list
                each element is a name of one goal (string)
            weight_list: list
                each element is the wieght for the goal at the same position of goal_list 
        """
        if len(goal_list) != len(weight_list):
            raise Exception("Goal list and weight list must have the same length")
        cls._goal_list = goal_list
        cls._weight_list = weight_list
    
    @classmethod
    def get_execution_goal(cls,
                 bench_dir,
                 sequence_str,
                 working_set=0):
        goal = Goal.prepare_goal(cls._goal_list,cls._weight_list)
        goal_seq = Engine.evaluate(goals=goal,
                                    sequence=sequence_str,
                                    compiler='opt',
                                    benchmark_directory=bench_dir,
                                    times=cls._number_runs,
                                    working_set=working_set)
        return goal_seq
        

class SpeedupExtractor(ExecutionGoalExtractor):
    """Class to extract speedup from benchmarks"""
    _baseline = '-O0'
    @classmethod 
    def set_baseline(cls,
                     baseline):
        """set the baseline used to calculate speedup (default O0)"""
        cls._baseline=baseline

    @classmethod
    def set_goal(cls,
                 goal_list,
                 weight_list):
        raise Exception("You can't change the goal for speedup. It must be ruuntime")

    @classmethod
    def get_sepeedup(cls, 
                     bench_dir,
                     sequence_str,
                     working_set=0):
        """
        Compile and execute the program with sequence argument and the baseline level O0
        (you can change the beseline method set_baseline).
        Calculates the speedup of sequence and baseline.
        You can define the number of runs with method set_number_runs 
        bench_dir: str
            directory of one benchmark ready to compile and run with Yacos 
            (with makefile.opt, configure.sh and execute.sh)
        sequence_str : string
            The optimization sequence string
        working_set: str
        """
        goal_baseline = cls.get_execution_goal(bench_dir=bench_dir,
                                               sequence_str=cls._baseline,
                                               working_set=working_set)
        
        goal_seq = cls.get_execution_goal(bench_dir=bench_dir,
                                          sequence_str=sequence_str,
                                          working_set=working_set)
        
        return goal_baseline/goal_seq