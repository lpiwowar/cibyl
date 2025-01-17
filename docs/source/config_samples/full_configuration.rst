::

  # Full Configuration Example

  environments:                 # List of CI/CD environments

    production:                 # An environment called "production"

      production_jenkins_1:     # A single system called "production_jenkins_1" belongs to "production" environment
        system_type: jenkins    # The type of the system (jenkins or zuul)
        sources:                # List of sources belong to "production_jenkins" system

          jenkins1_api:       # The name of the source which belongs to "production_jenkins_1" system
            driver: jenkins   # The driver the source will be using
            url: https://...  # The URL of the system
            username: user    # The username to use for the authentication
            token: xyz        # The token to use for the authentication
            cert: False       # Disable/Enable certificates to use for the authentication

          job_definitions:    # Another source that belongs to the same system called "production_jenkins_1"
            driver: jjb
            repos:
              - url: https://job_definitions_repo.git

      production_jenkins_2:     # Another system belongs to the "production" environment
        system_type: jenkins
        sources:

          jenkins2_api:
            driver: jenkins
            url: https://...
            username: user
            token: xyz
            cert: False

      production_zuul
        system_type: zuul
        sources:

          zuul_api:
            driver: zuul
            url: https://...

    staging:                    # Another environment called "staging"

      staging_jenkins:
        system_type: jenkins
        sources:

          staging_jenkins_api:
            driver: jenkins
            url: https://...
            username: user
            token: xyz
