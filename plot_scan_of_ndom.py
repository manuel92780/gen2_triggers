import glob, os
import numpy as np
from scipy import stats
from tabulate import tabulate
import matplotlib
matplotlib.use('agg')
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt

import argparse
parser = argparse.ArgumentParser(description = "selection used for triggers")
parser.add_argument('-dom_type', default="mDOM", type=str, dest = 'DOM_type')
parser.add_argument('-dom_time', default=300, type=int, dest = 'dom_time')
parser.add_argument('-event_time', default=5000, type=int, dest = 'event_time')
parser.add_argument('-pe_cut', default=3, type=int, dest = 'pe_cut',required=True)
args = parser.parse_args()

plt_dir="/home/msilva/public_html/gen2-triggers/all_scans/ndom_scan/"
colors={1:"blue",3:"red",5:"green",7:"black",9:"cyan"}
effs = []
first_pass =True
xbins= 10
xmin =2e3; xmax = 2e7;
bins = np.logspace(np.log10(xmin),np.log10(xmax), xbins)
for ndom in [1,3,5,7,9]:
    plot_string="%s_arrays_npe_%s_in_deltat_%s_ndom_%s_in_deltat_%s"%(args.DOM_type,args.pe_cut,args.dom_time,ndom,args.event_time)
    baseline  = np.load("/data/user/msilva/gen-2-trigs/%s.npy"%plot_string)
    weights = baseline[:,0]
    energy = baseline[:,1]
    cos_zenith = baseline[:,2]
    area_eff = baseline[:,3]
    passes_cut =baseline[:,4]

    #now make the cumulative energy dists
    cdf_all_weights =[]
    cdf_passes_weights = []
    for bin in bins:
        temp_weights = weights[energy > bin]
        temp_cuts = passes_cut[energy > bin]
        passing_weights= np.multiply(temp_weights,temp_cuts)
        cdf_all_weights.append(np.sum(temp_weights))
        cdf_passes_weights.append(np.sum(passing_weights))
    efficiencies = np.divide(cdf_passes_weights,cdf_all_weights)
    effs.append(efficiencies)
    if first_pass:
        plt.plot(bins,cdf_all_weights,label="baseline",color="magenta",linestyle="--"); first_pass = False
    plt.plot(bins,cdf_passes_weights,label=r"NDOM $\geq$ %s"%str(ndom),color=colors[ndom],linestyle="-")
plt.ylabel("Total Events Above Energy [Hz]")
plt.yscale('log')
plt.xscale('log')
plt.xlabel("Muon Energy [GeV]")
plt.legend(loc='upper right')
plt.savefig(plt_dir+"scan_%s_type_ndoms_with_pe%s_in_%s_ndoms_in_%s_cdf_energy.png"%(args.DOM_type,str(args.pe_cut),str(args.dom_time),str(args.event_time)), bbox_inches='tight')
print "made plot: " + plt_dir+"scan_%s_type_ndoms_with_pe%s_in_%s_ndoms_in_%s_cdf_energy.png"%(args.DOM_type,str(args.pe_cut),str(args.dom_time),str(args.event_time))
plt.clf()

ndom = 1
for efficiencies in effs:
    plt.plot(bins,efficiencies,label=r"NDOM $\geq$ %s"%str(ndom),color=colors[ndom])
    ndom+=2
plt.title(r"%s, PE $\geq$ %s in $\Delta$ t = %s ns, NDOMs in $\Delta$ t = %s $\mu$s"%(args.DOM_type,str(args.pe_cut),str(args.dom_time),str(args.event_time/1000.)))
plt.ylabel("Efficiency")
#plt.yscale('log')
plt.xscale('log')
plt.ylim(0,1.1)
plt.xlabel("Muon Energy [GeV]")
plt.legend(loc='lower right')
plt.savefig(plt_dir+"scan_%s_type_ndoms_with_pe%s_in_%s_ndoms_in_%s_eff_energy.png"%(args.DOM_type,str(args.pe_cut),str(args.dom_time),str(args.event_time)), bbox_inches='tight')
print "made plot: " + plt_dir+"scan_%s_type_ndoms_with_pe%s_in_%s_ndoms_in_%s_eff_energy.png"%(args.DOM_type,str(args.pe_cut),str(args.dom_time),str(args.event_time))
plt.clf()
