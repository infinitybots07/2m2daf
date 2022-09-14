if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/enthada-myre/ThomasBotV3 /ThomasBotV3
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /ThomasBotV3
fi
cd /ThomasBotV3
pip3 install -U -r requirements.txt
echo "sᴛᴀʀᴛɪɴɢ......."
python3 bot.py
