#!/bin/env python 


# Generation of CVs from coordination exel sheet
# Requiremts:
# -- python version >=2.7
# -- pandas library
# -- pyesgf library
# Input:
# -- File named CORDEX_ESGF_coordination_issues.xslx in directory ../Cordex_Forms
# -- Path to where the repo containing this script was checked out
#
# Output:
# -- cordex_rcm.txt     (cordex rcm name and institute cv)
# -- cordex_ToU.txt     (terms of use for rcms list)
# -- cordex_status.txt  (ESGV cordex availability)
# author: S. Kindermann
# verson: 0.3
#
import datetime
import time
import pandas as pd
from pyesgf.search import SearchConnection
from web import make_html_table, make_domain_table

class CV_Gen(object):
    
    def __init__(self, my_settings):
        self.Settings = my_settings  
        self.cv_sheet = self.load_coordination_sheet()

    
    def get_esgf_cordex_info(self):
        
        res_dict = {}
        models = {}
        driving_models = {}
        
        conn = SearchConnection('http://esgf-data.dkrz.de/esg-search',distrib=True)
        ctx = conn.new_context(project='CORDEX',replica=False)
        
        domains = ctx.facet_counts['domain'].keys()

        for key in domains:
            ctx2 = conn.new_context(project='CORDEX',domain=key,replica=False)
            models[key] = ctx2.facet_counts['model'].keys()
            driving_models[key]={}
            for thismodel in models[key]:
                 ctx3 = conn.new_context(project='CORDEX',domain=key,model=thismodel,replica=False)
            
                 driving_models[key][thismodel] =  ctx3.facet_counts['driving_model'].keys()
    
        return driving_models
    
    def print_status(self,info_dict,outputfile='Lists/cordex_status.html'):
        
        cv_file = open(self.Settings['git_dir']+outputfile,"w")
        timestamp = '# Timestamp: ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') +'\n'
        #cv_file.write('# CORDEX Availability Matrix \n')
        #cv_file.write('# dynamically retrieved from ESGF at \n')
        #cv_file.write(timestamp)
        #cv_file.write('\n')
        #cv_file.write('# Domain                   Model         Driving Model \n')
       
        cordex_status = {}
        for domain in sorted(info_dict.keys()):
            #cv_file.write('# --------------------------------------------------------\n')
            cordex_status[domain] = []
            for this_model in sorted(info_dict[domain]):
                    #cv_file.write('#                   --------------------------------------\n')
                    for this_driver in sorted(info_dict[domain][this_model]):
                        line = "{0:<25}".format(domain) + "{0:<15}".format(this_model) + "{0:<15}".format(this_driver) + "\n"
                       
                        cordex_status[domain].append([domain,this_model,this_driver])
                        #cv_file.write(line)
        print cordex_status                
        my_table = make_domain_table(cordex_status,timestamp)
        cv_file.write(my_table)
        #print cordex_status
        cv_file.close()
        
# domain / simulations for domain / what CMIP5 are downscaled by each RCM 
        
        
    
    
    def print_cv(self,output_format='plain',outputfile='Lists/CORDEX_ToU_RCMModel.txt'):
    # ToDo: use json as a primary format and write different export functionalities 
    # to support csv, xml, rdf etc. 
        print "schreibe:"
        print outputfile
        cv_file = open(self.Settings['git_dir']+outputfile,"w")
        
        val = ['  name','institute','status','ToU']
        line = '#'+"{0:<25}".format(val[0]) + "{0:<15}".format(val[1]) + "{0:<15}".format(val[2]) + "{0:<15}".format(val[3])+ "\n"
        
        timestamp = '# Timestamp: ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') +'\n'
        if output_format == "plain":
            
            my_heading1 = "# List of RCMModelName values for CORDEX \n"
            my_heading2 = "# Do not change this file, its auto-generated based on the contents \n"
            my_heading3 = "# of the CORDEX coordination sheet at: \n"
            my_heading4 = "# https://github.com/IS-ENES-Data/cordex-doc/blob/master/Sheets/CORDEX_ESGF_coordination_issues.xlsx \n"
            my_heading5 = "# -------------------------------------------------------------- \n"
                    
            
            cv_file.write(my_heading1+my_heading2+my_heading3+my_heading4+timestamp+my_heading5)
            cv_file.write(line)
            cv_file.write("#--------------------------------------------------------------- \n")
            for key, val in sorted(self.cv_sheet.iteritems()): 
                 if key != u'model_id': 
                    line = "{0:<25}".format(val[0]) + "{0:<15}".format(val[4]) + "{0:<15}".format(val[2]) + "{0:<15}".format(val[3]) + "\n"
                    if (isinstance(val[0],basestring) and isinstance(val[1],basestring) and isinstance(val[2],basestring)):
                        
                        cv_file.write(line)
                        
             
        if output_format == "csv": 
            for key, val in sorted(self.cv_sheet.iteritems()):
                line = "{0:<25}".format(key+',') + "{0:<15}".format(val[4]+',') + "{0:<15}".format(val[2]) + '\n'+ "{0:<15}".format(val[3]) +"\n"
                cv_file.write(line)
                
        if output_format =="html":
            
            output_dict = {}
            for key, val in sorted(self.cv_sheet.iteritems()):
                if key != u'model_id' and (isinstance(val[0],basestring) and isinstance(val[4],basestring) and isinstance(val[2],basestring)):
                     output_dict[key] = [key,val[4],val[2],val[3]]
            line = make_html_table(output_dict)
            cv_file.write(line)
            
        cv_file.close()    
        return
    
    
    def check_sheet_ok(self,wb):
    ## deprecated   
        if openpyxl_loaded == True:
            sheet_names = wb.get_sheet_names()
        elif xlrd_loaded == True:
            sheet_names = wb.sheet_names()
        else:
            sheet_names = ['Error: No sheet names']
            
        if sheet_names == ['GeneralRemarks', 'AllEntries', 'DatVol', 'ControlledVocabulary']:
            return True
        else:
            return False
            
    def is_valid(self,shval_list):
        valid = True
       
        for val in shval_list:
            if val == None: 
                valid = False
            elif not isinstance(val,basestring): 
                valid = False
            elif isinstance(val,basestring):
                if val.strip() in ["","model_id"]: 
                    valid = False         
                    
        return valid           
                
        
    def load_coordination_sheet(self):
        
        cordex_coordination_issues = self.Settings['git_dir']+'Sheets/CORDEX_ESGF_coordination_issues.xlsx'
        
        cv_sheet = pd.read_excel(cordex_coordination_issues,'ControlledVocabulary',index_col=None, na_values=['NA']) 
        
        res_dict = {}
        
        for item, frame in cv_sheet.iteritems():
            res_dict[frame[4]] = [frame[4], frame[3], frame[6],frame[5],frame[1]]
            
        return res_dict    
        


if __name__ == "__main__":  
    my_settings = {'git_dir':'/home/stephan/Repos/cordex-doc/'}
    
    my_cv = CV_Gen(my_settings)
    
    my_cv.print_cv(output_format='plain')
    my_cv.print_cv(output_format='html',outputfile='Lists/CORDEX_ToU_RCMModel.html')
    
    driving_models = my_cv.get_esgf_cordex_info()
    #print driving_models
        
#    for key,val in driving_models.iteritems():
#        
#        print key, val 
        
    my_cv.print_status(driving_models)   
    #my_cv.print_status(cordex_info)
    
    #my_cv.print_status(cordex_info)
    
    
    
    



