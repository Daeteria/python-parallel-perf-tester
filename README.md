# Python Parallel Task Performance Tester

A testing framework for evaluating performance scaling of different computational tasks when parallelized in Python.


## Overview

The intent of this project is to provide a tangible way of understanding the performance scaling of parallel processing in Python and how it depends on the task at hand. It could also be used as a reference point for building a foundation on how much parallelization one might want for a given task and resource constraints. For example, if you have a 4-core cloud instance, would it be best to have 2-4 parallel workers for your application, or no parallelization at all?

In a mixed workload of randomized tasks, my own testing resulted in a 5.9x average speedup (12 workers) at best when compared to running the same tasks sequentially. Best results for a single task type were 9.8x with 16 workers (password hashing & checking) while worst were a slowdown to 0.45x with 16 workers (image manipulation with OpenCV). Tests were run on a system with 12 performance and 4 efficiency CPU cores.


## Features

- Multiple task types:
  - Computationally intensive tasks
  - I/O intensive tasks
  - Memory intensive tasks
  - Fork and add your own or propose some!
- Configurable test parameters (JSON):
  - Number of worker processes (0-n) [0 = direct sequential function calls]
  - Task count
  - Task-specific parameters
  - Test iterations
- Performance metrics:
  - Initialization time
  - Average per task execution time
  - Total task execution time
  - Total runtime (init, work, cleanup)
- CSV export of results


## Installation

```sh
# Clone the repository
git clone https://github.com/daeteria/python-parallel-perf-tester.git
cd parallel-performance-tester

# Install dependencies
pip install -r requirements.txt
```


## Usage

```sh
python main.py --config example_configs/sum.json
```


A valid configuration file is as follows:

```json
{
    "iterations": 10,
    "task": "sort",
    "task_args": [1000000],
    "task_count": 100,
    "workers": [0, 1, 2, 4, 6, 8, 10, 12, 16],
    "wait_time_after_runner": 2.0,
    "wait_time_after_iteration": 2.0,
    "gc_after_iteration": true
}
```

Where
- `iterations`: How many test passes to perform per worker configuration. The output will be an average of all passes.
- `task`: Which task to run. Refer to the Task types section below for more.
- `task_args`: A list of arguments to pass to the task function. Check the `task_func` mapping in `main.py` to see what is the reffered function and what arguments it takes in from the function implementation. All tasks are defined in the `work` module. With the `random` task type this parameter is used to select which task types to include in the task list. 
- `task_count`: How many tasks to perform per test pass, e.g. how many times the task function gets called in total.
- `workers`: A list of worker configurations to test. 0 here means sequential and is a good reference point to use. 1 means that you have a single parallel process that gets fed tasks by the main process, so basically "sequential with scheduling overhead". It is adviced to at maximum have your system's CPU core count of workers. You can of course try higher numbers, but this can lead to crashing.
- `wait_time_after_runner`: How long to wait after each runner pipeline in seconds, e.g. between running the pipeline for 2 and then 4 workers. Can be used as a cooldown period for your CPU, so that the runs won't affect each other.
- `wait_time_after_iteration`: How long to wait after each test iteration loop in seconds. Can be used as a cooldown period and a reset for your CPU between iterations, so that the iterations won't affect each other.
- `gc_after_iteration`: Whether or not to run garbage collection after each test iteration.

Refer to the example configurations in `example_configs` for more configurations.


## Task types

- `sum`: Integer addition loop [computation]
- `multi`: Floating point multiplication loop [computation]
- `io`: File read/write/delete operations [drive access]
- `zip`: File compression/decompression [computation / drive access]
- `tensor`: Tensor dot product calculation [computation, internally parallelized (Numpy)]
- `sort`: Array sorting [memory-intensive]
- `matrix`: Matrix inversion [memory-intensive]
- `img`: Image manipulation [computation, internally parallelized (OpenCV)]
- `password`: Password hashing and checking [computation]
- `random`: Random mix of above tasks. Note that you can set a list of task types you wish to use by defining them in `task_args`, e.g. `["io", "zip", "img"]`. Leaving the array empty will use all available options when generating the task list. The arguments for each task are pulled at random from predefined pools of viable options. See `work/{task_type}.py` for details.


## Results

Running the application will output a CSV file into `results` directory with averaged runtime details of each configured worker count.

Example output of running task `password`:

```csv
Name,Workers,Task details,Task count,Time: init,Time: work,Time: task avg,Time: total,Tasks per second
sequential,0,"100/1000; [20, 20]; 0.5",10000,0.0,23.263290723164875,0.0023263290723164877,23.263290723164875,429.8617989604671
parallel_1,1,"100/1000; [20, 20]; 0.5",10000,0.039650678634643555,23.81737995147705,0.0023623600323994954,23.85883363087972,419.13197244719134
parallel_2,2,"100/1000; [20, 20]; 0.5",10000,0.04159665107727051,12.133824348449707,0.00240121800104777,12.177467346191406,821.1888166653614
parallel_4,4,"100/1000; [20, 20]; 0.5",10000,0.045926570892333984,6.233467022577922,0.0024528975089391073,6.281706889470418,1591.924006636205
parallel_6,6,"100/1000; [20, 20]; 0.5",10000,0.04733030001322428,4.185808022816976,0.002460975170135498,4.236040910085042,2360.694859247533
parallel_8,8,"100/1000; [20, 20]; 0.5",10000,0.05149205525716146,3.1759578386942544,0.00248035790125529,3.231079339981079,3094.9410236576114
parallel_10,10,"100/1000; [20, 20]; 0.5",10000,0.05439281463623047,2.5916500091552734,0.0025193341890970863,2.650707801183065,3772.5772699415593
parallel_12,12,"100/1000; [20, 20]; 0.5",10000,0.061316490173339844,2.3652519385019937,0.0027502798557281494,2.432237227757772,4111.4410575891025
parallel_16,16,"100/1000; [20, 20]; 0.5",10000,0.087737242380778,2.1500957012176514,0.0033195030212402345,2.2449360688527427,4454.469834907336
```

## Requirements

- Python 3.x (tested with 3.9.x)
- Python libraries listed in `requirements.txt`


## Credits

Test image from [Unsplash](https://unsplash.com/photos/brown-and-black-snake-on-ground-vec5yfUvCGs)
