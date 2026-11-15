
import sys
import platform

import numpy as np
import pandas as pd
import matplotlib
import sklearn


def main():
    print("=" * 45)
    print("AI ENGINEERING DEVELOPMENT ENVIRONMENT")
    print("=" * 45)

    print(f"Python version: {sys.version.split()[0]}")
    print(f"Operating system: {platform.system()}")
    print(f"NumPy version: {np.__version__}")
    print(f"Pandas version: {pd.__version__}")
    print(f"Matplotlib version: {matplotlib.__version__}")
    print(f"Scikit-learn version: {sklearn.__version__}")

    numbers = np.array([10, 20, 30, 40, 50])

    print("\nNumPy test:")
    print(f"Numbers: {numbers}")
    print(f"Average: {np.mean(numbers)}")

    data = {
        "Student": ["Abdi", "Sara", "Musa"],
        "Score": [85, 92, 78]
    }

    dataframe = pd.DataFrame(data)

    print("\nPandas test:")
    print(dataframe)

    print("\nEnvironment setup successful!")


if __name__ == "__main__":
    main()
