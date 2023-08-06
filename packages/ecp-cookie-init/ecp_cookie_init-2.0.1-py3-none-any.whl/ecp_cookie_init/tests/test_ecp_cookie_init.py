# -*- coding: utf-8 -*-
# Copyright 2020 Cardiff University
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

"""Tests for ecp-cookie-init
"""

import os.path
import tempfile
from unittest import mock

import pytest

from ciecplib import __version__ as CIECPLIB_VERSION

from .. import (
    __version__ as ECP_COOKIE_INIT_VERSION,
    CUSTOM_IDPS,
    DEFAULT_COOKIE_FILE,
    ecp_cookie_init,
)

ECP_CURL = "ecp_cookie_init.ecp_curl"
ECP_GET_COOKIE = "ecp_cookie_init.ecp_get_cookie"
USERNAME = "marie.curie"


def dummy_output(*args, **kwargs):
    print("TEST")


@pytest.mark.parametrize("arg", (
    "--kerberos",
    "--debug",
))
@mock.patch(ECP_CURL)
def test_ecp_cookie_init_args(ecp_curl, arg):
    ecp_cookie_init(["idp", "target", "user", arg])
    assert arg in ecp_curl.call_args[0][0]


@mock.patch(ECP_GET_COOKIE)
def test_ecp_cookie_init_destroy(ecp_get_cookie):
    ecp_cookie_init(["idp", "target", "user", "--destroy"])
    assert "--destroy" in ecp_get_cookie.call_args[0][0]


def test_ecp_cookie_init_version(capsys):
    """Check that `--version` does what it is supposed to
    """
    with pytest.raises(SystemExit):
        ecp_cookie_init(["--version"])
    assert capsys.readouterr()[0].rstrip() == (
        "ecp-cookie-init version {}\n"
        "ciecplib version {}".format(
            ECP_COOKIE_INIT_VERSION,
            CIECPLIB_VERSION,
        )
    )


@mock.patch(ECP_CURL, side_effect=dummy_output)
def test_ecp_cookie_init_output_file(_, capsys):
    """Check that `--output` does what it is supposed to
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpfile = os.path.join(tmpdir, "tmpfile")
        ecp_cookie_init(["idp", "target", "user", "--output", tmpfile])
        with open(tmpfile, "r") as tmp:
            assert tmp.read().strip() == "TEST"


@mock.patch(ECP_CURL, side_effect=dummy_output)
def test_ecp_cookie_init_no_output(_, capsys):
    """Check that `--no-output` does what it is supposed to
    """
    ecp_cookie_init(["idp", "target", "user", "--no-output"])
    assert not capsys.readouterr()[0].rstrip()  # no output


@mock.patch(ECP_CURL)
def test_ecp_cookie_init_positional_arguments(ecp_curl, capsys):
    """Check that positional arguments are handled properly
    """
    # no IdP/login without --kerberos is an error
    with pytest.raises(SystemExit):
        ecp_cookie_init(["target"])
    assert "login" in capsys.readouterr()[1]

    ecp_curl.reset_mock()

    # no username with --kerberos is fine
    ecp_cookie_init(["target", "--kerberos"])
    assert "--kerberos" in ecp_curl.call_args[0][0]

    ecp_curl.reset_mock()

    # IdP_tag and login should be passed along as options
    ecp_cookie_init(["idp", "target", "user"])
    ecp_curl.assert_called_once_with([
        "target",
        "--username", "user",
        "--cookiefile", DEFAULT_COOKIE_FILE,
        "--store-session-cookies",
        "--identity-provider", "idp",
    ])


@mock.patch(ECP_CURL)
def test_ecp_cookie_init_idp_hosts(ecp_curl):
    """Check that --idp-host is handled properly
    """
    # make sure that by default IdP_tag gets passed along properly
    ecp_cookie_init(["idp", "target", "user"])
    ecp_curl.assert_called_once_with([
        "target",
        "--username", "user",
        "--cookiefile", DEFAULT_COOKIE_FILE,
        "--store-session-cookies",
        "--identity-provider", "idp",
    ])

    ecp_curl.reset_mock()

    # but if the user gives --idp-host that takes precedence
    ecp_cookie_init(["idp", "target", "user", "-i", "different_idp"])
    ecp_curl.assert_called_once_with([
        "target",
        "--username", "user",
        "--cookiefile", DEFAULT_COOKIE_FILE,
        "--store-session-cookies",
        "--identity-provider", "different_idp",
    ])


@mock.patch(ECP_CURL, side_effect=(ValueError('soft failure'), None))
def test_ecp_cookie_init_idp_hosts_fail_pass(ecp_curl):
    # make sure that the failure is emitted as a warning
    with pytest.warns(UserWarning) as record:
        ecp_cookie_init(["LIGO.ORG", "target", "user"])
    assert len(record) == 1
    assert str(record[0].message) == "Caught ValueError: soft failure"

    # but that the second IdP is called and passes
    assert ecp_curl.call_count == 2
    for idp in CUSTOM_IDPS["LIGO.ORG"]:
        ecp_curl.assert_any_call([
            "target",
            "--username", "user",
            "--cookiefile", DEFAULT_COOKIE_FILE,
            "--store-session-cookies",
            "--identity-provider", idp,
        ])


@mock.patch(
    ECP_CURL,
    side_effect=(ValueError('soft failure'), ValueError('hard failure')),
)
def test_ecp_cookie_init_idp_hosts_fail_fail(ecp_curl):
    # make sure that the soft failure is emitted as a warning
    # and that the hard failure is emitted as an exception
    with pytest.raises(ValueError) as exc, pytest.warns(UserWarning) as record:
        ecp_cookie_init(["LIGO.ORG", "target", "user"])
    assert ecp_curl.call_count == 2
    assert len(record) == 1
    assert str(record[0].message) == "Caught ValueError: soft failure"
    assert str(exc.value) == "hard failure"
