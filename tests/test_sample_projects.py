# -*- coding: utf-8 -*-
import os
from contextlib import contextmanager
from cookiecutter.utils import rmtree


@contextmanager
def temporary_project(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))

def test_envrc(cookies):
    """
    Test if the .envrc file was created successfully
    """

    extra_context = {'project_name': 'environ'}

    with temporary_project(cookies, extra_context=extra_context) as result:
        envrc_file = result.project.join('environ', '.envrc')
        lines = [x.strip() for x in envrc_file.readlines(cr=False)]
        assert 'ENVIRON_SECRET_KEY' in lines
        assert 'ENVIRON_DATABASE_URL' in lines