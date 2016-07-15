#!/usr/bin/python
# -*- coding: utf-8 -*-
from adshli.connection import ads_connection
import adshli.protocol as adsprotocol 
from adshli.hli import ads_device, ads_var_single, idx_grp, ads_var_group
import time
'''
a new Route has to be created on the PLC with remote route "None" for CX-22747C
'''
plc_ams_id="5.34.116.124.1.1"   #"10.23.23.57.1.1"
plc_ams_port=851
plc_ip_adr='141.33.59.208'  #"127.0.0.1"
plc_ip_port=48898
pc_ams_id="141.33.59.7.1.1"
pc_ams_port=801
timeout=5
#var_name='Main.b_DomeOpen'
var_name='GVL.temperature'
var_type='f'
"""
var_type='?' ... BOOL
var_type='b' ... signed BYTE
'c' ... CHAR ?
'h' ... INT
'p'
's'... STRING
'x' ... ?
'f' ... real
'i' ...
'l' ...
1...0


"""
#var_fail_n=' Main.I_b_SafeState'
#var_fail_t='?'

var_name1='GVL.temperature'
var_type1='f'

var_name_array='GVL.fb_maps.Height'
var_type_array='625f'
var_shape_array=(25,25)

def low_level():
    # *** Reading and writing variables using the low level interface
    print 'Accessing the PLC using the low level ADS interface'
    connection=ads_connection(plc_ams_id, plc_ams_port, pc_ams_id, pc_ams_port)
    connection.open(plc_ip_adr, plc_ip_port, timeout)
    #Read the device name
    cmd=adsprotocol.ads_cmd_read_dev_info()
    dev_name= connection.execute_cmd(cmd)['dev_name']
    print 'Device name: ', dev_name
    #Read the device and ads state
    cmd=adsprotocol.ads_cmd_read_state()
    retval=connection.execute_cmd(cmd)
    ads_state=retval['ads_state']
    dev_state=retval['dev_state']
    print 'ADS state: ', ads_state
    print 'Device state: ', dev_state
    #Get a handle for a variable
    cmd=adsprotocol.ads_cmd_read_write(idx_grp['SYM_HNDBYNAME'], 0x0, 'L',  var_name)
    handle= connection.execute_cmd(cmd)['data'][0]
    #Read the variable
    cmd=adsprotocol.ads_cmd_read(idx_grp['SYM_VALBYHND'], handle, var_type)
    var_content=connection.execute_cmd(cmd)['data']
    print 'Variable contents: ',  var_content
    #Write back the variable
    cmd=adsprotocol.ads_cmd_write(idx_grp['SYM_VALBYHND'], handle, var_type, var_content)
    connection.execute_cmd(cmd)
    connection.close()

def high_level(var_type='?', verbose=False):
    # ***************************************************
    # *** Do the same using the high level interface
    # Open the connection
    if verbose: print '\n\nNow accessing the PLC using the high level ADS interface'
    
    connection=ads_connection(plc_ams_id, plc_ams_port, pc_ams_id, pc_ams_port)
    connection.open(plc_ip_adr, plc_ip_port, timeout)
    #Instanciate device: this immediately reads the device information
    device=ads_device(connection)
    
    if verbose: 
        print 'Device name: ', device.device_name
        print 'ADS state: ', device.ads_state
        print 'Device state: ', device.device_state
    #Accessing the variable: First instanciate, then read and write back
    variable=ads_var_single(connection, var_name, var_type)
    try:
        variable_content=variable.read()
    except adsprotocol.struct.error:
        print 'bad char (%s) in struct format' % var_type
        return
    
    print 'Variable content: ', variable_content,var_type
    variable.write(variable_content)
    connection.close()

def read_array():
    var_name_array='GVL.fb_maps.Height'
    var_type_array='625f'
    
    connection=ads_connection(plc_ams_id, plc_ams_port, pc_ams_id, pc_ams_port)
    connection.open(plc_ip_adr, plc_ip_port, timeout)
    
    # Now read an array 
    array_var=ads_var_single(connection, var_name_array, var_type_array, shape=var_shape_array)
    start_time=time.time()
    variable_content=array_var.read()
    print 'Time required for reading: ',  time.time()-start_time
    print 'Variable content: ', variable_content
    start_time=time.time()
    array_var.write(variable_content)
    print 'Time required for writing: ',  time.time()-start_time
    connection.close()

