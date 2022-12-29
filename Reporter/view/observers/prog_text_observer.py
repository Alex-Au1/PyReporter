from .observer import Observer
from ..export import ExportSubject
from ...data_frames import ExcelDf
from ...tools import DataFrameTools as DfTools
from ...events import ExcelExportEvent
from .excel_export_observer import ExcelExportObserver
from ...events.progress_event import *
import traceback
from typing import Any


# output of the progress for running the report
PROGRESS_OUTPUT_FILE = "progress_log.txt"


class ProgTextObserver(Observer):
    def __init__(self, verbose: bool = True, debug: bool = True, export_calc_tables: bool = False, progress_to_txt: bool = False):
        super().__init__()
        self.__verbose = bool(verbose or debug)
        self.__debug = debug
        self.__export = export_calc_tables
        self.__progress_to_txt = progress_to_txt

        self.__step = 0
        self.__excel_export_view = ExportSubject()
        self.__excel_export_view.attach(ExcelExportObserver())

        # get the file to write the progress
        self.__file = None
        if (self.__progress_to_txt):
            with open(PROGRESS_OUTPUT_FILE, 'w+') as file_ptr:
                file_ptr.seek(0)
                file_ptr.write(f"")


    # update(): Updates the message
    def __update(self, message: str, end_with_new_line: bool = True):
        if (not end_with_new_line):
            print(message, end = "")
        else:
            print(message)

        if (self.__progress_to_txt):
            with open(PROGRESS_OUTPUT_FILE, 'a+') as file_ptr:
                file_ptr.write(f"{message}\n")


    # __export_data(file_name, source_table): Export excel files containing the data
    def __export_data(self, file_name: str, source_table: pd.DataFrame) -> str:
        file = f"./debug/{file_name}.xlsx"
        source_table = DfTools.df_to_celled_df(source_table)
        self.__excel_export_view.notify(ExcelExportEvent([ExcelDf(source_table)], loc = file, sheet = file_name))
        return file


    # __check_debug_event_print(out_event): Determines if the 'out_event' is
    #   ready to be print
    def __check_debug_event_print(self, out_event: DebugOutEvent) -> bool:
        return (self.__verbose and not out_event.debug) or (self.__debug and out_event.debug)


    # notify_sql_check(out_event): Prints the corresponding SQL query
    def notify_sql_check(self, out_event: SqlQueryCheckEvent):
        if (self.__debug):
            message = f"\n############### SQL Query Check ##################"
            message += f"\n\nSource Name: {out_event.source_name}"
            message += f"\nDSN: {out_event.dsn_name}"
            message += f"\n\nSQL Query: \n\n{out_event.sql_query}"
            message += f"\n\n###################################################"
            self.__update(message)


    # notify_import(out_event): Prints the corresponding imported table
    def notify_import(self, out_event: ImportEvent):
        is_export = bool(self.__export and out_event.export_file_name is not None)

        # exoprt the table
        if (is_export):
            path = self.__export_data(out_event.export_file_name, out_event.source_table)

        if (self.__verbose):
            message = f"\n@@@@@@@@@@@@@@@ Imported Data @@@@@@@@@@@@@@@@@@@@@@"
            message += f"\n\nSource Name: {out_event.name}"
            message += f"\nSource Type: {out_event.source_type.__name__}"
            message += f"\nSource Content:\n\n{out_event.source_table}"

            if (is_export):
                message += f"\n\nExported Data to \"{path}\""

            message += f"\n\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

            self.__update(message)


    # notify_step(): Prints out the corresponding step being run in the report
    def notify_step(self, out_event: StepEvent):
        if (self.__verbose):
            # retrieve the corresponding step no.
            step = out_event.step_no
            if (out_event.step_no is None):
                self.__step += 1
                step = self.__step
            else:
                self.__step = step

            message = f"======== Step {step}: {out_event.step_name} ========"
            border_message = "=" * len(message)

            message = f"\n\n\n{border_message}\n{message}\n{border_message}\n\n"
            self.__update(message)


    # notify_table_check(out_event): Prints out the corresponding table and exports it if needed
    def notify_table_check(self, out_event: TableCheckEvent):
        is_debug = bool(self.__check_debug_event_print(out_event))
        is_export = bool(self.__export and out_event.export_file_name is not None)
        message = ""

        if (is_debug):
            message += "\n+--------------- Table Check ------------------------+"
            message += f"\n\nTable Name: {out_event.name}"

        if (is_debug):
            message += f"\nTable Content:\n\n{out_event.source_table}"

        # export the table
        if (is_export):
            path = self.__export_data(out_event.export_file_name, out_event.source_table)
            message += f"\n\nExported Data to \"{path}\""

        if (is_debug):
            message += f"\n\n+----------------------------------------------------+"
            self.__update(message)


    # notify_print(out_event): Prints out text flags
    def notify_print(self, out_event: PrintEvent):
        if (self.__check_debug_event_print(out_event)):
            self.__update(out_event.text, end_with_new_line = out_event.end_with_new_line)


    # notify_list(out_event): Prints out a list
    def notify_list(self, out_event: ListPrintEvent):
        if (self.__check_debug_event_print(out_event)):
            if (out_event.prefix is not None):
                self.__update(out_event.prefix)

            if (not out_event.flatten):
                for e in out_event.lst:
                    self.__update(e)
            else:
                self.__update(out_event.lst)

            if (out_event.suffix is not None):
                self.__update(out_event.suffix)


    # notify_err(out_event): Prints out the error
    def notify_err(self, out_event: ErrEvent):
        if (self.__check_debug_event_print(out_event)):
            exception_lst = traceback.format_exception(type(out_event.exception), out_event.exception, out_event.exception.__traceback__)
            exception_str = ""
            border_str = f"!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

            for e in exception_lst:
                exception_str += e

            message = ""
            if (not out_event.no_decorator):
                message += f"\n{border_str}"
                message += f"\n!!!!!!!!!!!!!! AN ERROR HAS OCCURRED !!!!!!!!!!!!!!!!!!!!\n\n"

            message += f"Error: {type(out_event.exception).__name__}: {out_event.exception}"
            message += f"\n\nTraceback:\n{exception_str}"

            if (not out_event.no_decorator):
                message += f"\n\n{border_str}"
                message += f"\n{border_str}"

            self.__update(message)



    # notify(target): Updates the observer based off 'target'
    def notify(self, target: Any):
        if (isinstance(target, SqlQueryCheckEvent)):
            self.notify_sql_check(target)

        elif (isinstance(target, ImportEvent)):
            self.notify_import(target)

        elif (isinstance(target, StepEvent)):
            self.notify_step(target)

        elif (isinstance(target, TableCheckEvent)):
            self.notify_table_check(target)

        elif (isinstance(target, PrintEvent)):
            self.notify_print(target)

        elif (isinstance(target, ListPrintEvent)):
            self.notify_list(target)

        elif (isinstance(target, ErrEvent)):
            self.notify_err(target)
