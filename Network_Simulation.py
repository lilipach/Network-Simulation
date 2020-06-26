import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import string
import random

NUMBER_OF_ROUTERS = 20
DEPTH = 15
VICTIM_NODE = 1
ATTACKER_NODES = [16, 17, 18, 19, 20]
CUSTOM_EDGES = [(1,2), (2,3), (2,4), (2,5), (3,8), (4,7), (5,6), (6,11),
                (7,10), (8,9), (9,15), (10,13), (10,14), (11,12), (12,20),
                (13,19), (13,18), (14,17), (15,16)]
'''
    Name: fillNetworkNodes
    Parameters: integer value -- numNodes,
                networkx graph -- network
    Description: This function will fill a graph with the number of specified
                 nodes.
'''
def fillNetworkNodes(numNodes, network):
    if numNodes < 0:
        print("Error: Cannot fill negative number of Nodes")
    else:
        for x in range(1, numNodes + 1):
            network.add_node(x)

'''
    Name: sendPackets
    Parameters: network -- graph data stucture for the specified network
                numNormalusers -- number of normal users to be simulated. Normal
                                  users will send only the number of packets
                                  specified
                numAttackers -- number of attackers to be simulated. for this
                                specific network only 5 attackers maybe simulated
                                attackers will send the number of specified packets
                                times the specified attackerPacketRate

                numPackets -- the number of packets each normal user will send.
                              Also signifies the base number of packets to be
                              sent by the attacker.
                attackerPacketRate -- this value is multiplied to numPackets to
                              calculate the number of packets an attacker will
                              send.
    Description: This function will create a list of paths. This list of paths are the
                 simulated packets being sent within the specified network.
'''
def sendPackets(network, numNormalUsers, numAttackers, numPackets, attackerPacketRate):
    print("Packets are being sent with the following information:")
    print("Number of Normal Users: " + str(numNormalUsers))
    print("Number of packets bing sent by a singular User : " + str(numPackets))
    print("Number of Attackers: " + str(numAttackers))
    print("Number of Packets being sent by a singular Attacker: " + str(numPackets*attackerPacketRate) + "\n")

    if(numAttackers > 5):
        print("Invalid number of attackers for the given network. Messages canceled.")
        return
    attackers = ATTACKER_NODES[:numAttackers]
    packetsSent = list()
    for router in range(2, numNormalUsers + 2):
        for message in range(0, numPackets):
            receiver = random.randrange(1, network.number_of_nodes() + 1)
            while (receiver == router):
                    receiver = random.randrange(1, network.number_of_nodes() + 1)
            packetsSent.append(sendMessage(network, router, receiver))

    for attacker in attackers:
        for message in range(0, numPackets * attackerPacketRate):
            packetsSent.append(sendMessage(network, attacker, VICTIM_NODE))
    return packetsSent

'''
    Name: sendMessage
    Parameters: network -- graph data stucture for the specified network
                sender -- integer value dictating the router sending a Message
                receiver -- integer value dictating the receiving router of the message
    Description: This function will find a path within the specified network/graph
                 between the sender and receiver routers and return the path.
'''
def sendMessage(network, sender, receiver):
    possiblePaths = nx.all_simple_paths(network, source = sender, target = receiver)
    selectedPath = random.choice(list(possiblePaths))
    print("\nPacket sent from router " + str(sender) + " to router " + str(receiver))
    print("Path Used: ")
    print(selectedPath)
    return selectedPath


def nodeSampling(paths, markingProb):
    print("Taking Node Samples...")
    packetMarkings = list()
    for path in paths:
        marks = list()
        for router in path:
            probability =  random.randrange(0, 100)
            if probability < (markingProb*100):
                marks.append(router)
        packetMarkings.append(marks)
    return packetMarkings

def sortNodeSamples(samples, numRouters):
    print("Processing Node Samples for traceback.")
    nodeTable = [[0 for i in range(numRouters + 1)] for j in range(2)]
    for router in range(0, numRouters + 1):
        nodeTable[0][router] = router

    for marks in samples:
        for router in marks:
            nodeTable[1][router] = nodeTable[1][router] + 1

    return nodeTable

