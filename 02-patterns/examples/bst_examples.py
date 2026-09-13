"""
Binary Search Tree Examples — Lesson 09
Core BST operations, validation, and classic problems.

Usage:
    python bst_examples.py
"""

from collections import deque


# ======================================================================
# TREENODE
# ======================================================================

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ======================================================================
# CORE BST OPERATIONS
# ======================================================================

def insert(root, val):
    """Insert val, ignoring duplicates. Returns (possibly new) root."""
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    elif val > root.val:
        root.right = insert(root.right, val)
    return root


def search(root, target):
    """Iterative search. Returns node or None."""
    while root:
        if root.val == target:
            return root
        root = root.left if target < root.val else root.right
    return None


def delete(root, val):
    """Delete val from tree. Returns (possibly new) root."""
    if not root:
        return None
    if val < root.val:
        root.left = delete(root.left, val)
    elif val > root.val:
        root.right = delete(root.right, val)
    else:                                    # found the node
        if not root.left:  return root.right
        if not root.right: return root.left
        # Two children: find inorder successor
        successor = root.right
        while successor.left:
            successor = successor.left
        root.val = successor.val
        root.right = delete(root.right, successor.val)
    return root


# ======================================================================
# TRAVERSALS
# ======================================================================

def inorder(root):
    """Iterative inorder — for a BST, this returns sorted values."""
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
# VALIDATION — the classic pitfall
# ======================================================================

def is_valid_bst_wrong(root):
    """⚠️ WRONG: only checks immediate children."""
    if not root:
        return True
    if root.left and root.left.val >= root.val:
        return False
    if root.right and root.right.val <= root.val:
        return False
    return is_valid_bst_wrong(root.left) and is_valid_bst_wrong(root.right)


def is_valid_bst(root):
    """✅ CORRECT: pass min/max bounds down the recursion."""
    def validate(node, min_val, max_val):
        if not node:
            return True
        if node.val <= min_val or node.val >= max_val:
            return False
        return (validate(node.left, min_val, node.val)
                and validate(node.right, node.val, max_val))
    return validate(root, float('-inf'), float('inf'))


# ======================================================================
# CLASSIC BST PROBLEMS
# ======================================================================

def kth_smallest(root, k):
    """Iterative inorder with early stop. O(h + k)."""
    stack = []
    current = root
    while current or stack:
        while current:
            stack.append(current)
            current = current.left
        current = stack.pop()
        k -= 1
        if k == 0:
            return current.val
        current = current.right


def lca_bst(root, p_val, q_val):
    """LCA using BST invariant. O(log n) if balanced."""
    while root:
        if p_val < root.val and q_val < root.val:
            root = root.left
        elif p_val > root.val and q_val > root.val:
            root = root.right
        else:
            return root


def sorted_array_to_bst(nums):
    """Middle → root, recurse on halves. Guaranteed balanced."""
    if not nums:
        return None
    mid = len(nums) // 2
    return TreeNode(
        nums[mid],
        sorted_array_to_bst(nums[:mid]),
        sorted_array_to_bst(nums[mid + 1:])
    )


# ======================================================================
# BUILD A BST FROM A LIST OF VALUES
# ======================================================================

def build_bst(values):
    root = None
    for v in values:
        root = insert(root, v)
    return root


# ======================================================================
# MAIN
# ======================================================================

if __name__ == "__main__":
    print("=" * 75)
    print("BINARY SEARCH TREES IN ACTION")
    print("=" * 75)

    # --- Build a BST ---
    print("\n🌱 Building BST from [8, 3, 10, 1, 6, 14, 4, 7, 13]")
    print("-" * 75)
    bst = build_bst([8, 3, 10, 1, 6, 14, 4, 7, 13])
    print(f"  Level-order:    {level_order(bst)}")
    print(f"  Inorder (sorted!): {inorder(bst)}")

    # --- Search ---
    print("\n🔍 Search")
    print("-" * 75)
    for target in [7, 100]:
        found = search(bst, target)
        print(f"  search({target})  → {'found' if found else 'not found'}")

    # --- Delete demonstrations ---
    print("\n✂️  Delete demonstrations")
    print("-" * 75)
    for target in [1, 10, 3]:                # leaf, one-child, two-children
        tree_copy = build_bst([8, 3, 10, 1, 6, 14, 4, 7, 13])
        tree_copy = delete(tree_copy, target)
        print(f"  Delete {target:>2}: inorder = {inorder(tree_copy)}")

    # --- Validation — the classic pitfall ---
    print("\n🚨 Validation: the classic pitfall")
    print("-" * 75)
    # A tree that looks valid but ISN'T (6 is in 10's right subtree, must be > 10)
    #        10
    #       /  \
    #      5    15
    #          /  \
    #         6    20
    tricky = TreeNode(10,
        TreeNode(5),
        TreeNode(15, TreeNode(6), TreeNode(20))
    )
    print(f"  is_valid_bst_WRONG(tricky) = {is_valid_bst_wrong(tricky)}   ← misses the bug!")
    print(f"  is_valid_bst(tricky)       = {is_valid_bst(tricky)}   ← catches it ✅")
    print(f"  is_valid_bst(good_bst)     = {is_valid_bst(bst)}    ← correctly True ✅")

    # --- Kth smallest ---
    print("\n🥇 K-th smallest")
    print("-" * 75)
    for k in [1, 3, 5, 9]:
        print(f"  kth_smallest(bst, k={k}) = {kth_smallest(bst, k)}")

    # --- LCA ---
    print("\n👨‍👩‍👦 Lowest Common Ancestor (BST version — O(log n))")
    print("-" * 75)
    for p, q in [(1, 7), (4, 13), (10, 14)]:
        print(f"  lca_bst({p}, {q}) = {lca_bst(bst, p, q).val}")

    # --- Sorted array to balanced BST ---
    print("\n⚖️  Convert sorted array [1..7] to balanced BST")
    print("-" * 75)
    balanced = sorted_array_to_bst([1, 2, 3, 4, 5, 6, 7])
    print(f"  Level-order: {level_order(balanced)}")
    print(f"  Inorder:     {inorder(balanced)}")
    print(f"  is_valid_bst: {is_valid_bst(balanced)}")

    # --- The dark side: skewed BST ---
    print("\n⚠️  The dark side: inserting sorted values → skewed BST")
    print("-" * 75)
    skewed = build_bst([1, 2, 3, 4, 5])
    print(f"  Level-order: {level_order(skewed)}")
    print(f"  This is basically a linked list — search is O(n), not O(log n)")
    print(f"  Balanced version instead: {level_order(sorted_array_to_bst([1, 2, 3, 4, 5]))}")

    print("\n✅ All BST operations working correctly!")
