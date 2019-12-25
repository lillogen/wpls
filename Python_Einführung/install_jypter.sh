echo "updating PIP"
pip install --upgrade pip
echo "Installing jupiter Notebook-Server"
sudo pip install jupyter
python2 -m pip install ipykernel
python2 -m ipykernel install --user
