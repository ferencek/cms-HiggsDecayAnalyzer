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
options.register('useInputDir', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Use input directory"
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

inputDir = '/eos/uscms/store/user/ferencek/noreplica/Stop2ToStop1H_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIISpring15DR74_AODSIM/150612_162933/0000/'
inputFiles = []
for f in os.listdir(inputDir):
    if not os.path.isfile(os.path.join(inputDir,f)) or not f.endswith('.root'):
        continue
    inputFiles.append( os.path.join(inputDir.replace('/eos/uscms',''),f) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        # MiniAOD
        #'/store/user/ferencek/noreplica/Stop2ToStop1H_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIISpring15DR74_MiniAOD/150613_192348/0000/Stop2ToStop1H_TuneCUETP8M1_13TeV-madgraph-pythia8_MiniAOD_Asympt25ns_1.root'
        # AOD
        '/store/user/ferencek/noreplica/Stop2ToStop1H_TuneCUETP8M1_13TeV-madgraph-pythia8/RunIISpring15DR74_AODSIM/150612_162933/0000/Stop2ToStop1H_TuneCUETP8M1_13TeV-madgraph-pythia8_AODSIM_Asympt25ns_1.root'
    ),
    #eventsToProcess = cms.untracked.VEventRange('1:19')
    #eventsToProcess = cms.untracked.VEventRange('1:25')
    #eventsToProcess = cms.untracked.VEventRange('1:23')
)
if options.useInputDir:
    process.source.fileNames = cms.untracked.vstring()
    process.source.fileNames.extend( inputFiles ) # see https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePoolInputSources#Example_3_More_than_255_input_fi

process.prunedGenParticles = cms.EDProducer('GenParticlePruner',
    src = cms.InputTag("genParticles"),
    select = cms.vstring(
        # MiniAOD configuration
        #"drop  *", # this is the default
        #"++keep abs(pdgId) == 11 || abs(pdgId) == 13 || abs(pdgId) == 15", # keep leptons, with history
        #"keep abs(pdgId) == 12 || abs(pdgId) == 14 || abs(pdgId) == 16",   # keep neutrinos
        #"drop   status == 2",                                              # drop the shower part of the history
        #"+keep pdgId == 22 && status == 1 && (pt > 10 || isPromptFinalState())", # keep gamma above 10 GeV (or all prompt) and its first parent
        #"+keep abs(pdgId) == 11 && status == 1 && (pt > 3 || isPromptFinalState())", # keep first parent of electrons above 3 GeV (or prompt)
        #"keep++ abs(pdgId) == 15",                                         # but keep keep taus with decays
        #"drop  status > 30 && status < 70 ",                               #remove pythia8 garbage
        #"drop  pdgId == 21 && pt < 5",                                    #remove pythia8 garbage
        #"drop   status == 2 && abs(pdgId) == 21",                          # but remove again gluons in the inheritance chain
        #"keep abs(pdgId) == 23 || abs(pdgId) == 24 || abs(pdgId) == 25 || abs(pdgId) == 6 || abs(pdgId) == 37 ",   # keep VIP(articles)s
        #"keep abs(pdgId) == 310 && abs(eta) < 2.5 && pt > 1 ",                                                     # keep K0
        ## keep heavy flavour quarks for parton-based jet flavour
        #"keep (4 <= abs(pdgId) <= 5) & (status = 2 || status = 11 || status = 71 || status = 72)",
        ## keep light-flavour quarks and gluons for parton-based jet flavour
        #"keep (1 <= abs(pdgId) <= 3 || pdgId = 21) & (status = 2 || status = 11 || status = 71 || status = 72) && pt>5", 
        ## keep b and c hadrons for hadron-based jet flavour
        #"keep (400 < abs(pdgId) < 600) || (4000 < abs(pdgId) < 6000)",
        ## additional c hadrons for jet fragmentation studies
        #"keep abs(pdgId) = 10411 || abs(pdgId) = 10421 || abs(pdgId) = 10413 || abs(pdgId) = 10423 || abs(pdgId) = 20413 || abs(pdgId) = 20423 || abs(pdgId) = 10431 || abs(pdgId) = 10433 || abs(pdgId) = 20433", 
        ## additional b hadrons for jet fragmentation studies
        #"keep abs(pdgId) = 10511 || abs(pdgId) = 10521 || abs(pdgId) = 10513 || abs(pdgId) = 10523 || abs(pdgId) = 20513 || abs(pdgId) = 20523 || abs(pdgId) = 10531 || abs(pdgId) = 10533 || abs(pdgId) = 20533 || abs(pdgId) = 10541 || abs(pdgId) = 10543 || abs(pdgId) = 20543", 
        ##keep SUSY particles
        #"keep (1000001 <= abs(pdgId) <= 1000039 ) || ( 2000001 <= abs(pdgId) <= 2000015)",
        ## keep protons 
        #"keep pdgId = 2212",
        #"keep status == 3 || ( 21 <= status <= 29) || ( 11 <= status <= 19)",  #keep event summary (status=3 for pythia6, 21 <= status <= 29 for pythia8)
        #"keep isHardProcess() || fromHardProcessFinalState() || fromHardProcessDecayed() || fromHardProcessBeforeFSR() || (statusFlags().fromHardProcess() && statusFlags().isLastCopy())",  #keep event summary based on status flags

        # Private configuration
        "drop  *  ",
        "keep ( status>=21 && status<=29 )", # keep hard process particles
        "keep abs(pdgId)==11 || abs(pdgId)==13 || abs(pdgId)==15", # keep electrons, muons, and taus
        #"keep ( abs(pdgId)==22 && status==1 )" # keep status=1 photons
        "keep (status==1)" # keep all stable particles
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
