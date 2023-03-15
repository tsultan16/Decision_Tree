'''
    ID3 Decision Tree Implementation
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
    for child in root_node.children:
        print(child.value + "  ", end ="")

    for child in root_node.children:
        if(len(child.children) > 0):
            print_tree(child)
        else:
            print(f"\nNode: {child.value}, Children: None", end = "")

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

# attributes
attributes = { 'outlook' : ['sunny', 'overcast', 'rainy'], 'temperature' : ['hot', 'mild', 'cool'], 'humidity' : ['high', 'normal'], 'wind' : ['weak', 'strong'], 'play' : ['no', 'yes'] }
# attribute values (play is the target attribute/class)
#play = ['no', 'yes']
#outlook = ['sunny', 'overcast', 'rainy']
#temperature = ['hot', 'mild', 'cool']
#humidity = ['high', 'normal']
#wind = ['weak', 'strong']

# function for computing the entropy 'H' of a given set S
#  where H := sum_i (p_i log2(p_i)), where the index runs over distinct values of S and p_i is the proportion of the ith value in the set
def entropy(S):
    S_play = []
    for instance in S:
        S_play.append(instance['play'])
    
    S_vals = set(S_play) # all distinct vaues in S  
    S_len = len(S_play) # total number of values in S
    H = 0.0
    for val in S_vals:
        p = S_play.count(val)/S_len # proportion of the distinct value
        H -= p * log2(p)
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
        partitions[val] = {'instances' : [], 'entropy' : 0.0}

    # create partitions and compute entropy of each partition
    for instance in S:
        partitions[instance[attribute]]['instances'].append(instance)
   
    for partition in partitions:
        print(f"{partition} : ", end="")
        for instance in partitions[partition]['instances']:
            print(instance['id'] + "  ", end="")
        print("")
    #print("\n Partitions: \n", partitions)   
    # compute information gain and split-information
    gain = entropy(S)
    split_info = 0.0
    for partition in partitions:
        p_s = len(partitions[partition]['instances']) / len(S)
        partitions[partition]['entropy'] = entropy(partitions[partition]['instances'])
        gain -= p_s * partitions[partition]['entropy'] 
        split_info -= p_s * log2(p_s)

    gain_ratio = gain / split_info
    return partitions, gain_ratio    

# training_data is a list of instances, each instance is a list of attributes with the target class at the end
# instance = [Outlook, Temperature, Humidity, Wind, Play (target class)]
training_data = [ {'id' : 'a', 'outlook' : attributes['outlook'][0],'temperature' : attributes['temperature'][0],'humidity' : attributes['humidity'][0], 'wind' : attributes['wind'][0], 'play' : attributes['play'][0]},
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

# root set
S = training_data
print(f"Entropy(S) = {entropy(S)}")

#########################
# choose best attribute #
#########################

# first partitions for each attribute
#outlook_partitions, outlook_gain_ratio = create_partitions(S, 'outlook')
#print(f"Outlook gain ratio: {outlook_gain_ratio}")
#humidity_partitions, humidity_gain_ratio = create_partitions(S, 'humidity')
#print(f"Humidity gain ratio: {humidity_gain_ratio}")

for attribute in {attribute for attribute in attributes if attribute is not 'play'}:
    partitions, gain_ratio = create_partitions(S, attribute)
    print(f"{attribute} gain ratio: {gain_ratio}")   