GEISTWAGEN

Stone Soup Dungeon Crawl bones sharing

Do you enjoy playing locally but get sick of killing your own
ghosts? Geistwagen fixes that. Upload your own ghosts, download
random people's ghosts and fight other people's failures for a change.

Inspired by Nethack's Hearse.

 ---

HOW? 

Short answer: use geistwagen-client https://github.com/akahs/geistwagen-client

Long answer:

To upload, PUT bones files to /bones.LEVEL, where LEVEL is a legitimate crawl level


examples:

curl -X PUT -T bones.LEVEL http://geistwagen-hardsun.rhcloud.com/bones.LEVEL

To download, GET /bones and save according to the Content-Disposition header


examples:

curl -J -O http://geistwagen-hardsun.rhcloud.com/bones

wget --content-disposition http://geistwagen-hardsun.rhcloud.com/bones


Options include:

sameip=True - download files uploaded by your IP address, which is usually disabled

delete=True - have the server delete the bones file you downloaded

exclude=D-1.D-2.D-3 period-separated list of levels to not download

debug=True - get debug output of what your request would give
