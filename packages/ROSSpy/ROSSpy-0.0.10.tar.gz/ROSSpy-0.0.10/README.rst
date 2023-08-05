ROSSpy
_______

-----------
Motivation
-----------

Desalination is an unavoidable technology for meeting the 6th SDG of clean freshwater for all people. Reverse Osmosis (RO) is the leading desalination technology, although, even greater energy efficiencies and economic practicalities are possible by mitigating membrane fouling, like mineral scaling. The geochemistry of mineral scaling is generally inaccessible to physical experimentation, thus a number of software -- like TOUGHREACT and French Creek -- to permit research into scaling phenomena. These software, however, are esoteric -- i.e. FORTRAN coding language and geochemical jargon -- and are computationally and financially expensive. We therefore developed a `Reverse Osmosis Scaling Software in Python (ROSSpy) <https://pypi.org/project/ROSSpy/>`_ as an open-source software -- which is predicated upon `PHREEQC <https://www.usgs.gov/software/phreeqc-version-3>`_ geochemical calculations -- that evaluates scaling and brine formation during the reactive transport of desalination. The code examples of the `ROSSpy GitHub <https://github.com/freiburgermsu/ROSSpy>`_ demonstrate the breadth and accuracy of ROSSpy for RO research applications. We encourage critiques and suggestions by the desalination or geochemical communities to support ROSSpy as integral component of the open-science that may expedite progress towards resolving water insecurities around the world.

++++++++++++++++
Installation
++++++++++++++++

ROSSpy is installed in a command prompt or terminal via the PyPI command::

 pip install rosspy

The package may need to specifically installed in the Anaconda Command Prompt to use the package in Anaconda environments like Jupyer Notebooks or Spyder.

-----------
Concept
-----------

The ROSSpy framework represents RO desalination as one-dimensional reactive transport. The feed solution can be bifurcated into the concentration polarization (CP) that is adjacent to the filtration membrane and the bulk solution bvia the dual porosity model, although, accurate results were observed without applying the dual porosity model. The inlet boundary is defined by the Dirichlet condition -- which assumes that the feed is an infinite reservoir which is unchanged by the reactive transport of the RO module -- while the outlet boundary is defined by the Cachy condition -- which assumes that the effluent concentrations are dynamically susceptible to the reactive transport of the RO module. 


----------------------
Functions
----------------------

ROSSpy essentially translates user specifications of an RO system into PHREEQ parameters that are executed via `PHREEQpy <https://pypi.org/project/phreeqpy/>`_. The translation of the specifications are organized into the following Python functions of a single class object ``ROSSPkg``, whose underlying calculations and logic are detailed in the ROSSpy manuscript. 


+++++++++++
__init__
+++++++++++

The __init__ of the ``ROSSPkg`` object defines the simulation environment::

 import rosspy
 ross = rosspy.ROSSPkg(operating_system = 'windows', verbose = False, jupyter = False)

- *operating_system* ``str``: specifies whether the user is using a "windows" or "unix" system, which directs subtle differences in importing the PHREEQpy package and incorporating comments to the PQI PHREEQ input files.
- *verbose* ``bool``: specifies whether intermediary details and parameters will be printed 
- *jupyter* ``bool``: specifies whether the simulation is being conducted in a Jupyter Notebook, which uses ``display`` instead of ``print`` for tables and figures.


++++++++++++++++
define_general
++++++++++++++++

The ``define_general`` function defines general conditions of the simulation::

 ross.define_general(database_selection, simulation = 'scaling', domain = 'single', 
 domain_phase = None, quantity_of_modules = 1, simulation_type = 'transport', simulation_title = None)

- *database_selection* ``str``: specifies which PHREEQ database file -- "Amm", "ColdChem", "core10", "frezchem", "iso", "llnl", "minteq", "minteq.v4", "phreeqc", "pitzer", "sit", "Tipping_Hurley", or "wateq4f" -- will be executed.
- *simulation* ``str``: specifies whether "scaling" or "brine" will be evaluated.
- *domain* ``str``: specifies whether the "single" or "dual" domain models will be simulated.
- *domain_phase* ``str``: specifies whether the "mobile" -- i.e. bulk solution -- or the "immobile" -- i.e. the CP solution layer -- will be evaluated for dual domain simulations.
- *quantity_of_modules* ``int``: specifies the number of RO modules that will be simulated.
- *simulation_type* ``str``: specifies whether the geochemistry of reactive transport "transport" or "evaporation" upon the feed solution will be evaluated.
- *simulation_title* ``str``: specifies the title of the simulation.


