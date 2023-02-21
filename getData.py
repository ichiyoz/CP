__author__ = "Yiye Zhang"
__date__="07/09/2016"

from app.logic.getV import Structure
from app.logic.getSample import Sample
from numpy import *
import json
from copy import deepcopy
from app.names import Names
from collections import Counter
import datetime
from datetime import datetime, timedelta
import os
import pickle
import csv
import copy

JSON_FILE = "data/sample_data.json"
n=Names()
conditionname, path = n.Names()

class Data:
    def getData(self,newdata,pidname,group,testing):

        # for pid in newdata:
        #     print (pid,'#',newdata[pid]['fips'],'#',newdata[pid]['race'],'#',newdata[pid]['age'])

        # firstdate={}
        # for pid in newdata:
        #     for date in newdata[pid]['appt']:
        #         firstdate[pid]=newdata[pid]['appt'][date]['actualdate']
        #         break
        #     for date in newdata[pid]['appt']:
        #         # print (pid,date,newdata[pid]['appt'][date]['EF'])
        #         diff = (datetime.strptime(newdata[pid]['appt'][date]['actualdate'], '%Y-%m-%d')-datetime.strptime(firstdate[pid],'%Y-%m-%d')).days
        #         # print (diff,firstdate[pid],newdata[pid]['appt'][date]['actualdate'])
        #         if diff<1825:
                
        #             if ('%' in newdata[pid]['appt'][date]['EF']) and ('-' in newdata[pid]['appt'][date]['EF']):
        #                 print (pid,diff+1,newdata[pid]['appt'][date]['EF'][0:2])
        #             elif '%' in newdata[pid]['appt'][date]['EF']:
        #                 print (pid,diff+1,newdata[pid]['appt'][date]['EF'].replace('%',''))
        #             elif 'greater than' in newdata[pid]['appt'][date]['EF']:
        #                 print (pid,diff+1,newdata[pid]['appt'][date]['EF'].replace('greater than \n',''))
        #             elif 'about' in newdata[pid]['appt'][date]['EF']:
        #                 print (pid,diff+1,newdata[pid]['appt'][date]['EF'][0:2])
        #             elif '-' in newdata[pid]['appt'][date]['EF']:
        #                 print (pid,diff+1,newdata[pid]['appt'][date]['EF'][0:2])
        #             elif '~ ' in newdata[pid]['appt'][date]['EF']:
        #                 print (pid,diff+1,newdata[pid]['appt'][date]['EF'].replace('~ ',''))
        #             elif newdata[pid]['appt'][date]['EF']=='':
        #                 pass
        #             elif float(newdata[pid]['appt'][date]['EF'])<1:
        #                 print (pid,diff+1,float(newdata[pid]['appt'][date]['EF'])*100)
        #             else:
        #                 print (pid,diff+1,newdata[pid]['appt'][date]['EF'])
        # for pid in newdata:
        #     for date in newdata[pid]['appt']:
        #         print (newdata[pid]['appt'][date]['type'])

        s = Sample()
        matchpt=len(newdata)
        
        print ("before",matchpt)
        ptlist=[]
        traindata={}
        testdata={}
        if group!='':
            newdata,ptlist=s.getSpecificGrp(newdata,group)
        elif testing==True:
            newdata,traindata,testdata=s.getTrainTest(newdata,0.2)
            print('getting training/testing')
            # pass
        elif pidname!='':
            newdata, ptlist = s.getSpecificPt(newdata, pidname)
            print('getting patient')
        else:
            print('getting all data')
            pass

        matchpt=len(newdata)
        print ("after",matchpt)
        ptlist=[]

        data3 = deepcopy(newdata)

        t = Structure()
        node = t.getNode(data3)
        t.getV(node, data3)
        # self.getDemo(newdata)
        
        return newdata,traindata,testdata,ptlist

    def getDuration(self,newdata):
        dur={}
        firstdate={}
        for pid in newdata:
            for date in newdata[pid]['appt']:
                firstdate[pid]=newdata[pid]['appt'][date]['actualdate']
                break
            dur[pid]=[]
            for date in newdata[pid]:
                diff = (datetime.strptime(newdata[pid]['appt'][date]['actualdate'], '%Y-%m-%d')-datetime.strptime(firstdate[pid],'%Y-%m-%d')).days
                if diff>0:
                    dur[pid].append(diff)
            print(sum(dur[pid])/len(dur[pid]))
        durall=[]
        for pid in dur:
            durall.append(sum(dur[pid])/len(dur[pid]))
        print('avg duration',sum(durall)/len(durall))

        return 

    def printDisco(self,newdata,group):
        disco={}
        firstdate={}
        for pid in newdata:
            visit=[]
            diag={}
            drug={}
            for date in newdata[pid]['appt']:
                firstdate[pid]=newdata[pid]['appt'][date]['actualdate']
                break
            disco[pid]=[]  
            diag[pid]=[]
            drug[pid]=[]              
            for date in sorted(newdata[pid]['appt']):
                diff = (datetime.strptime(newdata[pid]['appt'][date]['actualdate'], '%Y-%m-%d')-datetime.strptime(firstdate[pid],'%Y-%m-%d')).days
                # print (diff,firstdate[pid],newdata[pid]['appt'][date]['actualdate'])
                if diff<1825:
                    # if newdata[pid]['appt'][date]['type']=='E' or newdata[pid]['appt'][date]['type']=='I':
                    #     # disco[pid].append([newdata[pid]['appt'][date]['type'],newdata[pid]['appt'][date]['actualdate']])
                    #     disco[pid].append([newdata[pid]['appt'][date]['type'],diff])
                    for i in sorted(newdata[pid]['appt'][date]['diag']):
                        if i not in visit:
                            # disco[pid].append([i,newdata[pid]['appt'][date]['actualdate']])
                            disco[pid].append([i,str(diff+1)])
                            visit.append(i)
                    for i in sorted(newdata[pid]['appt'][date]['drugclass']):
                        if i not in visit:
                            disco[pid].append([i,str(diff+1)])
                            visit.append(i)
        with open(path+conditionname+'_DISCO_%s.csv'%group, "w") as csv_file:        
            writer = csv.writer(csv_file, delimiter=',')
            for pid in disco:    
              if len(disco[pid])>0:   
                for i in range(len(disco[pid])):
                    combined_row = []
                    combined_row.append(pid)
                    combined_row.append(disco[pid][i][1])                
                    combined_row.append(1)           
                    a=disco[pid][i][0].replace(",", "")
                    combined_row.append(a.replace(" ", ""))
                    writer.writerow(combined_row)
                    
                        # combined_row = []
                        # combined_row.append(pid)
                        # combined_row.append(data[pid]['appt'][date]['actualdate'])                   
                        # if str(data[pid]['appt'][date]['proc'])!='O_NR':
                        #     combined_row.append(str(list(nodedesc.keys())[list(nodedesc.values()).index(data[pid]['appt'][date]['proc'])]))
                        #     writer.writerow(combined_row)
                        
                        # if len(newdata[pid]['appt'][date]['drugclass'])>0:
                        #     i=i+1
                        #     combined_row = []
                        #     combined_row.append(pid)
                        #     combined_row.append(newdata[pid]['appt'][date]['actualdate'])                          
                        #     combined_row.append(len(newdata[pid]['appt'][date]['drugclass']))  
                        #     combined_row.append(newdata[pid]['appt'][date]['drugclass'])
                        #     writer.writerow(combined_row)
                     
        print ("Disco created")  
        return 

    def printSPADE(self,newdata,group):
        noincludelist=['Chronic kidney disease, unspecified','Other and unspecified mitral valve diseases','Other forms of asthma','Diastolic heart failure, unspecified','Chronic obstructive asthma with status asthmaticus','Chronic obstructive asthma, unspecified','Other osteoporosis','Diseases of aortic valve','Coronary atherosclerosis due to lipid rich plaque','Systolic heart failure, unspecified','Dementia, unspecified, without behavioral disturbance','Acutekidneyfailureunspecified']
        with open(path+conditionname+'_DISCO_%s.csv'%group, "w") as csv_file:        
            writer = csv.writer(csv_file, delimiter=',')
            firstdate={}
            diag={}
            for pid in newdata:
                diag[pid]=[]
                for date in newdata[pid]['appt']:
                    firstdate[pid]=newdata[pid]['appt'][date]['actualdate']
                    break
                             
                for date in sorted(newdata[pid]['appt']):
                    diff = (datetime.strptime(newdata[pid]['appt'][date]['actualdate'], '%Y-%m-%d')-datetime.strptime(firstdate[pid],'%Y-%m-%d')).days
                    
                    if diff<1825 and len(newdata[pid]['appt'][date]['diag'])>0:
                        diaglist=[]
                        for i in newdata[pid]['appt'][date]['diag']:
                          if i not in noincludelist:
                            a=i.replace(",", "")
                            if a.replace(" ", "") not in diag[pid]:
                                diaglist.append(a.replace(" ", ""))
                            diag[pid].append(a.replace(" ", ""))
                          else:
                            pass
                        if len(diaglist)>0:
                            combined_row = []
                            combined_row.append(pid)
                            combined_row.append(diff+1)
                            combined_row.append(len(diaglist))
                            combined_row.append(diaglist)
                            writer.writerow(combined_row)
                         
            print ("SPADE created")  
            return 
    def getStats(self,newdata):
        
        o=0
        h=0
        e=0
        for pid in newdata:            
            for date in newdata[pid]['appt']:
                if newdata[pid]['appt'][date]['type']=='P':
                    o=o+1
                elif newdata[pid]['appt'][date]['type'] == 'I':
                    h = h + 1
                elif newdata[pid]['appt'][date]['type'] == 'E':
                    e = e + 1
        print (o, h, e)
        print ('num he',(h+e)*1.0/(o+h+e))
        diaglist=[]
        for pid in newdata:
            for date in newdata[pid]['appt']:
                for diag in newdata[pid]['appt'][date]['diag']:
                    diaglist.append(diag)
        c=Counter(diaglist)
        print (c.most_common(100))    
        print ('numdiag',len(c))
        druglist=[]
        for pid in newdata:
            for date in newdata[pid]['appt']:
                for drug in newdata[pid]['appt'][date]['drugclass']:
                    druglist.append(drug)
        c=Counter(druglist)
        print (c.most_common(100)) 
        print ('numdrug',len(c))

        proclist=[]
        for pid in newdata:
            for date in newdata[pid]['appt']:
                for proc in newdata[pid]['appt'][date]['proc']:
                    proclist.append(proc)
        c=Counter(proclist)
        print (c.most_common(100))        
        
        # for pid in newdata:
        #     if 'AKI' in newdata[pid]['appt'][4]['diag']:
        #         print pid, 1, newdata[pid]['appt'][4]['stage']
        #     else:
        #         print pid,0,newdata[pid]['appt'][4]['stage']

        # for pid in newdata:
        #     print pid,(datetime.datetime.strptime(newdata[pid]['appt'][3]['actualdate'],'%Y-%m-%d')-datetime.datetime.strptime(newdata[pid]['appt'][0]['actualdate'],'%Y-%m-%d')).days

       

    def getLastDiag(self, newdata):
        for pid in newdata:
            print (pid, newdata[pid]['appt'][len(newdata[pid]['appt'])-1]['diag'])

    def printNoprice(self,newdata):
        emptyprice=[]

        for pid in newdata:
            for date in newdata[pid]['appt']:
                for d in newdata[pid]['appt'][date]['drug']:
                    if d['price']=='':
                        emptyprice.append(d['name'])
        emptyprice=list(set(emptyprice))


    def matchpt(self,data):
        matchpt=len(data)
        return matchpt

    def getDemo(self,newdata):
        for pid in newdata:
            print (pid, newdata[pid]['sex'], newdata[pid]['age'], newdata[pid]['race'])


def main():
    d=Data()
    d.getData()

if __name__ == '__main__':
    main()         
            
