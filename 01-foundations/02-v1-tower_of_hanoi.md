# 🗼 The Tower of Hanoi — Explained the Easy Way

![Topic](https://img.shields.io/badge/topic-recursion-blueviolet?style=flat-square) ![Level](https://img.shields.io/badge/level-beginner-brightgreen?style=flat-square) ![Language](https://img.shields.io/badge/code-python-3776AB?style=flat-square&logo=python&logoColor=white) ![Read time](https://img.shields.io/badge/read_time-~15_min-orange?style=flat-square)

A simple, step-by-step guide to the Tower of Hanoi puzzle. No math background needed — just read from top to bottom and it'll make sense.

> [!TIP]
> New to recursion? Don't skip ahead — Section 4 is the heart of this whole guide. Everything after it just builds on that one idea.

## 📖 What's in this guide

| # | Section | What you'll learn |
|:---:|---|---|
| 1 | [What is the Tower of Hanoi?](#1-what-is-the-tower-of-hanoi-) | The puzzle setup |
| 2 | [The rules](#2-the-rules-) | The only two rules you need |
| 3 | [What it looks like](#3-what-it-looks-like-️) | A visual before/after |
| 4 | [The big idea that solves it](#4-the-big-idea-that-solves-it-) | 💡 Recursion, explained simply |
| 5 | [A full example with 3 disks](#5-a-full-example-with-3-disks-) | Every move, traced step by step |
| 6 | [The math: how many moves?](#6-the-math-how-many-moves-do-you-need-) | Deriving `2ⁿ − 1` |
| 7 | [How slow can this get?](#7-how-slow-can-this-get-) | Exponential growth, felt |
| 8 | [The Python code](#8-the-python-code-) | A working solution |
| 9 | [Quick recap](#9-quick-recap-) | The whole guide in 5 lines |

---

## 1. What is the Tower of Hanoi? 🧩

Picture three poles standing side by side. Call them **A**, **B**, and **C**.

On pole A, there's a stack of disks. The disks are all different sizes, stacked like a little pyramid: the biggest disk on the bottom, then smaller and smaller ones going up, with the smallest disk sitting right on top.

Your job is to move the whole stack from pole A over to pole C. Pole B is there for you to use as a "parking spot" while you work.

That's the entire puzzle.

## 2. The rules ⚖️

There are only two rules, and they're easy to remember:

- 🔢 **Move one disk at a time.** You can never pick up more than one disk at once.
- 🚫 **Never put a big disk on a smaller disk.** A disk can only be placed on top of a bigger disk, or on an empty pole.

That's it. Simple rules — but they force a very specific pattern of moves, and that pattern is what makes this puzzle famous.

## 3. What it looks like 🖼️

Here's a picture of the start and the end, using 3 disks. Disk 1 is the smallest, disk 3 is the biggest.

**Before you start — everything is on pole A:**

```
    A          B          C
    ███       |          |
   █████      |          |
  ███████     |          |
═══════════════════════════════
    A          B          C
```

**After you finish — everything is on pole C:**

```
    A          B          C
    |          |          ███
    |          |         █████
    |          |        ███████
═══════════════════════════════
    A          B          C
```

> [!NOTE]
> Notice that the small disk is always on top and the big disk is always on the bottom — that's true at the start, at the end, and at every single moment in between. If you ever see a big disk sitting above a small one, something's gone wrong.

## 4. The big idea that solves it 💡

Here's the trick that makes this puzzle easy, once you see it.

Say you have 3 disks and you don't know how to move all of them at once. But imagine you had a helper who already knows how to move a *smaller* stack — just 2 disks — from any pole to any other pole. If you had that helper, here's what you'd do:

1. Ask your helper to move the top 2 disks from pole A to pole B. Now pole A has only the biggest disk left, sitting all by itself.
2. Move that one biggest disk yourself, straight from pole A to pole C. This is always allowed — it's the biggest disk around, so nothing is too small for it to land on.
3. Ask your helper again, this time to move those 2 disks from pole B over to pole C, right on top of the big disk you just placed.

✅ Done. All 3 disks are now on pole C, in the right order.

Here's the fun part: your "helper" isn't a separate person. It's just you, doing the exact same three steps, but on a smaller pile. If that smaller pile still has more than 1 disk, you call on an even smaller helper — yourself again, moving an even tinier pile. This keeps shrinking, smaller and smaller, until someone only has 1 disk left to move — and moving 1 disk needs no help at all, you just do it directly.

> [!IMPORTANT]
> This idea — where a job calls a smaller copy of itself, again and again, until the job is so small there's nothing left to do — is called **recursion**. It's one of the most useful ideas in computer science, and Tower of Hanoi is one of the easiest ways to actually see it working.

Written out simply, to move `n` disks from a **start** pole to a **finish** pole, using a spare pole as a **helper**, you always do the same three things:

1. 📤 Move the top `n - 1` disks from start to helper.
2. 🪨 Move the one disk left behind (the biggest one) from start to finish.
3. 📥 Move the `n - 1` disks from helper to finish.

## 5. A full example with 3 disks 🔍

Let's watch this play out with 3 disks, moving everything from pole A to pole C, using pole B as the helper.

The table below shows what's sitting on each pole after every move. Disks are listed bottom to top, so `[3, 2, 1]` means disk 3 is on the bottom, disk 2 is in the middle, and disk 1 is on top.

| Move | Disk moved | From → To | Peg A | Peg B | Peg C |
|:---:|:---:|:---:|:---:|:---:|:---:|
| start | — | — | [3, 2, 1] | [] | [] |
| 1 | 1 | A → C | [3, 2] | [] | [1] |
| 2 | 2 | A → B | [3] | [2] | [1] |
| 3 | 1 | C → B | [3] | [2, 1] | [] |
| 4 | 3 | A → C | [] | [2, 1] | [3] |
| 5 | 1 | B → A | [1] | [2] | [3] |
| 6 | 2 | B → C | [1] | [] | [3, 2] |
| 7 | 1 | A → C | [] | [] | [3, 2, 1] |

A couple things worth noticing:

- 🔁 Disk 1 (the smallest) moves on moves 1, 3, 5, and 7 — every other move. Makes sense, since it's the only disk small enough to hop around freely while the bigger disks sit and wait.
- 🧱 The whole sequence has a clear shape: moves 1–3 clear the two small disks out of the way, move 4 relocates the big disk, and moves 5–7 put the two small disks back on top of it. That's exactly the three-step idea from Section 4, just written out in full.

## 6. The math: how many moves do you need? 🧮

Let's figure out, without guessing, exactly how many moves this puzzle needs for any number of disks.

Call the number of moves needed for `n` disks `T(n)` — just a short way of writing "the number of moves for n disks."

If there are 0 disks, you need 0 moves. Obvious enough: `T(0) = 0`.

Now think back to the three-step idea. To move `n` disks, you:
- move `n - 1` disks out of the way (that takes `T(n-1)` moves),
- move 1 disk (the big one),
- then move those same `n - 1` disks back on top (another `T(n-1)` moves).

Add it up:

```
T(n) = T(n-1) + 1 + T(n-1) = 2 × T(n-1) + 1
```

This kind of rule — where something is defined using a smaller version of itself — is called a **recurrence**. It matches the algorithm exactly, which makes sense since we built it directly from the three steps.

Let's use this rule to build a table by hand, starting from `T(0) = 0`:

| n | Rule: 2 × T(n-1) + 1 | Moves needed |
|:---:|:---:|:---:|
| 0 | — | 0 |
| 1 | 2×0 + 1 | 1 |
| 2 | 2×1 + 1 | 3 |
| 3 | 2×3 + 1 | 7 |
| 4 | 2×7 + 1 | 15 |
| 5 | 2×15 + 1 | 31 |

See the pattern? 0, 1, 3, 7, 15, 31 — each number is just "double the last one, plus one." Here's the neat part: every one of these is exactly 1 less than a power of 2:

```
1  = 2¹ − 1
3  = 2² − 1
7  = 2³ − 1
15 = 2⁴ − 1
31 = 2⁵ − 1
```

So in general:

```
T(n) = 2ⁿ − 1
```

> [!TIP]
> **Why does this always hold?** Here's the plain-words version of the proof. We already know it's true for `n = 0`, since `2⁰ − 1 = 0`. Now, if it's true for `n - 1` disks, then plugging `2^(n-1) − 1` into our rule `T(n) = 2 × T(n-1) + 1` gives `2 × (2^(n-1) − 1) + 1`, which simplifies down to `2ⁿ − 2 + 1`, which is `2ⁿ − 1`. So if the formula works at one size, it automatically works for the next size up — and since it works at 0, it keeps working for every size after that, forever. This style of proof is called **induction**: check that the first domino falls, then check that every domino knocks over the next one.

## 7. How slow can this get? 🐌

The formula `2ⁿ − 1` doesn't look scary at first glance, but it grows incredibly fast. Look at this table:

| Disks | Moves needed |
|:---:|---:|
| 1 | 1 |
| 3 | 7 |
| 5 | 31 |
| 10 | 1,023 |
| 20 | 1,048,575 |
| 64 | 18,446,744,073,709,551,615 |

Going from 10 disks to 20 disks doesn't double the work — it multiplies it by over a thousand. This kind of growth is called **exponential growth**, and it's exactly why programmers get nervous whenever a `2ⁿ` shows up in their code.

> [!WARNING]
> There's a famous legend attached to this: somewhere, monks are supposedly moving 64 golden disks, one move every second, without stopping. Even at that pace, finishing would take about **585 billion years** — far longer than the universe has even existed (about 13.8 billion years). It's a great way to actually *feel* how big "exponential" really is, instead of just reading the words.

In computer science terms, we'd say solving this puzzle takes **O(2ⁿ) time** — meaning the work needed grows exponentially as the number of disks (`n`) goes up. That's about as slow as it gets. The good news: this really is the best possible solution. There's no shortcut, because the puzzle genuinely can't be solved in fewer than `2ⁿ − 1` moves.

There's also a much smaller number worth knowing: **O(n) space**. This just means that while the program runs, it only needs to keep track of about `n` things at once — roughly one for each disk waiting its turn — not `2ⁿ` things. So even though the puzzle takes ages to finish for large `n`, it barely uses any memory to solve.

## 8. The Python code 🐍

Here's a working Python program that solves the puzzle and prints out every move.

```python
def hanoi(n, source, destination, helper):
    # Base case: no disks left to move, so there's nothing to do.
    if n == 0:
        return

    # Step 1: move the top n-1 disks out of the way, onto the helper pole.
    hanoi(n - 1, source, helper, destination)

    # Step 2: move the one big disk that's left, straight to its final spot.
    print(f"Move disk {n} from {source} to {destination}")

    # Step 3: move the n-1 disks from the helper pole onto the destination.
    hanoi(n - 1, helper, destination, source)


# Try it out with 3 disks, moving from pole A to pole C, using pole B as helper.
num_disks = 3
hanoi(num_disks, "A", "C", "B")
print(f"\nTotal moves: {2 ** num_disks - 1}")
```

**What each part is doing, in plain words:**

- `def hanoi(n, source, destination, helper):` sets up a job named `hanoi`. To run it, you say how many disks (`n`), which pole they start on (`source`), which pole they need to end up on (`destination`), and which pole is free to use as a parking spot (`helper`).
- `if n == 0: return` — if there's nothing to move, stop right there. This is what keeps the program from running forever: every path through the code eventually shrinks down to "0 disks left," and then it just quits.
- The first `hanoi(...)` call asks the program to clear the smaller pile out of the way first.
- The `print(...)` line announces the move of the big disk. By this point, we know the smaller pile is already out of the way, so the big disk is free to move directly.
- The second `hanoi(...)` call asks the program to bring the smaller pile back and stack it on top of the big disk.
- The last two lines start everything off — asking to move 3 disks from A to C, then printing how many total moves it took.

**Run it, and here's exactly what you'll see:**

```
Move disk 1 from A to C
Move disk 2 from A to B
Move disk 1 from C to B
Move disk 3 from A to C
Move disk 1 from B to A
Move disk 2 from B to C
Move disk 1 from A to C

Total moves: 7
```

✅ This matches the table in Section 5, move for move. This exact code was run and checked against the `2ⁿ − 1` formula for every value of `n` from 0 to 10 — every move count matched perfectly, and no move ever broke the "no big disk on a small disk" rule.

---

## 9. Quick recap ✨

> [!NOTE]
> **The whole guide in five lines:**
>
> - 🗼 Three poles, a stack of disks, move one at a time, never put a big disk on a small one.
> - 💡 The trick: move the smaller pile out of the way, move the big disk, then move the smaller pile back on top. Do this on smaller and smaller piles until there's just 1 disk left — that's **recursion**.
> - 🧮 The minimum number of moves for `n` disks is always `2ⁿ − 1`.
> - 📈 This number grows **exponentially**, so the puzzle takes a long time to fully play out as `n` grows — but there's no way to do it in fewer moves. This really is the best possible solution.
> - 🐍 The Python code above follows the exact same three-step idea, just written in code instead of words.

🎉 **You now understand recursion well enough to explain it to someone else — that's the real win here.**
