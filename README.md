## FastService

Ready-to-go micro-service template based on [FastAPI](https://github.com/tiangolo/fastapi)

Just set configs, add endpoints and deploy using docker

##

### Local deployment for development

Deploy FastService in local development environment using docker-compose in just a few steps:

1. Modify environment configs in local_config directory as required.
2. Start DB and other external services as required.
3. Build service using `sudo docker-compose build`.
4. Start service using `sudo docker-compose up`.
5. Add test cases for your endpoints in `app/app/tests/test_api.py`.
6. Start adding API endpoints in `app/app/src/public_api.py` and `app/app/src/private_api.py`.
7. Service automatically refreshes for any changes made in the code in the development environment.

`Dockerfile` and `docker-compose.yml` are used as configuration files for local deployment.

##

### Production deployment

`Dockerfile_Prod` and `fastservice_stack.yml` are used as configuration files for production deployment.

1. A sample CI/CD config file for gitlab `.gitlab-ci.yml` is provided. Replace with configuration of CI/CD provider of your choice.
2. Add any service prestart script in `app/prestart.sh` as required.
3. Create configs and secrets for your service in your deployment environment.
4. Push and deploy to your environment.

##

### Some features and considerations of FastService

- **Authentication and Authorization** 
  - Authentication and authorization modules here use Auth0. Make relevent changes for using any other auth service.
  - All auth related code are in `app/app/dependency/authentication.py`
  - `requires_auth()` function is used for validating access token for every request coming to all private endpoints.
  - `requires_scope()` and `requires_permission()` functions are used to check authorization for protected endpoints. Their usage in given as sample endpoints in `app/app/src/private_api.py`

- **Private API endpoints** - Any endpoints defined in `app/app/src/private_api.py` using `@privateAPI` decorator is accessible only with a valid access token in the request header

- **Public API endpoints** - Any endpoints defined in `app/app/src/public_api.py` using `@publicAPI` decorator is accessible without any authentication

- **Context** - Context available throughout the request lifecycle along with a request id generated at very start of an incoming request

- **User id** - User id is automatically extracted from access token and added to context for private API endpoints

- **Logging** - Two log cofiguration files `app\app\dependency\app_logger\log_config_file.json` and `app\app\dependency\app_logger\log_config_stdout.json` are provided to configure logging to rotating file and stdout respectively. Select the logging configuration to use using `LOG_TYPE` config.

- **DB Connection** - Database connection is provided using [encode/databases](https://github.com/encode/databases). Sample connection is given in `app/app/src/public_api.py`

- **Test Framework** - Test are defined using pytest. Sample test cases present in `app/app/tests/test_api.py`

- **Healthcheck** - A heartbeat endpoint is used for checking health of service instance.

- **Access token for M2M calls** - To retrieve access token for M2M calls to private endpoints of other services use the `get_access_token()` function in `app/app/dependency/access_token.py`

##

### References

- [FastAPI](https://github.com/tiangolo/fastapi)
- [Starlette](https://github.com/encode/starlette)
- [Pydantic](https://github.com/samuelcolvin/pydantic/)
- [Starlette-Context](https://github.com/tomwojcik/starlette-context)
- [Python-Jose](https://github.com/mpdavis/python-jose)
- [Python-Dotenv](https://github.com/theskumar/python-dotenv)
- [Requests](https://github.com/psf/requests)
- [Databases](https://github.com/encode/databases)
- [Asyncpg](https://github.com/MagicStack/asyncpg)