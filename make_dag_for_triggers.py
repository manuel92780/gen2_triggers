import numpy as np

DOM_type = ["mDOM","DEgg","pDOM"]
DOM_times=[200,400,600,800,1000]
NPEs = [1,3,5,7,9]
event_times=[2000,4000,6000,8000,10000]
NDOMs = [1,3,5,7,9]
njobs=len(DOM_type)*len(DOM_times)*len(NPEs)*len(event_times)*len(NDOMs)

f = open('dagman_triggers.dag','w')
print "will submit " + str(njobs) + " jobs"
job_id=0
for D_type in DOM_type:
    for D_times in DOM_times:
        for NPE in NPEs:
            for e_times in event_times:
                for NDOM in NDOMs:
                    a="JOB job"+str(job_id)+" jobs.sub \n"
                    b="VARS job"+str(job_id)+" DOM=\"%s\" "%D_type
                    b+="dom_time=\"%s\" "%str(D_times)
                    b+="npes=\"%s\" "%str(NPE)
                    b+="event_time=\"%s\" "%str(e_times)
                    b+="ndoms=\"%s\" \n"%str(NDOM)
                    f.write(a)
                    f.write(b)
                    job_id+=1

