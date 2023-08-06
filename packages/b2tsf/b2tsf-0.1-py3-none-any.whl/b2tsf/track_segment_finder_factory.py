from b2tsf.belle_CDC_frame import CDCFrame
from b2tsf.track_segment_finder_LUT5 import TrackSegmentFinderLUT5
from b2tsf.track_segment_finder_LUT9 import TrackSegmentFinderLUT9
from b2tsf.track_segment_finder_hourglas import TrackSegmentFinderHourglas

class TrackSegmentFinderFactory:
    """
    Factory class TrackSegmentFinderFactory instantiates any necessary track segment
    finders and returns them to the end user. Multiple functions are hidden
    behind generic caller functions and type of function call or track
    segment finder is defined by mode parameter.
    ---------------------------------------------------------------------------
    Possible modes for constructor:
    ---------------------------------------------------------------------------
    mode='Unger':   Not yet implemented

    mode='LUT':     Baseline algorithm implementing a 5 bit bin look up tables.

    mode='LUT9':    Algorithm implementing a 9 bit bin look up tables.

    mode='Neuro':   Not yet implemented
    ---------------------------------------------------------------------------
    Methods:
    ---------------------------------------------------------------------------
    set_patterns:       Callable from track segment finder in mode 'LUT9'. Throws
                    warning otherwise. Gives access to dictionary setting of
                    LUT9 track segement finder

    get_hit_list:       Returns list of hits, e.g. datapoints of internal cdc
                    frame. Data format can be choosen between
                    'native' and 'r_theta'.

    get_number_of_hits: Returns number of hits. Throws warning if mode is not
                    set to 'hits' for track segment finder. In this case number
                    of possible hit map hits would be reported.

    detect:             Detect hits and returns internal frame as out frame.

    clear:              Clears data from internal frame without recreating the
                    TrackSegmentFinder object.

    """
    def __init__(self,mode,**kwargs):
        new_frame = CDCFrame(0)
        if(mode == 'hourglas'):
            if 'lr_lut_path' in kwargs.keys():
                self.__tsf = TrackSegmentFinderHourglas(new_frame,lr_lut_path=kwargs['lr_lut_path'])
            else:
                warnings.warn("No 'lr_lut_path' declared. Fallback to default path.")
                self.__tsf = TrackSegmentFinderHourglas(new_frame)
        elif(mode == 'LUT5'):
            self.__tsf = TrackSegmentFinderLUT5(new_frame)
        elif(mode == 'LUT9'):
            self.__tsf = TrackSegmentFinderLUT9(new_frame)
        else:
            raise ValueError(mode)
        self.mode = mode


    def set_patterns(self,binmode,patterns_lower,patterns_upper):
        if(self.mode == 'LUT9'):
            self.__tsf = self.__tsf.set_patterns(binmode,patterns_lower,patterns_upper)
        else:
            warnings.warn("This TSF mode can not be configured.")
        return self


    def get_hit_list(self,format='native'):
        return self.__tsf.get_frame().get_hit_list(format)


    def get_number_of_hits(self):
        n_hits = self.__tsf.get_frame().get_number_of_hits()

        if(self.__tsf.mode == 'hits'):
            pass
        else:
            warnings.warn("TSF mode is not set to 'hits'. This can lead to unwanted behavior.")

        return n_hits


    def detect(self,frame_in,mode='hits'):
        return self.__tsf.detect(frame_in,mode)


    def clear(self):
        return self.__tsf.clear()
