# Next Episode

next-episode is a set of console commands intended to make it easier to rename files into kodi series format. It is
intended to be used as hotkeys in the ranger or midnight commander file managers

- next-episode add .sxxexx in front of the file extension. With sxx being the current season and exx being the next
  episode number. Or s01e01 if the directory is 'fresh'
- next-season add .sxxe01 in front of the file extension. With sxx being the current season +1 or s01 if the directory
  is 'fresh'
- remove-episode remove .sxxexx tag from the given file
- fill-episode much the same as next-episode but it checks if there are missing episodes in seasons and assigns that tag
  instead.
- generate-nfo generate a minimal .nfo file with unique uuid and title based on the files filename without tag or
  extension
- generate-series-nfo generate a minimal tvseries.nfo with unique uuid and title based on the directory itlives in
- next-artwork copy image file to banner.jpg, season01-banner.jpg, season02-banner.jpg ...