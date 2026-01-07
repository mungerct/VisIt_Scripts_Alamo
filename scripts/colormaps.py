from matplotlib.colors import LinearSegmentedColormap

def hot(N=256):
    colors = [
        (0.0, 0.0, 1.0),
        (0.0, 1.0, 1.0),
        (0.0, 1.0, 0.0),
        (1.0, 1.0, 0.0),
        (1.0, 0.0, 0.0),
    ]
    return LinearSegmentedColormap.from_list(
        "hot", colors, N=N
    )