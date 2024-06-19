# Use the latest LTS Jenkins agent image as base
FROM jenkins/inbound-agent:4.10-1-alpine

# Switch to root user for installation
USER root

# Install Docker CLI
RUN apk add --no-cache docker

# Switch back to the Jenkins user
USER jenkins
