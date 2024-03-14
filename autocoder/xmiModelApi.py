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

    def __init__(self, packageName, stateMachineName):
        self.tree.package = packageName
        self.tree.stateMachine = stateMachineName

    def addState(self, name, parent, entry, exit, id):
        thisNode = Node("STATE", stateName = name, parent=parent, entry=entry, exit=exit, id=id)
        return thisNode

    def addTransition(self, source, target, event, guard, action, kind, parent):
        thisNode=Node("TRANSITION", source=source, target=target, event=event, guard=guard, action=action, kind=kind, parent=parent)
        return thisNode

    def addPsuedostate(self, id, parent):
        thisNode = Node("PSUEDOSTATE", id = id, parent = parent)
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
    # print
    #
    # Print the model as a tree
    # --------------------------------------------------------
    def print(self):
        print("---------------- xmi Model ------------")
        print(RenderTree(self.tree))
        print("------------------end------------------")


