from Progress_Bar import *
import random

def simple_sum(sum_list, progress_bar=False):
    if progress_bar:
        progress_bar_instance = Progress_Bar(len(sum_list))

    tot_sum = 0

    for i in range(len(sum_list)):
        tot_sum += sum_list[i]

        if progress_bar:
            progress_bar_instance.set_progress_info(i, time.time())
            progress_bar_instance.progress_report_simple_fn()

    return tot_sum


if __name__ == '__main__':

    iter_n = 100000
    sum_list = [random.randint(1, 10) for i in range(iter_n)]
    simple_sum_value = simple_sum(sum_list, progress_bar=True)