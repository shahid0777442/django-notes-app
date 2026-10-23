pipeline {
    agent any

    stages {
        stage('Clone the Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/shahid0777442/django-notes-app.git'
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh 'python3 -m venv django'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    . django/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Django App') {
            steps {
                sh '''
                    . django/bin/activate
                    python manage.py makemigrations
                    python manage.py migrate

                    pkill -f "manage.py runserver" || true

                    export DJANGO_ALLOWED_HOSTS="18.212.101.106,localhost,127.0.0.1"
                    export DJANGO_DEBUG=1
                    JENKINS_NODE_COOKIE=dontKillMe nohup python manage.py runserver 0.0.0.0:8000 > django.log 2>&1 &
                '''
            }
        }
    }
}
