##########################################################################################################################################################################################
########################################     Pipeline Lateral Buckling POSTPROCESSOR    ###############################################################################
########################################     Subject:    Abaqus FEA Postprocessing   ###############################################################################
########################################     Author :    Engr.Jesurobo Collins       #####################################################################################    #################################################################################################
########################################     Project:    Personal project            ##############################################################################################
########################################     Tools used: Python,Abaqus,xlsxriter     ##############################################################################################
########################################     Email:      collins4engr@yahoo.com      ##############################################################################################
#########################################################################################################################################################################################
import sys,os
from abaqus import*
from abaqusConstants import*
from math import*
import xlsxwriter
import glob
  
# CHANGE TO CURRENT WORKING DIRECTORY
os.chdir('C:/temp/LateralBuckling_Analysis')

###CREATE EXCEL WORKBOOK, SHEETS AND ITS PROPERTIES####
execFile = 'Results.xlsx'
workbook = xlsxwriter.Workbook(execFile)
workbook.set_properties({
    'title':    'This is Abaqus postprocessing',
    'subject':  'Pipeline Lateral Buckling Analysis',   
    'author':   'Collins Jesurobo',
    'company':  'Personal Project',
    'comments': 'Created with Python and XlsxWriter'})

# Create a format to use in the merged range.
merge_format = workbook.add_format({
    'bold': 1,
    'border': 1,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': 'yellow'})

SHEET1 = workbook.add_worksheet('Summary_sheet')
SHEET1.center_horizontally()
SHEET1.fit_to_pages(1, 1)
SHEET1.set_column(0,4,24)
SHEET1.set_column(5,7,30)
SHEET1.merge_range('A1:G1', 'SUMMARY - MAXIMUM AND MINIMUM VALUES WITH CORRESPONDING WORST LOADCASE,WORST LOAD STEP AND NODE WHERE IT OCCURS',merge_format)


SHEET2 = workbook.add_worksheet('All_steps')
SHEET2.center_horizontally()
SHEET2.fit_to_pages(1, 1)
SHEET2.set_column(0,1,20)
SHEET2.set_column(3,4,22)
SHEET2.set_column(5,6,13)
SHEET2.set_column(7,9,20)
SHEET2.merge_range('A1:J1', 'ALL STEP RESULTS - RESULTS FOR ALL LOAD STEPS CORRESPONDING EACH PIPELINE NODES AND ELEMENTS ',merge_format)

SHEET3 = workbook.add_worksheet('operating')
SHEET3.center_horizontally()
SHEET3.fit_to_pages(1, 1)
SHEET3.set_column(0,1,20)
SHEET3.set_column(3,4,22)
SHEET3.set_column(5,6,13)
SHEET3.set_column(7,9,20)
SHEET3.merge_range('A1:J1', 'OPERATING CASE - RESULTS FOR ALL LOAD STEPS CORRESPONDING EACH PIPELINE NODES AND ELEMENTS ',merge_format)

SHEET4 = workbook.add_worksheet('hydrotest')
SHEET4.center_horizontally()
SHEET4.fit_to_pages(1, 1)
SHEET4.set_column(0,1,20)
SHEET4.set_column(3,4,22)
SHEET4.set_column(5,6,13)
SHEET4.set_column(7,9,20)
SHEET4.merge_range('A1:J1', 'HYDROTEST CASE - RESULTS FOR ALL LOAD STEPS CORRESPONDING EACH PIPELINE NODES AND ELEMENTS ',merge_format)

# defines the worksheet formatting (font name, size, cell colour etc.)
format_title = workbook.add_format()
format_title.set_bold('bold')
format_title.set_align('center')
format_title.set_align('vcenter')
format_title.set_bg_color('#F2F2F2')
format_title.set_font_size(10)
format_title.set_font_name('Arial')
format_table_headers = workbook.add_format()
format_table_headers.set_align('center')
format_table_headers.set_align('vcenter')
format_table_headers.set_text_wrap('text_wrap')
format_table_headers.set_bg_color('#F2F2F2')
format_table_headers.set_border()
format_table_headers.set_font_size(10)
format_table_headers.set_font_name('Arial')

###WRITING THE TITLES TO SHEET1,SHEET2###
SHEET1.write_row('B2',['WorstNode@U3','WorstLoadStep@U3','U3-LateralDisplacement(m)','ESF1-Axial Force(kN)','SM2-Bending Moment(kNm)',
                       'EE11+PE11 - Strain(%)',],format_title)
SHEET1.write('A3', 'Max value',format_title)
SHEET1.write('A4', 'Min value',format_title)
SHEET1.write('A5', 'Absolute Max value',format_title)

SHEET2.write_row('A2',['Loadcase','LoadStep','Node','KP (m)','Lateral displacement (m)','',
                       'Element','Axial Force (KN)','Section moment (KNm)','Strain (%)'],format_title)
SHEET3.write_row('A2',['Loadcase','LoadStep','Node','KP (m)','Lateral displacement (m)','',
                       'Element','Axial Force (KN)','Section moment (KNm)','Strain (%)'],format_title)
SHEET4.write_row('A2',['Loadcase','LoadStep','Node','KP (m)','Lateral displacement (m)','',
                       'Element','Axial Force (KN)','Section moment (KNm)','Strain (%)'],format_title)

###LOOP THROUGH THE ODB AND EXTRACT RESULTS SPECIFIED NODESETS FOR ALL STEPS###
def output1():
        row=1
        col=0
        for i in glob.glob('*.odb'):     # loop  to access all odbs in the folder
                odb = session.openOdb(i) # open each odb
                step = odb.steps.keys()  # probe the content of the steps object in odb, steps object is a dictionary, so extract the step names with keys()
                instances = odb.rootAssembly.instances.keys() # probe instances
                nodeset = odb.rootAssembly.instances[instances[0]].nodeSets.keys()           # probe nodeset 
                section = odb.rootAssembly.instances[instances[0]].nodeSets['NODES']         # extract section for pipeline nodeset
                ###DEFINE RESULT OUTPUT####
                for k in range(len(step)):
                        U = odb.steps[step[k]].frames[-1].fieldOutputs['U'].getSubset(region=section).values        # results for all displacements U
                        coor = odb.steps[step[k]].frames[-1].fieldOutputs['COORD'].getSubset(region=section).values # results for x coordinate
                        for disp,coor in zip(U,coor):
                                U3 = disp.data[2]                                             # extract U3 (vertical) displacements from all the odbs and loadcases
                                n1 = disp.nodeLabel                                           # extract node numbers
                                coor1 = coor.data[0]                                          # extract kp distance
                                ### WRITE OUT MAIN RESULT OUTPUT####
                                SHEET2.write(row+1,col,i.split('.')[0],format_table_headers)  # write all loadcases to sheet2
                                SHEET2.write(row+1,col+1,step[k],format_table_headers)        # write all steps in odb to sheet2
                                SHEET2.write(row+1,col+2,n1,format_table_headers)             # write all nodes in the pipeline to sheet2      
                                SHEET2.write(row+1,col+3,coor1,format_table_headers)          # write distance KP to sheet2
                                SHEET2.write(row+1,col+4,U3,format_table_headers)             # write lateral displacements to sheet2
                                row+=1                               
output1()

###LOOP THROUGH THE ODB AND EXTRACT RESULTS FOR SPECIFIED ELEMENTSETS FOR ALL STEPS###
def output2():
        row=1
        col=0
        for i in glob.glob('*.odb'):     
                odb = session.openOdb(i) 
                step = odb.steps.keys()  
                instances = odb.rootAssembly.instances.keys() 
                elementset = odb.rootAssembly.instances[instances[0]].elementSets.keys()  
                section = odb.rootAssembly.instances[instances[0]].elementSets['ELEM']    
                ###DEFINE RESULT OUTPUT####
                for k in range(len(step)):
                        ESF = odb.steps[step[k]].frames[-1].fieldOutputs['ESF1'].getSubset(region=section).values # results for Effective axial force
                        SM = odb.steps[step[k]].frames[-1].fieldOutputs['SM'].getSubset(region=section).values    # results for section moment
                        EE = odb.steps[step[k]].frames[-1].fieldOutputs['EE'].getSubset(region=section).values    # results for elastic strain
                        PE = odb.steps[step[k]].frames[-1].fieldOutputs['PE'].getSubset(region=section).values    # results for plastic strain
                        for force,moment,strain1,strain2 in zip(ESF,SM,EE,PE):
                                ESF1 = force.data                                               # Effective axial force
                                SM2 = moment.data[1]                                            # Section moment in lateral direction
                                EE11 = strain1.data[0]                                          # Elastic strain in axial direction
                                PE11 = strain2.data[0]                                          # Plastic strain in axial direction
                                e1 = force.elementLabel                                         # Element label
                                ### WRITE OUT MAIN RESULT OUTPUT####
                                SHEET2.write(row+1,col+6,e1,format_table_headers)               # write all element in the pipeline to sheet2     
                                SHEET2.write(row+1,col+7,ESF1/1000,format_table_headers)        # write Effective axial force,KN to sheet2
                                SHEET2.write(row+1,col+8,SM2/1000,format_table_headers)         # write Section moment,KNm to sheet2
                                SHEET2.write(row+1,col+9,(EE11+PE11)*100,format_table_headers)  # write Strain (%) to sheet2
                                row+=1
output2()

###LOOP THROUGH THE ODB AND EXTRACT RESULTS FOR SPECIFIED NODESETS FOR OPERATING CONDITION###
def output3():
        row=1
        col=0
        for i in glob.glob('*.odb'):     
                odb = session.openOdb(i)
                step = odb.steps.keys()  
                instances = odb.rootAssembly.instances.keys() 
                nodeset = odb.rootAssembly.instances[instances[0]].nodeSets.keys()       
                section = odb.rootAssembly.instances[instances[0]].nodeSets['NODES'] 
                ###DEFINE RESULT OUTPUT FOR OPERATING AND HYDROTEST STEPS####
                U_op = odb.steps[step[-1]].frames[-1].fieldOutputs['U'].getSubset(region=section).values   
                U_hydro = odb.steps[step[5]].frames[-1].fieldOutputs['U'].getSubset(region=section).values   
                coor_op = odb.steps[step[-1]].frames[-1].fieldOutputs['COORD'].getSubset(region=section).values 
                coor_hydro = odb.steps[step[5]].frames[-1].fieldOutputs['COORD'].getSubset(region=section).values 
                for disp1,disp2,coor1,coor2 in zip(U_op,U_hydro,coor_op,coor_hydro):
                        U3_op = disp1.data[2]               # extract U3 (lateral) displacements 
                        U3_hydro = disp2.data[2]            # extract U3 (lateral) displacements 
                        n1 = disp1.nodeLabel                # extract node numbers
                        coor1_op = coor1.data[0]            # extract distance
                        coor2_hydro = coor2.data[0]         # extract distance
                        ### WRITE OUT MAIN RESULT OUTPUT####
                        SHEET3.write(row+1,col,i.split('.')[0],format_table_headers)        # write loadcases to sheet3 (operating step)
                        SHEET3.write(row+1,col+1,step[-1],format_table_headers)             # write steps in odb to sheet3 (operating step)
                        SHEET4.write(row+1,col,i.split('.')[0],format_table_headers)        # write loadcases to sheet4 (hydrotest step)
                        SHEET4.write(row+1,col+1,step[5],format_table_headers)              # write steps in odb to sheet4 (hydrotest step)
                        SHEET3.write(row+1,col+2,n1,format_table_headers)                   # write all nodes in the pipeline to sheet3
                        SHEET4.write(row+1,col+2,n1,format_table_headers)                   # write all nodes in the pipeline to sheet4
                        SHEET3.write(row+1,col+3,round(coor1_op,0),format_table_headers)    # write distance to sheet3
                        SHEET4.write(row+1,col+3,round(coor2_hydro,0),format_table_headers) # write distance to sheet4
                        SHEET3.write(row+1,col+4,U3_op,format_table_headers)                # write lateral displacements to sheet3
                        SHEET4.write(row+1,col+4,U3_hydro,format_table_headers)             # write lateral displacements to sheet4
                        row+=1
output3()
###LOOP THROUGH THE ODB AND EXTRACT RESULTS FOR SPECIFIED ELEMENTSETS FOR OPERATING CONDITION###
def output4():
        row=1
        col=0
        for i in glob.glob('*.odb'):     
                odb = session.openOdb(i) 
                step = odb.steps.keys()  
                instances = odb.rootAssembly.instances.keys() 
                elementset = odb.rootAssembly.instances[instances[0]].elementSets.keys()  
                section = odb.rootAssembly.instances[instances[0]].elementSets['ELEM']   
                ###DEFINE RESULT OUTPUT for OPERATING AND HYDROTEST RESPECTIVELY####
                ESF_op = odb.steps[step[-1]].frames[-1].fieldOutputs['ESF1'].getSubset(region=section).values    
                ESF_hydro = odb.steps[step[5]].frames[-1].fieldOutputs['ESF1'].getSubset(region=section).values 
                SM_op = odb.steps[step[-1]].frames[-1].fieldOutputs['SM'].getSubset(region=section).values      
                SM_hydro = odb.steps[step[5]].frames[-1].fieldOutputs['SM'].getSubset(region=section).values    
                EE_op = odb.steps[step[-1]].frames[-1].fieldOutputs['EE'].getSubset(region=section).values      
                EE_hydro = odb.steps[step[5]].frames[-1].fieldOutputs['EE'].getSubset(region=section).values
                PE_op = odb.steps[step[-1]].frames[-1].fieldOutputs['PE'].getSubset(region=section).values
                PE_hydro = odb.steps[step[5]].frames[-1].fieldOutputs['PE'].getSubset(region=section).values
                for force1,force2,moment1,moment2,strain1,strain2,strain3,strain4 in zip(ESF_op,ESF_hydro,SM_op,SM_hydro,EE_op,EE_hydro,PE_op,PE_hydro):
                        ESF1_op = force1.data           # Effective axial force for operating,N
                        ESF1_hydro = force2.data        # Effective axial force for hydrotest,N
                        SM2_op = moment1.data[1]        # Section moment for operating , Nm
                        SM2_hydro = moment2.data[1]     # Section moment for hydrotest, Nm
                        EE11_op = strain1.data[0]       # Elastic strain for operating
                        EE11_hydro = strain2.data[0]    # Elastic strain for hydrotest
                        PE11_op = strain3.data[0]       # Plastic strain for operating
                        PE11_hydro = strain4.data[0]    # Plastic strain for hydrotest
                        e1 = force1.elementLabel        # Element label
                        ### WRITE OUT MAIN RESULT OUTPUT####
                        SHEET3.write(row+1,col+6,e1,format_table_headers)                         # write all elements in the pipeline for operating in sheet3
                        SHEET4.write(row+1,col+6,e1,format_table_headers)                         # write all elements in the pipeline for hydrotest in sheet4
                        SHEET3.write(row+1,col+7,ESF1_op/1000,format_table_headers)               # Effective axial force,KN
                        SHEET3.write(row+1,col+8,SM2_op/1000,format_table_headers)                # Section moment ,KNm                               
                        SHEET4.write(row+1,col+7,ESF1_hydro/1000,format_table_headers)            # Effective axial force,KN
                        SHEET4.write(row+1,col+8,SM2_hydro/1000,format_table_headers)             # Section moment,KNm
                        SHEET3.write(row+1,col+9,(EE11_op+PE11_op)*100,format_table_headers)      # Strain (%) for operating 
                        SHEET4.write(row+1,col+9,(EE11_hydro+PE11_hydro)*100,format_table_headers)# Strain (%) for hydrotest
                        row+=1
output4()
### WRITE THE MAXIMUM AND MINIMUM, AND ABSOLUTE MAXIMUM VALUES AND WRITE THM INTO SUMMARY SHEET(SHEET1) 
def output5():
        SHEET1.write('D3', '=ROUND(max(All_steps!E3:E200000),2)',format_table_headers)    # maximum lateral displacement
        SHEET1.write('E3', '=ROUND(max(All_steps!H3:H200000),2)',format_table_headers)    # max effective axial force
        SHEET1.write('F3', '=ROUND(max(All_steps!I3:I200000),2)',format_table_headers)    # max bending moment
        SHEET1.write('G3', '=ROUND(max(All_steps!J3:J200000),3)',format_table_headers)    # max strain
        
        SHEET1.write('D4', '=ROUND(min(All_steps!E3:E200000),2)',format_table_headers)    # minimum lateral displacement
        SHEET1.write('E4', '=ROUND(min(All_steps!H3:H200000),2)',format_table_headers)    # min effective axial force
        SHEET1.write('F4', '=ROUND(min(All_steps!I3:I200000),2)',format_table_headers)    # min bending moment
        SHEET1.write('G4', '=ROUND(min(All_steps!J3:J200000),3)',format_table_headers)    # min bending moment
        
        SHEET1.write('D5','=IF(ABS(D3)>ABS(D4),ABS(D3),ABS(D4))',format_table_headers)    # absolute maximum lateral disp
        SHEET1.write('E5','=IF(ABS(E3)>ABS(E4),ABS(E3),ABS(E4))',format_table_headers)    # absolute maximum effective axial force
        SHEET1.write('F5','=IF(ABS(F3)>ABS(F4),ABS(F3),ABS(F4))',format_table_headers)    # absolute maximum bending moment
        SHEET1.write('G5','=IF(ABS(G3)>ABS(G4),ABS(G3),ABS(G4))',format_table_headers)    # absolute maximum strain


        ### WORST NODE AND LOADSTEP CORRESPONDING TO MAXIMUM AND MINIMUM LATERAL DISPLACEMENT VALUES
        SHEET1.write('B3','=INDEX(All_steps!C3:C200000,MATCH(MAX(All_steps!E3:E200000),All_steps!E3:E200000,0))',format_table_headers)
        SHEET1.write('C3','=INDEX(All_steps!B3:B200000,MATCH(MAX(All_steps!E3:E200000),All_steps!E3:E200000,0))',format_table_headers)
        SHEET1.write('B4','=INDEX(All_steps!C3:C200000,MATCH(MIN(All_steps!E3:E200000),All_steps!E3:E200000,0))',format_table_headers)
        SHEET1.write('C4','=INDEX(All_steps!B3:B200000,MATCH(MIN(All_steps!E3:E200000),All_steps!E3:E200000,0))',format_table_headers)


# PLOT CHARTS
chart1 = workbook.add_chart({'type': 'line'})
chart2 = workbook.add_chart({'type': 'line'})
chart3 = workbook.add_chart({'type': 'line'})

# plot lateral dsplacement with kp'''
chart1.set_x_axis({'line':{'none':True}})
chart1.add_series({
        'name': 'Operating',
        'categories':'=operating!$D$450:$D$2500',                   # Distance ,m
        'values': '=operating!$E$450:$E$2500',                      # Lateral displacement values(operating case),m
        'line':{'color':'blue'}})
chart1.add_series({
        'name': 'Hydrotest',
        'categories':'=hydrotest!$D$450:$D$2500',                   # Distance in x-axis
        'values': '=hydrotest!$E$450:$E$2500',                      # Lateral displacement values(hydrotest case),m
        'line':{'color':'green'}})  
chart1.set_title({'name': 'Lateral Displacement Plot ',})
chart1.set_x_axis(
        {'name': 'Distance (m)'})
chart1.set_y_axis({'name': 'Lateral displacements (m)',})
chart1.set_style(9)
chart1.set_size({'x_scale': 1.5, 'y_scale': 1.0})

# plot Bending moment with kp'''
chart2.add_series({
        'name': 'Operating',
        'categories':'=operating!$D$450:$D$2500',                   # Distance,m
        'values': '=operating!$I$450:$I$2500',
        'line':{'color':'blue'}})                                # Bending moment values,KNm (operating)
chart2.add_series({
        'name': 'Operating',
        'categories':'=hydrotest!$D$450:$D$2500',                   # Distance,m
        'values': '=hydrotest!$I$450:$I$2500',
        'line':{'color':'green'}})                               # Bending moment values,KNm (hydrotest)
chart2.set_x_axis({'line':{'none':True}})
chart2.set_x_axis({'name': 'Distance (m)'})
chart2.set_y_axis({'name': 'Bending moment (KNm)',
                   'major_unit': 100})
chart2.set_title({'name': 'Bending Moment Plot'})
chart2.set_style(9)
chart2.set_size({'x_scale': 1.5, 'y_scale': 1.0})

# plot Effective Axial Force with kp'''
chart3.add_series({
        'name': 'Operating',
        'categories':'=operating!$D$3:$D$2949',                     # Distance, m            
        'values': '=operating!$H$3:$H$2949',                        # Effective axial force values, KN (operating)
        'line':{'color':'blue'}})
chart3.add_series({
        'name': 'Hydrotest',
        'categories':'=hydrotest!$D$3:$D$2949',                     # Distance ,m          
        'values': '=hydrotest!$H$3:$H$2949',                        # Effective axial force values, KN (hydrotest)
        'line':{'color':'green'}})    
chart3.set_x_axis({'line':{'none':True}})
chart3.set_x_axis({'name': 'Distance (m)'})
chart3.set_y_axis({'name': 'Effective Axial Force(KN)',
                   'major_unit': 200})
chart3.set_title({'name': 'Effective Axial Force Plot'})
chart3.set_style(9)
chart3.set_size({'x_scale': 1.5, 'y_scale': 1.0})

# Insert the chart into the worksheet.
SHEET1.insert_chart('B8', chart1)
SHEET1.insert_chart('B23', chart2)
SHEET1.insert_chart('B38', chart3)
output5()
# closes the workbook once all data is written
workbook.close()
# opens the resultant spreadsheet
os.startfile(execFile)
# Lateral Buckling study completed























