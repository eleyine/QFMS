echo 'Installing pip requirements'
pip install -r requirements.txt

echo 'Installing bower requirements'
bower install

echo 'Creating private settings to smf_website/settings/private.py'
cp smf_website/settings/example_private_settings.py smf_website/settings/private.py

echo 'Setting up database'

python manage.py makemigrations
python manage.py migrate

echo 'Generating dummy data'
python manage.py generate_registrations 3

echo 'Run server'
python manage.py runserver
