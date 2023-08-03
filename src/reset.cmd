
rm /home/martin/.ectree.sqlite

python3 ectini.py
python3 ectar.py I "/home/martin/Music"
python3 ectar.py X "/home/martin/Music/Stowaway Soundtrack"
python3 ectar.py I "/home/martin/privat"
python3 ectar.py I "/home/martin/work"
python3 ectar.py I "/media/veracrypt1"
python3 ectar.py X "/media/veracrypt1/$RECYCLE.BIN"
python3 ectar.py X "/media/veracrypt1/System Volume Information"
python3 ectar.py X "/media/veracrypt1/.Trash-1000"
python3 ectar.py X "/media/veracrypt1/.Trash-1013"
python3 ectar.py I "/media/veracrypt2"
python3 ectar.py X "/media/veracrypt2/$RECYCLE.BIN"
python3 ectar.py X "/media/veracrypt2/System Volume Information"
python3 ectar.py X "/media/veracrypt2/.Trash-1000"
python3 ectar.py X "/media/veracrypt2/.Trash-1013"

# The following is not a good idea ... think init.py, .js, etc. - it is a mess!
# python3 ectar.py I /home/martin
# python3 ectar.py X /home/martin/.cache
# python3 ectar.py X /home/martin/.conda
# python3 ectar.py X /home/martin/.config
# python3 ectar.py X /home/martin/.eclipse
# python3 ectar.py X /home/martin/.gtk-gnutella
# python3 ectar.py X /home/martin/.local
# python3 ectar.py X /home/martin/.mozilla
# python3 ectar.py X /home/martin/.thunderbird
# python3 ectar.py X /home/martin/MEGA/.debris
# python3 ectar.py X /home/martin/software