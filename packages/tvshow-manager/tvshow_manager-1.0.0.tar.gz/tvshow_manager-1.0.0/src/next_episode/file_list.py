import re
import os
import uuid
from .artwork import ArtworkFactory
from .template import indentedText


class NotFoundException(Exception):
    pass


class File:
    def __init__(self, name):
        self.directoryPath = None
        self.name = name
        self.match = re.match('.+\.s([0-9]+)e([0-9]+)\..+', name)

    @staticmethod
    def fromRelativePath(relativePath):
        file = File.fromName( os.path.basename(relativePath) )

        target = os.path.abspath(relativePath)
        file.directoryPath = os.path.dirname(target)

        return file

    @staticmethod
    def fromName(name):
        return File(name)

    def appendSeasonList(self, files):
        if self.match:
            files.append(self)

    def season(self):
        return int( self.match.group(1) )

    def episode(self):
        return int( self.match.group(2) )

    def siblings(self):
        return list( filter( lambda file: file != self.name, os.listdir(self.directoryPath) ) )

    def applyNextEpisodeTag(self):
        self.applyTag(self.nextEpisodeTag() )

    def applyNextSeasonTag(self):
        self.applyTag(self.nextSeasonTag() )

    def applyFillerTag(self):
        self.applyTag( self.nextFillerTag() )

    def generate_nfo(self):
        if not self.hasTag():
            return

        name, tag, _ = self.nameTagExtension()
        with open(self.directoryPath + '/' + name+'.'+tag+'.nfo', 'w') as file:
            file.write(
                '<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>\n'
                '<episodedetails>\n'
                + indentedText(4, '<title>'+name+'</title>\n')
                + indentedText(4, '<uniqueid type="home" default="true">'+str(uuid.uuid4())+'</uniqueid>\n')
                + self.thumb() +
                '</episodedetails>'
            )

    def thumb(self):
        if not self.hasArt():
            return ''

        artwork = ArtworkFactory.from_path(self.possible_art_path())
        return indentedText(4, artwork.thumb())

    def hasArt(self):
        return self.possible_art_path() in self.siblings()

    def removeTag(self):
        if not self.hasTag():
            return

        os.rename(
            self.directoryPath+'/'+self.name,
            self.directoryPath+'/'+self.nameWithoutTag()
        )

        _, tag, _ = self.nameTagExtension()
        self.remove_artwork_tag(tag)

    def possible_art_path(self):
        name, _, _ = self.nameTagExtension()
        return name+'.jpg'

    def applyTag(self, tag):
        if self.hasTag():
            return

        os.rename(
            self.full_path(self.name),
            self.full_path(self.nameWithTag(tag))
        )
        self.match_artwork(tag)

    def match_artwork(self, tag):
        if not self.artwork_name_without_tag() in self.siblings():
            return

        os.rename(
            self.full_path(self.artwork_name_without_tag()),
            self.full_path(self.artwork_name_with_tag(tag))
        )

    def remove_artwork_tag(self, tag):
        if not self.artwork_name_with_tag(tag) in self.siblings():
            return

        os.rename(
            self.full_path(self.artwork_name_with_tag(tag)),
            self.full_path(self.artwork_name_without_tag()),
        )

    def use_as_next_artwork(self):
        pass

    def full_path(self, file):
        return self.directoryPath+'/'+file

    def artwork_name_without_tag(self):
        name, _, extension = self.nameTagExtension()
        return name+'.jpg'

    def artwork_name_with_tag(self, tag):
        name, _, extension = self.nameTagExtension()
        return '.'.join([name, self.tag_with_artwork_type(tag), 'jpg'])

    def tag_with_artwork_type(self, tag):
        return tag+'-thumb'

    def nameWithoutTag(self):
        name, _, extension = self.nameTagExtension()
        return '.'.join([name, extension])

    def nameWithTag(self, tag):
        name, _, extension = self.nameTagExtension()
        return '.'.join([name, tag, extension])

    def nextEpisodeTag(self):
        fileList = FileList.fromFilenames( self.siblings() )

        return self.tag(fileList.currentSeason(), fileList.nextEpisode())

    def nextSeasonTag(self):
        fileList = FileList.fromFilenames( self.siblings() )
        return self.tag(fileList.nextSeason(), 1)

    def nextFillerTag(self):
        fileList = FileList.fromFilenames( self.siblings() )
        season, episode = fileList.nextFiller()


        return self.tag(season, episode)


    def tag(self, season, episode):
        return "s%02de%02d" % (season, episode)

    def nameTagExtension(self):
        match = re.match('(.*?)(\.(s[0-9]+e[0-9]+))?\.([^.]+)', self.name)
        return [match.group(1), match.group(3), match.group(4)]

    def hasTag(self):
        _, tag, _ = self.nameTagExtension()
        return tag is not None


class FileList:
    def __init__(self, fileNames):
        self.fileNames = fileNames

    @staticmethod
    def fromFilenames(fileNames):
        return FileList(fileNames)

    def nextSeason(self):
        try:
            return self.highestSeason() + 1
        except NotFoundException:
            return 1

    def currentSeason(self):
        try:
            return self.highestSeason()
        except NotFoundException:
            return 1

    def currentEpisode(self):
        try:
            return self.highestEpisode()
        except NotFoundException:
            return 0

    def nextEpisode(self):
        try:
            return self.highestEpisode() + 1
        except NotFoundException:
            return 1

    def nextFiller(self):
        highestSeason = self.highestSeason()

        for currentSeason in oneBasedRange(highestSeason):
            highestEpisode = self.highestIn( self.episodesInSeason(currentSeason), lambda file: file.episode())
            episodes = list( map(lambda file: file.episode(), self.episodesInSeason(currentSeason) ) )
            for currentEpisode in range(1, highestEpisode):
                if currentEpisode not in episodes:
                    return [currentSeason, currentEpisode]

        return [self.currentSeason(), self.nextEpisode()]

    def highestSeason(self):
        return self.highestIn(self.filesFromFileNames(), lambda file: file.season())

    def highestEpisode(self):
        highestSeason = self.highestIn(self.filesFromFileNames(), lambda file: file.season())
        episodesInSeason = self.episodesInSeason(highestSeason)
        return self.highestIn(episodesInSeason, lambda file: file.episode())

    def episodesInSeason(self, seasonNumber):
        return list( filter(lambda file: file.season() == seasonNumber, self.filesFromFileNames()) )

    def highestIn(self, files, fileAttribute):
        if len(files) == 0:
            raise NotFoundException

        highest = 1
        for file in files:
            if fileAttribute(file) > highest:
                highest = fileAttribute(file)
        return highest

    def filesFromFileNames(self):
        files = []

        for fileName in self.fileNames:
            file = File.fromName(fileName)
            file.appendSeasonList(files)

        return files

def oneBasedRange(end):
    return range(1, end+1)