class ListNode:
    def __init__(self, val: int, prev_node=None, next_node=None):
        self.val = val
        self.prev_node = prev_node
        if self.prev_node:
            self.prev_node.next_node = self
        self.next_node = next_node
        if self.next_node:
            self.next_node.prev_node = self

    def __str__(self):
        return str(self.val)

    def __iter__(self):
        node = self
        while node:
            yield node.val
            node = node.next_node

    def pop_prev(self):
        if self.prev_node:
            return self.prev_node.pop()

    def pop_next(self):
        if self.next_node:
            return self.next_node.pop()

    def pop(self):
        if self.prev_node:
            self.prev_node.next_node = self.next_node
        if self.next_node:
            self.next_node.prev_node = self.prev_node
        return self

    def insert_after(self, val: int):
        node = ListNode(val, self, self.next_node)
        if self.next_node:
            self.next_node.prev_node = node
        self.next_node = node
        return node

    def insert_before(self, val: int):
        node = ListNode(val, self.prev_node, self)
        if self.prev_node:
            self.prev_node.next_node = node
        self.prev_node = node
        return node

    @classmethod
    def from_list(cls, elems):
        head = None
        current = None
        for e in elems:
            if not current:
                head = current = ListNode(e)
            else:
                current = current.insert_after(e)
        return head


class SinglyListNode:
    def __init__(self, val=0, next_node=None):
        self.val = val
        self.next_node = next_node

    def has_next(self):
        return self.next_node != None

    def __iter__(self):
        node = self
        while node:
            yield node.val
            node = node.next_node

    def __str__(self):
        return str(self.val) + ("" if self.next_node is None else "->[" + str(self.next_node.val) + "...]")

    def reverse(self, append=None):
        if self.next_node is None:
            self.next_node = append
            return self

        tail = self.next_node
        self.next_node = append
        return tail.reverse(self)

    @classmethod
    def from_list(cls, elems):
        head = None
        tail = None
        for e in elems:
            node = SinglyListNode(e)
            if tail is None:
                head = node
            else:
                tail.next_node = node
            tail = node
        return head


class LinkedList:
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.head = None
        self.tail = None
        self.size = 0

    def __str__(self) -> str:
        buf = []
        node = self.head
        while node:
            buf.append(str(node.val))
            node = node.next_node
        return "[" + (",".join(buf)) + "]"

    def validate(self) -> bool:
        if self.head is None:
            assert self.tail == self.head
            assert self.size == 0
        i = 0
        node = self.head
        while node:
            i += 1
            if node.next_node:
                assert node.next_node.prev_node == node
            else:
                assert self.tail == node
            node = node.next_node
        assert i == self.size
        return True

    def getNode(self, index: int) -> ListNode:
        if index < 0 or index >= self.size:
            return None
        node, i, forward = self.head, index, True
        if index > (self.size >> 1):
            node = self.tail
            forward = False
            i = self.size - index - 1

        while node and i > 0:
            node = node.next_node if forward else node.prev_node
            i = i - 1
        return node

    def isEmpty(self) -> bool:
        return self.head is None

    def get(self, index: int) -> int:
        """
        Get the value of the index-th node in the linked list. If the index is invalid, return -1.
        """
        node = self.getNode(index)
        return node.val if node else -1

    def addAtHead(self, val: int) -> None:
        """
        Add a node of value val before the first element of the linked list. After the insertion, the new node will be the first node of the linked list.
        """
        self.head = ListNode(val, None, self.head)
        self.size += 1
        if self.head.next_node:
            self.head.next_node.prev_node = self.head
        else:
            self.tail = self.head

    def addAtTail(self, val: int) -> None:
        """
        Append a node of value val to the last element of the linked list.
        """
        self.tail = ListNode(val, self.tail, None)
        self.size += 1
        if self.tail.prev_node:
            self.tail.prev_node.next_node = self.tail
        else:
            self.head = self.tail

    def addAtIndex(self, index: int, val: int) -> None:
        """
        Add a node of value val before the index-th node in the linked list. If index equals to the length of linked list, the node will be appended to the end of linked list. If index is greater than the length, the node will not be inserted.
        """
        if index <= 0:
            self.addAtHead(val)
        elif index > 0:
            node = self.getNode(index - 1)
            if node:
                node.next_node = ListNode(val, node, node.next_node)
                self.size += 1
                if node.next_node.next_node:
                    node.next_node.next_node.prev_node = node.next_node
                else:
                    self.tail = node.next_node

    def deleteAtIndex(self, index: int) -> None:
        """
        Delete the index-th node in the linked list, if the index is valid.
        """
        if index == 0:
            if self.head:
                self.head = self.head.next_node
                if self.head:
                    self.head.prev_node = None
                else:
                    self.tail = None
                self.size -= 1

        elif index > 0:
            node = self.getNode(index - 1)
            if node and node.next_node:
                node.next_node = node.next_node.next_node
                if node.next_node:
                    node.next_node.prev_node = node
                else:
                    self.tail = node
                self.size -= 1
