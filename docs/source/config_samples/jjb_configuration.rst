::

  environments:                    # List of CI/CD environments
    production:                    # An environment called "production"
      production_jenkins           # A single system called "production_jenkins"
        system_type: jenkins       # The type of the system (jenkins or zuul)
        sources:                   # List of sources belong to "production_jenkins" system
          jjb:                     # The name of the source which belongs to "production_jenkins" system
            driver: jjb            # The driver the source will be using
            repos:                 # List of repositories where the job definitions are located
                - url: 'https://jjb_repo_example.git'
