from api.one        import OneServer
from pyone.bindings import VM_POOLSub, MONITORING_DATASub



class OneVmpool:
    def __init__(self, one_api: OneServer) -> None:
        self._one_vmpool = one_api.vmpool

    def info(self, filter_flag: int = -2, start_id: int = -1, end_id: int = -1, vm_state_filter: int = -2, key_value_filter: str = "") -> VM_POOLSub:
        """Retrieves information for all or part of the VMs in the pool"""
        return self._one_vmpool.info(filter_flag, start_id, end_id, vm_state_filter, key_value_filter)

    def infoextended(self, filter_flag: int = -2, start_id: int = -1, end_id: int = -1, vm_state_filter: int = -2, key_value_filter: str = "") -> VM_POOLSub:
        """Retrieves information for all or part of the VMs in the pool"""
        return self._one_vmpool.infoextended(filter_flag, start_id, end_id, vm_state_filter, key_value_filter)
    
    def infoset(self, vm_set: str, extended: bool = False) -> VM_POOLSub:
        """Retrieves information for a specific set of VMs"""
        return self._one_vmpool.infoset(vm_set, extended)
    
    def monitoring(self, filter_flag: int = -2, last_seconds: int = -1) -> MONITORING_DATASub:
        """Returns all the virtual machine monitoring records"""
        return self._one_vmpool.monitoring(filter_flag, last_seconds)
    
    def accounting(self, filter_flag: int = -2, start_id: int = -1, end_id: int = -1) -> str:
        """Returns the virtual machine history records"""
        return self._one_vmpool.accounting(filter_flag, start_id, end_id)
    
    def showback(self, filter_flag: int = -2, first_month: int = -1, first_year: int = -1, last_month: int = -1, last_year: int = -1) -> str:
        """Returns the virtual machine showback records"""
        return self._one_vmpool.showback(filter_flag, first_month, first_year, last_month, last_year)

    def calculateshowback(self, first_month: int = -1, first_year: int = -1, last_month: int = -1, last_year: int = -1) -> str:
        """Processes all the history records, and stores the monthly cost for each VM"""
        return self._one_vmpool.calculateshowback(first_month, first_year, last_month, last_year)