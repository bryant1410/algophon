from algophon.symbols import UNKNOWN, UNDERSPECIFIED
from algophon.seg import Seg

import pkgutil

class SegInv:
    '''
    A class representing an inventory of phonological segments (Seg objects).
    '''
    def __init__(self, 
                 ipa_file_path: str=None, 
                 sep: str='\t'
        ):
        self._ipa_source = f'Panphon (https://github.com/dmort27/panphon)' if ipa_file_path is None else ipa_file_path
        self.ipa_file_path = ipa_file_path # uses Panphon features (https://github.com/dmort27/panphon) by default
        self.sep = sep

        # load the _seg_to_feat_vec map
        self._load_seg_to_feat_dict()

        # stores the Seg objects in the SegInv
        self.segs = set()

        # maps ipa symbols to their Seg object in the SegInv
        self._ipa_to_seg = dict()

    def __str__(self) -> str:
        return f'SegInv of size {len(self)}'
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __len__(self) -> int:
        return len(self.segs)
    
    def __iter__(self):
        return self.segs.__iter__()
    
    def __contains__(self, seg: object):
        '''
        :seg: Can be any of the following:
            - str IPA symbol
            - Seg object

        :return: True if the :seg: is in the alphabet, False if not
        '''
        return seg in self.segs
    
    def __getitem__(self, seg: object):
        '''
        :seg: Can be any of the following:
            - str IPA symbol
            - Seg object

        :return: the Seg object corresponding to :seg: if present, otherwise KeyError is raised
        '''
        if seg not in self:
            raise KeyError(f'{seg} of type {type(seg)} is not in the SegInv')
        return self._ipa_to_seg[seg]

    def _load_seg_to_feat_dict(self) -> None:
        self._seg_to_feat_vec = dict()
        # with open(self.ipa_file_path, 'r') as f: # load IPA file
        data = pkgutil.get_data(__name__, "ipa.txt")

        if self.ipa_file_path is None:
            lines = data.decode('utf-8').strip().split('\n')
        else:
            with open(self.ipa_file_path, 'r') as f:
                lines = f.readlines()
        for i, line in enumerate(lines): # iterate over lines
            line = line.strip().split(self.sep)
            seg, feats = line[0], line[1:] # extract the IPA segment and its features
            if i == 0: # extract the header
                self.feature_space = feats
            else: # add the segment to the dict
                self._seg_to_feat_vec[seg] = feats

    def add(self, ipa_seg: str) -> bool:
        '''
        :ipa_seg: a IPA segment in str form

        :return: True if the addition was successful
        '''
        if ipa_seg in self:
            return True
        if ipa_seg not in self._seg_to_feat_vec:
            raise KeyError(f'Segment {ipa_seg} is not in the IPA data from {self._ipa_source}.')
        feat_vec = self._seg_to_feat_vec[ipa_seg] # get the feature vector
        features = dict((feat, feat_vec[idx]) for idx, feat in enumerate(self.feature_space)) # convert the vector to dict form
        seg = Seg(ipa=ipa_seg, features=features)
        self.segs.add(seg)
        self._ipa_to_seg[ipa_seg] = seg
        return True

    def add_segments(self, ipa_segs: object) -> None:
        '''
        :ipa_segs: an iterable of IPA segments, each in str form

        :return: None
        '''
        for ipa in ipa_segs:
            self.add(ipa)