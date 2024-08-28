from PocketLogger import PocketLogger


def test_pocket_logger(plogger: PocketLogger):
    plogger.log('This is log message from a function')


plogger = PocketLogger(log_file_path='logs/test.log', print_caller=False, add_date_and_time_to_log_file_name=True)
plogger.log('This is a log message')
test_pocket_logger(plogger)
plogger.log('This is multi-line log message...\nIt is soo cool!\nI love it!')

plogger.save_time = False
# plogger.save_caller = False
plogger.log('This is another multi-line log message...\nIt is soo cool!\nIt shouldn\'t have time stamp or caller!')