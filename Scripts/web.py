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
    


