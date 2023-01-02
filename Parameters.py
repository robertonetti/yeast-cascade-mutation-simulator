from Utility import Utility
"""
Module containing all the input parameters of the 'Simulator' class.

Parameters
----------
number_of_generations (int): Number of generations to be simulated.
average_events_number (int): average number of events for each cell duplication.
cumulative_list (int): list containing the cumulative probability of the possible events.

n_events_distrib (Method): probability distribution of the number of events in one cell
                            duplication.
del_len_distrib (Method): probability distribution of the Deletion length. 
ins_len_distrib (Method): probability distribution of the Insertion length.
transl_len_distrib (Method): probability distribution of the Translocation length.
rec_transl_len_distrib (Method): probability distribution of the Reciprocal Translocation length.
dupl_len_distrib (Method): probability distribution of the Duplication length.

chromosome_lengths (list): list of contaning in order, the length of each chromosome.
chromosome_number (int): number of chromosomes.
chromosome_table (list): list of tuple. Each tuple contains the chromosome ID and its sequence.
"""
number_of_generations = 10
average_events_number = 3

#                  Delet.   Insert.   Transl.   Rec.Transl.   Dupl.   P.Ins.   P.Del.   P.Repl
cumulative_list = [ 1./8,    2./8,     3./8,       4./8,      5./8,    6./8,    7./8,     1.]
#cumulative_list = [    0,    1./3,        0,          0,         0,    2./3,      0,      1.]

n_events_distrib = Utility.poisson_events_number

del_len_distrib = Utility.int_trunc_exp
ins_len_distrib = Utility.int_trunc_exp
transl_len_distrib = Utility.int_trunc_exp
rec_transl_len_distrib = Utility.int_trunc_exp
dupl_len_distrib = Utility.int_trunc_exp

chromosome_lengths = [int(5e5), int(5e5), int(5e5), int(5e5), int(5e5),int(5e5), int(5e5), int(5e5),
                    int(5e5), int(5e5),int(5e5), int(5e5), int(5e5), int(5e5), int(5e5), int(5e5),
                    int(5e5), int(5e5)]         
#chromosome_lengths = [int(100), int(100), int(100), int(100), int(100), int(100), int(100), int(100),
                    #  int(100), int(100), int(100), int(100), int(100), int(100), int(100), int(100),
                    #  int(100), int(100), int(100), int(100), int(100), int(100), int(100), int(100)]
                    
chromosome_number = 16 
#chromosome_table = Utility.A_seq_initializer(chromosome_lengths)
chromosome_table = Utility.random_seq_initializer(chromosome_lengths)