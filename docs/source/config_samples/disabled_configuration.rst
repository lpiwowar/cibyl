::

  environments:
    production:
      production_jenkins_1:
        system_type: jenkins
        sources:
          jenkins_api_prod:
            driver: jenkins
            url: https://...
            username: user
            token: xyz
      production_jenkins_2:
        enabled: false        # Makes 'production_jenkins_2' system disabled
        system_type: jenkins
        sources:
          jenkins_api_prod:
            driver: jenkins
            url: https://...
            username: user
            token: xyz
    staging:
      enabled: false          # Makes 'staging' environment disabled
      staging_jenkins:
        system_type: jenkins
        sources:
          jenkins_api_staging:
            driver: jenkins
            url: https://...
            username: user
            token: xyz
