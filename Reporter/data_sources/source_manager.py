from .abs_source import AbsSource, DEFAULT_POST_PROCESSOR_KEY
from ..events.progress_event import *
from ..events.out_event import OutEvent
from .sql import SQLSource
from .sharepoint import SharepointSource
from ..exceptions import BadSourceException
from ..view.progress import ProgressSubject
import pandas as pd
from typing import Dict, Optional


# SourceManager: Class to handle a source that could be imported from many different methods
class SourceManager():
    def __init__(self, name: str, import_method: Optional[str], src: Dict[str, AbsSource], progress_checker: Optional[ProgressSubject] = None):
        self.src = src
        self.name = name
        self.progress_checker = progress_checker

        self._notify_progress(PrintEvent(f"{self.name}:", debug = True))
        self._notify_progress(PrintEvent(f"Desired Import Method: {import_method}", debug = True))

        # set the name to all the sources
        for imp_method in self.src:
            self.src[imp_method].name = self.name

        # choose the import method
        if (import_method is not None):
            try:
                source = self.src[import_method]
            except:
                self.__first_key_default()
            else:
                self.import_method = import_method
        else:
            self.__first_key_default()

        self._notify_progress(PrintEvent(f"Chosen Import Method: {self.import_method}\n", debug = True))


    # __notify_progress(event): Notifies the progress of an event
    def _notify_progress(self, event: OutEvent):
        if (self.progress_checker is not None):
            self.progress_checker.notify(event)


    # __first_key_default(): Chooses the first method as the default import_method
    def __first_key_default(self):
        first_key = list(self.src.keys())[0]
        self.import_method = first_key


    # __prepare_source(import_method): Tries to import the source using 'import_method'
    async def __prepare_source(self, import_method: str, post_processor_name: str = DEFAULT_POST_PROCESSOR_KEY) -> Optional[pd.DataFrame]:
        self._notify_progress(PrintEvent(f"\n**********************************************************************"))
        self._notify_progress(PrintEvent(f"Testing importing \"{self.name}\" using the \"{import_method}\" import method...\n", end_with_new_line = False))

        # try importing the source
        try:
            source = self.src[import_method]
            result = await source.prepare(post_processor_name)

        # when failed to import
        except Exception as exception:
            self._notify_progress(PrintEvent(f"\nResult of importing \"{self.name}\" using the \"{import_method}\" import method...\tFailed\n"))
            self._notify_progress(PrintEvent(f"\n--------------------------\n", debug = True))
            self._notify_progress(ErrEvent(exception, no_decorator = True, debug = True))
            self._notify_progress(PrintEvent(f"\n--------------------------", debug = True))

            result = None


        # when successfully imported the data
        else:
            self._notify_progress(PrintEvent(f"\nResult of importing \"{self.name}\" using the \"{import_method}\" import method...\tSuccess!"))

            # notify the imported data
            export_file_name = None
            if (isinstance(source, SQLSource) or isinstance(source, SharepointSource)):
                export_file_name = self.name.replace(" ", "_")
                export_file_name = f"import_{export_file_name}"

            self._notify_progress(ImportEvent(self.name, type(source), result, export_file_name = export_file_name))

        self._notify_progress(PrintEvent(f"\n**********************************************************************"))
        return result



    # prepare(): Prepares the chosen source to be imported to the report
    async def prepare(self, post_processor_name: str = DEFAULT_POST_PROCESSOR_KEY) -> pd.DataFrame:
        result = await self.__prepare_source(self.import_method, post_processor_name)

        # try all the possible source importing options
        if (result is None):
            for import_method in self.src:
                if (import_method != self.import_method):
                    result = await self.__prepare_source(import_method, post_processor_name)

                    if (result is not None):
                        break

        # if we fail to load any of the source options, raise an error
        if (result is None):
            raise BadSourceException(self.name)

        return result
