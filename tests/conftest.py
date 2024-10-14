import pytest


# def pytest_terminal_summary(terminalreporter, exitstatus, config):
#     if exitstatus == 0:
#         terminalreporter.write_sep("=", "!!!!PASSED")
#     else:
#         terminalreporter.write_sep("=", "FAILED")



# @pytest.hookimpl(tryfirst=True)
# def pytest_sessionfinish(session, exitstatus):
#     if exitstatus == 0:
#         print("PASS :0")
#     else:
#         print("FAIL >:(")
    


# @pytest.hookimpl(tryfirst=True)
# def pytest_runtest_makereport(item, call):
#     if call.when == "call":
#         if call.excinfo is not None:
#             print(f"Test {item.name} failed!!!! with error: {call.excinfo.value}")




