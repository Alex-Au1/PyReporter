import pandas as pd
from .df_processor import DFProcessor
from ..view import ProgressSubject
from ..events import OutEvent
from typing import Optional, Union, Dict


DEFAULT_POST_PROCESSOR_KEY = "default"


# AbsSource: An abstract Source
class AbsSource():
    def __init__(self, post_processor: Optional[Union[Dict[str, DFProcessor], DFProcessor]] = None, progress_checker: Optional[ProgressSubject] = None):
        # store the processors used to transform the source into a dataframe
        if (post_processor is None or isinstance(post_processor, dict)):
            self.post_processor = post_processor
        else:
            self.post_processor = {DEFAULT_POST_PROCESSOR_KEY: post_processor}

        self.progress_checker = progress_checker
        self.name = None


    def __getitem__(self, key: str):
        return self.post_processor[key]


    def __setitem__(self, key: str, value: DFProcessor):
        assert isinstance(isinstance(value, DFProcessor))
        self.post_processor[key] = value


    # notify(out_event): Prints update on the progress for the Source
    def notify(self, out_event: OutEvent):
        if (self.progress_checker is not None):
            self.progress_checker.notify(out_event)


    # import_data(): imports the data to become a Pandas Dataframe
    async def import_data(self) -> pd.DataFrame:
        pass


    # process(df): Prepares the data for use in the calculations
    async def prepare(self, post_processor_name: str = DEFAULT_POST_PROCESSOR_KEY):
        df = await self.import_data()

        if (self.post_processor is not None):
            result = None
            
            try:
                result = self.post_processor[post_processor_name].process(df)
            except KeyError as e:
                if (isinstance(self.post_processor, dict)):
                    key = list(self.post_processor.keys())[0]
                    result = self.post_processor[key].process(df)

                    return result
                else:
                    raise e
            else:
                return result
        else:
            return df
