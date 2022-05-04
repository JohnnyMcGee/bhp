cd "$(dirname "${BASH_SOURCE[0]}")"

python -m venv bhp
echo "[+] created venv 'bhp'"
if [ "$(uname -o)"=~"*Linux*" ];
then
	chmod 754 bhp/bin/activate 
	bhp/bin/activate
	echo "[+] activated 'bhp'"
else
       	bhp/Scripts/activate
	echo "[+] activated 'bhp'"
fi

echo "[+] installing requirements..."
pip install -r requirements.txt

echo "[+] getting paramiko test key"
cd ..
if [ ! -d ../paramiko ]; then
git clone "https://github.com/paramiko/paramiko"
fi
cp paramiko/demos/test_rsa.key ./bhp/network_tools/
cd -
echo "Setup complete!"
