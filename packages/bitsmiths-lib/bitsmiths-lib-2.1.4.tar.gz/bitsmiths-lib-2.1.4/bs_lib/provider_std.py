# **************************************************************************** #
#                           This file is part of:                              #
#                                BITSMITHS                                     #
#                           https://bitsmiths.co.za                            #
# **************************************************************************** #
#  Copyright (C) 2015 - 2021 Bitsmiths (Pty) Ltd.  All rights reserved.        #
#   * https://bitbucket.org/bitsmiths_za/bitsmiths                             #
#                                                                              #
#  Permission is hereby granted, free of charge, to any person obtaining a     #
#  copy of this software and associated documentation files (the "Software"),  #
#  to deal in the Software without restriction, including without limitation   #
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,    #
#  and/or sell copies of the Software, and to permit persons to whom the       #
#  Software is furnished to do so, subject to the following conditions:        #
#                                                                              #
#  The above copyright notice and this permission notice shall be included in  #
#  all copies or substantial portions of the Software.                         #
#                                                                              #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL     #
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  #
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
#  DEALINGS IN THE SOFTWARE.                                                   #
# **************************************************************************** #

import os
import os.path
import logging

import mettle

from . import IProvider
from . import Pod, PodAsync
from . import common


class ProviderStd(IProvider):
    """
    Standard provider object.
    """

    def new_config(self, options: dict = None) -> dict:
        """
        Overload.
        """
        if not options:
            raise Exception('Cannot create a new config with no options.')

        config_path = options.get('config-file')

        if not config_path:
            raise Exception('[config-file] key not found when initializing config.')

        return common.read_config_dict_from_file(os.path.expandvars(config_path))


    def new_db_connector(self, cfg: dict = None, options: dict = None) -> "mettle.db.IConnect":
        """
        Overload.
        """
        raise NotImplementedError('new_db_connector')


    def new_logger(self, cfg: dict = None, options: dict = None) -> "logging.Logger":
        """
        Overload.
        """
        import sys

        logger = common.get_logger(options)

        logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler(sys.stdout)
        fmt = logging.Formatter('[%(asctime)s.%(msecs)03d] [%(process)d] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        stream_handler.setFormatter(fmt)

        stream_handler.setLevel(logging.DEBUG)
        logger.addHandler(stream_handler)

        return common.get_logger(options)


    def new_pod(self,
                cfg: dict = None,
                logger: "logging.Logger" = None,
                dbcon: "mettle.db.IConnect" = None,
                options: dict = None) -> "Pod|PodAsync":
        """
        Overload.
        """
        return Pod(cfg, dbcon, logger)
