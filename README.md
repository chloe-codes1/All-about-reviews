# Movie Reviews

> A simple movie review app with Django

<br>

<br>

### 진행하며 어려웠던 점 & 새롭게 알게된 점

- #### `truncatechars_html`

  - 전체 review list를 보여주는 page( `review_html` ) 에서는 **content**를 다 보여주지 않고 **ellipsis** 로 표현하고 싶어서 Django documentation을 찾아보았더니 역시나 **built-in template**이 있었다...!

    ex)

    ```html
    {{review.content|truncatechars_html:30}}
    ```

  - 이렇게 해서 30자만 보여주어서 list에서는 각 review에 대한 크기가 일정하게 유지하도록 구현했다.

- #### `linebreaksbr`

  - Django는 좋은 template을 많이 갖고 있는 것 같다.  `\n` 을    `<br>` 로 바꿔주어 `<input>`에 입력된 줄바꿈을 출력 시 적용되도록 구현했다.

    ex)

    ```html
    {{review.content|linebreaksbr}}
    ```

- #### `.raw()`

  - Django에서는 **SQL query**를 어떻게 작성할지 궁금해서 찾아보니 `.raw()`라는 method가 있었다

  - *Raw query must include the primary key* 라고 error가 나서 찾아보고 select문에 `rowid as id` 를 추가하여 해결했다

  - Django에서 SQL문을 쓸 때 table명에 `[app name]_table name`인 것을 새로 알게 되었다  

    ex)

    ```python
    Review.objects.raw('select rowid as id, movie_title, avg_rate from (select movie_title, avg(rank) as avg_rate from community_review group by movie_title order by avg_rate desc) LIMIT 3')
    ```

    

<br>

<br>

### Features

- #### `Search`

  - 영화 제목을 기준으로 검색하도록 `Review.objects.filter(movie_title__icontains=keyword)` 를 활용했다.

- #### `Top rated movies`

  - 평점이 가장 높은 3개의 영화를 리뷰 리스트 화면 상단에 출력하는 기능을 추가했다.

  - 글이 하나도 없을 때에는 Top rated movie가 출력될 `table`을 출력하지 않기 위해 조건문을 사용했다. 

    ( `views.py`에서 **ranks**로 순위 정보를 넘겨준다)

    ```html
    {% if ranks %}
     ...
    {% endif %}
    ```

    

<br>

<br>

###  Deployment

