::

  environments:                 # List of CI/CD environments
    production:                 # An environment called "production"
      production_zuul           # A single system called "production_jenkins"
        system_type: zuul       # The type of the system
        sources:                # List of sources belong to "production_jenkins" system
          zuul_api:             # The name of the source which belongs to "production_zuul" system
            driver: zuul.d      # The driver the source will be using
            remote: True        # Query GitHub API instead of querying local repos
            username: user      # Required only when 'remote: True'
            token: xyz          # Required only when 'remote: True'
            repos:              # The repos to query using GitHub API
              - url: 'http://zuul_defitions_repo.git'
              - url: 'http://zuul_defitions_repo1.git'