+++++++++++
transport
+++++++++++

The ``transport`` function defines spatiotemporal conditions for reactive transport simulations in the TRANSPORT block of PHREEQ code::

 ross.transport(simulation_time, simulation_perspective = None, 
 module_characteristics = {}, cells_per_module = 12, parameterized_timestep = None, 
 kinematic_flow_velocity = None, exchange_factor = 1e10)

- *simulation_time* ``float``: specifies the total simulated time in seconds.
- *simulation_perspective* ``str``: specifies whether "all_time" or "all_distance" is evaluated in the simulation, where "None" allows the software to select the default perspectives of "all_distance" or "all_time" for the "scaling" and "brine" simulations, respectively.
- *module_characteristics* ``dict``: specifies custom conditions of the RO module, where any unprovided parameters -- including possibly all of the parameters -- will derive from the DOW FILMTEC BW30-400 RO module. The expected ``keys`` of the dictionary are 

 + 'module_diameter_mm'
 + 'permeate_tube_diameter_mm'
 + 'module_length_m'
 + 'permeate_flow_m3_per_day' 
 + 'max_feed_flow_m3_per_hour'
 + 'membrane_thickness_mm' 
 + 'feed_thickness_mm'
 + 'active_m2'
 + 'permeate_thickness_mm'
 + 'polysulfonic_layer_thickness_mm'
 + 'support_layer_thickness_mm'. 

The ``values`` for the dictionary are all floats in the units of the corresponding key.
 
- *cells_per_module* ``int``: specifies the quantity of cells into which the parameterized RO module is discretized through the simulation.
- *parameterized_timestep* ``float``: specifies the timestep length of the simulation in seconds, where "None" assigns the default maximum that adheres to the Courant Condition.
- *kinematic_flow_velocity* ``float``: specifies the kinetic flow velocity for the feed solution, where "None" assigns the default of 9.33E-7 (m^2/sec).
- *exchange_factor* ``float``: specifies the kinetic rate of exchange between the mobile and immobile phases of a dual domain simulation, which is described in units of (1/sec).


+++++++++++
reaction
+++++++++++

The ``reaction`` function calculates and parameterizes the permeate flux gradient in reactive transport simulations, or the rate of evaporation in evaporation simulations, in the REACTION blocks of PHREEQ code::

 ross.reaction(permeate_approach = 'linear_permeate', permeate_efficiency = 1, 
 head_loss = 0.89, final_cf = 2)

- *permeate_approach* ``str``: specifies either the "linear_permeate" or "linear_cf" the gradients of permeate flux in reactive transport simulations.
- *permeate_efficiency* ``float``: specifies 0<=PE<=1 proportion of calculated permeate flux that actually filters from the feed solution.
- *head_loss* ``float``: specifies the 0<=PE<=1 proportion of effluent pressure relative to the influent.
- *final_cf* ``float``: specifies the final CF of the effluent for the linear_cf gradient of permeate flux in reactive transport simulations. The default value of 0.89 -- an 11% pressure drop -- is sourced from “Reverse osmosis desalination: Modeling and experiment” by Fraidenraich et al., 2009.


+++++++++++
solutions
+++++++++++

The ``solutions`` function parameterizes the feed solution geochemistry and corresponding references into the SOLUTION block of PHREEQ code, either from a predefined water body or from a customized geochemical feed source. The elements that are not accepted by each database automatically rejected by ROSSpy to avoid PHREEQ errors in the computation::

 ross.solutions(water_selection = '', water_characteristics = {}, 
 solution_description = '', parameterized_alkalinity = False, parameterized_ph_charge = True)

- *water_selection* ``str``: specifies which feed water -- either natural waters of the "red_sea" or the "mediterranean_sea", or produced waters from fracking oil wells of the "bakken_formation", "marcellus_appalachian_basin", "michigan_basin", "north_german_basin", "palo_duro_basin", or "western_pennsylvania_basin" -- or a "custom" feed water.
- *water_characteristics* ``dict``: specifies the feed geochemistry, when the *water_selection* argument is "custom". The expected ``keys`` of the dictionary are 

 + 'elements'
 + 'temperature'
 + 'pe'
 + 'Alkalinity' 
 + 'pH'
 
