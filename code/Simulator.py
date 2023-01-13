from code.BinaryTree import Node
from code.Cell import Cell
from code.WTCell import WT_Cell
from code.MutantCell import MUT_Cell
from code.Utility import Utility
import copy
import numpy as np
import matplotlib.pyplot as plt
import gc

from code.PointwiseReplacement import PointReplacement
from code.PointwiseDeletion import PointDeletion
from code.PointwiseInsertion import PointInsertion
from code.Insertion import Insertion
from code.Deletion import Deletion
from code.Translocation import Translocation
from code.ReciprocalTranslocation import ReciprocalTranslocation
from code.Duplication import Duplication

class Simulator():
    """
    It simulates cell duplication up to the selected number of generations. It then reconstructs the
    DNA sequences considering all mutations and rearrangements added by the simulation.
    
    Attributes
    ----------
    parent : Node
        It ontains the ancestor (WT) cell, from which it is possible to acces the whole tree of cells
        generated.
    generations : int
        Number of generations simulated.
    leaves : list
        It contains the cells corresponding to the leaves of the tree generated by the simulation, 
        i.e. the last generation of cells. 
    average_genome_length : float
        The average length of the whole genome. Averaged over the last generation of cells.
    average_chromosome_length : list
        List of the average chromosome lenght for each chromosome. Averaged over the last generation
        of cells.
    chr_length_st_dev : list
        List of the standard deviation of the chromosome lenght for each chromosome. Computed over 
        the last generation of cells.

    General Methods
    ---------------
    leaves_collector(self, cell: Cell)
        It appends to a list all the leaves of the simulation.

    Methods Generating Random Rearrangement
    ---------------------------------------
    rand_insertion(self, cell: Cell, length_extraction_method, visual: bool)
        It generates a random Insertion, according to a given distirbution. Then calls the function 
        that adds it to the events of the considered cell.
    rand_deletion(self, cell :Cell, length_extraction_method, visual: bool)
        It generates a random Deletion, according to a given distirbution. Then calls the function 
        that adds it to the events of the considered cell.
    rand_translocation(self, cell :Cell, length_extraction_method, visual: bool)
        It generates a random Translocation, according to a given distirbution. Then calls the function 
        that adds it to the events of the considered cell.
    rand_reciprocal_translocation(self, cell :Cell, length_extraction_method, visual: bool)
        It generates a random Reciprocal Translocation, according to a given distirbution. Then calls
        the function that adds it to the events of the considered cell.
    rand_duplication(self, cell :Cell, length_extraction_method, visual: bool)
        It generates a random Duplication, according to a given distirbution. Then calls the function
        that adds it to the events of the considered cell.

    Methods Generating Random Mutation
    ----------------------------------
    rand_point_insertion(self, cell: Cell, visual: bool)
        It generates a random Pointwise Insertion, drawing its position from a Uniform distribution.
        Then calls the function that adds it to the events of the considered cell.
    rand_point_deletion(self, cell :Cell, visual: bool)
        It generates a random Pointwise Deletion, drawing its position from a Uniform distribution.
        Then calls the function that adds it to the events of the considered cell.
    rand_point_replacement(self, cell :Cell, visual: bool)
        It generates a random Pointwise Replacement, drawing its position from a Uniform distribution.
        Then calls the function that adds it to the events of the considered cell.

    Methods for Cell Duplication & Growth
    -------------------------------------
    random_choice(self, cell: Cell, cumulative_list :list, del_len_distrib, ins_len_distrib,
                  transl_len_distrib, rec_transl_len_distrib, dupl_len_distrib, visual: bool)
        Given that an event happens, this funciton chooses which event happen according to the
        cumulative probability given in 'cumulative_list'.
    node_duplication(self, node: Node, cumulative_list :list, ave_events_num, del_len_distrib,
                     ins_len_distrib, transl_len_distrib, rec_transl_len_distrib, dupl_len_distrib,
                     n_event_method, visual: bool)
        Given the current 'node' and the distribution of the number of events in one duplication
        (n_ave_method), it creates two doughter nodes, and calls 'random_choice' to add the
        extracted number of events to them.
    growth(self, node :Node, n_generations :int, ave_events_num, cumulative_list, n_event_method,
           del_len_distrib, ins_len_distrib, transl_len_distrib, rec_transl_len_distrib,
           dupl_len_distrib, visual: bool)
        Recurrent functions that starting with one Wild Type Cell (in a node) calls itself 
        duplicating every time each node, up to 'n_generations' generations. The result is a Binary
        Tree accessible from the parent node (WT Cell).
        It saves in an array all the leaves of the last generaitons and computes averages and 
        standard deviations on the chromosomes and genome lengths.

    Methods for Cell Sequences Reconstruction
    -----------------------------------------
    WT_sequence_initializer(self, cell: WT_Cell)
        Given a WT cell, it fills each of the chromosomes of the WT_Cell.DNA.CHRs attribute with the
        corresponding sequence according to the 'chromosome_table' parameter.
    single_doughter_reconstructor(self, parent: Node, doughter: Node)
        It copies the DNA sequences from the parent to the doughter cell. Then it modifies them 
        according to the new events present in the doughter cell.
    reconstructor(self, parent: Node, n_generations: int)
        Recurrent functions that starting with 'parent' node (from which the all tree of new 
        generations is accessible) calls itself reconstructing every time both the doughters of the
        parent, up to 'n_generations' generations. In the end only the leaves of the 'n_generation' 
        generation will contain the modified sequences.
    path_reconstructor(self, path, n_generations: int)
        Given a path and the total number of simulated generations 'n_generations', this function 
        reconstructs the sequence of the leaf corresponding to the path.
    
    Methods to compute statistics
    -----------------------------
    update_average_genome_length(self, node: Node)
        It updates the length of the whole genome in order to comute the average.
    update_average_chromosome_length(self, node: Node)
        It updates the length of each chromosome in order to comute the average.
    chromosome_std_dev(self, n_chr: int, n_gen: int)
        It computes the Standard Deviation of the final length of each Chromosome.

    Methods for result visualization
    --------------------------------
    chromosome_visualizator(self, leaf_number: int):
        Displays the chromosome of a selected leaf, highlighting locations where multiple 
        Rearrangements/Mutations have occurred.
    """
    def leaves_collector(self, cell: Cell):
        """
        It appends to a list all the leaves of the simulation.

        Parameters
        ----------
            cell (Cell): cell we want to add to the list of leaves
        """
        self.leaves.append(cell)

