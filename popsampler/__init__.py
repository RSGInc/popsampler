
import pandas as pd
import numpy as np

def read_tables(zoneSampleRateFileName, hhFileName, perFileName):
    
    sampleRates = pd.read_csv(zoneSampleRateFileName)
    hhTable = pd.read_csv(hhFileName)
    perTable = pd.read_csv(perFileName)
    return(sampleRates, hhTable, perTable)

def write_tables(hhOutFileName, perOutFileName, households, persons):
    
    households.to_csv(hhOutFileName, index=False)
    persons.to_csv(perOutFileName, index=False)
    
def sample_hhs(group, hhZoneField, hhExpFacField):
    
    #sample using the zone sample rate with replacement and a stable group seed
    seed = int(group[hhZoneField].min()*1000 + group.hhincbin.min()*100 + group.hhsizebin.min()*10 + group.hhworkerbin.min())
    sample = group.sample(frac=group.sample_rate.min(), replace=True, random_state=seed)

    if len(sample)==0:
        print('sample is empty')
        sample = group
    else:
        #set hh expansion factor based on actual sample size since sampling is lumpy
        sample[hhExpFacField] = 1.0 / (len(sample)*1.0/len(group))

    print(hhZoneField + " %i hhincbin %s hhsizebin %s hhworkerbin %s sample rate %.2f effective rate %.2f" % (group[hhZoneField].min(), 
    group.hhincbin.min(), group.hhsizebin.min(), group.hhworkerbin.min(), group.sample_rate.min(), 1.0 / sample[hhExpFacField].min()))
    
    return(sample)

def run(zoneSampleRateFileName, hhFileName, hhOutFileName, perFileName, perOutFileName, hhZoneField, 
        zoneField, useIncomeBins, useSizeBins, useWorkerBins, incomeField, sizeField, workersField,
        incomeBin1Max, incomeBin2Max, incomeBin3Max, hhExpFacField, hhHhIdField, perHhIdField):

    print("Synthetic Population Spatial Sampler")
    print("zoneSampleRateFileName: " + zoneSampleRateFileName)
    print("hhFileName: " + hhFileName)
    print("hhOutFileName: " + hhOutFileName)
    print("perFileName: " + perFileName)
    print("perOutFileName: " + perOutFileName)
    print("hhZoneField: " + hhZoneField)
    print("zoneField: " + zoneField)
    print("useIncomeBins: " + str(useIncomeBins))
    print("useSizeBins: " + str(useSizeBins))
    print("useWorkerBins: " + str(useWorkerBins))
    print("incomeField: " + incomeField)
    print("sizeField: " + sizeField)
    print("workersField: " + workersField)
    print("incomeBin1Max: " + str(incomeBin1Max))
    print("incomeBin2Max: " + str(incomeBin2Max))
    print("incomeBin3Max: " + str(incomeBin3Max))
    print("hhExpFacField: " + hhExpFacField)
    print("hhHhIdField: " + hhHhIdField)
    print("perHhIdField: " + perHhIdField)
        
    #get tables
    sampleRates, households, persons = read_tables(zoneSampleRateFileName, hhFileName, perFileName)

    #join sample rate by home zone
    households = pd.merge(households, sampleRates, left_on=hhZoneField, right_on=zoneField)

    #bin hhs by control fields
    if useIncomeBins:
      incbins = [-1, incomeBin1Max, incomeBin2Max, incomeBin3Max, households[incomeField].max()+1]
      households['hhincbin'] = pd.cut(households[incomeField], incbins, labels=False)
    else:
      households['hhincbin'] = 0
    if useSizeBins:
      sizebins = [-1, 1, 2, 3, households[sizeField].max()+1]
      households['hhsizebin'] = pd.cut(households[sizeField], sizebins, labels=False)
    else: 
      households['hhsizebin'] = 0 
    if useWorkerBins:
      workerbins = [-1, 0, 1, 2, households[workersField].max()+1]
      households['hhworkerbin'] = pd.cut(households[workersField], workerbins, labels=False)
    else:
      households['hhworkerbin'] = 0

    #group hhs by zone, control fields and sample and reset index
    hhsGrouped = households.groupby([hhZoneField,"hhincbin","hhsizebin","hhworkerbin"])
    new_households = hhsGrouped.apply(sample_hhs, hhZoneField=hhZoneField, hhExpFacField=hhExpFacField)
    new_households = new_households.reset_index(drop=True)
    
    #update ids and expand persons
    new_households['hhno_new'] = range(1,len(new_households)+1)
    new_persons = pd.merge(persons, new_households[[hhHhIdField,"hhno_new"]], left_on=perHhIdField, right_on=hhHhIdField)
    new_households[hhHhIdField] = new_households['hhno_new'].astype(np.int32)
    new_persons[perHhIdField] = new_persons['hhno_new'].astype(np.int32)

    #delete added fields
    del new_households[zoneField]
    del new_households['hhno_new']
    del new_households['sample_rate']
    del new_households['hhincbin']
    del new_households['hhsizebin']
    del new_households['hhworkerbin']
    del new_persons['hhno_new']
    
    #write result files
    write_tables(hhOutFileName, perOutFileName, new_households, new_persons)
