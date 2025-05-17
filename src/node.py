class Node:

    def __init__(self, token: str, left_node: "Node" = None, right_node: "Node" = None, value: str = str()):

        self.__token: str = token
        self.__value: str = value
        self.__first_pose: set = set()
        self.__last_pose: set = set()
        self.__nullable: bool = False
        self.__left_node: Node = left_node
        self.__right_node: Node = right_node
    

    def __str__(self):
        return f"token: {self.token}, value: {self.value}"

    @property
    def token(self):
        return self.__token
    
    @token.setter
    def token(self, token: str):
        self.__token = token
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value: str):
        self.__value = value

    @property
    def first_pose(self):
        return self.__first_pose
    
    @first_pose.setter
    def first_pose(self, first_pose: set):
        self.__first_pose = first_pose
    
    @property
    def last_pose(self):
        return self.__last_pose
    
    @last_pose.setter
    def last_pose(self, last_pose: set):
        self.__last_pose = last_pose
    
    @property
    def nullable(self):
        return self.__nullable

    @nullable.setter
    def nullable(self, nullable: bool):
        self.__nullable = nullable

    @property
    def left_node(self):
        return self.__left_node

    @left_node.setter
    def left_node(self, left_node: "Node"):
        self.__left_node = left_node

    @property
    def right_node(self):
        return self.__right_node

    @right_node.setter
    def right_node(self, right_node: "Node"):
        self.__right_node = right_node
    

    

    

    
