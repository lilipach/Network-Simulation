# Network-Simulation
This project uses networkX graphs to create a static network and allows the user to test Edge and Node sampling algorithms in a 
DOS attack simulation. The program allows the user to modify multiple variables such as the number of packets being sent, 
the number of normal users, the number of attackers and their package send rate. 

TO RUN:
$ Python Network_Simulation.py

Note: 
The projet only uses a static network. The Attack is always selected to be one of the "Ending Nodes" this is to be able to 
reconstruct a longer path and have a better visual of how the sampling algorithms work. Once all network simultions variables are
selected the project will display an image of the static network, the statistics of the seperate Traceback mechanism, and 
lastly the reconstructed network path leading from the victim node to the attacker node. 
