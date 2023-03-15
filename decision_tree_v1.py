'''
    Code Description: ID3 Decision Tree Implementation

    Author: Tanzid Sultan
'''

import numpy as np
from math import log2


class TreeNode(object):

    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child_node(self, child_node):
        print(f"Adding child_node with value: {child_node.value}")
        self.children.append(child_node)

    def remove_child_node(self, child_node):
        self.children = [child for child in self.children if child is not child_node] 

def print_tree(root_node):
   
    print(f"\nNode: {root_node.value}, Children: ", end = "")
    
    if(len(root.children) > 0):
        for child in root_node.children:
            print(child.value + "  ", end ="")        
    else:    
        print(f"None")

    for child in root_node.children:
        if(len(child.children) > 0):
            print_tree(child)
        else:
            print(f"\nNode: {child.value}, Children: None", end = "")
    print("")

'''
root = TreeNode('root')
child_node1 = TreeNode('c1')
child_node2 = TreeNode('c2')
child_node3 = TreeNode('c3')
child_node4 = TreeNode('c4')
root.add_child_node(child_node1)
root.add_child_node(child_node2)
child_node2.add_child_node(child_node3)
child_node2.add_child_node(child_node4)
print_tree(root)
'''

# attributes (Note: 'play' is our target attribute/class)
attributes = { 'outlook' : ['sunny', 'overcast', 'rainy'], 'temperature' : ['hot', 'mild', 'cool'], 'humidity' : ['high', 'normal'], 'wind' : ['weak', 'strong'], 'play' : ['no', 'yes'] }
target_attribute = 'play'

# function for computing the entropy 'H' of a given set S
#  where H := sum_i (p_i log2(p_i)), where the index runs over distinct values of S and p_i is the proportion of the ith value in the set
def entropy(S):
    S_target = []
    for instance in S:
        S_target.append(instance[target_attribute])
    
    S_vals = set(S_target) # all distinct vaues in S  
    S_len = len(S_target) # total number of values in S
    H = 0.0
    for val in S_vals:
        p = S_target.count(val)/S_len # proportion of the distinct value

        if(p == 0.0):
            log2_p= 0.0
        else:
            log2_p = log2(p)
        
        H -= p * log2_p
    return H

# function for creating partitions of the set S of instances according to the given attribute and computing the gain ratio for this partitioning
def create_partitions(S, attribute):
 
    print("\nSet: ", end = "")
    for instance in S:
        print(instance['id'] + "  ", end = "")
    print("")    
    print(f"Partitioning by '{attribute}' attribute:")

    S_attribute = []
    for instance in S:
        S_attribute.append(instance[attribute])

    S_attribute_vals = attributes[attribute]
    partitions = {}
    for val in S_attribute_vals:
        #print(f"{val} count: {S_attribute.count(val)}")
        partitions[val] = [] 

    # create partitions and compute entropy of each partition
    for instance in S:
        partitions[instance[attribute]].append(instance)
   
    for partition in partitions:
        print(f"{partition} : ", end="")
        for instance in partitions[partition]:
            print(instance['id'] + "  ", end="")
        print("")

    # compute information gain and split-information
    gain = entropy(S)
    split_info = 0.0
    for partition in partitions:
        p_s = len(partitions[partition]) / len(S)
        gain -= p_s * entropy(partitions[partition])
        
        if(p_s == 0.0):
            log2_ps = 0.0
        else:
            log2_ps = log2(p_s) 

        split_info -= p_s * log2_ps

    gain_ratio = gain / split_info
    return partitions, gain_ratio    

