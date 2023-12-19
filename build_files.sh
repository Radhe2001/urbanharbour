echo "BUILD START"
python3.9 -m pip install -r requirements.txt
python3.9 -m pip install pillow
python3.9 -m pip install psycopg2
python3.9 manage.py collectstatic --noinput --clear
python3.9 manage.py runserver
echo "BUILD END"