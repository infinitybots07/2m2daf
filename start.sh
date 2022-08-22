if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/enthada-myre/nouse /nouse
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /nouse
fi
cd /nouse
pip3 install -U -r requirements.txt
echo "sᴛᴀʀᴛɪɴɢ......."
python3 bot.py
