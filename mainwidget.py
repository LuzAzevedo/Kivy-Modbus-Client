from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, TransitionBase, NoTransition
from kivy.lang import Builder
from kivy.clock import Clock
from pyModbusTCP.client import ModbusClient

Builder.load_file("mainwidget.kv")
modclient = ModbusClient()
class SettingsScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
                
    def connect(self):
        if self.ids.bt_con.text == 'CONNECT':
            self.ids.bt_con.text = 'DISCONNECT'
            try:
                modclient.host = self.ids.ip_input.text
                modclient.port = int(self.ids.port_input.text)
                modclient.open()
            except Exception as e:
                print(f"Error connecting to server", e.args)
        else:
            self.ids.bt_con.text = 'CONNECT'
            modclient.close()

class DataScreen(Screen):

    def read1(self, dt):
        self.ids.readings_results.text = str(modclient.read_holding_registers(int(self.ids.modbus_adress_input.text),1)[0])
    
    def read2(self, dt):
        self.ids.readings_results.text = str(modclient.read_coils(int(self.ids.modbus_adress_input.text),1)[0])
    
    def read3(self, dt):
        self.ids.readings_results.text = str(modclient.read_input_registers(int(self.ids.modbus_adress_input.text),1)[0])

    def read4(self, dt):
        self.ids.readings_results.text = str(modclient.read_discrete_inputs(int(self.ids.modbus_adress_input.text),1)[0])

    def read(self, tipo):
        if tipo == 1:
            if self.ids.checkbox.active:
                self.ids.readings_results.text = str(modclient.read_holding_registers(int(self.ids.modbus_adress_input.text),1)[0])
            else:
                self._ev = Clock.schedule_interval(self.read1,1)
        
        if tipo == 2:
            if self.ids.checkbox.active:
                self.ids.readings_results.text = str(modclient.read_coils(int(self.ids.modbus_adress_input.text),1)[0])
            else:
                self._ev = Clock.schedule_interval(self.read2,1)

        if tipo == 3:
            if self.ids.checkbox.active:
                self.ids.readings_results.text = str(modclient.read_input_registers(int(self.ids.modbus_adress_input.text),1)[0])
            else:
                self._ev = Clock.schedule_interval(self.read3,1)

        if tipo == 4:
            if self.ids.checkbox.active:
                self.ids.readings_results.text = str(modclient.read_discrete_inputs(int(self.ids.modbus_adress_input.text),1)[0])
            else:
                self._ev = Clock.schedule_interval(self.read4,1)

class TestApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(DataScreen(name='data'))

        return sm