############################## RANDOM REARRANGEMENT METHODS ##########################################################

    def rand_insertion(self, cell: Cell, length_extraction_method, visual :bool):
        """
        It generates a random Insertion, according to a given distirbution. Then calls the function 
        that adds it to the events of the considered cell.

        Parameters
        ----------
            cell (Cell): considered cell.
            length_extraction_method (Method): probability distribution for the extraction of the 
                                               rearrangement length.
            visual (bool): True if the visualizaiton is active. False if not.
        """
        chr_id = np.random.choice(cell.DNA.IDs)
        ins_pos = np.random.randint(0, cell.DNA.CHRs[chr_id - 1].length) 
        max_ins_length = int((cell.DNA.CHRs[chr_id - 1].length - ins_pos))  
        ins_length = length_extraction_method(1, max_ins_length) if max_ins_length >= 2 else 1  
        Insertion(chr_id, ins_pos, ins_length, cell, visual=visual)

    def rand_deletion(self, cell :Cell, length_extraction_method, visual: bool):
        """
        It generates a random Deletion, according to a given distirbution. Then calls the function 
        that adds it to the events of the considered cell.

        Parameters
        ----------
            cell (Cell): considered cell.
            length_extraction_method (Method): probability distribution for the extraction of the 
                                               rearrangement length.
            visual (bool): True if the visualizaiton is active. False if not.
        """
        chr_id = np.random.choice(cell.DNA.IDs)

        if cell.DNA.CHRs[chr_id - 1].length <= 0: 
            print(f"Chromosome (ID:{chr_id}) length is {cell.DNA.CHRs[chr_id - 1].length}.")
            chr_list = list(range(1,len(cell.DNA.CHRs) + 1))
            chr_list.remove(chr_id)
            chr_id = np.random.choice(chr_list)
            print("ID new",chr_id)

        del_pos = np.random.randint(0, cell.DNA.CHRs[chr_id - 1].length) 
        max_del_length = int((cell.DNA.CHRs[chr_id - 1].length - del_pos)) 
        del_length = length_extraction_method(1, max_del_length) if max_del_length >= 2 else 1
        Deletion(chr_id, del_pos, del_length, cell, visual=visual)

    def rand_translocation(self, cell :Cell, length_extraction_method, visual :bool):
        """
        It generates a random Translocation, according to a given distirbution. Then calls the function 
        that adds it to the events of the considered cell.

        Parameters
        ----------
            cell (Cell): considered cell.
            length_extraction_method (Method): probability distribution for the extraction of the 
                                               rearrangement length.
            visual (bool): True if the visualizaiton is active. False if not.
        """ 
        chr_id = np.random.choice(cell.DNA.IDs)
        if cell.DNA.CHRs[chr_id - 1].length == 1: 
            print(f"(generation: {cell.generation}) Chromosome {chr_id} has only 1 base. Translocation has no meaning here.\n")
            return
        init_pos = np.random.randint(0, cell.DNA.CHRs[chr_id - 1].length) 
        max_transl_length = int((cell.DNA.CHRs[chr_id - 1].length - init_pos)) 
        transl_length = length_extraction_method(1, max_transl_length) if max_transl_length >= 2 else 1
        #print(f"ID: {chr_id}, init: {init_pos}, len: {transl_length}, chr_len: {cell.DNA.CHRs[chr_id - 1].length}")
        final_pos = np.random.randint(0, cell.DNA.CHRs[chr_id - 1].length - transl_length )
        Translocation(chr_id, init_pos, transl_length, final_pos, cell, visual=visual)

    def rand_reciprocal_translocation(self, cell :Cell, length_extraction_method, visual :bool):
        """
        It generates a random Reciprocal Translocation, according to a given distirbution. Then calls
        the function that adds it to the events of the considered cell.

        Parameters
        ----------
            cell (Cell): considered cell.
            length_extraction_method (Method): probability distribution for the extraction of the 
                                               rearrangement length.
            visual (bool): True if the visualizaiton is active. False if not.
        """
        chr_id1 = np.random.choice(cell.DNA.IDs)
        possible_chrs = list(copy.deepcopy(cell.DNA.IDs))
        possible_chrs.remove(chr_id1)
        chr_id2 = np.random.choice(possible_chrs)
        chr_ids = (chr_id1, chr_id2) 
        init_pos = np.random.randint(0, cell.DNA.CHRs[chr_ids[0] - 1].length) 
        max_transl_length = int((cell.DNA.CHRs[chr_ids[0] - 1].length - init_pos))  
        transl_length = length_extraction_method(1, max_transl_length) if max_transl_length >= 2 else 1
        final_pos = np.random.randint(0, cell.DNA.CHRs[chr_ids[1] - 1].length)
        ReciprocalTranslocation(chr_ids, init_pos, transl_length, final_pos, cell, visual=visual)

    def rand_duplication(self, cell :Cell, length_extraction_method, visual :bool):
        """
        It generates a random Duplication, according to a given distirbution. Then calls the function 
        that adds it to the events of the considered cell.

        Parameters
        ----------
            cell (Cell): considered cell.
            length_extraction_method (Method): probability distribution for the extraction of the 
                                               rearrangement length.
            visual (bool): True if the visualizaiton is active. False if not.
        """
        chr_id = np.random.choice(cell.DNA.IDs)
        init_pos = np.random.randint(0, cell.DNA.CHRs[chr_id - 1].length) 
        max_dupl_length = int((cell.DNA.CHRs[chr_id - 1].length - init_pos))  
        dupl_length = length_extraction_method(1, max_dupl_length) if max_dupl_length >= 2 else 1
        final_pos = np.random.randint(0, cell.DNA.CHRs[chr_id - 1].length)
        Duplication(chr_id, init_pos, dupl_length, final_pos, cell, visual=visual)
        
