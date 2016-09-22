# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 16:51:27 2014

@author: stephan

pupose:
   json files --> dicts
   dicts --> web tables

"""


from mako.template import Template

import commentjson
#import json
#from jsoncomment import JsonComment
def jsonfile_to_dict(jsonfilename):
    jsonfile = open(jsonfilename,"r")
    json_string = jsonfile.read()
    #parser = JsonComment(json)
    jsonfile.close()
    #json_dict = parser.loads(json_info)
    json_dict = commentjson.loads(json_string)
    return json_dict
    
def generate_obs_table(a_dict,timestamp):
    """
     a_dict: dictionary containing json_dictionaries
     structure: ["institution", "institute_id", "dataset", "dataset_id", "reference", "tou_bc_simulation" ]
    """
    my_template =  '''
   
<!DOCTYPE html>
 <html lang="en">
 <head>
  <title>Calibration datasets used for bias adjustment of CORDEX simulations</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
 </head>

 <body>
         
 <div class="container">
  <h2>Calibration datasets used for bias adjustment of CORDEX simulations</h2>
    <p> Information automatically generated based on controled vocabulary </p>
    <p> -- Timestamp: ${my_timestamp} </p>
    <p> To register new calibration datasets please contact <b> cordex-esd-registration /at/ cordex.org </b> </p>
    
    <table class="table table-striped table-bordered">
      <thead> 
       <tr>
        <th>Institution</th>
        <th>Institute ID</th>
        <th>Dataset</th>
        <th>Dataset ID</th>
        <th>Reference</th>
        <th>Terms of Use for bias adjusted CORDEX data</th>
        </tr>
      </thead>     
       
       
          
     <tbody>     
     % for a,b in my_dict.iteritems():
        <tr>
        <td>${b['institution']}</td>
        <td>${b['institute_id']}</td>
        <td>${b['dataset']}</td>
        <td>${b['dataset_id']}</td>
        <td>${b['reference']}</td>
        <td>${b['tou_bc_simulation']}</td>
    
        
        </tr>
     % endfor
     </tbody>
    </table>
    </div>
    
    </body>
    </html>
    '''
   
   
    my_mako_template = Template(my_template)
   
    result = my_mako_template.render(my_dict = a_dict,my_timestamp=timestamp)
    
    return result



    
def generate_bias_table(a_dict,timestamp): 
   """
   a_dict: dictionary containing json_dictionaries
   structure: ["institution", "institute_id", "bc_method", "bc_method_id", "institute_id"-"bc_method_id", 
              "terms_of_use", "CORDEX_domain", "reference", "package" ]
   """
   my_template =  '''
   
<!DOCTYPE html>
 <html lang="en">
 <head>
  <title>CORDEX bias adjustmen methods summary</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
 </head>

 <body>
         
 <div class="container">
  <h2>Summary of bias adjustment methods applied to CORDEX simulations</h2>
    <p> Information automatically generated based on controled vocabulary </p>
    <p> -- Timestamp: ${my_timestamp} </p>
    <p> <a href="http://is-enes-data.github.io/CORDEX_adjust_add.html">(additional information on these bias adjustment methods: reference and software package)</a></p>
    <p> To register new bias adjustment methods please contact <b> cordex-esd-registration /at/ cordex.org </b> </p>
    
    <table class="table table-striped table-bordered">
      <thead> 
       <tr>
        <th>Institution</th>
        <th>Institute ID</th>
        <th>Bias Adjustment</th>
        <th>Bias Adjustment ID</th>
        <th>Bias Adjustment Name</th>
        <th>Terms of Use</th>
        <th>CORDEX Domain</th>
        </tr>
      </thead>     
       
       
          
     <tbody>     
     % for a,b in my_dict.iteritems():
        <tr>
        <td>${b['institution']}</td>
        <td>${b['institute_id']}</td>
        <td>${b['bc_method']}</td>
        <td>${b['bc_method_id']}</td>
        <td>${b['institute_id']+'-'+b['bc_method_id']}</td>
        <td>${b['terms_of_use']}</td>
        <td>${b['CORDEX_domain']}</td>
    
        
        </tr>
     % endfor
     </tbody>
    </table>
    </div>
    
    </body>
    </html>
    '''
   
   
   my_mako_template = Template(my_template)
   
   result = my_mako_template.render(my_dict = a_dict,my_timestamp=timestamp)
    
   return result
              

def generate_bias_table_add(a_dict,timestamp): 
   """
   a_dict: dictionary containing json_dictionaries
   structure: ["institution", "institute_id", "bc_method", "bc_method_id", "institute_id"-"bc_method_id", 
              "terms_of_use", "CORDEX_domain", "reference", "package" ]
   """
   my_template =  '''
   
   
 <!DOCTYPE html>
 <html lang="en">
 <head>
  <title>CORDEX bias adjustment methods: additional info</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
  <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
 </head>
   
    <body>
  <div class="container">  
    <h2> Bias adjustment methods applied to CORDEX simulations: additional information  </h2>
    <p> Information automatically generated based on controled vocabulary </p>
    <p> -- Timestamp: ${my_timestamp} </p>
    <p> <a href="http://is-enes-data.github.io/CORDEX_adjust_summary.html">(Summary of bias adjustment methods)</a></p>
    <p> To register new bias adjustment methods please contact cordex-esd-registration /at/ cordex.org  </p>
    
    <table class="table table-striped table-bordered">
      <thead> 
        <th>Bias Adjustment Name</th>
        <th>Reference</th>
        <th>Package</th> 
      </thead> 
      <tbody>
     % for a,b in my_dict.iteritems():
        <tr>
        <td>${b['institute_id']+'-'+b['bc_method_id']}</td>
        <td>${b['reference']}</td>
        <td>${b['package']}</td>
        </tr>
     % endfor
      </tbody
    </table>
   </div> 
    </body>
    </html>
    '''
   
   
   my_mako_template = Template(my_template)
   
   result = my_mako_template.render(my_dict = a_dict, my_timestamp=timestamp)
    
   return result




def make_html_table(a_dict,timestamp):
    my_template =  '''
    <!DOCTYPE html>
       
<html>

</head>    
    
    
    <body>
    
    <h1> CORDEX RCM list</h1>
    <p> Information automatically generated based on ESGF CORDEX registration sheet. </p>
    <p> -- Timestamp: ${my_timestamp} </p>
    <p> To register CORDEX simulations please contact cordex-registration /at/ cordex.org  </p>
   
    
    <table border="1">
      <tr>
        <th>Model Name</th>
        <th>Institute</th>
        <th>Institution Name</th>
        <th>Terms of Use</th>
        
      % for a,b in my_dict.iteritems():
         % if b[6] == "unknown":
           <tr bgcolor=#FFC1C1>
         % elif b[6] == "non-commercial":
           <tr bgcolor=#FFCC99>
         % else:
           <tr bgcolor=#CCFFCC>
         % endif

            <td>${b[2]}</td>
            <td>${b[1]}</td>
            <td>${b[4]}</td>
            <td>${b[6]}</td>
          </tr>
      % endfor
      </tr>
    </table>
    
    
    </body>
    </html>
    '''
    
    my_mako_template = Template(my_template)
    
    result = my_mako_template.render(my_dict = a_dict,my_timestamp = timestamp)
    
    return result
    
def make_domain_table(a_dict,timestamp): 
    my_template = '''
    <!DOCTYPE html>
    <html>
    <head>
<!-- Javascript goes in the document HEAD -->
<script type="text/javascript">
function altRows(id){
        if(document.getElementsByTagName){  
                
                var table = document.getElementById(id);  
                var rows = table.getElementsByTagName("tr"); 
                 
                for(i = 0; i < rows.length; i++){          
                        if(i % 2 == 0){
                                rows[i].className = "evenrowcolor";
                        }else{
                                rows[i].className = "oddrowcolor";
                        }      
                }
        }
}
window.onload=function(){
        altRows('alternatecolor');
}
</script>

<!-- CSS goes in the document HEAD or added to your external stylesheet -->
<style type="text/css">
table.altrowstable {
        font-family: verdana,arial,sans-serif;
        font-size:11px;
        color:#333333;
        border-width: 1px;
        border-color: #a9c6c9;
        border-collapse: collapse;
}
table.altrowstable th {
        border-width: 1px;
        padding: 8px;
        border-style: solid;
        border-color: #a9c6c9;
}
table.altrowstable td {
        border-width: 1px;
        padding: 8px;
        border-style: solid;
        border-color: #a9c6c9;
}
.oddrowcolor{
        background-color:#d4e3e5;
}
.evenrowcolor{
        background-color:#c3dde0;
}
</style>

<!-- Table goes in the document BODY -->
</head>

    
    <body>
    
    <h1> CORDEX - ESGF data availability overview </h1>
    <h2> - sorted by domains - </h2> 

    <p> Information retrieved from ESGF index nodes at ${my_timestamp} </p>
    
    <table class="altrowstable" id="alternatecolor">
      <tr>
        <th> Domain </th>
        <th> Model </th>
        <th> Driving Model </th>
      % for a,b in sorted(my_dict.iteritems()):
         <tr>
           <td> ----------------------------------------- </td>
           <td> ----------------------------------------- </td>
           <td> -------------------------------------------------- </td>
         </tr>
      %    for c in b:
          <tr>
            <td>${c[0]}</td>
            <td>${c[1]}</td>
            <td>${c[2]}</td>
          </tr>
      % endfor 
      % endfor
        <tr>
      </tr>
    </table>
    
    
    </body>
    </html>
    '''
    
    my_mako_template = Template(my_template)
    
    result = my_mako_template.render(my_dict = a_dict, my_timestamp = timestamp)
    
    return result
      
    


