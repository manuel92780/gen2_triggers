#!/usr/bin/env python

#import icecube stuff
from icecube import icetray, dataclasses, dataio
from icecube import simclasses, MuonGun
from I3Tray import I3Tray
from icecube.icetray import I3Units
from icecube.MuonGun import load_model, StaticSurfaceInjector, Cylinder, OffsetPowerLaw, BundleConfiguration, BundleEntry

#import python stuff
import numpy as np
import glob, time

#useful for taking input variables
import argparse
parser = argparse.ArgumentParser(description = "selection used for triggers")
parser.add_argument('-dom_type', default="mDOM", type=str, dest = 'DOM_type')
#dom level triggers
#200nanosecond time window
#3PE cut
parser.add_argument('-dom_time', default=200, type=int, dest = 'dom_time')
parser.add_argument('-pe_cut', default=1, type=int, dest = 'pe_cut')
#event level triggers
#5000nanoseconds time window
#5doms cut
parser.add_argument('-event_time', default=5000, type=int, dest = 'event_time')
parser.add_argument('-ndom_cut', default=1, type=int, dest = 'ndom_cut')
args = parser.parse_args()

#prepare the array and time the script
final_cuts = []
start_time = time.asctime()
print 'Started:', start_time

def run_dom_trigger(list_of_pes, list_of_times):
    
    return passed, start_time
#find intersection with muons and gen2
gcd="/data/wipac/Gen2/HEE/geometries/Sunflower/IceCubeHEX_Sunflower_240m_v3_ExtendedDepthRange.GCD.i3.bz2"
surface_det = MuonGun.ExtrudedPolygon.from_file(gcd)
def todet(frame,surface):
    detmu = MuonGun.muons_at_surface(frame, surface)
    for i in range(len(detmu)):
        frame['EnteringMuon_'+str(i)] = detmu[i]
    if('EnteringMuon_0') not in frame: #does not contain an intersecting muon, toss it
        return False
    else: return True
#load the dataset
DOM_file = '/data/user/msilva/metaprojects/Gen2-Scripts/RECO_SPEs/MCReco_'+args.DOM_type+'.i3.bz2'
print DOM_file
f = dataio.I3File(DOM_file)
n_events = 0
for frame in f:
    if ("I3RecoPulseSeriesMapGen2" not in frame): continue;
    if(n_events%100 == 0):
        print "runing event: %s"%str(n_events); 
    n_events+=1
    #propagate muons to surface, if they dont intersect, throw the event away
    entering_muon_bool = todet(frame,surface_det)
    if not entering_muon_bool: continue;
    #should we include this cut
    if len(frame["I3RecoPulseSeriesMapGen2"]) < 1: continue #sometimes no charge is even recorded
    #first store the event level info like weights energy zeniths etc...
    model = MuonGun.load_model('GaisserH4a_atmod12_SIBYLL') #natural rate
    muon = frame["MCMuon"]
    flux = model.flux(MuonGun.depth(muon.pos.z), np.cos(muon.dir.zenith), 1)*model.energy(MuonGun.depth(muon.pos.z), np.cos(muon.dir.zenith), 1, 0, muon.energy)
    weight = flux*frame['MuonEffectiveArea'].value
    energy = frame["EnteringMuon_0"].energy
    cos_zenith = np.cos(frame["EnteringMuon_0"].dir.zenith)
    area_eff = frame["MuonEffectiveArea"].value 
    #now work on the triggers
    passes_cut = 0
    times = []; ndom = 0;
    string_dom = ""
    spes_times = []; spes = []
    first_dom = True
    for DOM, MCPE in frame["I3RecoPulseSeriesMapGen2"]:
        curr_string_dom = "%s,%s"%(DOM[0],DOM[1])
        if(first_dom):
            string_dom = curr_string_dom; first_dom = False
        if(curr_string_dom == string_dom): #group pmts together by string,dom
            for SPE in MCPE:
                spes_times.append(SPE.time); spes.append(SPE.charge)
            continue #then move onto the next string,dom/mcpe combo

        #book-keeping for the current step
        spes_times_np = np.array(spes_times)
        spes_np = np.array(spes)

        #book-keeping for the next step
        string_dom = curr_string_dom
        spes_times = []; spes = []
        for SPE in MCPE:
                spes_times.append(SPE.time); spes.append(SPE.charge)

        #now run the per dom level trigger
        for cur_time_index in range(len(spes_times_np)):
            cur_time=spes_times_np[cur_time_index]
            time_window = (spes_times_np>=cur_time) &(spes_times_np<=cur_time+args.dom_time)
            charges_in_window = spes_np[time_window]
            times_in_window = spes_times_np[time_window]
            charge_in_time = np.sum(charges_in_window)
            if(charge_in_time >= args.pe_cut):
                times.append(cur_time); ndom +=1;
                break; #if we hit the trigger, end the for loop and move onto event level triggers
            
        #finished the charge cut on the dom
        #now check if we also fulfill the ndom cut
        if(ndom >= args.ndom_cut):
            start_time_slice =  times[ndom-1] - args.event_time
            end_time_slice = times[ndom-1]
            doms_within_time = [value for value in times if (value >= start_time_slice) & (value <= end_time_slice)]
            #if there are ndoms that fulfill the time window criteria, end the loop
            if len(doms_within_time) >= args.ndom_cut:
                passes_cut = 1; break

    #one final loop for overflow
    spes_times_np = np.array(spes_times)
    spes_np = np.array(spes)
    for cur_time_index in range(len(spes_times_np)):
        cur_time=spes_times_np[cur_time_index]
        time_window = (spes_times_np>=cur_time) &(spes_times_np<=cur_time+args.dom_time)
        charges_in_window = spes_np[time_window]
        times_in_window = spes_times_np[time_window]
        charge_in_time = np.sum(charges_in_window)
        if(charge_in_time >= args.pe_cut):
            times.append(cur_time); ndom +=1;
    if(ndom >= args.ndom_cut):
        start_time_slice =  times[ndom-1] - args.event_time
        end_time_slice = times[ndom-1]
        doms_within_time = [value for value in times if (value >= start_time_slice) & (value <= end_time_slice)]
        if len(doms_within_time) >= args.ndom_cut:
            passes_cut = 1; 

    dummy_array = [weight,energy,cos_zenith,area_eff,passes_cut]
    final_cuts.append(dummy_array)

#after our loop is done over the sample, save it
output_file = "data/%s_arrays_npe_%s_in_deltat_%s_ndom_%s_in_deltat_%s.npy"%(args.DOM_type,args.pe_cut,args.dom_time,args.ndom_cut,args.event_time)
print "saving numpy array: " + output_file
np.save(output_file,final_cuts)

#run time is??
end_time = time.asctime()
print 'Ends:', end_time

