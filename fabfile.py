from invoke import task


PROJECT_PATH = '~/Citadel'


def get_docker_bash_command(command):
    return f'docker-compose -f {PROJECT_PATH}/docker-compose-dev.yml exec gunicorn bash -c "{command}"'


@task
def enter_sp(c):
    c.run(get_docker_bash_command('./manage.py shell_plus'), pty=True)


@task
def enter_bash(c):
    c.run(get_docker_bash_command('bash'), pty=True)


@task
def create_superuser(c):
    c.run(get_docker_bash_command('./manage.py createsuperuser'), pty=True)


@task
def download_db_backup(c):
    """
    Скачивает с удаленной машины дамп БД в формате json
    """
    models_to_exclude = ' '.join(map(
        lambda model: f'--exclude={model}',
        [
            'auth.Permission',
            'admin.LogEntry',
            'contenttypes.ContentType',
            'sessions.Session',
            'silk',
        ])
    )

    # Вызываем команду в докерконтейнр (результат выводится на stdout), перенаправляем в файл на удаленной машине
    c.run(get_docker_bash_command(f'./manage.py dumpdata --indent 2 --format json {models_to_exclude}') + ' > db.json', pty=True)
    print('Дамп создан на уделнной машине')

    c.get('db.json')
    print('Дамп загружен')

    c.run('rm db.json')
    print('Дамп удален с удаленной машины')
