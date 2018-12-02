class TreeNode:

    def __init__(self,
                 parent = None,
                 value = None,
                 children = None,
                 board = None):

        self.parent = parent
        self.value = value
        self.board = board

        if isinstance(children, dict):
            self.children = children
        else:
            self.children = {}


if __name__ == '__main__':

    root = TreeNode(value=2)
    root.children['move_1'] = TreeNode(parent= root, value=5)
    root.children['move_2'] = TreeNode(parent= root, value= 5)
    root.children['move_1'].children['move_1'] = TreeNode(parent= root.children['move_1'], value=10)

    print(root)
    print(root.children)
    print(root.children['move_1'].children)
