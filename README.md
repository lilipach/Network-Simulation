# Network-Simulation
This project uses networkX graphs to create a static network and allows the user to test Edge and Node sampling algorithms in a 
DOS attack simulation. The programs allows the user to modify multiple variables such as the number of packets being sent, 
the number of normal users, the number of attackers and their package send rate. 

TO RUN:
$ Python Network_Simulation.py

Note: 
The projet only uses a static network. The Attacke is always selected to be one of the "Ending Nodes" this is to be able to 
reconstruct a longer path and have a better visual of how the sampling algorithms work. Once all network simultions variables are
selected the project will display an image of the static network, the statistics of the seperate Traceback mechanism, and the 
lastly the reconstructed network pacht leating from the victime node to the attacker node. 
