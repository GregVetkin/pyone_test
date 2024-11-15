import pyone

from api            import One
from config         import ADMIN_NAME, API_URI
from utils          import get_user_auth


one  = One(pyone.OneServer(API_URI, get_user_auth(ADMIN_NAME)))
