import numpy
from bitarray import bitarray
from bitarray import frozenbitarray
import warnings
import plotly.graph_objects as go
from b2tsf.belle_CDC_layer import CDCLayer
from b2tsf.belle_CDC_frame import CDCFrame

class TrackSegmentFinderLUT9:
    """
    Track Segement Finder implenmenting a 9 bit look up table solution.

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
        self.mode = 'hits'
        self.__binsize = 9
        self.__binnumber = 16
        self.__binlayer = 2


    def __init_patterns(self,patterns):
        """
        Configure detection patterns during track segment finder construction. True
        candidate patterns are given as string list in the format defined in thesis
        documenation. As keys must be constant to be hashable this function must be
        be called seperately.
        Returns dict of bit patterns.
        """
        keys = []
        values = []
        for i in range(2**self.__binsize):
            key_pattern = f'{i:09b}'
            keys.append(frozenbitarray(key_pattern))
            values.append(key_pattern in patterns)
        return dict(zip(keys,values))


    def __detect_hit(self,hitmap_zip,seg_hits):
        """
        Implementation of per bin detetion algorithm, e.g. checking against
        look up table in form of a hash map. hitmap_zip contains both bins
        for upper and lower hitmap.
        This function requires a predefined array for performance reasons. This
        way the creation of many small arrays can be avoided by slicing.
        """
        hitmap_lower, hitmap_upper = hitmap_zip
        if(self.__binmode == 'lower' or self.__binmode == 'both'):
            for i in range(self.__binnumber):
                seg_hits[0,i] = self.__patterns_lower[hitmap_lower[i]]
        if(self.__binmode == 'upper' or self.__binmode == 'both'):
            for i in range(self.__binnumber):
                seg_hits[1,i] = self.__patterns_upper[hitmap_upper[i]]
        return seg_hits


    def __populate_bin(self,seg_pre, seg_act, seg_suc, edge_hit):
        """
        Populate bins for detection algorithm. Each segment has got 16 bins in 2 layers
        as specified in the alogrithm description in thesis. Furthermore edge_hits of
        sectors can be toggeled on/off.
        This function returns bins of a layer segment.
        """
        hit_bin_lower = [self.__binsize * bitarray() for i in range(self.__binnumber)]
        hit_bin_upper = [self.__binsize * bitarray() for i in range(self.__binnumber)]
        #Fill lower bins
        if(self.__binmode == 'lower' or self.__binmode == 'both'):
            if(edge_hit):
                hit_bin_lower[0] = frozenbitarray([
                    seg_act[2,1],seg_act[2,0],
                    seg_act[1,1],seg_act[1,0],seg_pre[1,15],
                    seg_act[0,2],seg_act[0,1],seg_act[0,0],seg_pre[0,15]])
                hit_bin_lower[14] = frozenbitarray([
                    seg_act[2,15],seg_act[2,14],
                    seg_act[1,15],seg_act[1,14],seg_act[1,13],
                    seg_suc[0,0],seg_act[0,15],seg_act[0,14],seg_act[0,13]])
                hit_bin_lower[15] = frozenbitarray([
                    seg_suc[2,0],seg_act[2,15],
                    seg_suc[1,0],seg_act[1,15],seg_act[1,14],
                    seg_suc[0,1],seg_suc[0,0],seg_act[0,15],seg_act[0,14]])
            else:
                hit_bin_lower[0] = frozenbitarray([
                    seg_act[2,1],seg_act[2,0],
                    seg_act[1,1],seg_act[1,0],0,
                    seg_act[0,2],seg_act[0,1],seg_act[0,0],0])
                hit_bin_lower[14] = frozenbitarray([
                    seg_act[2,15],seg_act[2,14],
                    seg_act[1,15],seg_act[1,14],seg_act[1,13],
                    0,seg_act[0,15],seg_act[0,14],seg_act[0,13]])
                hit_bin_lower[15] = frozenbitarray([
                    0,seg_act[2,15],
                    0,seg_act[1,15],seg_act[1,14],
                    0,0,seg_act[0,15],seg_act[0,14]])

            for i in range(1,self.__binnumber-2):
                hit_bin_lower[i] = frozenbitarray([
                    seg_act[2,i+1],seg_act[2,i],
                    seg_act[1,i+1],seg_act[1,i],seg_act[1,i-1],
                    seg_act[0,i+2],seg_act[0,i+1],seg_act[0,i],seg_act[0,i-1]])
        #Fill upper bins
        if(self.__binmode == 'upper' or self.__binmode == 'both'):
            if(edge_hit):
                hit_bin_upper[0] = frozenbitarray([
                    seg_act[4,2],seg_act[4,1],seg_act[4,0],seg_pre[4,15],
                    seg_act[3,1],seg_act[3,0],seg_pre[3,15],
                    seg_act[2,1],seg_act[2,0]])
                hit_bin_upper[14] = frozenbitarray([
                    seg_suc[4,0],seg_act[4,15],seg_act[4,14],seg_act[4,13],
                    seg_act[3,15],seg_act[3,14],seg_act[3,13],
                    seg_act[2,15],seg_act[2,14]])
                hit_bin_upper[15] = frozenbitarray([
                    seg_suc[4,1],seg_suc[4,0],seg_act[4,15],seg_act[4,14],
                    seg_suc[3,0],seg_act[3,15],seg_act[3,14],
                    seg_suc[2,0],seg_act[2,15]])
            else:
                hit_bin_upper[0] = frozenbitarray([
                    seg_act[4,2],seg_act[4,1],seg_act[4,0],0,
                    seg_act[3,1],seg_act[3,0],0,
                    seg_act[2,1],seg_act[2,0]])
                hit_bin_upper[14] = frozenbitarray([
                    0,seg_act[4,15],seg_act[4,14],seg_act[4,13],
                    seg_act[3,15],seg_act[3,14],seg_act[3,13],
                    seg_act[2,15],seg_act[2,14]])
                hit_bin_upper[15] = frozenbitarray([
                    0,0,seg_act[4,15],seg_act[4,14],
                    0,seg_act[3,15],seg_act[3,14],
                    0,seg_act[2,15]])

            for i in range(1,self.__binnumber-2):
                hit_bin_upper[i] = frozenbitarray([
                    seg_act[4,i+2],seg_act[4,i+1],seg_act[4,i],seg_act[4,i-1],
                    seg_act[3,i+1],seg_act[3,i],seg_act[3,i-1],
                    seg_act[2,i+1],seg_act[2,i]])

        return (hit_bin_lower,hit_bin_upper)


    def __check_layer_hit(self,layer_in, edge_hit):
        """
        Checks frame layer <layer_in> for hits. Using edge_hit True/False segemnt edge mode can be
        choosen. For production use edge_hit=True as non edge_hit is only used for hardware module
        testing.
        """
        n_segs = layer_in.n_segs
        hits = numpy.zeros(shape=(n_segs,self.__binlayer,self.__binnumber),dtype=int)
        #Segment 0
        seg_pre = layer_in.get_segment(n_segs-1)
        seg_act = layer_in.get_segment(0)
        seg_suc = layer_in.get_segment(1)
        hit_bin = self.__populate_bin(seg_pre, seg_act, seg_suc,edge_hit)
        hits[0,:,:] = self.__detect_hit(hit_bin, hits[0,:,:])
        #Inner segments
        for i in range (1,n_segs-1):
            seg_pre = layer_in.get_segment(i-1)
            seg_act = layer_in.get_segment(i)
            seg_suc = layer_in.get_segment(i+1)
            hit_bin = self.__populate_bin(seg_pre, seg_act, seg_suc,edge_hit)
            hits[i,:,:] = self.__detect_hit(hit_bin, hits[i,:,:])
        #Segment n_seg
        seg_pre = layer_in.get_segment(n_segs-2)
        seg_act = layer_in.get_segment(n_segs-1)
        seg_suc = layer_in.get_segment(0)
        hit_bin = self.__populate_bin(seg_pre, seg_act, seg_suc,edge_hit)
        hits[-1,:,:] = self.__detect_hit(hit_bin, hits[-1,:,:])

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
            #Calculate hits of layer
            hits = self.__check_layer_hit(layer_in,True)
            (seg_id_list,row_id_list,col_id_list) = numpy.nonzero(hits)
            for seg_id,row_id,col_id in zip(seg_id_list,row_id_list,col_id_list):
                if(row_id == 0):
                    layer_segments[seg_id,1,col_id] = 1
                else:
                    layer_segments[seg_id,3,col_id] = 1
        return self.__frame

    def __detect_candidates(self,frame_in):
        """
        Detects hits of all layers in <frame_in> and saves output in tsf frame.
        Hardcoded to layer 1...8, because hardware implementation for layer 0 is
        non existent. This feature could be implemented later.

        Step 1: Calculate hits for each layer. Returns 2D Array of hits
                with indices <segment_id> whose range depends on the layer
                and 0...31 for each checked hit bin inside the dection algorithm.
                E.g. Bin 5 in Segment 3 was hit => hits[2,4] == True

        Step 2: Find all hits and fill output frame accordingly.

        Identical to __detect_hits() except that it populates all hit bin
        candidates to the internal output data frame.
        """
        for layer_id in range(1,9):
            layer_in = frame_in.get_layer(layer_id)
            layer_segments = self.__frame.get_layer(layer_id).get_tsf_segments()
            #Calculate hits of layer
            hits = self.__check_layer_hit(layer_in,True)
            (seg_id_list,up_lo_id,col_id_list) = numpy.nonzero(hits)
            for seg_id,up_lo_id,col_id in zip(seg_id_list,up_lo_id,col_id_list):
                if(up_lo_id == 0):
                    if(col_id == 0):
                        layer_segments[seg_id-1,0,15] = 1
                        layer_segments[seg_id,0,0:3] = 1
                        layer_segments[seg_id-1,1,15] = 1
                        layer_segments[seg_id,1,0:2] = 1
                        layer_segments[seg_id,2,0:2] = 1
                    elif(col_id == 14):
                        layer_segments[seg_id,0,13:] = 1
                        layer_segments[(seg_id+1)%layer_in.n_segs,0,0] = 1
                        layer_segments[seg_id,1,13:] = 1
                        layer_segments[seg_id,2,14:] = 1
                    elif(col_id == 15):
                        layer_segments[seg_id,0,14:] = 1
                        layer_segments[(seg_id+1)%layer_in.n_segs,0,0:2] = 1
                        layer_segments[seg_id,1,14:] = 1
                        layer_segments[(seg_id+1)%layer_in.n_segs,1,0] = 1
                        layer_segments[seg_id,2,15] = 1
                        layer_segments[(seg_id+1)%layer_in.n_segs,2,0] = 1
                    else:
                        layer_segments[seg_id,0,col_id-1:col_id+3] = 1
                        layer_segments[seg_id,1,col_id-1:col_id+2] = 1
                        layer_segments[seg_id,2,col_id:col_id+2] = 1
                if(up_lo_id == 1):
                    if(col_id == 0):
                        layer_segments[seg_id-1,4,15] = 1
                        layer_segments[seg_id,4,0:3] = 1
                        layer_segments[seg_id-1,3,15] = 1
                        layer_segments[seg_id,3,0:2] = 1
                        layer_segments[seg_id,2,0:2] = 1
                    elif(col_id == 14):
                        layer_segments[seg_id,4,13:] = 1
                        layer_segments[(seg_id+1)%layer_in.n_segs,4,0] = 1
                        layer_segments[seg_id,3,13:] = 1
                        layer_segments[seg_id,2,14:] = 1
                    elif(col_id == 15):
                        layer_segments[seg_id,4,14:] = 1
                        layer_segments[(seg_id+1)%layer_in.n_segs,4,0:2] = 1
                        layer_segments[seg_id,3,14:] = 1
                        layer_segments[(seg_id+1)%layer_in.n_segs,3,0] = 1
                        layer_segments[seg_id,2,15] = 1
                        layer_segments[(seg_id+1)%layer_in.n_segs,2,0] = 1
                    else:
                        layer_segments[seg_id,4,col_id-1:col_id+3] = 1
                        layer_segments[seg_id,3,col_id-1:col_id+2] = 1
                        layer_segments[seg_id,2,col_id:col_id+2] = 1
        return self.__frame


    def get_frame(self):
        return self.__frame


    def set_patterns(self,binmode,patterns_lower,patterns_upper):
        """
        Creates patterns for lower and upper hit bins. Caution: This function is
        computational expensive!
        """
        self.__binmode = binmode
        if(binmode != 'lower' and binmode != 'upper' and binmode != 'both'):
            raise ValueError(binmode)
        self.__patterns_lower = self.__init_patterns(patterns_lower)
        self.__patterns_upper = self.__init_patterns(patterns_upper)
        return self


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
            raise ModeNotFoundError('Mode: ' + mode + 'does not exist. See documentation for valid arguments.')

        return frame_out


    def clear(self):
        self.__frame = self.__frame.clear()
        return self.__frame
