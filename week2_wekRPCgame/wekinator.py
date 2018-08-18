from pythonosc import dispatcher
from pythonosc import osc_server

from threading import Thread

class Wekinator():
    def __init__(self,*args,**kwargs):
        self.ip = args[0]
        self.port = args[1]
        self.wek_message_handler = args[2]
        self.init_wek_output(self.ip,self.port,self.wek_message_handler)


    """
    initialise Wekinator Output message receiver
    This function creates a thread of listening incoming OSC message at  
    """
    def init_wek_output(self,ip,port,wek_message_handler):

        wek_dispatcher = dispatcher.Dispatcher()
        ## create an event dispatcher for "/wek/outputs" address.
        ## set event handler "wek_message_handler"
        wek_dispatcher.map("/wek/outputs", wek_message_handler)

        ## setup and start an osc server thread on specified ip address and port.
        self.server = osc_server.ThreadingOSCUDPServer(
            (ip, port), wek_dispatcher)
        print("Serving on {}".format(self.server.server_address))

        server_thread = Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        return self.server
    
    def close(self):
        self.server.shutdown()