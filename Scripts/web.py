# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 16:51:27 2014

@author: stephan
"""

from mako.template import Template


def make_html_table(a_dict):
    my_template =  '''
    <!DOCTYPE html>
    <html>
    <body>
    
    <h1> CORDEX RCM table  </h1>
    
    <table border="1">
      <tr>
        <th>model_id</th>
        <th>RCM name</th>
        <th>confirmation status</th>
      % for a,b in my_dict.iteritems():
          </tr>
            <td>${b[0]} </td>
            <td>${b[1]}</td>
            <td>${b[2]}</td>
          </tr>
      % endfor
        <tr>
      </tr>
    </table>
    
    
    </body>
    </html>
    '''
    
    my_mako_template = Template(my_template)
    
    result = my_mako_template.render(my_dict = a_dict)
    
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
    
    <h1> CORDEX domain avalability table </h1>

    <p> Dynamically retrieved from ESGF at ${my_timestamp} </p>
    
    <table class="altrowstable" id="alternatecolor">
      <tr>
        <th> Domain </th>
        <th> Model </th>
        <th> Driving Model </th>
      % for a,b in my_dict.iteritems():
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
      
    