## RANDOM MUTATION METHODS ########################################################################

    def rand_point_insertion(self, cell: Cell, visual :bool):
        """
        It generates a random Pointwise Insertion, drawing its position from a Uniform distribution.
        Then calls the function that adds it to the events of the considered cell.

        Parameters
        ----------
            cell (Cell): considered cell.
            visual (bool): True if the visualizaiton is active. False if not.
        """
        chr_id = np.random.choice(cell.DNA.IDs)
        ins_pos = np.random.randint(0, cell.DNA.CHRs[chr_id - 1].length)  
        PointInsertion(chr_id, ins_pos, cell, visual=visual)

    def rand_point_deletion(self, cell :Cell, visual :bool):
        """
        It generates a random Pointwise Deletion, drawing its position from a Uniform distribution.
        Then calls the function that adds it to the events of the considered cell.

        Parameters
        ----------
            cell (Cell): considered cell.
            visual (bool): True if the visualizaiton is active. False if not.
        """
        chr_id = np.random.choice(cell.DNA.IDs)
        del_pos = np.random.randint(0, cell.DNA.CHRs[chr_id - 1].length) 
        PointDeletion(chr_id, del_pos, cell, visual=visual)

    def rand_point_replacement(self, cell :Cell, visual :bool):
        """
        It generates a random Pointwise Replacement, drawing its position from a Uniform distribution.
        Then calls the function that adds it to the events of the considered cell.

        Parameters
        ----------
            cell (Cell): considered cell.
            visual (bool): True if the visualizaiton is active. False if not.
        """
        chr_id = np.random.choice(cell.DNA.IDs)
        repl_pos = np.random.randint(0, cell.DNA.CHRs[chr_id - 1].length) 
        PointReplacement(chr_id, repl_pos, cell, visual=visual)

