# Use a valid Jenkins agent image as base
FROM jenkins/inbound-agent:4.10-3-jdk11

# Switch to root user for installation
USER root

# Install Docker CLI
RUN apt-get update && apt-get install -y docker.io

# Switch back to the Jenkins user
USER jenkins
