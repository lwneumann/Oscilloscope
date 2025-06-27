from math import ceil, floor
import numpy as np


def divide_time(t):
        """
        Divide t into equal-length chunks for each child.
        Each chunk includes the start and end of t, and a subset of values from the middle.
        Returns a list of t_sub arrays, one for each child.
        """
        number_of_children = len([1, 2, 3, 4, 5, 6, 7])
        if number_of_children == 0:
            return []

        chunk_size = ceil(len(t) / number_of_children)
        
        child_chunk = np.linspace(
              start=t[0],
              stop=t[-1],
              num=chunk_size
        )

        chunks = [ child_chunk for _ in range(number_of_children) ]

        # Remove elements from the end of each chunk so that the total number of elements in all chunks equals len(t)
        c_i = 0
        total = sum(len(chunk) for chunk in chunks)
        while total > len(t):
            if len(chunks[c_i]) > 2:
                chunks[c_i] = np.delete(chunks[c_i], -2)
            total -= 1
            c_i = (c_i + 1) % number_of_children

        return chunks


frames = 40
samplerate = 1
t = (np.arange(frames)) / samplerate

s = 0
for c in divide_time(t):
    s += len(c)
    print(c)
print()
print('Wanted', len(t))
print('Got', s)
