import glob, os
import numpy as np
from scipy import stats
from tabulate import tabulate
import matplotlib
matplotlib.use('agg')
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt

plt_dir="/home/msilva/public_html/gen2-triggers/all_scans/"
plot_string="mDOM_arrays_npe_3_in_deltat_200_ndom_5_in_deltat_5000"
baseline  = np.load("/data/user/msilva/gen-2-trigs/%s.npy"%plot_string)
weights = baseline[:,0]
energy = baseline[:,1]
cos_zenith = baseline[:,2]
area_eff = baseline[:,3]
passes_cut =baseline[:,4]

#first make the simple energy dists
xbins= 30
xmin =2e3; xmax = 2e7;
bins = np.logspace(np.log10(xmin),np.log10(xmax), xbins)
base, temp_bins, _ = plt.hist(energy,bins=bins, range=(xmin,xmax), normed=False, weights=weights,
                      histtype="step",label="Baseline",color="blue",linestyle="-");
with_cut, _, _ = plt.hist(energy,bins=bins, range=(xmin,xmax), normed=False, weights=np.multiply(weights,passes_cut),
                      histtype="step",label="with trigger",color="red",linestyle="-");
bincenters = 0.5*(temp_bins[1:]+temp_bins[:-1])

plt.ylabel("Events in %s bins [Hz]"%str(xbins))
plt.yscale('log')
plt.xscale('log')
plt.xlabel("Muon Energy [GeV]")
plt.legend(loc='upper right')
plt.savefig(plt_dir+"energy_%s.png"%plot_string, bbox_inches='tight')
print "made plot: " + plt_dir+"energy_%s.png"%plot_string
plt.clf()

#now make the cumulative energy dists
xbins= 100
xmin =2e3; xmax = 2e7;
bins = np.logspace(np.log10(xmin),np.log10(xmax), xbins)
cdf_all_weights =[]
cdf_passes_weights = []
for bin in bins:
    temp_weights = weights[energy > bin]
    temp_cuts = passes_cut[energy > bin]
    passing_weights= np.multiply(temp_weights,temp_cuts)
    cdf_all_weights.append(np.sum(temp_weights))
    cdf_passes_weights.append(np.sum(passing_weights))

plt.plot(bins,cdf_all_weights,label="Baseline",color="blue",linestyle="-")
plt.plot(bins,cdf_passes_weights,label="with trigger",color="red",linestyle="-")
plt.ylabel("Total Events Above Energy [Hz]")
plt.yscale('log')
plt.xscale('log')
plt.xlabel("Muon Energy [GeV]")
plt.legend(loc='upper right')
plt.savefig(plt_dir+"cdf_energy_%s.png"%plot_string, bbox_inches='tight')
print "made plot: " + plt_dir+"cdf_energy_%s.png"%plot_string
plt.clf()

efficiencies = np.divide(cdf_passes_weights,cdf_all_weights)
plt.plot(bins,efficiencies,label="Simple Trigger")
plt.ylabel("Efficiency")
#plt.yscale('log')
plt.xscale('log')
plt.xlabel("Muon Energy [GeV]")
plt.legend(loc='upper left')
plt.savefig(plt_dir+"eff_energy_%s.png"%plot_string, bbox_inches='tight')
print "made plot: " + plt_dir+"eff_energy_%s.png"%plot_string
plt.clf()
