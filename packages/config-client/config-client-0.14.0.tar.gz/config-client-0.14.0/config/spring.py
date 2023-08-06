"""Module for retrieve application's config from Spring Cloud Config."""
import os
from distutils.util import strtobool
from functools import wraps
from typing import Any, Callable, Dict, KeysView, Optional, Tuple

from attrs import field, fields_dict, mutable, validators
from glom import glom

from . import http
from .auth import OAuth2
from .core import singleton
from .exceptions import RequestFailedException
from .logger import logger


@mutable
class ConfigClient:
    """Spring Cloud Config Client."""

    address: str = field(
        default=os.getenv("CONFIGSERVER_ADDRESS", "http://localhost:8888"),
        validator=validators.instance_of(str),
    )
    branch: str = field(
        default=os.getenv("BRANCH", "master"),
        validator=validators.instance_of(str),
    )
    app_name: str = field(
        default=os.getenv("APP_NAME", ""),
        validator=validators.instance_of(str),
    )
    profile: str = field(
        default=os.getenv("PROFILE", "development"),
        validator=validators.instance_of(str),
    )
    _url: str = field(
        default="{address}/{branch}/{app_name}-{profile}.json",
        validator=validators.instance_of(str),
        repr=False,
    )
    fail_fast: bool = field(
        default=bool(strtobool(str(os.getenv("CONFIG_FAIL_FAST", True)))),
        validator=validators.instance_of(bool),
        converter=bool,
    )
    oauth2: Optional[OAuth2] = field(
        default=None,
        validator=validators.optional(validators.instance_of(OAuth2)),
    )
    _config: dict = field(
        factory=dict,
        init=False,
        validator=validators.instance_of(dict),
        repr=False,
    )

    @property
    def url(self) -> str:
        url = self._url.format(
            address=self.address,
            branch=self.branch,
            app_name=self.app_name,
            profile=self.profile,
        )
        return self._ensure_request_json(url)

    @url.setter
    def url(self, pattern: str) -> None:
        self._url = pattern

    def _ensure_request_json(self, url: str) -> str:
        """Ensure that the URI to retrieve the configuration will have the .json extension"""
        if not url.endswith(".json"):
            dot_position = url.rfind(".")
            if dot_position > 0:
                url = url.replace(url[dot_position:], ".json")
            else:
                url = f"{url}.json"
            logger.warning(
                "URL suffix adjusted to a supported format. "
                "For more details see: "
                "https://config-client.amenezes.net/docs/1.-overview/#default-values"
            )
        logger.debug(f"Target URL: [address='{url}']")
        return url

    def get_config(self, **kwargs: dict) -> None:
        """Request the configuration from the config server."""
        kwargs = self._configure_oauth2(**kwargs)
        try:
            response = http.get(self.url, **kwargs)
        except Exception as ex:
            logger.error(f"Failed to request: {self.url}")
            logger.error(ex)
            if self.fail_fast:
                logger.info("fail_fast enabled. Terminating process.")
                raise SystemExit(1)
            raise ConnectionError("fail_fast disabled.")
        self._config = response.json()

    def _configure_oauth2(self, **kwargs) -> dict:
        if self.oauth2:
            self.oauth2.configure(**kwargs)
            try:
                kwargs["headers"].update(self.oauth2.authorization_header)
            except KeyError:
                kwargs.update(dict(headers=self.oauth2.authorization_header))
        return kwargs

    def get_file(self, filename: str, **kwargs: dict) -> str:
        """Request a file from the config server."""
        uri = f"{self.address}/{self.app_name}/{self.profile}/{self.branch}/{filename}"
        try:
            response = http.get(uri, **kwargs)
        except Exception:
            raise RequestFailedException(f"Failed to request URI: {uri}")
        return response.text

    def encrypt(
        self,
        value: str,
        path: str = "/encrypt",
        headers: dict = {"Content-Type": "text/plain"},
        **kwargs: dict,
    ) -> str:
        """Request a encryption from a value to the config server."""
        try:
            response = http.post(
                uri=f"{self.address}{path}", data=value, headers=headers, **kwargs
            )
        except Exception:
            raise RequestFailedException(f"Failed to request URI: {self.address}{path}")
        return response.text

    def decrypt(
        self,
        value: str,
        path: str = "/decrypt",
        headers: dict = {"Content-Type": "text/plain"},
        **kwargs: dict,
    ) -> str:
        """Request a decryption from a value to the config server.."""
        try:
            response = http.post(
                uri=f"{self.address}{path}", data=value, headers=headers, **kwargs
            )
        except Exception:
            raise RequestFailedException(f"Failed to request URI: {self.address}{path}")
        return response.text

    @property
    def config(self) -> Dict:
        """Getter from configurations retrieved from ConfigClient."""
        return self._config

    def get(self, key: str, default: Any = "") -> Any:
        return glom(self._config, key, default=default)

    def keys(self) -> KeysView:
        return self._config.keys()

    def get_attribute(self, value: str) -> Any:
        """
        Get attribute from configuration.

        :value value: -- The filter to query on dict.
        :return: The value matches or ''
        """
        logger.warning("get_attribute it's deprecated, please use get() method.")
        return glom(self._config, value, default="")

    def get_keys(self) -> KeysView:
        """List all keys from configuration retrieved."""
        logger.warning("get_keys it's deprecated, please use keys() method.")
        return self._config.keys()


@singleton
def create_config_client(**kwargs) -> ConfigClient:
    """
    Create ConfigClient singleton instance.

    :param address:
    :param app_name:
    :param branch:
    :param fail_fast:
    :param profile:
    :param url:
    :return: ConfigClient instance.
    """
    instance_params, get_config_params = __get_params(**kwargs)
    obj = ConfigClient(**instance_params)
    obj.get_config(**get_config_params)
    return obj


def config_client(**kwargs) -> Callable[[Dict[str, str]], ConfigClient]:
    """ConfigClient decorator.

    Usage:

    @config_client(app_name='test')
    def get_config(config):
        db_user = config.get_attribute('database.user')

    :raises: ConnectionError: If fail_fast enabled.
    :return: ConfigClient instance.
    """
    instance_params, get_config_params = __get_params(**kwargs)

    def wrap_function(function):
        logger.debug(f"caller: [name='{function.__name__}']")

        @wraps(function)
        def enable_config():
            obj = ConfigClient(**instance_params)
            obj.get_config(**get_config_params)
            return function(obj)

        return enable_config

    return wrap_function


def __get_params(**kwargs) -> Tuple[Dict, Dict]:
    instance_params = {}
    get_config_params = {}
    for key, value in kwargs.items():
        if key in fields_dict(ConfigClient).keys():
            instance_params.update({key: value})
        else:
            get_config_params.update({key: value})
    logger.debug(
        f"params: [kwargs={kwargs}, instance={instance_params}, get_config={get_config_params}]"
    )
    return instance_params, get_config_params
