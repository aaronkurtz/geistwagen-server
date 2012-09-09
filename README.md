GEISTWAGEN

Stone Soup Dungeon Crawl bones sharing

Do you enjoy playing locally but get sick of killing your own
ghosts? Geistwagen fixes that. Upload your own ghosts, download
random people's ghosts and fight other people's failures for a change.

Inspired by Nethack's Hearse.

 ---

HOW? 

Short answer: use geistwagen-client

Long answer:

To upload, POST bones files to /bones.LEVEL, where LEVEL is a legitimate crawl level

examples:
#TODO Go to http://geistwagen-hardsun.rhcloud.com/upload in a browser
curl -X POST bones.LEVEL http://geistwagen-hardsun.rhcloud.com/bones.LEVEL
wget -O- --post-file bones.LEVEL http://geistwagen-hardsun.rhcloud.com/bones.LEVEL

To download, GET /bones and save according to the Content-Disposition header

examples:
#TODO Go to http://geistwagen-hardsun.rhcloud.com/bones in a browser
curl -J -O http://geistwagen-hardsun.rhcloud.com/bones
wget --content-disposition http://geistwagen-hardsun.rhcloud.com/bones

#TODO Include query option explanations
