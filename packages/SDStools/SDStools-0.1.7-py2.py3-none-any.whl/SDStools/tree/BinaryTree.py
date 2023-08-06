class Node(object):
    """节点类"""
    def __init__(self, val=-1, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class BinaryTree(object):
    """树类"""
    def __init__(self, root=None):
        self.root = root

    def add(self, elem):
        """为树添加节点"""
        node = Node(elem)
        #如果树是空的，则对根节点赋值
        if self.root == None:
            self.root = node
        else:
            queue = []
            queue.append(self.root)
            #对已有的节点进行层次遍历
            while queue:
                #弹出队列的第一个元素
                cur = queue.pop(0)
                if cur.left == None:
                    cur.left = node
                    return
                elif cur.right == None:
                    cur.right = node
                    return
                else:
                    #如果左右子树都不为空，加入队列继续判断
                    queue.append(cur.left)
                    queue.append(cur.right)
                    

# 层次遍历（广度优先）
def BFS(root):
    res = []
    if root:
        queue = [root]
        while queue:
            currentNode = queue.pop(0)
            res.append(currentNode.val)
            if currentNode.left:
                queue.append(currentNode.left)
            if currentNode.right:
                queue.append(currentNode.right)
    return res


# 深度优先
def DFS(root):
    res = []
    if root:
        stack = [root]
        while stack:
            currentNode = stack.pop()
            res.append(currentNode.val)
            if currentNode.right:
                stack.append(currentNode.right)
            if currentNode.left:
                stack.append(currentNode.left)
    return res

if __name__ == "__main__":
    tree = BinaryTree()
    for i in range(1,10):
        tree.add(i)

    print(DFS(tree.root))