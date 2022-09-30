from typing_extensions import Literal


class SIPInterface:
    cb_call_state_changed = None
    cb_code_received = None
    cb_on_error = None

    def __init__(self, call_state_changed_callback, code_received_callback, on_error_callback):
        self.cb_call_state_changed = call_state_changed_callback
        self.cb_code_received = code_received_callback
        self.cb_on_error = on_error_callback
        self.state = "init"
    
    def call(self, number: str):
        pass
    
    def hang_up():
        pass
    
    def call_state_changed(self, new_state: Literal["init", "estabilishing_call", "call_in_progess", "call_connected", "call_ended", "error"]):
        if self.cb_call_state_changed is not None:
            self.cb_call_state_changed(new_state)
            
    def code_received(self, code: str):
        if self.cb_code_received is not None:
            self.cb_code_received(code)
            
    def on_error(self, error: str):
        if self.cb_on_error is not None:
            self.cb_on_error(error)
