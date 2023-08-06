from .base import *
from .util import *

#non-standard libraries
import pandas as pd

#READER TYPES 
READER_SIMPLE_CSV_EXCEL = 'reader_singer_csv'
READERTYPES.extend([
    READER_SINGER_CSV
])

#WRITER TYPES
#directory
WRITER_SIMPLE_CSV_EXCEL = 'writer_singer_csv'
WRITERTYPES.extend([
    WRITER_SINGER_CSV
])

#@registerReader 
class BaseSingerReader(BaseReader):
    def __init__(self, cfg=None, src=None):
        super().__init__(cfg=cfg, src=src)
        
    @classmethod
    def type(cls):
        '''Returns key used to regsiter Reader type'''
        return #READER_SIMPLE_CSV_EXCEL
        
    @classmethod
    def ok(cls, src):
        '''Returns key used to regsiter Reader type'''
        #if isinstance(src, str) and (src[-4:]=='.csv' or src[-5:]=='.xlsx'):
        #    return True
        return False #don't register BaseReader
        
    def read(self):
        '''Returns dataframe based on config'''
        """if self._cfg:
            c = self._cfg
            if 'csv' in c.keys():
                return pd.read_csv(filepath_or_buffer=c['csv'])
            elif 'excel' in c.keys():
                return pd.read_excel(filepath_or_buffer=c['excel'])
            else:
                pass
        s = self._src
        if isinstance(src, str) and (src[-4:]=='.csv'):
            return pd.read_csv(filepath_or_buffer=s)
        elif isinstance(src, str) and (src[-5:]=='.xlsx'):
            return pd.read_excel(filepath_or_buffer=s)
        else:
            raise TypeError("Invalid reader source")
            """

#@registerWriter 
class BaseSingerWriter(BaseWriter):
    def __init__(self, cfg=None, tar=None):
        super().__init__(cfg=cfg, tar=tar)
        
    @classmethod
    def type(cls):
        '''Returns key used to regsiter Reader type'''
        return #WRITER_SIMPLE_CSV_EXCEL
        
    @classmethod
    def ok(cls, tar):
        '''Returns key used to register type'''
        #if isinstance(tar, str) and (tar[-4:]=='.csv' or tar[-5:]=='.xlsx'):
        #    return True
        return False #don't register BaseReader
        
    def write(self, data):
        '''Writes dataframe based on config'''
        """
        if self._cfg:
            c = self._cfg
            df = data[DATATYPE_DATAFRAME]['active']
            if 'csv' in c.keys():
                return df.to_csv(c['csv'], index=False)
            elif 'excel' in c.keys():
                return df.to_excel(c['excel'], index=False)
            else:
                pass
        t = self._tar
        if isinstance(t, str) and (t[-4:]=='.csv'):
            return pd.read_csv(filepath_or_buffer=s)
        elif isinstance(t, str) and (t[-5:]=='.xlsx'):
            return pd.read_excel(filepath_or_buffer=s)
        else:
            raise TypeError("Invalid writer target")
            """