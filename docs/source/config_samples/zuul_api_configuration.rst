::

  environments:                 # List of CI/CD environments
    production:                 # An environment called "production"
      production_zuul           # A single system called "production_jenkins"
        system_type: zuul       # The type of the system
        sources:                # List of sources belong to "production_jenkins" system
          zuul_api:             # The name of the source which belongs to "production_zuul" system
            driver: zuul        # The driver the source will be using
            url: https://...    # The URL of the system
            tenants:            # List of tenants to use. This section is optional
                - default       # and allows the user to restrict which zuul
                - local         # tenants will be queried can be useful
