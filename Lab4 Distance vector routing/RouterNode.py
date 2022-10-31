#!/usr/bin/env python
import GuiTextArea, RouterPacket, F
from typing import NamedTuple
from copy import deepcopy

class RouterNode():
    minimumcost = None
    distanceTable = None
    route = None
    myID = None
    myGUI = None
    sim = None
    costs = None
    

    # --------------------------------------------------
    def __init__(self, ID, sim, costs):
        self.myID = ID
        self.sim = sim
        self.myGUI = GuiTextArea.GuiTextArea("  Output window for Router #" + str(ID) + "  ")

        self.distanceTable = [[0 for i in range(self.sim.NUM_NODES)] for j in range(self.sim.NUM_NODES)]
        self.route = [0 for i in range(self.sim.NUM_NODES)]
        self.minimumcost = [0 for i in range(self.sim.NUM_NODES)]
        
        self.costs = deepcopy(costs)
        self.minimumcost = deepcopy(costs)

        for i in range (len(self.costs)) : 
            for j in range (len(self.costs)) : 
                if i == j : 
                    self.distanceTable[i][j] = 0
                elif i == self.myID :    
                    self.distanceTable[self.myID][j] = self.costs[j]  
                else :
                    self.distanceTable[i][j] = self.sim.INFINITY  
            if costs[i] < self.sim.INFINITY: 
                self.route[i] = i 
            else :
                self.route[i] = self.sim.INFINITY
        

        for node, cost in enumerate(costs):
            if cost != self.sim.INFINITY and node != self.myID:
                self.sendUpdate(RouterPacket.RouterPacket(self.myID, node, costs)) 

      # --------------------------------------------------
    def recvUpdate(self, pkt):
        self.myGUI.println(f"\nReceived packet - Source: {pkt.sourceid} Data: {pkt.mincost}")
        if self.distanceTable[pkt.sourceid] == pkt.mincost:
            return

      
        self.distanceTable[pkt.sourceid] = pkt.mincost   # Updating our distance table with data

        if self.bellman():
            self.sendpacket(self.distanceTable[self.myID])

    def sendUpdate(self, pkt):
        self.sim.toLayer2(pkt)

      # --------------------------------------------------
    def printDistanceTable(self):
        self.myGUI.println("\nCurrent table for " + str(self.myID) +
                           "  at time " + str(self.sim.getClocktime())+"\n")
        formating = "|============|"

        loop_costs = range (len(self.costs))
        loop_numnodes = range(self.sim.NUM_NODES)
                        
        self.myGUI.print("\n\n Our distance vector and routes:\n   dst |\t")
        for i in loop_costs:
            self.myGUI.print("\t" + str(i))
        self.myGUI.println("")

        for i in loop_numnodes:
            self.myGUI.print(formating)        
        self.myGUI.println("")

        self.myGUI.print(" cost  | \t")
        for i in loop_numnodes:
            self.myGUI.print("\t" + str(self.distanceTable[self.myID][i])) 
        self.myGUI.println("")
        
        self.myGUI.print(" route | \t")
        for i in loop_numnodes:
 
            self.myGUI.print("\t" + str(self.route[i])) 

      # --------------------------------------------------
    def updateLinkCost(self, dest, newcost):
        self.costs[dest] = newcost
        
        if self.bellman():
            if self.sim.POISONREVERSE:
                poison = deepcopy(self.distanceTable[self.myID]) #we copy the table
                poison[dest] = self.sim.INFINITY #we set the destination cost to infinity manually
                for neighbour in range(self.sim.NUM_NODES):# 
                    if neighbour != self.myID and neighbour != self.sim.INFINITY and neighbour != dest:
                        self.sendUpdate(RouterPacket.RouterPacket(self.myID, neighbour, poison))
            else:
                self.sendpacket(self.distanceTable[self.myID])

      # --------------------------------------------------
    def sendpacket(self, pkt):
        for target in range(len(self.costs)):
            if target != self.myID and target != self.sim.INFINITY:
                self.sendUpdate(RouterPacket.RouterPacket(self.myID,target, pkt)) 
     # --------------------------------------------------
    def bellman(self): #bellman algorithm sends back a bool
        n_Value = False
        for target in range(self.sim.NUM_NODES):
            if target != self.myID:
                routes = []
                for neighbour in range(self.sim.NUM_NODES):
                    if neighbour != self.myID:
                        # Calculate total distance from this node via neighbour node to target node
                        routes.append((self.costs[neighbour] + self.distanceTable[neighbour][target], neighbour))

             
                b_route = min(routes, key = lambda a: a[0])   # Find best route
                if b_route[0] <= self.costs[target]:
                    self.distanceTable[self.myID][target] = b_route[0]
                    self.route[target] = b_route[1]
                    n_Value = True
        return n_Value