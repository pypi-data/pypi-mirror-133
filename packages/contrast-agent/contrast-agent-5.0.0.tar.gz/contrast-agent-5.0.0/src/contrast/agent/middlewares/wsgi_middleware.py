# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

# TODO: PYT-1213 this import will eventually be deprecated
from contrast.wsgi.middleware import WSGIMiddleware  # pylint: disable=unused-import

WSGIMiddleware.MIDDLEWARE_IMPORT_DEPRECATED = True