## CELL DUPLICATION AND GROWTH ########################################################################

    def random_choice(self, cell: Cell, cumulative_list, del_len_distrib, ins_len_distrib, \
        transl_len_distrib, rec_transl_len_distrib, dupl_len_distrib, visual :bool):
        """
        Given that an event happens, this funciton chooses which event happen accordinf to the
        cumulative probability given in 'cumulative_list'.

        Parameters
        ----------
            cell (Cell): considered cell.
            cumulative_list (list): list containing the cumulative probability of the possible 
                                    events.
            del_len_distrib (Method): probability distribution of the Deletion length.
            ins_len_distrib (Method): probability distribution of the Insertion length.
            transl_len_distrib (Method): probability distribution of the Translocation length.
            rec_transl_len_distrib (Method): probability distribution of the Reciprocal 
                                             Translocation length.
            dupl_len_distrib (Method): probability distribution of the Duplication length.
            visual (bool): True if the visualizaiton is active. False if not.
        """
        r = np.random.rand()
        if r < cumulative_list[0]:
            self.rand_deletion(cell, del_len_distrib, visual=visual)
        elif cumulative_list[0] <= r < cumulative_list[1]:
            self.rand_insertion(cell, ins_len_distrib, visual=visual)
        elif cumulative_list[1] <= r < cumulative_list[2]:
            self.rand_translocation(cell, transl_len_distrib, visual=visual)
        elif cumulative_list[2] <= r < cumulative_list[3]:
            self.rand_reciprocal_translocation(cell, rec_transl_len_distrib, visual=visual)
        elif cumulative_list[3] <= r < cumulative_list[4]:
            self.rand_duplication(cell, dupl_len_distrib, visual=visual)
        elif cumulative_list[4] <= r < cumulative_list[5]:
            self.rand_point_insertion(cell, visual=visual)
        elif cumulative_list[5] <= r < cumulative_list[6]:
            self.rand_point_deletion(cell, visual=visual)
        elif cumulative_list[6] <= r <= cumulative_list[7]:
            self.rand_point_replacement(cell, visual=visual)

    def node_duplication(self, node: Node, cumulative_list, ave_events_num, del_len_distrib, \
        ins_len_distrib, transl_len_distrib, rec_transl_len_distrib, dupl_len_distrib, \
            n_event_method, visual: bool):
        """
        Given the current 'node' and the distribution of the number of events in one duplication
        (n_ave_method), it creates two doughter nodes, and calls 'random_choice' to add the 
        extracted number of events to them.

        Parameters
        ----------
            node (Node): parent node that will be duplicated in this function.
            cumulative_list (list): list containing the cumulative probability of the possible 
                                    events.
            ave_events_num (int): average number of events of each cell duplication.
            del_len_distrib (Method): probability distribution of the Deletion length.
            ins_len_distrib (Method): probability distribution of the Insertion length.
            transl_len_distrib (Method): probability distribution of the Translocation length.
            rec_transl_len_distrib (Method): probability distribution of the Reciprocal 
                                             Translocation length.
            dupl_len_distrib (Method): probability distribution of the Duplication length.
            n_event_method (Method): probability distribution of the number of events in one cell
                                     duplication.
            visual (bool): True if the visualizaiton is active. False if not.

        Returns
        -------
            node.left (Cell): left doughter cell of the parent one, with the its list of events.
            node.right (Cell): right doughter cell of the parent one, with the its list of events.
        """
        new_generation = node.generation + 1
        new_left = MUT_Cell(copy.deepcopy(node.data.DNA), [], new_generation)
        new_right = MUT_Cell(copy.deepcopy(node.data.DNA), [], new_generation)

        if visual == True:
            for chr in node.data.DNA.CHRs:
                del(chr.visual)
            gc.collect()

        n_event_left, n_event_right = n_event_method(ave_events_num), n_event_method(ave_events_num)
        for i in range(n_event_left): self.random_choice(new_left, cumulative_list, \
            del_len_distrib, ins_len_distrib, transl_len_distrib, rec_transl_len_distrib, \
                dupl_len_distrib, visual=visual)
        for j in range(n_event_right): self.random_choice(new_right, cumulative_list, \
            del_len_distrib, ins_len_distrib, transl_len_distrib, rec_transl_len_distrib, \
                dupl_len_distrib, visual=visual)
        node.left = Node(new_left, new_generation)
        node.right = Node(new_right, new_generation)
        return node.left, node.right

    def growth(self, node :Node, n_generations :int, ave_events_num: int, cumulative_list: list,\
                n_event_method, del_len_distrib, ins_len_distrib, transl_len_distrib, \
                rec_transl_len_distrib, dupl_len_distrib, visual: bool):
        """
        Recurrent functions that starting with one Wild Type Cell (in a node) calls itself 
        duplicating every time each node, up to 'n_generations' generations. The result is a Binary
        Tree accessible from the parent node (WT Cell).
        It saves in an array all the leaves of the last generaitons and computes averages and 
        standard deviations on the chromosomes and genome lengths.

        Parameters
        ----------
            node (Node): parent node that will be duplicated in this function.
            n_generations (int): number of generations to be simulated. 
            ave_events_num (int): average number of events of each cell duplication. (default: 1)
            cumulative_list (list): list containing the cumulative probability of the possible 
                                    events.
            n_event_method (Method): probability distribution of the number of events in one cell
                                     duplication.
            del_len_distrib (Method): probability distribution of the Deletion length. 
            ins_len_distrib (Method): probability distribution of the Insertion length.
            transl_len_distrib (Method): probability distribution of the Translocation length.
            rec_transl_len_distrib (Method): probability distribution of the Reciprocal 
                                             Translocation length.
            dupl_len_distrib (Method): probability distribution of the Duplication length.
            visual (bool): True if the visualizaiton is active. False if not.
        """
        if node.generation >= n_generations: 
            self.update_average_genome_length(node)
            self.update_average_chromosome_length(node)
            self.leaves_collector(node.data)
            return
        else: 
            doughter1, doughter2 = self.node_duplication(node, cumulative_list, ave_events_num, \
                del_len_distrib, ins_len_distrib, transl_len_distrib, rec_transl_len_distrib, \
                    dupl_len_distrib, n_event_method, visual=visual)
            self.growth(doughter1, n_generations, ave_events_num, cumulative_list, n_event_method, \
                del_len_distrib, ins_len_distrib, transl_len_distrib, rec_transl_len_distrib, \
                    dupl_len_distrib, visual=visual)
            self.growth(doughter2, n_generations, ave_events_num, cumulative_list, n_event_method, \
                del_len_distrib, ins_len_distrib, transl_len_distrib, rec_transl_len_distrib, \
                    dupl_len_distrib, visual=visual)

