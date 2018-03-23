**Comparison Module \
Argument parsing function\
Version 0.3\
23ʳᵈ March 2018\
Oisin Creaner**

**Outline**\
This function parses the arguments from the command line and returns the 
file names for the model data and the scope data

Several options are provided: Positional arguments, followed by optional
arguments followed by interactive entry of the argument values.

*future expansions to arguments will allow the user to specify modes of 
operation and the type of output generated*

**Dependencies**\
argparse

**Design Diagram**\
![Design Diagram](/images/comparison_module_parse_args_fig1_v1.PNG)


**Operations**
1.  Creates a mutually exclusive group for model filenames
    1.  adds the positional argument model_p to that group
    2.  adds the optional argument -m or --model to that group
2.  Creates a mutually exclusive group for scope filenames
    1.  adds the positional argument scope_p to that group
    2.  adds the optional argument -s or --scope to that group
3.  Retrieves the model file name
    1.  If the positional argument model_p was used, that is stored in a 
    variable called in_file_model
    2.  Otherwise, if the optional argument -m or --model was used, 
    that is stored in a variable called in_file_model
    3.  Otherwise, the user is prompted to enter the filename and
    that is stored in a variable called in_file_model
4.  Retrieves the scope file name
    1.  If the positional argument scope_p was used, that is stored in a 
    variable called in_file_scope
    2.  Otherwise, if the optional argument -s or --scope was used, 
    that is stored in a variable called in_file_scope
    3.  Otherwise, the user is prompted to enter the filename and
    that is stored in a variable called in_file_scope
5.  Returns in_file_model, in_file_scope

**Usage and arguments**\
usage: prototype_comparison_module_1d_0_1.py [-h] [--model MODEL]
                                             [--scope SCOPE]
                                             [model_p] [scope_p]

positional arguments:\
  model_p               The file containing the data from the model (Usually DreamBeam)\
  scope_p               The file containing the observed data from the telescope

optional arguments:\
  -h, --help            show this help message and exit\
  --model MODEL, -m MODEL Alternative way of specifying the file containing the
                        data from the model\
  --scope SCOPE, -s SCOPE
                        Alternative way of specifying the file containing the
                        observed data from the telescope
                        
**Sample Uses**\
prototype_comparison_module_1d_0_1.py model_file_name.csv scope_file_name.hdf5
prototype_comparison_module_1d_0_1.py -m model_file_name.csv -s scope_file_name.hdf5
prototype_comparison_module_1d_0_1.py --model model_file_name.csv --scope scope_file_name.hdf5
prototype_comparison_module_1d_0_1.py
