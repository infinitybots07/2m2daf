if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/NIHUU/Thomas-2 /Thomas-2
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /Thomas-2
fi
cd /Thomas-2
pip3 install -U -r requirements.txt
echo "sᴛᴀʀᴛɪɴɢ......."
python3 bot.py
