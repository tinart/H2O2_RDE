

def print_smoothing_help():
    help_text = """
    Help - Explanation of Smoothing Methods:

    1) Moving Average:
       Smooths the data by averaging each point with its neighbors within a window size.

    2) Exponential Smoothing:
       Weighs more recent data points more heavily, with an exponentially decreasing weight.

    3) Savitzky-Golay Filter:
       Performs a local polynomial regression to determine smoothed values, preserving the features of the signal.

    4) Lowess Smoothing:
       Uses local weighted regression to fit a line through points in a scatter plot, non-parametric.

    5) Gaussian Filter:
       Applies a Gaussian function to smooth the data, used for blurring and noise reduction.
    """
    print(help_text)


def print():

    pass
