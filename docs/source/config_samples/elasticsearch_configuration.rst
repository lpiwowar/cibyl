::

  environments:                    # List of CI/CD environments
    production:                    # An environment called "production"
      production_jenkins           # A single system called "production_jenkins"
        system_type: jenkins       # The type of the system (jenkins or zuul)
        sources:                   # List of sources belong to "production_jenkins" system
          es:                      # The name of the source which belongs to "production_jenkins" system
            driver: elasticsearch  # The driver the source will be using
            url: https://...       # The URL of the source
