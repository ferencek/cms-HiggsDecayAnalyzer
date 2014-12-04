// -*- C++ -*-
//
// Package:    MyAnalysis/HiggsDecayAnalyzer
// Class:      HiggsDecayAnalyzer
// 
/**\class HiggsDecayAnalyzer HiggsDecayAnalyzer.cc MyAnalysis/HiggsDecayAnalyzer/plugins/HiggsDecayAnalyzer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Dinko Ferencek
//         Created:  Thu, 04 Dec 2014 01:05:24 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "TH1F.h"

//
// class declaration
//

class HiggsDecayAnalyzer : public edm::EDAnalyzer {
   public:
      explicit HiggsDecayAnalyzer(const edm::ParameterSet&);
      ~HiggsDecayAnalyzer();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      //virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
      //virtual void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
      //virtual void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

      // ----------member data ---------------------------
      const edm::InputTag src;

      edm::Service<TFileService> fs;

      TH1F *h1_DecayPdgId;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
HiggsDecayAnalyzer::HiggsDecayAnalyzer(const edm::ParameterSet& iConfig) :

  src(iConfig.getParameter<edm::InputTag>("src"))

{
   //now do what ever initialization is needed
   h1_DecayPdgId = fs->make<TH1F>("h1_DecayPdgId",";PDG ID;",100,-0.5,99.5);

}


HiggsDecayAnalyzer::~HiggsDecayAnalyzer()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called for each event  ------------
void
HiggsDecayAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   edm::Handle<reco::GenParticleCollection> genParticles;
   iEvent.getByLabel(src,genParticles);

   // loop over GenParticles and select Higgs bosons
   for(reco::GenParticleCollection::const_iterator it = genParticles->begin(); it != genParticles->end(); ++it)
   {
     if( abs(it->pdgId())!=25 ) continue;

     if( it->numberOfDaughters()==0 )
     {
       edm::LogError("ZeroDecayProducts") << "Zero decay products found. This is not expected.";

       h1_DecayPdgId->Fill( 0 );

       continue;
     }

     h1_DecayPdgId->Fill( abs(it->daughter(0)->pdgId()) );
   }

}


// ------------ method called once each job just before starting event loop  ------------
void 
HiggsDecayAnalyzer::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
HiggsDecayAnalyzer::endJob() 
{
}

// ------------ method called when starting to processes a run  ------------
/*
void 
HiggsDecayAnalyzer::beginRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void 
HiggsDecayAnalyzer::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void 
HiggsDecayAnalyzer::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void 
HiggsDecayAnalyzer::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
HiggsDecayAnalyzer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(HiggsDecayAnalyzer);
