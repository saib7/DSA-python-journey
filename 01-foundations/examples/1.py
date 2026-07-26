def hanoi(n, source, destination, auxiliary):
    if n == 0:
        return  # base case: no disks left to move, do nothing

    # Step 1: move the top n-1 disks out of the way, onto the auxiliary peg
    hanoi(n - 1, source, auxiliary, destination)

    # Step 2: move the single remaining (largest) disk to its final spot
    print(f"Move disk {n} from {source} to {destination}")

    # Step 3: move the n-1 disks from the auxiliary peg onto the destination
    hanoi(n - 1, auxiliary, destination, source)



if __name__ == "__main__":
    # Kick it off: move 3 disks from peg A to peg C, using peg B as helper
    hanoi(10, 'A', 'C', 'B')