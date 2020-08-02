class anime:
    'the data class for an anime'

    def __init__(self, ID, title, rating, status, synopsis, image, episodes):
        ongoingDict = {True:'Ongoing', False:"Completed"}   
        self.ID = ID
        self.title = title
        self.rating = rating
        self.status = ongoingDict[status]
        self.synopsis = synopsis
        self.image = image
        self.episodes = episodes
    
    def __str__(self):
        return "Anime: " + self.title

