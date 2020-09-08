# -*- coding: utf-8 -*-


class ShareParameter(object):
    exec_yaml_path = None
    exec_yaml = None
    exec_date = None
    dry_run_mode = False
    batch_name = None
    log_name = None
    log_dir = None
    sub_module_result = None
    working_dir = None
    success_return_code = 0
    error_return_code = 1
    tries_count = 0
