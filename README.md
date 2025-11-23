# Conway's Game of Life Simulator

This is a Python implementation of Conway's Game of Life, a cellular automaton simulation where cells live, die, or reproduce based on simple rules. The simulator lets you load patterns, run the simulation, and log each step.

## Features

* Load built-in or custom patterns.
* Run the simulation for a specified number of rounds.
* Set the speed of the simulation.
* Save logs of each step in the `logs` folder.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/jorgennonstad/ACIT4420-conwayLife
cd ACIT4420-conwayLife
```

2. Install the package locally:

```bash
pip install .
```

3. Run the simulator:

```bash
conway
```

## Adding Patterns

You can add your own patterns:

1. Go to the `conwayLife/patterns` folder.
2. Add a `.txt` file containing your pattern.

   * Use `O` for alive cells and `.` for dead cells.
   * Each line in the file represents a row.
3. The simulator will automatically detect new pattern files.

Example pattern (glider):

```
.O.
..O
OOO
```

## Running Tests

Run the tests with pytest:

```bash
pytest
```

Make sure `pytest` is installed:

```bash
pip install pytest
```

## Setup Information

The package includes the `conwayLife` module and uses `patterns/*.txt` and `logs/*` as package data. The `setup.py` entry point allows running `conway` from the command line.

## Requirements

* Python 3.8+
* Optional: pytest for testing
