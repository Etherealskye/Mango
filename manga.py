class manga:
    'Data class for a manga'

    def __init__(self, ID, title, rating, status, synopsis, image, chapters, volumes):
        publishingDict = {True:'Ongoing', False:"Completed"}   
        self.ID = ID
        self.title = title
        self.rating = rating
        self.status = publishingDict[status]
        self.synopsis = synopsis
        self.image = image
        self.chapters = chapters
        self.volumes = volumes
    
    def __str__(self):
        return 'Manga: ' + self.title
