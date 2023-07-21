import pytest
from pytest_mock import MockerFixture
import pytest_asyncio
from main import get_file_data, get_repo_data, list_files

@pytest.mark.asyncio
async def test_get_file_data(mocker: MockerFixture):
    # Mock the GitHub API response
    mocker.patch('main.get_file_data', return_value='mocked response')

    # Call the function with test data
    response = await get_file_data('test_owner', 'test_repo', 'test_file_path')

    # Assert that the function returns the mocked response
    assert response == 'mocked response'

@pytest.mark.asyncio
async def test_get_repo_data(mocker: MockerFixture):
    # Mock the GitHub API response
    mocker.patch('main.get_repo_data', return_value='mocked response')

    # Call the function with test data
    response = await get_repo_data('test_username', 'test_repo_name')

    # Assert that the function returns the mocked response
    assert response == 'mocked response'

@pytest.mark.asyncio
async def test_list_files(mocker: MockerFixture):
    # Mock the GitHub API response
    mocker.patch('main.list_files', return_value='mocked response')

    # Call the function with test data
    response = await list_files('test_owner', 'test_repo', 'test_path')

    # Assert that the function returns the mocked response
    assert response == 'mocked response'