# altFACS

![build](https://github.com/BoHuangLab/altFACS/workflows/Project%20Tests/badge.svg)
![License](https://img.shields.io/github/license/BoHuangLab/altFACS)

Author: David Brown

Last Edited: 2020-August-07

## Aim:
This package is intended to standardise and simplify the investigation of protein-protein interactions by flow cytometry.

## Explanation:
In the [Huang Lab](http://huanglab.ucsf.edu/) we are interested in developing new tools to examine biological interactions. Split fluorescent proteins have proven to be a useful tool for the tagging and study of endogenous proteins in living cells, and we have been trying to maximise their utility. Appropriate use of a split fluorescent protein as a probe requires a good understanding of the complementation process, whereby the two halves of the split meet and fold to form the mature fluorescent protein. Complementation can be studied biochemically, however we can exploit the self-reporting nature of fluorescent proteins to study complementation in vivo by microscopy or or flow cytometry which offers a higher throughput. 

Flow cytometry and fluorescence activated cell sorting (FACS) are more frequently used to distinguish cell populations based on a characteristic intensity profile. In our case we often use it to study how proteins behave at a range of concentrations. This alternative approach to FACS is the main purpose of the altFACS package.

## Example Plots:
![Example altFACS plots](https://github.com/BoHuangLab/altFACS/blob/main/images/mNG3_mCloGFP_altFACS_example.png)

### Example altFACS Plots:
- **A.** Raw flow cytometry events. 
- **B.** Scatter gating. Events from **A** after events saturating in any channel have been removed from all channels. Events likely to correspond to live cells have been gated based on a contour map.
- **C.** Singlet gating. Events from **B** after likely to contain more than one cell (below the line) are excluded.
- **D.** Negative control without transfection. Events from **C** after fluorescence gates have been set to contain 99% of the population.
- **E.** Transfected with CloGFP(1-10) only. 
- **F.** Positive control with full length sfGFP::CTLA:T2A:mTagBFP 
- **G.** Fitting of full length GFP in BFP+ cells. altFACS facilitates model fitting to flow cytometry data.
- **H.** CloGFP with wild type GFP11::CTLA:T2A:mTagBFP. 
- **I.** CloGFP with Y9F mutant GFP11::CTLA:T2A:mTagBFP. 
- **J-L.** Data from panels **G-I** rescaled for comparison. 

We conclude that split CloGFP complementation efficiency is much less than 100%, and that the Y9F mutation in the GFP11 fragment has no impact of split CloGFP complementation efficiency.

## Installation
Currently, altFACS is available on GitHub or on the [test.Pypi](https://test.pypi.org/project/altFACS/1.0.7/) site. 
Most [requirements](https://github.com/BoHuangLab/altFACS/blob/master/requirements.txt) will install automatically, but you may need to install [fcsparser](https://github.com/eyurtsev/fcsparser) before installing altFACS.






