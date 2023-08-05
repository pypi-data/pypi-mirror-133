# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from . import _utilities
import typing
# Export this package's modules as members:
from .acl import *
from .device_authorization import *
from .device_subnet_routes import *
from .dns_nameservers import *
from .dns_preferences import *
from .dns_search_paths import *
from .get_device import *
from .get_devices import *
from .provider import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import pulumi_tailscale.config as __config
    config = __config
else:
    config = _utilities.lazy_import('pulumi_tailscale.config')

_utilities.register(
    resource_modules="""
[
 {
  "pkg": "tailscale",
  "mod": "index/acl",
  "fqn": "pulumi_tailscale",
  "classes": {
   "tailscale:index/acl:Acl": "Acl"
  }
 },
 {
  "pkg": "tailscale",
  "mod": "index/deviceAuthorization",
  "fqn": "pulumi_tailscale",
  "classes": {
   "tailscale:index/deviceAuthorization:DeviceAuthorization": "DeviceAuthorization"
  }
 },
 {
  "pkg": "tailscale",
  "mod": "index/deviceSubnetRoutes",
  "fqn": "pulumi_tailscale",
  "classes": {
   "tailscale:index/deviceSubnetRoutes:DeviceSubnetRoutes": "DeviceSubnetRoutes"
  }
 },
 {
  "pkg": "tailscale",
  "mod": "index/dnsNameservers",
  "fqn": "pulumi_tailscale",
  "classes": {
   "tailscale:index/dnsNameservers:DnsNameservers": "DnsNameservers"
  }
 },
 {
  "pkg": "tailscale",
  "mod": "index/dnsPreferences",
  "fqn": "pulumi_tailscale",
  "classes": {
   "tailscale:index/dnsPreferences:DnsPreferences": "DnsPreferences"
  }
 },
 {
  "pkg": "tailscale",
  "mod": "index/dnsSearchPaths",
  "fqn": "pulumi_tailscale",
  "classes": {
   "tailscale:index/dnsSearchPaths:DnsSearchPaths": "DnsSearchPaths"
  }
 }
]
""",
    resource_packages="""
[
 {
  "pkg": "tailscale",
  "token": "pulumi:providers:tailscale",
  "fqn": "pulumi_tailscale",
  "class": "Provider"
 }
]
"""
)
