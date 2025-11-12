set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput


# Load data into Postgres on demand (one-time)
if [ "${LOAD_FIXTURE}" = "1" ]; then
  echo "Loading fixture: core_config/fixtures/unfiltered_seed.json"
  python manage.py loaddata core_config/fixtures/unfiltered_seed.json
fi
