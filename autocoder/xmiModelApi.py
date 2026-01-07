#!/usr/bin/env python
# -----------------------------------------------------------------------
# xmiModelApi.py
#
# 
# -----------------------------------------------------------------------
# mypy: ignore-errors

from lxml import etree
from anytree import Node, RenderTree, PreOrderIter
import anytree
import sys
from copy import deepcopy
import argparse


class XmiModel:
    package = ''
    stateMachine = ''
    tree = Node('xmiModel')
    psuedoStateList = []
    idMap = {}
    transTargets = set()

    def __init__(self, packageName: str, stateMachineName:str):
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
    
    # -----------------------------------------------------------------------
    # getInitTranstions
    #
    # Update the xmi model to add Initial Transitions from Transitions
    # -----------------------------------------------------------------------  
    def getInitTransitions(self):
        for trans in PreOrderIter(self.tree):
            if trans.name == "TRANSITION":
                # If the transition source is a psuedostate and no other transition goes into that psuedostate
                if (trans.source in self.psuedoStateList) and (trans.source not in self.transTargets):
                    self.addInitial(trans)
    
    # -----------------------------------------------------------------------
    # getJunctions
    #
    # Update the xmi model to add Junctions
    # -----------------------------------------------------------------------  
    def getJunctions(self):
        for ps in PreOrderIter(self.tree):
            if ps.name == "PSUEDOSTATE":
                psId = ps.id
                transList = []
                for child in PreOrderIter(self.tree):
                    # Get the transitions that exit this psuedo state
                    if child.name == "TRANSITION":
                        if psId == child.source:
                            transList.append(child)
                if len(transList) == 2:
                    self.addJunction(transList, ps)

    # -----------------------------------------------------------------------
    # moveTransitions
    #
    # Transitions that start from a state are to be moved under that state
    # -----------------------------------------------------------------------  
    def moveTransitions(self):
        for child in PreOrderIter(self.tree):
            if child.name == "TRANSITION": 
                # Look up where this transition is supposed to go
                state = self.idMap[child.source]
                # Move the transition under the source state
                self.moveTransition(child, state)

            if child.name == "JUNCTION":
                for sourceTransition in PreOrderIter(self.tree):
                    if (sourceTransition.name == "TRANSITION") and (sourceTransition.target == child.id):
                        #state = xmiModel.idMap[parentState.source]
                        child.parent = sourceTransition.parent.parent
                        # Move the transition under the source state

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
    
    def getStates(self):
        stateList = []

        for child in PreOrderIter(self.tree):
            if child.name == "STATE":
                stateList.append(child.stateName)

        print(stateList)

        return stateList
    
    def flattenModel(self):
        flattenedTransitions = set()
        rootNode = self.tree

        #self.addState("State 7", rootNode, None, None, 7)

        for child in rootNode.children:
            if child.name == "STATE":
                if (self.isSuperstate(child)):
                    self.flattenSuperstate(child, flattenedTransitions)

                    #print("break loop")

                    break
    
    def flattenSuperstate(self, superstate: Node, flattenedTransitions: set):
        initial = self.getSuperstateInitial(superstate)

        self.retargetAllTransitionsToSuperstate(initial, superstate)

        for child in superstate.children:
            if child.name == "TRANSITION":
                if (child.target == None):
                    flattenedTransitions.add(child)
            if child.name == "STATE":
                if (self.isSuperstate(child)):
                    #print(f"{superstate.stateName} is a superstate. Moving transitions.")

                    self.flattenSuperstate(child, flattenedTransitions)
                else:
                    #print(f"{child.stateName} is innermost state of {superstate.stateName}")

                    for transition in superstate.children:
                        if transition.name == "TRANSITION":
                            if transition.target == None:
                                if (self.inheritTransition(child, transition)):
                                    self.addTransition(child.id, None, transition.event, transition.guard, transition.action, transition.kind, child)
                            elif transition.source == superstate.id:
                                self.addTransition(child.id, transition.target, transition.event, transition.guard, transition.action, transition.kind, child)

                    child.parent = superstate.parent

                    #self.resolveSuperstateTransitions(initial)
                
        #print(f"Removing superstate: {superstate.stateName}")

        superstate.parent = None

    def retargetAllTransitionsToSuperstate(self, initialTransition: Node, superstate: Node):
        target = superstate.id

        for child in PreOrderIter(self.tree):
            if child.name == "TRANSITION":
                if child.target == target:
                    child.target = initialTransition.target
    
    def inheritTransition(self, state: Node, transition: Node):
        for child in state.children:
            if child.name == "TRANSITION":
                if (child.event == transition.event):
                    return False
        
        return True

    def getSuperstateInitial(self, node: Node):
        for child in node.children:
            if child.name == "INITIAL":
                return child
            
    def resolveSuperstateTransitions(self, node: Node):
        flattenedTransitions = set()
        target = node.target

        for child in PreOrderIter(self.tree):
            if child.name == "TRANSITION":
                if child.target == target:
                    flattenedTransitions.add(child)

    def isSuperstate(self, node: Node):
        if node == None:
            print("Node is none. Cannot evaluate children")

            return False
        else:
            if node.name == "STATE":
                for child in node.children:
                    if child.name == "STATE":
                        #print(f"Substate of {node.stateName} is {child.stateName}")

                        return True
            else:
                print("Node is not a state. Children cannot be evaluated")

                return False



   # --------------------------------------------------------
    # print
    #
    # Print the model as a tree
    # --------------------------------------------------------
    def print(self):
        print("---------------- xmi Model ------------")
        print(RenderTree(self.tree))
        print("------------------end------------------")


