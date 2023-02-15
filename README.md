# Aerosol-Simulation
Repository to run simulation for aerosol based model

To run this code to obtain results from paper, start with Animate_Simulation_Bus.py, use any of the Sim_Var methods for desired outputs. Changing values in the Simulate method is how you will change values for the Sim_Var methods. 

 
All values related to agents can be found in AvgAgentBackground.py, this includes vectors of transmission


The way virions move can be found in Environment.py, this includes how virions are spread through the vectors of transmission (how far, how often, etc.) 


The actual method that is called upon each frame to create the overall model can be found in Animate_2.py