The ``value`` of each of these keys is itself a dictionary, with the keys of "value" and "reference" that correspond to the value of the respective geochemical condition and the literature reference for that value. The "elements" key, however, deviates slightly from this model, where its value is a dictionary that is further nested with key:alue pairs of each element and a dictionary of their "'concentration (ppm)" and "reference". An example of this structure is provided below.

{
    "element": {
        "Mn": {
            "concentration (ppm)": 3000,
            "reference": "Haluszczak, Rose, and Kump, 2013 [estimated from another Marcellus publication]"
			
        }, 

        "Li": {
            "concentration (ppm)": 95,
            "reference": "Haluszczak, Rose, and Kump, 2013 [reported average from another Marcellus publication]"
			
        }
		
    },

    "temperature": {
        "value": 24,
        "reference": "Dresel and Rose, 2010"
		
    }
	
}

- *solution_description* ``str``: describes a customized solution in a brief description, without spaces, which will be incorporated into the default naming scheme of the simulation.
- *parameterized_alkalinity* ``bool``: specifies whether the feed alkalinity will be parameterized, which is consequential since the alkalinity parameter is exclusive with balancing the charge of the solution.
- *parameterized_ph_charge* ``bool``: specifies whether the pH will be charged balance, which exclusive with parameterizing the alkalinity of the feed solution.



+++++++++++++++++++++
equilibrium_phases
+++++++++++++++++++++

The ``equilibrium_phases`` function parameterizes the EQUILIBRIUM_PHASES block of PHREEQ code with the minerals, and the pre-existing geochemical equilibria, that will be explored in scaling. The set of minerals that can precipitate from the parameterized ions is parameterized automatically into the simulation, however, may customize this set of analyzed minerals::

 ross.equilibrium_phases(block_comment = '', ignored_minerals = [], 
 existing_parameters = {})

- *block_comment* ``str``: describes any important details about the minerals or scaling phenomena of the simulation.
- *ignored_minerals* ``list``: describes the minerals that will not be explored in the simulation, regardless of whether they can potentially be precipitated from the geochemical profile of the feed.
- *existing_parameters* ``dict``: specifies pre-existing geochemical conditions in the system that may influence the geochemical predictions. The expected ``keys`` of the dictionary are the mineral names that pre-exist in the module, where the respective ``value`` is a dictionary with the keys of 

 + 'saturation'
 + 'initial_moles'
 
that correspond to the saturation index and the initial moles of the respective mineral in the solution at the start of the simulation.



++++++++++++++++
selected_output
++++++++++++++++

The ``selected_output`` function defines the content that will be incorporated to the output file of the simulation::

 ross.selected_output(output_filename = None)

- *output_filename* ``str``: specifies the name of an output file of the simulation that will be created whenever the developed input file is executed in a native PHREEQC environment, like IPHREEQC or the PHREEQC batch software that is the premise of iROSSpy.



+++++++++++
export
+++++++++++

The ``export`` function prepares and exports simulation content -- simulation parameters, raw and processed data, figures, and the input file -- into a discretely labeled that is designated for the simulation experiment::

 ross.export(simulation_name = None, input_path = None, output_path = None, 
 external_file = False)

- *simulation_name* ``str``: specifies the name simulation folder to which all of the ismulation files will be exported, where "None" assigns a default name for the simulation that incorporates details of the simulation with the scheme ``date-ROSSpy-water_selection-simulation_type-database_selection-simulation-simulation_perspective-#``. 
- *input_path* ``str``: specifies the directory path to where the input file will be saved, where "None' saves the input file as "input.pqi" to the designated folder with the other simulation files. 
- *output_path* ``str``: specifies the directory path to where the input file will be saved, where "None' saves the input file as "selected_output.pqo" to the designated folder with the other simulation files. 
- *external_file* ``str``: specifies whether the simulation executes a PHREEQ file that was developed beyond ROSSpy.



++++++++++++++++
parse_input
++++++++++++++++

The ``parse_input`` function parses, interprets, and exports a provided input file that was developed beyond ROSSpy::

 ross.parse_input(input_file_path, simulation, water_selection = None, 
 simulation_name = None, active_feed_area = None)

