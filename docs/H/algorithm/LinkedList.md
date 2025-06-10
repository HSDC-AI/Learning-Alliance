# LinkedList
手搓linked list 单节点， 力扣707题，执行时间16ms, 消耗内存44.7MB

这个类的实现关键在于节点的遍历，慢的原因也是因为要找某一个index的时候也需要从头开始遍历。当然也要考虑边界的问题，避免index越界。

实现需求必备的几个点
1. 创建Node类，Node中要有Node作为next 和 prev 节点的属性
2. 在主类中需要声明header Node和size，如果优化的话，可以把last Node也维护起来
3. 在按index 插入和删除的方法中，需要维护prev node
4. 要考虑边界问题，在插入的时候要考虑是不是头节点，和尾节点

实现了这几个条件后，一个比较简单的LinkedList就做好了

以下是单节点的Linked List的实现
```java 

package ArrayAndLinked;

/**
 * LeetCode No.707
 * Your MyLinkedList object will be instantiated and called as such:
 * MyLinkedList obj = new MyLinkedList();
 * int param_1 = obj.get(index);
 * obj.addAtHead(val);
 * obj.addAtTail(val);
 * obj.addAtIndex(index,val);
 * obj.deleteAtIndex(index);
 */
public class MyLinkedList {
    // record the first node
    Node header;
    int size;
    public MyLinkedList() {

    }

    public int get(int index) {
        int result = -1;
        Node current = header;
        // loop index number times to find the node if didn't find the node, return -1
        for (int i = 0; i < index; i++) {
            if(current == null){
                return -1;
            }
            current = current.next;
        }

        if (current != null){
            result = current.val;
        }
        return result;
    }

    public void addAtHead(int val) {
        // set the new val node as first and update the next index of original first node as original first node
        if (header != null){
            Node current = header;
            header = new Node(val, current);
        }else {
            header = new Node(val, null);
        }

        size++;
    }

    public void addAtTail(int val) {
        // the size is 0 case
        if (header == null){
            header = new Node(val, null);
        }
        // find the last node
        else{
            Node current = header;
            while (current.next != null){
                current = current.next;
            }
            current.next = new Node(val, null);
        }
        size++;
    }

    public void addAtIndex(int index, int val) {
        // the size is 0 or the index number equals the size
        if(index == size){
            addAtTail(val);
            return;
        }

        Node current = header;
        // record the previous node
        Node prev = null;
        for (int i = 0; i <= index; i++) {
            if (current == null){
                return;
            }

            // update the first node case
            if(i == index && prev == null ){
                header = new Node(val, header == null ? null : current);
                size++;
                return;
            } else if (i == index) {
                // insert the new node to the index position
                prev.next = new Node(val, current);
                size++;
                return;
            }

            // loop the node
            prev = current;
            current = current.next;
        }
    }

    public void deleteAtIndex(int index) {
        Node current = header;
        Node prev = null;
        for (int i = 0; i <= index; i++) {
            if(current == null){
                return;
            }

            if(i == index){
                if(prev == null){
                    header = header.next;
                    size--;
                    return;
                }

                // same as addAtIndex method, but this time we remove the middle node
                prev.next = current.next;
                size--;
                return;
            }
            prev = current;
            current = current.next;

        }
    }


    public static class Node {
        int val;
        Node next;

        public Node(int val, Node next){
            this.val = val;
            this.next = next;
        }

        public int getVal() {
            return val;
        }

        public void setVal(int val) {
            this.val = val;
        }
    }

}

}

```

这是两个节点的LinkedList的实现10ms, 消耗内存44.57MB，看起来这个实现要比上面的实现要快一点点，但是还是不是特别快的。
看完官方题解后参考他的实现改addAtHead & addAtTail 都直接调用addAtIndex， 就不需要像上面一样都实现一遍了。

而且我个人的实现方式是显示的处理了很多的边界问题，并不优雅，希望在后续的刷题当中能优化这个问题。

我的实现中是没有在构造中声明head节点的，直接就是空的，而是在addAtIndex中实现了这个边界问题。

```java

// only head and size ,I didn't maintenance the tail node
    private Node head;
    private int size;

    public LinkedListMultiNodes() {

    }

    public int get(int index) {
        int result = -1;
        if (index > size || index < 0 || size == 0){
            return result;
        }
        Node current = head;
        for (int i = 0; i <= index; i++) {
            // once the index == size , the loop will be get the empty code,  so I need to check the current node is null or not
            if(current == null){
                return -1;
            }
            // get the real node value
            if(i == index){
                result = current.val;
                return result;
            }
            // move to next node
            current = current.next;
        }
        return result;
    }

    public void addAtHead(int val) {
        addAtIndex(0, val);
    }

    public void addAtTail(int val) {
        addAtIndex(size, val);
    }

    public void addAtIndex(int index, int val) {
        index = Math.max(0, index);
        if (index > size){
            return;
        }
        Node current = head;
        // handle the first note case
        if(0 == index){
            this.head = new Node(val);
            this.head.next = current;
            // nothing at all nodes in linked list
            if(current != null){
                current.prev = this.head;
            }
            size++;
            return;
        }
        for (int i = 0; i <= index; i++) {
            // handle the last node case
            if(index == size && i == index - 1){
                Node node = new Node(val);
                current.next = node;
                node.prev = current;
                size++;
                return;
            }
            if(current == null){
                return;
            }
            // handle the middle node case
            if(i == index){
                Node newNode = new Node(val);
                // must execute the assignment value to the new node otherwise the new node can't get the previous node of current node
                newNode.prev = current.prev;
                newNode.next = current;
                current.prev.next = newNode;
                current.prev = newNode;
            }
            current = current.next;
        }
        size++;
    }

    public void deleteAtIndex(int index) {
        if(index < 0 || index > size-1){
            return;
        }

        if(size <= 1 && index == 0){
            head = null;
            return;
        }

        Node current = head;
        // first node case
        if(index == 0){
            head = head.next;
            head.next.prev = null;
            size--;
            return;
        }

        for (int i = 0; i <= index ; i++) {
            // last node case
            if(index == i && index == size){
                current.prev.next = null;
            }
            // middle node case
            else if(index == i){
                current.prev.next = current.next;
                // handle the last node as well
                if(index != size - 1){
                    current.next.prev = current.prev;
                }
            }
            current = current.next;
        }
        size--;
    }

    public class Node {
        public int val;
        public Node prev;
        public Node next;

        // referred the code from leetcode official solution, they only set up the val
        public Node(int val) {
            this.val = val;
        }
    }

```