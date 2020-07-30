class hololiveStreamer:
    'Data class for a hololive streamer'

    def __init__(self, group, title, profile):
        self.group = group
        self.channel_title = title
        self.channel_profile = profile

    def setposition(self,position):
        position = position
    
    def __str__(self):
        return self.channel_title + " " + self.channel_profile