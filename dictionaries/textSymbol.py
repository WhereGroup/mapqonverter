class TextSymbol:

    def __init__(self):
        pass

    textSymbolHorizontalAlign = {
        0: "1",  # Left
        1: "4",  # Center
        2: "2",  # Right
        3: "8"   # Full
    }

    textSymbolVerticalAlign = {
        0: "32",   # up
        1: "128",  # Center
        2: "64",   # down
        3: "128"   # Baseline doesnot exist in Qgis
    }
