def distance(p1, p2):
    """
    Euclidian distance based on minimum dimensions of given points
    """
    return ( sum([ (p1[i] - p2[i])**2 for i in range(min(len(p1), len(p2)))]) )**0.5
