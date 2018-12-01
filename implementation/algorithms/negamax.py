import tree
import chess

def call_get_value_by_key_for_child(root,key):
    for k in root.children.keys():
        get_value_by_key(root.children[k], key)

result=0
def get_value_by_key(root,key):
    global result
    for child in root.parent.children:
        if root==root.parent.children[child] and child==key:
            result=root.value
            return result
    if key in root.children.keys():
        result=root.children[key].value
        return result
    for k in root.children.keys():
        get_value_by_key(root.children[k], key)
    return result

MIN=-9999999
# score=0
max=MIN
def negamax(root,depth,key=MIN):
    global MIN
    # global max
    max=MIN
    global result
    if depth==0:
        result=0
        return get_value_by_key(root,key)
    else:
        max=MIN
        for k in root.children.keys():
            depth-=1
            result=negamax(root.children[k],depth,k)
            score=(-1)*result
            depth+=1
            if score>max:
                max=score
        return max


if __name__=='__main__':
    root = tree.TreeNode()
    #first test
    # root.children['move_1']=tree.TreeNode(parent= root, value=10)
    # root.children['move_2']=tree.TreeNode(parent= root, value=4)
    # root.children['move_1'].children['move_1_1']=tree.TreeNode(parent= root.children['move_1'], value=-20)
    # root.children['move_1'].children['move_1_2']=tree.TreeNode(parent= root.children['move_1'], value=-15)
    # root.children['move_2'].children['move_2_1']=tree.TreeNode(parent= root.children['move_2'], value=-2)
    # root.children['move_2'].children['move_2_2']=tree.TreeNode(parent= root.children['move_2'], value=-14)
    # root.children['move_1'].children['move_1_1'].children['move_1_1_1']=tree.TreeNode(parent= root.children['move_1'].children['move_1_1'], value=20)
    # root.children['move_1'].children['move_1_1'].children['move_1_1_2']=tree.TreeNode(parent= root.children['move_1'].children['move_1_1'], value=2)
    # root.children['move_1'].children['move_1_2'].children['move_1_2_1']=tree.TreeNode(parent= root.children['move_1'].children['move_1_2'], value=6)
    # root.children['move_1'].children['move_1_2'].children['move_1_2_2']=tree.TreeNode(parent= root.children['move_1'].children['move_1_2'], value=8)
    # root.children['move_2'].children['move_2_1'].children['move_2_1_1']=tree.TreeNode(parent= root.children['move_2'].children['move_2_1'], value=12)
    # root.children['move_2'].children['move_2_1'].children['move_2_1_2']=tree.TreeNode(parent= root.children['move_2'].children['move_2_1'], value=7)
    # root.children['move_2'].children['move_2_2'].children['move_2_2_1']=tree.TreeNode(parent= root.children['move_2'].children['move_2_2'], value=-10)
    # root.children['move_2'].children['move_2_2'].children['move_2_2_2']=tree.TreeNode(parent= root.children['move_2'].children['move_2_2'], value=-3)

    #second test
    root.value=4
    root.children['move_1']=tree.TreeNode(parent= root, value=4)
    root.children['move_2']=tree.TreeNode(parent= root, value=2)

    root.children['move_1'].children['move_1_1']=tree.TreeNode(parent= root.children['move_1'], value=4)
    root.children['move_1'].children['move_1_2']=tree.TreeNode(parent= root.children['move_1'], value=8)
    root.children['move_2'].children['move_2_1']=tree.TreeNode(parent= root.children['move_2'], value=2)
    root.children['move_2'].children['move_2_2']=tree.TreeNode(parent= root.children['move_2'], value=14)

    root.children['move_1'].children['move_1_1'].children['move_1_1_1']=tree.TreeNode(parent= root.children['move_1'].children['move_1_1'], value=4)
    root.children['move_1'].children['move_1_1'].children['move_1_1_2']=tree.TreeNode(parent= root.children['move_1'].children['move_1_1'], value=2)
    root.children['move_1'].children['move_1_2'].children['move_1_2_1']=tree.TreeNode(parent= root.children['move_1'].children['move_1_2'], value=6)
    root.children['move_1'].children['move_1_2'].children['move_1_2_2']=tree.TreeNode(parent= root.children['move_1'].children['move_1_2'], value=8)

    root.children['move_2'].children['move_2_1'].children['move_2_1_1']=tree.TreeNode(parent= root.children['move_2'].children['move_2_1'], value=1)
    root.children['move_2'].children['move_2_1'].children['move_2_1_2']=tree.TreeNode(parent= root.children['move_2'].children['move_2_1'], value=2)
    root.children['move_2'].children['move_2_2'].children['move_2_2_1']=tree.TreeNode(parent= root.children['move_2'].children['move_2_2'], value=12)
    root.children['move_2'].children['move_2_2'].children['move_2_2_2']=tree.TreeNode(parent= root.children['move_2'].children['move_2_2'], value=14)

    root.children['move_1'].children['move_1_1'].children['move_1_1_1'].children['move_1_1_1_1']=tree.TreeNode(parent= root.children['move_1'].children['move_1_1'].children['move_1_1_1'], value=4)
    root.children['move_1'].children['move_1_1'].children['move_1_1_1'].children['move_1_1_1_2']=tree.TreeNode(parent= root.children['move_1'].children['move_1_1'].children['move_1_1_1'], value=5)
    root.children['move_1'].children['move_1_1'].children['move_1_1_2'].children['move_1_1_2_1']=tree.TreeNode(parent= root.children['move_1'].children['move_1_1'].children['move_1_1_2'], value=3)
    root.children['move_1'].children['move_1_1'].children['move_1_1_2'].children['move_1_1_2_2']=tree.TreeNode(parent= root.children['move_1'].children['move_1_1'].children['move_1_1_2'], value=2)

    root.children['move_1'].children['move_1_2'].children['move_1_2_1'].children['move_1_2_1_1']=tree.TreeNode(parent= root.children['move_1'].children['move_1_2'].children['move_1_2_1'], value=6)
    root.children['move_1'].children['move_1_2'].children['move_1_2_1'].children['move_1_2_1_2']=tree.TreeNode(parent= root.children['move_1'].children['move_1_2'].children['move_1_2_1'], value=7)
    root.children['move_1'].children['move_1_2'].children['move_1_2_2'].children['move_1_2_2_1']=tree.TreeNode(parent= root.children['move_1'].children['move_1_2'].children['move_1_2_2'], value=8)
    root.children['move_1'].children['move_1_2'].children['move_1_2_2'].children['move_1_2_2_2']=tree.TreeNode(parent= root.children['move_1'].children['move_1_2'].children['move_1_2_2'], value=9)

    root.children['move_2'].children['move_2_1'].children['move_2_1_1'].children['move_2_1_1_1']=tree.TreeNode(parent= root.children['move_2'].children['move_2_1'].children['move_2_1_1'], value=1)
    root.children['move_2'].children['move_2_1'].children['move_2_1_1'].children['move_2_1_1_2']=tree.TreeNode(parent= root.children['move_2'].children['move_2_1'].children['move_2_1_1'], value=10)
    root.children['move_2'].children['move_2_1'].children['move_2_1_2'].children['move_2_1_2_1']=tree.TreeNode(parent= root.children['move_2'].children['move_2_1'].children['move_2_1_2'], value=2)
    root.children['move_2'].children['move_2_1'].children['move_2_1_2'].children['move_2_1_2_2']=tree.TreeNode(parent= root.children['move_2'].children['move_2_1'].children['move_2_1_2'], value=11)

    root.children['move_2'].children['move_2_2'].children['move_2_2_1'].children['move_2_2_1_1']=tree.TreeNode(parent= root.children['move_2'].children['move_2_2'].children['move_2_2_1'], value=12)
    root.children['move_2'].children['move_2_2'].children['move_2_2_1'].children['move_2_2_1_2']=tree.TreeNode(parent= root.children['move_2'].children['move_2_2'].children['move_2_2_1'], value=13)
    root.children['move_2'].children['move_2_2'].children['move_2_2_2'].children['move_2_2_2_1']=tree.TreeNode(parent= root.children['move_2'].children['move_2_2'].children['move_2_2_2'], value=14)
    root.children['move_2'].children['move_2_2'].children['move_2_2_2'].children['move_2_2_2_2']=tree.TreeNode(parent= root.children['move_2'].children['move_2_2'].children['move_2_2_2'], value=14)

    print(negamax(root,4))
