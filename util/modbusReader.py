from pymodbus.client import ModbusTcpClient, ModbusSerialClient
from pymodbus import ModbusException
import datetime
class ModbusReader:
    def __init__ (  self, mode: str = 'tcp', ip: str = '127.0.0.1', port: int = 502, timeout: int = 1,
                    comport: str = 'COM1', baudrate: int = 9600, slaveId:int = 0, bytesize: int = 8
                    , stopbit: int = 1, parity:str = 'N',) -> None:
        """_summary_

        Args:
            mode (str, optional): Modbus communicate mode. Defaults to 'tcp'.
            ip (str, optional): Modbus TCP device's ip. Defaults to '127.0.0.1'.
            port (int, optional): Modbus TCP device's port. Defaults to 502.
            timeout (int, optional): Modbus read timeout. Defaults to 1.
            comport (str, optional): Modbus RTU device comport. Defaults to 'COM1'.
            baudrate (int, optional): Modbus RTU device baudrate. Defaults to 9600.
            slaveId (int, optional): Modbus RTU device slaveID. Defaults to 0.
            bytesize (int, optional): Modbus RTU data packet size. Defaults to 8.
            stopbit (int, optional): Modbus RTU data packet stop bit. Defaults to 1.
            parity (str, optional): Modbus RTU data packet parity. Defaults to 'N'.
        """
        self._data_list = { 'function_03':[], 
                            'function_04':[], 
                            'Time': datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                            'modbusStatus': False}
        self._retry_count = 0
        if mode == 'tcp':
            self._ip = ip
            self._port = port
            self._connect_mode = 'tcp'
            self._slave_id = slaveId
            self._timeout = timeout
            self._create_client()
        elif mode == 'rtu':
            self._connect_mode = 'rtu'
            self._slave_id = slaveId
            self._comport = comport
            self._baudrate = baudrate
            self._bytesize = bytesize
            self._parity = parity
            self._timeout = timeout
            self._stopbit = stopbit
            self._create_client()
        else:
            assert AttributeError('mode error')
    def _create_client(self):
        """will create a client depending on the mode specified.
        """
        if self._connect_mode == 'tcp':
            self._client = ModbusTcpClient(host= self._ip, port= self._port, timeout=self._timeout, retries = 3 )
        elif self._connect_mode == 'rtu':
            self._client = ModbusSerialClient(port=self._comport, baudrate=self._baudrate, bytesize=self._bytesize, parity=self._parity, stopbits=self._stopbit, timeout=self._timeout)
    def readHoldingReg(self, startAddress:int, quantity:int) ->list:
        """Read modbus Holding Register function code(0x03)

        Args:
            startAddress (int): The Address start to read.
            quantity (int): The quantity to read from the modbus.

        Returns:
            list: The value read from the modbus.
        """
        output =[]
        if quantity == 0:
            return [0]
        if self._connect_mode == 'tcp':
            try:
                output = self._client.read_holding_registers(startAddress, quantity)
            except:
                # output = [0]*quantity
                output = None
        elif self._connect_mode == 'rtu':
            output = self._client.read_holding_registers(startAddress, quantity, slave = self._slave_id)
        # if output is None:
        #     return [0]*quantity
        try:
            output = output.registers
        except:
            # output = [0]*quantity
            output = None
        return output
    
    def readInputReg(self, startAddress:int, quantity:int) ->list:
        """Read modbus Input Register function code(0x04)

        Args:
            startAddress (int): The Address start to read.
            quantity (int): The quantity to read from the modbus.

        Returns:
            list: The value read from the modbus.
        """
        output =[]
        if quantity == 0:
            return [0]
        if self._connect_mode == 'tcp':
            try:
                output = self._client.read_input_registers(startAddress, quantity)
            except:
                output = [0]*quantity
        elif self._connect_mode == 'rtu':
            output = self._client.read_input_registers(startAddress, quantity, slave = self._slave_id)
        if output is None:
            return []
        try:
            output = output.registers
        except:
            assert InterruptedError('Modbus Read ERROR')
            output = [0]*quantity

        return output
    
    def writeHoldingReg(self, startAddress:int, data:int) -> bool:
        """Write data back to the modbus function code (0x06)

        Args:
            startAddress (int): The address to write.
            data (int): The value to write back.

        Returns:
            bool: When write success return True. If not return False.
        """
        if self._connect_mode == 'tcp':
            respond = self._client.write_register(startAddress, data)
        elif self._connect_mode == 'rtu':
            respond = self._client.write_register(startAddress, data, slave = self._slave_id)
        if respond.isError():
            return False
        else:
            return True

    def writeHoldingRegs(self, startAddress:int, datas:list)-> bool:
        """Write multiple datas back to the modbus. Function code(0x10)

        Args:
            startAddress (int): The address to write.
            data (list): The value to write back.

        Returns:
            bool: When write success return True. If not return False.
        """
        if self._connect_mode == 'tcp':
            respond = self._client.write_registers(startAddress, datas)
        elif self._connect_mode == 'rtu':
            respond = self._client.write_registers(startAddress, datas, slave= self._slave_id)
        if respond == ModbusException.isError():
            return False
        else:
            return True
    
if __name__ == '__main__':
    modbus_reader = ModbusReader()
    respond = modbus_reader.readHoldingReg(10000, 5)
    print(respond)
