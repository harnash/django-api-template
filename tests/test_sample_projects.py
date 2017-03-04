# -*- coding: utf-8 -*-
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
        envrc_file = result.project.join('.envrc')
        lines = [x.strip() for x in envrc_file.readlines(cr=False)]
        assert 'export ENVIRON_SECRET_KEY=FOR DEV ONLY - CHANGE ME' in lines
        assert 'export ENVIRON_DATABASE_URL=postgresql://path_to_database' in lines