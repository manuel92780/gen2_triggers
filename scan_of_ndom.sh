dom_type="mDOM"

for dom_time in 200 400 600 800 1000
do
    for event_time in 2000 4000 6000 8000 10000
    do
	for pe_cut in 1 3 5 7 9
	do
	    python plot_scan_of_ndom.py -dom_type $dom_type -dom_time $dom_time -event_time $event_time -pe_cut $pe_cut
	done
    done
done
