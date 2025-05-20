from node import Node
from af import AF

from typing import Dict, Set
from collections import defaultdict


class Tree:

    def __init__(self):
        self.__nodes: list[Node] = list()
        self.__follow_pose: Dict[str, Set[str]] = dict()
        self.__alphabet: Set[str] = set()
        self.__node_value_to_token: Dict[str, str] = defaultdict(str)
        self.__acceptance_node: Node = None

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
    
    @property
    def node_value_to_token(self):
        return self.__node_value_to_token
    
    @property
    def acceptance_node(self):
        return self.__acceptance_node
    
    @acceptance_node.setter
    def acceptance_node(self, node: Node):
        self.__acceptance_node = node
    
    def update_follow_pose(self, value:str, follow_pose:set):
        self.follow_pose[value] = self.follow_pose[value].union(follow_pose)
    
    def add_default_follow_pose(self, value:str):
        self.follow_pose[value] = set()
    
    def calculate_nodes_data(self):
        for node in self.nodes:

            if node.left_node == None and node.right_node == None and node.token != "&":
                node.first_pose.add(node.value)
                node.last_pose.add(node.value)

                if node.token != "#":
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
            
    def calculate_node_follow_pose(self, node: Node):
        if node.token == "*":
            for value in node.last_pose:
                self.update_follow_pose(value, node.first_pose)
    
        if node.token == ".":
            for value in node.left_node.last_pose:
                self.update_follow_pose(value, node.right_node.first_pose)
    
    def generate_automata(self) -> AF:
        format_states_name = dict()
        initial_state = self.nodes[-1].first_pose
        initial_state_name = self.format_automata_state_name(initial_state)
        states = {initial_state_name}
        final_states = set()
        transitions = dict()

        queue = [initial_state]

        while len(queue) != 0:
            current_state = queue.pop(0)
            current_state_name = self.format_automata_state_name(current_state)
            format_states_name[current_state_name] = "q" + str(len(states)-1)

            for character in self.alphabet:

                if self.acceptance_node.value in current_state: 
                    final_states.add(current_state_name)

                next_state = set()
                for node_value in current_state:
                    node_token = self.node_value_to_token[node_value]

                    if node_token == character:
                        next_state = next_state.union(self.follow_pose[node_value])

                                                                        
                if len(next_state) == 0:
                    continue
                
                next_state_name = self.format_automata_state_name(next_state)
                if next_state_name not in states:
                    states.add(next_state_name)
                    queue.append(next_state)
                
                transitions[(current_state_name, character)] = next_state_name

        initial_state = format_states_name[initial_state_name]

        states = list(states)
        for state in states[:]:
            states.remove(state)
            states.append(format_states_name[state])
        states = set(states)

        final_states = list(final_states)
        for state in final_states[:]:
            final_states.remove(state)
            final_states.append(format_states_name[state])
        final_states = set(final_states)

        new_transitions = dict()
        for state, alphabet_character in transitions:
            new_transitions[(format_states_name[state], alphabet_character)] = {format_states_name[transitions[(state, alphabet_character)]]}
        
        return AF(states, self.alphabet, initial_state, final_states, new_transitions)
        
    def format_automata_state_name(self, name: set):
        state = map(int, list(name))
        state = sorted(state)
        state = map(str, state)
        return "".join(state)
            
    def __str__(self):
        text = ""
        for node in self.nodes:
            text += f"Token: {node.token}, Value: {node.value}, First Pose: {node.first_pose}, Last pose: {node.last_pose}, Nullable: {node.nullable}\n"
        
        return text
                