- `MS Azure` 에 `Fabric` 으로 배포했다!
  - 처음 **Azure** 써보면서 많이 헤맸다. 
  - `Azure Virtual Machine` 만들고 배포한 과정을 **Github TIL repo**에 정리해서 <s>올려야겠다.</s>
  - 정리해서 올렸다!
    - [TIL 보러가기](https://github.com/chloe-codes1/TIL/blob/master/Server/Deployment/Deploying_a_Django_project_on_Microsoft_Azure.md) 
    - Deployed in [HERE](https://bit.ly/Movie-reviews) !





<br>

<br>

### 더 추가할 기능

- [x] Order by `rank`
  - 아무래도 review site인 만큼 영화 평점순으로 정렬하면 좋을 것 같다! <s> 추가해야징</s>
  - 추가했다!

- [x] Deployment
  - 지난 프로젝트에서 `PythonAnywhere`에 배포 해봤으므로 이번엔 다른 web hosting site에 <s> 배포해봐야겠다! </s>
  - `MS Azure` 에 배포했다!
  
  <br>

<br>

<br>

`+`

# Deploying a Django project on Microsoft Azure

<br>

<br>

### 1. Deploy `Azure Virtual machine`

<br>

#### 1-1. Go to the `Virtual Machine`

<br>

#### 1-2. Add Virtual Machine with `+Add` button

- I chose `Ubuntu Sever 18.04 LTS` because I personally like **Ubuntu** and I'm currently using `Ubuntu 18.04.4 LTS`.
- Other options are totally up-to your app condition

<br>

#### 1-3. When your server deployment is finished, go to `overviews`

- Copy your server's `IP address` (you'll need it when you edit `deploy.json`)

<br>

<br>

### 2. Upload & Deploy your Django project with `Fabric3`

<br>

#### 2-1. Install `Fabric3`

```bash
$ pip install fabric3
```

<br>

#### 2-2. Add `fabfile.py` and edit `deploy.json` & move them into your project (where `manage.py exists`)

> fabfile.py

```python
from fabric.contrib.files import append, exists, sed, put
from fabric.api import env, local, run, sudo
import random
import os
import json

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# deploy.json파일을 불러와 envs변수에 저장하긔
with open(os.path.join(PROJECT_DIR, "deploy.json")) as f:
    envs = json.loads(f.read())

REPO_URL = envs['REPO_URL']
PROJECT_NAME = envs['PROJECT_NAME']
REMOTE_HOST = envs['REMOTE_HOST']
REMOTE_USER = envs['REMOTE_USER']
STATIC_ROOT_NAME = envs['STATIC_ROOT']
STATIC_URL_NAME = envs['STATIC_URL']
MEDIA_ROOT = envs['MEDIA_ROOT']


env.user = REMOTE_USER
username = env.user
env.hosts = [
    REMOTE_HOST,
    ]
project_folder = '/home/{}/{}'.format(env.user, PROJECT_NAME)
apt_requirements = [
    'ufw',
    'curl',
    'git',
    'python3-dev',
    'python3-pip',
    'build-essential',
    'python3-setuptools',
    'apache2',
    'libapache2-mod-wsgi-py3',
    'libssl-dev',
    'libxml2-dev',
    'libjpeg8-dev',
    'zlib1g-dev',
]

def new_server():
    setup()
    deploy()

def setup():
    _mkdir_ssh()
    _register_ssh_key()
    _get_latest_apt()
    _install_apt_requirements(apt_requirements)
    _make_virtualenv()

def deploy():
    _get_latest_source()
    _update_settings()
    _update_virtualenv()
    _update_database()
    _make_virtualhost()
    _grant_apache2()
    _grant_sqlite3()
    _restart_apache2()
    
def create_superuser():
    virtualenv_folder = project_folder + '/../.virtualenvs/{}'.format(PROJECT_NAME)
    run('cd %s && %s/bin/python3 manage.py createsuperuser' % (
        project_folder, virtualenv_folder
    ))

def _mkdir_ssh():
    USER_HOME = os.path.expanduser('~')
    if not os.path.exists(os.path.join(USER_HOME, '.ssh/')):
        local("mkdir {}".format(os.path.join(USER_HOME, '.ssh')))
    
def _register_ssh_key():
    local("ssh-keyscan -H {} >> {}".format(REMOTE_HOST, os.path.expanduser('~/.ssh/known_hosts')))
    
def _get_latest_apt():
    update_or_not = input('Would U install Apache2/Python3 ?\n'
                          '[y/n, default: y]: ')
    if update_or_not!='n':
        sudo('sudo apt-get update && sudo apt-get -y upgrade')

def _install_apt_requirements(apt_requirements):
    reqs = ''
    for req in apt_requirements:
        reqs += (' ' + req)
    sudo('sudo apt-get -y install {}'.format(reqs))

def _make_virtualenv():
    if not exists('~/.virtualenvs'):
        script = '''"# python virtualenv settings
                    export WORKON_HOME=~/.virtualenvs
                    export VIRTUALENVWRAPPER_PYTHON="$(command \which python3)"  # location of python3
                    source /usr/local/bin/virtualenvwrapper.sh"'''
        run('mkdir ~/.virtualenvs')
        sudo('sudo pip3 install virtualenv virtualenvwrapper')
        run('echo {} >> ~/.bashrc'.format(script))

def _get_latest_source():
    if exists(project_folder + '/.git'):
        run('cd %s && git fetch' % (project_folder,))
    else:
        run('git clone %s %s' % (REPO_URL, project_folder))
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run('cd %s && git reset --hard %s' % (project_folder, current_commit))

def _update_settings():
    settings_path = project_folder + '/{}/settings.py'.format(PROJECT_NAME)
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS = .+$',
        'ALLOWED_HOSTS = ["%s"]' % (REMOTE_HOST,)
    )
    secret_key_file = project_folder + '/{}/secret_key.py'.format(PROJECT_NAME)
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv():
    virtualenv_folder = project_folder + '/../.virtualenvs/{}'.format(PROJECT_NAME)
    if not exists(virtualenv_folder + '/bin/pip'):
        run('cd /home/%s/.virtualenvs && virtualenv %s' % (env.user, PROJECT_NAME))
    run('%s/bin/pip install "django==3.0.4"' % (
        virtualenv_folder
    ))
    # 내 app INSTALLED_APPS에 bootstrap4가 있어서 (bootstrap4를 사용해서) VM에도 설치하지 않으면 error가 남!
    run('%s/bin/pip install "django-bootstrap4" ' %(
        virtualenv_folder
    ))



def _update_database():
    virtualenv_folder = project_folder + '/../.virtualenvs/{}'.format(PROJECT_NAME)
    run('cd %s && %s/bin/python3 manage.py migrate --noinput' % (
        project_folder, virtualenv_folder
    ))

def _make_virtualhost():
    script = """'<VirtualHost *:80>
    ServerName {servername}
    Alias /{static_url} /home/{username}/{project_name}/{static_root}
    Alias /{media_url} /home/{username}/{project_name}/{media_url}
    <Directory /home/{username}/{project_name}/{media_url}>
        Require all granted
    </Directory>
    <Directory /home/{username}/{project_name}/{static_root}>
        Require all granted
    </Directory>
    <Directory /home/{username}/{project_name}/{project_name}>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    WSGIDaemonProcess {project_name} python-home=/home/{username}/.virtualenvs/{project_name} python-path=/home/{username}/{project_name}
    WSGIProcessGroup {project_name}
    WSGIScriptAlias / /home/{username}/{project_name}/{project_name}/wsgi.py
    ErrorLog ${{APACHE_LOG_DIR}}/error.log
    CustomLog ${{APACHE_LOG_DIR}}/access.log combined
    </VirtualHost>'""".format(
        static_root=STATIC_ROOT_NAME,
        username=env.user,
        project_name=PROJECT_NAME,
        static_url=STATIC_URL_NAME,
        servername=REMOTE_HOST,
        media_url=MEDIA_ROOT
    )
    sudo('echo {} > /etc/apache2/sites-available/{}.conf'.format(script, PROJECT_NAME))
    sudo('a2ensite {}.conf'.format(PROJECT_NAME))

def _grant_apache2():
    sudo('sudo chown -R :www-data ~/{}'.format(PROJECT_NAME))

def _grant_sqlite3():
    sudo('sudo chmod 775 ~/{}/db.sqlite3'.format(PROJECT_NAME))

def _restart_apache2():
    sudo('sudo service apache2 restart'
```

<br>

> deploy.json - edit it!

```json
{
  "REPO_URL":"Your Github Repository URL",
  "PROJECT_NAME":"DjangoProject folder's name(where settings.py exists)",
  "REMOTE_HOST":"Your domain (IP address for your Azure server)",
  "REMOTE_USER":"Your user name on the Azure server",
  "STATIC_ROOT":"static",
  "STATIC_URL":"static",
  "MEDIA_ROOT":"media"
}
```

- I had to modify `fabfile.py` several times because of the errors
- Check the error messages & google it!
  - It could take some time, but I'm pretty sure that is worth it

<br>

#### 2-3 . Execute new server

```bash
$ fab new_server
```

- Install `python3`, `apache2`, and `mod_wsgi` to run django

<br>

#### 2-4. Deploy code through `Fabric3`

```bash
$ fab deploy
```

- **Fetch** latest code on your github repo and **migrate** db

<br>

#### 2-5. Create superuser

```bash
$ fab create_superuser
```

<br>

<br>

### 3. Congrats! Now you are live!

<br>