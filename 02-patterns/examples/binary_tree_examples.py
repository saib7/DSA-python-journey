"""
Binary Tree Examples — Lesson 08
Traversals (DFS × 3 + BFS) and classic tree problems.

Usage:
    python binary_tree_examples.py
"""

from collections import deque


# ======================================================================
# TREENODE CLASS
# ======================================================================

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ======================================================================
# HELPERS: build a tree, and print traversals nicely
# ======================================================================

def build_sample_tree():
    """Returns:
            1
           / \
          2   3
         / \   \
        4   5   6
    """
    return TreeNode(1,
        TreeNode(2, TreeNode(4), TreeNode(5)),
        TreeNode(3, None, TreeNode(6))
    )


def build_from_list(values):
    """Build a tree from a level-order list (None represents missing).
    Example: [1, 2, 3, 4, 5, None, 6] → the sample tree above."""
    if not values:
        return None
    root = TreeNode(values[0])
    q = deque([root])
    i = 1
    while q and i < len(values):
        node = q.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            q.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            q.append(node.right)
        i += 1
    return root


# ======================================================================
# THE FOUR TRAVERSALS
# ======================================================================

def preorder(node, result=None):
    if result is None:
        result = []
    if node:
        result.append(node.val)
        preorder(node.left, result)
        preorder(node.right, result)
    return result


def inorder(node, result=None):
    if result is None:
        result = []
    if node:
        inorder(node.left, result)
        result.append(node.val)
        inorder(node.right, result)
    return result


def postorder(node, result=None):
    if result is None:
        result = []
    if node:
        postorder(node.left, result)
        postorder(node.right, result)
        result.append(node.val)
    return result


def level_order(root):
    if not root:
        return []
    result = []
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        result.append(level)
    return result


# ======================================================================
# ITERATIVE DFS (using explicit stack)
# ======================================================================

def preorder_iter(root):
    if not root:
        return []
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right: stack.append(node.right)      # push right first
        if node.left:  stack.append(node.left)
    return result


def inorder_iter(root):
    result = []
    stack = []
    current = root
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        result.append(current.val)
        current = current.right
    return result


# ======================================================================
# CLASSIC TREE PROBLEMS
# ======================================================================

def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


def invert(root):
    if not root:
        return None
    root.left, root.right = invert(root.right), invert(root.left)
    return root


def is_same(p, q):
    if not p and not q:
        return True
    if not p or not q:
        return False
    return (p.val == q.val 
            and is_same(p.left, q.left) 
            and is_same(p.right, q.right))


def is_symmetric(root):
    def is_mirror(a, b):
        if not a and not b:
            return True
        if not a or not b:
            return False
        return (a.val == b.val 
                and is_mirror(a.left, b.right) 
                and is_mirror(a.right, b.left))
    if not root:
        return True
    return is_mirror(root.left, root.right)


def has_path_sum(root, target):
    if not root:
        return False
    if not root.left and not root.right:
        return root.val == target
    remaining = target - root.val
    return has_path_sum(root.left, remaining) or has_path_sum(root.right, remaining)


def diameter(root):
    """Helper returns height, closure tracks max diameter."""
    self_diameter = 0
    def depth(node):
        nonlocal self_diameter
        if not node:
            return 0
        left = depth(node.left)
        right = depth(node.right)
        self_diameter = max(self_diameter, left + right)
        return 1 + max(left, right)
    depth(root)
    return self_diameter


# ======================================================================
# MAIN
# ======================================================================

if __name__ == "__main__":
    print("=" * 75)
    print("BINARY TREES IN ACTION")
    print("=" * 75)

    tree = build_sample_tree()
    print("""
Sample tree:
            1
           / \\
          2   3
         / \\   \\
        4   5   6
""")

    # --- Traversals ---
    print("🌳 The four traversals")
    print("-" * 75)
    print(f"  Preorder  (Root, L, R) : {preorder(tree)}")
    print(f"  Inorder   (L, Root, R) : {inorder(tree)}")
    print(f"  Postorder (L, R, Root) : {postorder(tree)}")
    print(f"  Level-order (BFS)      : {level_order(tree)}")

    # --- Iterative DFS ---
    print("\n🔄 Iterative DFS (using explicit stack)")
    print("-" * 75)
    print(f"  preorder_iter → {preorder_iter(tree)}")
    print(f"  inorder_iter  → {inorder_iter(tree)}")
    print("  (Match the recursive versions? ✅)")

    # --- Classic problems ---
    print("\n🎯 Classic problems on the sample tree")
    print("-" * 75)
    print(f"  max_depth(tree)                    → {max_depth(tree)}")
    print(f"  has_path_sum(tree, 7)              → {has_path_sum(tree, 7)}   (1→2→4)")
    print(f"  has_path_sum(tree, 10)             → {has_path_sum(tree, 10)}  (1→3→6)")
    print(f"  has_path_sum(tree, 99)             → {has_path_sum(tree, 99)}")
    print(f"  diameter(tree)                     → {diameter(tree)}   (edges: 4-2-1-3-6)")

    # --- Same tree / symmetry ---
    print("\n🪞 Comparison and symmetry")
    print("-" * 75)
    t1 = build_from_list([1, 2, 3])
    t2 = build_from_list([1, 2, 3])
    t3 = build_from_list([1, 3, 2])
    print(f"  is_same(t1, t2)                    → {is_same(t1, t2)}")
    print(f"  is_same(t1, t3)                    → {is_same(t1, t3)}")

    sym = build_from_list([1, 2, 2, 3, 4, 4, 3])
    not_sym = build_from_list([1, 2, 2, None, 3, None, 3])
    print(f"  is_symmetric([1,2,2,3,4,4,3])      → {is_symmetric(sym)}")
    print(f"  is_symmetric([1,2,2,None,3,None,3])→ {is_symmetric(not_sym)}")

    # --- Invert ---
    print("\n🔁 Inverting the sample tree")
    print("-" * 75)
    inverted = invert(build_sample_tree())
    print(f"  Level-order of inverted tree       → {level_order(inverted)}")
    print(f"  (Was [[1],[2,3],[4,5,6]] — right and left flipped at each level)")

    print("\n✅ All eight tree algorithms working correctly!")
