# 📘 08 · Binary Trees & Traversals

> **Goal:** Master the four essential traversals (preorder/inorder/postorder DFS + level-order BFS) and the recursion pattern that solves almost every tree problem.

---

## ⚡ Quick Recap (read this for fast revision)

- `TreeNode` = `val` + `left` + `right`
- **Four traversals:**
  - **Preorder** (Root → L → R) — process BEFORE recursing
  - **Inorder** (L → Root → R) — for BST gives **sorted order**
  - **Postorder** (L → R → Root) — process AFTER recursing (deletion, LCA)
  - **Level-order** (BFS with `deque`) — level-by-level using `for _ in range(len(q))` trick
- **Core recursion pattern:** base case → recurse L & R → combine
- **Recursive** = O(n) time, O(h) space (call stack)
- **Iterative DFS** = use explicit stack (push RIGHT first for preorder)
- **Diameter/path-through-node pattern:** helper returns height, closure tracks answer

---

## 1. The `TreeNode` class

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

### Terminology

| Term         | Meaning                                                  |
| ------------ | -------------------------------------------------------- |
| **Root**     | Top node, no parent                                      |
| **Leaf**     | Node with no children                                    |
| **Height**   | Longest path from root to any leaf (in edges)            |
| **Depth**    | Distance from root to a given node                       |
| **Balanced** | Height diff between subtrees ≤ 1 everywhere              |

---

## 2. The four essential traversals

### DFS — same structure, only the process-step moves

**Preorder (Root, L, R)**
```python
def preorder(node, result):
    if not node:
        return
    result.append(node.val)       # ← BEFORE recursing
    preorder(node.left, result)
    preorder(node.right, result)
```

**Inorder (L, Root, R)** — for BST gives **sorted order** ✨
```python
def inorder(node, result):
    if not node:
        return
    inorder(node.left, result)
    result.append(node.val)       # ← BETWEEN recurses
    inorder(node.right, result)
```

**Postorder (L, R, Root)** — deletion, LCA
```python
def postorder(node, result):
    if not node:
        return
    postorder(node.left, result)
    postorder(node.right, result)
    result.append(node.val)       # ← AFTER recursing
```

### Level-order (BFS)

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    result = []
    q = deque([root])
    while q:
        level = []
        for _ in range(len(q)):    # ⚠️ snapshot level size!
            node = q.popleft()
            level.append(node.val)
            if node.left:  q.append(node.left)
            if node.right: q.append(node.right)
        result.append(level)
    return result
```

**Critical:** `for _ in range(len(q))` snapshots the level's size — without it you get a flat list.

### Example outputs for a sample tree

```
        1
       / \
      2   3
     / \   \
    4   5   6
```

- Preorder:   `[1, 2, 4, 5, 3, 6]`
- Inorder:    `[4, 2, 5, 1, 3, 6]`
- Postorder:  `[4, 5, 2, 6, 3, 1]`
- Level-order: `[[1], [2, 3], [4, 5, 6]]`

---

## 3. The core tree-recursion pattern

Almost every tree problem follows this shape:

```python
def solve(node):
    # 1. Base case
    if not node:
        return base_value
    
    # 2. Recurse on children (leap of faith)
    left_result = solve(node.left)
    right_result = solve(node.right)
    
    # 3. Combine with current node's value
    return combine(node.val, left_result, right_result)
```

### Examples using the pattern

```python
# Max Depth
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# Same Tree
def is_same(p, q):
    if not p and not q:
        return True
    if not p or not q:
        return False
    return (p.val == q.val 
            and is_same(p.left, q.left) 
            and is_same(p.right, q.right))

# Invert Binary Tree
def invert(root):
    if not root:
        return None
    root.left, root.right = invert(root.right), invert(root.left)
    return root
```

---

## 4. The helper-returns-one, closure-tracks-another pattern

Some tree problems need to **compute one quantity to return upward** while **tracking a different quantity globally**.

### Diameter of Binary Tree

```python
def diameter(root):
    self_diameter = 0
    
    def depth(node):
        nonlocal self_diameter
        if not node:
            return 0
        left = depth(node.left)
        right = depth(node.right)
        self_diameter = max(self_diameter, left + right)   # update globally
        return 1 + max(left, right)                        # return height upward
    
    depth(root)
    return self_diameter
