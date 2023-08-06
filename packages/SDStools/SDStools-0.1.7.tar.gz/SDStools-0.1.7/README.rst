Senior Data Structure Tools–SDStools

python标准库中没有链表、树、图等高级数据结构，所以整理了一些网上的代码到这个库中。仅供学习。

linkedlist
''''''''''

-  LinkList ## 单向链表
-  SinCycLinkList ## 单向循环链表
-  TwoWayLinkList ## 双向链表

tree
''''

-  Binary Tree # 二叉树

Install & Usage:

::

   pip install SDStools

   from SDStools.linkedlist.LinkList import SingleLinkList
   from SDStools.linkedlist.LinkList import linklist

   ## SingleLinkList实现的方法如下
   is_empty()   # 链表是否为空
   length()     # 链表长度
   items()      # 遍历整个链表
   add(item)    # 链表头部添加元素
   append(item) # 链表尾部添加元素
   insert(index, item) # 指定位置添加元素
   remove(item) # 删除节点
   find(item)   # 查找节点是否存在
   clear()      # 清除链表数据

   ## linklist 实现列表转链表
   list_data = [1, 2, 3, 4]
   link_list = linklist(list_data)
   print(link_list)
   ## [(0, 1), (1, 2), (2, 3), (3, 4)]
