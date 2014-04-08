# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:46:47 2014

@author: stephan
@version: 0.2 ( helper functions aggregated into helper class)
"""

# check data submission form 
#  -- against files in filesystem
#  -- (later: against CV`s)


import datetime
try:
    import xlrd
except ImportError:
    print "Error: Required xsl(x) handling module xlrd not available"

class submission(object):  
          
    def __init__(self,settings):
        self.Settings = settings 
    
    def load_wb(self,workbook_name):
        # ToDo: call some checks
        wb = xlrd.open_workbook(self.Settings['git_dir']+'Sheets/Submission_Sheets/'+workbook_name,formatting_info=True)
        
        return wb
        
        
    def load_wb_values(self,wb,sheet_name):
        
        sheet = wb.sheet_by_name(sheet_name)
        num_rows = sheet.nrows - 1
        # num_cells = sheet.ncols - 1
        curr_row = -1
        gen_info = {}
        while curr_row < num_rows:
            curr_row += 1
            # row = worksheet.row(curr_row)
            
            #cell = sheet.cell(curr_row,0)
            rd_xf = wb.xf_list[sheet.cell_xf_index(curr_row,0)]
            cell_font = wb.font_list[rd_xf.font_index]
            #print cell_font.colour_index
            
            raw_top = sheet.cell_value(curr_row, 0).strip()
            
            # fmt = wb.xf_list[cell.xf_index]
            # fmt.dump()
        
            raw_val = sheet.cell_value(curr_row, 3)
            raw_type = sheet.cell_type(curr_row, 3)
            # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
            if raw_type == 1:
                raw_val = raw_val.strip()
            if raw_type == 3:
                (year, month, day, hour, minute, second) = xlrd.xldate_as_tuple(raw_val,wb.datemode)
                raw_val = datetime.datetime(year, month, day, hour, minute, second)
            
            if gen_info.has_key(raw_top): 
               gen_info[raw_top] = gen_info[raw_top].append(raw_top)
            gen_info[raw_top] = [raw_val, raw_type]    
        return gen_info
    
    def check_cordex_submission_form_parts(self,form):
       cordex_forms = [u'ReadMe', u'GeneralInfo', u'day', u'mon', u'sem', u'fx', u'StatPublProc']
       if form.sheet_names() == cordex_forms:
         return "ok"
       else: 
         message1 = "Submission form sheets not matching:"
         message2=  "required are: ReadMe, GeneralInfo, day, mon, sem, fx and StatPublProc"
         return message1+message2
    
    # grab variable_lists from cordex worksheets
    def get_variable_list(self,wb, worksheet_name):
        
        worksheet = wb.sheet_by_name(worksheet_name)
        num_rows = worksheet.nrows - 1
        #num_cells = worksheet.ncols - 1
        curr_row = 4
        variable_list = []
        while curr_row < num_rows:
            curr_row += 1
            
         #   cell = worksheet.cell(curr_row,1)
            rd_xf = wb.xf_list[worksheet.cell_xf_index(curr_row,1)]
            cell_font = wb.font_list[rd_xf.font_index]
                        
            
            variable=worksheet.cell_value(curr_row,1)
            if cell_font.colour_index == 32767:
                variable_list.append(variable)  
            else:
                print "not provided:",
                print variable
        return variable_list
    
    def get_variables_on_disk(self,prefix,geninfo_dict):
        id_mapping = {       
                      'subdate':'Date',
                      'contact':'Contact point during data publication', 
                      'institute_id':'CORDEX institution ID',
                      'model_id':'CORDEX RCM model ID',
                      'experiment_id':'CORDEX experiment ID',
                      'driving_model_id':'CORDEX ID for driving (model) data',
                      'driving_model_ensemble_member':'driving_model_ensemble_member',
                      'rcm_version_id':'RCM version ID',
                      'CORDEX_domain':'CORDEX domain ID',
                      'qc':'Quality ensurance (QC)',
                      'TOU':'Terms of Use',
                      'exclude_vars':'Variables NOT to be published'
             }
      
        id_map = {}
        
        for id in id_mapping:
            id_map[id] = geninfo_dict[id_mapping[id]][0]
        
        print id_map  
        assert id_map['model_id'].startswith(id_map['institute_id']), 'model_id does not start with institute_id'
        
        import glob
        
    
        dir_pattern = prefix+"/%(CORDEX_domain)s/%(institute_id)s/%(driving_model_id)s/%(experiment_id)s/%(driving_model_ensemble_member)s/%(model_id)s/%(rcm_version_id)s/*/*"
        
        file_pattern = dir_pattern % id_map
        print file_pattern
        
        matching = glob.glob(file_pattern)
        
        disc_vars = []
        
        for i,val in enumerate(matching):
           result = matching[i].split("/")
           disc_vars.append(result[-1])
            
        return disc_vars    
   
def main():
    
    sheets_available = {'knmi1':"CORDEX_ESGF_data_submission_form-KNMI-req01.xls"}
    my_settings = {'git_dir':'/home/stephan/Repos/cordex/'}
    my_submission = submission(my_settings) 
    
    wb = my_submission.load_wb(sheets_available['knmi1'])
    
    generalinfo_dict = my_submission.load_wb_values(wb,'GeneralInfo')
    
    print generalinfo_dict
    
    var_list_day = my_submission.get_variable_list(wb,'day')
    var_list_mon = my_submission.get_variable_list(wb,'mon')
    var_list_sem = my_submission.get_variable_list(wb,'sem')
    var_list_fx = my_submission.get_variable_list(wb,'fx')
    
    announced_vars = var_list_day + var_list_mon + var_list_sem + var_list_fx
    
    disc_vars = my_submission.get_variables_on_disk("/gpfs_750/projects/CORDEX/data/cordex/output",generalinfo_dict)
    #print announced_vars
    # announced but not available
    missing_vars = set(announced_vars) - set(disc_vars)
    # available but not announced
    additional_vars = set(disc_vars) - set(announced_vars)
    
    print "Missing Vars:" 
    print missing_vars
    print "Addintional_vars"
    print additional_vars
    
        
    
if __name__ == '__main__':
   main()    
    
    

    
    