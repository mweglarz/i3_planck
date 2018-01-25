
import re
from subprocess import Popen, PIPE

class VolumeProvider:

    def __init__(self, sink):
        self.sink = sink
        
    def get_volume(self):
        process = Popen(['pactl', 'list', 'sinks'],
                  stdin=PIPE, stdout=PIPE, stderr=PIPE,
                  universal_newlines=True)

        out, err = process.communicate()

        volume = self.handle(out)
        if volume == None:
            volume = "unkw"

        return volume

    def handle(self, out):
        sink_start = out.find(self.sink)

        if sink_start == -1:
            return None

        volume_start = out.find("Volume", sink_start)

        if volume_start == -1:
            return None
        
        volume_end = out.find("\n", volume_start)

        if volume_end == -1:
            return None

        volume_line = out[volume_start: volume_end]
        m = re.search('[0-9]+%', volume_line)
        if m == None:
            return m

        return m.group(0)


