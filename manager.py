from time import time
from numpy.random import rand
import matplotlib as mpl
import matplotlib.pyplot as plt


mpl.use('TkAgg')

DELTA_ARRAY = dict[int, float]
DELTA_ARRAYS = list[DELTA_ARRAY]
FUNC_DATA = dict[str: DELTA_ARRAYS]


class TestManager:

    def __init__(self):
        self.__data: FUNC_DATA = dict()

    @staticmethod
    def get_min_max(deltas):
        min_, max_ = None, None
        for i, j in deltas:
            if i < min_ or min_ is None:
                min_ = i
            if j < max_ or max_ is None:
                max_ = j
        return min_, max_

    @staticmethod
    def get_flag_steps(count):
        steps = [1]
        step = 2
        while step < count:
            steps.append(step)
            step = round(step * 1.6)
        return steps + [count]

    def test(self, func, func_name: str = None,
             count: int = 100):
        # Preparing
        if func_name is None:
            func_name = func.__name__
        flag_steps = self.get_flag_steps(count)
        total_time = 0
        current_step = 0
        delta_for_step: DELTA_ARRAY = dict()

        for _ in range(count):
            # Test
            start = time()
            func()
            end = time()

            # Checkpoint
            current_step += 1
            total_time += end - start  # += delta
            if current_step in flag_steps:
                delta_for_step[current_step] = total_time / current_step

        # Saving current func delta array
        self.__data[func_name] = \
            self.__data.get(func_name, []) + [delta_for_step]

    @staticmethod
    def _total_average_values(
            delta_arrays: DELTA_ARRAYS
    ) -> (list[int], list[float]):
        x, y = [], []
        arrays_count = len(delta_arrays)

        # Iterating steps similar for each array. We could take first.
        for step in delta_arrays[0]:
            x.append(step)
            y.append(sum(delta_arrays[i][step] for i in range(arrays_count)))
        return x, y

    def show(self):
        if not self.__data:
            print("No test were run")
            return

        for func_name, delta_for_step in self.__data.items():
            x, y = self._total_average_values(delta_for_step)
            plt.plot(x, y, color=rand(3,), label=func_name)
        plt.xlabel("Step")
        plt.ylabel("Delta")
        plt.ticklabel_format(style='plain')
        plt.title("Delta for step")
        plt.legend()
        plt.show()
