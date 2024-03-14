#!/usr/bin/env python
# -----------------------------------------------------------------------
# qmModelApi.py
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


class qmModel:
    package = ''
    stateMachine = ''
    tree = Node('new')

    def __init__(self, packageName, stateMachineName):
        self.tree.package = packageName
        self.tree.stateMachine = stateMachineName
        self.tree.position=[]

    def addState(self, entry, exit, id, name, parent):
        thisNode = Node("STATE", entry=entry, exit=exit, id=id, stateName=name, parent=parent)
        return thisNode

    def addInit(self, target, action, guard, event, parent):
        thisNode = Node("INIT", target=target, action=action, guard=guard, event=event, parent=parent)
        return thisNode

    def addTransition(self, source, target, action, guard, event):
        # Figure out the parent by searching the source in the state nodes
        parent = anytree.search.find_by_attr(self.tree, name="id", value=source)
        thisNode = Node("TRANSITION", source=source, target=target, action=action, guard=guard, event=event, parent=parent)
        return thisNode

    def addChoice(self, target, action, guard, parent):
        thisNode = Node("CHOICE", target=target, action=action, guard=guard, parent=parent)
        return thisNode

    def getRoot(self):
        return self.tree

    def getPackageName(self):
        return self.tree.package

    def getStateMachineName(self):
        return self.tree.stateMachine

    #-----------------------------------------------------------------------
    # assignAbsolutePositions
    #
    # Assign absolute position value to all nodes in the tree
    # -----------------------------------------------------------------------
    def assignAbsolutePositions(self, treeNode = tree):
        nodeNum = 0
        for node in treeNode.children:
            nodeNum = nodeNum + 1
            node.position = node.parent.position + [nodeNum]
            self.assignAbsolutePositions(node)

    #-----------------------------------------------------------------------
    # makeRelativeTargets
    #
    # Make all target attributes in the tree relative
    # -----------------------------------------------------------------------
    def makeRelativeTargets(self, treeNode = tree):
        for node in treeNode.children:
            if (node.name == "CHOICE") or (node.name == "TRANSITION") or (node.name == "INIT"):
                if node.target is not None:
                    node.target = self.getRelativePosition(node)
            self.makeRelativeTargets(node)

       

    #-----------------------------------------------------------------------
    # getRelativePosition
    #
    # Given a sourceId and a targetId, compute the relative path from 
    # source to target.
    # Return the relative path as a string.
    # -----------------------------------------------------------------------
    def getRelativePosition(self, sourceNode):
        
        targetNode = anytree.search.find_by_attr(self.tree, name="id", value=sourceNode.target)
        sourcePos = sourceNode.position
        targetPos = targetNode.position
        ancestorNodes = anytree.util.commonancestors(sourceNode, targetNode)
        ancestorPos = ancestorNodes[-1].position

        up = len(sourcePos) - len(ancestorPos)
        down = len(targetPos) - len(ancestorPos)
        downList = targetPos[-down:]
        
        downPath = ""
        for e in downList:
            downPath = downPath + str(e) + "/"

        upPath = "../"*up
        rel = upPath + downPath.strip('/')

        return(rel)


   # --------------------------------------------------------
    # print
    #
    # Print the model as a tree
    # --------------------------------------------------------
    def print(self):
        print("---------------- qm Model ------------")
        print(RenderTree(self.tree))
        print("------------------end------------------")


