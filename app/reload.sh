rm test_db.sqlite3
find . -wholename "*migrations/000*py" -delete
poetry run python manage.py makemigrations
poetry run python manage.py migrate
poetry run python manage.py shell <../dev_tools/create_superuser.py
poetry run python manage.py loaddata ../dev_tools/fixtures/auth_app.json
poetry run python manage.py loaddata ../dev_tools/fixtures/cv_app_busy_type.json
poetry run python manage.py loaddata ../dev_tools/fixtures/cv_app_relocation_type.json
poetry run python manage.py loaddata ../dev_tools/fixtures/cv_app_cv.json
poetry run python manage.py loaddata ../dev_tools/fixtures/project_app_project.json
poetry run python manage.py loaddata ../dev_tools/fixtures/role_app.json
poetry run python manage.py loaddata ../dev_tools/fixtures/project_app_membership.json
poetry run python manage.py loaddata ../dev_tools/fixtures/favorite_app.json
poetry run python manage.py loaddata ../dev_tools/fixtures/vacancy_app_applicant_level.json
poetry run python manage.py loaddata ../dev_tools/fixtures/vacancy_app_employment_type.json
poetry run python manage.py loaddata ../dev_tools/fixtures/vacancy_app_job_type.json
poetry run python manage.py loaddata ../dev_tools/fixtures/vacancy_app_payment_account.json
poetry run python manage.py loaddata ../dev_tools/fixtures/vacancy_app_company.json
poetry run python manage.py loaddata ../dev_tools/fixtures/vacancy_app_vacancy.json
