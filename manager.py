import sys
from time import time
from numpy.random import rand
import matplotlib as mpl
import matplotlib.pyplot as plt

# Fixme: add execution code output as:
# import inspect
# Fixme: ...or...
# s="str(1)"
# lambda: eval(s)


mpl.use('TkAgg')

DELTA_ARRAY = dict[int, float]
DELTA_ARRAYS = list[DELTA_ARRAY]
FUNC_DATA = dict[str: DELTA_ARRAYS]


class TestManager:

    def __init__(self):
        self.__tests = dict()
        self.__data = dict()
        self.__current_test_name = None

    def add_test(self, test, count: int = 1):
        """
        Add test to order.

        :param test: Function, than runs all compared functions
        :param count: Count of test runs improves the accuracy of comparison results
        """
        test_name = test.__name__
        self.__tests[test_name] = (test, count)
        self.__data[test_name] = {}

    def run(self):
        """ Run tests in order """
        print("Tests were launched...")
        for test_name, test_data in self.__tests.items():
            self.__current_test_name = test_name
            test, count = test_data
            print(f"Test {test_name} started...")
            for _ in range(count):
                test()
            print(f"Test {test_name} finished.")

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

    def test(self, func, func_name: str = None, steps_count: int = 100):
        # Preparing
        if func_name is None:
            func_name = func.__name__
        flag_steps = self.get_flag_steps(steps_count)
        total_time = 0
        current_step = 0
        delta_for_step: DELTA_ARRAY = dict()

        for _ in range(steps_count):
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
        test_name = self.__current_test_name
        if func_name not in self.__data[test_name]:
            self.__data[test_name][func_name] = []
        self.__data[test_name][func_name].append(delta_for_step)

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

    def _add_plot(self):
        ...

    def show(self):
        if not self.__current_test_name:
            raise Exception("No test were run!")
        if not self.__data:
            raise Exception("Test were run, but data not found!")
        if not any([bool(test_data) for test_data in self.__data.values()]):
            raise Exception("Test data not found!")

        fig, axs = plt.subplots(1)
        for test_index, test_name in enumerate(self.__data):
            for func_name, delta_for_step in self.__data[test_name].items():
                x, y = self._total_average_values(delta_for_step)
                func_color = rand(3,)
                axs.plot(x, y, color=func_color, label=func_name)
            axs.set(xlabel='Step', ylabel='Delta (sec)')
            axs.set_title(test_name)
            axs.ticklabel_format(style='plain')
            axs.get_yaxis().get_major_formatter().set_useOffset(False)
            axs.legend()

        plt.suptitle(f"All tests | Python {sys.version}")
        plt.show()
        # Fixme: add removing test data for saving temp result
        plt.close()
