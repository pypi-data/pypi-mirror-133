import os
import re
import shutil

class ArtworkFactory:
    @staticmethod
    def from_path(path):
        return Artwork(path)


class Artwork:
    def __init__(self, path):
        self.path = path

        target = os.path.abspath(path)
        self.directoryPath = os.path.dirname(target)

    def as_next_season(self):
        siblings = self._siblings()

        if 'banner.jpg' not in siblings:
            self._copy('banner.jpg')
            return

        self._copy(self.next_season_name())

    def next_season_name(self):
        return self.season_name(self.next_season())

    def season_name(self, season_number):
        return 'season%s-banner.jpg' % (str(season_number).zfill(2))

    def next_season(self):
        return self.last_season() + 1

    def last_season(self):
        siblings = self._siblings()

        expression = re.compile('season([0-9]+)-banner.jpg')
        seasons = [0]
        for file_name in siblings:
            match = expression.match(file_name)
            if match:
                seasons.append(int(match.group(1)))
        return max(seasons)

    def _siblings(self):
        return os.listdir(self.directoryPath)

    def _copy(self, file_name):
        shutil.copy(self.path, self.directoryPath+'/'+file_name)

