# algophon

**Code for working on computational phonology and morphology in Python.** 

The project is based on code developed by [Caleb Belth](https://cbelth.github.io/) during the course of his PhD; the title of his [dissertation](https://cbelth.github.io/public/assets/documents/belth_dissertation.pdf), *Towards an Algorithmic Account of Phonological Rules and Representations*, serves as the origin for the repository's name *algophon*.

This is a <span style="color:orange">work in progress</span>. The pypi distribution and documentation will be updated as the project progresses! The initial plan for the project is to include:
1. Handy tools for working with strings of phonological segments.
2. Implementations of computational learning models.

Item (1) will be implemented first.

**Suggestions are welcome!**

## Install

```
pip install algophon
```

## Working With Strings of Segments

The code at the top level of the package provides some nice functionality for easily working with strings of phonological segments.

The following examples assume you have imported the appropriate classes:

```python
>>> from algophon import Seg, SegInv, SegStr, NatClass
```

### Segments: `Seg`

**A class to represent a phonological segment.**

You are unlikely to be creating `Seg` objects yourself very often. They will usually be constructed internally by other parts of the package (in particular, see `SegInv` and `SegStr`). However, if you ever need to, creating a `Seg` object requires the following arguments:
- `ipa`: a `str` IPA symbol
- `features` (optional): a `dict` of features mapping to their corresponding values

```python
>>> seg = Seg(ipa='i', features={'syl': '+', 'voi': '+', 'stri': '0'})
```

What is important to know is how `Seg` objects behave, and why they are handy.

<span style="color:green">**First**</span>, in the important respects `Seg` behaves like the `str` IPA segment used to create it.

If you `print` a `Seg` object, it will print its IPA:

```python
>>> print(seg)
i
```

If you compare a `Seg` object to a `str`, it will behave like it is the IPA symbol:

```python
>>> print(seg == 'i')
True
>>> print(seg == 'e')
False
```

A `Seg` object hashes to the same value as its IPA symbol:

```python
>>> print(len({seg, 'i'}))
1
>>> print('i' in {seg}, seg in {'i'})
True True
```

<span style="color:green">**Second**</span>, in the important respects `Seg` behaves like a feature bundle (see also the other classes, where other benefits will become clear).

```python
>>> print(seg.features['syl'])
+
```

<span style="color:green">**Third**</span>, `Seg` handles IPA symbols that are longer than one unicode char.

```python
>>> tsh = Seg(ipa='t͡ʃ')
>>> print(tsh)
t͡ʃ
>>> print(len(tsh))
1
>>> from algophon.symbols import LONG # see description of symbols below
>>> long_i = Seg(ipa=f'i{LONG}')
>>> print(long_i)
iː
>> print(len(long_i))
1
```

### Segment Inventory: `SegInv`

**A class to represent an inventory of phonological segments (Seg objects).**

A `SegInv` object is a collection of `Seg` objects. A `SegInv` requires no arguments to construct, though it provides two optional arguments:
- `ipa_file_path`: a `str` pointing to a file of segment-feature mappings.
- `sep`: a `str` specifying the column separator of the `ipa_file_path` file.

By default, `SegInv` uses [Panphon](https://github.com/dmort27/panphon) (Mortensen et. al., 2016) features. The optional parameters allow you to use your own features. The file at `ipa_file_path` must be formatted like this:
- The first row must be a header of feature names, separated by the `sep` (by default, `\t`)
- The first column must contain the segment IPAs (the header row can have anything, e.g., `SEG`)
- The remaining columns (non first row) must contain the feature values.

When a `SegInv` object is created, it is empty:

```python
>>> seginv = SegInv()
>>> seginv
SegInv of size 0
```

You can add segments by the `add`, `add_segments`, and `add_segments_by_str` methods:

```python
>>> seginv.add('i')
>>> print(seginv.segs)
{i}
>>> seginv.add_segs({'p', 'b', 't', 'd'})
>>> print(seginv.segs)
{b, t, d, i, p}
>>> seginv.add_segs_by_str('eː n t j ə') # segments in str must be space-separated
>>> print(seginv.segs)
{b, t, d, i, j, n, p, ə, eː}
```

The reason that `add_segs_by_str` requires the segments be space-separated is because not all IPA symbols are only one char (e.g., `'eː'`). Moreover, this is consistent with the [Sigmorphon](https://github.com/sigmorphon) challenges data format commonly used in morphophonology tasks.

These `add*` methods automatically create `Seg` objects and assign them `features` based on either Panphon (default) or the `ipa_file_path` file.

```python
>>> print(seginv['eː'].features)
{'syl': '+', 'son': '+', 'cons': '-', 'cont': '+', 'delrel': '-', 'lat': '-', 'nas': '-', 'strid': '0', 'voi': '+', 'sg': '-', 'cg': '-', 'ant': '0', 'cor': '-', 'distr': '0', 'lab': '-', 'hi': '-', 'lo': '-', 'back': '-', 'round': '-', 'velaric': '-', 'tense': '+', 'long': '+', 'hitone': '0', 'hireg': '0'}
```

This also demonstrates that `seginv` operates like a dictionary in that you can retrieve and check the existence of segments by their IPA.

```python
>>> 'eː' in seginv
True
```

### Strings of Segments: `SegStr`

**A class to represent a sequence of phonological segments (Seg objects).**

The class `SegStr` allows for handling several tricky aspects of IPA sequences. It is common practice to represent strings of IPA sequences in a space-separated fashion such that, for example, [eːntjə] is represented `'eː n t j ə'`.

Creating a `SegStr` object requires the following arguments:
  - `segs`: a collection of segments, which can be in any of the following formats:
    - str of IPA symbols, where each symbol is separated by a space ' ' (**most common**)
    - list of IPA symbols
    - list of Seg objects
  - `seginv`: a `SegInv` object

```python
>>> seginv = SegInv() # init SegInv
>>> seq = SegStr('eː n t j ə', seginv)
>>> print(seq)
eːntjə
```

Creating the `SegStr` object automatically adds the segments in the object to the `SegInv` object.

```python
>>> print(seginv.segs)
{ə, t, n, j, eː}
```

For clean visuzliation, `SegStr` displays the sequence of segments without spaces, as `print(seq)` shows above. But internally a `SegStr` object knows what the segments are:

```python
>>> print(len(seq))
5
>>> seq[0]
eː
>>> type(seq[0]) # indexing returns a Seg object
<class 'algophon.seg.Seg'>
>>> seq[-2:]
jə
>>> type(seq[-2:]) # slicing returns a new SegStr object
<class 'algophon.segstr.SegStr'>
>>> seq[-2:] == 'j ə' # comparison to str objects works as expected
True
>>> seq[-2:] == 'ə n'
False
```

`SegStr` also implements equivalents of useful str methods.

```python
>>> seq.endswith('j ə')
True
>>> dim_sufx = seq[-2:]
>>> seq.endswith(dim_sufx)
True
>>> seq.startswith(seq[:-2])
True
```

A `SegStr` object hashes to the value of its (space-separated) string:

```python
>>> len({seq, 'eː n t j ə'})
1
>>> seq in {'eː n t j ə'}
True
```

### Natural Class: `NatClass`

**A class to represent a Natural class, in the sense of sets of segments represented intensionally as conjunctions of features.**

```python
>>> son = NatClass(feats={'+son'}, seginv=seginv)
>>> son
[+son]
>>> 'ə' in son
True
>>> 'n' in son
True
>>> 't' in son
False
```

The class also allows you to get the natural class's extension and the extension's complement, relative to the `SegInv` (in our example, only `{ə, t, n, j, eː}` are in `seginv`):

```python
>>> son.extension()
{eː, j, ə, n}
>>> son.extension_complement()
{t}
```

You can also retrieve an extension (complement) directly from a `SegInv` object without creating a `NatClass` obj:

```python
>>> seginv.extension({'+syl'})
{ə, eː}
>>> seginv.extension_complement({'+syl'})
{j, t, n}
```

### Symbols: The `symbols` module

The `symbols` module (techincally just a file...) contains a number of constant variables that store some useful symbols:

```python
LWB = '⋊'
RWB = '⋉'
SYL_BOUNDARY = '.'
PRIMARY_STRESS = 'ˈ'
SEC_STRESS = 'ˌ'
LONG = 'ː'
NASALIZED = '\u0303' # ◌̃
UNDERSPECIFIED = '0'
UNK = '?'
NEG = '¬'
```

These can be accessed like this:

```python
>>> from algophon.symbols import *
>>> NASALIZED
'̃'
>>> f'i{LONG}'
iː
```

## Learning Models

<span style="color:orange">Work in Progress</span>

## Citation

If you use this package in your research, you can use the following citation:

```bibtex
@phdthesis{belth2023towards,
  title={{Towards an Algorithmic Account of Phonological Rules and Representations}},
  author={Belth, Caleb},
  year={2023},
  school={{University of Michigan}}
}
```

## References

- Mortensen, D. R., Littell, P., Bharadwaj, A., Goyal, K., Dyer, C., & Levin, L. (2016, December). Panphon: A resource for mapping IPA segments to articulatory feature vectors. In Proceedings of COLING 2016, the 26th International Conference on Computational Linguistics: Technical Papers (pp. 3475-3484).