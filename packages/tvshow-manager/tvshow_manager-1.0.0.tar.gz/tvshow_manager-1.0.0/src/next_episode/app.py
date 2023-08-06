import sys
import os
from .file_list import File
from .artwork import Artwork
from .show_nfo import ShowNfo


class App:
    def next_episode(self):
        self.assert_argument_passed()


        target = File.fromRelativePath(sys.argv[1])
        target.applyNextEpisodeTag()
        return 0

    def next_artwork(self):
        self.assert_argument_passed()

        target = Artwork(sys.argv[1])
        target.as_next_season()
        return 0

    def nextSeason(self):
        self.assert_argument_passed()

        target = File.fromRelativePath(sys.argv[1])
        target.applyNextSeasonTag()
        return 0

    def removeTag(self):
        self.assert_argument_passed()

        target = File.fromRelativePath(sys.argv[1])
        target.removeTag()
        return 0

    def fillEpisode(self):
        self.assert_argument_passed()

        target = File.fromRelativePath(sys.argv[1])
        target.applyFillerTag()
        return 0

    def generate_nfo(self):
        self.assert_argument_passed()

        target = File.fromRelativePath(sys.argv[1])
        target.generate_nfo()

    def generate_show_nfo(self):
        series_nfo = ShowNfo.fromDirectory(os.getcwd())
        series_nfo.save()

    def assert_argument_passed(self):
        if len(sys.argv) < 2:
            self.print_help()
            sys.exit(1)

    def print_help(self):
        print("USAGE")
        print(sys.argv[0]+" path/to/next/file")

