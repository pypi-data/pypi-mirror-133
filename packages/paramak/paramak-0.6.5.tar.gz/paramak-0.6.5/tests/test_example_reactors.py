import os
import sys
import time
from pathlib import Path

from notebook_testing import notebook_run

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "examples"))


def main():
    timings = []
    for notebook in Path().rglob("examples/example_parametric_reactors/*.ipynb"):
        start = time.time()

        print(notebook)
        errors = notebook_run(notebook)
        assert errors == []

        stop = time.time()
        duration = stop - start

        print((notebook, duration))
        timings.append((notebook, duration))

    # to see timings run with pytest --capture=tee-sys
    print(timings)


if __name__ == "__main__":
    main()