## RECONSTRUCTION OF THE SEQUENCES GIVEN THE EVENTS ######################################################

    def WT_sequence_initializer(self, cell: WT_Cell, chromosome_table :list):
        """ 
        Given a WT cell, it fills each of the chromosomes of the WT_Cell.DNA.CHRs attribute with the
        corresponding sequence according to the 'chromosome_table' parameter.

        Parameters
        ----------
            cell (WT_Cell): Wild Type cell to be initialized with its DNA sequences.
            chromosome_table (list): list of tuple. Each tuple contains the chromosome ID and its
                                     sequence.
        """
        for ID,seq in chromosome_table:
            cell.DNA.CHRs[ID-1].sequence = seq

    def single_doughter_reconstructor(self, parent: Node, doughter: Node):
        """
        It copies the DNA sequences from the parent to the doughter cell. Then it modifies them 
        according to the new events present in the doughter cell.

        Parameters
        ----------
            parent (Node): parent cell from which the DNA sequences will be copied.
            doughter (Node): doughter cell in which the DNA sequences will be copied and modified.

        Methods
        -------
            check_chr_length(): cheks if the parent cell has the correct number of DNA bases.
        """
        def check_chr_length():
            """
            It checks if the parent cell has the correct number of DNA bases.

            Raises
            ------
                Exception
                    If the chromosome length does not corresponde to the effective length of the
                    sequences.
            """
            for chr in doughter.data.DNA.CHRs:
                if chr.length != len(chr.sequence): 
                    raise Exception(f"Chromosome lenght ({chr.length}) does not correspond to the length of sequences ({len(chr.sequence)})")

        doughter.copy_chr_sequences(parent)
        for event in doughter.data.events:
            event.reconstruct(doughter)
        check_chr_length()

    def reconstructor(self, parent: Node, n_generations: int, chromosome_table :list):
        """
        Recurrent functions that starting with 'parent' node (from which the all tree of new 
        generations is accessible) calls itself reconstructing every time both the doughters of the
        parent, up to 'n_generations' generations. In the end only the leaves of the 'n_generation' 
        generation will contain the modified sequences.

        Parameters
        ----------
            parent (Node): ancestor (WT) cell from which the recostruction will begin.
            n_generations (int): number of generations that we want to reconstruct.
            chromosome_table (list): list of tuple. Each tuple contains the chromosome ID and its
                                     sequence.
        """
        if n_generations < self.generations and parent.generation == 0: 
            print(f"The generations you want to reconstruct ({n_generations}) are less than the \
                    possible ones ({self.generations})")
        if parent.generation >= n_generations: return
        else:
            if type(parent.data) == WT_Cell: 
                self.WT_sequence_initializer(parent.data, chromosome_table)
            doughter1, doughter2 = parent.left, parent.right
            self.single_doughter_reconstructor(parent, doughter1)
            self.single_doughter_reconstructor(parent, doughter2)
        # CHECK ##################################
            for chr in parent.data.DNA.CHRs:
                del(chr.sequence)
            gc.collect()
        ##########################################
            self.reconstructor(doughter1, n_generations, chromosome_table)
            self.reconstructor(doughter2, n_generations, chromosome_table)

    def path_reconstructor(self, path: list, chromosome_table: list):
        """
        Given a path and the total number of simulated generations 'n_generations', this function 
        reconstructs the sequence of the leaf corresponding to the path.

        Parameters
        ----------
            path (list): list of 0 or 1. 0 corresponds to "left", 1 to "right".
            chromosome_table (list): list of tuple. Each tuple contains the chromosome ID and its
                                     sequence.

        Returns
        -------
            current_node (Node): leaf corresponding to the selected path.

        Raises
        ------
            Exception
                If the path's length is larger than the number of simulated generations.
        """
        if self.generations < len(path): 
            raise Exception(f"path's length ({len(path)}) larger than number of generations ({self.generations})")
        if self.generations > len(path): 
            print(f"path's length ({len(path)}) is shorter than number of generations ({self.generations})")
        current_node = self.parent
        if type(current_node.data) == WT_Cell: 
            self.WT_sequence_initializer(current_node.data, chromosome_table)
        for direction in path:
            if direction == 0: 
                self.single_doughter_reconstructor(current_node, current_node.left)
            # CHECK ##################################
                for chr in current_node.data.DNA.CHRs:
                    del(chr.sequence)
            ###########################################
                current_node = current_node.left
            elif direction == 1: 
                self.single_doughter_reconstructor(current_node, current_node.right)
            # CHECK ##################################
                for chr in current_node.data.DNA.CHRs:
                    del(chr.sequence)
                    gc.collect
            ###########################################
                current_node = current_node.right
        return current_node
            
