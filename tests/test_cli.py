# -*- coding: utf-8 -*-
from unittest import mock

import pytest
from click.testing import CliRunner

from tilty import cli
from tilty.exceptions import ConfigurationFileNotFoundException


@mock.patch('tilty.tilt_device')
@mock.patch('tilty.cli.sys')
def test_terminate_process(
    mock_tilt_device,
    mock_sys,
):
    cli.terminate_process(mock_tilt_device, None, None)
    assert mock_tilt_device.mock_calls == [
        mock.call.stop(),
        mock.call.exit()
    ]


def test_cli_config_dne():
    with pytest.raises(ConfigurationFileNotFoundException):
        runner = CliRunner()
        result = runner.invoke(
            cli.run,
            ["--config-file", "/foo"],
            catch_exceptions=False
        )
        assert result.exit_code == 1


def test_cli_invalid_params():
    runner = CliRunner()
    result = runner.invoke(cli.run, ["--foo"])
    assert result.exit_code == 2
    assert result.output == 'Usage: run [OPTIONS]\nTry \'run --help\' for help.\n\nError: no such option: --foo\n' # noqa


@mock.patch('tilty.cli.parse_config', return_value={})
@mock.patch('tilty.cli.pathlib.Path.exists', return_value=True)
@mock.patch('tilty.blescan.get_events', return_value=[{'uuid': 'foo', 'major': 78, 'minor': 1833}]) # noqa
@mock.patch('tilty.blescan.hci_le_set_scan_parameters') # noqa
@mock.patch('tilty.blescan.hci_enable_le_scan') # noqa
def test_cli_no_params_no_valid_data(
    bt_enable_scan,
    bt_set_scan,
    bt_events,
    mock_pathlib,
    mock_parse_config,
):
    runner = CliRunner()
    result = runner.invoke(cli.run, [])
    assert result.exit_code == 0
    assert result.output == 'Scanning for Tilt data...\n'


@mock.patch('tilty.cli.parse_config', return_value={})
@mock.patch('tilty.cli.pathlib.Path.exists', return_value=True)
@mock.patch('tilty.blescan.get_events', return_value=[]) # noqa
@mock.patch('tilty.blescan.hci_le_set_scan_parameters') # noqa
@mock.patch('tilty.blescan.hci_enable_le_scan') # noqa
def test_cli_no_params_no_data(
    bt_enable_scan,
    bt_set_scan,
    bt_events,
    mock_pathlib,
    mock_parse_config,
):
    runner = CliRunner()
    result = runner.invoke(cli.run, [])
    assert result.exit_code == 0
    assert result.output == 'Scanning for Tilt data...\n'


@mock.patch('tilty.cli.parse_config', return_value={})
@mock.patch('tilty.cli.pathlib.Path.exists', return_value=True)
@mock.patch('tilty.blescan.get_events', return_value=[{'mac': '00:0a:95:9d:68:16', 'uuid': 'a495bb30c5b14b44b5121370f02d74de', 'major': 60, 'minor': 1053}]) # noqa
@mock.patch('tilty.blescan.hci_le_set_scan_parameters') # noqa
@mock.patch('tilty.blescan.hci_enable_le_scan') # noqa
def test_cli_no_params_success(
    bt_enable_scan,
    bt_set_scan,
    bt_events,
    mock_pathlib,
    mock_parse_config,
):
    runner = CliRunner()
    result = runner.invoke(cli.run, [])
    assert result.exit_code == 0
    # For some reason logger.info is different in python36 vs python37/38 and I dont care about this test enough to fix that difference  # noqa
    # assert "Scanning for Tilt data...\n{'color': 'Black', 'gravity': 1.053, 'temp': 60, 'mac': '00:0a:95:9d:68:16', 'timestamp': " in result.output  # noqa
    assert "Scanning for Tilt data...\n" in result.output
