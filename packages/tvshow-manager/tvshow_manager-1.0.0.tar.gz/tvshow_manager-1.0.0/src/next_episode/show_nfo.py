import os
import uuid
from .template import indentedText
from .artwork import ArtworkFactory

class ShowNfo:
    @staticmethod
    def fromDirectory(directory):
        return ShowNfo(directory)

    def __init__(self, directory):
        self.directory = os.path.abspath(directory)

    def save(self):
        if os.path.exists(self.tv_show_nfo()):
            return

        with open(self.tv_show_nfo(), 'w') as file:
            file.write(
                '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n'
                '<tvshow>\n'
                + indentedText(4, '<title>' + self.title_from_directory() + '</title>\n')
                + indentedText(4, '<uniqueid type="home" default="true">' + str(uuid.uuid4()) + '</uniqueid>\n')
                + self.thumb() +
                '</tvshow>'
            )

    def thumb(self):
        if not self.has_thumb():
            return ''

        artwork = ArtworkFactory.from_path(self.possible_thumb())
        return indentedText(4, artwork.thumb())

    def has_thumb(self):
        siblings = os.listdir(self.directory)

        if self.possible_thumb() in siblings:
            return True

        return False

    def possible_thumb(self):
        title = self.title_from_directory()

        return title+'.jpg'

    def tv_show_nfo(self):
        return self.directory+'/tvshow.nfo'

    def title_from_directory(self):
        parts = self.directory.split(os.sep)
        return last(parts)


def last(_list):
    return _list[len(_list) - 1]