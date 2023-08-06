import numpy
import warnings
import plotly.graph_objects as go
from b2tsf.belle_CDC_layer import CDCLayer
from b2tsf.belle_CDC_frame import CDCFrame

class TrackSegmentFinderLUT5:
    """
    Track Segement Finder implenmenting a 5 bit look up table solution.
    TODO: Legacy implementation using numpy instead of ByteArray. Poor performance!

    ---------------------------------------------------------------------------
    Methods:
    ---------------------------------------------------------------------------
    detect:     Detects hits in incoming frame <frame_in> and saves result in
                internal data strucutre. Two possible detetction modes are
                available. 'hits' returns real hardware hits whereas 'candidates'
                returns all hit candidates of a hit bin.

    get_frame:  Retruns internal data frame as reference.

    clear:      Clears internal data structure.

    """
    def __init__(self,frame):
        self.__frame = frame
        self.__binsize = 5
        self.__binnumber = 16
        self.__binlayer = 2
        self.mode = 'hits'


    def __detect_hit(self,hitmap):
        """
        Implementation of per bin detection algorithm. For detailed description and index
        definiton checks thesis documentation.
        TODO: Insert Page
        """
        result = (numpy.array_equal(hitmap, [1,1,1,1,1])) or \
                 (numpy.array_equal(hitmap, [1,0,0,1,1])) or \
                 (numpy.array_equal(hitmap, [0,0,1,1,1])) or \
                 (numpy.array_equal(hitmap, [1,1,0,0,1])) or \
                 (numpy.array_equal(hitmap, [0,1,1,1,0])) or \
                 (numpy.array_equal(hitmap, [1,1,1,0,0]))
        return result


    def __populate_bin(self,seg_pre, seg_act, seg_suc, edge_hit=True):
        """
        Populate bins for detection algorithm. Each segment has got 32 bins as specified
        in the alogrithm description in thesis. Furthermore edge_hits of sectors can be
        toggeled on/off.
        This function returns bins of a layer segment.
        """

        hit_bin = 32 * [None]

        if(edge_hit):
            # Circulation counterclockwise - successor left, predecessor right
            hit_bin[0] = [seg_act[1,0],seg_pre[1,15],seg_act[0,1],seg_act[0,0],seg_pre[0,15]]
            hit_bin[15] = [seg_act[1,15],seg_act[1,14],seg_suc[0,0],seg_act[0,15],seg_act[0,14]]
            hit_bin[16] = [seg_act[4,1],seg_act[4,0],seg_pre[4,15],seg_act[3,0],seg_pre[3,15]]
            hit_bin[31] = [seg_suc[4,0],seg_act[4,15],seg_act[4,14],seg_act[3,15],seg_act[3,14]]
        else:
            hit_bin[0] = [seg_act[1,0],0,seg_act[0,1],seg_act[0,0],0]
            hit_bin[15] = [seg_act[1,15],seg_act[1,14],0,seg_act[0,15],seg_act[0,14]]
            hit_bin[16] = [seg_act[4,1],seg_act[4,0],0,seg_act[3,0],0]
            hit_bin[31] = [0,seg_act[4,15],seg_act[4,14],seg_act[3,15],seg_act[3,14]]

        for i in range(1,16-1):
            hit_bin[i] = [seg_act[1,i],seg_act[1,i-1],seg_act[0,i+1],seg_act[0,i],seg_act[0,i-1]]

        for i in range(1,16-1):
            hit_bin[i+16] = [seg_act[4,i+1],seg_act[4,i],seg_act[4,i-1],seg_act[3,i],seg_act[3,i-1]]

        return hit_bin


    def __check_layer_hit(self,layer_in, edge_hit=True):
        """
        Checks frame layer <layer_in> for hits. Using edge_hit True/False segemnt edge mode can be
        choosen. For production use edge_hit=True as non edge_hit is only used for hardware module
        testing.
        """
        n_segs = layer_in.n_segs
        hits = numpy.zeros(shape=(n_segs,32))
        # Segment 0
        seg_pre = layer_in.get_segment(n_segs-1)
        seg_act = layer_in.get_segment(0)
        seg_suc = layer_in.get_segment(1)
        hit_bin = self.__populate_bin(seg_pre, seg_act, seg_suc,edge_hit)
        hits[0] = numpy.array(list(map(self.__detect_hit, hit_bin)))
        # Inner segments
        for i in range (1,n_segs-1):
            seg_pre = layer_in.get_segment(i-1)
            seg_act = layer_in.get_segment(i)
            seg_suc = layer_in.get_segment(i+1)
            hit_bin = self.__populate_bin(seg_pre, seg_act, seg_suc,edge_hit)
            hits[i] = numpy.array(list(map(self.__detect_hit, hit_bin)))
        # Segment n_seg
        seg_pre = layer_in.get_segment(n_segs-2)
        seg_act = layer_in.get_segment(n_segs-1)
        seg_suc = layer_in.get_segment(0)
        hit_bin = self.__populate_bin(seg_pre, seg_act, seg_suc,edge_hit)
        hits[n_segs-1] = numpy.array(list(map(self.__detect_hit, hit_bin)))

        return hits


    def __detect_hits(self,frame_in):
        """
        Detects hits of all layers in <frame_in> and saves output in tsf frame.
        Hardcoded to layer 1...8, because hardware implementation for layer 0 is
        non existent. This feature could be implemented later.

        Step 1: Calculate hits for each layer. Returns 2D Array of hits
                with indices <segment_id> whose range depends on the layer
                and 0...31 for each checked hit bin inside the dection algorithm.
                E.g. Bin 5 in Segment 3 was hit => hits[2,4] == True

        Step 2: Find all hits and fill output frame accordingly.
        """
        for layer_id in range(1,9):
            layer_in = frame_in.get_layer(layer_id)
            layer_segments = self.__frame.get_layer(layer_id).get_tsf_segments()
            hits = self.__check_layer_hit(layer_in,True)

            for i in range(0,layer_in.n_segs):
                segment_id = i
                for j in range(0,32):
                    if(hits[segment_id,j] == True):
                        if(j < 16):
                            layer_segments[segment_id,0,j] = 1
                        else:
                            layer_segments[segment_id,4,j-16] = 1

        return self.__frame


    def __detect_candidates(self,frame_in):
        """
        Detects hits of all layers in <frame_in> and saves output in tsf frame.
        Hardcoded to layer 1...8, because hardware implementation for layer 0
        is non existent. This feature could be implemented later.

        Step 1: Calculate hits for each layer. Returns 2D Array of hits
                with indices <segment_id> whose range depends on the layer
                and 0...31 for each checked hit bin inside the dection
                algorithm, e.g. Bin 5 in Segment 3 was hit => hits[2,4] == True

        Step 2: Find all hits and fill output frame accordingly.

        Identical to __detect_hits() except that it populates all hit bin
        candidates to the internal output data frame.
        """
        for layer_id in range(1,9):
            layer_in = frame_in.get_layer(layer_id)
            layer_segments = self.__frame.get_layer(layer_id).get_tsf_segments()
            hits = self.__check_layer_hit(layer_in,True)

            for i in range(0,layer_in.n_segs):
                segment_id = i
                for j in range(0,32):
                    if(hits[segment_id,j] == True):
                        if(j==0):
                            layer_segments[segment_id-1,0,15] = 1
                            layer_segments[segment_id,0,0] = 1
                            layer_segments[segment_id,0,1] = 1
                            layer_segments[segment_id-1,1,15] = 1
                            layer_segments[segment_id,1,0] = 1
                        elif(j==15):
                            layer_segments[segment_id,0,14] = 1
                            layer_segments[segment_id,0,15] = 1
                            layer_segments[(segment_id+1)%layer_in.n_segs,0,0] = 1
                            layer_segments[segment_id,1,14] = 1
                            layer_segments[segment_id,1,15] = 1
                        elif(j < 16):
                            layer_segments[segment_id,0,j-1] = 1
                            layer_segments[segment_id,0,j] = 1
                            layer_segments[segment_id,0,j+1] = 1
                            layer_segments[segment_id,1,j-1] = 1
                            layer_segments[segment_id,1,j] = 1
                        elif(j==16):
                            layer_segments[segment_id-1,4,15] = 1
                            layer_segments[segment_id,4,0] = 1
                            layer_segments[segment_id,4,1] = 1
                            layer_segments[segment_id-1,3,15] = 1
                            layer_segments[segment_id,3,0] = 1
                        elif(j==31):
                            layer_segments[segment_id,4,14] = 1
                            layer_segments[segment_id,4,15] = 1
                            layer_segments[(segment_id+1)%layer_in.n_segs,4,0] = 1
                            layer_segments[segment_id,3,14] = 1
                            layer_segments[segment_id,3,15] = 1
                        else:
                            layer_segments[segment_id,4,j-1-16] = 1
                            layer_segments[segment_id,4,j-16] = 1
                            layer_segments[segment_id,4,j+1-16] = 1
                            layer_segments[segment_id,3,j-1-16] = 1
                            layer_segments[segment_id,3,j-16] = 1

        return self.__frame


    def detect(self,frame_in,mode='hits'):
        """
        Interface function for detection algorithm.
        """
        frame_out = None
        self.mode = mode
        if(mode == 'hits'):
            frame_out = self.__detect_hits(frame_in)
        elif(mode == 'candidates'):
            frame_out = self.__detect_candidates(frame_in)
        else:
            raise ValueError(mode)

        return frame_out


    def get_frame(self):
        return self.__frame


    def clear(self):
        self.__frame = self.__frame.clear()
        return self.__frame
