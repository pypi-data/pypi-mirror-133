from hdsr_pygithub import GithubDirDownloader
from hdsr_wis_config_reader import constants
from hdsr_wis_config_reader.location_sets.collection import LocationSetCollection
from hdsr_wis_config_reader.readers.config_reader import FewsConfigReader
from pathlib import Path

import datetime
import pytest


@pytest.fixture(scope="session")  # 'session', so we cache the fixture for all tests (instead of default 'function')
def fews_config_local() -> FewsConfigReader:
    # we use config saved in this repo (=static), instead of downloading from repo 'wis_config'
    assert constants.WIS_CONFIG_TEST_DIR.is_dir()
    fews_config = FewsConfigReader(path=constants.WIS_CONFIG_TEST_DIR)
    return fews_config


@pytest.fixture(scope="session")  # 'session', so we cache the fixture for all tests (instead of default 'function')
def fews_config_github() -> FewsConfigReader:
    target_dir = Path("FEWS/Config")
    github_downloader = GithubDirDownloader(
        target_dir=target_dir,
        only_these_extensions=[".csv", ".xml"],
        allowed_period_no_updates=datetime.timedelta(weeks=52 * 2),
        repo_name=constants.GITHUB_WIS_CONFIG_REPO_NAME,
        branch_name=constants.GITHUB_WIS_CONFIG_BRANCH_NAME,
        repo_organisation=constants.GITHUB_ORGANISATION_NAME,
    )
    download_dir = github_downloader.download_files(use_tmp_dir=True)
    config_dir = download_dir / target_dir
    fews_config = FewsConfigReader(path=config_dir)
    return fews_config


@pytest.fixture
def loc_sets() -> LocationSetCollection:
    fews_config = FewsConfigReader(path=constants.WIS_CONFIG_TEST_DIR)
    loc_sets = LocationSetCollection(fews_config=fews_config)
    return loc_sets


WIS_CONFIG_TEST_DIR = constants.BASE_DIR / "tests" / "data" / "input" / "config_wis60prd_202002"


def test_test_dir_exists():
    assert WIS_CONFIG_TEST_DIR.is_dir()
