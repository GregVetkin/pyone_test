from api                import One
from utils.commands     import run_command_via_ssh
from utils.connection   import local_admin_ssh_conn



def test_get_version(one: One):
    version_by_api  = one.system.version()
    version_by_file = run_command_via_ssh(local_admin_ssh_conn, "cat /var/lib/one/remotes/VERSION")
    assert version_by_api == version_by_file