def edgeSampling(paths, markingProb):
    print("Taking Edge Samples...")
    packetMarkings = list()
    for path in paths:
        marks = [0,0,-1]
        for router in path:
            probability =  random.randrange(0, 100)
            if probability < (markingProb*100):
                marks[0] = router
                marks[2] = 0
            else:
                if (marks[2] == 0):
                    marks[1] = router
                if (marks[2] != -1):
                    marks[2] = marks[2] + 1
        packetMarkings.append(marks)
    return packetMarkings

def drawEdgeSamples(samples, numRouters):
    print("Processing Edge Samples for traceback.")
    sampleGraph = nx.Graph()
    ### add root to graph
    sampleGraph.add_node(VICTIM_NODE)
    for sample in samples:
        if  sample[2] != -1 and sample[2] != 0:
            if sample[0] not in sampleGraph:
                sampleGraph.add_node(sample[0])
            if sample[1] not in sampleGraph:
                sampleGraph.add_node(sample[1])
            sampleGraph.add_edge(sample[0], sample[1], weight = sample[2])
    return sampleGraph

def sortEdgeSamples(samples, numRouters):
    networkEdges = []
    edgesTally = []
    for sample in samples:
        if  sample[2] != -1 and sample[2] != 0:
            edge = "{" + str(sample[0]) + "," + str(sample[1]) + "}"

            if edge not in networkEdges:
                networkEdges.append(edge)
                edgesTally.append(1)
            else:
                index = networkEdges.index(edge)
                edgesTally[index] = edgesTally[index] + 1

    #Display Node Sampling Result
    x = np.arange(len(networkEdges))
    y = edgesTally
    plt.bar(x, y, align = 'center', alpha = 0.5)
    plt.xticks(x, networkEdges)
    plt.ylabel("Number of Times Sampled")
    plt.xlabel("Edge Sample")
    plt.title("Edge Sample Results")
    plt.savefig("Edge_sampling_results.png")
    plt.show()
    plt.clf()



'''
    Run Network Simulation
'''
random.seed(123)

#Create static Network
network = nx.Graph()
fillNetworkNodes(NUMBER_OF_ROUTERS, network)
network.add_edges_from(CUSTOM_EDGES)

check = "Y"
while  check == "Y" or check == "YES":
    check = input("continue with simulations? (Y/N): ")
    check = check.upper()
    if (check == "Y" or check == "YES") != True :
        break

    numNormalUsers = int(input("Input the number of Normal Users: "))
    numAttackers = int(input("Input the number of Attackers: "))
    numPackets = int(input("Input the number of Packets: "))
    attackerPacketRate = int(input("Input the attacker Packet Rate: "))
    probability = float(input("Input sampling probability: "))
    simNode = input("Simulate Node Sampling? (Y/N): ")
    simEdge = input("Simulate Edge Sampling? (Y/N): ")
    showNet = input("View static Network? (Y/N)")

    if showNet == "Y" or showNet == "y":
        #Draw static Network
        nx.draw_circular(network, seed = 123, with_labels = True)
        plt.savefig("network.png")
        plt.show()
        plt.clf()

    if simNode == "Y" or simNode == "y":
        #Send Packets for Node Sampling
        nodePackets = sendPackets(network, numNormalUsers, numAttackers, numPackets, attackerPacketRate)
        nodeSamples = nodeSampling(nodePackets, probability)
        nodeResults = sortNodeSamples(nodeSamples, network.number_of_nodes())

        #Display Node Sampling Result
        x = np.arange(len(nodeResults[0]))
        y = nodeResults[1]
        plt.bar(x, y, align = 'center', alpha = 0.5)
        plt.xticks(x, nodeResults[0])
        plt.ylabel("Number of Times Sampled")
        plt.xlabel("Router Number")
        plt.title("Node Sample Results")
        plt.savefig("node_sampling_results.png")
        plt.show()
        plt.clf()

    if simEdge == "Y" or simEdge == "y":
        #send Packets for Edge Sampling
        edgePackets = sendPackets(network, numNormalUsers, numAttackers, numPackets, attackerPacketRate)
        edgeSamples = edgeSampling(edgePackets, probability)
        edgeGraph = drawEdgeSamples(edgeSamples, network.number_of_nodes())
        sortEdgeSamples(edgeSamples, network.number_of_nodes())

        #Display Edge Sampling Results
        nx.draw_circular(edgeGraph, seed = 123, with_labels = True)
        plt.savefig("edge_sampling_graph.png")
        plt.show()
        plt.clf()
