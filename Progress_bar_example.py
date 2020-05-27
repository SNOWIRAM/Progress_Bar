from Progress_Bar import *
import random

def simple_sum(sum_list, progress_bar=False):
    if progress_bar:
        progress_bar_instance = Progress_Bar(len(sum_list), report_interval=100)

    tot_sum = 0

    for i in range(len(sum_list)):
        tot_sum += sum_list[i]

        if progress_bar:
            progress_bar_instance.set_progress_info(i, time.time())
            progress_bar_instance.report_progress()

    return tot_sum

if __name__ == '__main__':

    iter_n = 1000000
    sum_list = [random.randint(1, 10) for i in range(iter_n)]
    start_time = time.time()
    simple_sum_value = simple_sum(sum_list, progress_bar=True)
    print(time.time()- start_time)