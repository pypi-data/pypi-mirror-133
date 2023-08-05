from swagger_gen.lib.utils import element_at
from swagger_gen.lib.exceptions import NullReferenceException
from swagger_gen.lib.logger import get_logger
from swagger_gen.lib.constants import (
    DependencyInfo,
    Method,
    SwaggerRoute,
)
from werkzeug.exceptions import abort
from flask import Flask, Response
import importlib.resources
import pickle

logger = get_logger()

mimetype_mapping = {
    'css': 'text/css',
    'js': 'text/javascript'
}


class DependencyProvider:
    def __init__(self, app: Flask, url: str):
        if not app:
            raise NullReferenceException('app')
        if not url:
            raise NullReferenceException('url')

        self._app = app
        self._url = url
        self._resources = self._load_resources()

    def _load_resources(self) -> dict:
        '''
        The Swagger dependencies (html, css, js) are stored in a pickle
        and loaded into memory.  This wasy we can keep the package light
        and clean and we don't have to deal with handling static files.
        There's a considerable performance benefit here from storing and
        serving these files from memory as well.
        '''

        try:
            # Loading the pickled Swagger UI JS, CSS and HTML files from
            # the module source directory
            data = importlib.resources.open_binary(
                DependencyInfo.PKG_RESOURCE_MODULE,
                DependencyInfo.PKG_SWAGGER)

            return pickle.load(data)
        except Exception as ex:
            logger.info(f'failed to load swagger dependencies')
            logger.info(f'error: {str(ex)}')

    def _get_resource_type(self, resource_name: str) -> str:
        '''
        Get the extension of the Swagger resource type (ex. css, json, 
        etc)

        params:
            resource_name   :   resource filename

        returns:
            the resource file extension
        '''

        if not resource_name:
            raise NullReferenceException('resource_name')

        return element_at(resource_name.split('.'), -1)

    def bind_routes(self) -> None:
        '''
        Bind all required Swagger dependency routes.  The  dependencies 
        defined in swagger.pkl will get served from memory via the rules 
        defined
        '''

        def get_resource(resource_name: str):
            resource = self._resources.get(resource_name)
            if not resource:
                abort(404)

            mimetype = mimetype_mapping.get(
                self._get_resource_type(resource_name))

            if mimetype:
                return Response(
                    resource,
                    mimetype=mimetype)
            return resource

        logger.info(
            f'binding base dependency route: {SwaggerRoute.SWAG_DEPS_BASE}')

        self._app.add_url_rule(
            rule=SwaggerRoute.SWAG_DEPS_BASE,
            view_func=get_resource,
            methods=[Method.GET])

        def get_index():
            return Response(
                self._resources.get(DependencyInfo.PKG_SWAG_UI))

        # Bind the Swagger UI index at the default route '/swagger' or
        # the optional route specified in the main class constructor
        index_path = self._url or SwaggerRoute.SWAG_INDEX_DEFAULT

        logger.info(
            f'binding index route: {index_path}')

        self._app.add_url_rule(
            rule=index_path,
            view_func=get_index,
            methods=[Method.GET])
