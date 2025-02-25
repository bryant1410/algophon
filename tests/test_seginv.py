import unittest
import sys
sys.path.append('../')
from algophon.seginv import SegInv

class TestSegInv(unittest.TestCase):
    def test_init(self):
        seginv = SegInv()
        assert(seginv is not None)

    def test_add(self):
        seginv = SegInv()
        
        seginv.add('i')
        assert(len(seginv) == 1)
        assert(seginv.segs == {'i'}) 

        seginv.add_segs({'p', 'b', 't', 'd'})
        assert(len(seginv) == 5)
        assert(seginv.segs == {'i', 'p', 'b', 't', 'd'}) 

        seginv.add_segs_by_str('eː n t j ə')
        assert(len(seginv) == 9)
        assert(seginv.segs == {'i', 'p', 'b', 't', 'd', 'eː', 'n', 'j', 'ə'}) 

    def test_get(self):
        seginv = SegInv()
        seginv.add('eː')
        assert(seginv['eː'].features == {'syl': '+', 'son': '+', 'cons': '-', 'cont': '+', 'delrel': '-', 'lat': '-', 'nas': '-', 
                                         'strid': '0', 'voi': '+', 'sg': '-', 'cg': '-', 'ant': '0', 'cor': '-', 'distr': '0', 'lab': '-',
                                         'hi': '-', 'lo': '-', 'back': '-', 'round': '-', 'velaric': '-', 'tense': '+', 'long': '+', 
                                         'hitone': '0', 'hireg': '0'})
        
    def test_extension(self):
        seginv = SegInv()
        seginv.add_segs({'a', 'e', 'i', 'o', 'u', 'p', 'b', 't', 'd', 'k', 'g', 's', 'm', 'n'})
        assert(seginv.extension({'+syl'}) == {'a', 'e', 'i', 'o', 'u'})
        assert(seginv.extension({'+cons'}) == {'p', 'b', 't', 'd', 'k', 'g', 's', 'm', 'n'})
        assert(seginv.extension({'-syl', '+voi'}) == {'b', 'd', 'g', 'm', 'n'})

    def test_extension_complement(self):
        seginv = SegInv()
        seginv.add_segs({'a', 'e', 'i', 'o', 'u', 'p', 'b', 't', 'd', 'k', 'g', 's', 'm', 'n'})
        assert(seginv.extension_complement({'+syl'}) == {'p', 'b', 't', 'd', 'k', 'g', 's', 'm', 'n'})
        assert(seginv.extension_complement({'+cons'}) == {'a', 'e', 'i', 'o', 'u'})
        assert(seginv.extension_complement({'-syl', '+voi'}) == {'a', 'e', 'i', 'o', 'u', 'p', 't', 'k', 's'})

    def test_feature_intersection(self):
        seginv = SegInv()
        vs = {'a', 'e', 'i', 'o', 'u'}
        seginv.add_segs(vs)
        assert(seginv.feature_intersection(vs) == {'+cont', '-sg', '-delrel', '+tense', '-long', '-cons', '-velaric',
                                                   '-nas', '+syl', '-cg', '+voi', '-lat', '+son', '-cor'})
        
    def test_feature_diff(self):
        seginv = SegInv()
        seginv.add_segs({'t', 'd'})
        assert(seginv.feature_diff('t', 'd') == {'voi'})

        seginv.add_segs({'i', 'e'})
        assert(seginv.feature_diff('i', 'e') == {'hi'})

if __name__ == "__main__":
    unittest.main()