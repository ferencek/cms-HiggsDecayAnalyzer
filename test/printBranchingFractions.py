#!/usr/bin/env python

from ROOT import TFile, TH1F

file = TFile('decay_histo.root')

histo = file.Get('analyzer/h1_DecayPdgId')

total = histo.GetEntries()

decayModes = {
  4:  'H->cc',
  5:  'H->bb',
  15: 'H->tautau',
  21: 'H->gg',
  22: 'H->gammagamma',
  23: 'H->ZZ',
  24: 'H->WW',
}

for decay in decayModes.keys():
  bin = histo.GetXaxis().FindBin(float(decay))
  print 'Br(' + decayModes[decay] + ') = ' + str(histo.GetBinContent(bin)/total)
