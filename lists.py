class Node:
    """Node class for stacks and queues: with v the saved value"""
    def __init__(self, v=None, s=None):
        """Constructor of the class that stores the values"""
        self.value = v
        self.next = s

    def __str__(self):
        """Function that allows displaying lists"""
        if self.next == None:
            return f"{self.value}"
        else:
            return f"{self.value} - {self.next}"
        
class Stack:
    """Stack class"""
    def __init__(self):
        """Constructor of the Stack class"""
        # constructor of the class
        self.first = None

    def add(self, v):
        """Function that adds a node with the new value to the stack"""
        m = Node(v)
        n = self.first
        self.first = m
        self.first.next = n
    
    def remove(self):
        """Function that removes the topmost element"""
        if self.first != None:
            v = self.first.value
            self.first = self.first.next
            return v
        else:
            return None

    def size(self):
        """Function that returns the size of the stack"""
        n = 0
        if self.first != None:
            current = self.first
            n = n + 1
            while current.next != None:
                n = n + 1
                current = current.next
        return n
    
    def contains(self, value):
        """Function that checks if a value is present in the stack"""
        result = False
        if self.first != None:
            current = self.first
            
            if self.first == value:
                result = True
            while current.next != None:
                current = current.next
                if current.value == value:
                    result = True
            
        return result

    def __str__(self):
        return f"{self.first}"

class Queue:
    """Queue class"""
    def __init__(self):
        """Constructor of the Queue class"""
        # constructor of the class
        self.first = None

    def add(self, v):
        """Function that adds a node with the new value to the queue"""
        m = Node(v)
        if self.first == None:
            self.first = m
        else:
            current = self.first
            while current.next != None:
                current = current.next
            current.next = m
    
    def remove(self):
        """Function that removes the first element"""
        if self.first != None:
            v = self.first.value
            self.first = self.first.next
            return v
    
    def check(self):
        """Function that returns the first element's "bar"""
        if self.first != None:
            v = self.first.value
            return v[0]
    
    def copy(self):
        """Function that allows copying an entire queue"""
        elements = []
        current = None
        if self.first != None:
            current = self.first
            elements.append(current.value)
            while current.next != None:
                elements.append(current.next.value)
                current = current.next
        new_queue = Queue()
        for elt in elements:
            new_queue.add(elt)
        return new_queue
    
    def size(self):
        """Function that returns the size of the queue"""
        n = 0
        if self.first != None:
            current = self.first
            n = n + 1
            while current.next != None:
                n = n + 1
                current = current.next
        return n

    def __str__(self):
        return f"{self.first}"