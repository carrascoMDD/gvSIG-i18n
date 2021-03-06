<dtml-var "generator.generateModuleInfoHeader(package)">
# There are three ways to inject custom code here:
#
#   - To set global configuration variables, create a file AppConfig.py.
#       This will be imported in config.py, which in turn is imported in
#       each generated class and in this file.
#   - To perform custom initialisation after types have been registered,
#       use the protected code section at the bottom of initialize().
#   - To register a customisation policy, create a file CustomizationPolicy.py
#       with a method register(context) to register the policy.

import logging
logger = logging.getLogger('<dtml-var "product_name">')
logger.info('Installing Product')

try:
    import CustomizationPolicy
except ImportError:
    CustomizationPolicy = None

import os, os.path
from Globals import package_home
from Products.CMFCore import utils as cmfutils

try: # New CMF
    from Products.CMFCore import permissions as CMFCorePermissions 
except: # Old CMF
    from Products.CMFCore import CMFCorePermissions

from Products.CMFCore import DirectoryView
from Products.CMFPlone.utils import ToolInit
from Products.Archetypes.atapi import *
from Products.Archetypes import listTypes
from Products.Archetypes.utils import capitalize
from config import *

DirectoryView.registerDirectory('skins', product_globals)
DirectoryView.registerDirectory('skins/<dtml-var "product_name">',
                                    product_globals)
<dtml-if "additional_permissions">

# Register additional (custom) permissions used by this product
<dtml-in "additional_permissions">
<dtml-let permdef="_['sequence-item']">
CMFCorePermissions.setDefaultRoles('<dtml-var "product_name">: <dtml-var "permdef[0]">',[<dtml-var "','.join(permdef[1])">])
</dtml-let>
</dtml-in>
</dtml-if>

<dtml-var "protected_init_section_head">

def initialize(context):
<dtml-var "protected_init_section_top">
    # imports packages and types for registration
<dtml-in "package_imports">
<dtml-if sequence-item>
    import <dtml-var sequence-item>
</dtml-if>
</dtml-in>

<dtml-in "class_imports">
    import <dtml-var sequence-item>
</dtml-in>

<dtml-if "has_tools">
    # Initialize portal tools
    tools = [<dtml-var "', '.join (tool_names)">]
    ToolInit( PROJECTNAME +' Tools',
                tools = tools,
<dtml-if "generator.getOption('cmf_target_version', package, '1.5') == '1.4'">
                product_name = PROJECTNAME,
</dtml-if>
<dtml-if "generator.getOption('cmf_target_version', package, '1.5') >= '1.4'">
                icon='tool.gif'
</dtml-if>
                ).initialize( context )

</dtml-if>
    # Initialize portal content
<dtml-if "creation_permissions">
    all_content_types, all_constructors, all_ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = all_content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = all_constructors,
        fti                = all_ftis,
        ).initialize(context)

    # Give it some extra permissions to control them on a per class limit
    for i in range(0,len(all_content_types)):
        klassname=all_content_types[i].__name__
        if not klassname in ADD_CONTENT_PERMISSIONS:
            continue

        context.registerClass(meta_type   = all_ftis[i]['meta_type'],
                              constructors= (all_constructors[i],),
                              permission  = ADD_CONTENT_PERMISSIONS[klassname])
<dtml-else>
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)
</dtml-if>

    # Apply customization-policy, if theres any
    if CustomizationPolicy and hasattr(CustomizationPolicy, 'register'):
        CustomizationPolicy.register(context)
        print 'Customization policy for <dtml-var "product_name"> installed'

<dtml-var "protected_init_section_bottom">
