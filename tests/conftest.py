# # pylint: skip-file
#
# import os
# import subprocess
#
# import pytest
#
#
# @pytest.fixture(scope='session', autouse=True)
# def start_icl():
#     if os.environ.get('HAS_HARDWARE') == 'true':
#         try:
#             result = subprocess.run(['C:\\Program Files\\Horiba Scientific\\SDK\\icl.exe'], check=True,
#                                     capture_output=True, text=True, timeout=10)
#             print(result.stdout)
#             print(result.stderr)
#         except subprocess.CalledProcessError as e:
#             print('The subprocess encountered an error:', e)
