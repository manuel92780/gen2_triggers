import numpy as np
import matplotlib, os, time, argparse
matplotlib.use('agg')
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt

start_time = time.asctime()
print 'Started:', start_time

parser = argparse.ArgumentParser(description='')
parser.add_argument("-o","--domfilebase",dest="domfilebase",type=str,
                    default="mDOM",help="base name for DOM type")
args = parser.parse_args()
domtype=args.domfilebase

infile = np.load("data/"+domtype+".npy")

print infile[:,2]
plt_dir="/home/msilva/public_html/gen2-triggers/"
#plot simple stuff first
xbins= 30
xmin = 1e3; xmax = 5e8; log_xbins = np.logspace(np.log10(xmin),np.log10(xmax), xbins)
weird_eff_areas_values, new_xbins, _ = plt.hist(infile[:,1], bins=log_xbins, range=(xmin,xmax), histtype='step')
plt.ylabel("Number of Events")
plt.xlabel("Muon Energy at Entry [GeV]")
plt.yscale("log")
plt.xscale("log")
plt.savefig(plt_dir+"count_events_"+domtype+".pdf")
print "Made file: " + plt_dir+"count_events_"+domtype+".pdf"
plt.clf()

xbins= 30
xmin = -1; xmax = 1; xbins = np.linspace(xmin,xmax,xbins)
values, new_xbins, _ = plt.hist(np.cos(infile[:,2]), bins=xbins, range=(xmin,xmax), histtype='step')
plt.ylabel("Number of Events")
plt.xlabel("cos(zenith)")
#plt.yscale("log")
#plt.xscale("log")
plt.savefig(plt_dir+"count_events_zenith_"+domtype+".pdf")
plt.clf()

xbins= 30
xmin = 1e0; xmax = 1e5; log_xbins = np.logspace(np.log10(xmin),np.log10(xmax), xbins)
nDoms, _, _ = plt.hist(infile[:,3], bins=log_xbins, range=(xmin,xmax), histtype='step')
plt.ylabel("Number of Events")
plt.xlabel("Number of PMTs hit per event")
plt.yscale("log")
plt.xscale("log")
plt.savefig(plt_dir+"NPMTs_"+domtype+".pdf")
plt.clf()

xbins= 30
xmin = 1e0; xmax = 1e6; log_xbins = np.logspace(np.log10(xmin),np.log10(xmax), xbins)
nDoms, _, _ = plt.hist(infile[:,4], bins=log_xbins, range=(xmin,xmax), histtype='step')
plt.ylabel("Number of Events")
plt.xlabel("Number of NPEs in each event")
plt.yscale("log")
plt.xscale("log")
plt.savefig(plt_dir+"NPEs_"+domtype+".pdf")
plt.clf()

xbins= 20
xmin = 1e0; xmax = 1e4; log_xbins = np.logspace(np.log10(xmin),np.log10(xmax), xbins)
nDoms1, _, _ = plt.hist(infile[:,5], bins=log_xbins, range=(xmin,xmax), histtype='step', label="NPE > 1")
#nDoms2, _, _ = plt.hist(infile[:,6], bins=log_xbins, range=(xmin,xmax), histtype='step', label="NPE > 2")
nDoms3, _, _ = plt.hist(infile[:,7], bins=log_xbins, range=(xmin,xmax), histtype='step', label="NPE > 3")
#nDoms4, _, _ = plt.hist(infile[:,8], bins=log_xbins, range=(xmin,xmax), histtype='step', label="NPE > 4")
nDoms5, _, _ = plt.hist(infile[:,9], bins=log_xbins, range=(xmin,xmax), histtype='step', label="NPE > 5")
nDoms10, _, _ = plt.hist(infile[:,10], bins=log_xbins, range=(xmin,xmax), histtype='step', label="NPE > 10")
plt.ylabel("Number of Events")
plt.xlabel("Number of OMs with NPE criteria per OM")
plt.yscale("log")
plt.xscale("log")
plt.legend(loc='upper right')
plt.savefig(plt_dir+"NDOMs_"+domtype+".pdf")
print "Made file: " + plt_dir+"NDOMs_"+domtype+".pdf"
plt.clf()

#plot weird eff areas
xbins= 30
xmin = 1e3; xmax = 5e8; log_xbins = np.logspace(np.log10(xmin),np.log10(xmax), xbins)
weird_eff_areas_values, new_xbins, _ = plt.hist(infile[:,1], weights=infile[:,0], bins=log_xbins, range=(xmin,xmax), histtype='step')
plt.clf()

#compute the eff area
bin_widths = log_xbins[1:]-log_xbins[:-1]
eff_areas = np.divide(weird_eff_areas_values,bin_widths)/(4.*np.pi)

#new, plot good eff areas
bincenters = 10**(0.5*(np.log10(new_xbins[1:])+np.log10(new_xbins[:-1])))
eff_areas_values, _, _ = plt.hist(bincenters, weights=eff_areas, bins=log_xbins, range=(xmin,xmax), histtype='step')
plt.ylabel("Effective Area [km2]")
plt.xlabel("Muon Energy at Entry [GeV]")
plt.yscale("log")
plt.xscale("log")
plt.savefig(plt_dir+"effective_areas_"+domtype+".pdf")
print "Made file: " + plt_dir+"effective_areas_"+domtype+".pdf"
plt.clf()
