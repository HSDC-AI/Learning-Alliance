## ArrayList 的实现

要实现一个ArrayList，首先要明白ArrayList底层就是一个数组，重要的就是**考虑扩容/缩容**的问题（当数组当前长度等于size的变量，那么就给数组扩容2倍，使用系统的System.arraycopy 方法， 如果size小于数组长度的1/4，那么就缩容2倍），以及在**添加/删除element的时候index的位置，避免index越界**（这个时候就需要判断index是否大于size以及是否小于0），另一个就是**防止内存泄漏**（在remove element时，需要把最后一个index设置成null，这样data[size - 1]的内存就没有其它的对象在引用了，在可达性算法分析后，这个对象就会被回收掉，而不是一直在内存中占着空间）

```java
package ArrayAndLinked;

import java.util.NoSuchElementException;

/**
 * 注意事项
 * 1. 扩容/缩容问题
 * 2. 避免index越界 checkElementIndex() index < size and checkPositionIndex() index <= size
 * 3. 防止内存泄露
 *
 * [0, 1, 2, 3, 4, 5]
 * Array list 的本质其实就是数组，只要依据注意事项中的三个条件，就可以实现一个简单的ArrayList
 */
public class MyArrayList<E> {
    // storage the real data, the E means element
    private E[] data;
    private int size;
    private static final int DEFAULT_CAPACITY = 1;

    // init the array list as a new empty arrays
    public MyArrayList (int capacity) {
        data = (E[]) new Object[capacity];
        size = 0;
    }

    public MyArrayList () {
        this(DEFAULT_CAPACITY);
    }

    public int size () {
        return size;
    }

    public boolean isEmpty () {
        return size == 0;
    }

    public void addLast(E item){
        if(size == data.length){
            resize(size * 2);
        }

        // insert the element at the last index
        data[size] = item;
        size++;
    }

    public void add(int index, E item){

        checkPositionIndex(index);

        if(size == data.length){
            resize(size * 2);
        }
        // remove the currently elements to next and give a place for new element
        System.arraycopy(data, index, data, index+1, size - index);

        data[index] = item;
        size++;
    }

    public E removeLast(){

        if (size == 0){
            throw new NoSuchElementException("the list is empty");
        }

        // reduce the capacity when the size is less than 1/4
        if(size < data.length / 4){
            resize(data.length / 2);
        }

        E removedItem = data[size - 1];
        // set the last index as null in case of memory leak
        data[size - 1] = null;
        size--;
        return removedItem;
    }

    public E remove(int index){

        checkElementIndex(index);

        if(size < data.length / 4){
            resize(data.length / 2);
        }

        E removedItem = data[index];
        System.arraycopy(data, index+1, data, index, size - index - 1);
        data[size - 1] = null;
        size--;
        return removedItem;
    }

    private void checkElementIndex(int index){
        if(index > size || index < 0){
            throw new ArrayIndexOutOfBoundsException("the index exceeded the original size");
        }
    }

    private void checkPositionIndex(int index){
        if (index > size + 1 || index < 0){
            throw new ArrayIndexOutOfBoundsException("the index exceeded the original size");
        }
    }

    public void resize(int capacity){
        E[] newData = (E[]) new Object[capacity];
        System.arraycopy(data, 0, newData, 0, data.length);
        data = newData;
    }

    public static void main(String[] args) {
        MyArrayList<Integer> list = new MyArrayList<>();
        list.addLast(0);
        list.addLast(1);
        list.addLast(3);
        list.addLast(4);
        list.addLast(5);

        list.add(2,2);

        list.removeLast();

        list.remove(3);

    }
}



```