# training_data is a list of instances, each instance is a list of attributes with the target class at the end
# instance = [Outlook, Temperature, Humidity, Wind, Play (target class)]
training_data = [ {'id' : 'a', 'outlook' : attributes['outlook'][0],'temperature' : attributes['temperature'][0],'humidity' : attributes        ['humidity'][0], 'wind' : attributes['wind'][0], 'play' : attributes['play'][0]},
                  {'id' : 'b', 'outlook' : attributes['outlook'][0],'temperature' : attributes['temperature'][0],'humidity' : attributes['humidity'][0], 'wind' : attributes['wind'][1], 'play' : attributes['play'][0]},
                  {'id' : 'c', 'outlook' : attributes['outlook'][1],'temperature' : attributes['temperature'][0],'humidity' : attributes['humidity'][0], 'wind' : attributes['wind'][0], 'play' : attributes['play'][1]},
                  {'id' : 'd', 'outlook' : attributes['outlook'][2],'temperature' : attributes['temperature'][1],'humidity' : attributes['humidity'][0], 'wind' : attributes['wind'][0], 'play' : attributes['play'][1]},
                  {'id' : 'e', 'outlook' : attributes['outlook'][2],'temperature' : attributes['temperature'][2],'humidity' : attributes['humidity'][1], 'wind' : attributes['wind'][0], 'play' : attributes['play'][1]},
                  {'id' : 'f', 'outlook' : attributes['outlook'][2],'temperature' : attributes['temperature'][2],'humidity' : attributes['humidity'][1], 'wind' : attributes['wind'][1], 'play' : attributes['play'][0]},
                  {'id' : 'g', 'outlook' : attributes['outlook'][1],'temperature' : attributes['temperature'][2],'humidity' : attributes['humidity'][1], 'wind' : attributes['wind'][1], 'play' : attributes['play'][1]},
                  {'id' : 'h', 'outlook' : attributes['outlook'][0],'temperature' : attributes['temperature'][1],'humidity' : attributes['humidity'][0], 'wind' : attributes['wind'][0], 'play' : attributes['play'][0]},
                  {'id' : 'i', 'outlook' : attributes['outlook'][0],'temperature' : attributes['temperature'][2],'humidity' : attributes['humidity'][1], 'wind' : attributes['wind'][0], 'play' : attributes['play'][1]},
                  {'id' : 'j', 'outlook' : attributes['outlook'][2],'temperature' : attributes['temperature'][1],'humidity' : attributes['humidity'][1], 'wind' : attributes['wind'][0], 'play' : attributes['play'][1]},
                  {'id' : 'k', 'outlook' : attributes['outlook'][0],'temperature' : attributes['temperature'][1],'humidity' : attributes['humidity'][1], 'wind' : attributes['wind'][1], 'play' : attributes['play'][1]},
                  {'id' : 'l', 'outlook' : attributes['outlook'][1],'temperature' : attributes['temperature'][1],'humidity' : attributes['humidity'][0], 'wind' : attributes['wind'][1], 'play' : attributes['play'][1]},
                  {'id' : 'm', 'outlook' : attributes['outlook'][1],'temperature' : attributes['temperature'][0],'humidity' : attributes['humidity'][1], 'wind' : attributes['wind'][0], 'play' : attributes['play'][1]},
                  {'id' : 'n', 'outlook' : attributes['outlook'][2],'temperature' : attributes['temperature'][1],'humidity' : attributes['humidity'][0], 'wind' : attributes['wind'][1], 'play' : attributes['play'][0]} ]

#################
# ID3 algorithm #
#################


#########################
# choose best attribute #
#########################


def ID3(S, attributes_remaining, root_node):

    # create partitions for each attribute and find the best attribute
    attribute_partitions = {}
    max_GR = 0.0
    best_attribute = None
    for attribute in attributes_remaining:
        partitions, gain_ratio = create_partitions(S, attribute)
        attribute_partitions[attribute] = partitions
        print(f"{attribute} gain ratio: {gain_ratio}")   
        if(gain_ratio > max_GR):
            best_attribute = attribute
            max_GR = gain_ratio

    partitions = attribute_partitions[best_attribute]
    print(f"\nBest attribute is '{best_attribute}'")     

    attributes_remaining.remove(best_attribute)

    #print(partitions)
    
    # create the root node
    root_node.value = best_attribute 

    print_tree(root_node)


    print(f"\nAttributes remaining: {attributes_remaining}\n")

    # iterate over each new partition, and test condition for further partitioning
    for partition in partitions:
        H = entropy(partitions[partition]) 
        print(f"Partition: {partition}, Entropy = {H}")

        # stopping conditions: (1) if a partition has entropy = 0, it's a leaf
        #                      (2) if no more attributes remaining  
        if(H == 0.0 or len(attributes_remaining) == 0):
            print("Found a zero entropy partition!")
            play_vals = []
            for instance in partitions[partition]:
                play_vals.append(instance['play'])
            print(f"play values: {play_vals}")
            if (play_vals.count('yes') > play_vals.count('no')):
                leaf = 'yes'
            else:
                leaf = 'no'     

            # add leaf node
            child_node = TreeNode(leaf)
            root_node.add_child_node(child_node)

        else:

            # add child node
            child_node = TreeNode(partition)
            print("\n############################")
            root_node.add_child_node(child_node)
            print("############################")

            # recursively call ID3 for further partitioning
            ID3(partitions[partition], attributes_remaining, child_node)


        print_tree(root)


S = training_data
root = TreeNode('root')
attributes_remaining = [attribute for attribute in attributes if attribute is not target_attribute]

print("\n### Building decision tree...\n")
ID3(S, attributes_remaining, root)
