::

  # Minimal configuration

  environments:                 # List of CI/CD environments
    production:                 # An environment called "production"
      production_jenkins:       # A single system called "production_jenkins"
        system_type: jenkins    # The type of the system (jenkins or zuul)
        sources:                # List of sources belong to "production_jenkins" system
          jenkins_api:          # The name of the source which belongs to "production_jenkins" system
            driver: jenkins     # The driver the source will be using
            url: https://...    # The URL of the system
            username: user      # The username to use for the authentication
            token: xyz          # The token to use for the authentication
            cert: False         # Disable/Enable certificates to use for the authentication

  plugins:                      # (Optional) Specify the plugins to enable when running Cibyl
    - openstack                 # OpenStack adds its own product related models and arguments