```

**Why:** the parent needs child's **height** to compute its own; the **diameter** at each node is `left_height + right_height`. Two different quantities — return one, track the other.

This pattern appears in many medium tree problems: **max path sum, balanced check, LCA**, etc.

---

## 5. Iterative traversals (using explicit stack/queue)

### Iterative preorder — stack

```python
def preorder_iter(root):
    if not root:
        return []
    result = []
    stack = [root]
    while stack:
        node = stack.pop()
        result.append(node.val)
        # Push RIGHT first so LEFT is popped first (LIFO)
        if node.right: stack.append(node.right)
        if node.left:  stack.append(node.left)
    return result
```

### Iterative inorder — walk left first

```python
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
```

**Key insight:** recursion IS a stack — iterative DFS just makes it explicit.

---

## 6. Recognition signals

| Phrase in problem                             | Approach                        |
| --------------------------------------------- | ------------------------------- |
| "depth" / "height" / "path from root"         | DFS + recursion pattern         |
| "level order" / "by level" / "left/right view"| BFS (queue)                     |
| "path sum" / "root-to-leaf"                   | DFS with running sum            |
| "sorted order from BST"                       | **Inorder** traversal           |
| "compare two trees"                           | Simultaneous DFS on both        |
| "invert / mirror"                             | Recursive swap                  |
| "diameter" / "longest path"                   | Helper returns height, closure tracks answer |
| "serialize / deserialize"                     | Preorder/level-order with markers |
| "lowest common ancestor"                      | Postorder recursion             |

---

## 7. Common pitfalls

| Pitfall                                            | Why it bites                                    |
| -------------------------------------------------- | ----------------------------------------------- |
| Forgetting base case `if not node: return`         | `AttributeError` on `None.left`                 |
| Not snapshotting `len(q)` in level-order BFS       | Levels blur into a flat list                    |
| Confusing depth vs diameter                        | Return one, track the other                     |
| Iterative preorder: pushing left first             | Get right subtree first (wrong order)           |
| Recursion on very deep/skewed tree (>1000)         | Hits Python's recursion limit                   |
| Modifying tree during traversal                    | Iterator invalidation / bugs                    |

---

## 8. Practice problems

```python
# 1. Maximum Depth (LC 104, Easy)
def max_depth(root):
    ...

# 2. Invert Binary Tree (LC 226, Easy)
def invert(root):
    ...

# 3. Same Tree (LC 100, Easy)
def is_same(p, q):
    ...

# 4. Symmetric Tree (LC 101, Easy) — mirror check
def is_symmetric(root):
    ...

# 5. Binary Tree Level Order Traversal (LC 102, Medium)
def level_order(root):
    ...

# 6. Path Sum (LC 112, Easy) — root-to-leaf sum = target?
def has_path_sum(root, target):
    ...

# 7. Diameter of Binary Tree (LC 543)
def diameter(root):
    ...
```

<details>
<summary>📋 Click to reveal solutions</summary>

```python
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# 1. Max Depth
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


# 2. Invert
def invert(root):
    if not root:
        return None
    root.left, root.right = invert(root.right), invert(root.left)
    return root


# 3. Same Tree
def is_same(p, q):
    if not p and not q:
        return True
    if not p or not q:
        return False
    return (p.val == q.val 
            and is_same(p.left, q.left) 
            and is_same(p.right, q.right))


# 4. Symmetric — compare left and right subtrees as mirrors
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


# 5. Level Order — the BFS template
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


# 6. Path Sum — subtract target as we go down; check at leaves
def has_path_sum(root, target):
    if not root:
        return False
    if not root.left and not root.right:              # leaf
        return root.val == target
    remaining = target - root.val
    return has_path_sum(root.left, remaining) or has_path_sum(root.right, remaining)


# 7. Diameter — helper returns height, closure tracks max diameter
def diameter(root):
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
```

**Complexity for all:** O(n) time, O(h) space where h is tree height (call stack). Balanced tree: h = log n. Skewed tree: h = n.

</details>

---

## 9. 🎯 Must-Memorize

- `TreeNode` = `val` + `left` + `right`. That's the whole data structure.
- **Preorder/Inorder/Postorder** differ only in **where** you place the process step
- **Inorder on BST** gives **sorted order** — one of the most useful facts in interviews
- **Level-order BFS** uses `deque` + `for _ in range(len(q))` for per-level grouping
- **Core recursion pattern:** base case → recurse L & R → combine
- **Helper-returns-one, closure-tracks-another** for diameter / max-path-sum / balanced-check
- Space complexity is **O(h)** for recursive tree code (call stack)

---

## 🔗 Related
- 🔬 Runnable demo: [`examples/binary_tree_examples.py`](./examples/binary_tree_examples.py)
- ⏮️ Previous: [Stacks & Queues](../02-linear-structures/05-stacks-queues.md)
- ⏭️ Next: Binary Search Trees *(coming)*
