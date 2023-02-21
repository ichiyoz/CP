import json
from app.logic.LookUp import LookUp
from app.logic.getVV import getVV
from app.logic.processPair2 import processPair2
from app.logic.getTr2 import getTr2
from app.logic.getTr import getTr
from app.logic.processPair import processPair
from app.logic.getGraph import getGraph
import datetime
from app.logic.getV import Structure
import pickle
from app.logic.getSample import Sample
import csv
import pickle
from app.names import Names
import copy
import numpy as np
from pandas import Timestamp
import substring
JSON_FILE_OUT = "output/data_out2.json"
# conditionname='schizo'
n = Names()
conditionname, path = n.Names()

class Sequence:

    def getNodes(self, data):
        
        l = LookUp()
        nodedesc = l.getNode()

        for pid in data:
            if len(data[pid]) != 0:
                for date in sorted(data[pid]['appt'].keys()):
                  if 'withinappt' not in data[pid]['appt'][date] or len(data[pid]['appt'][date]['withinappt']) == 0:
                        if len(data[pid]['appt'][date]['diag']) == 0:
                            data[pid]['appt'][date]['diag'] = 'D_NR'
                        else:
                            data[pid]['appt'][date]['diag'] = nodedesc[str(data[pid]['appt'][date]['diag'])]
                        
                        if len(data[pid]['appt'][date]['proc']) == 0:
                            data[pid]['appt'][date]['proc'] = 'O_NR'
                        else:
                            data[pid]['appt'][date]['proc'] = nodedesc[str(data[pid]['appt'][date]['proc'])]

                        if len(data[pid]['appt'][date]['drugclass']) == 0:
                            data[pid]['appt'][date]['drugclass'] = 'M_NR'
                        else:
                            data[pid]['appt'][date]['drugclass'] = nodedesc[str(data[pid]['appt'][date]['drugclass'])]
                  elif len(data[pid]['appt'][date]['withinappt']) > 0:
                        for time in sorted(iter(data[pid]['appt'][date]['withinappt'])):
                            # for i in data[pid]['appt'][date]['withinappt'][time]['diag']:
                            if len(data[pid]['appt'][date]['withinappt'][time]['diag']) == 0:
                                data[pid]['appt'][date]['withinappt'][time]['diag'] = 'D_NR'
                            else:
                                data[pid]['appt'][date]['withinappt'][time]['diag'] = nodedesc[
                                    str(data[pid]['appt'][date]['withinappt'][time]['diag'])]
                                
                        for time in sorted(iter(data[pid]['appt'][date]['withinappt'])):
                            if len(data[pid]['appt'][date]['withinappt'][time]['proc']) == 0:
                                data[pid]['appt'][date]['withinappt'][time]['proc'] = 'O_NR'
                            else:
                                data[pid]['appt'][date]['withinappt'][time]['proc'] = nodedesc[
                                    str(data[pid]['appt'][date]['withinappt'][time]['proc'])]
                                
                        for time in sorted(iter(data[pid]['appt'][date]['withinappt'])):
                            # for drg in data[pid]['appt'][date]['withinappt'][time]['drugclass']:
                            if len(data[pid]['appt'][date]['withinappt'][time]['drugclass']) == 0:
                                data[pid]['appt'][date]['withinappt'][time]['drugclass'] = 'M_NR'
                            else:
                                data[pid]['appt'][date]['withinappt'][time]['drugclass'] = nodedesc[
                                    str(data[pid]['appt'][date]['withinappt'][time]['drugclass'])]


        return data

    def getSeq(self, data,group):

        # pickle_out = open(path + conditionname + '_readmit.pickle', 'rb')
        # readmitlist = pickle.load(pickle_out)
        # pickle_out.close()
        l = LookUp()
        nodedesc = l.getNode()
        tempVT = dict()
        VT = dict()
        tempDT = dict()
        OT = {}
        l = LookUp()
        Vdesc = l.getV()
        # Vdesc=t.filterV()  #filter out rare V
        # obsdesc = l.getO()

        t = Structure()
        for pid in data:
            start = True   #change for clever cohort
            VT[pid] = list()
            tempDT[pid] = list()
            tempVT[pid] = list()
            OT[pid] = list()
            
            # if readmitlist[pid] == 1 or readmitlist[pid] == 0:
            VT[pid].append('Start')
            # tempDT[pid].append('Start')
            for date in sorted(data[pid]['appt']):
              if 'withinappt' not in data[pid]['appt'][date] or len(data[pid]['appt'][date]['withinappt']) == 0:
                # if Vdesc[str(data[pid]['appt'][date]['type']) + str(data[pid]['appt'][date]['diag']) + str(
                #         data[pid]['appt'][date]['proc']) + str(data[pid]['appt'][date]['drugclass'])] == 'V1': # V1 is clever cohort only
                #     start = True
                
                #not letting repeats in VT
                # if start == True and Vdesc[str(data[pid]['appt'][date]['type']) + str(data[pid]['appt'][date]['diag']) + str(data[pid]['appt'][date]['proc']) + str(data[pid]['appt'][date]['drugclass'])] not in \
                #         VT[pid] and
                if (str(data[pid]['appt'][date]['diag']) + str(data[pid]['appt'][date]['proc']) + str(data[pid]['appt'][date]['drugclass']) != 'D_NRO_NRM_NR'):
                    VT[pid].append(Vdesc[str(data[pid]['appt'][date]['type']) + str(\
                        data[pid]['appt'][date]['diag']) + str(data[pid]['appt'][date]['proc']) + str(
                        data[pid]['appt'][date]['drugclass'])])
                    # tempDT[pid].append(data[pid]['appt'][date]['actualdate'])

              elif len(data[pid]['appt'][date]['withinappt']) > 0:
                    for time in sorted(iter(data[pid]['appt'][date]['withinappt'])):
                        if str(data[pid]['appt'][date]['withinappt'][time]['diag']) + str(data[pid]['appt'][date]['withinappt'][time]['proc']) + str(data[pid]['appt'][date]['withinappt'][time]['drugclass']) != 'D_NRO_NRM_NR':
                            VT[pid].append(Vdesc[str(data[pid]['appt'][date]['type']) +str(data[pid]['appt'][date]['withinappt'][time]['diag']) + str(data[pid]['appt'][date]['withinappt'][time]['proc']) + str(data[pid]['appt'][date]['withinappt'][time]['drugclass'])])
                        # tempDT[pid].append(data[pid]['appt'][date]['withinappt'][time]['actualtime'])
                        #print (data[pid]['appt'][date]['withinappt'][time]['actualtime'])
                    if data[pid]['appt'][date]['enddate']!='NA' and Timestamp(np.datetime64(data[pid]['appt'][date]['enddate'])).strftime('%Y-%m-%d')==Timestamp(date).strftime('%Y-%m-%d'):
                        VT[pid].append(data[pid]['appt'][date]['dischargetype'])
                        
            # if data[pid]['death']!=0:  #DEATH
            #     VT[pid].append('death')
            #     tempDT[pid].append('death')

        # d2={}
        # d2['DISCHARGE']='DISCHARGE'
        # d2['ED/ADMIT']='ED/ADMIT'
        # d2['Readmitted']='Readmitted'
        # for Vkey in Vdesc.keys():
        #     if Vkey[1:].split('_')[0]!='D_NRO_NRM_NR' and Vkey[0]!='D':
        #         T=Vkey.split('D')[0]
        #         if T=='I':
        #             enc='Inpatient'
        #         elif T=='E':
        #             enc='EM'
        #         elif T=='P':
        #             enc='Outpatient'
        #         else:
        #             enc='Other'
        #         v=Vkey[1:].split('O')[0]
        #         D=list(nodedesc.keys())[list(nodedesc.values()).index(v)]
        #         if D=='D_NR':
        #             D='None'
        #         v=Vkey[1:].split('M')[0]
        #         v2=substring.substringByChar(v, startChar="O")
        #         O=list(nodedesc.keys())[list(nodedesc.values()).index(v2)]
        #         if O=='O_NR':
        #             O='None'
        #         v=substring.substringByChar(Vkey[1:], startChar="M")
        #         M=list(nodedesc.keys())[list(nodedesc.values()).index(v)]
        #         if M=='M_NR':
        #             M='None'
        #         d2[Vdesc[Vkey]]=(enc[0]+':'+'diagnosis=' + D + ',' + 'procedure=' + O+', '+'drug='+ M.split('_')[0])#+': '+Vdesc[Vkey])

        # with open(path+conditionname+'_SPADE_%s.csv'%group, "w") as csv_file:
        #     for pid in sorted(VT):
        #         writer = csv.writer(csv_file, delimiter=',')
                
        #         for i in range(1,len(VT[pid])):
        #             combined_row = []
        #             combined_row.append(pid)
        #             combined_row.append(tempDT[pid][i])
        #             combined_row.append(1)
        #             combined_row.append(d2[VT[pid][i]])
        #             writer.writerow(combined_row)
        
        # # with open(path+conditionname+'_SPADE_%s.csv'%group, "w") as csv_file:
        # #     for pid in data:
        # #         start=False
        # #         for date in sorted(data[pid]['appt']):
        # #             if 'Benign' in str(list(nodedesc.keys())[list(nodedesc.values()).index(data[pid]['appt'][date]['diag'])]):
        # #                 start =True
        # #             if start ==True:
        # #                 writer = csv.writer(csv_file, delimiter=',')
        # #                 # combined_row = []
        # #                 # combined_row.append(pid)
        # #                 # combined_row.append(data[pid]['appt'][date]['actualdate'])                    
        # #                 # if data[pid]['appt'][date]['type']=='E':
        # #                 #     combined_row.append(data[pid]['appt'][date]['type']+'type')
        # #                 #     writer.writerow(combined_row)

        # #                 combined_row = []
        # #                 combined_row.append(pid)
        # #                 combined_row.append(data[pid]['appt'][date]['actualdate'])                    
        # #                 if str(data[pid]['appt'][date]['diag'])!='D_NR':
        # #                     combined_row.append(str(list(nodedesc.keys())[list(nodedesc.values()).index(data[pid]['appt'][date]['diag'])]))
        # #                     combined_row.append(data[pid]['appt'][date]['type']+'type')
        # #                     writer.writerow(combined_row)
                        
        # #                 combined_row = []
        # #                 combined_row.append(pid)
        # #                 combined_row.append(data[pid]['appt'][date]['actualdate'])                   
        # #                 if str(data[pid]['appt'][date]['proc'])!='O_NR':
        # #                     combined_row.append(str(data[pid]['appt'][date]['proc']))
        # #                     combined_row.append(data[pid]['appt'][date]['type']+'type')
        # #                     writer.writerow(combined_row)
                        
        # #                 combined_row = []
        # #                 combined_row.append(pid)
        # #                 combined_row.append(data[pid]['appt'][date]['actualdate'])
        # #                 if str(data[pid]['appt'][date]['drugclass'])!='M_NR':
        # #                 # combined_row.append(str(data[pid]['appt'][date]['drugclass']))
        # #                 # combined_row.append(data[pid]['appt'][date]['type']+'type')
        # #                 # writer.writerow(combined_row)
                    
        # print ("spde created")  

        # VT = self.findRepeats(VT)
       

        # VT2=copy.deepcopy(VT)  
        # for pid in VT2:
             
        #     if len(VT2[pid])>1: 
        #         if VT2[pid][1][0]!='V':  #for inpatient with discharge type
        #             del VT[pid]
        # c=0
        print('len data', len(VT))
        for pid in VT:
          if len(VT[pid])>1:
            print (pid,VT[pid])
        #     for i in range(len(VT[pid])):
        #         print (pid,i+1,1,VT[pid][i])
        
        # s = Sample()
        # VT_train, VT_test = s.getTrainTest(VT, 0.2)

        # pickle_out = open('output/' + conditionname + '_VT_test.pickle', 'wb')
        # pickle.dump(VT_test, pickle_out)
        # pickle_out.close()
        return VT,tempDT
        # return VT_train, VT_test, tempDT, OT

    def findRepeats(self, VT):
        
        # #IF GET ACTUAL REPEATS
        # for pid in VT:
        #     seen[pid]=set()
        #     uniq[pid]={}
        #     for x in range(len(VT[pid])):
        #         if VT[pid][x] not in seen[pid]:
        #             uniq[pid][VT[pid][x]]=0
        #             uniq[pid][VT[pid][x]]=1+uniq[pid][VT[pid][x]]
        #             seen[pid].add(VT[pid][x])
        #         else:
        #             uniq[pid][VT[pid][x]]=uniq[pid][VT[pid][x]]+1
        #             VT[pid][x]=str(VT[pid][x])+'_'+str(uniq[pid][VT[pid][x]])
        # IF ONLY LABEL per patient
        seen={}
        uniq={}
        for pid in VT:
            seen[pid] = set()
            uniq[pid] = {}
            for x in range(len(VT[pid])):
                if VT[pid][x] not in seen[pid]:
                    uniq[pid][VT[pid][x]] = 0
                    uniq[pid][VT[pid][x]] = 1 + uniq[pid][VT[pid][x]]
                    seen[pid].add(VT[pid][x])
                else:
                    uniq[pid][VT[pid][x]] = uniq[pid][VT[pid][x]]
                    VT[pid][x] = str(VT[pid][x]) + '_' + str(uniq[pid][VT[pid][x]])

        
        return VT

    def addTime(self, VT, traindata,testdata,tempDT):
        DT = dict()
        # for pid in tempDT:
        #     DT[pid] = list()
        #     for i in range(len(tempDT[pid])-1):
        #         try:
        #             # diff=(datetime.datetime.strptime(tempDT[pid][i+1],'%Y-%m-%d')-datetime.datetime.strptime(tempDT[pid][i],'%Y-%m-%d')).days
        #             # # print diff,tempDT[pid][i+1],tempDT[pid][i]
        #             # if diff>0 and diff<122:

        #             #     diff='less than 4 months'
        #             # elif diff>=122:

        #             #     diff='more than 4 months'
        #             # else:
        #             #     # print diff,pid,tempDT[pid][3],tempDT[pid][2]
        #             #     diff='na'
        #             diff='na'
        #             DT[pid].append(diff)

        #             # DT[pid].append('na')
        #         except:
        #             pass
        # # for pid in DT:
        # #     print pid, DT[pid]
        # path = '/Users/yiz2014/Documents/Data/OMOP/'
        # pickle_out = open(path+'CLEVER_VT.pickle','rb')
        # VT = pickle.load(pickle_out)
        # pickle_out.close()
        # s = Sample()
        # sample=s.getSubgroup('18')
        # print ('sample',len(sample))

        # for pid in VT:
        #     print (pid,VT[pid])

        # with open(path+'CLEVER_seq.csv', "wb") as csv_file:
        #     writer = csv.writer(csv_file, delimiter=',')
        #     for line in VT:
        #         writer.writerow(line)

        visitpair_train = dict()
        j = 0

        for pid in VT:
            if pid in traindata:
                for i in range(0, len(VT[pid]) - 1):
                    # for i in range(0, min(len(VT[pid]) - 1, 4)):
                    try:
                        # visitpair[j]=(VT[pid][i],VT[pid][i+1],DT[pid][i])
                        visitpair_train[j] = [VT[pid][i], VT[pid][i + 1], pid]
                        j = j + 1
                    except:
                        pass
        visitpair_test = dict()
        j = 0

        for pid in VT:
            if pid in testdata:
                for i in range(0, len(VT[pid]) - 1):
                    # for i in range(0, min(len(VT[pid]) - 1, 4)):
                    try:
                        # visitpair[j]=(VT[pid][i],VT[pid][i+1],DT[pid][i])
                        visitpair_test[j] = [VT[pid][i], VT[pid][i + 1], pid]

                        j = j + 1
                    except:
                        pass

        visitpair=copy.deepcopy(visitpair_train)

        for key in visitpair_train:
            delflag = True
            for key2 in visitpair_test:
                if (visitpair_train[key][0],visitpair_train[key][1])==(visitpair_test[key2][0],visitpair_test[key2][1]):
                    # print (visitpair_train[key][0],visitpair_train[key][1])
                    delflag=False
                    break
            if delflag==True:
                del visitpair[key]


        # print('train',visitpair_train)
        # print('test', visitpair_test)
        # print('final', visitpair)
        return visitpair, DT

    def getTrans(self, visitpair, VT, DT, prob, count):
        pairinput, pairinputdelta = processPair(visitpair)
        pairoutput = getTr(pairinput, pairinputdelta)
        # getVV.getVV(pairoutput)
        # visitpair2,VVseq=self.getVVseq(VT,DT)
        # VVseqinput,targetct=processPair2.processPair2(visitpair2)
        # VVseqoutput=getTr2.getTr2(VVseqinput,targetct)
        # # finalgraph=VVseqoutput
        # finalgraphVV=getGraph.getGraph(VVseqoutput,prob,count) #using VV

        # with open(JSON_FILE_OUT, 'w') as outfile:
        #     json.dump(finalgraphVV, outfile)

        # return finalgraphVV,pairoutput,VVseq #using VV
        
        return pairoutput  # using V

    def visualizeV(self, pairoutput, prob, count):
        finalgraphV = getGraph(pairoutput, prob, count)
        with open(JSON_FILE_OUT, 'w') as outfile:
            json.dump(finalgraphV, outfile)

        return finalgraphV

    def getVVseq(self, VT, DT):
        l = LookUp()
        VVdesc = l.getVV()
        VVseq = dict()
        visitpair = dict()

        j = 0
        for pid in VT:
            VVseq[pid] = list()
            for i in range(0, len(VT[pid]) - 1):
                # for i in range(0, min(len(VT[pid]) - 1,2)):

                visitpair[j] = list()
                visitpair[j].append(VT[pid][i])
                visitpair[j].append(VT[pid][i + 1])
                try:
                    visitpair[j].append(DT[pid][i])
                except Exception as e:
                    print (e)

                for t in VVdesc.keys():
                    if visitpair[j] == VVdesc[t]:
                        VVseq[pid].append(t)
                        break

                j = j + 1

        for pid in VVseq:
            # for i in range(len(VVseq[pid])):
            #     print pid, i,'1',VVseq[pid][i]
            print (pid, VVseq[pid])

        visitpair2 = {}
        j = 0
        for pid in VVseq:
            for i in range(0, len(VVseq[pid]) - 1):
                visitpair2[j] = (VVseq[pid][i], VVseq[pid][i + 1])
                j = j + 1

        return visitpair2, VVseq
