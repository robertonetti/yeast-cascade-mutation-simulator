import subprocess
import numpy as np

class Utility:
    """
    This 'Utility' class contains all the useful function that can be used inside and outside the 
    'Simulator' class. It contains: 
    - some methods to communicate with the MacOS zsh in order to test the RAM usage;
    - some probability distribution methods useful to extract the number of events happening in one
        DNA duplication, or the length of the rearrangement;
    - some methods to randomly initialize the WT chromosomes and their sequence.
    
    Attributes: 
    ----------
        output : str
            It contains the output of the command 'top' of the MacOS zsh which monitors the activity 
            of all the active processes.

    Methods that communicate with zsh for RAM usage: 
    -----------------------------------------------
        get_pid(self)
            It returns the process ID <pid> of the current python process. 
        get_output(self)
            It returns the output of the 'top' command as a string.
        multiplier(self, num: str, lit :str)
            It transfoms the output of the memory usage from the different units (Kb, Mb, Gb) into
            bytes.
        mem_count(self)
            Calls the method 'get_output'. Then it elaborates the output to compute the memory used
            by the python process, and the total amount of used RAM.

    Probability distributions methods:
    ---------------------------------
    int_trunc_exp(a :int, b :int)
        It extracts the length of the rearrangement (integer number) from an exponential 
        distribution truncated between "a" and "b".
    int_trunc_uniform(a :int, b :int)
        It extracts the length of the rearrangement (integer number) from a uniform distribution 
        truncated between "a" and "b".
    poisson_events_number(n_ave: int)
        It extracts the number of events in one cell duplication (integer number) from the Poisson 
        distribution with average "n_ave".

    Methods for WT sequences initialization:
    ---------------------------------------
    random_sequence(self, n_bases :int) -> list
        It creates a DNA sequence of random bases of length 'n_bases'.
    reference_seq_builder(self, n_chromosomes: int, chromosome_lengths) -> list
        It creates a random DNA sequence of the respective length for each of the chromosomes.
    random_seq_initializer(chromosome_lengths: list, n_chr: int)
        Given an array containing the lenghts of the chromosomes and the number of chromosomes, it
        creates a 'chromosome_table' with random sequences.
    A_seq_initializer(chromosome_lengths :list, n_chr: int)
        Given an array containing the lenghts of the chromosomes and the number of chromosomes, it
        creates a 'chromosome_table' with sequences completely composed by the base 'A'.
    """
    output = []

    def get_pid(self):
        """
        It returns the process ID <pid> of the current python process. 

        Returns: 
        -------
            pid (int): process ID of the python3.8 process.
        """
        cmd = "ps -A|grep 'python3.8'"
        output = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0]
        dirty_pid = str(output).split('\n')[0].split()[0]
        pid = dirty_pid[2:]
        return pid

    def get_output(self):
        """
        It returns the output of the 'top' command as a string.

        Returns:
        -------
            self.output (str): splitted output of the command 'top' of the MacOS zsh.
        """
        self.output = subprocess.Popen(["top", "-stats", "pid, command, rsize","-l 1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).communicate()[0]
        return self.output.split("\n")

    def multiplier(self, num: str, unit :str):
        """
        It transfoms the output of the memory usage from the different units (Kb, Mb, Gb) into
        bytes. The original format is: 'number' 'unit'. Where 'number' is an integer while 'unit'
        could be: 'K' (Kb), 'M' (Mb), 'G' (Gb).

        Parameters:
        ----------
            num (str): is the number of Kb, Mb or Gb used by the process.
            unit (str): is the unit 'K','M', or 'G' which respectively are Kb, Mb and Gb.

        Returns:
        -------
            It returns the product between the 'number' and the respective of 1 unit in bytes.
        """
        if unit == 'K': return float(num) * 1024
        elif unit == 'M': return float(num) * 1048576
        elif unit == 'G': return float(num) * 1073741824
        else: return 0

    def mem_count(self):
        """
        Calls the method 'get_output'. Then it elaborates the output to compute the memory used
        by the python process, and the total amount of used RAM.
        
        Returns: 
        -------
            tot_mem (float): total RAM usage in Mb.
            py_mem (float): RAM used by the process 'python3.8' in Mb.
        """
        self.output = self.get_output()
        tot_mem, py_mem = 0.0, 0.0
        for raw in self.output[12:-1]:
            raw_splitted = raw.split()
            num, lit = raw_splitted[2][:-1], raw_splitted[2][-1]
            if raw_splitted[1] == 'python3.8': py_mem += self.multiplier(num, lit)/ 1048576
            tot_mem += self.multiplier(num, lit)
        tot_mem /= 1048576 
        return tot_mem, py_mem

    @staticmethod
    def int_trunc_exp(a :int, b :int):
        """
        It extracts the length of the rearrangement (integer number) from an exponential distribution
        truncated between "a" and "b".

        Parameters:
        ----------
            a (int): left extreme of the distribution domain.
            b (int): right extreme of the distribution domain.

        Returns:
        -------
            rands (int): extracted number.

        Raises:
        ------
            Exception
                If 'a' or 'b' are negative.
        """
        if a <= 0 or b <= 0: raise Exception(f"a<=0 or b<=0. They must be positive")
        a = -np.log(a)
        b = -np.log(b)
        rands = int( np.exp(-(np.random.rand()*(b-a) + a))) 
        return rands

    @staticmethod
    def int_trunc_uniform(a :int, b :int):
        """
        It extracts the length of the rearrangement (integer number) from a uniform distribution 
        truncated between "a" and "b".

        Parameters:
        ----------
            a (int): left extreme of the distribution domain.
            b (int): right extreme of the distribution domain.

        Returns:
        -------
            rands (int): extracted number.

        Raises:
        ------
            Exception
                If 'a' or 'b' are negative.
        """
        if a <= 0 or b <= 0: raise Exception(f"a<=0 or b<=0. They must be positive")
        rands = np.random.randint(a, b)
        return rands

    @staticmethod
    def poisson_events_number(n_ave: int):
        """
        It extracts the number of events in one cell duplicaiton (integer number) from the Poisson 
        distribution with average "n_ave".

        Parameters:
        ----------
            n_ave (int): average number of events in one cell duplication.

        Returns:
        -------
            n_events (int): extracted number of events.
        """
        n_events = np.random.poisson(n_ave)
        return n_events

    @staticmethod
    def random_sequence(n_bases :int): 
        """
        It creates a DNA sequence of random bases of length 'n_bases'. 

        Parameters:
        ----------
            n_bases (int): number of bases of the sequence we want to build.

        Returns:
        -------
            sequence (list): generated sequence (list of strings).
        """
        bases = ["A","G","C","T"]
        sequence = ''.join(np.random.choice(bases, n_bases)) 
        return sequence

    @staticmethod
    def reference_seq_builder(n_chromosomes: int, chromosome_lengths):
        """
        It creates a random DNA sequence of the respective length for each of the chromosomes.

        Parameters:
        ----------
            n_chromosomes (int): number of chromosomes for which we want to build the sequences.
            chromosome_lenghts (list): list of the lengths of the chromosomes considered.

        Returns:
        -------
            reference_seqs (list): list containing the created sequences.

        Raises:
        ------
            Exception
                If the number of chromosomes is larger then the simulated ones.
        """
        if n_chromosomes > len(chromosome_lengths): raise Exception(f"number of chromosomes \
            ({n_chromosomes}) larger than the list of chromosome_lengths ({len(chromosome_lengths)})")
        reference_seqs = [Utility.random_sequence(chromosome_lengths[n]) for n in range(n_chromosomes)]
        return reference_seqs

    def random_seq_initializer(chromosome_lengths: list, n_chr: int):
        """
        Given an array containing the lenghts of the chromosomes and the number of chromosomes, it
        creates a 'chromosome_table' with random sequences.

        Parameters:
        ----------
            chromosome_lengths: list containing the lengths of the chromosomes.
            n_chr (int): number of chromosomes.

        Returns: 
        -------
            chromosome_table (list): list of tuple. Each tuple contains the chromosome ID and its
                                     sequence.
        """
        chromosome_table = []
        id = 1
        for id in range(1, n_chr + 1):
            chromosome_table.append((id, Utility.random_sequence(chromosome_lengths[id - 1])))
        return chromosome_table
        
    def A_seq_initializer(chromosome_lengths: list, n_chr: int):
        """
        Given an array containing the lenghts of the chromosomes and the number of chromosomes, it
        creates a 'chromosome_table' with sequences completely composed by the base 'A'.

        Parameters:
        ----------
            chromosome_lengths: list containing the lengths of the chromosomes.
            n_chr (int): number of chromosomes.

        Returns: 
        -------
            chromosome_table (list): list of tuple. Each tuple contains the chromosome ID and its
                                     sequence.
        """
        chromosome_table = []
        id = 1
        for id in range(1, n_chr + 1):
            chromosome_table.append((id, "A"*chromosome_lengths[id - 1]))
        return chromosome_table