from .cbt import Recorder
try:
    recorder = Recorder()
except Exception as e:
    print(e)
