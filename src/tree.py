from node import Node

from typing import Dict, Set


class Tree:

    def __init__(self):
        self.__nodes: list[Node] = list()
        self.__follow_pose: Dict[str, Set[str]] = dict()
        self.__alphabet: Set[str] = set()

    @property
    def nodes(self):
        return self.__nodes

    def add_node(self, node: Node):
        self.__nodes.append(node)

        if node.value:
            self.add_default_follow_pose(node.value)
    
    @property
    def follow_pose(self):
        return self.__follow_pose
    
    @property
    def alphabet(self):
        return self.__alphabet
    
    def update_follow_pose(self, value:str, follow_pose:set):
        self.follow_pose[value] = self.follow_pose[value].union(follow_pose)
    
    def add_default_follow_pose(self, value:str):
        self.follow_pose[value] = set()
    
    def calculate_nodes_data(self):
        for node in self.nodes:

            if node.left_node == None and node.right_node == None and node.token != "&":
                node.first_pose.add(node.value)
                node.last_pose.add(node.value)
                self.alphabet.add(node.token)

            if node.token == "|":
                node.nullable = node.left_node.nullable or node.right_node.nullable
                node.first_pose = node.left_node.first_pose.union(node.right_node.first_pose)
                node.last_pose = node.left_node.last_pose.union(node.right_node.last_pose)
            
            if node.token == "*":
                node.nullable = True
                node.first_pose = node.left_node.first_pose
                node.last_pose = node.left_node.last_pose

            if node.token == ".":
                node.nullable = node.left_node.nullable and node.right_node.nullable
                
                if node.left_node.nullable:
                    node.first_pose = node.left_node.first_pose.union(node.right_node.first_pose)
                else:
                    node.first_pose = node.left_node.first_pose
                
                if node.right_node.nullable:
                    node.last_pose = node.left_node.last_pose.union(node.right_node.last_pose)
                else:
                    node.last_pose = node.right_node.last_pose
                
            if node.token == "&":
                node.nullable = True

            if node.token in ["*", "."]:
                self.calculate_node_follow_pose(node)
        
        print(self.follow_pose)
    
    def calculate_node_follow_pose(self, node: Node):
        if node.token == "*":
            for value in node.last_pose:
                self.update_follow_pose(value, node.first_pose)
    
        if node.token == ".":
            for value in node.left_node.last_pose:
                self.update_follow_pose(value, node.right_node.first_pose)
    
    def generate_automata(self):
        states = set()
        initial_state_values = map(str, (list(self.nodes[-1].first_pose)))
        initial_state = "".join(initial_state_values)
        transitions = dict()

        states.add(initial_state)

        for character in self.alphabet:
            for value in initial_state_values:
                ...

        
            
    def __str__(self):
        text = ""
        for node in self.nodes:
            text += f"Token: {node.token}, Value: {node.value}, First Pose: {node.first_pose}, Last pose: {node.last_pose}, Nullable: {node.nullable}\n"
        
        return text
                
