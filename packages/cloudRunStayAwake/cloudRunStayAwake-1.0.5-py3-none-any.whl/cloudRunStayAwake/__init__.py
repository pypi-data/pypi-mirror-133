import signal
from .cloudRunStayAwake import stayAwake

# Define trigger for SIGTERM signal, just before the service to be stopped
signal.signal(signal.SIGTERM, stayAwake)
signal.signal(signal.SIGINT, stayAwake)