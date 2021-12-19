
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None
    
class DoublyLinkedList:
    def __init__(self, value):
        self.start_node = Node(value)

    def append(self, value):
        current = self.start_node
        while current.next is not None:
            current = current.next
        new_node = Node(value)
        current.next = new_node
        new_node.prev = current

    def print_list(self):
        current = self.start_node
        while current is not None:
            print(current.value)
            current = current.next



dlist = DoublyLinkedList("START GAME")
dlist.append("DIFFICULTY")
dlist.append("CREDITS")
dlist.append("QUIT")

node = dlist.start_node
node2 = node.next
print(node2.prev.value)