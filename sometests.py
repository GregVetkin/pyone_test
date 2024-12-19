import pyone

from api            import One
from config         import API_URI, ADMIN_NAME


brestadm_auth = ADMIN_NAME+":"+"70057021d19af04aac15dea6bacf1205b3767e794d7b4921428c984ac8314063"


one  = One(pyone.OneServer(API_URI, brestadm_auth))


one.vm.action("terminate-hard", 25)





# from one_cli.group import Group
# group_def_quotas = Group(148).info().DEFAULT_GROUP_QUOTAS
# print(group_def_quotas.DATASTORE_QUOTA)
# print(group_def_quotas.NETWORK_QUOTA)
# print(group_def_quotas.VM_QUOTA)
# print(group_def_quotas.IMAGE_QUOTA)



# import xmlrpc.client
# from one_cli.group._common  import ImageQuotaInfo, NetworkQuotaInfo, DatastoreQuotaInfo, DefaultGroupQuotasInfo, parse_default_group_quotas
# import xml.etree.ElementTree as xmlTree


# image_quota = ImageQuotaInfo(
#         ID= 999,
#         RVMS= 999,
#         RVMS_USED=0,
#     )
# server = xmlrpc.client.ServerProxy(API_URI)
# session_string = brestadm_auth


# response = server.one.groupquota.update(session_string, "")
# print(response[1])
# xml_string = response[1]
# # xml_string = "<TEST>" + xml_string + "</TEST>"
# default_quota_element   = xmlTree.fromstring(xml_string)
# default_quota_info      = parse_default_group_quotas(default_quota_element)
# assert image_quota in default_quota_info.IMAGE_QUOTA