def test_group():
    connection=ads_connection(plc_ams_id, plc_ams_port, pc_ams_id, pc_ams_port)
    connection.open(plc_ip_adr, plc_ip_port, timeout)

    # Test variable group
    print 'Now accessing the PLC using a variable group'
    var_grp=ads_var_group()
    # Setting all variables
    var_bool=var_grp.add_variable(var_name, var_type)
    var_arr=var_grp.add_variable(var_name_array, var_type_array, shape=var_shape_array)
    
    #Connecting
    var_grp.connect(connection)
    #Read everything
    start_time=time.time()
    var_grp.read()
    print 'Time required for reading: ',  time.time()-start_time
    print 'Variable content: ', var_bool.value
    print 'Variable content: ', var_arr.value
    
    start_time=time.time()
    var_grp.write()
    print 'Time required for writing: ',  time.time()-start_time

    connection.close()

def main():
    #low_level()
    #return
    for vt in 'bchpsxfdilq':
        high_level(vt)
    return
    # *** Reading and writing variables using the low level interface
    print 'Accessing the PLC using the low level ADS interface'
    connection=ads_connection(plc_ams_id, plc_ams_port, pc_ams_id, pc_ams_port)
    connection.open(plc_ip_adr, plc_ip_port, timeout)
    #Read the device name
    cmd=adsprotocol.ads_cmd_read_dev_info()
    dev_name= connection.execute_cmd(cmd)['dev_name']
    print 'Device name: ', dev_name
    #Read the device and ads state
    cmd=adsprotocol.ads_cmd_read_state()
    retval=connection.execute_cmd(cmd)
    ads_state=retval['ads_state']
    dev_state=retval['dev_state']
    print 'ADS state: ', ads_state
    print 'Device state: ', dev_state
    #Get a handle for a variable
    cmd=adsprotocol.ads_cmd_read_write(idx_grp['SYM_HNDBYNAME'], 0x0, 'L',  var_name)
    handle= connection.execute_cmd(cmd)['data'][0]
    #Read the variable
    cmd=adsprotocol.ads_cmd_read(idx_grp['SYM_VALBYHND'], handle, var_type)
    var_content=connection.execute_cmd(cmd)['data']
    print 'Variable contents: ',  var_content
    #Write back the variable
    cmd=adsprotocol.ads_cmd_write(idx_grp['SYM_VALBYHND'], handle, var_type, var_content)
    connection.execute_cmd(cmd)
    connection.close()
    
    # ***************************************************
    # *** Do the same using the high level interface
    # Open the connection
    print '\n\nNow accessing the PLC using the high level ADS interface'
    connection=ads_connection(plc_ams_id, plc_ams_port, pc_ams_id, pc_ams_port)
    connection.open(plc_ip_adr, plc_ip_port, timeout)
    #Instanciate device: this immediately reads the device information
    device=ads_device(connection)
    print 'Device name: ', device.device_name
    print 'ADS state: ', device.ads_state
    print 'Device state: ', device.device_state
    #Accessing the variable: First instanciate, then read and write back
    variable=ads_var_single(connection, var_name, var_type)
    variable_content=variable.read()
    print 'Variable content: ', variable_content
    variable.write(variable_content)
    # Now read an array 
    array_var=ads_var_single(connection, var_name_array, var_type_array, shape=var_shape_array)
    start_time=time.time()
    variable_content=array_var.read()
    print 'Time required for reading: ',  time.time()-start_time
    print 'Variable content: ', variable_content
    start_time=time.time()
    array_var.write(variable_content)
    print 'Time required for writing: ',  time.time()-start_time
    # Test variable group
    print 'Now accessing the PLC using a variable group'
    var_grp=ads_var_group()
    # Setting all variables
    var_bool=var_grp.add_variable(var_name, var_type)
    var_arr=var_grp.add_variable(var_name_array, var_type_array, shape=var_shape_array)
    #Connecting
    var_grp.connect(connection)
    #Read everithing
    start_time=time.time()
    var_grp.read()
    print 'Time required for reading: ',  time.time()-start_time
    print 'Variable content: ', var_bool.value
    print 'Variable content: ', var_arr.value
    start_time=time.time()
    var_grp.write()
    print 'Time required for writing: ',  time.time()-start_time
    
    
    

if __name__ == '__main__':
    main()


