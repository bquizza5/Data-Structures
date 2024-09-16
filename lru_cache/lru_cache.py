
def printList(item1):
    print(item1.value)
    if item1.next != None:
        return printList(item1.next)

def returnNode(item1, value):
    if str(item1.value) == value:
        print('same', item1.value, value)
        return item1
    else:
        print('different', item1.value, value)
        if item1.next != None:
            return returnNode(item1.next, value)
        else:
            return None


class ListNode:
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next
    
    def __str__(self):
        return f'{self.value}'

    """Wrap the given value in a ListNode and insert it
    after this node. Note that this node could already
    have a next node it is point to."""
    def insert_after(self, value):
        current_next = self.next
        self.next = ListNode(value, self, current_next)
        if current_next:
            current_next.prev = self.next

    """Wrap the given value in a ListNode and insert it
    before this node. Note that this node could already
    have a previous node it is point to."""
    def insert_before(self, value):
        current_prev = self.prev
        self.prev = ListNode(value, current_prev, self)
        if current_prev:
            current_prev.next = self.prev

    """Rearranges this ListNode's previous and next pointers
    accordingly, effectively deleting this ListNode."""
    def delete(self):
        if self.prev:
            self.prev.next = self.next
        if self.next:
            self.next.prev = self.prev


"""Our doubly-linked list class. It holds references to
the list's head and tail nodes."""



class DoublyLinkedList:
    def __init__(self, node=None):
        self.head = node
        self.tail = node
        self.length = 1 if node is not None else 0

    def __len__(self):
        return self.length

    """Wraps the given value in a ListNode and inserts it 
    as the new head of the list. Don't forget to handle 
    the old head node's previous pointer accordingly."""
    def add_to_head(self, value):
        newNode = ListNode(value, None, self.head)

        if not self.head and not self.tail:
            self.head = newNode
            self.tail = newNode
        else:
            newNode.next = self.head
            self.head.prev = newNode
            self.head = newNode
        self.length += 1


    """Removes the List's current head node, making the
    current head's next node the new head of the List.
    Returns the value of the removed Node."""
    def remove_from_head(self):
        value = self.head.value
        self.delete(self.head)
        return value

    """Wraps the given value in a ListNode and inserts it 
    as the new tail of the list. Don't forget to handle 
    the old tail node's next pointer accordingly."""
    def add_to_tail(self, value):
        newNode = ListNode(value, self.tail, None)

        if not self.head and not self.tail:
            self.head = newNode
            self.tail = newNode
        else:
            self.tail.next = newNode
            self.tail = newNode
        self.length += 1

    """Removes the List's current tail node, making the 
    current tail's previous node the new tail of the List.
    Returns the value of the removed Node."""
    def remove_from_tail(self):
        value = self.tail.value
        self.delete(self.tail)
        return value

    """Removes the input node from its current spot in the 
    List and inserts it as the new head node of the List."""
    def move_to_front(self, node):
        if node == self.head:
            return
        value = node.value
        self.delete(node)
        self.add_to_head(value)

    """Removes the input node from its current spot in the 
    List and inserts it as the new tail node of the List."""
    def move_to_end(self, node):
        if node == self.tail:
            return
        value = node.value
        self.delete(node)
        self.add_to_tail(value)

    """Removes a node from the list and handles cases where
    the node was the head or the tail"""
    def delete(self, node):
        self.length -= 1

        if self.head is self.tail:
            self.head = None
            self.tail = None
        elif node == self.head:
            self.head = self.head.next
            node.delete()
        elif node == self.tail:
            self.tail = self.tail.prev
            node.delete()
        else:
            node.delete()

        
    """Returns the highest value currently in the list"""
    def get_max(self):
        if not self.head:
            return None

        max_val = self.head.value
        current = self.head

        while current:
            if current.value > max_val:
                max_val = current.value
            current = current.next
        return max_val



class LRUCache:
    """
    Our LRUCache class keeps track of the max number of nodes it
    can hold, the current number of nodes it is holding, a doubly-
    linked list that holds the key-value entries in the correct
    order, as well as a storage dict that provides fast access
    to every node stored in the cache.
    """
    def __init__(self, limit=10):
        self.limit = limit
        self.length = 0
        self.order = DoublyLinkedList()
        self.storage = dict()

    """
    Retrieves the value associated with the given key. Also
    needs to move the key-value pair to the end of the order
    such that the pair is considered most-recently used.
    Returns the value associated with the key or None if the
    key-value pair doesn't exist in the cache.
    """
    def get(self, key):
        if key in self.storage.keys():
            node = returnNode(self.order.head, key)
            if node != None:
                self.order.move_to_front(node)
            # print('***start***')
            # printList(self.order.head)
            # print("***end***")
                return self.storage[key]
            else:
                return None
        else:
            return None


    """
    Adds the given key-value pair to the cache. The newly-
    added pair should be considered the most-recently used
    entry in the cache. If the cache is already at max capacity
    before this entry is added, then the oldest entry in the
    cache needs to be removed to make room. Additionally, in the
    case that the key already exists in the cache, we simply
    want to overwrite the old value associated with the key with
    the newly-specified value.
    """
    def set(self, key, value):
        if key in self.storage.keys():
            self.storage[key] = value
            node = returnNode(self.order.head, key)
            self.order.move_to_front(node)

        else:
            if self.order.length == self.limit:
                del self.storage[str(self.order.tail.value)]
                self.order.remove_from_tail()

            self.storage[key] = value
            node = ListNode(key)
            self.order.add_to_head(node)



cache = LRUCache(3)
cache.set('item1', 'a')
cache.set('item2', 'b')
cache.set('item3', 'c')

print(1,cache.get('item1'))
cache.set('item4', 'd')

print(2,cache.get('item1'))
print(3,cache.get('item3'))
print(4,cache.get('item4'))
print(5,cache.get('item2'))
