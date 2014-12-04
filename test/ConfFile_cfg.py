import FWCore.ParameterSet.Config as cms
import os

from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing ('python')

options.register('reportEvery', 100,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    "Report every N events (default is N=100)"
)
options.register('wantSummary', True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Print out trigger and timing summary"
)
options.register('outFilename', 'decay_histo.root',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "Output file name"
)

## 'maxEvents' is already registered by the Framework, changing default value
options.setDefault('maxEvents', 1000)

options.parseArguments()

process = cms.Process("USER")

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery
process.MessageLogger.cerr.default.limit = 10

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(options.wantSummary) )

process.TFileService = cms.Service("TFileService",
   fileName = cms.string(options.outFilename)
)

inputDir = '/eos/uscms/store/user/algomez/St2TOhst1_RPVSt1tojj_pythia8_13TeV/500st2TOhst1_100RPVst1TOjj_v706patch1/141202_040514/0000/'
inputFiles = []
for f in os.listdir(inputDir):
    if not os.path.isfile(os.path.join(inputDir,f)) or not f.endswith('.root'):
        continue
    inputFiles.append( os.path.join(inputDir.replace('/eos/uscms',''),f) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #'/store/user/algomez/St2TOhst1_RPVSt1tojj_pythia8_13TeV/500st2TOhst1_100RPVst1TOjj_v706patch1/141202_040514/0000/500St2TOhst1_100RPVSt1tojj_13TeV_pythia8_GEN_1.root'
        #'/store/user/algomez/St2TOhst1_RPVSt1tojj_pythia8_13TeV/500st2TOhst1_100RPVst1TOjj_v706patch1/141202_040514/0000/500St2TOhst1_100RPVSt1tojj_13TeV_pythia8_GEN_286.root'
        #'/store/user/algomez/St2TOhst1_RPVSt1tojj_pythia8_13TeV/500st2TOhst1_100RPVst1TOjj_v706patch1/141202_040514/0000/500St2TOhst1_100RPVSt1tojj_13TeV_pythia8_GEN_345.root'
    ),
    #eventsToProcess = cms.untracked.VEventRange('1:19')
    #eventsToProcess = cms.untracked.VEventRange('1:25')
    #eventsToProcess = cms.untracked.VEventRange('1:23')
)
process.source.fileNames.extend( inputFiles ) # see https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePoolInputSources#Example_3_More_than_255_input_fi

process.prunedGenParticles = cms.EDProducer('GenParticlePruner',
    src = cms.InputTag("genParticles"),
    select = cms.vstring(
        "drop  *  ",
        "keep ( status>=21 && status<=29 )", # keep hard process particles
        "keep abs(pdgId)==11 || abs(pdgId)==13 || abs(pdgId)==15", # keep electrons, muons, and taus
        "keep ( abs(pdgId)==22 && status==1 )" # keep status=1 photons
    )
)

process.printParticleList = cms.EDAnalyzer("ParticleListDrawer",
    #src = cms.InputTag("genParticles"),
    src = cms.InputTag("prunedGenParticles"),
    maxEventsToPrint = cms.untracked.int32(1)
)

process.analyzer = cms.EDAnalyzer('HiggsDecayAnalyzer',
    src = cms.InputTag('prunedGenParticles')
)

process.p = cms.Path(
    process.prunedGenParticles
    * (
    process.analyzer
    + process.printParticleList
    )
)
