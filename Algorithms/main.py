class Trace:
    BUBBLE = "Bubble Sort"
    INSERTION = "Insertion Sort"
    MERGE = "Merge Sort"
    QUICK = "Quick Sort"

    LINEAR = "Linear Search"
    BINARY = "Binary Search"

    DEPTH = "Depth-First Traversal"
    BREADTH = "Breadth-First Traversal"

    DIJKSTRA = "Dijkstra's Pathfinding Algorithm"
    A_STAR = "A* Pathfinding Algorithm"

    def __init__(self, trace_type, steps=None):
        self.trace_type = trace_type
        self.steps = steps
        if steps is None: self.steps = []

    def add_step(self, step):
        self.steps.append(step)

    def to_string(self):
        result = f"\n{self.trace_type}\t{self.steps[0]}\n\n"

        for index in range(1, len(self.steps) - 2):
            result += f"Step {index}\t\t{self.steps[index]}\n"

        result += f"\nResult\t\t{self.steps[-1]}\n"

        return result


def bubble_sort(values, steps=False):
    """
    This implementation of bubble sort uses the fact that after n
    iterations of the outer loop, the last n values will be sorted.
    This means that the function will take the same number of steps
    even if the input array is partially or fully sorted.

    If is also possible to create a bubble sort using a while loop and a flag.
    If no swaps have been made within the inner loop, the flag is updated
    and the loop is exited, as this means that the array is sorted.

    :param values: List of values to be sorted.
    :param steps: Whether to include the steps of the sorting.
    :return: Sorted list, or Trace object containing the steps and type of sorting.
    """

    # -- Trace object to show each step:
    trace = Trace(Trace.BUBBLE)
    trace.add_step(values.copy())

    # Iterating over values:
    for i in range(len(values)):
        # Last 'i' values have been sorted correctly, no need to check them again.
        # Length is always 1 greater than max index so subtracting 1.
        for j in range(len(values) - i - 1):
            # If the current value is greater than the next, swapping them.
            if values[j] > values[j + 1]:
                temp = values[j]
                values[j] = values[j + 1]
                values[j + 1] = temp

        # -- Adding step to Trace object:
        trace.add_step(values.copy())

    # If the user would like the steps, return Trace object:
    if steps: return trace
    return values


def insertion_sort(values, steps=False): pass


def merge_sort(values, steps=False): pass


def quick_sort(values, steps=False): pass


def linear_search(values, target): pass


def binary_search(values, target): pass


def depth_traverse(nodes): pass


def breadth_traverse(nodes): pass


def dijkstra_path(): pass


def a_star_path(): pass


def is_prime(x):
    if x < 2: return False

    for i in range(2, int(x**0.5) + 1):
        if x % i == 0: return False
    return True


def main():
    vals = [-4, 9, 4, -8, 2, -6, -7, -5, 1, 5, 6, -3, -1, 8, -2, 0, -9, 7]
    test_vals = [-5, 41.5, -56.664, 1, -99.6434, 2, 47.3, -8, 0.1, 3.99, 5.0, 3.98]

    print(bubble_sort(vals, steps=True).to_string())






if __name__ == "__main__": main()
