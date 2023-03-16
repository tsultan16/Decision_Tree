'''
    Code Description: ID3 Decision Tree Implementation

    Author: Tanzid Sultan
'''
from math import log2

class TreeNode(object):

    def __init__(self, value, branch = None):
        self.value = value
        self.branch = branch
        self.children = []

    def add_child_node(self, child_node):
        print(f"Adding child_node with value: '{child_node.value}' from branch: '{child_node.branch}'")
        self.children.append(child_node)

    def remove_child_node(self, child_node):
        self.children = [child for child in self.children if child is not child_node] 

def print_tree(root_node, level):
   
    print(f"\nLevel: {level}, Node: {root_node.value}, Branch: {root_node.branch} , Children: ", end = "")
    if(len(root_node.children) > 0):
        for child in root_node.children:
            print(child.value + "  ", end ="")  

        for child in root_node.children:
            print_tree(child, level+1)

    else:    
        print("None", end ="")


# function for predicting the target attribute/class of an unclassified instance
def classify(unclassified_instance, tree_root):

    root = tree_root

    print("\nUnclassified instance: \n",unclassified_instance)
    
    # make sure attribute data is valid
    for attribute in unclassified_instance:
        if(attribute not in [attribute for attribute in attributes]):
            print("Invalid attribute name in unclassified instance data!")
            return -1

        if(unclassified_instance[attribute] not in attributes[attribute]):
            print("Invalid attribute value name in unclassified instance data!")
            return -1
    
    stop = False
    while (not stop):

        print(f"root.value: {root.value}")
        print(f"root_children: {[child.value for child in root.children]}" ) 
        print(f"root_children_branch: ", [child.branch for child in root.children])
    
        if(len(root.children) == 0):
            print("Found a leaf node!")
            prediction = root.value
            stop = True
        else:
            print(f"Instance attribute : {root.value}, Value: {unclassified_instance[root.value]}")

            child_index = [child.branch for child in root.children].index(unclassified_instance[root.value])
            root = root.children[child_index]

            print("\nTraversing tree to new root.\n")

    print(f"Prediction: {prediction}")
    return prediction

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

# function for partioining according to the attribute with largest gain ratio 
def partition_by_best_attribute(S, attributes_remaining):
    
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
    return partitions, best_attribute

#################
# ID3 algorithm #
#################
def ID3(S, attributes_remaining, root_node):

    # create partitions for each attribute and find the best attribute
    partitions, best_attribute = partition_by_best_attribute(S, attributes_remaining)
    attributes_remaining.remove(best_attribute)

    print(f"\nBest attribute is '{best_attribute}'")     
    print(f"\nAttributes remaining: {attributes_remaining}\n")
    
    # set the root node value to best attribute
    root_node.value = best_attribute 

    # iterate over each new partition, and test stopping condition for further partitioning
    for partition in partitions:
        H = entropy(partitions[partition]) 
        print(f"Partition: {partition}, Entropy = {H}")

        # stopping conditions: (1) if a partition has entropy = 0, it's a leaf
        #                      (2) if no more attributes remaining  
        if(H == 0.0 or len(attributes_remaining) == 0):
            print("Found a zero entropy partition!")
            target_vals = []
            for instance in partitions[partition]:
                target_vals.append(instance[target_attribute])
            print(f"target values: {target_vals}")

            # find target attribute value with the highest count
            # (TO DO: need to decide what to do in case there's a tie between different attribute value counts)
            max_count = 0
            max_target_val = None
            for val in attributes[target_attribute]:
                if (target_vals.count(val) > max_count):
                    max_target_val = val
           
            # assign target attribute value with the highest count as leaf node
            leaf = max_target_val

            # add leaf node
            child_node = TreeNode(value = leaf, branch = partition)
            root_node.add_child_node(child_node)

        else:

            # add child node
            child_node = TreeNode(value = partition, branch = partition)
            root_node.add_child_node(child_node)

            # recursively call ID3 for further partitioning
            ID3(partitions[partition], attributes_remaining, child_node)



# attributes (Note: 'play' is our target attribute/class)
attributes = { 'outlook' : ['sunny', 'overcast', 'rainy'], 'temperature' : ['hot', 'mild', 'cool'], 'humidity' : ['high', 'normal'], 'wind' : ['weak', 'strong'], 'play' : ['no', 'yes'] }
target_attribute = 'play'


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


# set of training instances
S = training_data
# create a root node for our decision tree
root = TreeNode('root')

attributes_remaining = [attribute for attribute in attributes if attribute is not target_attribute]

print("\n### Building decision tree...\n")
ID3(S, attributes_remaining, root)
print("\n### Done!\n")

example_unclassified_instance = {'outlook' : 'overcast','temperature' : 'cool', 'humidity' : 'high', 'wind' : 'strong'}

print_tree(root_node = root, level = 0)
classify(example_unclassified_instance, root)


