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
import collections
import operator
import datetime
import time
import pandas as pd
from pyesgf.search import SearchConnection
from web import make_html_table, make_domain_table, generate_bias_table, generate_bias_table_add, generate_obs_table
from unidecode import unidecode
import commentjson

class CV_Gen(object):
    
    def __init__(self, my_settings):
        self.Settings = my_settings  
        self.cv_sheet = self.load_coordination_sheet()
      
        # [institute_id,institution, RCM_name,model_id,ToU,Status,comments] = [cv_sheet[0],cv_sheet[1],cv_sheet[2],cv_sheet[3],cv_sheet[4],cv_sheet[5],cv_sheet[6)]
        #print self.cv_sheet
        
        #for key,val in self.cv_sheet.iteritems():
        #    for item in val:
        #       print item
    def load_bias_sheet(self,jsonfilename):    
        jsonfile = open(jsonfilename,"r")
        json_string = jsonfile.read()
        #parser = JsonComment(json)
        jsonfile.close()
        #json_dict = parser.loads(json_info)
        json_dict = commentjson.loads(json_string)
        return json_dict
        
    def get_esgf_cordex_info(self):
        
        res_dict = {}
        models = {}
        driving_models = {}
        
        conn = SearchConnection('http://esgf-data.dkrz.de/esg-search',distrib=True)
        ctx = conn.new_context(project='CORDEX',replica=False)
        #print ctx.hit_count
        
        domains = ctx.facet_counts['domain'].keys()
        #print domains

        for key in domains:
            ctx2 = conn.new_context(project='CORDEX',domain=key,replica=False)
            #print ctx2.hit_count 
            models[key] = ctx2.facet_counts['rcm_name'].keys()
            #print models[key]
            driving_models[key]={}
            for thismodel in models[key]:
              
                 ctx3 = conn.new_context(project='CORDEX',domain=key,rcm_name=thismodel,replica=False)
                 #print key,thismodel
                 #print ctx3.hit_count           
                 driving_models[key][thismodel] =  ctx3.facet_counts['driving_model'].keys()
    
        return driving_models
    
    def print_status(self,info_dict,outputfile='CORDEX_status.html'):
        
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
        
        
    def print_cv(self,output_format='plain',outputfile='CORDEX_RCMs_ToU.txt'):
    # ToDo: use json as a primary format and write different export functionalities 
    # to support csv, xml, rdf etc. 
        #print "schreibe ORDEX_ToU_RCMModel.txt:"
        # print outputfile
        cv_file = open(self.Settings['output_dir']+outputfile,"w")
        
        
        
        timestamp = '# Timestamp:  ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') +'\n'
        if output_format == "info":
            
            val = [' model id','institute id','ToU','institution name']
            line = '#'+"{0:<25}".format(val[0]) + "{0:<15}".format(val[1]) + "{0:<20}".format(val[2])  + "{0:<15}".format(val[3])+ "\n"
            
            my_heading1 = "# List of CORDEX RCMs (full version - including institution names)  \n"
            my_heading2 = "# Do not change this file, its auto-generated based on the contents \n"
            my_heading3 = "# of the CORDEX RCM registration sheet managed at: \n"
            my_heading4 = "# https://github.com/IS-ENES-Data/cordex/raw/master/CORDEX_ESGF_register.xlsx \n"
            my_heading5 = "# ---------------------------------------------------------------------------------------------- \n"
                    
            
            cv_file.write(my_heading1+my_heading2+my_heading3+my_heading4+timestamp+my_heading5)
            cv_file.write(line)
            cv_file.write("# ----------------------------------------------------------------------------------------------- \n")
                
              
            for key, val in self.cv_sheet.iteritems():
                
                [RCM_name_val,institute_id_val,model_id_val,contact_val,institution_val,target_domains_val, terms_of_use_val] = [val[0].encode('utf8'),val[1].encode('utf8'),val[2].encode('utf8'),val[3].encode('utf8'),val[4].encode('utf8'),val[5].encode('utf8'),val[6].encode('utf8')]
                print model_id_val,institute_id_val,terms_of_use_val,institution_val
                line = "{0:<25}".format(model_id_val) + "{0:<15}".format(institute_id_val)   + "{0:<20}".format(terms_of_use_val) + "{0:<15}".format(institution_val)  +"\n"
                #    if (isinstance(val[0],basestring) and isinstance(val[1],basestring) and isinstance(val[2],basestring)):
                cv_file.write(line)
        
        if output_format == "summary":
         
            val = [' model id','institute id','ToU']
            line = '#'+"{0:<20}".format(val[0]) + "{0:<25}".format(val[1]) + "{0:<5}".format(val[2])  + "\n"
            
            my_heading1 = "# List of CORDEX RCMs (short, machine readable version)  \n"
            my_heading2 = "# Do not change this file - it is auto-generated based on the contents \n"
            my_heading3 = "# of the CORDEX RCM registration sheet  \n"
            my_heading4 = "# To register CORDEX simulations please contact cordex-registration /at/ smhi.se \n"
            my_heading5 = "# -------------------------------------------------------------- \n"
                    
            
            cv_file.write(my_heading1+my_heading2+my_heading3+my_heading4+timestamp+my_heading5)
            cv_file.write(line)
            cv_file.write("# --------------------------------------------------------------- \n")
                
              
            for key, val in self.cv_sheet.iteritems():
                
                [RCM_name_val,institute_id_val,model_id_val,contact_val,institution_val,target_domains_val, terms_of_use_val] = [val[0],val[1],val[2],val[3],val[4],val[5],val[6]]
                
                line = "{0:<25}".format(model_id_val) + "{0:<15}".format(institute_id_val)  + "{0:<15}".format(terms_of_use_val) +"\n"
                #    if (isinstance(val[0],basestring) and isinstance(val[1],basestring) and isinstance(val[2],basestring)):
                cv_file.write(line)
                
                
        if output_format == "csv":
         
            
            line = ' model_id, institute_id, terms_of_use \n' 
            cv_file.write(line)
                    
            for key, val in self.cv_sheet.iteritems():
                
                [RCM_name_val,institute_id_val,model_id_val,contact_val,institution_val,target_domains_val, terms_of_use_val] = [val[0],val[1],val[2],val[3],val[4],val[5],val[6]]
                
                line = model_id_val + ", " + institute_id_val + ", " + terms_of_use_val +"\n"
               
                cv_file.write(line)       
         
                        
                
        if output_format =="html":
            
            #output_dict = {}
            #for key, val in self.cv_sheet.iteritems():
                #[institute_id_val,institution_val,RCM_name_val,model_id_val,ToU_val,Status_val,Commments_val] = [val[0],val[1],val[2],val[3],val[4],val[5],val[6]]
                #if key != u'model_id' and (isinstance(val[0],basestring) and isinstance(val[4],basestring) and isinstance(val[2],basestring)):
                #     output_dict[key] = [key,RCM_name_val,Status_val,ToU_val]
            timestamp = '#  ' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + ' # \n'         
            print "llllllllllllllllllllllllllllllllllllllllllllllllll"
            #print output_dict
            #print self.cv_sheet
            line = make_html_table(self.cv_sheet,timestamp)
            cv_file.write(line.encode('utf16'))
            #cv_file.write(line)
            
        cv_file.close()    
        return line
        
    def print_bias(self):
         timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
         infile = self.Settings['cordex_dir']+'CORDEX_adjust_register.json'
         bias_sum_file = open(self.Settings['output_dir']+'CORDEX_adjust_summary.html',"w")
         bias_add_file = open(self.Settings['output_dir']+'CORDEX_adjust_add.html',"w")
         bias_dict = self.load_bias_sheet(infile)
         bias_sum = generate_bias_table(bias_dict,timestamp)
         bias_add = generate_bias_table_add(bias_dict,timestamp)
         bias_sum_file.write(bias_sum.encode('utf8'))
         bias_add_file.write(bias_add.encode('utf8'))
         bias_sum_file.close()
         bias_add_file.close()
         return True
         
    def print_obs(self):
        timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        infile = self.Settings['cordex_dir']+'CORDEX_adjust_obs_register.json'
        obs_file = open(self.Settings['output_dir']+'CORDEX_adjust_obs.html',"w")
        obs_dict = self.load_bias_sheet(infile)
        obs = generate_obs_table(obs_dict,timestamp)
        obs_file.write(obs.encode('utf8'))
        obs_file.close()
        return True
    
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
        
        cordex_coordination_issues = self.Settings['cordex_dir']+'CORDEX_register.xlsx'
        print cordex_coordination_issues

        
        cv_sheet = pd.read_excel(cordex_coordination_issues,'AllEntries',skiprows=0, index_col=None, na_values=['NA']) 
        
        ires_dict = {}
        
        #print("The list of row indices")
        #print(cv_sheet.index)
        #print("The column headings")
        #print(cv_sheet.columns)
       
        ix = 1
        for item, frame in cv_sheet.iterrows():
                
           res=[]
           for el in frame.iteritems():  
               val = el[1]
               res.append(val)
               
           ires_dict[ix]=res
           ix = ix+1
        
        ures_dict = {}
        for key, val in ires_dict.iteritems():
            
                 [RCM_name_val,institute_id_val,model_id_val,contact_val,institution_val,target_domains_val, terms_of_use_val] = [val[0],val[1],val[2],val[3],val[4],val[5],val[6]]
                 if not(model_id_val == 'model_id'): 
                        ures_dict[model_id_val] = val
       
        res_dict = collections.OrderedDict()
        
        for key, val in sorted(ures_dict.iteritems()):
            res_dict[key] = val
    
        
        #print res_dict  
        return res_dict    
    


if __name__ == "__main__":  
    my_settings = {'git_dir':'/home/stephan/Repos/ENES-EUDAT/scripts/','cordex_dir':'/home/stephan/Repos/ENES-EUDAT/cordex/','output_dir':'/home/stephan/Repos/ENES-EUDAT/IS-ENES-Data.github.io/'}
    
    my_cv = CV_Gen(my_settings)
    
    my_cv.print_cv(output_format='summary')
    my_cv.print_cv(output_format='info',outputfile="CORDEX_RCMs_info.txt")
    my_cv.print_cv(output_format='html',outputfile='CORDEX_RCMs_info.html')
    my_cv.print_cv(output_format='csv',outputfile='CORDEX_RCMs_ToU.csv')
    my_cv.print_cv(output_format='summary',outputfile='CORDEX_RCMs_ToU.txt')
    
    driving_models = my_cv.get_esgf_cordex_info()
    #print driving_models
        
#    for key,val in driving_models.iteritems():
#        
#        print key, val 
        
    my_cv.print_status(driving_models)   
    #my_cv.print_status(cordex_info)
    
    #my_cv.print_status(cordex_info)
    
    my_cv.print_bias()

    my_cv.print_obs()
    
    



