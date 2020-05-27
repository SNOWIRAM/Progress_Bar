import time
import matplotlib
import sys
import inspect
import math

class Progress_Bar:
    avg_time_inc = 0
    weight_avg_time_inc = 0
    executing_time = 0
    time_inc = 0
    avg_time_inc_ratio = 1

    cmd_max_bar = 20
    percentage_transform_factor = 100

    def __init__(self, total_len, report_interval=1):
        self.total_len = total_len
        self.start_time = time.time()
        self.report_interval = report_interval
        self.print_outer_function_name()
        self.progress_time = time.time()

    @staticmethod
    def print_outer_function_name():
        outer_function = inspect.getframeinfo(inspect.currentframe().f_back.f_back).function
        print(outer_function)

    def set_start_time(self, start_time=time.time()):
        self.start_time = start_time

    def set_progress_iter_num(self, i):
        self.i = i

    def set_time_inc(self, executing_time):
        self.time_inc = executing_time - self.executing_time

    def cal_time_inc(self, executing_time):
        return executing_time - self.executing_time

    def get_pre_time_inc(self):
        return self.time_inc

    def set_executing_time(self, progress_time):
        self.executing_time = progress_time - self.progress_time

    def set_progress_time(self, progress_time):
        self.progress_time = progress_time

    def set_avg_time_inc(self, time_inc_unit):
        if self.avg_time_inc == 0:
            self.avg_time_inc = self.time_inc
        self.avg_time_inc = time_inc_unit / (self.i + 1) + ((self.avg_time_inc) * self.i / (self.i + 1))


    def set_progress_info(self, i, progress_time):

        if self.avg_time_inc == 0:
            self.avg_time_inc = self.time_inc
        temp_executing_time = progress_time - self.progress_time

        self.set_progress_iter_num(i)

        if i>=2:
            self.set_time_inc(temp_executing_time)
            self.set_avg_time_inc(self.time_inc)
        if i>=1:
            self.set_executing_time(progress_time)

        self.set_progress_time(progress_time)

        # print('Executing_time:',self.executing_time)
        # print('avg_inc:',self.avg_time_inc)
        # print('time_inc:',self.time_inc)

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

    def get_progress_report_elements(self):
        time_now = time.time()
        progress_ratio = (self.i+1) / (self.total_len + 1)
        progress_ratio_round = int(round((self.i + 1) / self.total_len * 100))
        elapsed_time = (time_now - self.start_time)

        return time_now, progress_ratio, progress_ratio_round, elapsed_time

    def clear_report_bar(self):
        if (self.i +1) == self.total_len:
            print()
            self.report_elapsed_time()

    def estimate_time_left(self, elapsed_time, progress_ratio, type='simple'):
        if type == 'simple':
            time_left = (elapsed_time / progress_ratio) - elapsed_time
        elif type == 'cons_inc':
            time_left = (elapsed_time / progress_ratio +
                         1/2 * self.avg_time_inc * (self.total_len - (self.i + 1)) ** 2 +
                         1/2 * self.avg_time_inc * (self.total_len - (self.i + 1))) - elapsed_time

        return time_left

    def report_progress(self, cal_type='simple'):
        if (self.i % self.report_interval) == 0:
            time_now, progress_ratio, progress_ratio_round, elapsed_time = self.get_progress_report_elements()

            if self.i > 0:
                time_left = self.estimate_time_left(elapsed_time, progress_ratio, cal_type)
                self.progress_bar_cmd(progress_ratio_round, elapsed_time, time_left)

            self.clear_report_bar()