## STATISTICS ####################################################################################

    def update_average_genome_length(self, node: Node):   
        """
        Updates the length of the whole genome in order to comute the average.

        Parameters
        ----------
            node (Node): node considered for the computation of the average.
        """
        for chr in node.data.DNA.CHRs:
                self.average_genome_length += chr.length

    def update_average_chromosome_length(self, node: Node):   
        """
        Updates the length of each chromosome in order to comute the average.

        Parameters
        ----------
            node (Node): node considered for the computation of the average.
        """
        for chr in node.data.DNA.CHRs:
                self.average_chromosome_length[chr.ID - 1] += chr.length

    def chromosome_std_dev(self, n_chr: int, n_gen: int):
        """
        Computes the Standard Deviation of the final length of each Chromosome.

        Parameters
        ----------
            n_chr (int): number of chromosomes.
            n_gen (int). number of generations.            
        """
        st_dev = np.zeros(n_chr)
        for cell in self.leaves:
            for chr in cell.DNA.CHRs:
                st_dev[chr.ID - 1] += (chr.length - self.average_chromosome_length[chr.ID - 1])**2
        return np.sqrt(st_dev / (2 ** n_gen))

## VISUALIZATION ####################################################################################

    def chromosome_visualizator(self, leaf_number):
        """
        Displays the chromosome of a selected leaf, highlighting locations where multiple 
        Rearrangements/Mutations have occurred.

        Parameters
        ----------
            leaf_number (int): number corresponding to the leaf of the simulation that we want to visualize.
        
        Raises
        -----
            Exception
                If the option 'visual' is set to 'False', the function cannot display the result.
        """
        if self.visual == False: raise Exception(f"The 'visual' option is set to 'False'.")
        Max = 0
        for chr in self.leaves[leaf_number].DNA.CHRs:
            max = np.amax(chr.visual)
            if max >= Max: Max = max
        scale_max_value = Max
        data = []
        fig, axs = plt.subplots(16, figsize = (20,9.9))
        fig.suptitle(f'Chromosomes of leaf n°{leaf_number} ({self.generations} generations)', fontname = 'Helvetica', fontsize = 24)
        for id in range(1,17):
            ax = axs[id-1]
            data.append([np.array(self.leaves[leaf_number].DNA.CHRs[id-1].visual)])
            im = ax.imshow(data[id-1], aspect = 100000*len(data[id-1]), cmap='Greys', vmin = 0, vmax = scale_max_value, \
                interpolation='nearest')
            ax.set_ylabel(f"CHR {id}", rotation=0, fontname = 'Helvetica', fontsize=15, labelpad=30)
            ax.xaxis.get_label()
            ax.axes.get_yaxis().set_ticks([])
            ax.axes.get_xaxis().set_ticks([])
        fig.subplots_adjust(bottom=0., top=0.9, left=0., right=1, wspace=10, hspace=0.2)
        cbar = fig.colorbar(im, ax=axs.ravel().tolist(),  shrink=1.0)
        cbar.set_ticks(np.arange(0, scale_max_value, 1))
        cbar.ax.tick_params(labelsize = 18)
        cbar.ax.set_ylabel('Number of superposed mutations', rotation=270, fontname = 'Helvetica', fontsize = 18,labelpad=30)
        plt.show()


    def __init__(self, chromosome_table, n_gen, ave_events_num = 1, \
                 cumulative_list = [1./7, 2./7, 3./7, 4./7, 5./7, 6./7, 1.], \
                 n_events_distrib = Utility.poisson_events_number, \
                 del_len_distrib = Utility.int_trunc_uniform, \
                 ins_len_distrib = Utility.int_trunc_uniform, 
                 transl_len_distrib = Utility.int_trunc_uniform, \
                 rec_transl_len_distrib = Utility.int_trunc_uniform, \
                 dupl_len_distrib = Utility.int_trunc_uniform, visual = False):
        """ 
        It initializes the Wild Type Cell,the Binary Tree, the number of generations, the average 
        genome and chromosome lengths and the array containing the leaves. Then simulates the cell 
        duplication up to "self.generation" generations, and computes the statistics.

        Parameters
        ----------
            chromosome_table (list): list of tuple. Each tuple contains the chromosome ID and its
                                     sequence.
            n_gen (int): number of generations.
            ave_events_num (int): average number of events of each cell duplication.
            cumulative_list (list): list containing the cumulative probability of the possible 
                                    events. (default: [1./7, 2./7, 3./7, 4./7, 5./7, 6./7, 1.]) 
            n_events_distrib (Method): probability distribution of the number of events in one cell
                                       duplication. (default: poisson_events_number)
            del_len_distrib (Method): probability distribution of the Deletion length. 
                                      (default: int_trunc_uniform)
            ins_len_distrib (Method): probability distribution of the Insertion length.
                                      (default: int_trunc_uniform)
            transl_len_distrib (Method): probability distribution of the Translocation length.
                                      (default: int_trunc_uniform)
            rec_transl_len_distrib (Method): probability distribution of the Reciprocal 
                                             Translocation length. (default: int_trunc_uniform)
            dupl_len_distrib (Method): probability distribution of the Duplication length.
                                      (default: int_trunc_uniform)
            visual (bool): True if the visualizaiton is active. False if not.
        """
        n_chr = len(chromosome_table)
        wt = WT_Cell(n_chr, chromosome_table, visual=visual)
        self.visual = visual
        self.parent = Node(wt)
        self.generations = n_gen
        self.average_genome_length, self.average_chromosome_length = 0, np.zeros(n_chr)
        self.leaves = []
        self.growth(self.parent, n_gen, ave_events_num, cumulative_list, n_events_distrib, \
                    del_len_distrib, ins_len_distrib, transl_len_distrib, rec_transl_len_distrib,\
                    dupl_len_distrib, visual=visual)
        self.average_genome_length /= 2 ** n_gen
        self.average_chromosome_length = self.average_chromosome_length / 2 ** n_gen 
        self.chr_length_st_dev = self.chromosome_std_dev(n_chr, n_gen)
        

