# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.model import TeaModel
from typing import Dict, List


class ChangeAccountPasswordRequest(TeaModel):
    def __init__(
        self,
        account_name: str = None,
        drds_instance_id: str = None,
        password: str = None,
    ):
        self.account_name = account_name
        self.drds_instance_id = drds_instance_id
        self.password = password

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_name is not None:
            result['AccountName'] = self.account_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.password is not None:
            result['Password'] = self.password
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountName') is not None:
            self.account_name = m.get('AccountName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('Password') is not None:
            self.password = m.get('Password')
        return self


class ChangeAccountPasswordResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ChangeAccountPasswordResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ChangeAccountPasswordResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ChangeAccountPasswordResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ChangeInstanceAzoneRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
        drds_region_id: str = None,
        origin_azone_id: str = None,
        target_azone_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id
        self.drds_region_id = drds_region_id
        self.origin_azone_id = origin_azone_id
        self.target_azone_id = target_azone_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.drds_region_id is not None:
            result['DrdsRegionId'] = self.drds_region_id
        if self.origin_azone_id is not None:
            result['OriginAzoneId'] = self.origin_azone_id
        if self.target_azone_id is not None:
            result['TargetAzoneId'] = self.target_azone_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('DrdsRegionId') is not None:
            self.drds_region_id = m.get('DrdsRegionId')
        if m.get('OriginAzoneId') is not None:
            self.origin_azone_id = m.get('OriginAzoneId')
        if m.get('TargetAzoneId') is not None:
            self.target_azone_id = m.get('TargetAzoneId')
        return self


class ChangeInstanceAzoneResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ChangeInstanceAzoneResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ChangeInstanceAzoneResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ChangeInstanceAzoneResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CheckDrdsDbNameRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class CheckDrdsDbNameResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: bool = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.result = result
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.result is not None:
            result['Result'] = self.result
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CheckDrdsDbNameResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CheckDrdsDbNameResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CheckDrdsDbNameResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CheckExpandStatusRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class CheckExpandStatusResponseBodyData(TeaModel):
    def __init__(
        self,
        is_active: bool = None,
        msg: str = None,
    ):
        self.is_active = is_active
        self.msg = msg

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.is_active is not None:
            result['IsActive'] = self.is_active
        if self.msg is not None:
            result['Msg'] = self.msg
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('IsActive') is not None:
            self.is_active = m.get('IsActive')
        if m.get('Msg') is not None:
            self.msg = m.get('Msg')
        return self


class CheckExpandStatusResponseBody(TeaModel):
    def __init__(
        self,
        data: CheckExpandStatusResponseBodyData = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = CheckExpandStatusResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CheckExpandStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CheckExpandStatusResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CheckExpandStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CheckSqlAuditEnableStatusRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class CheckSqlAuditEnableStatusResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        status: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.status = status
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.status is not None:
            result['Status'] = self.status
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CheckSqlAuditEnableStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CheckSqlAuditEnableStatusResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CheckSqlAuditEnableStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateDrdsDBRequestInstDbName(TeaModel):
    def __init__(
        self,
        db_instance_id: str = None,
        shard_db_name: List[str] = None,
    ):
        self.db_instance_id = db_instance_id
        self.shard_db_name = shard_db_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_instance_id is not None:
            result['DbInstanceId'] = self.db_instance_id
        if self.shard_db_name is not None:
            result['ShardDbName'] = self.shard_db_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbInstanceId') is not None:
            self.db_instance_id = m.get('DbInstanceId')
        if m.get('ShardDbName') is not None:
            self.shard_db_name = m.get('ShardDbName')
        return self


class CreateDrdsDBRequestRdsSuperAccount(TeaModel):
    def __init__(
        self,
        account_name: str = None,
        db_instance_id: str = None,
        password: str = None,
    ):
        self.account_name = account_name
        self.db_instance_id = db_instance_id
        self.password = password

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_name is not None:
            result['AccountName'] = self.account_name
        if self.db_instance_id is not None:
            result['DbInstanceId'] = self.db_instance_id
        if self.password is not None:
            result['Password'] = self.password
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountName') is not None:
            self.account_name = m.get('AccountName')
        if m.get('DbInstanceId') is not None:
            self.db_instance_id = m.get('DbInstanceId')
        if m.get('Password') is not None:
            self.password = m.get('Password')
        return self


class CreateDrdsDBRequest(TeaModel):
    def __init__(
        self,
        account_name: str = None,
        db_inst_type: str = None,
        db_instance_is_creating: bool = None,
        db_name: str = None,
        drds_instance_id: str = None,
        encode: str = None,
        inst_db_name: List[CreateDrdsDBRequestInstDbName] = None,
        password: str = None,
        rds_instance: List[str] = None,
        rds_super_account: List[CreateDrdsDBRequestRdsSuperAccount] = None,
        type: str = None,
    ):
        self.account_name = account_name
        self.db_inst_type = db_inst_type
        self.db_instance_is_creating = db_instance_is_creating
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.encode = encode
        self.inst_db_name = inst_db_name
        self.password = password
        self.rds_instance = rds_instance
        self.rds_super_account = rds_super_account
        self.type = type

    def validate(self):
        if self.inst_db_name:
            for k in self.inst_db_name:
                if k:
                    k.validate()
        if self.rds_super_account:
            for k in self.rds_super_account:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_name is not None:
            result['AccountName'] = self.account_name
        if self.db_inst_type is not None:
            result['DbInstType'] = self.db_inst_type
        if self.db_instance_is_creating is not None:
            result['DbInstanceIsCreating'] = self.db_instance_is_creating
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.encode is not None:
            result['Encode'] = self.encode
        result['InstDbName'] = []
        if self.inst_db_name is not None:
            for k in self.inst_db_name:
                result['InstDbName'].append(k.to_map() if k else None)
        if self.password is not None:
            result['Password'] = self.password
        if self.rds_instance is not None:
            result['RdsInstance'] = self.rds_instance
        result['RdsSuperAccount'] = []
        if self.rds_super_account is not None:
            for k in self.rds_super_account:
                result['RdsSuperAccount'].append(k.to_map() if k else None)
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountName') is not None:
            self.account_name = m.get('AccountName')
        if m.get('DbInstType') is not None:
            self.db_inst_type = m.get('DbInstType')
        if m.get('DbInstanceIsCreating') is not None:
            self.db_instance_is_creating = m.get('DbInstanceIsCreating')
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('Encode') is not None:
            self.encode = m.get('Encode')
        self.inst_db_name = []
        if m.get('InstDbName') is not None:
            for k in m.get('InstDbName'):
                temp_model = CreateDrdsDBRequestInstDbName()
                self.inst_db_name.append(temp_model.from_map(k))
        if m.get('Password') is not None:
            self.password = m.get('Password')
        if m.get('RdsInstance') is not None:
            self.rds_instance = m.get('RdsInstance')
        self.rds_super_account = []
        if m.get('RdsSuperAccount') is not None:
            for k in m.get('RdsSuperAccount'):
                temp_model = CreateDrdsDBRequestRdsSuperAccount()
                self.rds_super_account.append(temp_model.from_map(k))
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class CreateDrdsDBResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateDrdsDBResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateDrdsDBResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateDrdsDBResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateDrdsInstanceRequest(TeaModel):
    def __init__(
        self,
        client_token: str = None,
        description: str = None,
        duration: int = None,
        instance_series: str = None,
        is_auto_renew: bool = None,
        master_inst_id: str = None,
        my_sqlversion: int = None,
        pay_type: str = None,
        pricing_cycle: str = None,
        quantity: int = None,
        region_id: str = None,
        resource_group_id: str = None,
        specification: str = None,
        type: str = None,
        vpc_id: str = None,
        vswitch_id: str = None,
        zone_id: str = None,
        is_ha: bool = None,
    ):
        self.client_token = client_token
        self.description = description
        self.duration = duration
        self.instance_series = instance_series
        self.is_auto_renew = is_auto_renew
        self.master_inst_id = master_inst_id
        self.my_sqlversion = my_sqlversion
        self.pay_type = pay_type
        self.pricing_cycle = pricing_cycle
        self.quantity = quantity
        self.region_id = region_id
        self.resource_group_id = resource_group_id
        self.specification = specification
        self.type = type
        self.vpc_id = vpc_id
        self.vswitch_id = vswitch_id
        self.zone_id = zone_id
        self.is_ha = is_ha

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.client_token is not None:
            result['ClientToken'] = self.client_token
        if self.description is not None:
            result['Description'] = self.description
        if self.duration is not None:
            result['Duration'] = self.duration
        if self.instance_series is not None:
            result['InstanceSeries'] = self.instance_series
        if self.is_auto_renew is not None:
            result['IsAutoRenew'] = self.is_auto_renew
        if self.master_inst_id is not None:
            result['MasterInstId'] = self.master_inst_id
        if self.my_sqlversion is not None:
            result['MySQLVersion'] = self.my_sqlversion
        if self.pay_type is not None:
            result['PayType'] = self.pay_type
        if self.pricing_cycle is not None:
            result['PricingCycle'] = self.pricing_cycle
        if self.quantity is not None:
            result['Quantity'] = self.quantity
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.specification is not None:
            result['Specification'] = self.specification
        if self.type is not None:
            result['Type'] = self.type
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.vswitch_id is not None:
            result['VswitchId'] = self.vswitch_id
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        if self.is_ha is not None:
            result['isHa'] = self.is_ha
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClientToken') is not None:
            self.client_token = m.get('ClientToken')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Duration') is not None:
            self.duration = m.get('Duration')
        if m.get('InstanceSeries') is not None:
            self.instance_series = m.get('InstanceSeries')
        if m.get('IsAutoRenew') is not None:
            self.is_auto_renew = m.get('IsAutoRenew')
        if m.get('MasterInstId') is not None:
            self.master_inst_id = m.get('MasterInstId')
        if m.get('MySQLVersion') is not None:
            self.my_sqlversion = m.get('MySQLVersion')
        if m.get('PayType') is not None:
            self.pay_type = m.get('PayType')
        if m.get('PricingCycle') is not None:
            self.pricing_cycle = m.get('PricingCycle')
        if m.get('Quantity') is not None:
            self.quantity = m.get('Quantity')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('Specification') is not None:
            self.specification = m.get('Specification')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VswitchId') is not None:
            self.vswitch_id = m.get('VswitchId')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        if m.get('isHa') is not None:
            self.is_ha = m.get('isHa')
        return self


class CreateDrdsInstanceResponseBodyDataDrdsInstanceIdList(TeaModel):
    def __init__(
        self,
        drds_instance_id_list: List[str] = None,
    ):
        self.drds_instance_id_list = drds_instance_id_list

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id_list is not None:
            result['drdsInstanceIdList'] = self.drds_instance_id_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('drdsInstanceIdList') is not None:
            self.drds_instance_id_list = m.get('drdsInstanceIdList')
        return self


class CreateDrdsInstanceResponseBodyData(TeaModel):
    def __init__(
        self,
        drds_instance_id_list: CreateDrdsInstanceResponseBodyDataDrdsInstanceIdList = None,
        order_id: int = None,
    ):
        self.drds_instance_id_list = drds_instance_id_list
        self.order_id = order_id

    def validate(self):
        if self.drds_instance_id_list:
            self.drds_instance_id_list.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id_list is not None:
            result['DrdsInstanceIdList'] = self.drds_instance_id_list.to_map()
        if self.order_id is not None:
            result['OrderId'] = self.order_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceIdList') is not None:
            temp_model = CreateDrdsInstanceResponseBodyDataDrdsInstanceIdList()
            self.drds_instance_id_list = temp_model.from_map(m['DrdsInstanceIdList'])
        if m.get('OrderId') is not None:
            self.order_id = m.get('OrderId')
        return self


class CreateDrdsInstanceResponseBody(TeaModel):
    def __init__(
        self,
        data: CreateDrdsInstanceResponseBodyData = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = CreateDrdsInstanceResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateDrdsInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateDrdsInstanceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateDrdsInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateInstanceAccountRequestDbPrivilege(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        privilege: str = None,
    ):
        self.db_name = db_name
        self.privilege = privilege

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.privilege is not None:
            result['Privilege'] = self.privilege
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('Privilege') is not None:
            self.privilege = m.get('Privilege')
        return self


class CreateInstanceAccountRequest(TeaModel):
    def __init__(
        self,
        account_name: str = None,
        db_privilege: List[CreateInstanceAccountRequestDbPrivilege] = None,
        drds_instance_id: str = None,
        password: str = None,
    ):
        self.account_name = account_name
        self.db_privilege = db_privilege
        self.drds_instance_id = drds_instance_id
        self.password = password

    def validate(self):
        if self.db_privilege:
            for k in self.db_privilege:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_name is not None:
            result['AccountName'] = self.account_name
        result['DbPrivilege'] = []
        if self.db_privilege is not None:
            for k in self.db_privilege:
                result['DbPrivilege'].append(k.to_map() if k else None)
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.password is not None:
            result['Password'] = self.password
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountName') is not None:
            self.account_name = m.get('AccountName')
        self.db_privilege = []
        if m.get('DbPrivilege') is not None:
            for k in m.get('DbPrivilege'):
                temp_model = CreateInstanceAccountRequestDbPrivilege()
                self.db_privilege.append(temp_model.from_map(k))
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('Password') is not None:
            self.password = m.get('Password')
        return self


class CreateInstanceAccountResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateInstanceAccountResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateInstanceAccountResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateInstanceAccountResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateInstanceInternetAddressRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
        region_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class CreateInstanceInternetAddressResponseBody(TeaModel):
    def __init__(
        self,
        code: int = None,
        data: bool = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.code = code
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.code is not None:
            result['Code'] = self.code
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Code') is not None:
            self.code = m.get('Code')
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateInstanceInternetAddressResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateInstanceInternetAddressResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateInstanceInternetAddressResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateOrderForRdsRequest(TeaModel):
    def __init__(
        self,
        params: str = None,
        region_id: str = None,
    ):
        self.params = params
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.params is not None:
            result['Params'] = self.params
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Params') is not None:
            self.params = m.get('Params')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class CreateOrderForRdsResponseBody(TeaModel):
    def __init__(
        self,
        data: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateOrderForRdsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateOrderForRdsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateOrderForRdsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class CreateShardTaskRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        region_id: str = None,
        source_table_name: str = None,
        target_table_name: str = None,
        task_type: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id
        self.source_table_name = source_table_name
        self.target_table_name = target_table_name
        self.task_type = task_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.source_table_name is not None:
            result['SourceTableName'] = self.source_table_name
        if self.target_table_name is not None:
            result['TargetTableName'] = self.target_table_name
        if self.task_type is not None:
            result['TaskType'] = self.task_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('SourceTableName') is not None:
            self.source_table_name = m.get('SourceTableName')
        if m.get('TargetTableName') is not None:
            self.target_table_name = m.get('TargetTableName')
        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')
        return self


class CreateShardTaskResponseBody(TeaModel):
    def __init__(
        self,
        data: bool = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class CreateShardTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: CreateShardTaskResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = CreateShardTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeBackMenuRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeBackMenuResponseBodyListList(TeaModel):
    def __init__(
        self,
        menu_name: str = None,
        support: bool = None,
    ):
        self.menu_name = menu_name
        self.support = support

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.menu_name is not None:
            result['MenuName'] = self.menu_name
        if self.support is not None:
            result['Support'] = self.support
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('MenuName') is not None:
            self.menu_name = m.get('MenuName')
        if m.get('Support') is not None:
            self.support = m.get('Support')
        return self


class DescribeBackMenuResponseBodyList(TeaModel):
    def __init__(
        self,
        list: List[DescribeBackMenuResponseBodyListList] = None,
    ):
        self.list = list

    def validate(self):
        if self.list:
            for k in self.list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['list'] = []
        if self.list is not None:
            for k in self.list:
                result['list'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.list = []
        if m.get('list') is not None:
            for k in m.get('list'):
                temp_model = DescribeBackMenuResponseBodyListList()
                self.list.append(temp_model.from_map(k))
        return self


class DescribeBackMenuResponseBody(TeaModel):
    def __init__(
        self,
        list: DescribeBackMenuResponseBodyList = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.list = list
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.list:
            self.list.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.list is not None:
            result['List'] = self.list.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('List') is not None:
            temp_model = DescribeBackMenuResponseBodyList()
            self.list = temp_model.from_map(m['List'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeBackMenuResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeBackMenuResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeBackMenuResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeBackupDbsRequest(TeaModel):
    def __init__(
        self,
        backup_id: str = None,
        drds_instance_id: str = None,
        preferred_restore_time: str = None,
    ):
        self.backup_id = backup_id
        self.drds_instance_id = drds_instance_id
        self.preferred_restore_time = preferred_restore_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.backup_id is not None:
            result['BackupId'] = self.backup_id
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.preferred_restore_time is not None:
            result['PreferredRestoreTime'] = self.preferred_restore_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BackupId') is not None:
            self.backup_id = m.get('BackupId')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('PreferredRestoreTime') is not None:
            self.preferred_restore_time = m.get('PreferredRestoreTime')
        return self


class DescribeBackupDbsResponseBodyDbNames(TeaModel):
    def __init__(
        self,
        db_name: List[str] = None,
    ):
        self.db_name = db_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['dbName'] = self.db_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('dbName') is not None:
            self.db_name = m.get('dbName')
        return self


class DescribeBackupDbsResponseBody(TeaModel):
    def __init__(
        self,
        db_names: DescribeBackupDbsResponseBodyDbNames = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.db_names = db_names
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.db_names:
            self.db_names.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_names is not None:
            result['DbNames'] = self.db_names.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbNames') is not None:
            temp_model = DescribeBackupDbsResponseBodyDbNames()
            self.db_names = temp_model.from_map(m['DbNames'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeBackupDbsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeBackupDbsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeBackupDbsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeBackupLocalRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeBackupLocalResponseBodyBackupPolicyDO(TeaModel):
    def __init__(
        self,
        backup_app_name: str = None,
        backup_db_name: str = None,
        backup_level: str = None,
        backup_log: str = None,
        backup_mode: str = None,
        backup_policy_mode: str = None,
        backup_retention_period: int = None,
        backup_type: str = None,
        data_backup_retention_period: int = None,
        gmt_create: int = None,
        gmt_modified: int = None,
        high_space_usage_protection: int = None,
        local_log_retention_hours: int = None,
        local_log_retention_space: int = None,
        log_backup_retention_period: int = None,
        next_backup_actually_time: str = None,
        preferred_backup_period: str = None,
        preferred_backup_time: str = None,
    ):
        self.backup_app_name = backup_app_name
        self.backup_db_name = backup_db_name
        self.backup_level = backup_level
        self.backup_log = backup_log
        self.backup_mode = backup_mode
        self.backup_policy_mode = backup_policy_mode
        self.backup_retention_period = backup_retention_period
        self.backup_type = backup_type
        self.data_backup_retention_period = data_backup_retention_period
        self.gmt_create = gmt_create
        self.gmt_modified = gmt_modified
        self.high_space_usage_protection = high_space_usage_protection
        self.local_log_retention_hours = local_log_retention_hours
        self.local_log_retention_space = local_log_retention_space
        self.log_backup_retention_period = log_backup_retention_period
        self.next_backup_actually_time = next_backup_actually_time
        self.preferred_backup_period = preferred_backup_period
        self.preferred_backup_time = preferred_backup_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.backup_app_name is not None:
            result['BackupAppName'] = self.backup_app_name
        if self.backup_db_name is not None:
            result['BackupDbName'] = self.backup_db_name
        if self.backup_level is not None:
            result['BackupLevel'] = self.backup_level
        if self.backup_log is not None:
            result['BackupLog'] = self.backup_log
        if self.backup_mode is not None:
            result['BackupMode'] = self.backup_mode
        if self.backup_policy_mode is not None:
            result['BackupPolicyMode'] = self.backup_policy_mode
        if self.backup_retention_period is not None:
            result['BackupRetentionPeriod'] = self.backup_retention_period
        if self.backup_type is not None:
            result['BackupType'] = self.backup_type
        if self.data_backup_retention_period is not None:
            result['DataBackupRetentionPeriod'] = self.data_backup_retention_period
        if self.gmt_create is not None:
            result['GmtCreate'] = self.gmt_create
        if self.gmt_modified is not None:
            result['GmtModified'] = self.gmt_modified
        if self.high_space_usage_protection is not None:
            result['HighSpaceUsageProtection'] = self.high_space_usage_protection
        if self.local_log_retention_hours is not None:
            result['LocalLogRetentionHours'] = self.local_log_retention_hours
        if self.local_log_retention_space is not None:
            result['LocalLogRetentionSpace'] = self.local_log_retention_space
        if self.log_backup_retention_period is not None:
            result['LogBackupRetentionPeriod'] = self.log_backup_retention_period
        if self.next_backup_actually_time is not None:
            result['NextBackupActuallyTime'] = self.next_backup_actually_time
        if self.preferred_backup_period is not None:
            result['PreferredBackupPeriod'] = self.preferred_backup_period
        if self.preferred_backup_time is not None:
            result['PreferredBackupTime'] = self.preferred_backup_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BackupAppName') is not None:
            self.backup_app_name = m.get('BackupAppName')
        if m.get('BackupDbName') is not None:
            self.backup_db_name = m.get('BackupDbName')
        if m.get('BackupLevel') is not None:
            self.backup_level = m.get('BackupLevel')
        if m.get('BackupLog') is not None:
            self.backup_log = m.get('BackupLog')
        if m.get('BackupMode') is not None:
            self.backup_mode = m.get('BackupMode')
        if m.get('BackupPolicyMode') is not None:
            self.backup_policy_mode = m.get('BackupPolicyMode')
        if m.get('BackupRetentionPeriod') is not None:
            self.backup_retention_period = m.get('BackupRetentionPeriod')
        if m.get('BackupType') is not None:
            self.backup_type = m.get('BackupType')
        if m.get('DataBackupRetentionPeriod') is not None:
            self.data_backup_retention_period = m.get('DataBackupRetentionPeriod')
        if m.get('GmtCreate') is not None:
            self.gmt_create = m.get('GmtCreate')
        if m.get('GmtModified') is not None:
            self.gmt_modified = m.get('GmtModified')
        if m.get('HighSpaceUsageProtection') is not None:
            self.high_space_usage_protection = m.get('HighSpaceUsageProtection')
        if m.get('LocalLogRetentionHours') is not None:
            self.local_log_retention_hours = m.get('LocalLogRetentionHours')
        if m.get('LocalLogRetentionSpace') is not None:
            self.local_log_retention_space = m.get('LocalLogRetentionSpace')
        if m.get('LogBackupRetentionPeriod') is not None:
            self.log_backup_retention_period = m.get('LogBackupRetentionPeriod')
        if m.get('NextBackupActuallyTime') is not None:
            self.next_backup_actually_time = m.get('NextBackupActuallyTime')
        if m.get('PreferredBackupPeriod') is not None:
            self.preferred_backup_period = m.get('PreferredBackupPeriod')
        if m.get('PreferredBackupTime') is not None:
            self.preferred_backup_time = m.get('PreferredBackupTime')
        return self


class DescribeBackupLocalResponseBody(TeaModel):
    def __init__(
        self,
        backup_policy_do: DescribeBackupLocalResponseBodyBackupPolicyDO = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.backup_policy_do = backup_policy_do
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.backup_policy_do:
            self.backup_policy_do.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.backup_policy_do is not None:
            result['BackupPolicyDO'] = self.backup_policy_do.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BackupPolicyDO') is not None:
            temp_model = DescribeBackupLocalResponseBodyBackupPolicyDO()
            self.backup_policy_do = temp_model.from_map(m['BackupPolicyDO'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeBackupLocalResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeBackupLocalResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeBackupLocalResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeBackupPolicyRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeBackupPolicyResponseBodyBackupPolicyDO(TeaModel):
    def __init__(
        self,
        backup_app_name: str = None,
        backup_db_name: str = None,
        backup_level: str = None,
        backup_log: str = None,
        backup_mode: str = None,
        backup_policy_mode: str = None,
        backup_retention_period: int = None,
        backup_type: str = None,
        data_backup_retention_period: int = None,
        gmt_create: int = None,
        gmt_modified: int = None,
        high_space_usage_protection: int = None,
        local_log_retention_hours: int = None,
        local_log_retention_space: int = None,
        log_backup_retention_period: int = None,
        next_backup_actually_time: str = None,
        preferred_backup_period: str = None,
        preferred_backup_time: str = None,
    ):
        self.backup_app_name = backup_app_name
        self.backup_db_name = backup_db_name
        self.backup_level = backup_level
        self.backup_log = backup_log
        self.backup_mode = backup_mode
        self.backup_policy_mode = backup_policy_mode
        self.backup_retention_period = backup_retention_period
        self.backup_type = backup_type
        self.data_backup_retention_period = data_backup_retention_period
        self.gmt_create = gmt_create
        self.gmt_modified = gmt_modified
        self.high_space_usage_protection = high_space_usage_protection
        self.local_log_retention_hours = local_log_retention_hours
        self.local_log_retention_space = local_log_retention_space
        self.log_backup_retention_period = log_backup_retention_period
        self.next_backup_actually_time = next_backup_actually_time
        self.preferred_backup_period = preferred_backup_period
        self.preferred_backup_time = preferred_backup_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.backup_app_name is not None:
            result['BackupAppName'] = self.backup_app_name
        if self.backup_db_name is not None:
            result['BackupDbName'] = self.backup_db_name
        if self.backup_level is not None:
            result['BackupLevel'] = self.backup_level
        if self.backup_log is not None:
            result['BackupLog'] = self.backup_log
        if self.backup_mode is not None:
            result['BackupMode'] = self.backup_mode
        if self.backup_policy_mode is not None:
            result['BackupPolicyMode'] = self.backup_policy_mode
        if self.backup_retention_period is not None:
            result['BackupRetentionPeriod'] = self.backup_retention_period
        if self.backup_type is not None:
            result['BackupType'] = self.backup_type
        if self.data_backup_retention_period is not None:
            result['DataBackupRetentionPeriod'] = self.data_backup_retention_period
        if self.gmt_create is not None:
            result['GmtCreate'] = self.gmt_create
        if self.gmt_modified is not None:
            result['GmtModified'] = self.gmt_modified
        if self.high_space_usage_protection is not None:
            result['HighSpaceUsageProtection'] = self.high_space_usage_protection
        if self.local_log_retention_hours is not None:
            result['LocalLogRetentionHours'] = self.local_log_retention_hours
        if self.local_log_retention_space is not None:
            result['LocalLogRetentionSpace'] = self.local_log_retention_space
        if self.log_backup_retention_period is not None:
            result['LogBackupRetentionPeriod'] = self.log_backup_retention_period
        if self.next_backup_actually_time is not None:
            result['NextBackupActuallyTime'] = self.next_backup_actually_time
        if self.preferred_backup_period is not None:
            result['PreferredBackupPeriod'] = self.preferred_backup_period
        if self.preferred_backup_time is not None:
            result['PreferredBackupTime'] = self.preferred_backup_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BackupAppName') is not None:
            self.backup_app_name = m.get('BackupAppName')
        if m.get('BackupDbName') is not None:
            self.backup_db_name = m.get('BackupDbName')
        if m.get('BackupLevel') is not None:
            self.backup_level = m.get('BackupLevel')
        if m.get('BackupLog') is not None:
            self.backup_log = m.get('BackupLog')
        if m.get('BackupMode') is not None:
            self.backup_mode = m.get('BackupMode')
        if m.get('BackupPolicyMode') is not None:
            self.backup_policy_mode = m.get('BackupPolicyMode')
        if m.get('BackupRetentionPeriod') is not None:
            self.backup_retention_period = m.get('BackupRetentionPeriod')
        if m.get('BackupType') is not None:
            self.backup_type = m.get('BackupType')
        if m.get('DataBackupRetentionPeriod') is not None:
            self.data_backup_retention_period = m.get('DataBackupRetentionPeriod')
        if m.get('GmtCreate') is not None:
            self.gmt_create = m.get('GmtCreate')
        if m.get('GmtModified') is not None:
            self.gmt_modified = m.get('GmtModified')
        if m.get('HighSpaceUsageProtection') is not None:
            self.high_space_usage_protection = m.get('HighSpaceUsageProtection')
        if m.get('LocalLogRetentionHours') is not None:
            self.local_log_retention_hours = m.get('LocalLogRetentionHours')
        if m.get('LocalLogRetentionSpace') is not None:
            self.local_log_retention_space = m.get('LocalLogRetentionSpace')
        if m.get('LogBackupRetentionPeriod') is not None:
            self.log_backup_retention_period = m.get('LogBackupRetentionPeriod')
        if m.get('NextBackupActuallyTime') is not None:
            self.next_backup_actually_time = m.get('NextBackupActuallyTime')
        if m.get('PreferredBackupPeriod') is not None:
            self.preferred_backup_period = m.get('PreferredBackupPeriod')
        if m.get('PreferredBackupTime') is not None:
            self.preferred_backup_time = m.get('PreferredBackupTime')
        return self


class DescribeBackupPolicyResponseBody(TeaModel):
    def __init__(
        self,
        backup_policy_do: DescribeBackupPolicyResponseBodyBackupPolicyDO = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.backup_policy_do = backup_policy_do
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.backup_policy_do:
            self.backup_policy_do.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.backup_policy_do is not None:
            result['BackupPolicyDO'] = self.backup_policy_do.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BackupPolicyDO') is not None:
            temp_model = DescribeBackupPolicyResponseBodyBackupPolicyDO()
            self.backup_policy_do = temp_model.from_map(m['BackupPolicyDO'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeBackupPolicyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeBackupPolicyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeBackupPolicyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeBackupSetsRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
        end_time: str = None,
        start_time: str = None,
    ):
        self.drds_instance_id = drds_instance_id
        self.end_time = end_time
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class DescribeBackupSetsResponseBodyBackupSetsBackupSetBackupDbs(TeaModel):
    def __init__(
        self,
        backup_db: List[str] = None,
    ):
        self.backup_db = backup_db

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.backup_db is not None:
            result['backupDb'] = self.backup_db
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('backupDb') is not None:
            self.backup_db = m.get('backupDb')
        return self


class DescribeBackupSetsResponseBodyBackupSetsBackupSet(TeaModel):
    def __init__(
        self,
        backup_consitent_time: str = None,
        backup_dbs: DescribeBackupSetsResponseBodyBackupSetsBackupSetBackupDbs = None,
        backup_end_time: int = None,
        backup_level: str = None,
        backup_mode: str = None,
        backup_start_time: int = None,
        backup_total_size: str = None,
        backup_type: str = None,
        enable_recovery: bool = None,
        id: str = None,
        status: int = None,
    ):
        self.backup_consitent_time = backup_consitent_time
        self.backup_dbs = backup_dbs
        self.backup_end_time = backup_end_time
        self.backup_level = backup_level
        self.backup_mode = backup_mode
        self.backup_start_time = backup_start_time
        self.backup_total_size = backup_total_size
        self.backup_type = backup_type
        self.enable_recovery = enable_recovery
        self.id = id
        self.status = status

    def validate(self):
        if self.backup_dbs:
            self.backup_dbs.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.backup_consitent_time is not None:
            result['BackupConsitentTime'] = self.backup_consitent_time
        if self.backup_dbs is not None:
            result['BackupDbs'] = self.backup_dbs.to_map()
        if self.backup_end_time is not None:
            result['BackupEndTime'] = self.backup_end_time
        if self.backup_level is not None:
            result['BackupLevel'] = self.backup_level
        if self.backup_mode is not None:
            result['BackupMode'] = self.backup_mode
        if self.backup_start_time is not None:
            result['BackupStartTime'] = self.backup_start_time
        if self.backup_total_size is not None:
            result['BackupTotalSize'] = self.backup_total_size
        if self.backup_type is not None:
            result['BackupType'] = self.backup_type
        if self.enable_recovery is not None:
            result['EnableRecovery'] = self.enable_recovery
        if self.id is not None:
            result['Id'] = self.id
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BackupConsitentTime') is not None:
            self.backup_consitent_time = m.get('BackupConsitentTime')
        if m.get('BackupDbs') is not None:
            temp_model = DescribeBackupSetsResponseBodyBackupSetsBackupSetBackupDbs()
            self.backup_dbs = temp_model.from_map(m['BackupDbs'])
        if m.get('BackupEndTime') is not None:
            self.backup_end_time = m.get('BackupEndTime')
        if m.get('BackupLevel') is not None:
            self.backup_level = m.get('BackupLevel')
        if m.get('BackupMode') is not None:
            self.backup_mode = m.get('BackupMode')
        if m.get('BackupStartTime') is not None:
            self.backup_start_time = m.get('BackupStartTime')
        if m.get('BackupTotalSize') is not None:
            self.backup_total_size = m.get('BackupTotalSize')
        if m.get('BackupType') is not None:
            self.backup_type = m.get('BackupType')
        if m.get('EnableRecovery') is not None:
            self.enable_recovery = m.get('EnableRecovery')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class DescribeBackupSetsResponseBodyBackupSets(TeaModel):
    def __init__(
        self,
        backup_set: List[DescribeBackupSetsResponseBodyBackupSetsBackupSet] = None,
    ):
        self.backup_set = backup_set

    def validate(self):
        if self.backup_set:
            for k in self.backup_set:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['backupSet'] = []
        if self.backup_set is not None:
            for k in self.backup_set:
                result['backupSet'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.backup_set = []
        if m.get('backupSet') is not None:
            for k in m.get('backupSet'):
                temp_model = DescribeBackupSetsResponseBodyBackupSetsBackupSet()
                self.backup_set.append(temp_model.from_map(k))
        return self


class DescribeBackupSetsResponseBody(TeaModel):
    def __init__(
        self,
        backup_sets: DescribeBackupSetsResponseBodyBackupSets = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.backup_sets = backup_sets
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.backup_sets:
            self.backup_sets.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.backup_sets is not None:
            result['BackupSets'] = self.backup_sets.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BackupSets') is not None:
            temp_model = DescribeBackupSetsResponseBodyBackupSets()
            self.backup_sets = temp_model.from_map(m['BackupSets'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeBackupSetsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeBackupSetsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeBackupSetsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeBackupTimesRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeBackupTimesResponseBodyRestoreTime(TeaModel):
    def __init__(
        self,
        end_time: str = None,
        start_time: str = None,
    ):
        self.end_time = end_time
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class DescribeBackupTimesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        restore_time: DescribeBackupTimesResponseBodyRestoreTime = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.restore_time = restore_time
        self.success = success

    def validate(self):
        if self.restore_time:
            self.restore_time.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.restore_time is not None:
            result['RestoreTime'] = self.restore_time.to_map()
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('RestoreTime') is not None:
            temp_model = DescribeBackupTimesResponseBodyRestoreTime()
            self.restore_time = temp_model.from_map(m['RestoreTime'])
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeBackupTimesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeBackupTimesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeBackupTimesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeBroadcastTablesRequest(TeaModel):
    def __init__(
        self,
        current_page: int = None,
        db_name: str = None,
        drds_instance_id: str = None,
        page_size: int = None,
        query: str = None,
        region_id: str = None,
    ):
        self.current_page = current_page
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.page_size = page_size
        self.query = query
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.current_page is not None:
            result['CurrentPage'] = self.current_page
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.query is not None:
            result['Query'] = self.query
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CurrentPage') is not None:
            self.current_page = m.get('CurrentPage')
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Query') is not None:
            self.query = m.get('Query')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeBroadcastTablesResponseBodyList(TeaModel):
    def __init__(
        self,
        broadcast: bool = None,
        broadcast_type: str = None,
        db_inst_type: int = None,
        is_shard: bool = None,
        status: int = None,
        table: str = None,
    ):
        self.broadcast = broadcast
        self.broadcast_type = broadcast_type
        self.db_inst_type = db_inst_type
        self.is_shard = is_shard
        self.status = status
        self.table = table

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.broadcast is not None:
            result['Broadcast'] = self.broadcast
        if self.broadcast_type is not None:
            result['BroadcastType'] = self.broadcast_type
        if self.db_inst_type is not None:
            result['DbInstType'] = self.db_inst_type
        if self.is_shard is not None:
            result['IsShard'] = self.is_shard
        if self.status is not None:
            result['Status'] = self.status
        if self.table is not None:
            result['Table'] = self.table
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Broadcast') is not None:
            self.broadcast = m.get('Broadcast')
        if m.get('BroadcastType') is not None:
            self.broadcast_type = m.get('BroadcastType')
        if m.get('DbInstType') is not None:
            self.db_inst_type = m.get('DbInstType')
        if m.get('IsShard') is not None:
            self.is_shard = m.get('IsShard')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Table') is not None:
            self.table = m.get('Table')
        return self


class DescribeBroadcastTablesResponseBody(TeaModel):
    def __init__(
        self,
        is_shard: bool = None,
        list: List[DescribeBroadcastTablesResponseBodyList] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        success: bool = None,
        total: int = None,
    ):
        self.is_shard = is_shard
        self.list = list
        self.page_number = page_number
        self.page_size = page_size
        self.request_id = request_id
        self.success = success
        self.total = total

    def validate(self):
        if self.list:
            for k in self.list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.is_shard is not None:
            result['IsShard'] = self.is_shard
        result['List'] = []
        if self.list is not None:
            for k in self.list:
                result['List'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('IsShard') is not None:
            self.is_shard = m.get('IsShard')
        self.list = []
        if m.get('List') is not None:
            for k in m.get('List'):
                temp_model = DescribeBroadcastTablesResponseBodyList()
                self.list.append(temp_model.from_map(k))
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class DescribeBroadcastTablesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeBroadcastTablesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeBroadcastTablesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDbInstanceDbsRequest(TeaModel):
    def __init__(
        self,
        account_name: str = None,
        db_inst_type: str = None,
        db_instance_id: str = None,
        drds_instance_id: str = None,
        password: str = None,
    ):
        self.account_name = account_name
        self.db_inst_type = db_inst_type
        self.db_instance_id = db_instance_id
        self.drds_instance_id = drds_instance_id
        self.password = password

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_name is not None:
            result['AccountName'] = self.account_name
        if self.db_inst_type is not None:
            result['DbInstType'] = self.db_inst_type
        if self.db_instance_id is not None:
            result['DbInstanceId'] = self.db_instance_id
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.password is not None:
            result['Password'] = self.password
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountName') is not None:
            self.account_name = m.get('AccountName')
        if m.get('DbInstType') is not None:
            self.db_inst_type = m.get('DbInstType')
        if m.get('DbInstanceId') is not None:
            self.db_instance_id = m.get('DbInstanceId')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('Password') is not None:
            self.password = m.get('Password')
        return self


class DescribeDbInstanceDbsResponseBodyDatabasesDatabase(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        description: str = None,
        status: int = None,
    ):
        self.db_name = db_name
        self.description = description
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.description is not None:
            result['Description'] = self.description
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class DescribeDbInstanceDbsResponseBodyDatabases(TeaModel):
    def __init__(
        self,
        database: List[DescribeDbInstanceDbsResponseBodyDatabasesDatabase] = None,
    ):
        self.database = database

    def validate(self):
        if self.database:
            for k in self.database:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Database'] = []
        if self.database is not None:
            for k in self.database:
                result['Database'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.database = []
        if m.get('Database') is not None:
            for k in m.get('Database'):
                temp_model = DescribeDbInstanceDbsResponseBodyDatabasesDatabase()
                self.database.append(temp_model.from_map(k))
        return self


class DescribeDbInstanceDbsResponseBody(TeaModel):
    def __init__(
        self,
        databases: DescribeDbInstanceDbsResponseBodyDatabases = None,
        request_id: str = None,
        success: bool = None,
        total: str = None,
    ):
        self.databases = databases
        self.request_id = request_id
        self.success = success
        self.total = total

    def validate(self):
        if self.databases:
            self.databases.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.databases is not None:
            result['Databases'] = self.databases.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Databases') is not None:
            temp_model = DescribeDbInstanceDbsResponseBodyDatabases()
            self.databases = temp_model.from_map(m['Databases'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class DescribeDbInstanceDbsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDbInstanceDbsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDbInstanceDbsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDbInstancesRequest(TeaModel):
    def __init__(
        self,
        db_inst_type: str = None,
        drds_instance_id: str = None,
        page_number: int = None,
        page_size: int = None,
        search: str = None,
    ):
        self.db_inst_type = db_inst_type
        self.drds_instance_id = drds_instance_id
        self.page_number = page_number
        self.page_size = page_size
        self.search = search

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_inst_type is not None:
            result['DbInstType'] = self.db_inst_type
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.search is not None:
            result['Search'] = self.search
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbInstType') is not None:
            self.db_inst_type = m.get('DbInstType')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Search') is not None:
            self.search = m.get('Search')
        return self


class DescribeDbInstancesResponseBodyItemsDBInstanceReadOnlyDBInstanceId(TeaModel):
    def __init__(
        self,
        read_only_dbinstance_id: List[str] = None,
    ):
        self.read_only_dbinstance_id = read_only_dbinstance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.read_only_dbinstance_id is not None:
            result['ReadOnlyDBInstanceId'] = self.read_only_dbinstance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ReadOnlyDBInstanceId') is not None:
            self.read_only_dbinstance_id = m.get('ReadOnlyDBInstanceId')
        return self


class DescribeDbInstancesResponseBodyItemsDBInstance(TeaModel):
    def __init__(
        self,
        dbinstance_description: str = None,
        dbinstance_id: str = None,
        dbinstance_status: int = None,
        dbinstance_type: str = None,
        engine: str = None,
        engine_version: str = None,
        instance_network_type: str = None,
        read_only_dbinstance_id: DescribeDbInstancesResponseBodyItemsDBInstanceReadOnlyDBInstanceId = None,
        region_id: str = None,
        zone_id: str = None,
    ):
        self.dbinstance_description = dbinstance_description
        self.dbinstance_id = dbinstance_id
        self.dbinstance_status = dbinstance_status
        self.dbinstance_type = dbinstance_type
        self.engine = engine
        self.engine_version = engine_version
        self.instance_network_type = instance_network_type
        self.read_only_dbinstance_id = read_only_dbinstance_id
        self.region_id = region_id
        self.zone_id = zone_id

    def validate(self):
        if self.read_only_dbinstance_id:
            self.read_only_dbinstance_id.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dbinstance_description is not None:
            result['DBInstanceDescription'] = self.dbinstance_description
        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id
        if self.dbinstance_status is not None:
            result['DBInstanceStatus'] = self.dbinstance_status
        if self.dbinstance_type is not None:
            result['DBInstanceType'] = self.dbinstance_type
        if self.engine is not None:
            result['Engine'] = self.engine
        if self.engine_version is not None:
            result['EngineVersion'] = self.engine_version
        if self.instance_network_type is not None:
            result['InstanceNetworkType'] = self.instance_network_type
        if self.read_only_dbinstance_id is not None:
            result['ReadOnlyDBInstanceId'] = self.read_only_dbinstance_id.to_map()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DBInstanceDescription') is not None:
            self.dbinstance_description = m.get('DBInstanceDescription')
        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')
        if m.get('DBInstanceStatus') is not None:
            self.dbinstance_status = m.get('DBInstanceStatus')
        if m.get('DBInstanceType') is not None:
            self.dbinstance_type = m.get('DBInstanceType')
        if m.get('Engine') is not None:
            self.engine = m.get('Engine')
        if m.get('EngineVersion') is not None:
            self.engine_version = m.get('EngineVersion')
        if m.get('InstanceNetworkType') is not None:
            self.instance_network_type = m.get('InstanceNetworkType')
        if m.get('ReadOnlyDBInstanceId') is not None:
            temp_model = DescribeDbInstancesResponseBodyItemsDBInstanceReadOnlyDBInstanceId()
            self.read_only_dbinstance_id = temp_model.from_map(m['ReadOnlyDBInstanceId'])
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class DescribeDbInstancesResponseBodyItems(TeaModel):
    def __init__(
        self,
        dbinstance: List[DescribeDbInstancesResponseBodyItemsDBInstance] = None,
    ):
        self.dbinstance = dbinstance

    def validate(self):
        if self.dbinstance:
            for k in self.dbinstance:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['DBInstance'] = []
        if self.dbinstance is not None:
            for k in self.dbinstance:
                result['DBInstance'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.dbinstance = []
        if m.get('DBInstance') is not None:
            for k in m.get('DBInstance'):
                temp_model = DescribeDbInstancesResponseBodyItemsDBInstance()
                self.dbinstance.append(temp_model.from_map(k))
        return self


class DescribeDbInstancesResponseBody(TeaModel):
    def __init__(
        self,
        items: DescribeDbInstancesResponseBodyItems = None,
        request_id: str = None,
    ):
        self.items = items
        self.request_id = request_id

    def validate(self):
        if self.items:
            self.items.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.items is not None:
            result['Items'] = self.items.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Items') is not None:
            temp_model = DescribeDbInstancesResponseBodyItems()
            self.items = temp_model.from_map(m['Items'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeDbInstancesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDbInstancesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDbInstancesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsDBRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeDrdsDBResponseBodyData(TeaModel):
    def __init__(
        self,
        create_time: str = None,
        db_inst_type: str = None,
        db_name: str = None,
        inst_role: str = None,
        mode: str = None,
        schema: str = None,
        status: str = None,
    ):
        self.create_time = create_time
        self.db_inst_type = db_inst_type
        self.db_name = db_name
        self.inst_role = inst_role
        self.mode = mode
        self.schema = schema
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.db_inst_type is not None:
            result['DbInstType'] = self.db_inst_type
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.inst_role is not None:
            result['InstRole'] = self.inst_role
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.schema is not None:
            result['Schema'] = self.schema
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('DbInstType') is not None:
            self.db_inst_type = m.get('DbInstType')
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('InstRole') is not None:
            self.inst_role = m.get('InstRole')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('Schema') is not None:
            self.schema = m.get('Schema')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class DescribeDrdsDBResponseBody(TeaModel):
    def __init__(
        self,
        data: DescribeDrdsDBResponseBodyData = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = DescribeDrdsDBResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeDrdsDBResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsDBResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsDBResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsDBClusterRequest(TeaModel):
    def __init__(
        self,
        db_instance_id: str = None,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_instance_id = db_instance_id
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_instance_id is not None:
            result['DbInstanceId'] = self.db_instance_id
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbInstanceId') is not None:
            self.db_instance_id = m.get('DbInstanceId')
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeDrdsDBClusterResponseBodyDbInstanceDBNodesDBNode(TeaModel):
    def __init__(
        self,
        dbnode_id: str = None,
        dbnode_role: str = None,
        dbnode_status: str = None,
        zone_id: str = None,
    ):
        self.dbnode_id = dbnode_id
        self.dbnode_role = dbnode_role
        self.dbnode_status = dbnode_status
        self.zone_id = zone_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dbnode_id is not None:
            result['DBNodeId'] = self.dbnode_id
        if self.dbnode_role is not None:
            result['DBNodeRole'] = self.dbnode_role
        if self.dbnode_status is not None:
            result['DBNodeStatus'] = self.dbnode_status
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DBNodeId') is not None:
            self.dbnode_id = m.get('DBNodeId')
        if m.get('DBNodeRole') is not None:
            self.dbnode_role = m.get('DBNodeRole')
        if m.get('DBNodeStatus') is not None:
            self.dbnode_status = m.get('DBNodeStatus')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class DescribeDrdsDBClusterResponseBodyDbInstanceDBNodes(TeaModel):
    def __init__(
        self,
        dbnode: List[DescribeDrdsDBClusterResponseBodyDbInstanceDBNodesDBNode] = None,
    ):
        self.dbnode = dbnode

    def validate(self):
        if self.dbnode:
            for k in self.dbnode:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['DBNode'] = []
        if self.dbnode is not None:
            for k in self.dbnode:
                result['DBNode'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.dbnode = []
        if m.get('DBNode') is not None:
            for k in m.get('DBNode'):
                temp_model = DescribeDrdsDBClusterResponseBodyDbInstanceDBNodesDBNode()
                self.dbnode.append(temp_model.from_map(k))
        return self


class DescribeDrdsDBClusterResponseBodyDbInstanceEndpointsEndpoint(TeaModel):
    def __init__(
        self,
        endpoint_id: str = None,
        node_ids: str = None,
        read_weight: int = None,
    ):
        self.endpoint_id = endpoint_id
        self.node_ids = node_ids
        self.read_weight = read_weight

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.endpoint_id is not None:
            result['EndpointId'] = self.endpoint_id
        if self.node_ids is not None:
            result['NodeIds'] = self.node_ids
        if self.read_weight is not None:
            result['ReadWeight'] = self.read_weight
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('EndpointId') is not None:
            self.endpoint_id = m.get('EndpointId')
        if m.get('NodeIds') is not None:
            self.node_ids = m.get('NodeIds')
        if m.get('ReadWeight') is not None:
            self.read_weight = m.get('ReadWeight')
        return self


class DescribeDrdsDBClusterResponseBodyDbInstanceEndpoints(TeaModel):
    def __init__(
        self,
        endpoint: List[DescribeDrdsDBClusterResponseBodyDbInstanceEndpointsEndpoint] = None,
    ):
        self.endpoint = endpoint

    def validate(self):
        if self.endpoint:
            for k in self.endpoint:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Endpoint'] = []
        if self.endpoint is not None:
            for k in self.endpoint:
                result['Endpoint'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.endpoint = []
        if m.get('Endpoint') is not None:
            for k in m.get('Endpoint'):
                temp_model = DescribeDrdsDBClusterResponseBodyDbInstanceEndpointsEndpoint()
                self.endpoint.append(temp_model.from_map(k))
        return self


class DescribeDrdsDBClusterResponseBodyDbInstance(TeaModel):
    def __init__(
        self,
        dbinstance_id: str = None,
        dbinstance_status: str = None,
        dbnodes: DescribeDrdsDBClusterResponseBodyDbInstanceDBNodes = None,
        db_inst_type: str = None,
        endpoints: DescribeDrdsDBClusterResponseBodyDbInstanceEndpoints = None,
        engine: str = None,
        engine_version: str = None,
        expire_time: str = None,
        network_type: str = None,
        pay_type: str = None,
        port: int = None,
        rds_inst_type: str = None,
        read_mode: str = None,
        remain_days: str = None,
    ):
        self.dbinstance_id = dbinstance_id
        self.dbinstance_status = dbinstance_status
        self.dbnodes = dbnodes
        self.db_inst_type = db_inst_type
        self.endpoints = endpoints
        self.engine = engine
        self.engine_version = engine_version
        self.expire_time = expire_time
        self.network_type = network_type
        self.pay_type = pay_type
        self.port = port
        self.rds_inst_type = rds_inst_type
        self.read_mode = read_mode
        self.remain_days = remain_days

    def validate(self):
        if self.dbnodes:
            self.dbnodes.validate()
        if self.endpoints:
            self.endpoints.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id
        if self.dbinstance_status is not None:
            result['DBInstanceStatus'] = self.dbinstance_status
        if self.dbnodes is not None:
            result['DBNodes'] = self.dbnodes.to_map()
        if self.db_inst_type is not None:
            result['DbInstType'] = self.db_inst_type
        if self.endpoints is not None:
            result['Endpoints'] = self.endpoints.to_map()
        if self.engine is not None:
            result['Engine'] = self.engine
        if self.engine_version is not None:
            result['EngineVersion'] = self.engine_version
        if self.expire_time is not None:
            result['ExpireTime'] = self.expire_time
        if self.network_type is not None:
            result['NetworkType'] = self.network_type
        if self.pay_type is not None:
            result['PayType'] = self.pay_type
        if self.port is not None:
            result['Port'] = self.port
        if self.rds_inst_type is not None:
            result['RdsInstType'] = self.rds_inst_type
        if self.read_mode is not None:
            result['ReadMode'] = self.read_mode
        if self.remain_days is not None:
            result['RemainDays'] = self.remain_days
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')
        if m.get('DBInstanceStatus') is not None:
            self.dbinstance_status = m.get('DBInstanceStatus')
        if m.get('DBNodes') is not None:
            temp_model = DescribeDrdsDBClusterResponseBodyDbInstanceDBNodes()
            self.dbnodes = temp_model.from_map(m['DBNodes'])
        if m.get('DbInstType') is not None:
            self.db_inst_type = m.get('DbInstType')
        if m.get('Endpoints') is not None:
            temp_model = DescribeDrdsDBClusterResponseBodyDbInstanceEndpoints()
            self.endpoints = temp_model.from_map(m['Endpoints'])
        if m.get('Engine') is not None:
            self.engine = m.get('Engine')
        if m.get('EngineVersion') is not None:
            self.engine_version = m.get('EngineVersion')
        if m.get('ExpireTime') is not None:
            self.expire_time = m.get('ExpireTime')
        if m.get('NetworkType') is not None:
            self.network_type = m.get('NetworkType')
        if m.get('PayType') is not None:
            self.pay_type = m.get('PayType')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        if m.get('RdsInstType') is not None:
            self.rds_inst_type = m.get('RdsInstType')
        if m.get('ReadMode') is not None:
            self.read_mode = m.get('ReadMode')
        if m.get('RemainDays') is not None:
            self.remain_days = m.get('RemainDays')
        return self


class DescribeDrdsDBClusterResponseBody(TeaModel):
    def __init__(
        self,
        db_instance: DescribeDrdsDBClusterResponseBodyDbInstance = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.db_instance = db_instance
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.db_instance:
            self.db_instance.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_instance is not None:
            result['DbInstance'] = self.db_instance.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbInstance') is not None:
            temp_model = DescribeDrdsDBClusterResponseBodyDbInstance()
            self.db_instance = temp_model.from_map(m['DbInstance'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeDrdsDBClusterResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsDBClusterResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsDBClusterResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsDBIpWhiteListRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        group_name: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.group_name = group_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        return self


class DescribeDrdsDBIpWhiteListResponseBodyIpWhiteList(TeaModel):
    def __init__(
        self,
        ip: List[str] = None,
    ):
        self.ip = ip

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.ip is not None:
            result['Ip'] = self.ip
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Ip') is not None:
            self.ip = m.get('Ip')
        return self


class DescribeDrdsDBIpWhiteListResponseBody(TeaModel):
    def __init__(
        self,
        ip_white_list: DescribeDrdsDBIpWhiteListResponseBodyIpWhiteList = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.ip_white_list = ip_white_list
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.ip_white_list:
            self.ip_white_list.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.ip_white_list is not None:
            result['IpWhiteList'] = self.ip_white_list.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('IpWhiteList') is not None:
            temp_model = DescribeDrdsDBIpWhiteListResponseBodyIpWhiteList()
            self.ip_white_list = temp_model.from_map(m['IpWhiteList'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeDrdsDBIpWhiteListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsDBIpWhiteListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsDBIpWhiteListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsDBsRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
        page_number: int = None,
        page_size: int = None,
        region_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id
        self.page_number = page_number
        self.page_size = page_size
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeDrdsDBsResponseBodyDataDb(TeaModel):
    def __init__(
        self,
        create_time: str = None,
        db_inst_type: str = None,
        db_name: str = None,
        mode: str = None,
        schema: str = None,
        status: str = None,
    ):
        self.create_time = create_time
        self.db_inst_type = db_inst_type
        self.db_name = db_name
        self.mode = mode
        self.schema = schema
        self.status = status

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.db_inst_type is not None:
            result['DbInstType'] = self.db_inst_type
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.mode is not None:
            result['Mode'] = self.mode
        if self.schema is not None:
            result['Schema'] = self.schema
        if self.status is not None:
            result['Status'] = self.status
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('DbInstType') is not None:
            self.db_inst_type = m.get('DbInstType')
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        if m.get('Schema') is not None:
            self.schema = m.get('Schema')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        return self


class DescribeDrdsDBsResponseBodyData(TeaModel):
    def __init__(
        self,
        db: List[DescribeDrdsDBsResponseBodyDataDb] = None,
    ):
        self.db = db

    def validate(self):
        if self.db:
            for k in self.db:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Db'] = []
        if self.db is not None:
            for k in self.db:
                result['Db'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.db = []
        if m.get('Db') is not None:
            for k in m.get('Db'):
                temp_model = DescribeDrdsDBsResponseBodyDataDb()
                self.db.append(temp_model.from_map(k))
        return self


class DescribeDrdsDBsResponseBody(TeaModel):
    def __init__(
        self,
        data: DescribeDrdsDBsResponseBodyData = None,
        page_number: str = None,
        page_size: str = None,
        request_id: str = None,
        success: bool = None,
        total: str = None,
    ):
        self.data = data
        self.page_number = page_number
        self.page_size = page_size
        self.request_id = request_id
        self.success = success
        self.total = total

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = DescribeDrdsDBsResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class DescribeDrdsDBsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsDBsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsDBsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsDbInstanceRequest(TeaModel):
    def __init__(
        self,
        db_instance_id: str = None,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_instance_id = db_instance_id
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_instance_id is not None:
            result['DbInstanceId'] = self.db_instance_id
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbInstanceId') is not None:
            self.db_instance_id = m.get('DbInstanceId')
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeDrdsDbInstanceResponseBodyDbInstanceReadOnlyInstancesReadOnlyInstance(TeaModel):
    def __init__(
        self,
        connect_url: str = None,
        dbinstance_id: str = None,
        dbinstance_status: str = None,
        db_inst_type: str = None,
        dm_instance_id: str = None,
        engine: str = None,
        engine_version: str = None,
        expire_time: str = None,
        network_type: str = None,
        pay_type: str = None,
        port: int = None,
        rds_inst_type: str = None,
        read_weight: int = None,
        remain_days: str = None,
        version_action: int = None,
    ):
        self.connect_url = connect_url
        self.dbinstance_id = dbinstance_id
        self.dbinstance_status = dbinstance_status
        self.db_inst_type = db_inst_type
        self.dm_instance_id = dm_instance_id
        self.engine = engine
        self.engine_version = engine_version
        self.expire_time = expire_time
        self.network_type = network_type
        self.pay_type = pay_type
        self.port = port
        self.rds_inst_type = rds_inst_type
        self.read_weight = read_weight
        self.remain_days = remain_days
        self.version_action = version_action

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.connect_url is not None:
            result['ConnectUrl'] = self.connect_url
        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id
        if self.dbinstance_status is not None:
            result['DBInstanceStatus'] = self.dbinstance_status
        if self.db_inst_type is not None:
            result['DbInstType'] = self.db_inst_type
        if self.dm_instance_id is not None:
            result['DmInstanceId'] = self.dm_instance_id
        if self.engine is not None:
            result['Engine'] = self.engine
        if self.engine_version is not None:
            result['EngineVersion'] = self.engine_version
        if self.expire_time is not None:
            result['ExpireTime'] = self.expire_time
        if self.network_type is not None:
            result['NetworkType'] = self.network_type
        if self.pay_type is not None:
            result['PayType'] = self.pay_type
        if self.port is not None:
            result['Port'] = self.port
        if self.rds_inst_type is not None:
            result['RdsInstType'] = self.rds_inst_type
        if self.read_weight is not None:
            result['ReadWeight'] = self.read_weight
        if self.remain_days is not None:
            result['RemainDays'] = self.remain_days
        if self.version_action is not None:
            result['VersionAction'] = self.version_action
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConnectUrl') is not None:
            self.connect_url = m.get('ConnectUrl')
        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')
        if m.get('DBInstanceStatus') is not None:
            self.dbinstance_status = m.get('DBInstanceStatus')
        if m.get('DbInstType') is not None:
            self.db_inst_type = m.get('DbInstType')
        if m.get('DmInstanceId') is not None:
            self.dm_instance_id = m.get('DmInstanceId')
        if m.get('Engine') is not None:
            self.engine = m.get('Engine')
        if m.get('EngineVersion') is not None:
            self.engine_version = m.get('EngineVersion')
        if m.get('ExpireTime') is not None:
            self.expire_time = m.get('ExpireTime')
        if m.get('NetworkType') is not None:
            self.network_type = m.get('NetworkType')
        if m.get('PayType') is not None:
            self.pay_type = m.get('PayType')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        if m.get('RdsInstType') is not None:
            self.rds_inst_type = m.get('RdsInstType')
        if m.get('ReadWeight') is not None:
            self.read_weight = m.get('ReadWeight')
        if m.get('RemainDays') is not None:
            self.remain_days = m.get('RemainDays')
        if m.get('VersionAction') is not None:
            self.version_action = m.get('VersionAction')
        return self


class DescribeDrdsDbInstanceResponseBodyDbInstanceReadOnlyInstances(TeaModel):
    def __init__(
        self,
        read_only_instance: List[DescribeDrdsDbInstanceResponseBodyDbInstanceReadOnlyInstancesReadOnlyInstance] = None,
    ):
        self.read_only_instance = read_only_instance

    def validate(self):
        if self.read_only_instance:
            for k in self.read_only_instance:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['ReadOnlyInstance'] = []
        if self.read_only_instance is not None:
            for k in self.read_only_instance:
                result['ReadOnlyInstance'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.read_only_instance = []
        if m.get('ReadOnlyInstance') is not None:
            for k in m.get('ReadOnlyInstance'):
                temp_model = DescribeDrdsDbInstanceResponseBodyDbInstanceReadOnlyInstancesReadOnlyInstance()
                self.read_only_instance.append(temp_model.from_map(k))
        return self


class DescribeDrdsDbInstanceResponseBodyDbInstance(TeaModel):
    def __init__(
        self,
        connect_url: str = None,
        dbinstance_id: str = None,
        dbinstance_status: str = None,
        db_inst_type: str = None,
        dm_instance_id: str = None,
        engine: str = None,
        engine_version: str = None,
        expire_time: str = None,
        network_type: str = None,
        pay_type: str = None,
        port: int = None,
        rds_inst_type: str = None,
        read_only_instances: DescribeDrdsDbInstanceResponseBodyDbInstanceReadOnlyInstances = None,
        read_weight: int = None,
        remain_days: str = None,
    ):
        self.connect_url = connect_url
        self.dbinstance_id = dbinstance_id
        self.dbinstance_status = dbinstance_status
        self.db_inst_type = db_inst_type
        self.dm_instance_id = dm_instance_id
        self.engine = engine
        self.engine_version = engine_version
        self.expire_time = expire_time
        self.network_type = network_type
        self.pay_type = pay_type
        self.port = port
        self.rds_inst_type = rds_inst_type
        self.read_only_instances = read_only_instances
        self.read_weight = read_weight
        self.remain_days = remain_days

    def validate(self):
        if self.read_only_instances:
            self.read_only_instances.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.connect_url is not None:
            result['ConnectUrl'] = self.connect_url
        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id
        if self.dbinstance_status is not None:
            result['DBInstanceStatus'] = self.dbinstance_status
        if self.db_inst_type is not None:
            result['DbInstType'] = self.db_inst_type
        if self.dm_instance_id is not None:
            result['DmInstanceId'] = self.dm_instance_id
        if self.engine is not None:
            result['Engine'] = self.engine
        if self.engine_version is not None:
            result['EngineVersion'] = self.engine_version
        if self.expire_time is not None:
            result['ExpireTime'] = self.expire_time
        if self.network_type is not None:
            result['NetworkType'] = self.network_type
        if self.pay_type is not None:
            result['PayType'] = self.pay_type
        if self.port is not None:
            result['Port'] = self.port
        if self.rds_inst_type is not None:
            result['RdsInstType'] = self.rds_inst_type
        if self.read_only_instances is not None:
            result['ReadOnlyInstances'] = self.read_only_instances.to_map()
        if self.read_weight is not None:
            result['ReadWeight'] = self.read_weight
        if self.remain_days is not None:
            result['RemainDays'] = self.remain_days
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConnectUrl') is not None:
            self.connect_url = m.get('ConnectUrl')
        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')
        if m.get('DBInstanceStatus') is not None:
            self.dbinstance_status = m.get('DBInstanceStatus')
        if m.get('DbInstType') is not None:
            self.db_inst_type = m.get('DbInstType')
        if m.get('DmInstanceId') is not None:
            self.dm_instance_id = m.get('DmInstanceId')
        if m.get('Engine') is not None:
            self.engine = m.get('Engine')
        if m.get('EngineVersion') is not None:
            self.engine_version = m.get('EngineVersion')
        if m.get('ExpireTime') is not None:
            self.expire_time = m.get('ExpireTime')
        if m.get('NetworkType') is not None:
            self.network_type = m.get('NetworkType')
        if m.get('PayType') is not None:
            self.pay_type = m.get('PayType')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        if m.get('RdsInstType') is not None:
            self.rds_inst_type = m.get('RdsInstType')
        if m.get('ReadOnlyInstances') is not None:
            temp_model = DescribeDrdsDbInstanceResponseBodyDbInstanceReadOnlyInstances()
            self.read_only_instances = temp_model.from_map(m['ReadOnlyInstances'])
        if m.get('ReadWeight') is not None:
            self.read_weight = m.get('ReadWeight')
        if m.get('RemainDays') is not None:
            self.remain_days = m.get('RemainDays')
        return self


class DescribeDrdsDbInstanceResponseBody(TeaModel):
    def __init__(
        self,
        db_instance: DescribeDrdsDbInstanceResponseBodyDbInstance = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.db_instance = db_instance
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.db_instance:
            self.db_instance.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_instance is not None:
            result['DbInstance'] = self.db_instance.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbInstance') is not None:
            temp_model = DescribeDrdsDbInstanceResponseBodyDbInstance()
            self.db_instance = temp_model.from_map(m['DbInstance'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeDrdsDbInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsDbInstanceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsDbInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsDbInstancesRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeDrdsDbInstancesResponseBodyDbInstancesDbInstanceReadOnlyInstancesReadOnlyInstance(TeaModel):
    def __init__(
        self,
        connect_url: str = None,
        dbinstance_status: str = None,
        db_inst_type: str = None,
        dm_instance_id: str = None,
        engine: str = None,
        engine_version: str = None,
        expire_time: str = None,
        instance_name: str = None,
        network_type: str = None,
        pay_type: str = None,
        port: int = None,
        rds_inst_type: str = None,
        read_weight: int = None,
        remain_days: int = None,
    ):
        self.connect_url = connect_url
        self.dbinstance_status = dbinstance_status
        self.db_inst_type = db_inst_type
        self.dm_instance_id = dm_instance_id
        self.engine = engine
        self.engine_version = engine_version
        self.expire_time = expire_time
        self.instance_name = instance_name
        self.network_type = network_type
        self.pay_type = pay_type
        self.port = port
        self.rds_inst_type = rds_inst_type
        self.read_weight = read_weight
        self.remain_days = remain_days

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.connect_url is not None:
            result['ConnectUrl'] = self.connect_url
        if self.dbinstance_status is not None:
            result['DBInstanceStatus'] = self.dbinstance_status
        if self.db_inst_type is not None:
            result['DbInstType'] = self.db_inst_type
        if self.dm_instance_id is not None:
            result['DmInstanceId'] = self.dm_instance_id
        if self.engine is not None:
            result['Engine'] = self.engine
        if self.engine_version is not None:
            result['EngineVersion'] = self.engine_version
        if self.expire_time is not None:
            result['ExpireTime'] = self.expire_time
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.network_type is not None:
            result['NetworkType'] = self.network_type
        if self.pay_type is not None:
            result['PayType'] = self.pay_type
        if self.port is not None:
            result['Port'] = self.port
        if self.rds_inst_type is not None:
            result['RdsInstType'] = self.rds_inst_type
        if self.read_weight is not None:
            result['ReadWeight'] = self.read_weight
        if self.remain_days is not None:
            result['RemainDays'] = self.remain_days
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConnectUrl') is not None:
            self.connect_url = m.get('ConnectUrl')
        if m.get('DBInstanceStatus') is not None:
            self.dbinstance_status = m.get('DBInstanceStatus')
        if m.get('DbInstType') is not None:
            self.db_inst_type = m.get('DbInstType')
        if m.get('DmInstanceId') is not None:
            self.dm_instance_id = m.get('DmInstanceId')
        if m.get('Engine') is not None:
            self.engine = m.get('Engine')
        if m.get('EngineVersion') is not None:
            self.engine_version = m.get('EngineVersion')
        if m.get('ExpireTime') is not None:
            self.expire_time = m.get('ExpireTime')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('NetworkType') is not None:
            self.network_type = m.get('NetworkType')
        if m.get('PayType') is not None:
            self.pay_type = m.get('PayType')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        if m.get('RdsInstType') is not None:
            self.rds_inst_type = m.get('RdsInstType')
        if m.get('ReadWeight') is not None:
            self.read_weight = m.get('ReadWeight')
        if m.get('RemainDays') is not None:
            self.remain_days = m.get('RemainDays')
        return self


class DescribeDrdsDbInstancesResponseBodyDbInstancesDbInstanceReadOnlyInstances(TeaModel):
    def __init__(
        self,
        read_only_instance: List[DescribeDrdsDbInstancesResponseBodyDbInstancesDbInstanceReadOnlyInstancesReadOnlyInstance] = None,
    ):
        self.read_only_instance = read_only_instance

    def validate(self):
        if self.read_only_instance:
            for k in self.read_only_instance:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['ReadOnlyInstance'] = []
        if self.read_only_instance is not None:
            for k in self.read_only_instance:
                result['ReadOnlyInstance'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.read_only_instance = []
        if m.get('ReadOnlyInstance') is not None:
            for k in m.get('ReadOnlyInstance'):
                temp_model = DescribeDrdsDbInstancesResponseBodyDbInstancesDbInstanceReadOnlyInstancesReadOnlyInstance()
                self.read_only_instance.append(temp_model.from_map(k))
        return self


class DescribeDrdsDbInstancesResponseBodyDbInstancesDbInstance(TeaModel):
    def __init__(
        self,
        connect_url: str = None,
        dbinstance_id: str = None,
        dbinstance_status: str = None,
        db_inst_type: str = None,
        dm_instance_id: str = None,
        engine: str = None,
        engine_version: str = None,
        expire_time: str = None,
        network_type: str = None,
        pay_type: str = None,
        port: int = None,
        rds_inst_type: str = None,
        read_only_instances: DescribeDrdsDbInstancesResponseBodyDbInstancesDbInstanceReadOnlyInstances = None,
        read_weight: int = None,
        remain_days: int = None,
    ):
        self.connect_url = connect_url
        self.dbinstance_id = dbinstance_id
        self.dbinstance_status = dbinstance_status
        self.db_inst_type = db_inst_type
        self.dm_instance_id = dm_instance_id
        self.engine = engine
        self.engine_version = engine_version
        self.expire_time = expire_time
        self.network_type = network_type
        self.pay_type = pay_type
        self.port = port
        self.rds_inst_type = rds_inst_type
        self.read_only_instances = read_only_instances
        self.read_weight = read_weight
        self.remain_days = remain_days

    def validate(self):
        if self.read_only_instances:
            self.read_only_instances.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.connect_url is not None:
            result['ConnectUrl'] = self.connect_url
        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id
        if self.dbinstance_status is not None:
            result['DBInstanceStatus'] = self.dbinstance_status
        if self.db_inst_type is not None:
            result['DbInstType'] = self.db_inst_type
        if self.dm_instance_id is not None:
            result['DmInstanceId'] = self.dm_instance_id
        if self.engine is not None:
            result['Engine'] = self.engine
        if self.engine_version is not None:
            result['EngineVersion'] = self.engine_version
        if self.expire_time is not None:
            result['ExpireTime'] = self.expire_time
        if self.network_type is not None:
            result['NetworkType'] = self.network_type
        if self.pay_type is not None:
            result['PayType'] = self.pay_type
        if self.port is not None:
            result['Port'] = self.port
        if self.rds_inst_type is not None:
            result['RdsInstType'] = self.rds_inst_type
        if self.read_only_instances is not None:
            result['ReadOnlyInstances'] = self.read_only_instances.to_map()
        if self.read_weight is not None:
            result['ReadWeight'] = self.read_weight
        if self.remain_days is not None:
            result['RemainDays'] = self.remain_days
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConnectUrl') is not None:
            self.connect_url = m.get('ConnectUrl')
        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')
        if m.get('DBInstanceStatus') is not None:
            self.dbinstance_status = m.get('DBInstanceStatus')
        if m.get('DbInstType') is not None:
            self.db_inst_type = m.get('DbInstType')
        if m.get('DmInstanceId') is not None:
            self.dm_instance_id = m.get('DmInstanceId')
        if m.get('Engine') is not None:
            self.engine = m.get('Engine')
        if m.get('EngineVersion') is not None:
            self.engine_version = m.get('EngineVersion')
        if m.get('ExpireTime') is not None:
            self.expire_time = m.get('ExpireTime')
        if m.get('NetworkType') is not None:
            self.network_type = m.get('NetworkType')
        if m.get('PayType') is not None:
            self.pay_type = m.get('PayType')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        if m.get('RdsInstType') is not None:
            self.rds_inst_type = m.get('RdsInstType')
        if m.get('ReadOnlyInstances') is not None:
            temp_model = DescribeDrdsDbInstancesResponseBodyDbInstancesDbInstanceReadOnlyInstances()
            self.read_only_instances = temp_model.from_map(m['ReadOnlyInstances'])
        if m.get('ReadWeight') is not None:
            self.read_weight = m.get('ReadWeight')
        if m.get('RemainDays') is not None:
            self.remain_days = m.get('RemainDays')
        return self


class DescribeDrdsDbInstancesResponseBodyDbInstances(TeaModel):
    def __init__(
        self,
        db_instance: List[DescribeDrdsDbInstancesResponseBodyDbInstancesDbInstance] = None,
    ):
        self.db_instance = db_instance

    def validate(self):
        if self.db_instance:
            for k in self.db_instance:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['DbInstance'] = []
        if self.db_instance is not None:
            for k in self.db_instance:
                result['DbInstance'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.db_instance = []
        if m.get('DbInstance') is not None:
            for k in m.get('DbInstance'):
                temp_model = DescribeDrdsDbInstancesResponseBodyDbInstancesDbInstance()
                self.db_instance.append(temp_model.from_map(k))
        return self


class DescribeDrdsDbInstancesResponseBody(TeaModel):
    def __init__(
        self,
        db_instances: DescribeDrdsDbInstancesResponseBodyDbInstances = None,
        page_number: str = None,
        page_size: str = None,
        request_id: str = None,
        success: bool = None,
        total: str = None,
    ):
        self.db_instances = db_instances
        self.page_number = page_number
        self.page_size = page_size
        self.request_id = request_id
        self.success = success
        self.total = total

    def validate(self):
        if self.db_instances:
            self.db_instances.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_instances is not None:
            result['DbInstances'] = self.db_instances.to_map()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbInstances') is not None:
            temp_model = DescribeDrdsDbInstancesResponseBodyDbInstances()
            self.db_instances = temp_model.from_map(m['DbInstances'])
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class DescribeDrdsDbInstancesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsDbInstancesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsDbInstancesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsDbRdsNameListRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeDrdsDbRdsNameListResponseBodyInstanceNameList(TeaModel):
    def __init__(
        self,
        instance_name: List[str] = None,
    ):
        self.instance_name = instance_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        return self


class DescribeDrdsDbRdsNameListResponseBody(TeaModel):
    def __init__(
        self,
        instance_name_list: DescribeDrdsDbRdsNameListResponseBodyInstanceNameList = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.instance_name_list = instance_name_list
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.instance_name_list:
            self.instance_name_list.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_name_list is not None:
            result['InstanceNameList'] = self.instance_name_list.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceNameList') is not None:
            temp_model = DescribeDrdsDbRdsNameListResponseBodyInstanceNameList()
            self.instance_name_list = temp_model.from_map(m['InstanceNameList'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeDrdsDbRdsNameListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsDbRdsNameListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsDbRdsNameListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsDbTasksRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        task_type: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.task_type = task_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.task_type is not None:
            result['TaskType'] = self.task_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')
        return self


class DescribeDrdsDbTasksResponseBodyTasksTask(TeaModel):
    def __init__(
        self,
        allow_cancel: bool = None,
        db_compute_length: int = None,
        detail_task_id: str = None,
        expand_type: str = None,
        gmt_create: int = None,
        label: str = None,
        parent_job_id: str = None,
        progress: int = None,
        show_progress: bool = None,
        target_id: int = None,
        task_detail: str = None,
        task_name: str = None,
        task_phase: str = None,
        task_status: int = None,
        task_type: int = None,
        tb_compute_length: int = None,
    ):
        self.allow_cancel = allow_cancel
        self.db_compute_length = db_compute_length
        self.detail_task_id = detail_task_id
        self.expand_type = expand_type
        self.gmt_create = gmt_create
        self.label = label
        self.parent_job_id = parent_job_id
        self.progress = progress
        self.show_progress = show_progress
        self.target_id = target_id
        self.task_detail = task_detail
        self.task_name = task_name
        self.task_phase = task_phase
        self.task_status = task_status
        self.task_type = task_type
        self.tb_compute_length = tb_compute_length

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.allow_cancel is not None:
            result['AllowCancel'] = self.allow_cancel
        if self.db_compute_length is not None:
            result['DbComputeLength'] = self.db_compute_length
        if self.detail_task_id is not None:
            result['DetailTaskId'] = self.detail_task_id
        if self.expand_type is not None:
            result['ExpandType'] = self.expand_type
        if self.gmt_create is not None:
            result['GmtCreate'] = self.gmt_create
        if self.label is not None:
            result['Label'] = self.label
        if self.parent_job_id is not None:
            result['ParentJobId'] = self.parent_job_id
        if self.progress is not None:
            result['Progress'] = self.progress
        if self.show_progress is not None:
            result['ShowProgress'] = self.show_progress
        if self.target_id is not None:
            result['TargetId'] = self.target_id
        if self.task_detail is not None:
            result['TaskDetail'] = self.task_detail
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.task_phase is not None:
            result['TaskPhase'] = self.task_phase
        if self.task_status is not None:
            result['TaskStatus'] = self.task_status
        if self.task_type is not None:
            result['TaskType'] = self.task_type
        if self.tb_compute_length is not None:
            result['TbComputeLength'] = self.tb_compute_length
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AllowCancel') is not None:
            self.allow_cancel = m.get('AllowCancel')
        if m.get('DbComputeLength') is not None:
            self.db_compute_length = m.get('DbComputeLength')
        if m.get('DetailTaskId') is not None:
            self.detail_task_id = m.get('DetailTaskId')
        if m.get('ExpandType') is not None:
            self.expand_type = m.get('ExpandType')
        if m.get('GmtCreate') is not None:
            self.gmt_create = m.get('GmtCreate')
        if m.get('Label') is not None:
            self.label = m.get('Label')
        if m.get('ParentJobId') is not None:
            self.parent_job_id = m.get('ParentJobId')
        if m.get('Progress') is not None:
            self.progress = m.get('Progress')
        if m.get('ShowProgress') is not None:
            self.show_progress = m.get('ShowProgress')
        if m.get('TargetId') is not None:
            self.target_id = m.get('TargetId')
        if m.get('TaskDetail') is not None:
            self.task_detail = m.get('TaskDetail')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('TaskPhase') is not None:
            self.task_phase = m.get('TaskPhase')
        if m.get('TaskStatus') is not None:
            self.task_status = m.get('TaskStatus')
        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')
        if m.get('TbComputeLength') is not None:
            self.tb_compute_length = m.get('TbComputeLength')
        return self


class DescribeDrdsDbTasksResponseBodyTasks(TeaModel):
    def __init__(
        self,
        task: List[DescribeDrdsDbTasksResponseBodyTasksTask] = None,
    ):
        self.task = task

    def validate(self):
        if self.task:
            for k in self.task:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Task'] = []
        if self.task is not None:
            for k in self.task:
                result['Task'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.task = []
        if m.get('Task') is not None:
            for k in m.get('Task'):
                temp_model = DescribeDrdsDbTasksResponseBodyTasksTask()
                self.task.append(temp_model.from_map(k))
        return self


class DescribeDrdsDbTasksResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
        tasks: DescribeDrdsDbTasksResponseBodyTasks = None,
    ):
        self.request_id = request_id
        self.success = success
        self.tasks = tasks

    def validate(self):
        if self.tasks:
            self.tasks.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.tasks is not None:
            result['Tasks'] = self.tasks.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Tasks') is not None:
            temp_model = DescribeDrdsDbTasksResponseBodyTasks()
            self.tasks = temp_model.from_map(m['Tasks'])
        return self


class DescribeDrdsDbTasksResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsDbTasksResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsDbTasksResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsInstanceRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
        region_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeDrdsInstanceResponseBodyDataReadOnlyDBInstanceIds(TeaModel):
    def __init__(
        self,
        read_only_dbinstance_id: List[str] = None,
    ):
        self.read_only_dbinstance_id = read_only_dbinstance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.read_only_dbinstance_id is not None:
            result['ReadOnlyDBInstanceId'] = self.read_only_dbinstance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ReadOnlyDBInstanceId') is not None:
            self.read_only_dbinstance_id = m.get('ReadOnlyDBInstanceId')
        return self


class DescribeDrdsInstanceResponseBodyDataVipsVip(TeaModel):
    def __init__(
        self,
        dns: str = None,
        expire_days: int = None,
        port: str = None,
        type: str = None,
        vpc_id: str = None,
        vswitch_id: str = None,
    ):
        self.dns = dns
        self.expire_days = expire_days
        self.port = port
        self.type = type
        self.vpc_id = vpc_id
        self.vswitch_id = vswitch_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dns is not None:
            result['Dns'] = self.dns
        if self.expire_days is not None:
            result['ExpireDays'] = self.expire_days
        if self.port is not None:
            result['Port'] = self.port
        if self.type is not None:
            result['Type'] = self.type
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.vswitch_id is not None:
            result['VswitchId'] = self.vswitch_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Dns') is not None:
            self.dns = m.get('Dns')
        if m.get('ExpireDays') is not None:
            self.expire_days = m.get('ExpireDays')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VswitchId') is not None:
            self.vswitch_id = m.get('VswitchId')
        return self


class DescribeDrdsInstanceResponseBodyDataVips(TeaModel):
    def __init__(
        self,
        vip: List[DescribeDrdsInstanceResponseBodyDataVipsVip] = None,
    ):
        self.vip = vip

    def validate(self):
        if self.vip:
            for k in self.vip:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Vip'] = []
        if self.vip is not None:
            for k in self.vip:
                result['Vip'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.vip = []
        if m.get('Vip') is not None:
            for k in m.get('Vip'):
                temp_model = DescribeDrdsInstanceResponseBodyDataVipsVip()
                self.vip.append(temp_model.from_map(k))
        return self


class DescribeDrdsInstanceResponseBodyData(TeaModel):
    def __init__(
        self,
        commodity_code: str = None,
        create_time: int = None,
        description: str = None,
        drds_instance_id: str = None,
        expire_date: int = None,
        inst_role: str = None,
        instance_series: str = None,
        instance_spec: str = None,
        label: str = None,
        machine_type: str = None,
        master_instance_id: str = None,
        mysql_version: int = None,
        network_type: str = None,
        order_instance_id: str = None,
        product_version: str = None,
        read_only_dbinstance_ids: DescribeDrdsInstanceResponseBodyDataReadOnlyDBInstanceIds = None,
        region_id: str = None,
        resource_group_id: str = None,
        status: str = None,
        storage_type: str = None,
        type: str = None,
        version: int = None,
        version_action: str = None,
        vips: DescribeDrdsInstanceResponseBodyDataVips = None,
        vpc_cloud_instance_id: str = None,
        zone_id: str = None,
    ):
        self.commodity_code = commodity_code
        self.create_time = create_time
        self.description = description
        self.drds_instance_id = drds_instance_id
        self.expire_date = expire_date
        self.inst_role = inst_role
        self.instance_series = instance_series
        self.instance_spec = instance_spec
        self.label = label
        self.machine_type = machine_type
        self.master_instance_id = master_instance_id
        self.mysql_version = mysql_version
        self.network_type = network_type
        self.order_instance_id = order_instance_id
        self.product_version = product_version
        self.read_only_dbinstance_ids = read_only_dbinstance_ids
        self.region_id = region_id
        self.resource_group_id = resource_group_id
        self.status = status
        self.storage_type = storage_type
        self.type = type
        self.version = version
        self.version_action = version_action
        self.vips = vips
        self.vpc_cloud_instance_id = vpc_cloud_instance_id
        self.zone_id = zone_id

    def validate(self):
        if self.read_only_dbinstance_ids:
            self.read_only_dbinstance_ids.validate()
        if self.vips:
            self.vips.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.commodity_code is not None:
            result['CommodityCode'] = self.commodity_code
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.description is not None:
            result['Description'] = self.description
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.expire_date is not None:
            result['ExpireDate'] = self.expire_date
        if self.inst_role is not None:
            result['InstRole'] = self.inst_role
        if self.instance_series is not None:
            result['InstanceSeries'] = self.instance_series
        if self.instance_spec is not None:
            result['InstanceSpec'] = self.instance_spec
        if self.label is not None:
            result['Label'] = self.label
        if self.machine_type is not None:
            result['MachineType'] = self.machine_type
        if self.master_instance_id is not None:
            result['MasterInstanceId'] = self.master_instance_id
        if self.mysql_version is not None:
            result['MysqlVersion'] = self.mysql_version
        if self.network_type is not None:
            result['NetworkType'] = self.network_type
        if self.order_instance_id is not None:
            result['OrderInstanceId'] = self.order_instance_id
        if self.product_version is not None:
            result['ProductVersion'] = self.product_version
        if self.read_only_dbinstance_ids is not None:
            result['ReadOnlyDBInstanceIds'] = self.read_only_dbinstance_ids.to_map()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.status is not None:
            result['Status'] = self.status
        if self.storage_type is not None:
            result['StorageType'] = self.storage_type
        if self.type is not None:
            result['Type'] = self.type
        if self.version is not None:
            result['Version'] = self.version
        if self.version_action is not None:
            result['VersionAction'] = self.version_action
        if self.vips is not None:
            result['Vips'] = self.vips.to_map()
        if self.vpc_cloud_instance_id is not None:
            result['VpcCloudInstanceId'] = self.vpc_cloud_instance_id
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CommodityCode') is not None:
            self.commodity_code = m.get('CommodityCode')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('ExpireDate') is not None:
            self.expire_date = m.get('ExpireDate')
        if m.get('InstRole') is not None:
            self.inst_role = m.get('InstRole')
        if m.get('InstanceSeries') is not None:
            self.instance_series = m.get('InstanceSeries')
        if m.get('InstanceSpec') is not None:
            self.instance_spec = m.get('InstanceSpec')
        if m.get('Label') is not None:
            self.label = m.get('Label')
        if m.get('MachineType') is not None:
            self.machine_type = m.get('MachineType')
        if m.get('MasterInstanceId') is not None:
            self.master_instance_id = m.get('MasterInstanceId')
        if m.get('MysqlVersion') is not None:
            self.mysql_version = m.get('MysqlVersion')
        if m.get('NetworkType') is not None:
            self.network_type = m.get('NetworkType')
        if m.get('OrderInstanceId') is not None:
            self.order_instance_id = m.get('OrderInstanceId')
        if m.get('ProductVersion') is not None:
            self.product_version = m.get('ProductVersion')
        if m.get('ReadOnlyDBInstanceIds') is not None:
            temp_model = DescribeDrdsInstanceResponseBodyDataReadOnlyDBInstanceIds()
            self.read_only_dbinstance_ids = temp_model.from_map(m['ReadOnlyDBInstanceIds'])
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('StorageType') is not None:
            self.storage_type = m.get('StorageType')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('VersionAction') is not None:
            self.version_action = m.get('VersionAction')
        if m.get('Vips') is not None:
            temp_model = DescribeDrdsInstanceResponseBodyDataVips()
            self.vips = temp_model.from_map(m['Vips'])
        if m.get('VpcCloudInstanceId') is not None:
            self.vpc_cloud_instance_id = m.get('VpcCloudInstanceId')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class DescribeDrdsInstanceResponseBody(TeaModel):
    def __init__(
        self,
        data: DescribeDrdsInstanceResponseBodyData = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = DescribeDrdsInstanceResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeDrdsInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsInstanceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsInstanceDbMonitorRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        end_time: int = None,
        key: str = None,
        region_id: str = None,
        start_time: int = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.end_time = end_time
        self.key = key
        self.region_id = region_id
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.key is not None:
            result['Key'] = self.key
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class DescribeDrdsInstanceDbMonitorResponseBodyDataValues(TeaModel):
    def __init__(
        self,
        date: int = None,
        value: str = None,
    ):
        self.date = date
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.date is not None:
            result['Date'] = self.date
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Date') is not None:
            self.date = m.get('Date')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class DescribeDrdsInstanceDbMonitorResponseBodyData(TeaModel):
    def __init__(
        self,
        key: str = None,
        unit: str = None,
        values: List[DescribeDrdsInstanceDbMonitorResponseBodyDataValues] = None,
    ):
        self.key = key
        self.unit = unit
        self.values = values

    def validate(self):
        if self.values:
            for k in self.values:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.unit is not None:
            result['Unit'] = self.unit
        result['Values'] = []
        if self.values is not None:
            for k in self.values:
                result['Values'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Unit') is not None:
            self.unit = m.get('Unit')
        self.values = []
        if m.get('Values') is not None:
            for k in m.get('Values'):
                temp_model = DescribeDrdsInstanceDbMonitorResponseBodyDataValues()
                self.values.append(temp_model.from_map(k))
        return self


class DescribeDrdsInstanceDbMonitorResponseBody(TeaModel):
    def __init__(
        self,
        data: List[DescribeDrdsInstanceDbMonitorResponseBodyData] = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Data'] = []
        if self.data is not None:
            for k in self.data:
                result['Data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = DescribeDrdsInstanceDbMonitorResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeDrdsInstanceDbMonitorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsInstanceDbMonitorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsInstanceDbMonitorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsInstanceLevelTasksRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeDrdsInstanceLevelTasksResponseBodyTasksTask(TeaModel):
    def __init__(
        self,
        allow_cancel: bool = None,
        err_msg: str = None,
        gmt_create: int = None,
        progress: int = None,
        progress_description: str = None,
        show_progress: bool = None,
        target_id: int = None,
        task_name: str = None,
        task_phase: str = None,
        task_status: int = None,
        task_type: int = None,
    ):
        self.allow_cancel = allow_cancel
        self.err_msg = err_msg
        self.gmt_create = gmt_create
        self.progress = progress
        self.progress_description = progress_description
        self.show_progress = show_progress
        self.target_id = target_id
        self.task_name = task_name
        self.task_phase = task_phase
        self.task_status = task_status
        self.task_type = task_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.allow_cancel is not None:
            result['AllowCancel'] = self.allow_cancel
        if self.err_msg is not None:
            result['ErrMsg'] = self.err_msg
        if self.gmt_create is not None:
            result['GmtCreate'] = self.gmt_create
        if self.progress is not None:
            result['Progress'] = self.progress
        if self.progress_description is not None:
            result['ProgressDescription'] = self.progress_description
        if self.show_progress is not None:
            result['ShowProgress'] = self.show_progress
        if self.target_id is not None:
            result['TargetId'] = self.target_id
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        if self.task_phase is not None:
            result['TaskPhase'] = self.task_phase
        if self.task_status is not None:
            result['TaskStatus'] = self.task_status
        if self.task_type is not None:
            result['TaskType'] = self.task_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AllowCancel') is not None:
            self.allow_cancel = m.get('AllowCancel')
        if m.get('ErrMsg') is not None:
            self.err_msg = m.get('ErrMsg')
        if m.get('GmtCreate') is not None:
            self.gmt_create = m.get('GmtCreate')
        if m.get('Progress') is not None:
            self.progress = m.get('Progress')
        if m.get('ProgressDescription') is not None:
            self.progress_description = m.get('ProgressDescription')
        if m.get('ShowProgress') is not None:
            self.show_progress = m.get('ShowProgress')
        if m.get('TargetId') is not None:
            self.target_id = m.get('TargetId')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        if m.get('TaskPhase') is not None:
            self.task_phase = m.get('TaskPhase')
        if m.get('TaskStatus') is not None:
            self.task_status = m.get('TaskStatus')
        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')
        return self


class DescribeDrdsInstanceLevelTasksResponseBodyTasks(TeaModel):
    def __init__(
        self,
        task: List[DescribeDrdsInstanceLevelTasksResponseBodyTasksTask] = None,
    ):
        self.task = task

    def validate(self):
        if self.task:
            for k in self.task:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Task'] = []
        if self.task is not None:
            for k in self.task:
                result['Task'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.task = []
        if m.get('Task') is not None:
            for k in m.get('Task'):
                temp_model = DescribeDrdsInstanceLevelTasksResponseBodyTasksTask()
                self.task.append(temp_model.from_map(k))
        return self


class DescribeDrdsInstanceLevelTasksResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
        tasks: DescribeDrdsInstanceLevelTasksResponseBodyTasks = None,
    ):
        self.request_id = request_id
        self.success = success
        self.tasks = tasks

    def validate(self):
        if self.tasks:
            self.tasks.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.tasks is not None:
            result['Tasks'] = self.tasks.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Tasks') is not None:
            temp_model = DescribeDrdsInstanceLevelTasksResponseBodyTasks()
            self.tasks = temp_model.from_map(m['Tasks'])
        return self


class DescribeDrdsInstanceLevelTasksResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsInstanceLevelTasksResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsInstanceLevelTasksResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsInstanceMonitorRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
        end_time: int = None,
        key: str = None,
        period_multiple: int = None,
        region_id: str = None,
        start_time: int = None,
    ):
        self.drds_instance_id = drds_instance_id
        self.end_time = end_time
        self.key = key
        self.period_multiple = period_multiple
        self.region_id = region_id
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.key is not None:
            result['Key'] = self.key
        if self.period_multiple is not None:
            result['PeriodMultiple'] = self.period_multiple
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('PeriodMultiple') is not None:
            self.period_multiple = m.get('PeriodMultiple')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class DescribeDrdsInstanceMonitorResponseBodyDataValues(TeaModel):
    def __init__(
        self,
        date: int = None,
        value: str = None,
    ):
        self.date = date
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.date is not None:
            result['Date'] = self.date
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Date') is not None:
            self.date = m.get('Date')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class DescribeDrdsInstanceMonitorResponseBodyData(TeaModel):
    def __init__(
        self,
        key: str = None,
        node_num: int = None,
        unit: str = None,
        values: List[DescribeDrdsInstanceMonitorResponseBodyDataValues] = None,
    ):
        self.key = key
        self.node_num = node_num
        self.unit = unit
        self.values = values

    def validate(self):
        if self.values:
            for k in self.values:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.node_num is not None:
            result['NodeNum'] = self.node_num
        if self.unit is not None:
            result['Unit'] = self.unit
        result['Values'] = []
        if self.values is not None:
            for k in self.values:
                result['Values'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('NodeNum') is not None:
            self.node_num = m.get('NodeNum')
        if m.get('Unit') is not None:
            self.unit = m.get('Unit')
        self.values = []
        if m.get('Values') is not None:
            for k in m.get('Values'):
                temp_model = DescribeDrdsInstanceMonitorResponseBodyDataValues()
                self.values.append(temp_model.from_map(k))
        return self


class DescribeDrdsInstanceMonitorResponseBody(TeaModel):
    def __init__(
        self,
        data: List[DescribeDrdsInstanceMonitorResponseBodyData] = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Data'] = []
        if self.data is not None:
            for k in self.data:
                result['Data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = DescribeDrdsInstanceMonitorResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeDrdsInstanceMonitorResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsInstanceMonitorResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsInstanceMonitorResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsInstanceVersionRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
        region_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeDrdsInstanceVersionResponseBodyData(TeaModel):
    def __init__(
        self,
        instance_version: str = None,
        newest_version: str = None,
    ):
        self.instance_version = instance_version
        self.newest_version = newest_version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_version is not None:
            result['InstanceVersion'] = self.instance_version
        if self.newest_version is not None:
            result['NewestVersion'] = self.newest_version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceVersion') is not None:
            self.instance_version = m.get('InstanceVersion')
        if m.get('NewestVersion') is not None:
            self.newest_version = m.get('NewestVersion')
        return self


class DescribeDrdsInstanceVersionResponseBody(TeaModel):
    def __init__(
        self,
        data: DescribeDrdsInstanceVersionResponseBodyData = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = DescribeDrdsInstanceVersionResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeDrdsInstanceVersionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsInstanceVersionResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsInstanceVersionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsInstancesRequestTag(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class DescribeDrdsInstancesRequest(TeaModel):
    def __init__(
        self,
        description: str = None,
        expired: bool = None,
        mix: bool = None,
        page_number: int = None,
        page_size: int = None,
        product_version: str = None,
        region_id: str = None,
        resource_group_id: str = None,
        tag: List[DescribeDrdsInstancesRequestTag] = None,
        type: str = None,
    ):
        self.description = description
        self.expired = expired
        self.mix = mix
        self.page_number = page_number
        self.page_size = page_size
        self.product_version = product_version
        self.region_id = region_id
        self.resource_group_id = resource_group_id
        self.tag = tag
        self.type = type

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.description is not None:
            result['Description'] = self.description
        if self.expired is not None:
            result['Expired'] = self.expired
        if self.mix is not None:
            result['Mix'] = self.mix
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.product_version is not None:
            result['ProductVersion'] = self.product_version
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        if self.type is not None:
            result['Type'] = self.type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Expired') is not None:
            self.expired = m.get('Expired')
        if m.get('Mix') is not None:
            self.mix = m.get('Mix')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('ProductVersion') is not None:
            self.product_version = m.get('ProductVersion')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = DescribeDrdsInstancesRequestTag()
                self.tag.append(temp_model.from_map(k))
        if m.get('Type') is not None:
            self.type = m.get('Type')
        return self


class DescribeDrdsInstancesResponseBodyInstancesInstanceReadOnlyDBInstanceIds(TeaModel):
    def __init__(
        self,
        read_only_dbinstance_id: List[str] = None,
    ):
        self.read_only_dbinstance_id = read_only_dbinstance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.read_only_dbinstance_id is not None:
            result['ReadOnlyDBInstanceId'] = self.read_only_dbinstance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ReadOnlyDBInstanceId') is not None:
            self.read_only_dbinstance_id = m.get('ReadOnlyDBInstanceId')
        return self


class DescribeDrdsInstancesResponseBodyInstancesInstanceVipsVip(TeaModel):
    def __init__(
        self,
        ip: str = None,
        port: str = None,
        type: str = None,
        vpc_id: str = None,
        vswitch_id: str = None,
    ):
        self.ip = ip
        self.port = port
        self.type = type
        self.vpc_id = vpc_id
        self.vswitch_id = vswitch_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.ip is not None:
            result['IP'] = self.ip
        if self.port is not None:
            result['Port'] = self.port
        if self.type is not None:
            result['Type'] = self.type
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.vswitch_id is not None:
            result['VswitchId'] = self.vswitch_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('IP') is not None:
            self.ip = m.get('IP')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VswitchId') is not None:
            self.vswitch_id = m.get('VswitchId')
        return self


class DescribeDrdsInstancesResponseBodyInstancesInstanceVips(TeaModel):
    def __init__(
        self,
        vip: List[DescribeDrdsInstancesResponseBodyInstancesInstanceVipsVip] = None,
    ):
        self.vip = vip

    def validate(self):
        if self.vip:
            for k in self.vip:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Vip'] = []
        if self.vip is not None:
            for k in self.vip:
                result['Vip'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.vip = []
        if m.get('Vip') is not None:
            for k in m.get('Vip'):
                temp_model = DescribeDrdsInstancesResponseBodyInstancesInstanceVipsVip()
                self.vip.append(temp_model.from_map(k))
        return self


class DescribeDrdsInstancesResponseBodyInstancesInstance(TeaModel):
    def __init__(
        self,
        commodity_code: str = None,
        create_time: int = None,
        description: str = None,
        drds_instance_id: str = None,
        expire_date: int = None,
        inst_role: str = None,
        instance_series: str = None,
        instance_spec: str = None,
        label: str = None,
        machine_type: str = None,
        master_instance_id: str = None,
        network_type: str = None,
        order_instance_id: str = None,
        product_version: str = None,
        read_only_dbinstance_ids: DescribeDrdsInstancesResponseBodyInstancesInstanceReadOnlyDBInstanceIds = None,
        region_id: str = None,
        resource_group_id: str = None,
        status: str = None,
        type: str = None,
        version: int = None,
        version_action: str = None,
        vips: DescribeDrdsInstancesResponseBodyInstancesInstanceVips = None,
        vpc_cloud_instance_id: str = None,
        vpc_id: str = None,
        zone_id: str = None,
    ):
        self.commodity_code = commodity_code
        self.create_time = create_time
        self.description = description
        self.drds_instance_id = drds_instance_id
        self.expire_date = expire_date
        self.inst_role = inst_role
        self.instance_series = instance_series
        self.instance_spec = instance_spec
        self.label = label
        self.machine_type = machine_type
        self.master_instance_id = master_instance_id
        self.network_type = network_type
        self.order_instance_id = order_instance_id
        self.product_version = product_version
        self.read_only_dbinstance_ids = read_only_dbinstance_ids
        self.region_id = region_id
        self.resource_group_id = resource_group_id
        self.status = status
        self.type = type
        self.version = version
        self.version_action = version_action
        self.vips = vips
        self.vpc_cloud_instance_id = vpc_cloud_instance_id
        self.vpc_id = vpc_id
        self.zone_id = zone_id

    def validate(self):
        if self.read_only_dbinstance_ids:
            self.read_only_dbinstance_ids.validate()
        if self.vips:
            self.vips.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.commodity_code is not None:
            result['CommodityCode'] = self.commodity_code
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.description is not None:
            result['Description'] = self.description
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.expire_date is not None:
            result['ExpireDate'] = self.expire_date
        if self.inst_role is not None:
            result['InstRole'] = self.inst_role
        if self.instance_series is not None:
            result['InstanceSeries'] = self.instance_series
        if self.instance_spec is not None:
            result['InstanceSpec'] = self.instance_spec
        if self.label is not None:
            result['Label'] = self.label
        if self.machine_type is not None:
            result['MachineType'] = self.machine_type
        if self.master_instance_id is not None:
            result['MasterInstanceId'] = self.master_instance_id
        if self.network_type is not None:
            result['NetworkType'] = self.network_type
        if self.order_instance_id is not None:
            result['OrderInstanceId'] = self.order_instance_id
        if self.product_version is not None:
            result['ProductVersion'] = self.product_version
        if self.read_only_dbinstance_ids is not None:
            result['ReadOnlyDBInstanceIds'] = self.read_only_dbinstance_ids.to_map()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_group_id is not None:
            result['ResourceGroupId'] = self.resource_group_id
        if self.status is not None:
            result['Status'] = self.status
        if self.type is not None:
            result['Type'] = self.type
        if self.version is not None:
            result['Version'] = self.version
        if self.version_action is not None:
            result['VersionAction'] = self.version_action
        if self.vips is not None:
            result['Vips'] = self.vips.to_map()
        if self.vpc_cloud_instance_id is not None:
            result['VpcCloudInstanceId'] = self.vpc_cloud_instance_id
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.zone_id is not None:
            result['ZoneId'] = self.zone_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CommodityCode') is not None:
            self.commodity_code = m.get('CommodityCode')
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('ExpireDate') is not None:
            self.expire_date = m.get('ExpireDate')
        if m.get('InstRole') is not None:
            self.inst_role = m.get('InstRole')
        if m.get('InstanceSeries') is not None:
            self.instance_series = m.get('InstanceSeries')
        if m.get('InstanceSpec') is not None:
            self.instance_spec = m.get('InstanceSpec')
        if m.get('Label') is not None:
            self.label = m.get('Label')
        if m.get('MachineType') is not None:
            self.machine_type = m.get('MachineType')
        if m.get('MasterInstanceId') is not None:
            self.master_instance_id = m.get('MasterInstanceId')
        if m.get('NetworkType') is not None:
            self.network_type = m.get('NetworkType')
        if m.get('OrderInstanceId') is not None:
            self.order_instance_id = m.get('OrderInstanceId')
        if m.get('ProductVersion') is not None:
            self.product_version = m.get('ProductVersion')
        if m.get('ReadOnlyDBInstanceIds') is not None:
            temp_model = DescribeDrdsInstancesResponseBodyInstancesInstanceReadOnlyDBInstanceIds()
            self.read_only_dbinstance_ids = temp_model.from_map(m['ReadOnlyDBInstanceIds'])
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceGroupId') is not None:
            self.resource_group_id = m.get('ResourceGroupId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Type') is not None:
            self.type = m.get('Type')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        if m.get('VersionAction') is not None:
            self.version_action = m.get('VersionAction')
        if m.get('Vips') is not None:
            temp_model = DescribeDrdsInstancesResponseBodyInstancesInstanceVips()
            self.vips = temp_model.from_map(m['Vips'])
        if m.get('VpcCloudInstanceId') is not None:
            self.vpc_cloud_instance_id = m.get('VpcCloudInstanceId')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('ZoneId') is not None:
            self.zone_id = m.get('ZoneId')
        return self


class DescribeDrdsInstancesResponseBodyInstances(TeaModel):
    def __init__(
        self,
        instance: List[DescribeDrdsInstancesResponseBodyInstancesInstance] = None,
    ):
        self.instance = instance

    def validate(self):
        if self.instance:
            for k in self.instance:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Instance'] = []
        if self.instance is not None:
            for k in self.instance:
                result['Instance'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.instance = []
        if m.get('Instance') is not None:
            for k in m.get('Instance'):
                temp_model = DescribeDrdsInstancesResponseBodyInstancesInstance()
                self.instance.append(temp_model.from_map(k))
        return self


class DescribeDrdsInstancesResponseBody(TeaModel):
    def __init__(
        self,
        instances: DescribeDrdsInstancesResponseBodyInstances = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        total: int = None,
    ):
        self.instances = instances
        self.page_number = page_number
        self.page_size = page_size
        self.request_id = request_id
        self.total = total

    def validate(self):
        if self.instances:
            self.instances.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instances is not None:
            result['Instances'] = self.instances.to_map()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Instances') is not None:
            temp_model = DescribeDrdsInstancesResponseBodyInstances()
            self.instances = temp_model.from_map(m['Instances'])
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class DescribeDrdsInstancesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsInstancesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsInstancesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsParamsRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        param_level: str = None,
        region_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.param_level = param_level
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.param_level is not None:
            result['ParamLevel'] = self.param_level
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('ParamLevel') is not None:
            self.param_level = m.get('ParamLevel')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeDrdsParamsResponseBodyList(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        need_restart: bool = None,
        param_default_value: str = None,
        param_desc: str = None,
        param_english_name: str = None,
        param_level: str = None,
        param_name: str = None,
        param_ranges: str = None,
        param_type: str = None,
        param_value: str = None,
        param_variable_name: str = None,
    ):
        self.db_name = db_name
        self.need_restart = need_restart
        self.param_default_value = param_default_value
        self.param_desc = param_desc
        self.param_english_name = param_english_name
        self.param_level = param_level
        self.param_name = param_name
        self.param_ranges = param_ranges
        self.param_type = param_type
        self.param_value = param_value
        self.param_variable_name = param_variable_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.need_restart is not None:
            result['NeedRestart'] = self.need_restart
        if self.param_default_value is not None:
            result['ParamDefaultValue'] = self.param_default_value
        if self.param_desc is not None:
            result['ParamDesc'] = self.param_desc
        if self.param_english_name is not None:
            result['ParamEnglishName'] = self.param_english_name
        if self.param_level is not None:
            result['ParamLevel'] = self.param_level
        if self.param_name is not None:
            result['ParamName'] = self.param_name
        if self.param_ranges is not None:
            result['ParamRanges'] = self.param_ranges
        if self.param_type is not None:
            result['ParamType'] = self.param_type
        if self.param_value is not None:
            result['ParamValue'] = self.param_value
        if self.param_variable_name is not None:
            result['ParamVariableName'] = self.param_variable_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('NeedRestart') is not None:
            self.need_restart = m.get('NeedRestart')
        if m.get('ParamDefaultValue') is not None:
            self.param_default_value = m.get('ParamDefaultValue')
        if m.get('ParamDesc') is not None:
            self.param_desc = m.get('ParamDesc')
        if m.get('ParamEnglishName') is not None:
            self.param_english_name = m.get('ParamEnglishName')
        if m.get('ParamLevel') is not None:
            self.param_level = m.get('ParamLevel')
        if m.get('ParamName') is not None:
            self.param_name = m.get('ParamName')
        if m.get('ParamRanges') is not None:
            self.param_ranges = m.get('ParamRanges')
        if m.get('ParamType') is not None:
            self.param_type = m.get('ParamType')
        if m.get('ParamValue') is not None:
            self.param_value = m.get('ParamValue')
        if m.get('ParamVariableName') is not None:
            self.param_variable_name = m.get('ParamVariableName')
        return self


class DescribeDrdsParamsResponseBody(TeaModel):
    def __init__(
        self,
        list: List[DescribeDrdsParamsResponseBodyList] = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.list = list
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.list:
            for k in self.list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['List'] = []
        if self.list is not None:
            for k in self.list:
                result['List'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.list = []
        if m.get('List') is not None:
            for k in m.get('List'):
                temp_model = DescribeDrdsParamsResponseBodyList()
                self.list.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeDrdsParamsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsParamsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsParamsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsRdsInstancesRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeDrdsRdsInstancesResponseBodyDbInstancesDbInstance(TeaModel):
    def __init__(
        self,
        connect_url: str = None,
        dbinstance_cpu: str = None,
        dbinstance_class_type: str = None,
        dbinstance_id: str = None,
        dbinstance_memory: int = None,
        dbinstance_status: str = None,
        dbinstance_storage: int = None,
        db_inst_type: str = None,
        dm_instance_id: str = None,
        engine: str = None,
        engine_version: str = None,
        network_type: str = None,
        pay_type: str = None,
        port: int = None,
        rds_inst_type: str = None,
        read_weight: int = None,
    ):
        self.connect_url = connect_url
        self.dbinstance_cpu = dbinstance_cpu
        self.dbinstance_class_type = dbinstance_class_type
        self.dbinstance_id = dbinstance_id
        self.dbinstance_memory = dbinstance_memory
        self.dbinstance_status = dbinstance_status
        self.dbinstance_storage = dbinstance_storage
        self.db_inst_type = db_inst_type
        self.dm_instance_id = dm_instance_id
        self.engine = engine
        self.engine_version = engine_version
        self.network_type = network_type
        self.pay_type = pay_type
        self.port = port
        self.rds_inst_type = rds_inst_type
        self.read_weight = read_weight

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.connect_url is not None:
            result['ConnectUrl'] = self.connect_url
        if self.dbinstance_cpu is not None:
            result['DBInstanceCPU'] = self.dbinstance_cpu
        if self.dbinstance_class_type is not None:
            result['DBInstanceClassType'] = self.dbinstance_class_type
        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id
        if self.dbinstance_memory is not None:
            result['DBInstanceMemory'] = self.dbinstance_memory
        if self.dbinstance_status is not None:
            result['DBInstanceStatus'] = self.dbinstance_status
        if self.dbinstance_storage is not None:
            result['DBInstanceStorage'] = self.dbinstance_storage
        if self.db_inst_type is not None:
            result['DbInstType'] = self.db_inst_type
        if self.dm_instance_id is not None:
            result['DmInstanceId'] = self.dm_instance_id
        if self.engine is not None:
            result['Engine'] = self.engine
        if self.engine_version is not None:
            result['EngineVersion'] = self.engine_version
        if self.network_type is not None:
            result['NetworkType'] = self.network_type
        if self.pay_type is not None:
            result['PayType'] = self.pay_type
        if self.port is not None:
            result['Port'] = self.port
        if self.rds_inst_type is not None:
            result['RdsInstType'] = self.rds_inst_type
        if self.read_weight is not None:
            result['ReadWeight'] = self.read_weight
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ConnectUrl') is not None:
            self.connect_url = m.get('ConnectUrl')
        if m.get('DBInstanceCPU') is not None:
            self.dbinstance_cpu = m.get('DBInstanceCPU')
        if m.get('DBInstanceClassType') is not None:
            self.dbinstance_class_type = m.get('DBInstanceClassType')
        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')
        if m.get('DBInstanceMemory') is not None:
            self.dbinstance_memory = m.get('DBInstanceMemory')
        if m.get('DBInstanceStatus') is not None:
            self.dbinstance_status = m.get('DBInstanceStatus')
        if m.get('DBInstanceStorage') is not None:
            self.dbinstance_storage = m.get('DBInstanceStorage')
        if m.get('DbInstType') is not None:
            self.db_inst_type = m.get('DbInstType')
        if m.get('DmInstanceId') is not None:
            self.dm_instance_id = m.get('DmInstanceId')
        if m.get('Engine') is not None:
            self.engine = m.get('Engine')
        if m.get('EngineVersion') is not None:
            self.engine_version = m.get('EngineVersion')
        if m.get('NetworkType') is not None:
            self.network_type = m.get('NetworkType')
        if m.get('PayType') is not None:
            self.pay_type = m.get('PayType')
        if m.get('Port') is not None:
            self.port = m.get('Port')
        if m.get('RdsInstType') is not None:
            self.rds_inst_type = m.get('RdsInstType')
        if m.get('ReadWeight') is not None:
            self.read_weight = m.get('ReadWeight')
        return self


class DescribeDrdsRdsInstancesResponseBodyDbInstances(TeaModel):
    def __init__(
        self,
        db_instance: List[DescribeDrdsRdsInstancesResponseBodyDbInstancesDbInstance] = None,
    ):
        self.db_instance = db_instance

    def validate(self):
        if self.db_instance:
            for k in self.db_instance:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['DbInstance'] = []
        if self.db_instance is not None:
            for k in self.db_instance:
                result['DbInstance'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.db_instance = []
        if m.get('DbInstance') is not None:
            for k in m.get('DbInstance'):
                temp_model = DescribeDrdsRdsInstancesResponseBodyDbInstancesDbInstance()
                self.db_instance.append(temp_model.from_map(k))
        return self


class DescribeDrdsRdsInstancesResponseBody(TeaModel):
    def __init__(
        self,
        db_instances: DescribeDrdsRdsInstancesResponseBodyDbInstances = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.db_instances = db_instances
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.db_instances:
            self.db_instances.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_instances is not None:
            result['DbInstances'] = self.db_instances.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbInstances') is not None:
            temp_model = DescribeDrdsRdsInstancesResponseBodyDbInstances()
            self.db_instances = temp_model.from_map(m['DbInstances'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeDrdsRdsInstancesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsRdsInstancesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsRdsInstancesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsShardingDbsRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        db_name_pattern: str = None,
        drds_instance_id: str = None,
        page_number: int = None,
        page_size: int = None,
    ):
        self.db_name = db_name
        self.db_name_pattern = db_name_pattern
        self.drds_instance_id = drds_instance_id
        self.page_number = page_number
        self.page_size = page_size

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.db_name_pattern is not None:
            result['DbNamePattern'] = self.db_name_pattern
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DbNamePattern') is not None:
            self.db_name_pattern = m.get('DbNamePattern')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        return self


class DescribeDrdsShardingDbsResponseBodyShardingDbsShardingDb(TeaModel):
    def __init__(
        self,
        blocking_timeout: int = None,
        connect_url: str = None,
        connection_properties: str = None,
        db_instance_id: str = None,
        db_status: str = None,
        db_type: str = None,
        group_name: str = None,
        idle_time_out: int = None,
        max_pool_size: int = None,
        min_pool_size: int = None,
        prepared_statement_cache_size: int = None,
        sharding_db_name: str = None,
        user_name: str = None,
    ):
        self.blocking_timeout = blocking_timeout
        self.connect_url = connect_url
        self.connection_properties = connection_properties
        self.db_instance_id = db_instance_id
        self.db_status = db_status
        self.db_type = db_type
        self.group_name = group_name
        self.idle_time_out = idle_time_out
        self.max_pool_size = max_pool_size
        self.min_pool_size = min_pool_size
        self.prepared_statement_cache_size = prepared_statement_cache_size
        self.sharding_db_name = sharding_db_name
        self.user_name = user_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.blocking_timeout is not None:
            result['BlockingTimeout'] = self.blocking_timeout
        if self.connect_url is not None:
            result['ConnectUrl'] = self.connect_url
        if self.connection_properties is not None:
            result['ConnectionProperties'] = self.connection_properties
        if self.db_instance_id is not None:
            result['DbInstanceId'] = self.db_instance_id
        if self.db_status is not None:
            result['DbStatus'] = self.db_status
        if self.db_type is not None:
            result['DbType'] = self.db_type
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.idle_time_out is not None:
            result['IdleTimeOut'] = self.idle_time_out
        if self.max_pool_size is not None:
            result['MaxPoolSize'] = self.max_pool_size
        if self.min_pool_size is not None:
            result['MinPoolSize'] = self.min_pool_size
        if self.prepared_statement_cache_size is not None:
            result['PreparedStatementCacheSize'] = self.prepared_statement_cache_size
        if self.sharding_db_name is not None:
            result['ShardingDbName'] = self.sharding_db_name
        if self.user_name is not None:
            result['UserName'] = self.user_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BlockingTimeout') is not None:
            self.blocking_timeout = m.get('BlockingTimeout')
        if m.get('ConnectUrl') is not None:
            self.connect_url = m.get('ConnectUrl')
        if m.get('ConnectionProperties') is not None:
            self.connection_properties = m.get('ConnectionProperties')
        if m.get('DbInstanceId') is not None:
            self.db_instance_id = m.get('DbInstanceId')
        if m.get('DbStatus') is not None:
            self.db_status = m.get('DbStatus')
        if m.get('DbType') is not None:
            self.db_type = m.get('DbType')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('IdleTimeOut') is not None:
            self.idle_time_out = m.get('IdleTimeOut')
        if m.get('MaxPoolSize') is not None:
            self.max_pool_size = m.get('MaxPoolSize')
        if m.get('MinPoolSize') is not None:
            self.min_pool_size = m.get('MinPoolSize')
        if m.get('PreparedStatementCacheSize') is not None:
            self.prepared_statement_cache_size = m.get('PreparedStatementCacheSize')
        if m.get('ShardingDbName') is not None:
            self.sharding_db_name = m.get('ShardingDbName')
        if m.get('UserName') is not None:
            self.user_name = m.get('UserName')
        return self


class DescribeDrdsShardingDbsResponseBodyShardingDbs(TeaModel):
    def __init__(
        self,
        sharding_db: List[DescribeDrdsShardingDbsResponseBodyShardingDbsShardingDb] = None,
    ):
        self.sharding_db = sharding_db

    def validate(self):
        if self.sharding_db:
            for k in self.sharding_db:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['ShardingDb'] = []
        if self.sharding_db is not None:
            for k in self.sharding_db:
                result['ShardingDb'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.sharding_db = []
        if m.get('ShardingDb') is not None:
            for k in m.get('ShardingDb'):
                temp_model = DescribeDrdsShardingDbsResponseBodyShardingDbsShardingDb()
                self.sharding_db.append(temp_model.from_map(k))
        return self


class DescribeDrdsShardingDbsResponseBody(TeaModel):
    def __init__(
        self,
        page_number: str = None,
        page_size: str = None,
        request_id: str = None,
        sharding_dbs: DescribeDrdsShardingDbsResponseBodyShardingDbs = None,
        success: bool = None,
        total: str = None,
    ):
        self.page_number = page_number
        self.page_size = page_size
        self.request_id = request_id
        self.sharding_dbs = sharding_dbs
        self.success = success
        self.total = total

    def validate(self):
        if self.sharding_dbs:
            self.sharding_dbs.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.sharding_dbs is not None:
            result['ShardingDbs'] = self.sharding_dbs.to_map()
        if self.success is not None:
            result['Success'] = self.success
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('ShardingDbs') is not None:
            temp_model = DescribeDrdsShardingDbsResponseBodyShardingDbs()
            self.sharding_dbs = temp_model.from_map(m['ShardingDbs'])
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class DescribeDrdsShardingDbsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsShardingDbsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsShardingDbsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsSlowSqlsRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        end_time: int = None,
        exe_time: int = None,
        page_number: int = None,
        page_size: int = None,
        start_time: int = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.end_time = end_time
        self.exe_time = exe_time
        self.page_number = page_number
        self.page_size = page_size
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.exe_time is not None:
            result['ExeTime'] = self.exe_time
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('ExeTime') is not None:
            self.exe_time = m.get('ExeTime')
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class DescribeDrdsSlowSqlsResponseBodyItemsItem(TeaModel):
    def __init__(
        self,
        host: str = None,
        response_time: int = None,
        schema: str = None,
        send_time: int = None,
        sql: str = None,
    ):
        self.host = host
        self.response_time = response_time
        self.schema = schema
        self.send_time = send_time
        self.sql = sql

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.host is not None:
            result['Host'] = self.host
        if self.response_time is not None:
            result['ResponseTime'] = self.response_time
        if self.schema is not None:
            result['Schema'] = self.schema
        if self.send_time is not None:
            result['SendTime'] = self.send_time
        if self.sql is not None:
            result['Sql'] = self.sql
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Host') is not None:
            self.host = m.get('Host')
        if m.get('ResponseTime') is not None:
            self.response_time = m.get('ResponseTime')
        if m.get('Schema') is not None:
            self.schema = m.get('Schema')
        if m.get('SendTime') is not None:
            self.send_time = m.get('SendTime')
        if m.get('Sql') is not None:
            self.sql = m.get('Sql')
        return self


class DescribeDrdsSlowSqlsResponseBodyItems(TeaModel):
    def __init__(
        self,
        item: List[DescribeDrdsSlowSqlsResponseBodyItemsItem] = None,
    ):
        self.item = item

    def validate(self):
        if self.item:
            for k in self.item:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Item'] = []
        if self.item is not None:
            for k in self.item:
                result['Item'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.item = []
        if m.get('Item') is not None:
            for k in m.get('Item'):
                temp_model = DescribeDrdsSlowSqlsResponseBodyItemsItem()
                self.item.append(temp_model.from_map(k))
        return self


class DescribeDrdsSlowSqlsResponseBody(TeaModel):
    def __init__(
        self,
        items: DescribeDrdsSlowSqlsResponseBodyItems = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        success: bool = None,
        total: int = None,
    ):
        self.items = items
        self.page_number = page_number
        self.page_size = page_size
        self.request_id = request_id
        self.success = success
        self.total = total

    def validate(self):
        if self.items:
            self.items.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.items is not None:
            result['Items'] = self.items.to_map()
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Items') is not None:
            temp_model = DescribeDrdsSlowSqlsResponseBodyItems()
            self.items = temp_model.from_map(m['Items'])
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class DescribeDrdsSlowSqlsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsSlowSqlsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsSlowSqlsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsSqlAuditStatusRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeDrdsSqlAuditStatusResponseBodyDataData(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        detailed: str = None,
        enabled: str = None,
        extra_ali_uid: int = None,
        extra_sls_log_store: str = None,
        extra_sls_project: str = None,
        extra_write_enabled: bool = None,
    ):
        self.db_name = db_name
        self.detailed = detailed
        self.enabled = enabled
        self.extra_ali_uid = extra_ali_uid
        self.extra_sls_log_store = extra_sls_log_store
        self.extra_sls_project = extra_sls_project
        self.extra_write_enabled = extra_write_enabled

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.detailed is not None:
            result['Detailed'] = self.detailed
        if self.enabled is not None:
            result['Enabled'] = self.enabled
        if self.extra_ali_uid is not None:
            result['ExtraAliUid'] = self.extra_ali_uid
        if self.extra_sls_log_store is not None:
            result['ExtraSlsLogStore'] = self.extra_sls_log_store
        if self.extra_sls_project is not None:
            result['ExtraSlsProject'] = self.extra_sls_project
        if self.extra_write_enabled is not None:
            result['ExtraWriteEnabled'] = self.extra_write_enabled
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('Detailed') is not None:
            self.detailed = m.get('Detailed')
        if m.get('Enabled') is not None:
            self.enabled = m.get('Enabled')
        if m.get('ExtraAliUid') is not None:
            self.extra_ali_uid = m.get('ExtraAliUid')
        if m.get('ExtraSlsLogStore') is not None:
            self.extra_sls_log_store = m.get('ExtraSlsLogStore')
        if m.get('ExtraSlsProject') is not None:
            self.extra_sls_project = m.get('ExtraSlsProject')
        if m.get('ExtraWriteEnabled') is not None:
            self.extra_write_enabled = m.get('ExtraWriteEnabled')
        return self


class DescribeDrdsSqlAuditStatusResponseBodyData(TeaModel):
    def __init__(
        self,
        data: List[DescribeDrdsSqlAuditStatusResponseBodyDataData] = None,
    ):
        self.data = data

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Data'] = []
        if self.data is not None:
            for k in self.data:
                result['Data'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = DescribeDrdsSqlAuditStatusResponseBodyDataData()
                self.data.append(temp_model.from_map(k))
        return self


class DescribeDrdsSqlAuditStatusResponseBody(TeaModel):
    def __init__(
        self,
        data: DescribeDrdsSqlAuditStatusResponseBodyData = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = DescribeDrdsSqlAuditStatusResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeDrdsSqlAuditStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsSqlAuditStatusResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsSqlAuditStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeDrdsTasksRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        task_type: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.task_type = task_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.task_type is not None:
            result['TaskType'] = self.task_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')
        return self


class DescribeDrdsTasksResponseBodyTasksTask(TeaModel):
    def __init__(
        self,
        content: str = None,
        id: int = None,
        state: str = None,
    ):
        self.content = content
        self.id = id
        self.state = state

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.content is not None:
            result['Content'] = self.content
        if self.id is not None:
            result['Id'] = self.id
        if self.state is not None:
            result['State'] = self.state
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Content') is not None:
            self.content = m.get('Content')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('State') is not None:
            self.state = m.get('State')
        return self


class DescribeDrdsTasksResponseBodyTasks(TeaModel):
    def __init__(
        self,
        task: List[DescribeDrdsTasksResponseBodyTasksTask] = None,
    ):
        self.task = task

    def validate(self):
        if self.task:
            for k in self.task:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Task'] = []
        if self.task is not None:
            for k in self.task:
                result['Task'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.task = []
        if m.get('Task') is not None:
            for k in m.get('Task'):
                temp_model = DescribeDrdsTasksResponseBodyTasksTask()
                self.task.append(temp_model.from_map(k))
        return self


class DescribeDrdsTasksResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
        tasks: DescribeDrdsTasksResponseBodyTasks = None,
    ):
        self.request_id = request_id
        self.success = success
        self.tasks = tasks

    def validate(self):
        if self.tasks:
            self.tasks.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.tasks is not None:
            result['Tasks'] = self.tasks.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Tasks') is not None:
            temp_model = DescribeDrdsTasksResponseBodyTasks()
            self.tasks = temp_model.from_map(m['Tasks'])
        return self


class DescribeDrdsTasksResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeDrdsTasksResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeDrdsTasksResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeExpandLogicTableInfoListRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeExpandLogicTableInfoListResponseBodyDataData(TeaModel):
    def __init__(
        self,
        shard_db_key: str = None,
        shard_tb_key: str = None,
        table_name: str = None,
    ):
        self.shard_db_key = shard_db_key
        self.shard_tb_key = shard_tb_key
        self.table_name = table_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.shard_db_key is not None:
            result['ShardDbKey'] = self.shard_db_key
        if self.shard_tb_key is not None:
            result['ShardTbKey'] = self.shard_tb_key
        if self.table_name is not None:
            result['TableName'] = self.table_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ShardDbKey') is not None:
            self.shard_db_key = m.get('ShardDbKey')
        if m.get('ShardTbKey') is not None:
            self.shard_tb_key = m.get('ShardTbKey')
        if m.get('TableName') is not None:
            self.table_name = m.get('TableName')
        return self


class DescribeExpandLogicTableInfoListResponseBodyData(TeaModel):
    def __init__(
        self,
        data: List[DescribeExpandLogicTableInfoListResponseBodyDataData] = None,
    ):
        self.data = data

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['data'] = []
        if self.data is not None:
            for k in self.data:
                result['data'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('data') is not None:
            for k in m.get('data'):
                temp_model = DescribeExpandLogicTableInfoListResponseBodyDataData()
                self.data.append(temp_model.from_map(k))
        return self


class DescribeExpandLogicTableInfoListResponseBody(TeaModel):
    def __init__(
        self,
        data: DescribeExpandLogicTableInfoListResponseBodyData = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = DescribeExpandLogicTableInfoListResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeExpandLogicTableInfoListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeExpandLogicTableInfoListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeExpandLogicTableInfoListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeHotDbListRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeHotDbListResponseBodyDataListInstanceDbHotDbList(TeaModel):
    def __init__(
        self,
        data: List[str] = None,
    ):
        self.data = data

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['data'] = self.data
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('data') is not None:
            self.data = m.get('data')
        return self


class DescribeHotDbListResponseBodyDataListInstanceDb(TeaModel):
    def __init__(
        self,
        hot_db_list: DescribeHotDbListResponseBodyDataListInstanceDbHotDbList = None,
        instance_name: str = None,
    ):
        self.hot_db_list = hot_db_list
        self.instance_name = instance_name

    def validate(self):
        if self.hot_db_list:
            self.hot_db_list.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.hot_db_list is not None:
            result['HotDbList'] = self.hot_db_list.to_map()
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('HotDbList') is not None:
            temp_model = DescribeHotDbListResponseBodyDataListInstanceDbHotDbList()
            self.hot_db_list = temp_model.from_map(m['HotDbList'])
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        return self


class DescribeHotDbListResponseBodyDataList(TeaModel):
    def __init__(
        self,
        instance_db: List[DescribeHotDbListResponseBodyDataListInstanceDb] = None,
    ):
        self.instance_db = instance_db

    def validate(self):
        if self.instance_db:
            for k in self.instance_db:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['InstanceDb'] = []
        if self.instance_db is not None:
            for k in self.instance_db:
                result['InstanceDb'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.instance_db = []
        if m.get('InstanceDb') is not None:
            for k in m.get('InstanceDb'):
                temp_model = DescribeHotDbListResponseBodyDataListInstanceDb()
                self.instance_db.append(temp_model.from_map(k))
        return self


class DescribeHotDbListResponseBodyData(TeaModel):
    def __init__(
        self,
        list: DescribeHotDbListResponseBodyDataList = None,
        random_code: str = None,
    ):
        self.list = list
        self.random_code = random_code

    def validate(self):
        if self.list:
            self.list.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.list is not None:
            result['List'] = self.list.to_map()
        if self.random_code is not None:
            result['RandomCode'] = self.random_code
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('List') is not None:
            temp_model = DescribeHotDbListResponseBodyDataList()
            self.list = temp_model.from_map(m['List'])
        if m.get('RandomCode') is not None:
            self.random_code = m.get('RandomCode')
        return self


class DescribeHotDbListResponseBody(TeaModel):
    def __init__(
        self,
        data: DescribeHotDbListResponseBodyData = None,
        msg: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.msg = msg
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.msg is not None:
            result['Msg'] = self.msg
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = DescribeHotDbListResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('Msg') is not None:
            self.msg = m.get('Msg')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeHotDbListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeHotDbListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeHotDbListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeInstDbLogInfoRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeInstDbLogInfoResponseBodyLogTimeRange(TeaModel):
    def __init__(
        self,
        support_latest_time: int = None,
        support_oldest_time: int = None,
    ):
        self.support_latest_time = support_latest_time
        self.support_oldest_time = support_oldest_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.support_latest_time is not None:
            result['SupportLatestTime'] = self.support_latest_time
        if self.support_oldest_time is not None:
            result['SupportOldestTime'] = self.support_oldest_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SupportLatestTime') is not None:
            self.support_latest_time = m.get('SupportLatestTime')
        if m.get('SupportOldestTime') is not None:
            self.support_oldest_time = m.get('SupportOldestTime')
        return self


class DescribeInstDbLogInfoResponseBody(TeaModel):
    def __init__(
        self,
        log_time_range: DescribeInstDbLogInfoResponseBodyLogTimeRange = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.log_time_range = log_time_range
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.log_time_range:
            self.log_time_range.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.log_time_range is not None:
            result['LogTimeRange'] = self.log_time_range.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LogTimeRange') is not None:
            temp_model = DescribeInstDbLogInfoResponseBodyLogTimeRange()
            self.log_time_range = temp_model.from_map(m['LogTimeRange'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeInstDbLogInfoResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeInstDbLogInfoResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeInstDbLogInfoResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeInstDbSlsInfoRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeInstDbSlsInfoResponseBodyAuditInfo(TeaModel):
    def __init__(
        self,
        log_store: str = None,
        project: str = None,
    ):
        self.log_store = log_store
        self.project = project

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.log_store is not None:
            result['LogStore'] = self.log_store
        if self.project is not None:
            result['Project'] = self.project
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('LogStore') is not None:
            self.log_store = m.get('LogStore')
        if m.get('Project') is not None:
            self.project = m.get('Project')
        return self


class DescribeInstDbSlsInfoResponseBody(TeaModel):
    def __init__(
        self,
        audit_info: DescribeInstDbSlsInfoResponseBodyAuditInfo = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.audit_info = audit_info
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.audit_info:
            self.audit_info.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.audit_info is not None:
            result['AuditInfo'] = self.audit_info.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AuditInfo') is not None:
            temp_model = DescribeInstDbSlsInfoResponseBodyAuditInfo()
            self.audit_info = temp_model.from_map(m['AuditInfo'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeInstDbSlsInfoResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeInstDbSlsInfoResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeInstDbSlsInfoResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeInstanceAccountsRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeInstanceAccountsResponseBodyInstanceAccountsInstanceAccountDbPrivilegesDbPrivilege(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        privilege: str = None,
    ):
        self.db_name = db_name
        self.privilege = privilege

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.privilege is not None:
            result['Privilege'] = self.privilege
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('Privilege') is not None:
            self.privilege = m.get('Privilege')
        return self


class DescribeInstanceAccountsResponseBodyInstanceAccountsInstanceAccountDbPrivileges(TeaModel):
    def __init__(
        self,
        db_privilege: List[DescribeInstanceAccountsResponseBodyInstanceAccountsInstanceAccountDbPrivilegesDbPrivilege] = None,
    ):
        self.db_privilege = db_privilege

    def validate(self):
        if self.db_privilege:
            for k in self.db_privilege:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['DbPrivilege'] = []
        if self.db_privilege is not None:
            for k in self.db_privilege:
                result['DbPrivilege'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.db_privilege = []
        if m.get('DbPrivilege') is not None:
            for k in m.get('DbPrivilege'):
                temp_model = DescribeInstanceAccountsResponseBodyInstanceAccountsInstanceAccountDbPrivilegesDbPrivilege()
                self.db_privilege.append(temp_model.from_map(k))
        return self


class DescribeInstanceAccountsResponseBodyInstanceAccountsInstanceAccount(TeaModel):
    def __init__(
        self,
        account_name: str = None,
        account_type: int = None,
        db_privileges: DescribeInstanceAccountsResponseBodyInstanceAccountsInstanceAccountDbPrivileges = None,
        description: str = None,
        host: str = None,
    ):
        self.account_name = account_name
        self.account_type = account_type
        self.db_privileges = db_privileges
        self.description = description
        self.host = host

    def validate(self):
        if self.db_privileges:
            self.db_privileges.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_name is not None:
            result['AccountName'] = self.account_name
        if self.account_type is not None:
            result['AccountType'] = self.account_type
        if self.db_privileges is not None:
            result['DbPrivileges'] = self.db_privileges.to_map()
        if self.description is not None:
            result['Description'] = self.description
        if self.host is not None:
            result['Host'] = self.host
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountName') is not None:
            self.account_name = m.get('AccountName')
        if m.get('AccountType') is not None:
            self.account_type = m.get('AccountType')
        if m.get('DbPrivileges') is not None:
            temp_model = DescribeInstanceAccountsResponseBodyInstanceAccountsInstanceAccountDbPrivileges()
            self.db_privileges = temp_model.from_map(m['DbPrivileges'])
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('Host') is not None:
            self.host = m.get('Host')
        return self


class DescribeInstanceAccountsResponseBodyInstanceAccounts(TeaModel):
    def __init__(
        self,
        instance_account: List[DescribeInstanceAccountsResponseBodyInstanceAccountsInstanceAccount] = None,
    ):
        self.instance_account = instance_account

    def validate(self):
        if self.instance_account:
            for k in self.instance_account:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['InstanceAccount'] = []
        if self.instance_account is not None:
            for k in self.instance_account:
                result['InstanceAccount'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.instance_account = []
        if m.get('InstanceAccount') is not None:
            for k in m.get('InstanceAccount'):
                temp_model = DescribeInstanceAccountsResponseBodyInstanceAccountsInstanceAccount()
                self.instance_account.append(temp_model.from_map(k))
        return self


class DescribeInstanceAccountsResponseBody(TeaModel):
    def __init__(
        self,
        instance_accounts: DescribeInstanceAccountsResponseBodyInstanceAccounts = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.instance_accounts = instance_accounts
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.instance_accounts:
            self.instance_accounts.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_accounts is not None:
            result['InstanceAccounts'] = self.instance_accounts.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceAccounts') is not None:
            temp_model = DescribeInstanceAccountsResponseBodyInstanceAccounts()
            self.instance_accounts = temp_model.from_map(m['InstanceAccounts'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeInstanceAccountsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeInstanceAccountsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeInstanceAccountsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeInstanceSwitchAzoneRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeInstanceSwitchAzoneResponseBodyResultTargetAzones(TeaModel):
    def __init__(
        self,
        target_azone: List[str] = None,
    ):
        self.target_azone = target_azone

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.target_azone is not None:
            result['TargetAzone'] = self.target_azone
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('TargetAzone') is not None:
            self.target_azone = m.get('TargetAzone')
        return self


class DescribeInstanceSwitchAzoneResponseBodyResult(TeaModel):
    def __init__(
        self,
        origin_azone_id: str = None,
        region_id: str = None,
        switch_able: bool = None,
        target_azones: DescribeInstanceSwitchAzoneResponseBodyResultTargetAzones = None,
    ):
        self.origin_azone_id = origin_azone_id
        self.region_id = region_id
        self.switch_able = switch_able
        self.target_azones = target_azones

    def validate(self):
        if self.target_azones:
            self.target_azones.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.origin_azone_id is not None:
            result['OriginAzoneId'] = self.origin_azone_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.switch_able is not None:
            result['SwitchAble'] = self.switch_able
        if self.target_azones is not None:
            result['TargetAzones'] = self.target_azones.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('OriginAzoneId') is not None:
            self.origin_azone_id = m.get('OriginAzoneId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('SwitchAble') is not None:
            self.switch_able = m.get('SwitchAble')
        if m.get('TargetAzones') is not None:
            temp_model = DescribeInstanceSwitchAzoneResponseBodyResultTargetAzones()
            self.target_azones = temp_model.from_map(m['TargetAzones'])
        return self


class DescribeInstanceSwitchAzoneResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: DescribeInstanceSwitchAzoneResponseBodyResult = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.result = result
        self.success = success

    def validate(self):
        if self.result:
            self.result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.result is not None:
            result['Result'] = self.result.to_map()
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Result') is not None:
            temp_model = DescribeInstanceSwitchAzoneResponseBodyResult()
            self.result = temp_model.from_map(m['Result'])
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeInstanceSwitchAzoneResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeInstanceSwitchAzoneResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeInstanceSwitchAzoneResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeInstanceSwitchNetworkRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeInstanceSwitchNetworkResponseBodyVpcInfosVpcInfoVswitchInfosVswitchInfo(TeaModel):
    def __init__(
        self,
        azone_id: str = None,
        drds_supported: bool = None,
        vpc_id: str = None,
        vswitch_id: str = None,
        vswitch_name: str = None,
    ):
        self.azone_id = azone_id
        self.drds_supported = drds_supported
        self.vpc_id = vpc_id
        self.vswitch_id = vswitch_id
        self.vswitch_name = vswitch_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.azone_id is not None:
            result['AzoneId'] = self.azone_id
        if self.drds_supported is not None:
            result['DrdsSupported'] = self.drds_supported
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.vswitch_id is not None:
            result['VswitchId'] = self.vswitch_id
        if self.vswitch_name is not None:
            result['VswitchName'] = self.vswitch_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AzoneId') is not None:
            self.azone_id = m.get('AzoneId')
        if m.get('DrdsSupported') is not None:
            self.drds_supported = m.get('DrdsSupported')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VswitchId') is not None:
            self.vswitch_id = m.get('VswitchId')
        if m.get('VswitchName') is not None:
            self.vswitch_name = m.get('VswitchName')
        return self


class DescribeInstanceSwitchNetworkResponseBodyVpcInfosVpcInfoVswitchInfos(TeaModel):
    def __init__(
        self,
        vswitch_info: List[DescribeInstanceSwitchNetworkResponseBodyVpcInfosVpcInfoVswitchInfosVswitchInfo] = None,
    ):
        self.vswitch_info = vswitch_info

    def validate(self):
        if self.vswitch_info:
            for k in self.vswitch_info:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['VswitchInfo'] = []
        if self.vswitch_info is not None:
            for k in self.vswitch_info:
                result['VswitchInfo'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.vswitch_info = []
        if m.get('VswitchInfo') is not None:
            for k in m.get('VswitchInfo'):
                temp_model = DescribeInstanceSwitchNetworkResponseBodyVpcInfosVpcInfoVswitchInfosVswitchInfo()
                self.vswitch_info.append(temp_model.from_map(k))
        return self


class DescribeInstanceSwitchNetworkResponseBodyVpcInfosVpcInfo(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        vpc_id: str = None,
        vpc_name: str = None,
        vswitch_infos: DescribeInstanceSwitchNetworkResponseBodyVpcInfosVpcInfoVswitchInfos = None,
    ):
        self.region_id = region_id
        self.vpc_id = vpc_id
        self.vpc_name = vpc_name
        self.vswitch_infos = vswitch_infos

    def validate(self):
        if self.vswitch_infos:
            self.vswitch_infos.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        if self.vpc_name is not None:
            result['VpcName'] = self.vpc_name
        if self.vswitch_infos is not None:
            result['VswitchInfos'] = self.vswitch_infos.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        if m.get('VpcName') is not None:
            self.vpc_name = m.get('VpcName')
        if m.get('VswitchInfos') is not None:
            temp_model = DescribeInstanceSwitchNetworkResponseBodyVpcInfosVpcInfoVswitchInfos()
            self.vswitch_infos = temp_model.from_map(m['VswitchInfos'])
        return self


class DescribeInstanceSwitchNetworkResponseBodyVpcInfos(TeaModel):
    def __init__(
        self,
        vpc_info: List[DescribeInstanceSwitchNetworkResponseBodyVpcInfosVpcInfo] = None,
    ):
        self.vpc_info = vpc_info

    def validate(self):
        if self.vpc_info:
            for k in self.vpc_info:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['VpcInfo'] = []
        if self.vpc_info is not None:
            for k in self.vpc_info:
                result['VpcInfo'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.vpc_info = []
        if m.get('VpcInfo') is not None:
            for k in m.get('VpcInfo'):
                temp_model = DescribeInstanceSwitchNetworkResponseBodyVpcInfosVpcInfo()
                self.vpc_info.append(temp_model.from_map(k))
        return self


class DescribeInstanceSwitchNetworkResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
        vpc_infos: DescribeInstanceSwitchNetworkResponseBodyVpcInfos = None,
    ):
        self.request_id = request_id
        self.success = success
        self.vpc_infos = vpc_infos

    def validate(self):
        if self.vpc_infos:
            self.vpc_infos.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.vpc_infos is not None:
            result['VpcInfos'] = self.vpc_infos.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('VpcInfos') is not None:
            temp_model = DescribeInstanceSwitchNetworkResponseBodyVpcInfos()
            self.vpc_infos = temp_model.from_map(m['VpcInfos'])
        return self


class DescribeInstanceSwitchNetworkResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeInstanceSwitchNetworkResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeInstanceSwitchNetworkResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribePreCheckResultRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
        region_id: str = None,
        task_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id
        self.task_id = task_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class DescribePreCheckResultResponseBodyPreCheckResultSubCheckItems(TeaModel):
    def __init__(
        self,
        error_msg_code: str = None,
        error_msg_params: List[str] = None,
        pre_check_item_name: str = None,
        state: str = None,
    ):
        self.error_msg_code = error_msg_code
        self.error_msg_params = error_msg_params
        self.pre_check_item_name = pre_check_item_name
        self.state = state

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.error_msg_code is not None:
            result['ErrorMsgCode'] = self.error_msg_code
        if self.error_msg_params is not None:
            result['ErrorMsgParams'] = self.error_msg_params
        if self.pre_check_item_name is not None:
            result['PreCheckItemName'] = self.pre_check_item_name
        if self.state is not None:
            result['State'] = self.state
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ErrorMsgCode') is not None:
            self.error_msg_code = m.get('ErrorMsgCode')
        if m.get('ErrorMsgParams') is not None:
            self.error_msg_params = m.get('ErrorMsgParams')
        if m.get('PreCheckItemName') is not None:
            self.pre_check_item_name = m.get('PreCheckItemName')
        if m.get('State') is not None:
            self.state = m.get('State')
        return self


class DescribePreCheckResultResponseBodyPreCheckResult(TeaModel):
    def __init__(
        self,
        pre_check_name: str = None,
        state: str = None,
        sub_check_items: List[DescribePreCheckResultResponseBodyPreCheckResultSubCheckItems] = None,
    ):
        self.pre_check_name = pre_check_name
        self.state = state
        self.sub_check_items = sub_check_items

    def validate(self):
        if self.sub_check_items:
            for k in self.sub_check_items:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pre_check_name is not None:
            result['PreCheckName'] = self.pre_check_name
        if self.state is not None:
            result['State'] = self.state
        result['SubCheckItems'] = []
        if self.sub_check_items is not None:
            for k in self.sub_check_items:
                result['SubCheckItems'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PreCheckName') is not None:
            self.pre_check_name = m.get('PreCheckName')
        if m.get('State') is not None:
            self.state = m.get('State')
        self.sub_check_items = []
        if m.get('SubCheckItems') is not None:
            for k in m.get('SubCheckItems'):
                temp_model = DescribePreCheckResultResponseBodyPreCheckResultSubCheckItems()
                self.sub_check_items.append(temp_model.from_map(k))
        return self


class DescribePreCheckResultResponseBody(TeaModel):
    def __init__(
        self,
        pre_check_result: DescribePreCheckResultResponseBodyPreCheckResult = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.pre_check_result = pre_check_result
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.pre_check_result:
            self.pre_check_result.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.pre_check_result is not None:
            result['PreCheckResult'] = self.pre_check_result.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('PreCheckResult') is not None:
            temp_model = DescribePreCheckResultResponseBodyPreCheckResult()
            self.pre_check_result = temp_model.from_map(m['PreCheckResult'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribePreCheckResultResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribePreCheckResultResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribePreCheckResultResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRDSPerformanceRequest(TeaModel):
    def __init__(
        self,
        db_inst_type: str = None,
        drds_instance_id: str = None,
        end_time: int = None,
        keys: str = None,
        rds_instance_id: str = None,
        start_time: int = None,
    ):
        self.db_inst_type = db_inst_type
        self.drds_instance_id = drds_instance_id
        self.end_time = end_time
        self.keys = keys
        self.rds_instance_id = rds_instance_id
        self.start_time = start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_inst_type is not None:
            result['DbInstType'] = self.db_inst_type
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.keys is not None:
            result['Keys'] = self.keys
        if self.rds_instance_id is not None:
            result['RdsInstanceId'] = self.rds_instance_id
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbInstType') is not None:
            self.db_inst_type = m.get('DbInstType')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('Keys') is not None:
            self.keys = m.get('Keys')
        if m.get('RdsInstanceId') is not None:
            self.rds_instance_id = m.get('RdsInstanceId')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        return self


class DescribeRDSPerformanceResponseBodyDataValues(TeaModel):
    def __init__(
        self,
        date: int = None,
        value: str = None,
    ):
        self.date = date
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.date is not None:
            result['Date'] = self.date
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Date') is not None:
            self.date = m.get('Date')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class DescribeRDSPerformanceResponseBodyData(TeaModel):
    def __init__(
        self,
        key: str = None,
        node_name: str = None,
        node_num: int = None,
        unit: str = None,
        values: List[DescribeRDSPerformanceResponseBodyDataValues] = None,
    ):
        self.key = key
        self.node_name = node_name
        self.node_num = node_num
        self.unit = unit
        self.values = values

    def validate(self):
        if self.values:
            for k in self.values:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.node_name is not None:
            result['NodeName'] = self.node_name
        if self.node_num is not None:
            result['NodeNum'] = self.node_num
        if self.unit is not None:
            result['Unit'] = self.unit
        result['Values'] = []
        if self.values is not None:
            for k in self.values:
                result['Values'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('NodeName') is not None:
            self.node_name = m.get('NodeName')
        if m.get('NodeNum') is not None:
            self.node_num = m.get('NodeNum')
        if m.get('Unit') is not None:
            self.unit = m.get('Unit')
        self.values = []
        if m.get('Values') is not None:
            for k in m.get('Values'):
                temp_model = DescribeRDSPerformanceResponseBodyDataValues()
                self.values.append(temp_model.from_map(k))
        return self


class DescribeRDSPerformanceResponseBody(TeaModel):
    def __init__(
        self,
        data: List[DescribeRDSPerformanceResponseBodyData] = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Data'] = []
        if self.data is not None:
            for k in self.data:
                result['Data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = DescribeRDSPerformanceResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeRDSPerformanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeRDSPerformanceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeRDSPerformanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRdsCommodityRequest(TeaModel):
    def __init__(
        self,
        commodity_code: str = None,
        drds_instance_id: str = None,
        order_type: str = None,
    ):
        self.commodity_code = commodity_code
        self.drds_instance_id = drds_instance_id
        self.order_type = order_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.commodity_code is not None:
            result['CommodityCode'] = self.commodity_code
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.order_type is not None:
            result['OrderType'] = self.order_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CommodityCode') is not None:
            self.commodity_code = m.get('CommodityCode')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('OrderType') is not None:
            self.order_type = m.get('OrderType')
        return self


class DescribeRdsCommodityResponseBody(TeaModel):
    def __init__(
        self,
        data: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeRdsCommodityResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeRdsCommodityResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeRdsCommodityResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRdsPerformanceSummaryRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
        rds_instance_id: List[str] = None,
        region_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id
        self.rds_instance_id = rds_instance_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.rds_instance_id is not None:
            result['RdsInstanceId'] = self.rds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RdsInstanceId') is not None:
            self.rds_instance_id = m.get('RdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeRdsPerformanceSummaryResponseBodyRdsPerformanceInfos(TeaModel):
    def __init__(
        self,
        active_sessions: int = None,
        cpu: float = None,
        iops: float = None,
        rds_id: str = None,
        space_usage: int = None,
        total_sessions: int = None,
    ):
        self.active_sessions = active_sessions
        self.cpu = cpu
        self.iops = iops
        self.rds_id = rds_id
        self.space_usage = space_usage
        self.total_sessions = total_sessions

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.active_sessions is not None:
            result['ActiveSessions'] = self.active_sessions
        if self.cpu is not None:
            result['Cpu'] = self.cpu
        if self.iops is not None:
            result['Iops'] = self.iops
        if self.rds_id is not None:
            result['RdsId'] = self.rds_id
        if self.space_usage is not None:
            result['SpaceUsage'] = self.space_usage
        if self.total_sessions is not None:
            result['TotalSessions'] = self.total_sessions
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ActiveSessions') is not None:
            self.active_sessions = m.get('ActiveSessions')
        if m.get('Cpu') is not None:
            self.cpu = m.get('Cpu')
        if m.get('Iops') is not None:
            self.iops = m.get('Iops')
        if m.get('RdsId') is not None:
            self.rds_id = m.get('RdsId')
        if m.get('SpaceUsage') is not None:
            self.space_usage = m.get('SpaceUsage')
        if m.get('TotalSessions') is not None:
            self.total_sessions = m.get('TotalSessions')
        return self


class DescribeRdsPerformanceSummaryResponseBody(TeaModel):
    def __init__(
        self,
        rds_performance_infos: List[DescribeRdsPerformanceSummaryResponseBodyRdsPerformanceInfos] = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.rds_performance_infos = rds_performance_infos
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.rds_performance_infos:
            for k in self.rds_performance_infos:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['RdsPerformanceInfos'] = []
        if self.rds_performance_infos is not None:
            for k in self.rds_performance_infos:
                result['RdsPerformanceInfos'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.rds_performance_infos = []
        if m.get('RdsPerformanceInfos') is not None:
            for k in m.get('RdsPerformanceInfos'):
                temp_model = DescribeRdsPerformanceSummaryResponseBodyRdsPerformanceInfos()
                self.rds_performance_infos.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeRdsPerformanceSummaryResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeRdsPerformanceSummaryResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeRdsPerformanceSummaryResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRdsSuperAccountInstancesRequest(TeaModel):
    def __init__(
        self,
        db_inst_type: str = None,
        drds_instance_id: str = None,
        rds_instance: List[str] = None,
    ):
        self.db_inst_type = db_inst_type
        self.drds_instance_id = drds_instance_id
        self.rds_instance = rds_instance

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_inst_type is not None:
            result['DbInstType'] = self.db_inst_type
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.rds_instance is not None:
            result['RdsInstance'] = self.rds_instance
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbInstType') is not None:
            self.db_inst_type = m.get('DbInstType')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RdsInstance') is not None:
            self.rds_instance = m.get('RdsInstance')
        return self


class DescribeRdsSuperAccountInstancesResponseBodyDbInstances(TeaModel):
    def __init__(
        self,
        db_instance: List[str] = None,
    ):
        self.db_instance = db_instance

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_instance is not None:
            result['DbInstance'] = self.db_instance
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbInstance') is not None:
            self.db_instance = m.get('DbInstance')
        return self


class DescribeRdsSuperAccountInstancesResponseBody(TeaModel):
    def __init__(
        self,
        db_instances: DescribeRdsSuperAccountInstancesResponseBodyDbInstances = None,
        request_id: str = None,
    ):
        self.db_instances = db_instances
        self.request_id = request_id

    def validate(self):
        if self.db_instances:
            self.db_instances.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_instances is not None:
            result['DbInstances'] = self.db_instances.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbInstances') is not None:
            temp_model = DescribeRdsSuperAccountInstancesResponseBodyDbInstances()
            self.db_instances = temp_model.from_map(m['DbInstances'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class DescribeRdsSuperAccountInstancesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeRdsSuperAccountInstancesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeRdsSuperAccountInstancesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRecycleBinStatusRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        region_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeRecycleBinStatusResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        status: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.status = status
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.status is not None:
            result['Status'] = self.status
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeRecycleBinStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeRecycleBinStatusResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeRecycleBinStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRecycleBinTablesRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        region_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeRecycleBinTablesResponseBodyData(TeaModel):
    def __init__(
        self,
        create_time: str = None,
        original_table_name: str = None,
        table_name: str = None,
    ):
        self.create_time = create_time
        self.original_table_name = original_table_name
        self.table_name = table_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.create_time is not None:
            result['CreateTime'] = self.create_time
        if self.original_table_name is not None:
            result['OriginalTableName'] = self.original_table_name
        if self.table_name is not None:
            result['TableName'] = self.table_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CreateTime') is not None:
            self.create_time = m.get('CreateTime')
        if m.get('OriginalTableName') is not None:
            self.original_table_name = m.get('OriginalTableName')
        if m.get('TableName') is not None:
            self.table_name = m.get('TableName')
        return self


class DescribeRecycleBinTablesResponseBody(TeaModel):
    def __init__(
        self,
        data: List[DescribeRecycleBinTablesResponseBodyData] = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Data'] = []
        if self.data is not None:
            for k in self.data:
                result['Data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = DescribeRecycleBinTablesResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeRecycleBinTablesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeRecycleBinTablesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeRecycleBinTablesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeRestoreOrderRequest(TeaModel):
    def __init__(
        self,
        backup_db_names: str = None,
        backup_id: str = None,
        backup_level: str = None,
        backup_mode: str = None,
        drds_instance_id: str = None,
        preferred_backup_time: str = None,
    ):
        self.backup_db_names = backup_db_names
        self.backup_id = backup_id
        self.backup_level = backup_level
        self.backup_mode = backup_mode
        self.drds_instance_id = drds_instance_id
        self.preferred_backup_time = preferred_backup_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.backup_db_names is not None:
            result['BackupDbNames'] = self.backup_db_names
        if self.backup_id is not None:
            result['BackupId'] = self.backup_id
        if self.backup_level is not None:
            result['BackupLevel'] = self.backup_level
        if self.backup_mode is not None:
            result['BackupMode'] = self.backup_mode
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.preferred_backup_time is not None:
            result['PreferredBackupTime'] = self.preferred_backup_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BackupDbNames') is not None:
            self.backup_db_names = m.get('BackupDbNames')
        if m.get('BackupId') is not None:
            self.backup_id = m.get('BackupId')
        if m.get('BackupLevel') is not None:
            self.backup_level = m.get('BackupLevel')
        if m.get('BackupMode') is not None:
            self.backup_mode = m.get('BackupMode')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('PreferredBackupTime') is not None:
            self.preferred_backup_time = m.get('PreferredBackupTime')
        return self


class DescribeRestoreOrderResponseBodyRestoreOrderDODrdsOrderDOListDrdsOrderDOList(TeaModel):
    def __init__(
        self,
        azone_id: str = None,
        inst_spec: str = None,
        network: str = None,
        region_id: str = None,
        vswtich_id: str = None,
        vpc_id: str = None,
    ):
        self.azone_id = azone_id
        self.inst_spec = inst_spec
        self.network = network
        self.region_id = region_id
        self.vswtich_id = vswtich_id
        self.vpc_id = vpc_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.azone_id is not None:
            result['AzoneId'] = self.azone_id
        if self.inst_spec is not None:
            result['InstSpec'] = self.inst_spec
        if self.network is not None:
            result['Network'] = self.network
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.vswtich_id is not None:
            result['VSwtichId'] = self.vswtich_id
        if self.vpc_id is not None:
            result['VpcId'] = self.vpc_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AzoneId') is not None:
            self.azone_id = m.get('AzoneId')
        if m.get('InstSpec') is not None:
            self.inst_spec = m.get('InstSpec')
        if m.get('Network') is not None:
            self.network = m.get('Network')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('VSwtichId') is not None:
            self.vswtich_id = m.get('VSwtichId')
        if m.get('VpcId') is not None:
            self.vpc_id = m.get('VpcId')
        return self


class DescribeRestoreOrderResponseBodyRestoreOrderDODrdsOrderDOList(TeaModel):
    def __init__(
        self,
        drds_order_dolist: List[DescribeRestoreOrderResponseBodyRestoreOrderDODrdsOrderDOListDrdsOrderDOList] = None,
    ):
        self.drds_order_dolist = drds_order_dolist

    def validate(self):
        if self.drds_order_dolist:
            for k in self.drds_order_dolist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['DrdsOrderDOList'] = []
        if self.drds_order_dolist is not None:
            for k in self.drds_order_dolist:
                result['DrdsOrderDOList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.drds_order_dolist = []
        if m.get('DrdsOrderDOList') is not None:
            for k in m.get('DrdsOrderDOList'):
                temp_model = DescribeRestoreOrderResponseBodyRestoreOrderDODrdsOrderDOListDrdsOrderDOList()
                self.drds_order_dolist.append(temp_model.from_map(k))
        return self


class DescribeRestoreOrderResponseBodyRestoreOrderDOPolarOrderDOListPolarOrderDOList(TeaModel):
    def __init__(
        self,
        azone_id: str = None,
        db_instance_storage: str = None,
        engine: str = None,
        instance_class: str = None,
        network: str = None,
        num: int = None,
        region_id: str = None,
        version: str = None,
    ):
        self.azone_id = azone_id
        self.db_instance_storage = db_instance_storage
        self.engine = engine
        self.instance_class = instance_class
        self.network = network
        self.num = num
        self.region_id = region_id
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.azone_id is not None:
            result['AzoneId'] = self.azone_id
        if self.db_instance_storage is not None:
            result['DbInstanceStorage'] = self.db_instance_storage
        if self.engine is not None:
            result['Engine'] = self.engine
        if self.instance_class is not None:
            result['InstanceClass'] = self.instance_class
        if self.network is not None:
            result['Network'] = self.network
        if self.num is not None:
            result['Num'] = self.num
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.version is not None:
            result['Version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AzoneId') is not None:
            self.azone_id = m.get('AzoneId')
        if m.get('DbInstanceStorage') is not None:
            self.db_instance_storage = m.get('DbInstanceStorage')
        if m.get('Engine') is not None:
            self.engine = m.get('Engine')
        if m.get('InstanceClass') is not None:
            self.instance_class = m.get('InstanceClass')
        if m.get('Network') is not None:
            self.network = m.get('Network')
        if m.get('Num') is not None:
            self.num = m.get('Num')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        return self


class DescribeRestoreOrderResponseBodyRestoreOrderDOPolarOrderDOList(TeaModel):
    def __init__(
        self,
        polar_order_dolist: List[DescribeRestoreOrderResponseBodyRestoreOrderDOPolarOrderDOListPolarOrderDOList] = None,
    ):
        self.polar_order_dolist = polar_order_dolist

    def validate(self):
        if self.polar_order_dolist:
            for k in self.polar_order_dolist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['PolarOrderDOList'] = []
        if self.polar_order_dolist is not None:
            for k in self.polar_order_dolist:
                result['PolarOrderDOList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.polar_order_dolist = []
        if m.get('PolarOrderDOList') is not None:
            for k in m.get('PolarOrderDOList'):
                temp_model = DescribeRestoreOrderResponseBodyRestoreOrderDOPolarOrderDOListPolarOrderDOList()
                self.polar_order_dolist.append(temp_model.from_map(k))
        return self


class DescribeRestoreOrderResponseBodyRestoreOrderDORdsOrderDOListRdsOrderDOList(TeaModel):
    def __init__(
        self,
        azone_id: str = None,
        db_instance_storage: str = None,
        engine: str = None,
        instance_class: str = None,
        network: str = None,
        num: int = None,
        region_id: str = None,
        version: str = None,
    ):
        self.azone_id = azone_id
        self.db_instance_storage = db_instance_storage
        self.engine = engine
        self.instance_class = instance_class
        self.network = network
        self.num = num
        self.region_id = region_id
        self.version = version

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.azone_id is not None:
            result['AzoneId'] = self.azone_id
        if self.db_instance_storage is not None:
            result['DbInstanceStorage'] = self.db_instance_storage
        if self.engine is not None:
            result['Engine'] = self.engine
        if self.instance_class is not None:
            result['InstanceClass'] = self.instance_class
        if self.network is not None:
            result['Network'] = self.network
        if self.num is not None:
            result['Num'] = self.num
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.version is not None:
            result['Version'] = self.version
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AzoneId') is not None:
            self.azone_id = m.get('AzoneId')
        if m.get('DbInstanceStorage') is not None:
            self.db_instance_storage = m.get('DbInstanceStorage')
        if m.get('Engine') is not None:
            self.engine = m.get('Engine')
        if m.get('InstanceClass') is not None:
            self.instance_class = m.get('InstanceClass')
        if m.get('Network') is not None:
            self.network = m.get('Network')
        if m.get('Num') is not None:
            self.num = m.get('Num')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Version') is not None:
            self.version = m.get('Version')
        return self


class DescribeRestoreOrderResponseBodyRestoreOrderDORdsOrderDOList(TeaModel):
    def __init__(
        self,
        rds_order_dolist: List[DescribeRestoreOrderResponseBodyRestoreOrderDORdsOrderDOListRdsOrderDOList] = None,
    ):
        self.rds_order_dolist = rds_order_dolist

    def validate(self):
        if self.rds_order_dolist:
            for k in self.rds_order_dolist:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['RdsOrderDOList'] = []
        if self.rds_order_dolist is not None:
            for k in self.rds_order_dolist:
                result['RdsOrderDOList'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.rds_order_dolist = []
        if m.get('RdsOrderDOList') is not None:
            for k in m.get('RdsOrderDOList'):
                temp_model = DescribeRestoreOrderResponseBodyRestoreOrderDORdsOrderDOListRdsOrderDOList()
                self.rds_order_dolist.append(temp_model.from_map(k))
        return self


class DescribeRestoreOrderResponseBodyRestoreOrderDO(TeaModel):
    def __init__(
        self,
        drds_order_dolist: DescribeRestoreOrderResponseBodyRestoreOrderDODrdsOrderDOList = None,
        polar_order_dolist: DescribeRestoreOrderResponseBodyRestoreOrderDOPolarOrderDOList = None,
        rds_order_dolist: DescribeRestoreOrderResponseBodyRestoreOrderDORdsOrderDOList = None,
    ):
        self.drds_order_dolist = drds_order_dolist
        self.polar_order_dolist = polar_order_dolist
        self.rds_order_dolist = rds_order_dolist

    def validate(self):
        if self.drds_order_dolist:
            self.drds_order_dolist.validate()
        if self.polar_order_dolist:
            self.polar_order_dolist.validate()
        if self.rds_order_dolist:
            self.rds_order_dolist.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_order_dolist is not None:
            result['DrdsOrderDOList'] = self.drds_order_dolist.to_map()
        if self.polar_order_dolist is not None:
            result['PolarOrderDOList'] = self.polar_order_dolist.to_map()
        if self.rds_order_dolist is not None:
            result['RdsOrderDOList'] = self.rds_order_dolist.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsOrderDOList') is not None:
            temp_model = DescribeRestoreOrderResponseBodyRestoreOrderDODrdsOrderDOList()
            self.drds_order_dolist = temp_model.from_map(m['DrdsOrderDOList'])
        if m.get('PolarOrderDOList') is not None:
            temp_model = DescribeRestoreOrderResponseBodyRestoreOrderDOPolarOrderDOList()
            self.polar_order_dolist = temp_model.from_map(m['PolarOrderDOList'])
        if m.get('RdsOrderDOList') is not None:
            temp_model = DescribeRestoreOrderResponseBodyRestoreOrderDORdsOrderDOList()
            self.rds_order_dolist = temp_model.from_map(m['RdsOrderDOList'])
        return self


class DescribeRestoreOrderResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        restore_order_do: DescribeRestoreOrderResponseBodyRestoreOrderDO = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.restore_order_do = restore_order_do
        self.success = success

    def validate(self):
        if self.restore_order_do:
            self.restore_order_do.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.restore_order_do is not None:
            result['RestoreOrderDO'] = self.restore_order_do.to_map()
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('RestoreOrderDO') is not None:
            temp_model = DescribeRestoreOrderResponseBodyRestoreOrderDO()
            self.restore_order_do = temp_model.from_map(m['RestoreOrderDO'])
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeRestoreOrderResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeRestoreOrderResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeRestoreOrderResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeShardTaskInfoRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        region_id: str = None,
        source_table_name: str = None,
        target_table_name: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id
        self.source_table_name = source_table_name
        self.target_table_name = target_table_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.source_table_name is not None:
            result['SourceTableName'] = self.source_table_name
        if self.target_table_name is not None:
            result['TargetTableName'] = self.target_table_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('SourceTableName') is not None:
            self.source_table_name = m.get('SourceTableName')
        if m.get('TargetTableName') is not None:
            self.target_table_name = m.get('TargetTableName')
        return self


class DescribeShardTaskInfoResponseBodyDataFull(TeaModel):
    def __init__(
        self,
        expired: int = None,
        progress: int = None,
        start_time: str = None,
        total: int = None,
        tps: int = None,
    ):
        self.expired = expired
        self.progress = progress
        self.start_time = start_time
        self.total = total
        self.tps = tps

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.expired is not None:
            result['Expired'] = self.expired
        if self.progress is not None:
            result['Progress'] = self.progress
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.total is not None:
            result['Total'] = self.total
        if self.tps is not None:
            result['Tps'] = self.tps
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Expired') is not None:
            self.expired = m.get('Expired')
        if m.get('Progress') is not None:
            self.progress = m.get('Progress')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Tps') is not None:
            self.tps = m.get('Tps')
        return self


class DescribeShardTaskInfoResponseBodyDataFullCheck(TeaModel):
    def __init__(
        self,
        expired: int = None,
        progress: int = None,
        start_time: str = None,
        total: int = None,
        tps: int = None,
    ):
        self.expired = expired
        self.progress = progress
        self.start_time = start_time
        self.total = total
        self.tps = tps

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.expired is not None:
            result['Expired'] = self.expired
        if self.progress is not None:
            result['Progress'] = self.progress
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.total is not None:
            result['Total'] = self.total
        if self.tps is not None:
            result['Tps'] = self.tps
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Expired') is not None:
            self.expired = m.get('Expired')
        if m.get('Progress') is not None:
            self.progress = m.get('Progress')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Tps') is not None:
            self.tps = m.get('Tps')
        return self


class DescribeShardTaskInfoResponseBodyDataFullRevise(TeaModel):
    def __init__(
        self,
        expired: int = None,
        progress: int = None,
        start_time: str = None,
        total: int = None,
        tps: int = None,
    ):
        self.expired = expired
        self.progress = progress
        self.start_time = start_time
        self.total = total
        self.tps = tps

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.expired is not None:
            result['Expired'] = self.expired
        if self.progress is not None:
            result['Progress'] = self.progress
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.total is not None:
            result['Total'] = self.total
        if self.tps is not None:
            result['Tps'] = self.tps
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Expired') is not None:
            self.expired = m.get('Expired')
        if m.get('Progress') is not None:
            self.progress = m.get('Progress')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Tps') is not None:
            self.tps = m.get('Tps')
        return self


class DescribeShardTaskInfoResponseBodyDataIncrement(TeaModel):
    def __init__(
        self,
        delay: int = None,
        start_time: str = None,
        tps: int = None,
    ):
        self.delay = delay
        self.start_time = start_time
        self.tps = tps

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.delay is not None:
            result['Delay'] = self.delay
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.tps is not None:
            result['Tps'] = self.tps
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Delay') is not None:
            self.delay = m.get('Delay')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Tps') is not None:
            self.tps = m.get('Tps')
        return self


class DescribeShardTaskInfoResponseBodyDataReview(TeaModel):
    def __init__(
        self,
        expired: int = None,
        progress: int = None,
        start_time: str = None,
        total: int = None,
        tps: int = None,
    ):
        self.expired = expired
        self.progress = progress
        self.start_time = start_time
        self.total = total
        self.tps = tps

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.expired is not None:
            result['Expired'] = self.expired
        if self.progress is not None:
            result['Progress'] = self.progress
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.total is not None:
            result['Total'] = self.total
        if self.tps is not None:
            result['Tps'] = self.tps
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Expired') is not None:
            self.expired = m.get('Expired')
        if m.get('Progress') is not None:
            self.progress = m.get('Progress')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        if m.get('Tps') is not None:
            self.tps = m.get('Tps')
        return self


class DescribeShardTaskInfoResponseBodyData(TeaModel):
    def __init__(
        self,
        expired: str = None,
        full: DescribeShardTaskInfoResponseBodyDataFull = None,
        full_check: DescribeShardTaskInfoResponseBodyDataFullCheck = None,
        full_revise: DescribeShardTaskInfoResponseBodyDataFullRevise = None,
        increment: DescribeShardTaskInfoResponseBodyDataIncrement = None,
        progress: str = None,
        review: DescribeShardTaskInfoResponseBodyDataReview = None,
        source_table_name: str = None,
        stage: str = None,
        status: str = None,
        target_table_name: str = None,
    ):
        self.expired = expired
        self.full = full
        self.full_check = full_check
        self.full_revise = full_revise
        self.increment = increment
        self.progress = progress
        self.review = review
        self.source_table_name = source_table_name
        self.stage = stage
        self.status = status
        self.target_table_name = target_table_name

    def validate(self):
        if self.full:
            self.full.validate()
        if self.full_check:
            self.full_check.validate()
        if self.full_revise:
            self.full_revise.validate()
        if self.increment:
            self.increment.validate()
        if self.review:
            self.review.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.expired is not None:
            result['Expired'] = self.expired
        if self.full is not None:
            result['Full'] = self.full.to_map()
        if self.full_check is not None:
            result['FullCheck'] = self.full_check.to_map()
        if self.full_revise is not None:
            result['FullRevise'] = self.full_revise.to_map()
        if self.increment is not None:
            result['Increment'] = self.increment.to_map()
        if self.progress is not None:
            result['Progress'] = self.progress
        if self.review is not None:
            result['Review'] = self.review.to_map()
        if self.source_table_name is not None:
            result['SourceTableName'] = self.source_table_name
        if self.stage is not None:
            result['Stage'] = self.stage
        if self.status is not None:
            result['Status'] = self.status
        if self.target_table_name is not None:
            result['TargetTableName'] = self.target_table_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Expired') is not None:
            self.expired = m.get('Expired')
        if m.get('Full') is not None:
            temp_model = DescribeShardTaskInfoResponseBodyDataFull()
            self.full = temp_model.from_map(m['Full'])
        if m.get('FullCheck') is not None:
            temp_model = DescribeShardTaskInfoResponseBodyDataFullCheck()
            self.full_check = temp_model.from_map(m['FullCheck'])
        if m.get('FullRevise') is not None:
            temp_model = DescribeShardTaskInfoResponseBodyDataFullRevise()
            self.full_revise = temp_model.from_map(m['FullRevise'])
        if m.get('Increment') is not None:
            temp_model = DescribeShardTaskInfoResponseBodyDataIncrement()
            self.increment = temp_model.from_map(m['Increment'])
        if m.get('Progress') is not None:
            self.progress = m.get('Progress')
        if m.get('Review') is not None:
            temp_model = DescribeShardTaskInfoResponseBodyDataReview()
            self.review = temp_model.from_map(m['Review'])
        if m.get('SourceTableName') is not None:
            self.source_table_name = m.get('SourceTableName')
        if m.get('Stage') is not None:
            self.stage = m.get('Stage')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('TargetTableName') is not None:
            self.target_table_name = m.get('TargetTableName')
        return self


class DescribeShardTaskInfoResponseBody(TeaModel):
    def __init__(
        self,
        data: DescribeShardTaskInfoResponseBodyData = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = DescribeShardTaskInfoResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeShardTaskInfoResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeShardTaskInfoResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeShardTaskInfoResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeShardTaskListRequest(TeaModel):
    def __init__(
        self,
        current_page: int = None,
        db_name: str = None,
        drds_instance_id: str = None,
        page_size: int = None,
        query: str = None,
        region_id: str = None,
        task_type: str = None,
    ):
        self.current_page = current_page
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.page_size = page_size
        self.query = query
        self.region_id = region_id
        self.task_type = task_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.current_page is not None:
            result['CurrentPage'] = self.current_page
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.query is not None:
            result['Query'] = self.query
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.task_type is not None:
            result['TaskType'] = self.task_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CurrentPage') is not None:
            self.current_page = m.get('CurrentPage')
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Query') is not None:
            self.query = m.get('Query')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')
        return self


class DescribeShardTaskListResponseBodyList(TeaModel):
    def __init__(
        self,
        delay: int = None,
        expired: int = None,
        progress: int = None,
        source_table_name: str = None,
        stage: int = None,
        status: str = None,
        target_table_name: str = None,
    ):
        self.delay = delay
        self.expired = expired
        self.progress = progress
        self.source_table_name = source_table_name
        self.stage = stage
        self.status = status
        self.target_table_name = target_table_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.delay is not None:
            result['Delay'] = self.delay
        if self.expired is not None:
            result['Expired'] = self.expired
        if self.progress is not None:
            result['Progress'] = self.progress
        if self.source_table_name is not None:
            result['SourceTableName'] = self.source_table_name
        if self.stage is not None:
            result['Stage'] = self.stage
        if self.status is not None:
            result['Status'] = self.status
        if self.target_table_name is not None:
            result['TargetTableName'] = self.target_table_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Delay') is not None:
            self.delay = m.get('Delay')
        if m.get('Expired') is not None:
            self.expired = m.get('Expired')
        if m.get('Progress') is not None:
            self.progress = m.get('Progress')
        if m.get('SourceTableName') is not None:
            self.source_table_name = m.get('SourceTableName')
        if m.get('Stage') is not None:
            self.stage = m.get('Stage')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('TargetTableName') is not None:
            self.target_table_name = m.get('TargetTableName')
        return self


class DescribeShardTaskListResponseBody(TeaModel):
    def __init__(
        self,
        list: List[DescribeShardTaskListResponseBodyList] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        success: bool = None,
        total: int = None,
    ):
        self.list = list
        self.page_number = page_number
        self.page_size = page_size
        self.request_id = request_id
        self.success = success
        self.total = total

    def validate(self):
        if self.list:
            for k in self.list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['List'] = []
        if self.list is not None:
            for k in self.list:
                result['List'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.list = []
        if m.get('List') is not None:
            for k in m.get('List'):
                temp_model = DescribeShardTaskListResponseBodyList()
                self.list.append(temp_model.from_map(k))
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class DescribeShardTaskListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeShardTaskListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeShardTaskListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeSqlFlashbakTaskRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DescribeSqlFlashbakTaskResponseBodySqlFlashbackTasksSqlFlashbackTask(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        download_url: str = None,
        expire_time: int = None,
        gmt_create: int = None,
        gmt_modified: int = None,
        id: int = None,
        inst_id: str = None,
        recall_progress: int = None,
        recall_restore_type: int = None,
        recall_status: int = None,
        recall_type: int = None,
        search_end_time: int = None,
        search_start_time: int = None,
        sql_counter: int = None,
        sql_pk: str = None,
        sql_type: str = None,
        table_name: str = None,
        trace_id: str = None,
    ):
        self.db_name = db_name
        self.download_url = download_url
        self.expire_time = expire_time
        self.gmt_create = gmt_create
        self.gmt_modified = gmt_modified
        self.id = id
        self.inst_id = inst_id
        self.recall_progress = recall_progress
        self.recall_restore_type = recall_restore_type
        self.recall_status = recall_status
        self.recall_type = recall_type
        self.search_end_time = search_end_time
        self.search_start_time = search_start_time
        self.sql_counter = sql_counter
        self.sql_pk = sql_pk
        self.sql_type = sql_type
        self.table_name = table_name
        self.trace_id = trace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.download_url is not None:
            result['DownloadUrl'] = self.download_url
        if self.expire_time is not None:
            result['ExpireTime'] = self.expire_time
        if self.gmt_create is not None:
            result['GmtCreate'] = self.gmt_create
        if self.gmt_modified is not None:
            result['GmtModified'] = self.gmt_modified
        if self.id is not None:
            result['Id'] = self.id
        if self.inst_id is not None:
            result['InstId'] = self.inst_id
        if self.recall_progress is not None:
            result['RecallProgress'] = self.recall_progress
        if self.recall_restore_type is not None:
            result['RecallRestoreType'] = self.recall_restore_type
        if self.recall_status is not None:
            result['RecallStatus'] = self.recall_status
        if self.recall_type is not None:
            result['RecallType'] = self.recall_type
        if self.search_end_time is not None:
            result['SearchEndTime'] = self.search_end_time
        if self.search_start_time is not None:
            result['SearchStartTime'] = self.search_start_time
        if self.sql_counter is not None:
            result['SqlCounter'] = self.sql_counter
        if self.sql_pk is not None:
            result['SqlPk'] = self.sql_pk
        if self.sql_type is not None:
            result['SqlType'] = self.sql_type
        if self.table_name is not None:
            result['TableName'] = self.table_name
        if self.trace_id is not None:
            result['TraceId'] = self.trace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DownloadUrl') is not None:
            self.download_url = m.get('DownloadUrl')
        if m.get('ExpireTime') is not None:
            self.expire_time = m.get('ExpireTime')
        if m.get('GmtCreate') is not None:
            self.gmt_create = m.get('GmtCreate')
        if m.get('GmtModified') is not None:
            self.gmt_modified = m.get('GmtModified')
        if m.get('Id') is not None:
            self.id = m.get('Id')
        if m.get('InstId') is not None:
            self.inst_id = m.get('InstId')
        if m.get('RecallProgress') is not None:
            self.recall_progress = m.get('RecallProgress')
        if m.get('RecallRestoreType') is not None:
            self.recall_restore_type = m.get('RecallRestoreType')
        if m.get('RecallStatus') is not None:
            self.recall_status = m.get('RecallStatus')
        if m.get('RecallType') is not None:
            self.recall_type = m.get('RecallType')
        if m.get('SearchEndTime') is not None:
            self.search_end_time = m.get('SearchEndTime')
        if m.get('SearchStartTime') is not None:
            self.search_start_time = m.get('SearchStartTime')
        if m.get('SqlCounter') is not None:
            self.sql_counter = m.get('SqlCounter')
        if m.get('SqlPk') is not None:
            self.sql_pk = m.get('SqlPk')
        if m.get('SqlType') is not None:
            self.sql_type = m.get('SqlType')
        if m.get('TableName') is not None:
            self.table_name = m.get('TableName')
        if m.get('TraceId') is not None:
            self.trace_id = m.get('TraceId')
        return self


class DescribeSqlFlashbakTaskResponseBodySqlFlashbackTasks(TeaModel):
    def __init__(
        self,
        sql_flashback_task: List[DescribeSqlFlashbakTaskResponseBodySqlFlashbackTasksSqlFlashbackTask] = None,
    ):
        self.sql_flashback_task = sql_flashback_task

    def validate(self):
        if self.sql_flashback_task:
            for k in self.sql_flashback_task:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['SqlFlashbackTask'] = []
        if self.sql_flashback_task is not None:
            for k in self.sql_flashback_task:
                result['SqlFlashbackTask'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.sql_flashback_task = []
        if m.get('SqlFlashbackTask') is not None:
            for k in m.get('SqlFlashbackTask'):
                temp_model = DescribeSqlFlashbakTaskResponseBodySqlFlashbackTasksSqlFlashbackTask()
                self.sql_flashback_task.append(temp_model.from_map(k))
        return self


class DescribeSqlFlashbakTaskResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        sql_flashback_tasks: DescribeSqlFlashbakTaskResponseBodySqlFlashbackTasks = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.sql_flashback_tasks = sql_flashback_tasks
        self.success = success

    def validate(self):
        if self.sql_flashback_tasks:
            self.sql_flashback_tasks.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.sql_flashback_tasks is not None:
            result['SqlFlashbackTasks'] = self.sql_flashback_tasks.to_map()
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('SqlFlashbackTasks') is not None:
            temp_model = DescribeSqlFlashbakTaskResponseBodySqlFlashbackTasks()
            self.sql_flashback_tasks = temp_model.from_map(m['SqlFlashbackTasks'])
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeSqlFlashbakTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeSqlFlashbakTaskResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeSqlFlashbakTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeTableRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        region_id: str = None,
        table_name: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id
        self.table_name = table_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.table_name is not None:
            result['TableName'] = self.table_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TableName') is not None:
            self.table_name = m.get('TableName')
        return self


class DescribeTableResponseBodyDataList(TeaModel):
    def __init__(
        self,
        column_name: str = None,
        column_type: str = None,
        extra: str = None,
        index: str = None,
        is_allow_null: str = None,
        is_pk: str = None,
    ):
        self.column_name = column_name
        self.column_type = column_type
        self.extra = extra
        self.index = index
        self.is_allow_null = is_allow_null
        self.is_pk = is_pk

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.column_name is not None:
            result['ColumnName'] = self.column_name
        if self.column_type is not None:
            result['ColumnType'] = self.column_type
        if self.extra is not None:
            result['Extra'] = self.extra
        if self.index is not None:
            result['Index'] = self.index
        if self.is_allow_null is not None:
            result['IsAllowNull'] = self.is_allow_null
        if self.is_pk is not None:
            result['IsPk'] = self.is_pk
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ColumnName') is not None:
            self.column_name = m.get('ColumnName')
        if m.get('ColumnType') is not None:
            self.column_type = m.get('ColumnType')
        if m.get('Extra') is not None:
            self.extra = m.get('Extra')
        if m.get('Index') is not None:
            self.index = m.get('Index')
        if m.get('IsAllowNull') is not None:
            self.is_allow_null = m.get('IsAllowNull')
        if m.get('IsPk') is not None:
            self.is_pk = m.get('IsPk')
        return self


class DescribeTableResponseBodyData(TeaModel):
    def __init__(
        self,
        list: List[DescribeTableResponseBodyDataList] = None,
    ):
        self.list = list

    def validate(self):
        if self.list:
            for k in self.list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['List'] = []
        if self.list is not None:
            for k in self.list:
                result['List'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.list = []
        if m.get('List') is not None:
            for k in m.get('List'):
                temp_model = DescribeTableResponseBodyDataList()
                self.list.append(temp_model.from_map(k))
        return self


class DescribeTableResponseBody(TeaModel):
    def __init__(
        self,
        data: DescribeTableResponseBodyData = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.data:
            self.data.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data.to_map()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            temp_model = DescribeTableResponseBodyData()
            self.data = temp_model.from_map(m['Data'])
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DescribeTableResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeTableResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeTableResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeTableListByTypeRequest(TeaModel):
    def __init__(
        self,
        current_page: int = None,
        db_name: str = None,
        drds_instance_id: str = None,
        page_size: int = None,
        query: str = None,
        region_id: str = None,
        table_type: str = None,
    ):
        self.current_page = current_page
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.page_size = page_size
        self.query = query
        self.region_id = region_id
        self.table_type = table_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.current_page is not None:
            result['CurrentPage'] = self.current_page
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.query is not None:
            result['Query'] = self.query
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.table_type is not None:
            result['TableType'] = self.table_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CurrentPage') is not None:
            self.current_page = m.get('CurrentPage')
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Query') is not None:
            self.query = m.get('Query')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TableType') is not None:
            self.table_type = m.get('TableType')
        return self


class DescribeTableListByTypeResponseBodyList(TeaModel):
    def __init__(
        self,
        property: str = None,
        table_name: str = None,
    ):
        self.property = property
        self.table_name = table_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.property is not None:
            result['Property'] = self.property
        if self.table_name is not None:
            result['TableName'] = self.table_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Property') is not None:
            self.property = m.get('Property')
        if m.get('TableName') is not None:
            self.table_name = m.get('TableName')
        return self


class DescribeTableListByTypeResponseBody(TeaModel):
    def __init__(
        self,
        list: List[DescribeTableListByTypeResponseBodyList] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        success: bool = None,
        total: int = None,
    ):
        self.list = list
        self.page_number = page_number
        self.page_size = page_size
        self.request_id = request_id
        self.success = success
        self.total = total

    def validate(self):
        if self.list:
            for k in self.list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['List'] = []
        if self.list is not None:
            for k in self.list:
                result['List'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.list = []
        if m.get('List') is not None:
            for k in m.get('List'):
                temp_model = DescribeTableListByTypeResponseBodyList()
                self.list.append(temp_model.from_map(k))
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class DescribeTableListByTypeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeTableListByTypeResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeTableListByTypeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DescribeTablesRequest(TeaModel):
    def __init__(
        self,
        current_page: int = None,
        db_name: str = None,
        drds_instance_id: str = None,
        page_size: int = None,
        query: str = None,
        region_id: str = None,
    ):
        self.current_page = current_page
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.page_size = page_size
        self.query = query
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.current_page is not None:
            result['CurrentPage'] = self.current_page
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.query is not None:
            result['Query'] = self.query
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('CurrentPage') is not None:
            self.current_page = m.get('CurrentPage')
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('Query') is not None:
            self.query = m.get('Query')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class DescribeTablesResponseBodyList(TeaModel):
    def __init__(
        self,
        allow_full_table_scan: bool = None,
        broadcast: bool = None,
        db_inst_type: int = None,
        is_locked: bool = None,
        is_shard: bool = None,
        shard_key: str = None,
        status: int = None,
        table: str = None,
    ):
        self.allow_full_table_scan = allow_full_table_scan
        self.broadcast = broadcast
        self.db_inst_type = db_inst_type
        self.is_locked = is_locked
        self.is_shard = is_shard
        self.shard_key = shard_key
        self.status = status
        self.table = table

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.allow_full_table_scan is not None:
            result['AllowFullTableScan'] = self.allow_full_table_scan
        if self.broadcast is not None:
            result['Broadcast'] = self.broadcast
        if self.db_inst_type is not None:
            result['DbInstType'] = self.db_inst_type
        if self.is_locked is not None:
            result['IsLocked'] = self.is_locked
        if self.is_shard is not None:
            result['IsShard'] = self.is_shard
        if self.shard_key is not None:
            result['ShardKey'] = self.shard_key
        if self.status is not None:
            result['Status'] = self.status
        if self.table is not None:
            result['Table'] = self.table
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AllowFullTableScan') is not None:
            self.allow_full_table_scan = m.get('AllowFullTableScan')
        if m.get('Broadcast') is not None:
            self.broadcast = m.get('Broadcast')
        if m.get('DbInstType') is not None:
            self.db_inst_type = m.get('DbInstType')
        if m.get('IsLocked') is not None:
            self.is_locked = m.get('IsLocked')
        if m.get('IsShard') is not None:
            self.is_shard = m.get('IsShard')
        if m.get('ShardKey') is not None:
            self.shard_key = m.get('ShardKey')
        if m.get('Status') is not None:
            self.status = m.get('Status')
        if m.get('Table') is not None:
            self.table = m.get('Table')
        return self


class DescribeTablesResponseBody(TeaModel):
    def __init__(
        self,
        list: List[DescribeTablesResponseBodyList] = None,
        page_number: int = None,
        page_size: int = None,
        request_id: str = None,
        success: bool = None,
        total: int = None,
    ):
        self.list = list
        self.page_number = page_number
        self.page_size = page_size
        self.request_id = request_id
        self.success = success
        self.total = total

    def validate(self):
        if self.list:
            for k in self.list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['List'] = []
        if self.list is not None:
            for k in self.list:
                result['List'].append(k.to_map() if k else None)
        if self.page_number is not None:
            result['PageNumber'] = self.page_number
        if self.page_size is not None:
            result['PageSize'] = self.page_size
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.total is not None:
            result['Total'] = self.total
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.list = []
        if m.get('List') is not None:
            for k in m.get('List'):
                temp_model = DescribeTablesResponseBodyList()
                self.list.append(temp_model.from_map(k))
        if m.get('PageNumber') is not None:
            self.page_number = m.get('PageNumber')
        if m.get('PageSize') is not None:
            self.page_size = m.get('PageSize')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('Total') is not None:
            self.total = m.get('Total')
        return self


class DescribeTablesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DescribeTablesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DescribeTablesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class DisableSqlAuditRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class DisableSqlAuditResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: bool = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.result = result
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.result is not None:
            result['Result'] = self.result
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class DisableSqlAuditResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: DisableSqlAuditResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = DisableSqlAuditResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class EnableInstanceIpv6AddressRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
        region_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class EnableInstanceIpv6AddressResponseBody(TeaModel):
    def __init__(
        self,
        data: bool = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class EnableInstanceIpv6AddressResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: EnableInstanceIpv6AddressResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = EnableInstanceIpv6AddressResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class EnableSqlAuditRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        is_recall: bool = None,
        recall_end_timestamp: str = None,
        recall_start_timestamp: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.is_recall = is_recall
        self.recall_end_timestamp = recall_end_timestamp
        self.recall_start_timestamp = recall_start_timestamp

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.is_recall is not None:
            result['IsRecall'] = self.is_recall
        if self.recall_end_timestamp is not None:
            result['RecallEndTimestamp'] = self.recall_end_timestamp
        if self.recall_start_timestamp is not None:
            result['RecallStartTimestamp'] = self.recall_start_timestamp
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('IsRecall') is not None:
            self.is_recall = m.get('IsRecall')
        if m.get('RecallEndTimestamp') is not None:
            self.recall_end_timestamp = m.get('RecallEndTimestamp')
        if m.get('RecallStartTimestamp') is not None:
            self.recall_start_timestamp = m.get('RecallStartTimestamp')
        return self


class EnableSqlAuditResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: bool = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.result = result
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.result is not None:
            result['Result'] = self.result
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class EnableSqlAuditResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: EnableSqlAuditResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = EnableSqlAuditResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class EnableSqlFlashbackMatchSwitchRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class EnableSqlFlashbackMatchSwitchResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: bool = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.result = result
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.result is not None:
            result['Result'] = self.result
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class EnableSqlFlashbackMatchSwitchResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: EnableSqlFlashbackMatchSwitchResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = EnableSqlFlashbackMatchSwitchResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class FlashbackRecycleBinTableRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        region_id: str = None,
        table_name: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id
        self.table_name = table_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.table_name is not None:
            result['TableName'] = self.table_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TableName') is not None:
            self.table_name = m.get('TableName')
        return self


class FlashbackRecycleBinTableResponseBody(TeaModel):
    def __init__(
        self,
        data: bool = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class FlashbackRecycleBinTableResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: FlashbackRecycleBinTableResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = FlashbackRecycleBinTableResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class GetDrdsDbRdsRelationInfoRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class GetDrdsDbRdsRelationInfoResponseBodyData(TeaModel):
    def __init__(
        self,
        rds_instance_id: str = None,
        read_only_instance_info: List[str] = None,
        used_instance_id: str = None,
        used_instance_type: str = None,
    ):
        self.rds_instance_id = rds_instance_id
        self.read_only_instance_info = read_only_instance_info
        self.used_instance_id = used_instance_id
        self.used_instance_type = used_instance_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.rds_instance_id is not None:
            result['RdsInstanceId'] = self.rds_instance_id
        if self.read_only_instance_info is not None:
            result['ReadOnlyInstanceInfo'] = self.read_only_instance_info
        if self.used_instance_id is not None:
            result['UsedInstanceId'] = self.used_instance_id
        if self.used_instance_type is not None:
            result['UsedInstanceType'] = self.used_instance_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RdsInstanceId') is not None:
            self.rds_instance_id = m.get('RdsInstanceId')
        if m.get('ReadOnlyInstanceInfo') is not None:
            self.read_only_instance_info = m.get('ReadOnlyInstanceInfo')
        if m.get('UsedInstanceId') is not None:
            self.used_instance_id = m.get('UsedInstanceId')
        if m.get('UsedInstanceType') is not None:
            self.used_instance_type = m.get('UsedInstanceType')
        return self


class GetDrdsDbRdsRelationInfoResponseBody(TeaModel):
    def __init__(
        self,
        data: List[GetDrdsDbRdsRelationInfoResponseBodyData] = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Data'] = []
        if self.data is not None:
            for k in self.data:
                result['Data'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = GetDrdsDbRdsRelationInfoResponseBodyData()
                self.data.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class GetDrdsDbRdsRelationInfoResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: GetDrdsDbRdsRelationInfoResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = GetDrdsDbRdsRelationInfoResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ListTagResourcesRequestTag(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class ListTagResourcesRequest(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        region_id: str = None,
        resource_id: List[str] = None,
        resource_type: str = None,
        tag: List[ListTagResourcesRequestTag] = None,
    ):
        self.next_token = next_token
        self.region_id = region_id
        self.resource_id = resource_id
        self.resource_type = resource_type
        self.tag = tag

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = ListTagResourcesRequestTag()
                self.tag.append(temp_model.from_map(k))
        return self


class ListTagResourcesResponseBodyTagResourcesTagResource(TeaModel):
    def __init__(
        self,
        resource_id: str = None,
        resource_type: str = None,
        tag_key: str = None,
        tag_value: str = None,
    ):
        self.resource_id = resource_id
        self.resource_type = resource_type
        self.tag_key = tag_key
        self.tag_value = tag_value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        if self.tag_value is not None:
            result['TagValue'] = self.tag_value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        if m.get('TagValue') is not None:
            self.tag_value = m.get('TagValue')
        return self


class ListTagResourcesResponseBodyTagResources(TeaModel):
    def __init__(
        self,
        tag_resource: List[ListTagResourcesResponseBodyTagResourcesTagResource] = None,
    ):
        self.tag_resource = tag_resource

    def validate(self):
        if self.tag_resource:
            for k in self.tag_resource:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['TagResource'] = []
        if self.tag_resource is not None:
            for k in self.tag_resource:
                result['TagResource'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.tag_resource = []
        if m.get('TagResource') is not None:
            for k in m.get('TagResource'):
                temp_model = ListTagResourcesResponseBodyTagResourcesTagResource()
                self.tag_resource.append(temp_model.from_map(k))
        return self


class ListTagResourcesResponseBody(TeaModel):
    def __init__(
        self,
        next_token: str = None,
        request_id: str = None,
        success: bool = None,
        tag_resources: ListTagResourcesResponseBodyTagResources = None,
    ):
        self.next_token = next_token
        self.request_id = request_id
        self.success = success
        self.tag_resources = tag_resources

    def validate(self):
        if self.tag_resources:
            self.tag_resources.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.next_token is not None:
            result['NextToken'] = self.next_token
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.tag_resources is not None:
            result['TagResources'] = self.tag_resources.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('NextToken') is not None:
            self.next_token = m.get('NextToken')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TagResources') is not None:
            temp_model = ListTagResourcesResponseBodyTagResources()
            self.tag_resources = temp_model.from_map(m['TagResources'])
        return self


class ListTagResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ListTagResourcesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ListTagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ManagePrivateRdsRequest(TeaModel):
    def __init__(
        self,
        dbinstance_id: str = None,
        drds_instance_id: str = None,
        params: str = None,
        rds_action: str = None,
        region_id: str = None,
    ):
        self.dbinstance_id = dbinstance_id
        self.drds_instance_id = drds_instance_id
        self.params = params
        self.rds_action = rds_action
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.params is not None:
            result['Params'] = self.params
        if self.rds_action is not None:
            result['RdsAction'] = self.rds_action
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('Params') is not None:
            self.params = m.get('Params')
        if m.get('RdsAction') is not None:
            self.rds_action = m.get('RdsAction')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class ManagePrivateRdsResponseBody(TeaModel):
    def __init__(
        self,
        data: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ManagePrivateRdsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ManagePrivateRdsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ManagePrivateRdsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyAccountDescriptionRequest(TeaModel):
    def __init__(
        self,
        account_name: str = None,
        description: str = None,
        drds_instance_id: str = None,
    ):
        self.account_name = account_name
        self.description = description
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_name is not None:
            result['AccountName'] = self.account_name
        if self.description is not None:
            result['Description'] = self.description
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountName') is not None:
            self.account_name = m.get('AccountName')
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class ModifyAccountDescriptionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ModifyAccountDescriptionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyAccountDescriptionResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyAccountDescriptionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyAccountPrivilegeRequestDbPrivilege(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        privilege: str = None,
    ):
        self.db_name = db_name
        self.privilege = privilege

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.privilege is not None:
            result['Privilege'] = self.privilege
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('Privilege') is not None:
            self.privilege = m.get('Privilege')
        return self


class ModifyAccountPrivilegeRequest(TeaModel):
    def __init__(
        self,
        account_name: str = None,
        db_privilege: List[ModifyAccountPrivilegeRequestDbPrivilege] = None,
        drds_instance_id: str = None,
        region_id: str = None,
    ):
        self.account_name = account_name
        self.db_privilege = db_privilege
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id

    def validate(self):
        if self.db_privilege:
            for k in self.db_privilege:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_name is not None:
            result['AccountName'] = self.account_name
        result['DbPrivilege'] = []
        if self.db_privilege is not None:
            for k in self.db_privilege:
                result['DbPrivilege'].append(k.to_map() if k else None)
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountName') is not None:
            self.account_name = m.get('AccountName')
        self.db_privilege = []
        if m.get('DbPrivilege') is not None:
            for k in m.get('DbPrivilege'):
                temp_model = ModifyAccountPrivilegeRequestDbPrivilege()
                self.db_privilege.append(temp_model.from_map(k))
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class ModifyAccountPrivilegeResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ModifyAccountPrivilegeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyAccountPrivilegeResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyAccountPrivilegeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyDrdsInstanceDescriptionRequest(TeaModel):
    def __init__(
        self,
        description: str = None,
        drds_instance_id: str = None,
    ):
        self.description = description
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.description is not None:
            result['Description'] = self.description
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Description') is not None:
            self.description = m.get('Description')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class ModifyDrdsInstanceDescriptionResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ModifyDrdsInstanceDescriptionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyDrdsInstanceDescriptionResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyDrdsInstanceDescriptionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyDrdsIpWhiteListRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        group_attribute: str = None,
        group_name: str = None,
        ip_white_list: str = None,
        mode: bool = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.group_attribute = group_attribute
        self.group_name = group_name
        self.ip_white_list = ip_white_list
        self.mode = mode

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.group_attribute is not None:
            result['GroupAttribute'] = self.group_attribute
        if self.group_name is not None:
            result['GroupName'] = self.group_name
        if self.ip_white_list is not None:
            result['IpWhiteList'] = self.ip_white_list
        if self.mode is not None:
            result['Mode'] = self.mode
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('GroupAttribute') is not None:
            self.group_attribute = m.get('GroupAttribute')
        if m.get('GroupName') is not None:
            self.group_name = m.get('GroupName')
        if m.get('IpWhiteList') is not None:
            self.ip_white_list = m.get('IpWhiteList')
        if m.get('Mode') is not None:
            self.mode = m.get('Mode')
        return self


class ModifyDrdsIpWhiteListResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ModifyDrdsIpWhiteListResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyDrdsIpWhiteListResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyDrdsIpWhiteListResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyPolarDbReadWeightRequest(TeaModel):
    def __init__(
        self,
        db_instance_id: str = None,
        db_name: str = None,
        db_node_ids: str = None,
        drds_instance_id: str = None,
        weights: str = None,
    ):
        self.db_instance_id = db_instance_id
        self.db_name = db_name
        self.db_node_ids = db_node_ids
        self.drds_instance_id = drds_instance_id
        self.weights = weights

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_instance_id is not None:
            result['DbInstanceId'] = self.db_instance_id
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.db_node_ids is not None:
            result['DbNodeIds'] = self.db_node_ids
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.weights is not None:
            result['Weights'] = self.weights
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbInstanceId') is not None:
            self.db_instance_id = m.get('DbInstanceId')
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DbNodeIds') is not None:
            self.db_node_ids = m.get('DbNodeIds')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('Weights') is not None:
            self.weights = m.get('Weights')
        return self


class ModifyPolarDbReadWeightResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ModifyPolarDbReadWeightResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyPolarDbReadWeightResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyPolarDbReadWeightResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ModifyRdsReadWeightRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        instance_names: str = None,
        weights: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.instance_names = instance_names
        self.weights = weights

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.instance_names is not None:
            result['InstanceNames'] = self.instance_names
        if self.weights is not None:
            result['Weights'] = self.weights
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('InstanceNames') is not None:
            self.instance_names = m.get('InstanceNames')
        if m.get('Weights') is not None:
            self.weights = m.get('Weights')
        return self


class ModifyRdsReadWeightResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ModifyRdsReadWeightResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ModifyRdsReadWeightResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ModifyRdsReadWeightResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class PutStartBackupRequest(TeaModel):
    def __init__(
        self,
        backup_db_names: str = None,
        backup_level: str = None,
        backup_mode: str = None,
        drds_instance_id: str = None,
    ):
        self.backup_db_names = backup_db_names
        self.backup_level = backup_level
        self.backup_mode = backup_mode
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.backup_db_names is not None:
            result['BackupDbNames'] = self.backup_db_names
        if self.backup_level is not None:
            result['BackupLevel'] = self.backup_level
        if self.backup_mode is not None:
            result['BackupMode'] = self.backup_mode
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BackupDbNames') is not None:
            self.backup_db_names = m.get('BackupDbNames')
        if m.get('BackupLevel') is not None:
            self.backup_level = m.get('BackupLevel')
        if m.get('BackupMode') is not None:
            self.backup_mode = m.get('BackupMode')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class PutStartBackupResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.result = result
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.result is not None:
            result['Result'] = self.result
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class PutStartBackupResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: PutStartBackupResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = PutStartBackupResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RefreshDrdsAtomUrlRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class RefreshDrdsAtomUrlResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: bool = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.result = result
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.result is not None:
            result['Result'] = self.result
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class RefreshDrdsAtomUrlResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RefreshDrdsAtomUrlResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RefreshDrdsAtomUrlResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ReleaseInstanceInternetAddressRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
        region_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class ReleaseInstanceInternetAddressResponseBody(TeaModel):
    def __init__(
        self,
        data: bool = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class ReleaseInstanceInternetAddressResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ReleaseInstanceInternetAddressResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ReleaseInstanceInternetAddressResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RemoveBackupsSetRequest(TeaModel):
    def __init__(
        self,
        backup_id: str = None,
        drds_instance_id: str = None,
    ):
        self.backup_id = backup_id
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.backup_id is not None:
            result['BackupId'] = self.backup_id
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BackupId') is not None:
            self.backup_id = m.get('BackupId')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class RemoveBackupsSetResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.result = result
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.result is not None:
            result['Result'] = self.result
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class RemoveBackupsSetResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RemoveBackupsSetResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RemoveBackupsSetResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RemoveDrdsDbRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class RemoveDrdsDbResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class RemoveDrdsDbResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RemoveDrdsDbResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RemoveDrdsDbResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RemoveDrdsDbFailedRecordRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class RemoveDrdsDbFailedRecordResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: bool = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.result = result
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.result is not None:
            result['Result'] = self.result
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class RemoveDrdsDbFailedRecordResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RemoveDrdsDbFailedRecordResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RemoveDrdsDbFailedRecordResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RemoveDrdsInstanceRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class RemoveDrdsInstanceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class RemoveDrdsInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RemoveDrdsInstanceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RemoveDrdsInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RemoveInstanceAccountRequest(TeaModel):
    def __init__(
        self,
        account_name: str = None,
        drds_instance_id: str = None,
    ):
        self.account_name = account_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.account_name is not None:
            result['AccountName'] = self.account_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AccountName') is not None:
            self.account_name = m.get('AccountName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class RemoveInstanceAccountResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class RemoveInstanceAccountResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RemoveInstanceAccountResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RemoveInstanceAccountResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RemoveRecycleBinTableRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        region_id: str = None,
        table_name: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id
        self.table_name = table_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.table_name is not None:
            result['TableName'] = self.table_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TableName') is not None:
            self.table_name = m.get('TableName')
        return self


class RemoveRecycleBinTableResponseBody(TeaModel):
    def __init__(
        self,
        data: bool = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class RemoveRecycleBinTableResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RemoveRecycleBinTableResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RemoveRecycleBinTableResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RestartDrdsInstanceRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class RestartDrdsInstanceResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
        task_id: int = None,
    ):
        self.request_id = request_id
        self.success = success
        self.task_id = task_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class RestartDrdsInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RestartDrdsInstanceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RestartDrdsInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class RollbackInstanceVersionRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
        region_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class RollbackInstanceVersionResponseBody(TeaModel):
    def __init__(
        self,
        data: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class RollbackInstanceVersionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: RollbackInstanceVersionResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = RollbackInstanceVersionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetBackupLocalRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
        high_space_usage_protection: str = None,
        local_log_retention_hours: str = None,
        local_log_retention_space: str = None,
    ):
        self.drds_instance_id = drds_instance_id
        self.high_space_usage_protection = high_space_usage_protection
        self.local_log_retention_hours = local_log_retention_hours
        self.local_log_retention_space = local_log_retention_space

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.high_space_usage_protection is not None:
            result['HighSpaceUsageProtection'] = self.high_space_usage_protection
        if self.local_log_retention_hours is not None:
            result['LocalLogRetentionHours'] = self.local_log_retention_hours
        if self.local_log_retention_space is not None:
            result['LocalLogRetentionSpace'] = self.local_log_retention_space
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('HighSpaceUsageProtection') is not None:
            self.high_space_usage_protection = m.get('HighSpaceUsageProtection')
        if m.get('LocalLogRetentionHours') is not None:
            self.local_log_retention_hours = m.get('LocalLogRetentionHours')
        if m.get('LocalLogRetentionSpace') is not None:
            self.local_log_retention_space = m.get('LocalLogRetentionSpace')
        return self


class SetBackupLocalResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.result = result
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.result is not None:
            result['Result'] = self.result
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class SetBackupLocalResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetBackupLocalResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetBackupLocalResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetBackupPolicyRequest(TeaModel):
    def __init__(
        self,
        backup_db_names: str = None,
        backup_level: str = None,
        backup_log: str = None,
        backup_mode: str = None,
        data_backup_retention_period: str = None,
        drds_instance_id: str = None,
        log_backup_retention_period: str = None,
        preferred_backup_end_time: str = None,
        preferred_backup_period: str = None,
        preferred_backup_start_time: str = None,
    ):
        self.backup_db_names = backup_db_names
        self.backup_level = backup_level
        self.backup_log = backup_log
        self.backup_mode = backup_mode
        self.data_backup_retention_period = data_backup_retention_period
        self.drds_instance_id = drds_instance_id
        self.log_backup_retention_period = log_backup_retention_period
        self.preferred_backup_end_time = preferred_backup_end_time
        self.preferred_backup_period = preferred_backup_period
        self.preferred_backup_start_time = preferred_backup_start_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.backup_db_names is not None:
            result['BackupDbNames'] = self.backup_db_names
        if self.backup_level is not None:
            result['BackupLevel'] = self.backup_level
        if self.backup_log is not None:
            result['BackupLog'] = self.backup_log
        if self.backup_mode is not None:
            result['BackupMode'] = self.backup_mode
        if self.data_backup_retention_period is not None:
            result['DataBackupRetentionPeriod'] = self.data_backup_retention_period
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.log_backup_retention_period is not None:
            result['LogBackupRetentionPeriod'] = self.log_backup_retention_period
        if self.preferred_backup_end_time is not None:
            result['PreferredBackupEndTime'] = self.preferred_backup_end_time
        if self.preferred_backup_period is not None:
            result['PreferredBackupPeriod'] = self.preferred_backup_period
        if self.preferred_backup_start_time is not None:
            result['PreferredBackupStartTime'] = self.preferred_backup_start_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BackupDbNames') is not None:
            self.backup_db_names = m.get('BackupDbNames')
        if m.get('BackupLevel') is not None:
            self.backup_level = m.get('BackupLevel')
        if m.get('BackupLog') is not None:
            self.backup_log = m.get('BackupLog')
        if m.get('BackupMode') is not None:
            self.backup_mode = m.get('BackupMode')
        if m.get('DataBackupRetentionPeriod') is not None:
            self.data_backup_retention_period = m.get('DataBackupRetentionPeriod')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('LogBackupRetentionPeriod') is not None:
            self.log_backup_retention_period = m.get('LogBackupRetentionPeriod')
        if m.get('PreferredBackupEndTime') is not None:
            self.preferred_backup_end_time = m.get('PreferredBackupEndTime')
        if m.get('PreferredBackupPeriod') is not None:
            self.preferred_backup_period = m.get('PreferredBackupPeriod')
        if m.get('PreferredBackupStartTime') is not None:
            self.preferred_backup_start_time = m.get('PreferredBackupStartTime')
        return self


class SetBackupPolicyResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.result = result
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.result is not None:
            result['Result'] = self.result
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class SetBackupPolicyResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetBackupPolicyResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetBackupPolicyResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetupBroadcastTablesRequest(TeaModel):
    def __init__(
        self,
        active: bool = None,
        db_name: str = None,
        drds_instance_id: str = None,
        region_id: str = None,
        table_name: List[str] = None,
    ):
        self.active = active
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id
        self.table_name = table_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.active is not None:
            result['Active'] = self.active
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.table_name is not None:
            result['TableName'] = self.table_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Active') is not None:
            self.active = m.get('Active')
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TableName') is not None:
            self.table_name = m.get('TableName')
        return self


class SetupBroadcastTablesResponseBody(TeaModel):
    def __init__(
        self,
        data: bool = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class SetupBroadcastTablesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetupBroadcastTablesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetupBroadcastTablesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetupDrdsParamsRequestData(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        param_ranges: str = None,
        param_type: str = None,
        param_value: str = None,
        param_variable_name: str = None,
    ):
        self.db_name = db_name
        self.param_ranges = param_ranges
        self.param_type = param_type
        self.param_value = param_value
        self.param_variable_name = param_variable_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.param_ranges is not None:
            result['ParamRanges'] = self.param_ranges
        if self.param_type is not None:
            result['ParamType'] = self.param_type
        if self.param_value is not None:
            result['ParamValue'] = self.param_value
        if self.param_variable_name is not None:
            result['ParamVariableName'] = self.param_variable_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('ParamRanges') is not None:
            self.param_ranges = m.get('ParamRanges')
        if m.get('ParamType') is not None:
            self.param_type = m.get('ParamType')
        if m.get('ParamValue') is not None:
            self.param_value = m.get('ParamValue')
        if m.get('ParamVariableName') is not None:
            self.param_variable_name = m.get('ParamVariableName')
        return self


class SetupDrdsParamsRequest(TeaModel):
    def __init__(
        self,
        data: List[SetupDrdsParamsRequestData] = None,
        drds_instance_id: str = None,
        param_level: str = None,
        region_id: str = None,
    ):
        self.data = data
        self.drds_instance_id = drds_instance_id
        self.param_level = param_level
        self.region_id = region_id

    def validate(self):
        if self.data:
            for k in self.data:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['Data'] = []
        if self.data is not None:
            for k in self.data:
                result['Data'].append(k.to_map() if k else None)
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.param_level is not None:
            result['ParamLevel'] = self.param_level
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.data = []
        if m.get('Data') is not None:
            for k in m.get('Data'):
                temp_model = SetupDrdsParamsRequestData()
                self.data.append(temp_model.from_map(k))
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('ParamLevel') is not None:
            self.param_level = m.get('ParamLevel')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class SetupDrdsParamsResponseBody(TeaModel):
    def __init__(
        self,
        data: bool = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class SetupDrdsParamsResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetupDrdsParamsResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetupDrdsParamsResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetupRecycleBinStatusRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        region_id: str = None,
        status_action: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id
        self.status_action = status_action

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.status_action is not None:
            result['StatusAction'] = self.status_action
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('StatusAction') is not None:
            self.status_action = m.get('StatusAction')
        return self


class SetupRecycleBinStatusResponseBody(TeaModel):
    def __init__(
        self,
        data: bool = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class SetupRecycleBinStatusResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetupRecycleBinStatusResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetupRecycleBinStatusResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SetupTableRequest(TeaModel):
    def __init__(
        self,
        allow_full_table_scan: bool = None,
        db_name: str = None,
        drds_instance_id: str = None,
        region_id: str = None,
        table_name: List[str] = None,
    ):
        self.allow_full_table_scan = allow_full_table_scan
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id
        self.table_name = table_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.allow_full_table_scan is not None:
            result['AllowFullTableScan'] = self.allow_full_table_scan
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.table_name is not None:
            result['TableName'] = self.table_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AllowFullTableScan') is not None:
            self.allow_full_table_scan = m.get('AllowFullTableScan')
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('TableName') is not None:
            self.table_name = m.get('TableName')
        return self


class SetupTableResponseBody(TeaModel):
    def __init__(
        self,
        data: bool = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class SetupTableResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SetupTableResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SetupTableResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class StartRestoreRequest(TeaModel):
    def __init__(
        self,
        backup_db_names: str = None,
        backup_id: str = None,
        backup_level: str = None,
        backup_mode: str = None,
        drds_instance_id: str = None,
        preferred_backup_time: str = None,
    ):
        self.backup_db_names = backup_db_names
        self.backup_id = backup_id
        self.backup_level = backup_level
        self.backup_mode = backup_mode
        self.drds_instance_id = drds_instance_id
        self.preferred_backup_time = preferred_backup_time

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.backup_db_names is not None:
            result['BackupDbNames'] = self.backup_db_names
        if self.backup_id is not None:
            result['BackupId'] = self.backup_id
        if self.backup_level is not None:
            result['BackupLevel'] = self.backup_level
        if self.backup_mode is not None:
            result['BackupMode'] = self.backup_mode
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.preferred_backup_time is not None:
            result['PreferredBackupTime'] = self.preferred_backup_time
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('BackupDbNames') is not None:
            self.backup_db_names = m.get('BackupDbNames')
        if m.get('BackupId') is not None:
            self.backup_id = m.get('BackupId')
        if m.get('BackupLevel') is not None:
            self.backup_level = m.get('BackupLevel')
        if m.get('BackupMode') is not None:
            self.backup_mode = m.get('BackupMode')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('PreferredBackupTime') is not None:
            self.preferred_backup_time = m.get('PreferredBackupTime')
        return self


class StartRestoreResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        result: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.result = result
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.result is not None:
            result['Result'] = self.result
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class StartRestoreResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: StartRestoreResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = StartRestoreResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SubmitCleanTaskRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        expand_type: str = None,
        job_id: str = None,
        parent_job_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.expand_type = expand_type
        self.job_id = job_id
        self.parent_job_id = parent_job_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.expand_type is not None:
            result['ExpandType'] = self.expand_type
        if self.job_id is not None:
            result['JobId'] = self.job_id
        if self.parent_job_id is not None:
            result['ParentJobId'] = self.parent_job_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('ExpandType') is not None:
            self.expand_type = m.get('ExpandType')
        if m.get('JobId') is not None:
            self.job_id = m.get('JobId')
        if m.get('ParentJobId') is not None:
            self.parent_job_id = m.get('ParentJobId')
        return self


class SubmitCleanTaskResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class SubmitCleanTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SubmitCleanTaskResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SubmitCleanTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SubmitHotExpandPreCheckTaskRequest(TeaModel):
    def __init__(
        self,
        db_inst_type: str = None,
        db_name: str = None,
        drds_instance_id: str = None,
        table_list: List[str] = None,
    ):
        self.db_inst_type = db_inst_type
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.table_list = table_list

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_inst_type is not None:
            result['DbInstType'] = self.db_inst_type
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.table_list is not None:
            result['TableList'] = self.table_list
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbInstType') is not None:
            self.db_inst_type = m.get('DbInstType')
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('TableList') is not None:
            self.table_list = m.get('TableList')
        return self


class SubmitHotExpandPreCheckTaskResponseBody(TeaModel):
    def __init__(
        self,
        msg: str = None,
        request_id: str = None,
        success: bool = None,
        task_id: int = None,
    ):
        self.msg = msg
        self.request_id = request_id
        self.success = success
        self.task_id = task_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.msg is not None:
            result['Msg'] = self.msg
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Msg') is not None:
            self.msg = m.get('Msg')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class SubmitHotExpandPreCheckTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SubmitHotExpandPreCheckTaskResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SubmitHotExpandPreCheckTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SubmitHotExpandTaskRequestExtendedMapping(TeaModel):
    def __init__(
        self,
        src_db: str = None,
        src_instance_id: str = None,
    ):
        self.src_db = src_db
        self.src_instance_id = src_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.src_db is not None:
            result['SrcDb'] = self.src_db
        if self.src_instance_id is not None:
            result['SrcInstanceId'] = self.src_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('SrcDb') is not None:
            self.src_db = m.get('SrcDb')
        if m.get('SrcInstanceId') is not None:
            self.src_instance_id = m.get('SrcInstanceId')
        return self


class SubmitHotExpandTaskRequestInstanceDbMapping(TeaModel):
    def __init__(
        self,
        db_list: str = None,
        instance_name: str = None,
    ):
        self.db_list = db_list
        self.instance_name = instance_name

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_list is not None:
            result['DbList'] = self.db_list
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbList') is not None:
            self.db_list = m.get('DbList')
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        return self


class SubmitHotExpandTaskRequestMapping(TeaModel):
    def __init__(
        self,
        db_shard_column: str = None,
        hot_db_name: str = None,
        hot_table_name: str = None,
        logic_table: str = None,
        shard_db_value: str = None,
        shard_tb_value: str = None,
        tb_shard_column: str = None,
    ):
        self.db_shard_column = db_shard_column
        self.hot_db_name = hot_db_name
        self.hot_table_name = hot_table_name
        self.logic_table = logic_table
        self.shard_db_value = shard_db_value
        self.shard_tb_value = shard_tb_value
        self.tb_shard_column = tb_shard_column

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_shard_column is not None:
            result['DbShardColumn'] = self.db_shard_column
        if self.hot_db_name is not None:
            result['HotDbName'] = self.hot_db_name
        if self.hot_table_name is not None:
            result['HotTableName'] = self.hot_table_name
        if self.logic_table is not None:
            result['LogicTable'] = self.logic_table
        if self.shard_db_value is not None:
            result['ShardDbValue'] = self.shard_db_value
        if self.shard_tb_value is not None:
            result['ShardTbValue'] = self.shard_tb_value
        if self.tb_shard_column is not None:
            result['TbShardColumn'] = self.tb_shard_column
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbShardColumn') is not None:
            self.db_shard_column = m.get('DbShardColumn')
        if m.get('HotDbName') is not None:
            self.hot_db_name = m.get('HotDbName')
        if m.get('HotTableName') is not None:
            self.hot_table_name = m.get('HotTableName')
        if m.get('LogicTable') is not None:
            self.logic_table = m.get('LogicTable')
        if m.get('ShardDbValue') is not None:
            self.shard_db_value = m.get('ShardDbValue')
        if m.get('ShardTbValue') is not None:
            self.shard_tb_value = m.get('ShardTbValue')
        if m.get('TbShardColumn') is not None:
            self.tb_shard_column = m.get('TbShardColumn')
        return self


class SubmitHotExpandTaskRequestSupperAccountMapping(TeaModel):
    def __init__(
        self,
        instance_name: str = None,
        supper_account: str = None,
        supper_password: str = None,
    ):
        self.instance_name = instance_name
        self.supper_account = supper_account
        self.supper_password = supper_password

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.instance_name is not None:
            result['InstanceName'] = self.instance_name
        if self.supper_account is not None:
            result['SupperAccount'] = self.supper_account
        if self.supper_password is not None:
            result['SupperPassword'] = self.supper_password
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('InstanceName') is not None:
            self.instance_name = m.get('InstanceName')
        if m.get('SupperAccount') is not None:
            self.supper_account = m.get('SupperAccount')
        if m.get('SupperPassword') is not None:
            self.supper_password = m.get('SupperPassword')
        return self


class SubmitHotExpandTaskRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        extended_mapping: List[SubmitHotExpandTaskRequestExtendedMapping] = None,
        instance_db_mapping: List[SubmitHotExpandTaskRequestInstanceDbMapping] = None,
        mapping: List[SubmitHotExpandTaskRequestMapping] = None,
        supper_account_mapping: List[SubmitHotExpandTaskRequestSupperAccountMapping] = None,
        task_desc: str = None,
        task_name: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.extended_mapping = extended_mapping
        self.instance_db_mapping = instance_db_mapping
        self.mapping = mapping
        self.supper_account_mapping = supper_account_mapping
        self.task_desc = task_desc
        self.task_name = task_name

    def validate(self):
        if self.extended_mapping:
            for k in self.extended_mapping:
                if k:
                    k.validate()
        if self.instance_db_mapping:
            for k in self.instance_db_mapping:
                if k:
                    k.validate()
        if self.mapping:
            for k in self.mapping:
                if k:
                    k.validate()
        if self.supper_account_mapping:
            for k in self.supper_account_mapping:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        result['ExtendedMapping'] = []
        if self.extended_mapping is not None:
            for k in self.extended_mapping:
                result['ExtendedMapping'].append(k.to_map() if k else None)
        result['InstanceDbMapping'] = []
        if self.instance_db_mapping is not None:
            for k in self.instance_db_mapping:
                result['InstanceDbMapping'].append(k.to_map() if k else None)
        result['Mapping'] = []
        if self.mapping is not None:
            for k in self.mapping:
                result['Mapping'].append(k.to_map() if k else None)
        result['SupperAccountMapping'] = []
        if self.supper_account_mapping is not None:
            for k in self.supper_account_mapping:
                result['SupperAccountMapping'].append(k.to_map() if k else None)
        if self.task_desc is not None:
            result['TaskDesc'] = self.task_desc
        if self.task_name is not None:
            result['TaskName'] = self.task_name
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        self.extended_mapping = []
        if m.get('ExtendedMapping') is not None:
            for k in m.get('ExtendedMapping'):
                temp_model = SubmitHotExpandTaskRequestExtendedMapping()
                self.extended_mapping.append(temp_model.from_map(k))
        self.instance_db_mapping = []
        if m.get('InstanceDbMapping') is not None:
            for k in m.get('InstanceDbMapping'):
                temp_model = SubmitHotExpandTaskRequestInstanceDbMapping()
                self.instance_db_mapping.append(temp_model.from_map(k))
        self.mapping = []
        if m.get('Mapping') is not None:
            for k in m.get('Mapping'):
                temp_model = SubmitHotExpandTaskRequestMapping()
                self.mapping.append(temp_model.from_map(k))
        self.supper_account_mapping = []
        if m.get('SupperAccountMapping') is not None:
            for k in m.get('SupperAccountMapping'):
                temp_model = SubmitHotExpandTaskRequestSupperAccountMapping()
                self.supper_account_mapping.append(temp_model.from_map(k))
        if m.get('TaskDesc') is not None:
            self.task_desc = m.get('TaskDesc')
        if m.get('TaskName') is not None:
            self.task_name = m.get('TaskName')
        return self


class SubmitHotExpandTaskResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class SubmitHotExpandTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SubmitHotExpandTaskResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SubmitHotExpandTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SubmitSmoothExpandPreCheckRequest(TeaModel):
    def __init__(
        self,
        db_inst_type: str = None,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_inst_type = db_inst_type
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_inst_type is not None:
            result['DbInstType'] = self.db_inst_type
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbInstType') is not None:
            self.db_inst_type = m.get('DbInstType')
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class SubmitSmoothExpandPreCheckResponseBody(TeaModel):
    def __init__(
        self,
        msg: str = None,
        request_id: str = None,
        success: bool = None,
        task_id: int = None,
    ):
        self.msg = msg
        self.request_id = request_id
        self.success = success
        self.task_id = task_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.msg is not None:
            result['Msg'] = self.msg
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Msg') is not None:
            self.msg = m.get('Msg')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class SubmitSmoothExpandPreCheckResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SubmitSmoothExpandPreCheckResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SubmitSmoothExpandPreCheckResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SubmitSmoothExpandPreCheckTaskRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        return self


class SubmitSmoothExpandPreCheckTaskResponseBody(TeaModel):
    def __init__(
        self,
        msg: str = None,
        request_id: str = None,
        success: bool = None,
        task_id: int = None,
    ):
        self.msg = msg
        self.request_id = request_id
        self.success = success
        self.task_id = task_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.msg is not None:
            result['Msg'] = self.msg
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Msg') is not None:
            self.msg = m.get('Msg')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class SubmitSmoothExpandPreCheckTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SubmitSmoothExpandPreCheckTaskResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SubmitSmoothExpandPreCheckTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SubmitSqlFlashbackTaskRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        end_time: str = None,
        recall_restore_type: int = None,
        recall_type: int = None,
        sql_pk: str = None,
        sql_type: str = None,
        start_time: str = None,
        table_name: str = None,
        trace_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.end_time = end_time
        self.recall_restore_type = recall_restore_type
        self.recall_type = recall_type
        self.sql_pk = sql_pk
        self.sql_type = sql_type
        self.start_time = start_time
        self.table_name = table_name
        self.trace_id = trace_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.end_time is not None:
            result['EndTime'] = self.end_time
        if self.recall_restore_type is not None:
            result['RecallRestoreType'] = self.recall_restore_type
        if self.recall_type is not None:
            result['RecallType'] = self.recall_type
        if self.sql_pk is not None:
            result['SqlPk'] = self.sql_pk
        if self.sql_type is not None:
            result['SqlType'] = self.sql_type
        if self.start_time is not None:
            result['StartTime'] = self.start_time
        if self.table_name is not None:
            result['TableName'] = self.table_name
        if self.trace_id is not None:
            result['TraceId'] = self.trace_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('EndTime') is not None:
            self.end_time = m.get('EndTime')
        if m.get('RecallRestoreType') is not None:
            self.recall_restore_type = m.get('RecallRestoreType')
        if m.get('RecallType') is not None:
            self.recall_type = m.get('RecallType')
        if m.get('SqlPk') is not None:
            self.sql_pk = m.get('SqlPk')
        if m.get('SqlType') is not None:
            self.sql_type = m.get('SqlType')
        if m.get('StartTime') is not None:
            self.start_time = m.get('StartTime')
        if m.get('TableName') is not None:
            self.table_name = m.get('TableName')
        if m.get('TraceId') is not None:
            self.trace_id = m.get('TraceId')
        return self


class SubmitSqlFlashbackTaskResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
        task_id: int = None,
    ):
        self.request_id = request_id
        self.success = success
        self.task_id = task_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        if self.task_id is not None:
            result['TaskId'] = self.task_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        if m.get('TaskId') is not None:
            self.task_id = m.get('TaskId')
        return self


class SubmitSqlFlashbackTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SubmitSqlFlashbackTaskResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SubmitSqlFlashbackTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class SwitchGlobalBroadcastTypeRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        region_id: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class SwitchGlobalBroadcastTypeResponseBody(TeaModel):
    def __init__(
        self,
        data: bool = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class SwitchGlobalBroadcastTypeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: SwitchGlobalBroadcastTypeResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = SwitchGlobalBroadcastTypeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class TagResourcesRequestTag(TeaModel):
    def __init__(
        self,
        key: str = None,
        value: str = None,
    ):
        self.key = key
        self.value = value

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.key is not None:
            result['Key'] = self.key
        if self.value is not None:
            result['Value'] = self.value
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Key') is not None:
            self.key = m.get('Key')
        if m.get('Value') is not None:
            self.value = m.get('Value')
        return self


class TagResourcesRequest(TeaModel):
    def __init__(
        self,
        region_id: str = None,
        resource_id: List[str] = None,
        resource_type: str = None,
        tag: List[TagResourcesRequestTag] = None,
    ):
        self.region_id = region_id
        self.resource_id = resource_id
        self.resource_type = resource_type
        self.tag = tag

    def validate(self):
        if self.tag:
            for k in self.tag:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        result['Tag'] = []
        if self.tag is not None:
            for k in self.tag:
                result['Tag'].append(k.to_map() if k else None)
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        self.tag = []
        if m.get('Tag') is not None:
            for k in m.get('Tag'):
                temp_model = TagResourcesRequestTag()
                self.tag.append(temp_model.from_map(k))
        return self


class TagResourcesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class TagResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: TagResourcesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = TagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UntagResourcesRequest(TeaModel):
    def __init__(
        self,
        all: bool = None,
        region_id: str = None,
        resource_id: List[str] = None,
        resource_type: str = None,
        tag_key: List[str] = None,
    ):
        self.all = all
        self.region_id = region_id
        self.resource_id = resource_id
        self.resource_type = resource_type
        self.tag_key = tag_key

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.all is not None:
            result['All'] = self.all
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.resource_id is not None:
            result['ResourceId'] = self.resource_id
        if self.resource_type is not None:
            result['ResourceType'] = self.resource_type
        if self.tag_key is not None:
            result['TagKey'] = self.tag_key
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('All') is not None:
            self.all = m.get('All')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('ResourceId') is not None:
            self.resource_id = m.get('ResourceId')
        if m.get('ResourceType') is not None:
            self.resource_type = m.get('ResourceType')
        if m.get('TagKey') is not None:
            self.tag_key = m.get('TagKey')
        return self


class UntagResourcesResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class UntagResourcesResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UntagResourcesResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UntagResourcesResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateInstanceNetworkRequest(TeaModel):
    def __init__(
        self,
        classic_expired_days: int = None,
        drds_instance_id: str = None,
        retain_classic: bool = None,
        src_instance_network_type: str = None,
    ):
        self.classic_expired_days = classic_expired_days
        self.drds_instance_id = drds_instance_id
        self.retain_classic = retain_classic
        self.src_instance_network_type = src_instance_network_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.classic_expired_days is not None:
            result['ClassicExpiredDays'] = self.classic_expired_days
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.retain_classic is not None:
            result['RetainClassic'] = self.retain_classic
        if self.src_instance_network_type is not None:
            result['SrcInstanceNetworkType'] = self.src_instance_network_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('ClassicExpiredDays') is not None:
            self.classic_expired_days = m.get('ClassicExpiredDays')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RetainClassic') is not None:
            self.retain_classic = m.get('RetainClassic')
        if m.get('SrcInstanceNetworkType') is not None:
            self.src_instance_network_type = m.get('SrcInstanceNetworkType')
        return self


class UpdateInstanceNetworkResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
        success: bool = None,
    ):
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class UpdateInstanceNetworkResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateInstanceNetworkResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateInstanceNetworkResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdatePrivateRdsClassRequest(TeaModel):
    def __init__(
        self,
        auto_use_coupon: bool = None,
        dbinstance_id: str = None,
        drds_instance_id: str = None,
        pre_pay_duration: int = None,
        rds_class: str = None,
        storage: str = None,
    ):
        self.auto_use_coupon = auto_use_coupon
        self.dbinstance_id = dbinstance_id
        self.drds_instance_id = drds_instance_id
        self.pre_pay_duration = pre_pay_duration
        self.rds_class = rds_class
        self.storage = storage

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.auto_use_coupon is not None:
            result['AutoUseCoupon'] = self.auto_use_coupon
        if self.dbinstance_id is not None:
            result['DBInstanceId'] = self.dbinstance_id
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.pre_pay_duration is not None:
            result['PrePayDuration'] = self.pre_pay_duration
        if self.rds_class is not None:
            result['RdsClass'] = self.rds_class
        if self.storage is not None:
            result['Storage'] = self.storage
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('AutoUseCoupon') is not None:
            self.auto_use_coupon = m.get('AutoUseCoupon')
        if m.get('DBInstanceId') is not None:
            self.dbinstance_id = m.get('DBInstanceId')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('PrePayDuration') is not None:
            self.pre_pay_duration = m.get('PrePayDuration')
        if m.get('RdsClass') is not None:
            self.rds_class = m.get('RdsClass')
        if m.get('Storage') is not None:
            self.storage = m.get('Storage')
        return self


class UpdatePrivateRdsClassResponseBody(TeaModel):
    def __init__(
        self,
        data: str = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.data = data
        self.request_id = request_id
        self.success = success

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class UpdatePrivateRdsClassResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdatePrivateRdsClassResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdatePrivateRdsClassResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpdateResourceGroupAttributeRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
        new_resource_group_id: str = None,
        region_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id
        self.new_resource_group_id = new_resource_group_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.new_resource_group_id is not None:
            result['NewResourceGroupId'] = self.new_resource_group_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('NewResourceGroupId') is not None:
            self.new_resource_group_id = m.get('NewResourceGroupId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class UpdateResourceGroupAttributeResponseBody(TeaModel):
    def __init__(
        self,
        request_id: str = None,
    ):
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpdateResourceGroupAttributeResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpdateResourceGroupAttributeResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpdateResourceGroupAttributeResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpgradeHiStoreInstanceRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
        histore_instance_id: str = None,
        region_id: str = None,
    ):
        self.drds_instance_id = drds_instance_id
        self.histore_instance_id = histore_instance_id
        self.region_id = region_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.histore_instance_id is not None:
            result['HistoreInstanceId'] = self.histore_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('HistoreInstanceId') is not None:
            self.histore_instance_id = m.get('HistoreInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        return self


class UpgradeHiStoreInstanceResponseBody(TeaModel):
    def __init__(
        self,
        data: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpgradeHiStoreInstanceResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpgradeHiStoreInstanceResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpgradeHiStoreInstanceResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class UpgradeInstanceVersionRequest(TeaModel):
    def __init__(
        self,
        drds_instance_id: str = None,
        region_id: str = None,
        rpm: str = None,
    ):
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id
        self.rpm = rpm

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.rpm is not None:
            result['Rpm'] = self.rpm
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('Rpm') is not None:
            self.rpm = m.get('Rpm')
        return self


class UpgradeInstanceVersionResponseBody(TeaModel):
    def __init__(
        self,
        data: str = None,
        request_id: str = None,
    ):
        self.data = data
        self.request_id = request_id

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.data is not None:
            result['Data'] = self.data
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Data') is not None:
            self.data = m.get('Data')
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        return self


class UpgradeInstanceVersionResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: UpgradeInstanceVersionResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = UpgradeInstanceVersionResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


class ValidateShardTaskRequest(TeaModel):
    def __init__(
        self,
        db_name: str = None,
        drds_instance_id: str = None,
        region_id: str = None,
        source_table_name: str = None,
        target_table_name: str = None,
        task_type: str = None,
    ):
        self.db_name = db_name
        self.drds_instance_id = drds_instance_id
        self.region_id = region_id
        self.source_table_name = source_table_name
        self.target_table_name = target_table_name
        self.task_type = task_type

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.db_name is not None:
            result['DbName'] = self.db_name
        if self.drds_instance_id is not None:
            result['DrdsInstanceId'] = self.drds_instance_id
        if self.region_id is not None:
            result['RegionId'] = self.region_id
        if self.source_table_name is not None:
            result['SourceTableName'] = self.source_table_name
        if self.target_table_name is not None:
            result['TargetTableName'] = self.target_table_name
        if self.task_type is not None:
            result['TaskType'] = self.task_type
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('DbName') is not None:
            self.db_name = m.get('DbName')
        if m.get('DrdsInstanceId') is not None:
            self.drds_instance_id = m.get('DrdsInstanceId')
        if m.get('RegionId') is not None:
            self.region_id = m.get('RegionId')
        if m.get('SourceTableName') is not None:
            self.source_table_name = m.get('SourceTableName')
        if m.get('TargetTableName') is not None:
            self.target_table_name = m.get('TargetTableName')
        if m.get('TaskType') is not None:
            self.task_type = m.get('TaskType')
        return self


class ValidateShardTaskResponseBodyList(TeaModel):
    def __init__(
        self,
        item: str = None,
        result: int = None,
    ):
        self.item = item
        self.result = result

    def validate(self):
        pass

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.item is not None:
            result['Item'] = self.item
        if self.result is not None:
            result['Result'] = self.result
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('Item') is not None:
            self.item = m.get('Item')
        if m.get('Result') is not None:
            self.result = m.get('Result')
        return self


class ValidateShardTaskResponseBody(TeaModel):
    def __init__(
        self,
        list: List[ValidateShardTaskResponseBodyList] = None,
        request_id: str = None,
        success: bool = None,
    ):
        self.list = list
        self.request_id = request_id
        self.success = success

    def validate(self):
        if self.list:
            for k in self.list:
                if k:
                    k.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        result['List'] = []
        if self.list is not None:
            for k in self.list:
                result['List'].append(k.to_map() if k else None)
        if self.request_id is not None:
            result['RequestId'] = self.request_id
        if self.success is not None:
            result['Success'] = self.success
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        self.list = []
        if m.get('List') is not None:
            for k in m.get('List'):
                temp_model = ValidateShardTaskResponseBodyList()
                self.list.append(temp_model.from_map(k))
        if m.get('RequestId') is not None:
            self.request_id = m.get('RequestId')
        if m.get('Success') is not None:
            self.success = m.get('Success')
        return self


class ValidateShardTaskResponse(TeaModel):
    def __init__(
        self,
        headers: Dict[str, str] = None,
        body: ValidateShardTaskResponseBody = None,
    ):
        self.headers = headers
        self.body = body

    def validate(self):
        self.validate_required(self.headers, 'headers')
        self.validate_required(self.body, 'body')
        if self.body:
            self.body.validate()

    def to_map(self):
        _map = super().to_map()
        if _map is not None:
            return _map

        result = dict()
        if self.headers is not None:
            result['headers'] = self.headers
        if self.body is not None:
            result['body'] = self.body.to_map()
        return result

    def from_map(self, m: dict = None):
        m = m or dict()
        if m.get('headers') is not None:
            self.headers = m.get('headers')
        if m.get('body') is not None:
            temp_model = ValidateShardTaskResponseBody()
            self.body = temp_model.from_map(m['body'])
        return self


