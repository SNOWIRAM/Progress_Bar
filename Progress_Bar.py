import time
import matplotlib
import sys
import inspect

class Progress_Bar:
    avg_time_inc = 0
    start_time = time.time()
    progress_time = start_time
    executing_time = 0
    time_inc = 0

    cmd_max_bar = 20
    percentage_transform_factor = 100

    def __init__(self, total_len, report_interval=1):
        self.total_len = total_len
        self.start_time = time.time()
        self.report_interval = report_interval
        self.print_outer_function_name()

    @staticmethod
    def print_outer_function_name():
        outer_function = inspect.getframeinfo(inspect.currentframe().f_back.f_back).function
        print(outer_function)

    def set_start_time(self, start_time=time.time()):
        self.start_time = start_time

    def set_progress_iter_num(self, i):
        self.i = i

    def set_time_inc(self, executing_time):
        if self.time_inc == 0:
            self.time_inc = executing_time - self.executing_time

    def set_executing_time(self, progress_time):
        if self.executing_time == 0:
            self.executing_time = progress_time - self.progress_time

    def set_progress_time(self, progress_time):
        self.progress_time = progress_time

    def set_progress_info(self, i, progress_time):
        temp_executing_time = progress_time - self.progress_time

        self.set_progress_iter_num(i)

        if i>=2:
            self.set_time_inc(temp_executing_time)
            self.set_avg_time_inc(self.time_inc)
        if i>=1:
            self.set_executing_time(progress_time)

        self.set_progress_time(progress_time)

    def progress_bar_cmd(self, progress_ratio, elapsed_time, time_left):

        iter_per_sec = round((self.i + 1)/elapsed_time, 2)
        adj_progress_ratio_factor = int(round(progress_ratio * self.cmd_max_bar/self.percentage_transform_factor))
        progress_bar_graph = ['#' for i in range(adj_progress_ratio_factor)]
        progress_bar_graph_compliment = ['-' for i in range(self.cmd_max_bar-adj_progress_ratio_factor)]
        progress_bar_tot = progress_bar_graph + progress_bar_graph_compliment

        progress_bar = '|'

        for progress_unit in progress_bar_tot:
            progress_bar = progress_bar + progress_unit

        print('Work progress:', progress_bar,
              int(round(time_left)), 'sec(s),(', progress_ratio, '% complete', ')',
              'iter/s(', iter_per_sec, ')\r', end='')

    def report_elapsed_time(self):
        print('Elapsed time:', round(self.progress_time - self.start_time), 'sec(s)', '\n')


    def set_avg_time_inc(self, time_inc_unit):
        self.avg_time_inc = time_inc_unit/(self.i+1) + ((self.avg_time_inc)*self.i)/(self.i+1)

    def progress_report_simple_fn(self):

        time_now = time.time()
        progress_ratio = (self.i+1) / (self.total_len + 1)
        progress_ratio_round = int(round((self.i + 1) / self.total_len * 100))
        elapsed_time = (time_now - self.start_time)

        if (self.i > 0) & ((self.i % self.report_interval) == 0):
            time_left = (elapsed_time / progress_ratio) - elapsed_time
            self.progress_bar_cmd(progress_ratio_round, elapsed_time, time_left)

        if (self.i +1) == self.total_len:
            print()
            self.report_elapsed_time()

        return 0

    #FIMXE: 여기서 부터
    def progress_report_adj_time_inc_fn(self):

        time_now = time.time()
        progress_ratio = (self.i+1) / (self.total_len + 1)
        progress_ratio_round = int(round((self.i + 1) / self.total_len * 100))
        elapsed_time = (time_now - self.start_time)

        if (self.i > 0) & ((self.i % self.report_interval) == 0):
            time_left = ((time_now - self.start_time) / progress_ratio + self.avg_time_inc *
                         (self.total_len - (self.i + 1))) - (time_now - self.start_time)

            self.progress_bar_cmd(progress_ratio_round, elapsed_time, time_left)

        if (self.i +1) == self.total_len:
            print()
            self.report_elapsed_time()

        return 0

    def progress_report_adj_time_inc_sq_fn(self):

        time_now = time.time()
        progress_ratio = (self.i+1) / (self.total_len + 1)
        progress_ratio_round = int(round((self.i + 1) / self.total_len * 100))
        elapsed_time = (time_now - self.start_time)

        if (self.i > 0) & ((self.i % self.report_interval) == 0):
            time_left = ((time_now - self.start_time) / progress_ratio +
                         self.avg_time_inc * (self.total_len - (self.i + 1)) +
                         (self.avg_time_inc)**2 * (self.total_len - (self.i + 1))) - (time_now - self.start_time)

            self.progress_bar_cmd(progress_ratio_round, elapsed_time, time_left)

        if (self.i +1) == self.total_len:
            print()
            self.report_elapsed_time()

        return 0