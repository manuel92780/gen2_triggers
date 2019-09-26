import os, sys, numpy, argparse, time, glob
from collections import Counter

from icecube import icetray
from I3Tray import I3Tray

from I3Tray import I3Tray
from icecube import icetray, dataio

start_time = time.asctime()
print 'Started:', start_time

parser = argparse.ArgumentParser(description='')
parser.add_argument("-o","--domfilebase",dest="domfilebase",type=str,
                    default="pDOM",help="base name for DOM type")
args = parser.parse_args()
domtype=args.domfilebase

#load files
infiles=glob.glob("/data/user/msilva/metaprojects/Gen2-Scripts/RECO_SPEs/MCReco_"+domtype+".i3.bz2")
print infiles

#load icetray
tray = I3Tray()
tray.AddModule("I3Reader", "reader", FilenameList=infiles)

global output_array; output_array = [];
global counting; counting = 0;
def save_to_array(frame):
    global counting; counting += 1
    if(counting % 100 < 1): print "event number : "+ str(counting)
    Muon = frame["MCMuon"]
    energy = Muon.energy
    if(energy > 1e6): return False
    zenith = Muon.dir.zenith
    eff_area = frame["MuonEffectiveArea"].value/(1000*1000) #convert from m^2 to km^2
    tot_NPE = 0; tot_charge = 0;
    NPE_DOM = 0; charge_DOM = 0;
    cnt = Counter()
    for dom, MCPE in frame["I3RecoPulseSeriesMapGen2"]:
        cnt["%s,%s"%(dom[0],dom[1])] += 1
        print len(cnt)
        for PE in MCPE:
            tot_charge += PE.charge
    for dom, MCPE in frame["I3MCPESeriesMap"]:
        for PE in MCPE:
            tot_NPE += PE.npe
    dummy = [eff_area,energy,zenith,tot_NPE,tot_charge]
    output_array.append(dummy)
    return True
tray.Add(save_to_array,Streams=[icetray.I3Frame.DAQ])

#cleanup
tray.AddModule("TrashCan", "thecan")
tray.Execute()
tray.Finish()

#save numpy array for processing
outfile = "data/"+domtype+".npy"
print "saving numpy array: " + outfile
print "total number of events: " + str(counting)
numpy.save(outfile,output_array)
