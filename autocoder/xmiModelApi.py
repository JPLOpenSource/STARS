#!/usr/bin/env python
# -----------------------------------------------------------------------
# xmiModelApi.py
#
# 
# -----------------------------------------------------------------------
# mypy: ignore-errors

from lxml import etree
from anytree import Node, RenderTree
import anytree
import sys
from copy import deepcopy
import argparse


class xmiModel:
    package = ''
    stateMachine = ''
    tree = Node('xmiModel')
    psuedoStateList = []
    idMap = {}
    transTargets = set()

    def __init__(self, packageName, stateMachineName):
        self.tree.package = packageName
        self.tree.stateMachine = stateMachineName

    def addState(self, name, parent, entry, exit, id):
        thisNode = Node("STATE", stateName = name, parent=parent, entry=entry, exit=exit, id=id)
        self.idMap[id] = thisNode
        return thisNode

    def addTransition(self, source, target, event, guard, action, kind, parent=tree):
        thisNode=Node("TRANSITION", 
                      source=source, 
                      target=target, 
                      event=event, 
                      guard=guard, 
                      action=action, 
                      kind=kind, 
                      parent=parent)
        
        self.transTargets.add(target)
        return thisNode
    
    def moveTransition(self, transition, state):
        thisNode=Node("TRANSITION", 
                      source=transition.source, 
                      target=transition.target, 
                      event=transition.event, 
                      guard=transition.guard, 
                      action=transition.action, 
                      kind=transition.kind, 
                      parent=state)
        transition.parent = None
        return thisNode

    def addPsuedostate(self, id, parent=tree):
        thisNode = Node("PSUEDOSTATE", id = id, parent = parent, stateName = "J"+str(id))
        self.idMap[id] = thisNode
        self.psuedoStateList.append(id)
        return thisNode
    
    def addInitial(self, transition):
        parent = transition.parent
        thisNode = Node("INITIAL", 
                        target = transition.target, 
                        action = transition.action,
                        parent = parent)
        
        # Remove the transition
        transition.parent = None

        # Remove the psuedo state
        self.idMap[transition.source].parent = None
        del self.idMap[transition.source]

        return thisNode
        

    def addJunction(self, transList, psuedoState):
        psId = psuedoState.id
        parent = psuedoState.parent

        # Assign ifNode and elseNode based on the presence of a guard
        ifNode, elseNode = (transList[0], transList[1]) if transList[0].guard else (transList[1], transList[0])

        assert ifNode.guard is not None
        assert elseNode.guard is None

        stateName = "J" + str(psId)
        thisNode = Node("JUNCTION", 
                        id = psId, 
                        stateName = stateName,
                        guard = ifNode.guard, 
                        ifTarget = ifNode.target,
                        ifAction = ifNode.action,
                        elseTarget = elseNode.target,
                        elseAction = elseNode.action, 
                        parent = parent)
        
        self.idMap[psId] = thisNode

        # Remove the psuedoState
        psuedoState.parent = None

        # Remove the transitions
        transList[0].parent = None
        transList[1].parent = None


        return thisNode


    def getRoot(self):
        return self.tree
    
    def getPackageName(self):
        return self.tree.package

    def getStateMachineName(self):
        return self.tree.stateMachine

    def getPackageAndStatMachineNames(self):
        return (self.tree.package, self.tree.stateMachine)

    # --------------------------------------------------------
    # getTransitionsList
    #
    # Return a list of transitions source and targets
    # --------------------------------------------------------
    def getTransitionsList(self, treeNode = tree):

        class Transition:
                source = 0
                target = 0
                guard = None
                action = None
                
                def __init__(self, source, target, guard, action):
                    self.source = source
                    self.target = target
                    self.guard = guard
                    self.action = action

        thisList = []
        for node in treeNode.children:
            if node.name == "TRANSITION":
                thisList.append(Transition(node.source, node.target, node.guard, node.action))
            thisList = thisList + self.getTransitionsList(node)

        return thisList

    # --------------------------------------------------------
    # getPsuedoStateList
    #
    # Return a list of psuedo state ID's in the tree
    # --------------------------------------------------------
    def getPsuedoStateList(self, treeNode = tree):
        thisList = []

        for node in treeNode.children:
            if node.name == "PSUEDOSTATE":
                thisList.append(node.id)
            thisList = thisList + self.getPsuedoStateList(node)

        return thisList
    
    # --------------------------------------------------------
    # getStates
    #
    # Return a list of state ID's in the tree
    # --------------------------------------------------------
    def getStatesList(self, treeNode = tree):
        thisList = []

        for node in treeNode.children:
            if node.name == "STATE":
                thisList.append(node.id)
            thisList = thisList + self.getStatesList(node)

        return thisList

   # --------------------------------------------------------
    # print
    #
    # Print the model as a tree
    # --------------------------------------------------------
    def print(self):
        print("---------------- xmi Model ------------")
        print(RenderTree(self.tree))
        print("------------------end------------------")


