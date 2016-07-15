#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jul 14, 2016

@author: Joerg Weingrill <jweingrill@aip.de>
'''

class PLCVariable(object):
    def __init__(self, PLC, variablename, variabletype):
        from adshli.hli import ads_var_single

        self.var_name = variablename
        self.var_type = variabletype
        self.variable = ads_var_single(PLC.connection, self.var_name, self.var_type)
    
    def read(self):
        import adshli.protocol as adsprotocol 
        
        try:
            variable_content=self.variable.read()
        except adsprotocol.struct.error:
            print 'bad char (%s) in struct format' % self.var_type
            return
        return variable_content
    
    def write(self, value):
        self.variable.write(value)
        

class PLC(object):
    plc_ams_id="5.34.116.124.1.1"   #"10.23.23.57.1.1"
    plc_ams_port=851
    plc_ip_adr='141.33.59.208'  #"127.0.0.1"
    plc_ip_port=48898
    pc_ams_id="141.33.59.7.1.1"
    pc_ams_port=801
    timeout=5
    def __init__(self):
        """
        Builds up the connection to the device
        """
        from adshli.connection import ads_connection
        
        self.connection=ads_connection(self.plc_ams_id, self.plc_ams_port, self.pc_ams_id, self.pc_ams_port)
        self.connection.open(self.plc_ip_adr, self.plc_ip_port, self.timeout)

    def __str__(self):
        """
        returns the state of the device and the connection
        """
        from adshli.hli import ads_device
        
        device=ads_device(self.connection)
        
        params = {'device_name':    device.device_name,
                  'ads_state':      device.ads_state,
                  'device_state':   device.device_state,
                  'plc_ams_id':     self.plc_ams_id,
                  'plc_ams_port':   self.plc_ams_port,
                  'plc_ip_adr':     self.plc_ip_adr,
                  'plc_ip_port':    self.plc_ip_port,
                  'pc_ams_id':      self.pc_ams_id,
                  'pc_ams_port':    self.pc_ams_port
                  
                  }
        result = 'Device name:    %(device_name)s\n' \
                 'ADS state:      %(ads_state)s\n' \
                 'Device state:   %(device_state)s\n' \
                 'PLC AMS ID:     %(plc_ams_id)s:%(plc_ams_port)d\n' \
                 'PLC IP address: %(plc_ip_adr)s:%(plc_ip_port)d\n' \
                 'PC AMS ID:      %(pc_ams_id)s:%(pc_ams_port)d\n' % params
        return result
    
    def close(self):
        """
        closes the connection gracefully
        """
        self.connection.close()
    
    def __del__(self):
        self.connection.close()

    def __getattribute__(self, name):
        var_name = name[1:]
        var_type = name[0]
        return self.read_variable(var_name, var_type)

    def __setattr__(self, name, value):
        var_name = name[1:]
        var_type = name[0]
        return self.write_variable(var_name, var_type, value)


    def read_variable(self, var_name, var_type='?', verbose=False):
        from adshli.hli import ads_var_single
        import adshli.protocol as adsprotocol 
        
        variable=ads_var_single(self.connection, var_name, var_type)
        try:
            variable_content=variable.read()
        except adsprotocol.struct.error:
            print 'bad char (%s) in struct format' % var_type
            return
        
        if verbose: 
            print 'Variable content: ', variable_content,var_type
#        variable.write(variable_content)
        return variable_content

    def write_variable(self, var_name, var_type, value):
        from adshli.hli import ads_var_single

        variable=ads_var_single(self.connection, var_name, var_type)
        variable.write(value)

if __name__ == '__main__':
    import datetime
    import time
    '''
    a new Route has to be created on the PLC with remote route "None" for CX-22747C
    '''
    
    weatherstation = PLC()
    
    print weatherstation
    
    for _ in range(54000):
        temperature_raw = weatherstation.read_variable('GVL.temperature_raw', var_type='h')
        humidity_raw = weatherstation.read_variable('GVL.humidity_raw', var_type='h')
        temperature = weatherstation.read_variable('GVL.temperature', var_type='f')
        humidity = weatherstation.read_variable('GVL.humidity', var_type='f')
        t = datetime.datetime.now()
        print '%s %.2f %.2f %d %d' % (t,temperature,humidity, temperature_raw, humidity_raw)
        s = '%s %.2f %.2f %d %d\n' % (t,temperature,humidity, temperature_raw, humidity_raw)
        with open('data.txt', 'a+t') as f:
            f.write(s)
        time.sleep(1)
    
    weatherstation.close()    
    
    