# -*- coding: utf-8 -*-
from unittest import mock

from click.testing import CliRunner

from tilty import cli


def test_cli_invalid_params():
    runner = CliRunner()
    result = runner.invoke(cli.run, ["--foo"])
    assert result.exit_code == 2
    assert result.output == 'Usage: run [OPTIONS]\nTry "run --help" for help.\n\nError: no such option: --foo\n' # noqa


@mock.patch('tilty.blescan.parse_events', return_value=[{'uuid': 'foo', 'major': 2, 'minor': 1}]) # noqa
@mock.patch('tilty.blescan.hci_le_set_scan_parameters') # noqa
@mock.patch('tilty.blescan.hci_enable_le_scan') # noqa
def test_cli_no_params_no_valid_data(
    bt_enable_scan,
    bt_set_scan,
    bt_events,
):
    runner = CliRunner()
    result = runner.invoke(cli.run, [])
    assert result.exit_code == 0
    assert result.output == 'Scanning for Tilt data...\n' # noqa


@mock.patch('tilty.blescan.parse_events', return_value=[]) # noqa
@mock.patch('tilty.blescan.hci_le_set_scan_parameters') # noqa
@mock.patch('tilty.blescan.hci_enable_le_scan') # noqa
def test_cli_no_params_no_data(
    bt_enable_scan,
    bt_set_scan,
    bt_events,
):
    runner = CliRunner()
    result = runner.invoke(cli.run, [])
    assert result.exit_code == 0
    assert result.output == 'Scanning for Tilt data...\n' # noqa

@mock.patch('tilty.blescan.parse_events', return_value=[{'uuid': 'a495bb30c5b14b44b5121370f02d74de', 'major': 2, 'minor': 1}]) # noqa
@mock.patch('tilty.tilt_device.datetime') # noqa
@mock.patch('tilty.blescan.hci_le_set_scan_parameters') # noqa
@mock.patch('tilty.blescan.hci_enable_le_scan') # noqa
def test_cli_no_params_success(
    bt_enable_scan,
    bt_set_scan,
    bt_events,
    dt,
):
    runner = CliRunner()
    result = runner.invoke(cli.run, [])
    assert result.exit_code == 0
    assert "Scanning for Tilt data...\n{'color': 'Black', 'gravity': 1, 'temp': 2, 'timestamp'" in result.output# noqa