- *input_file_path* ``str``: specifies the path of the input file. 
- *simulation* ``str``: defines the simulation as either evaluating "scaling" or "brine". 
- *water_selection* ``str``: specifies the name of the water body that is described in the SOLUTION block of the developed input PQI file. 
- *simulation_name* ``str``: specifies the name simulation folder to which all of the ismulation files will be exported, where "None" assigns a default name for the simulation that incorporates details of the simulation with the scheme ``date-ROSSpy-water_selection-simulation_type-database_selection-simulation-simulation_perspective-#``. 
- *active_feed_area* ``float``: specifies the active filtration area of the simulated RO module, where "None" assigns the 37 (m^2) from the default FILMTEC BW30-400 module. 



+++++++++++
execute
+++++++++++

The ``execute`` function executes the developed or imported input file through PHREEQpy in ROSSpy or the batch PHREEQC software in iROSSpy::

 ross.execute(simulated_to_real_time = 9.29)

- *simulated_to_real_time* ``float``: specifies the ratio of simulated time to real computational time when executing ROSSpy simulations. The 9.29 ratio was identified for extended simulations of multiple days or weeks, however, shorter simulations on the order of minutes/hours may have a higher ratio.

The raw simulation data is returned by this function as a ``pandas.DataFrame`` object, which can be manipulated by the user for custom effects beyond the operations of ROSSpy.



++++++++++++++++++++++++++
process_selected_output
++++++++++++++++++++++++++

The ``process_selected_output`` function processes the output data from the simulation into figures and corresponding datatables::

 ross.process_selected_output(selected_output_path = None, plot_title = None, 
 title_font = 'xx-large', label_font = 'x-large', x_label_number = 6, 
 export_name = None, export_format = 'svg', individual_plots = None)

- *selected_output_path* ``str``: specifies the path of a simulation output file that can be processed independently of developing or importing the corresponding input file to ROSSpy object, where "None" necessitates that an input file was executed in the ROSSpy object.
- *plot_title* ``str``: specifies the title of the figure from the simulation data, where "None" defaults to titles that are customized for either "scaling" or "brine" simulations and contain parameter details of the simulated water body and the total simulation time.
- *title_font* & *label_font* ``str``: these specify the fonts of the title and labels of the simulation figure in terms of MatPlotLib font identifications of 'xx-small','x-small','small', 'medium', 'large', 'x-large', or 'xx-large'. 
- *x_label_number* ``int``: specifies the total quantity of labels that are assigned to the x-axis of the simulation figure.
- *export_name* ``str``: specifies the export name of the simulation figure, which defaults to 'brine' for "brine" simulations, or 'all_minerals' or an individual mineral name for "scaling" simulations, depending upon the value of the *individual_plots* argument.
- *export_format* ``str``: specifies the format of the exported simulation figure, from the MatPlotLib options of 'svg', 'pdf', 'png', 'jpeg', 'jpg', or 'eps'.
- *individual_plots* ``bool``: specifies whether each mineral of "scaling" simulations are plotted individually or combined in a single figure, where "None" allows the default of "True" for the "all_time" *simulation_perspective* or "False" otherwise.

The processed simulation data that is the basis of the generated figures is returned by this function as a ``pandas.DataFrame`` object, which can be manipulated by the user for other purposes beyond ROSSpy.


----------------------
Execution
----------------------

ROSSpy is executed through a deliberate sequence of the aforementioned functions::
 
 import rosspy
 ross = rosspy.ROSSPkg()
 ross.define_general(database_selection, simulation)
 ross.transport(simulation_time, simulation_perspective, )
 ross.reaction(permeate_approach, final_cf)
 ross.solutions(water_selection, custom_water_parameters, solution_description)
 ross.equilibrium_phases()
 ross.selected_output()
 ross.export()
 raw_data = ross.execute()
 processed_data = ross.process_selected_output()

ROSSpy can be tested via a simple sequence with the ``test`` function::

 pip install rosspy
 ross = rosspy.ROSSPkg(operating_system = 'windows', verbose = False, jupyter = False)
 ross.test()

This is execute a predefined simulation with simple parameters, which should emulate the same exported files and processes of a cusotmized simulation experiment.