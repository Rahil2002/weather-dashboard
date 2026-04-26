pipeline {

    // Run this pipeline on the Jenkins server itself
    agent any

    // Environment variables available to all stages
    environment {
        DOCKER_IMAGE    = "rahil2002/weather-dashboard"
        DOCKER_TAG      = "v${BUILD_NUMBER}"   // auto-increments each build e.g. v1, v2, v3
        CONTAINER_NAME  = "weather-app"
        APP_PORT        = "5000"
    }

    stages {

        // ── Stage 1: Get the code ─────────────────────────────
        stage('Checkout') {
            steps {
                echo '📥 Pulling latest code from GitHub...'
                checkout scm   // Jenkins pulls your GitHub repo automatically
            }
        }

        // ── Stage 2: Install dependencies and test ────────────
        stage('Test') {
            steps {
                echo '🧪 Installing dependencies and running tests...'
                bat '''
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pytest
                    pytest test_app.py -v
                '''
            }
        }

        // ── Stage 3: Build Docker image ───────────────────────
        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                bat "docker build -t %DOCKER_IMAGE%:%DOCKER_TAG% ."
                bat "docker tag %DOCKER_IMAGE%:%DOCKER_TAG% %DOCKER_IMAGE%:latest"
            }
        }

        // ── Stage 4: Push to Docker Hub ───────────────────────
        stage('Push to Docker Hub') {
            steps {
                echo '📤 Pushing image to Docker Hub...'
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-credentials',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    bat "docker login -u %DOCKER_USER% -p %DOCKER_PASS%"
                    bat "docker push %DOCKER_IMAGE%:%DOCKER_TAG%"
                    bat "docker push %DOCKER_IMAGE%:latest"
                }
            }
        }

        // ── Stage 5: Deploy locally (we'll add Azure later) ───
        stage('Deploy') {
            steps {
                echo '🚀 Deploying container...'
                withCredentials([string(
                    credentialsId: 'openweather-api-key',
                    variable: 'API_KEY'
                )]) {
                    // Stop and remove old container if running
                    bat "docker stop %CONTAINER_NAME% || exit 0"
                    bat "docker rm %CONTAINER_NAME% || exit 0"

                    // Run the new container
                    bat "docker run -d -p %APP_PORT%:%APP_PORT% --name %CONTAINER_NAME% --restart always -e OPENWEATHER_API_KEY=%API_KEY% %DOCKER_IMAGE%:latest"
                }
            }
        }

    }

    // ── Run these after every build regardless of result ──────
    post {
        success {
            echo '✅ Pipeline completed successfully! Weather app is live.'
        }
        failure {
            echo '❌ Pipeline failed. Check the logs above to see which stage failed.'
        }
        always {
            echo '🧹 Cleaning up unused Docker images...'
            bat "docker image prune -f"
        }
    }

}