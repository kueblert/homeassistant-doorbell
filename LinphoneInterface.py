import os
import time
import subprocess
import sys
from time import sleep
from queue import Queue
from threading import Thread
from typing_extensions import Literal
from SIPInterface import SIPInterface
import logging
from Config import RING_SIP_NUMBER, SIP_USERNAME, SIP_PASSWORD

log = logging.getLogger("Linphone")
log.setLevel(logging.ERROR)

class LinphoneInterface(SIPInterface):
    __process = None
    __thread: Thread = None
    should_run: bool = True
    # Linphone subprocess is observed in a separate thread.
    # Thus, we need queues for non-blocking communication.
    cmd_queue: Queue = Queue()
    #out_queue: Queue = Queue()

    def __init__(self, call_state_changed_callback, code_received_callback, on_error_callback):
        SIPInterface.__init__(self, call_state_changed_callback, code_received_callback, on_error_callback)
        self.__thread = Thread(target=self.__run, daemon=True)
        self.__thread.start()
        
    def __run(self):
        cmd = 'linphonec', '-b', '.linphonerc', '-d', '0'
        self.__process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        os.set_blocking(self.__process.stdout.fileno(), False)
        os.set_blocking(self.__process.stderr.fileno(), False)
        # suppress echos while the other end is talking
        self.send("el on")
        while self.should_run and self.__process.returncode is None:
            line = self.__process.stdout.readline()
            if line:
                self.__handle(line.decode("utf-8").rstrip())
            err_line = self.__process.stderr.readline()
            if err_line:
                self.__handle_error(err_line.decode("utf-8").rstrip())
            sleep(0.01)
        log.debug("Exiting linphone thread main loop")
        self.should_run = False

    def call(self, number: str):
        self.send("call %s" % number)
    
    def hang_up():
        self.send("terminate")
    
    def send(self, cmd: str):
        self.cmd_queue.put(cmd)

    def __handle(self, line: str):
        log.info("h: %s" % line)
        if line.startswith("linphonec>"):
            if not self.cmd_queue.empty():
                self.__write(self.cmd_queue.get())
        elif line == f"Password for {SIP_USERNAME} on fritz.box:":
            self.send(SIP_PASSWORD)
        elif line.startswith("Receiving tone "):
            code = line[len("Receiving tone ")]
            self.code_received(code)
        elif line.startswith(f"Establishing call id to sip:{RING_SIP_NUMBER}@fritz.box"):
            self.call_state_changed("estabilishing_call")
        elif line.endswith("to sip:{RING_SIP_NUMBER}@fritz.box in progress."):
            self.call_state_changed("call_in_progress")
        elif line.endswith("with sip:{RING_SIP_NUMBER}@fritz.box ended (Call declined)."):
            self.call_state_changed("call_declined")
        elif line.endswith("with sip:{RING_SIP_NUMBER}@fritz.box connected."):
            self.call_state_changed("call_connected")
            # the other side has answered the call.
            #self.send("unmute")
        elif "with sip:{RING_SIP_NUMBER}@fritz.box ended" in line:
            self.call_state_changed("call_ended")
            self.should_run = False
        #self.out_queue.put(line)
    
    def __handle_error(self, err: str):
        if "belle-sip-error-TCP bind() failed for ::0 port 5060: Address already in use" in err:
            log.warning("ERROR: Port blocked!")
        self.on_error(err)

    def __write(self, cmd: str):
        self.__process.stdin.write(("%s\n"%cmd).encode("utf-8"))
        self.__process.stdin.flush()
        log.info("I: %s"%cmd)

    def __del__(self):
        self.__process.terminate()


