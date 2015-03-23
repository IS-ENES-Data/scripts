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
        # [institute_id,institution, RCM_name,model_id,ToU,Status,comments] = [cv_sheet[0],cv_sheet[1],cv_sheet[2],cv_sheet[3],cv_sheet[4],cv_sheet[5],cv_sheet[6)]
       
    
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
    
    def print_status(self,info_dict,outputfile='cordex_status.html'):
        
        cv_file = open(self.Settings['output_dir']+outputfile,"w")
        timestamp = '#  ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' # \n'
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
        
        
    
    
    def print_cv(self,output_format='plain',outputfile='CORDEX_ToU_RCMModel.txt'):
    # ToDo: use json as a primary format and write different export functionalities 
    # to support csv, xml, rdf etc. 
        print "schreibe ORDEX_ToU_RCMModel.txt:"
        print outputfile
        cv_file = open(self.Settings['output_dir']+outputfile,"w")
        
        val = ['  name','institute','status','ToU']
        line = '#'+"{0:<25}".format(val[0]) + "{0:<15}".format(val[1]) + "{0:<15}".format(val[2]) + "{0:<15}".format(val[3])+ "\n"
        
        timestamp = '# Timestamp:  ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') +'\n'
        if output_format == "plain":
            
            my_heading1 = "# List of RCMModelName values for CORDEX \n"
            my_heading2 = "# Do not change this file, its auto-generated based on the contents \n"
            my_heading3 = "# of the CORDEX coordination sheet at: \n"
            my_heading4 = "# https://github.com/IS-ENES-Data/cordex/raw/master/CORDEX_ESGF_coordination_issues.xlsx \n"
            my_heading5 = "# -------------------------------------------------------------- \n"
                    
            
            cv_file.write(my_heading1+my_heading2+my_heading3+my_heading4+timestamp+my_heading5)
            cv_file.write(line)
            cv_file.write("#--------------------------------------------------------------- \n")
                
              
            for key, val in sorted(self.cv_sheet.iteritems()):
                
                [institute_id_val,institution_val,RCM_name_val,model_id_val,ToU_val,Status_val,Commments_val] = [val[0],val[1],val[2],val[3],val[4],val[5],val[6]]
                
                print institute_id_val
                print "--------/n"
                if key != 'model_id' and not(pd.isnull(key)): 
                    line = "{0:<25}".format(model_id_val) + "{0:<15}".format(institute_id_val) + "{0:<15}".format(Status_val) + "{0:<15}".format(ToU_val) + "\n"
                    if (isinstance(val[0],basestring) and isinstance(val[1],basestring) and isinstance(val[2],basestring)):
                        cv_file.write(line)
               
                        
             
        if output_format == "csv": 
            for key, val in sorted(self.cv_sheet.iteritems()):
                line = "{0:<25}".format(key+',') + "{0:<15}".format(val[4]+',') + "{0:<15}".format(val[2]) + '\n'+ "{0:<15}".format(val[3]) +"\n"
                cv_file.write(line)
                
        if output_format =="html":
            
            output_dict = {}
            for key, val in sorted(self.cv_sheet.iteritems()):
                [institute_id_val,institution_val,RCM_name_val,model_id_val,ToU_val,Status_val,Commments_val] = [val[0],val[1],val[2],val[3],val[4],val[5],val[6]]
                if key != u'model_id' and (isinstance(val[0],basestring) and isinstance(val[4],basestring) and isinstance(val[2],basestring)):
                     output_dict[key] = [key,RCM_name_val,Status_val,ToU_val]
            timestamp = '#  ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' # \n'         
            print "llllllllllllllllllllllllllllllllllllllllllllllllll"
            print output_dict
            line = make_html_table(output_dict,timestamp)
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
         
    def filter_val(self,val):            
        if pd.isnull(val): val = "not filled"
        
        return val
        
    def load_coordination_sheet(self):
        
        cordex_coordination_issues = self.Settings['cordex_dir']+'CORDEX_ESGF_coordination_issues.xlsx'
        
        cv_sheet = pd.read_excel(cordex_coordination_issues,'ControlledVocabulary',skiprows=0, index_col=None, na_values=['NA']) 
        
        res_dict = {}
        
        for item, frame in cv_sheet.iteritems():
            if not pd.isnull(frame[4]): 
                # frame[1]=institute_id
                # frmae[2]=institution
                # frame[3]=RCM name
                # frmae[4]=model_id
                # frame[5]=ToU
                # frmae[6]=Status
                # frame[7]=Comments
                res_dict[frame[4]] = [self.filter_val(frame[1]),self.filter_val(frame[2]),self.filter_val(frame[3]),self.filter_val(frame[4]),self.filter_val(frame[5]),self.filter_val(frame[6]),self.filter_val(frame[7])] 
        print res_dict    
        return res_dict    
        


if __name__ == "__main__":  
    my_settings = {'git_dir':'/home/stephan/Repos/scripts/','cordex_dir':'/home/stephan/Repos/cordex/','output_dir':'/home/stephan/Repos/IS-ENES-Data.github.io/'}
    
    my_cv = CV_Gen(my_settings)
    
    my_cv.print_cv(output_format='plain')
    my_cv.print_cv(output_format='html',outputfile='CORDEX_ToU_RCMModel.html')
    
    driving_models = my_cv.get_esgf_cordex_info()
    #print driving_models
        
#    for key,val in driving_models.iteritems():
#        
#        print key, val 
        
    my_cv.print_status(driving_models)   
    #my_cv.print_status(cordex_info)
    
    #my_cv.print_status(cordex_info)
    
    
    
    



