echo ":: Starting Inital Setup"

echo ":: Coping enviroment"
cp .env.template .env

echo ":: Creating virtual environment"
python -m venv venv

echo ":: Activating virtual environment"
.\venv\Scripts\Activate.ps1

echo ":: Installing requirements"
pip install -r requirements.txt

echo ":: Installation complete"



