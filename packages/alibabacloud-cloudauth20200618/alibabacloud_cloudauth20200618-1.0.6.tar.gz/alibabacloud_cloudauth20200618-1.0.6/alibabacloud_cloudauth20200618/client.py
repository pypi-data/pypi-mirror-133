# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from Tea.core import TeaCore
from typing import Dict

from alibabacloud_tea_rpc.client import Client as RPCClient
from alibabacloud_tea_rpc import models as rpc_models
from alibabacloud_cloudauth20200618 import models as cloudauth_20200618_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_openplatform20191219.client import Client as OpenPlatformClient
from alibabacloud_openplatform20191219 import models as open_platform_models
from alibabacloud_oss_sdk import models as oss_models
from alibabacloud_tea_fileform import models as file_form_models
from alibabacloud_oss_util import models as ossutil_models
from alibabacloud_rpc_util.client import Client as RPCUtilClient
from alibabacloud_oss_sdk.client import Client as OSSClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient


class Client(RPCClient):
    def __init__(
        self, 
        config: rpc_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = 'central'
        self.check_config(config)
        self._endpoint = self.get_endpoint('cloudauth', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def contrast_smart_verify(
        self,
        request: cloudauth_20200618_models.ContrastSmartVerifyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.ContrastSmartVerifyResponse:
        UtilClient.validate_model(request)
        return TeaCore.from_map(
            cloudauth_20200618_models.ContrastSmartVerifyResponse(),
            self.do_request('ContrastSmartVerify', 'HTTPS', 'POST', '2020-06-18', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def contrast_smart_verify_async(
        self,
        request: cloudauth_20200618_models.ContrastSmartVerifyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.ContrastSmartVerifyResponse:
        UtilClient.validate_model(request)
        return TeaCore.from_map(
            cloudauth_20200618_models.ContrastSmartVerifyResponse(),
            await self.do_request_async('ContrastSmartVerify', 'HTTPS', 'POST', '2020-06-18', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def contrast_smart_verify_simply(
        self,
        request: cloudauth_20200618_models.ContrastSmartVerifyRequest,
    ) -> cloudauth_20200618_models.ContrastSmartVerifyResponse:
        runtime = util_models.RuntimeOptions()
        return self.contrast_smart_verify(request, runtime)

    async def contrast_smart_verify_simply_async(
        self,
        request: cloudauth_20200618_models.ContrastSmartVerifyRequest,
    ) -> cloudauth_20200618_models.ContrastSmartVerifyResponse:
        runtime = util_models.RuntimeOptions()
        return await self.contrast_smart_verify_async(request, runtime)

    def contrast_smart_verify_advance(
        self,
        request: cloudauth_20200618_models.ContrastSmartVerifyAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.ContrastSmartVerifyResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        open_platform_endpoint = self._open_platform_endpoint
        security_token = self._credential.get_security_token()
        credential_type = self._credential.get_type()
        if UtilClient.is_unset(open_platform_endpoint):
            open_platform_endpoint = 'openplatform.aliyuncs.com'
        if UtilClient.is_unset(credential_type):
            credential_type = 'access_key'
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            security_token=security_token,
            type=credential_type,
            endpoint=open_platform_endpoint,
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='Cloudauth',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        contrast_smart_verify_req = cloudauth_20200618_models.ContrastSmartVerifyRequest()
        RPCUtilClient.convert(request, contrast_smart_verify_req)
        if not UtilClient.is_unset(request.face_pic_file_object):
            auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
            oss_config.access_key_id = auth_response.access_key_id
            oss_config.endpoint = RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
            oss_client = OSSClient(oss_config)
            file_obj = file_form_models.FileField(
                filename=auth_response.object_key,
                content=request.face_pic_file_object,
                content_type=''
            )
            oss_header = oss_models.PostObjectRequestHeader(
                access_key_id=auth_response.access_key_id,
                policy=auth_response.encoded_policy,
                signature=auth_response.signature,
                key=auth_response.object_key,
                file=file_obj,
                success_action_status='201'
            )
            upload_request = oss_models.PostObjectRequest(
                bucket_name=auth_response.bucket,
                header=oss_header
            )
            oss_client.post_object(upload_request, oss_runtime)
            contrast_smart_verify_req.face_pic_file = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        contrast_smart_verify_resp = self.contrast_smart_verify(contrast_smart_verify_req, runtime)
        return contrast_smart_verify_resp

    async def contrast_smart_verify_advance_async(
        self,
        request: cloudauth_20200618_models.ContrastSmartVerifyAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.ContrastSmartVerifyResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        open_platform_endpoint = self._open_platform_endpoint
        security_token = await self._credential.get_security_token_async()
        credential_type = self._credential.get_type()
        if UtilClient.is_unset(open_platform_endpoint):
            open_platform_endpoint = 'openplatform.aliyuncs.com'
        if UtilClient.is_unset(credential_type):
            credential_type = 'access_key'
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            security_token=security_token,
            type=credential_type,
            endpoint=open_platform_endpoint,
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='Cloudauth',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        contrast_smart_verify_req = cloudauth_20200618_models.ContrastSmartVerifyRequest()
        RPCUtilClient.convert(request, contrast_smart_verify_req)
        if not UtilClient.is_unset(request.face_pic_file_object):
            auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
            oss_config.access_key_id = auth_response.access_key_id
            oss_config.endpoint = RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
            oss_client = OSSClient(oss_config)
            file_obj = file_form_models.FileField(
                filename=auth_response.object_key,
                content=request.face_pic_file_object,
                content_type=''
            )
            oss_header = oss_models.PostObjectRequestHeader(
                access_key_id=auth_response.access_key_id,
                policy=auth_response.encoded_policy,
                signature=auth_response.signature,
                key=auth_response.object_key,
                file=file_obj,
                success_action_status='201'
            )
            upload_request = oss_models.PostObjectRequest(
                bucket_name=auth_response.bucket,
                header=oss_header
            )
            await oss_client.post_object_async(upload_request, oss_runtime)
            contrast_smart_verify_req.face_pic_file = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        contrast_smart_verify_resp = await self.contrast_smart_verify_async(contrast_smart_verify_req, runtime)
        return contrast_smart_verify_resp

    def describe_smart_verify(
        self,
        request: cloudauth_20200618_models.DescribeSmartVerifyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.DescribeSmartVerifyResponse:
        UtilClient.validate_model(request)
        return TeaCore.from_map(
            cloudauth_20200618_models.DescribeSmartVerifyResponse(),
            self.do_request('DescribeSmartVerify', 'HTTPS', 'POST', '2020-06-18', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def describe_smart_verify_async(
        self,
        request: cloudauth_20200618_models.DescribeSmartVerifyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.DescribeSmartVerifyResponse:
        UtilClient.validate_model(request)
        return TeaCore.from_map(
            cloudauth_20200618_models.DescribeSmartVerifyResponse(),
            await self.do_request_async('DescribeSmartVerify', 'HTTPS', 'POST', '2020-06-18', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def describe_smart_verify_simply(
        self,
        request: cloudauth_20200618_models.DescribeSmartVerifyRequest,
    ) -> cloudauth_20200618_models.DescribeSmartVerifyResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_smart_verify(request, runtime)

    async def describe_smart_verify_simply_async(
        self,
        request: cloudauth_20200618_models.DescribeSmartVerifyRequest,
    ) -> cloudauth_20200618_models.DescribeSmartVerifyResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_smart_verify_async(request, runtime)

    def describe_sms_detail(
        self,
        request: cloudauth_20200618_models.DescribeSmsDetailRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.DescribeSmsDetailResponse:
        UtilClient.validate_model(request)
        return TeaCore.from_map(
            cloudauth_20200618_models.DescribeSmsDetailResponse(),
            self.do_request('DescribeSmsDetail', 'HTTPS', 'POST', '2020-06-18', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def describe_sms_detail_async(
        self,
        request: cloudauth_20200618_models.DescribeSmsDetailRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.DescribeSmsDetailResponse:
        UtilClient.validate_model(request)
        return TeaCore.from_map(
            cloudauth_20200618_models.DescribeSmsDetailResponse(),
            await self.do_request_async('DescribeSmsDetail', 'HTTPS', 'POST', '2020-06-18', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def describe_sms_detail_simply(
        self,
        request: cloudauth_20200618_models.DescribeSmsDetailRequest,
    ) -> cloudauth_20200618_models.DescribeSmsDetailResponse:
        runtime = util_models.RuntimeOptions()
        return self.describe_sms_detail(request, runtime)

    async def describe_sms_detail_simply_async(
        self,
        request: cloudauth_20200618_models.DescribeSmsDetailRequest,
    ) -> cloudauth_20200618_models.DescribeSmsDetailResponse:
        runtime = util_models.RuntimeOptions()
        return await self.describe_sms_detail_async(request, runtime)

    def element_smart_verify(
        self,
        request: cloudauth_20200618_models.ElementSmartVerifyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.ElementSmartVerifyResponse:
        UtilClient.validate_model(request)
        return TeaCore.from_map(
            cloudauth_20200618_models.ElementSmartVerifyResponse(),
            self.do_request('ElementSmartVerify', 'HTTPS', 'POST', '2020-06-18', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def element_smart_verify_async(
        self,
        request: cloudauth_20200618_models.ElementSmartVerifyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.ElementSmartVerifyResponse:
        UtilClient.validate_model(request)
        return TeaCore.from_map(
            cloudauth_20200618_models.ElementSmartVerifyResponse(),
            await self.do_request_async('ElementSmartVerify', 'HTTPS', 'POST', '2020-06-18', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def element_smart_verify_simply(
        self,
        request: cloudauth_20200618_models.ElementSmartVerifyRequest,
    ) -> cloudauth_20200618_models.ElementSmartVerifyResponse:
        runtime = util_models.RuntimeOptions()
        return self.element_smart_verify(request, runtime)

    async def element_smart_verify_simply_async(
        self,
        request: cloudauth_20200618_models.ElementSmartVerifyRequest,
    ) -> cloudauth_20200618_models.ElementSmartVerifyResponse:
        runtime = util_models.RuntimeOptions()
        return await self.element_smart_verify_async(request, runtime)

    def element_smart_verify_advance(
        self,
        request: cloudauth_20200618_models.ElementSmartVerifyAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.ElementSmartVerifyResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        open_platform_endpoint = self._open_platform_endpoint
        security_token = self._credential.get_security_token()
        credential_type = self._credential.get_type()
        if UtilClient.is_unset(open_platform_endpoint):
            open_platform_endpoint = 'openplatform.aliyuncs.com'
        if UtilClient.is_unset(credential_type):
            credential_type = 'access_key'
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            security_token=security_token,
            type=credential_type,
            endpoint=open_platform_endpoint,
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='Cloudauth',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        element_smart_verify_req = cloudauth_20200618_models.ElementSmartVerifyRequest()
        RPCUtilClient.convert(request, element_smart_verify_req)
        if not UtilClient.is_unset(request.cert_file_object):
            auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
            oss_config.access_key_id = auth_response.access_key_id
            oss_config.endpoint = RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
            oss_client = OSSClient(oss_config)
            file_obj = file_form_models.FileField(
                filename=auth_response.object_key,
                content=request.cert_file_object,
                content_type=''
            )
            oss_header = oss_models.PostObjectRequestHeader(
                access_key_id=auth_response.access_key_id,
                policy=auth_response.encoded_policy,
                signature=auth_response.signature,
                key=auth_response.object_key,
                file=file_obj,
                success_action_status='201'
            )
            upload_request = oss_models.PostObjectRequest(
                bucket_name=auth_response.bucket,
                header=oss_header
            )
            oss_client.post_object(upload_request, oss_runtime)
            element_smart_verify_req.cert_file = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        element_smart_verify_resp = self.element_smart_verify(element_smart_verify_req, runtime)
        return element_smart_verify_resp

    async def element_smart_verify_advance_async(
        self,
        request: cloudauth_20200618_models.ElementSmartVerifyAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.ElementSmartVerifyResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        open_platform_endpoint = self._open_platform_endpoint
        security_token = await self._credential.get_security_token_async()
        credential_type = self._credential.get_type()
        if UtilClient.is_unset(open_platform_endpoint):
            open_platform_endpoint = 'openplatform.aliyuncs.com'
        if UtilClient.is_unset(credential_type):
            credential_type = 'access_key'
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            security_token=security_token,
            type=credential_type,
            endpoint=open_platform_endpoint,
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='Cloudauth',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        element_smart_verify_req = cloudauth_20200618_models.ElementSmartVerifyRequest()
        RPCUtilClient.convert(request, element_smart_verify_req)
        if not UtilClient.is_unset(request.cert_file_object):
            auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
            oss_config.access_key_id = auth_response.access_key_id
            oss_config.endpoint = RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
            oss_client = OSSClient(oss_config)
            file_obj = file_form_models.FileField(
                filename=auth_response.object_key,
                content=request.cert_file_object,
                content_type=''
            )
            oss_header = oss_models.PostObjectRequestHeader(
                access_key_id=auth_response.access_key_id,
                policy=auth_response.encoded_policy,
                signature=auth_response.signature,
                key=auth_response.object_key,
                file=file_obj,
                success_action_status='201'
            )
            upload_request = oss_models.PostObjectRequest(
                bucket_name=auth_response.bucket,
                header=oss_header
            )
            await oss_client.post_object_async(upload_request, oss_runtime)
            element_smart_verify_req.cert_file = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        element_smart_verify_resp = await self.element_smart_verify_async(element_smart_verify_req, runtime)
        return element_smart_verify_resp

    def init_smart_verify(
        self,
        request: cloudauth_20200618_models.InitSmartVerifyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.InitSmartVerifyResponse:
        UtilClient.validate_model(request)
        return TeaCore.from_map(
            cloudauth_20200618_models.InitSmartVerifyResponse(),
            self.do_request('InitSmartVerify', 'HTTPS', 'POST', '2020-06-18', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def init_smart_verify_async(
        self,
        request: cloudauth_20200618_models.InitSmartVerifyRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.InitSmartVerifyResponse:
        UtilClient.validate_model(request)
        return TeaCore.from_map(
            cloudauth_20200618_models.InitSmartVerifyResponse(),
            await self.do_request_async('InitSmartVerify', 'HTTPS', 'POST', '2020-06-18', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def init_smart_verify_simply(
        self,
        request: cloudauth_20200618_models.InitSmartVerifyRequest,
    ) -> cloudauth_20200618_models.InitSmartVerifyResponse:
        runtime = util_models.RuntimeOptions()
        return self.init_smart_verify(request, runtime)

    async def init_smart_verify_simply_async(
        self,
        request: cloudauth_20200618_models.InitSmartVerifyRequest,
    ) -> cloudauth_20200618_models.InitSmartVerifyResponse:
        runtime = util_models.RuntimeOptions()
        return await self.init_smart_verify_async(request, runtime)

    def send_sms(
        self,
        request: cloudauth_20200618_models.SendSmsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.SendSmsResponse:
        UtilClient.validate_model(request)
        return TeaCore.from_map(
            cloudauth_20200618_models.SendSmsResponse(),
            self.do_request('SendSms', 'HTTPS', 'POST', '2020-06-18', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def send_sms_async(
        self,
        request: cloudauth_20200618_models.SendSmsRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.SendSmsResponse:
        UtilClient.validate_model(request)
        return TeaCore.from_map(
            cloudauth_20200618_models.SendSmsResponse(),
            await self.do_request_async('SendSms', 'HTTPS', 'POST', '2020-06-18', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def send_sms_simply(
        self,
        request: cloudauth_20200618_models.SendSmsRequest,
    ) -> cloudauth_20200618_models.SendSmsResponse:
        runtime = util_models.RuntimeOptions()
        return self.send_sms(request, runtime)

    async def send_sms_simply_async(
        self,
        request: cloudauth_20200618_models.SendSmsRequest,
    ) -> cloudauth_20200618_models.SendSmsResponse:
        runtime = util_models.RuntimeOptions()
        return await self.send_sms_async(request, runtime)

    def verify_bank_element(
        self,
        request: cloudauth_20200618_models.VerifyBankElementRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.VerifyBankElementResponse:
        UtilClient.validate_model(request)
        return TeaCore.from_map(
            cloudauth_20200618_models.VerifyBankElementResponse(),
            self.do_request('VerifyBankElement', 'HTTPS', 'POST', '2020-06-18', 'AK', None, TeaCore.to_map(request), runtime)
        )

    async def verify_bank_element_async(
        self,
        request: cloudauth_20200618_models.VerifyBankElementRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.VerifyBankElementResponse:
        UtilClient.validate_model(request)
        return TeaCore.from_map(
            cloudauth_20200618_models.VerifyBankElementResponse(),
            await self.do_request_async('VerifyBankElement', 'HTTPS', 'POST', '2020-06-18', 'AK', None, TeaCore.to_map(request), runtime)
        )

    def verify_bank_element_simply(
        self,
        request: cloudauth_20200618_models.VerifyBankElementRequest,
    ) -> cloudauth_20200618_models.VerifyBankElementResponse:
        runtime = util_models.RuntimeOptions()
        return self.verify_bank_element(request, runtime)

    async def verify_bank_element_simply_async(
        self,
        request: cloudauth_20200618_models.VerifyBankElementRequest,
    ) -> cloudauth_20200618_models.VerifyBankElementResponse:
        runtime = util_models.RuntimeOptions()
        return await self.verify_bank_element_async(request, runtime)

    def verify_bank_element_advance(
        self,
        request: cloudauth_20200618_models.VerifyBankElementAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.VerifyBankElementResponse:
        # Step 0: init client
        access_key_id = self._credential.get_access_key_id()
        access_key_secret = self._credential.get_access_key_secret()
        open_platform_endpoint = self._open_platform_endpoint
        security_token = self._credential.get_security_token()
        credential_type = self._credential.get_type()
        if UtilClient.is_unset(open_platform_endpoint):
            open_platform_endpoint = 'openplatform.aliyuncs.com'
        if UtilClient.is_unset(credential_type):
            credential_type = 'access_key'
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            security_token=security_token,
            type=credential_type,
            endpoint=open_platform_endpoint,
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='Cloudauth',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        verify_bank_element_req = cloudauth_20200618_models.VerifyBankElementRequest()
        RPCUtilClient.convert(request, verify_bank_element_req)
        if not UtilClient.is_unset(request.bank_card_file_object):
            auth_response = auth_client.authorize_file_upload_with_options(auth_request, runtime)
            oss_config.access_key_id = auth_response.access_key_id
            oss_config.endpoint = RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
            oss_client = OSSClient(oss_config)
            file_obj = file_form_models.FileField(
                filename=auth_response.object_key,
                content=request.bank_card_file_object,
                content_type=''
            )
            oss_header = oss_models.PostObjectRequestHeader(
                access_key_id=auth_response.access_key_id,
                policy=auth_response.encoded_policy,
                signature=auth_response.signature,
                key=auth_response.object_key,
                file=file_obj,
                success_action_status='201'
            )
            upload_request = oss_models.PostObjectRequest(
                bucket_name=auth_response.bucket,
                header=oss_header
            )
            oss_client.post_object(upload_request, oss_runtime)
            verify_bank_element_req.bank_card_file = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        verify_bank_element_resp = self.verify_bank_element(verify_bank_element_req, runtime)
        return verify_bank_element_resp

    async def verify_bank_element_advance_async(
        self,
        request: cloudauth_20200618_models.VerifyBankElementAdvanceRequest,
        runtime: util_models.RuntimeOptions,
    ) -> cloudauth_20200618_models.VerifyBankElementResponse:
        # Step 0: init client
        access_key_id = await self._credential.get_access_key_id_async()
        access_key_secret = await self._credential.get_access_key_secret_async()
        open_platform_endpoint = self._open_platform_endpoint
        security_token = await self._credential.get_security_token_async()
        credential_type = self._credential.get_type()
        if UtilClient.is_unset(open_platform_endpoint):
            open_platform_endpoint = 'openplatform.aliyuncs.com'
        if UtilClient.is_unset(credential_type):
            credential_type = 'access_key'
        auth_config = rpc_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            security_token=security_token,
            type=credential_type,
            endpoint=open_platform_endpoint,
            protocol=self._protocol,
            region_id=self._region_id
        )
        auth_client = OpenPlatformClient(auth_config)
        auth_request = open_platform_models.AuthorizeFileUploadRequest(
            product='Cloudauth',
            region_id=self._region_id
        )
        auth_response = open_platform_models.AuthorizeFileUploadResponse()
        oss_config = oss_models.Config(
            access_key_secret=access_key_secret,
            type='access_key',
            protocol=self._protocol,
            region_id=self._region_id
        )
        oss_client = None
        file_obj = file_form_models.FileField()
        oss_header = oss_models.PostObjectRequestHeader()
        upload_request = oss_models.PostObjectRequest()
        oss_runtime = ossutil_models.RuntimeOptions()
        RPCUtilClient.convert(runtime, oss_runtime)
        verify_bank_element_req = cloudauth_20200618_models.VerifyBankElementRequest()
        RPCUtilClient.convert(request, verify_bank_element_req)
        if not UtilClient.is_unset(request.bank_card_file_object):
            auth_response = await auth_client.authorize_file_upload_with_options_async(auth_request, runtime)
            oss_config.access_key_id = auth_response.access_key_id
            oss_config.endpoint = RPCUtilClient.get_endpoint(auth_response.endpoint, auth_response.use_accelerate, self._endpoint_type)
            oss_client = OSSClient(oss_config)
            file_obj = file_form_models.FileField(
                filename=auth_response.object_key,
                content=request.bank_card_file_object,
                content_type=''
            )
            oss_header = oss_models.PostObjectRequestHeader(
                access_key_id=auth_response.access_key_id,
                policy=auth_response.encoded_policy,
                signature=auth_response.signature,
                key=auth_response.object_key,
                file=file_obj,
                success_action_status='201'
            )
            upload_request = oss_models.PostObjectRequest(
                bucket_name=auth_response.bucket,
                header=oss_header
            )
            await oss_client.post_object_async(upload_request, oss_runtime)
            verify_bank_element_req.bank_card_file = f'http://{auth_response.bucket}.{auth_response.endpoint}/{auth_response.object_key}'
        verify_bank_element_resp = await self.verify_bank_element_async(verify_bank_element_req, runtime)
        return verify_bank_element_resp

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)
