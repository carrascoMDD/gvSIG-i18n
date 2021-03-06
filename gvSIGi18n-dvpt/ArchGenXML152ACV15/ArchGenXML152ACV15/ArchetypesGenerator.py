# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------
# Name:        ArchetypesGenerator.py
# Purpose:     main class generating archetypes code out of an UML-model
#
# Author:      Philipp Auersperg
#
# Created:     2003/16/04
# Copyright:   (c) 2003-2006 BlueDynamics
# Licence:     GPL
#-----------------------------------------------------------------------------



# ###################################################################################
# ACV OJO FIX 2008/05/01
#     relations.xml fails to generate multiple allowedSourceType elements and multiple allowedTargetType elements
#     for specializations of related types
# SEE BELOW in ruleset.XMLImportDOM.importDOM() 
#




import sys
import time
import types
import os.path
import logging
from types import StringTypes

import utils
from odict import odict
from sets import Set
from codesnippets import *

from xml.dom import minidom
from zipfile import ZipFile
from cStringIO import StringIO

# AGX-specific imports
import PyParser
import XMIParser
from UMLProfile import UMLProfile

from BaseGenerator import BaseGenerator
from WorkflowGenerator import WorkflowGenerator

from documenttemplate.documenttemplate import HTML

_marker = []
log = logging.getLogger('generator')

try:
    from i18ndude import catalog as msgcatalog
except ImportError:
    has_i18ndude = False
else:
    has_i18ndude = True

try:
    'abca'.strip('a')
except:
    has_enhanced_strip_support = False
else:
    has_enhanced_strip_support = True

#
# Global variables etc.
#

Elements = []
AlreadyGenerated = []
Force = 0


# ACV OJO ADDITION 20080903

cIndentLen = 4
cIndent = ' ' * cIndentLen    
cConfigDictKeysPreferedOrder = [ 'portal_types', 'title', 'description', 'name', 'kind', 'type', 'optional', 'hide_label', 'reuse_config', 'config_name', 'aggregation_name', 'relation_name',  'columns', 'dependency',  'contains_collections', 'generic_references', 'indirection',  'mode', 'if_not_included', 'tabular_tree', 'extension', 'exclude_from_views', 'divider', 'attrs', 'traversals',  'related_types', ]




class DummyModel:

    def __init__(self, name=''):
        self.name = name

    def getName(self):
        return self.name

    getCleanName = getName
    getFilePath = getName
    getModuleFilePath = getName
    getProductModuleName = getName
    getProductName = getName

    def hasStereoType(self, s, umlprofile=None):
        return True

    def getClasses(self, *a, **kw):
        return []

    getInterfaces = getClasses
    getPackages = getClasses
    getStateMachines = getClasses
    getAssociations = getClasses

    def isRoot(self):
        return 1

    def getAnnotation(self, *a, **kw):
        return None

    def getDocumentation(self, **kw):
        return None

    def hasTaggedValue(self, *a, **kw):
        return None

    def getParent(self, *a, **kw):
        return None


class ArchetypesGenerator(BaseGenerator):

    generator_generator = 'archetypes'
    default_class_type = 'content_class'
    default_interface_type = 'z2'

    uml_profile = UMLProfile(BaseGenerator.uml_profile)

    uml_profile.addStereoType(
        'portal_tool', ['XMIClass'],
        description='Turns the class into a portal tool.')

    uml_profile.addStereoType(
        'stub', ['XMIClass', 'XMIModel', 'XMIPackage'],
        description='Prevents a class/package/model from being generated.')

    uml_profile.addStereoType(
        'odStub', ['XMIClass', 'XMIModel', 'XMIPackage'],
        description='Prevents a class/package/model from being generated. '
        "Same as '<<stub>>'.")

    uml_profile.addStereoType(
        'content_class', ['XMIClass'],
        dispatching=1,
        generator='generateArchetypesClass',
        description='TODO')

    uml_profile.addStereoType(
        'z2', ['XMIInterface'],
        dispatching=1,
        generator='generateZope2Interface',
        description='Generates a Zope 2 Interface inheriting from Zope.Interface.Base.')

    uml_profile.addStereoType(
        'tests', ['XMIPackage'],
        description='Treats a package as test package. Inside such a test '
        "package, you need at a '<<plone_testcase>>' and a "
        "'<<setup_testcase>>'.")

    uml_profile.addStereoType(
        'plone_testcase', ['XMIClass'],
        dispatching=1,
        template='tests/PloneTestcase.py',
        generator='generateBaseTestcaseClass',
        description='Turns a class into the (needed) base class for all '
        "other '<<testcase>>' and '<<doc_testcase>>' classes "
        "inside a '<<test>>' package.")

    uml_profile.addStereoType(
        'testcase', ['XMIClass'],
        dispatching=1,
        template='tests/GenericTestcase.py',
        generator='generateTestcaseClass',
        description='Turns a class into a testcase. It must subclass a '
        "'<<plone_testcase>>'. Adding an interface arrow to "
        'another class automatically adds that class\'s '
        'methods to the testfile for testing.')

    uml_profile.addStereoType(
        'doc_testcase', ['XMIClass'],
        dispatching=1,
        template='tests/DocTestcase.py',
        generator='generateDocTestcaseClass',
        description='Turns a class into a doctest class. It must subclass '
        "a '<<plone_testcase>>'.")

    uml_profile.addStereoType(
        'setup_testcase', ['XMIClass'],
        dispatching=1,
        generator='generateTestcaseClass',
        template='tests/SetupTestcase.py',
        description='Turns a class into a testcase for the setup, with '
        'pre-defined common checks.')

    uml_profile.addStereoType(
        'interface_testcase', ['XMIClass'],
        dispatching=1,
        generator='generateTestcaseClass',
        template='tests/InterfaceTestcase.py',
        description='Turns a class into a testcase for the interfaces.')

    # This looks like a tagged value...
    #uml_profile.addStereoType(
    #    'relation_implementation',
    #    ['XMIClass', 'XMIAssociation', 'XMIPackage'],
    #    default='basic',
    #    description='specifies how relations should be implemented')

    uml_profile.addStereoType(
        'field', ['XMIClass'],
        dispatching=1,
        generator='generateFieldClass',
        template='field.py',
        description='TODO')

    uml_profile.addStereoType(
        'widget', ['XMIClass'],
        dispatching=1,
        generator='generateWidgetClass',
        template='widget.py',
        description='TODO')

    uml_profile.addStereoType(
        'value_class', ['XMIDependency'],
        description='Declares a class to be used as value class for a '
        "certain field class (see '<<field>>' stereotype).")

    uml_profile.addStereoType(
        'CMFMember', ['XMIClass'],
        description='The class will be treated as a CMFMember member '
        'type. It will derive from CMFMember\'s Member '
        'class and be installed as a member data type. '
        'Note that you need to install the separate CMFMember product. '
        "Identical to '<<member>>'.")

    uml_profile.addStereoType(
        'remember', ['XMIClass'],
        description='The class will be treated as a remember member '
        'type. It will derive from remember\'s Member '
        'class and be installed as a member data type. '
        'Note that you need to install the separate remember product. ')

    uml_profile.addStereoType(
        'member', ['XMIClass'],
        description='The class will be treated as a CMFMember member '
        'type. It will derive from CMFMember\'s Member '
        'class and be installed as a member data type. '
        'Note that you need to install the separate CMFMember product. '
        "Identical to '<<CMFMember>>'.")

    uml_profile.addStereoType(
        'action', ['XMIMethod'],
        description='Generate a CMF action which will be available on the '
        'object. The tagged values "action" (defaults to method '
        'name), "id" (defaults to method name), "category" '
        '(defaults to "object"), "label" (defaults to method '
        'name), "condition" (defaults to empty), and "permission" '
        '(defaults to empty) set on the method and mapped to '
        'the equivalent fields of any CMF action can be used to '
        'control the behaviour of the action.')

    uml_profile.addStereoType(
        'archetype', ['XMIClass'],
        description='Explicitly specify that a class represents an Archetypes '
        'type. This may be necessary if you are including a class '
        'as a base class for another class and ArchGenXML is unable '
        'to determine whether the parent class is an Archetype '
        'or not. Without knowing that the parent class in an '
        'Archetype, ArchGenXML cannot ensure that the parent\'s '
        'schema is available in the derived class.')

    uml_profile.addStereoType(
        'btree', ['XMIClass'],
        description="Like '<<folder>>', it generates a folderish object. "
        'But it uses a BTree folder for support of large amounts '
        "of content. The same as '<<large>>'.")

    uml_profile.addStereoType(
        'large', ['XMIClass'],
        description="Like '<<folder>>', it generates a folderish object. "
        'But it uses a BTree folder for support of large amounts '
        "of content. The same as '<<large>>'.")

    uml_profile.addStereoType(
        'folder', ['XMIClass'],
        description='Turns the class into a folderish object. When a UML '
        'class contains or aggregates other classes, it is '
        'automatically turned into a folder; this stereotype '
        'can be used to turn normal classes into folders, too.')

    uml_profile.addStereoType(
        'ordered', ['XMIClass'],
        description='For folderish types, include folder ordering support. '
        'This will allow the user to re-order items in the folder '
        'manually.')

    uml_profile.addStereoType(
        'form', ['XMIMethod'],
        description="Generate an action like with the '<<action>>' stereotype, "
        'but also copy an empty controller page template to the '
        'skins directory with the same name as the method and set '
        'this up as the target of the action. If the template '
        'already exists, it is not overwritten.')

    uml_profile.addStereoType(
        'hidden', ['XMIClass'],
        description='Generate the class, but turn off "global_allow", thereby '
        'making it unavailable in the portal by default. Note that '
        'if you use composition to specify that a type should be '
        'addable only inside another (folderish) type, then '
        '"global_allow" will be turned off automatically, and the '
        'type be made addable only inside the designated parent. '
        '(You can use aggregation instead of composition to make a '
        'type both globally addable and explicitly addable inside '
        'another folderish type).')

    uml_profile.addStereoType(
        'mixin', ['XMIClass'],
        description='Don\'t inherit automatically from "BaseContent" and so. '
        'This makes the class suitable as a mixin class. See also '
        "'<<archetype>>'.")

    uml_profile.addStereoType(
        'portlet', ['XMIMethod'],
        description='Create a simple portlet page template with the same '
        'name as the method. You can override the name by setting '
        'the "view" tagged value on the method. If you add a '
        'tagged value "autoinstall" and set it to "left" or '
        '"right", the portlet will be automatically installed '
        'with your product in either the left or the right slot. '
        'If the page template already exists, it will not be '
        'overwritten.')

    uml_profile.addStereoType(
        'portlet_view', ['XMIMethod'],
        description='Create a simple portlet page template with the same '
        'name as the method. You can override the name by setting '
        'the "view" tagged value on the method. If you add a '
        'tagged value "autoinstall" and set it to "left" or '
        '"right", the portlet will be automatically installed '
        'with your product in either the left or the right slot. '
        'If the page template already exists, it will not be '
        "overwritten. Same as '<<portlet>>'.")

    uml_profile.addStereoType(
        'tool', ['XMIClass'],
        description='Turns the class into a portal tool. Similar to '
        "'<<portal_tool>>'.")

    uml_profile.addStereoType(
        'variable_schema', ['XMIClass'],
        description='Include variable schema support in a content type by '
        'deriving from the VariableSchema mixin class.')

    uml_profile.addStereoType(
        'view', ['XMIMethod'],
        description="Generate an action like with the '<<action>>' stereotype, "
        'but also copy an empty page template to the skins '
        'directory with the same name as the method and set this '
        'up as the target of the action. If the template exists, '
        'it is not overwritten.')

    uml_profile.addStereoType(
        'vocabulary', ['XMIClass'],
        description='TODO')

    uml_profile.addStereoType(
        'vocabulary_term', ['XMIClass'],
        description='TODO')

    # The defaults here are already handled by OptionParser
    # (And we want only a single authorative source of information :-)

    # force = 1
    # unknownTypesAsString = 0
    # generateActions = 1
    # generateDefaultActions = 0
    # prefix = ''
    # parse_packages = [] # Packages to scan for classes
    # generate_packages = [] # Packages to be generated
    # noclass = 0 # If set no module is reverse engineered,
    #             # just an empty project + skin is created
    # ape_support = 0 # Generate APE config and serializers/gateways?
    # method_preservation = 1 # Should the method bodies be preserved?
    # i18n_content_support = 0

    build_msgcatalog = 1
    striphtml = 0

    reservedAtts = ['id']
    portal_tools = ['portal_tool', 'tool']
    variable_schema = 'variable_schema'

    stub_stereotypes = ['odStub','stub']
    archetype_stereotype = ['archetype']
    vocabulary_item_stereotype = ['vocabulary_term']
    vocabulary_container_stereotype = ['vocabulary']
    cmfmember_stereotype = ['CMFMember', 'member']
    remember_stereotype = ['remember']
    python_stereotype = ['python', 'python_class']
    folder_stereotype = ['folder', 'ordered', 'large', 'btree']

    i18n_at = ['i18n-archetypes', 'i18n', 'i18n-at']
    generate_datatypes = ['field', 'compound_field']

    left_slots = []
    right_slots = []

    # Should be 'Products.' be prepended to all absolute paths?
    force_plugin_root = 1

    customization_policy = 0
    backreferences_support = 0

    # Contains the parsed sources by class names (for preserving method codes)
    parsed_class_sources = {}

    # Contains the parsed sources (for preserving method codes)
    parsed_sources = []

    # TaggedValues that are not strings, e.g. widget or vocabulary
    nonstring_tgvs = ['widget', 'vocabulary', 'required', 'precision',
                      'storage', 'enforceVocabulary', 'multiValued',
                      'visible', 'validators', 'validation_expression',
                      'sizes', 'original_size', 'max_size', 'searchable',
                      'show_hm', 'move:pos', 'move:top', 'move:bottom',
                      'primary', 'array:widget','array:size']

    msgcatstack = []

    # ATVM: collects all used vocabularies in the format:
    # { productsname: (name, meta_type) }
    # If metatype is None, it defaults to SimpleVocabulary.
    vocabularymap = {}

    # If a reference has the same name as another _and_
    # its source object is the same, we want only one ReferenceWidget
    # _unless_ we have a tagged value 'single' on the reference
    reference_groups = []

    # for each class an own permission can be defined, how should be able to add
    # it. It default to "Add Portal Content" and
    creation_permissions = []

    # the stack is needed to remind permissions while a subproduct is generated
    creation_permission_stack = []

    def __init__(self, xschemaFileName, **kwargs):

        log.debug("Initializing ArchetypesGenerator. "
                  "We're being passed a file '%s' and keyword "
                  "arguments %r.", xschemaFileName, kwargs)
        self.xschemaFileName = xschemaFileName
        self.__dict__.update(kwargs)
        log.debug("After copying over the keyword arguments (read: "
                  "OptionParser's options), outfilename is '%s'.",
                  self.outfilename)
        if self.outfilename:
            # Remove trailing delimiters on purpose
            if self.outfilename[-1] in ('/','\\'):
                self.outfilename = self.outfilename[:-1]
            log.debug("Stripped off the eventual trailing slashes: '%s'.",
                      self.outfilename)

            # Split off the parent directory part so that
            # we can call ArchgenXML.py -o /tmp/prod prod.xmi
            path = os.path.split(self.outfilename)
            self.targetRoot = path[0]
            log.debug("Targetroot is set to everything except the last "
                      "directory in the outfilename: %s.", self.targetRoot)
        else:
            log.debug("Outfilename hasn't been set. Setting "
                      "targetroot to the current directory.")
            self.targetRoot = '.'
        log.debug("Initialization finished.")

    def makeFile(self, fn, force=1, binary=0):
        log.debug("Calling makeFile to create '%s'.", fn)
        ffn = os.path.join(self.targetRoot, fn)
        log.debug("Together with the targetroot that means '%s'.", ffn)
        return utils.makeFile(ffn, force=force, binary=binary)

    def readFile(self,fn):
        ffn = os.path.join(self.targetRoot, fn)
        return utils.readFile(ffn)

    def makeDir(self, fn, force=1):
        log.debug("Calling makeDir to create '%s'.", fn)
        ffn = os.path.join(self.targetRoot, fn)
        log.debug("Together with the targetroot that means '%s'.", ffn)
        return utils.makeDir(ffn, force=force)

    def getSkinPath(self, element):
        fp = element.getRootPackage().getFilePath()
        mn = element.getRootPackage().getModuleName()
        return os.path.join(fp, 'skins', mn)

    def generateDependentImports(self, element):
        out = StringIO()
        res = BaseGenerator.generateDependentImports(self, element)
        print >> out, res
        generate_expression_validator = False

        for att in element.getAttributeDefs():
            if att.getTaggedValue('validation_expression'):
                generate_expression_validator = True

        if generate_expression_validator:
            print >> out, 'from Products.validation.validators import ExpressionValidator'

        # Check for necessity to import ArrayField
        import_array_field = False
        for att in element.getAttributeDefs():
            if att.getUpperBound() != 1:
                import_array_field = True
                break

        if import_array_field:
            print >>out, 'from Products.CompoundField.ArrayField import ArrayField'

        start_marker = True
        for iface in self.getAggregatedInterfaces(element):
            if start_marker:
                print >>out, 'from Products.Archetypes.AllowedTypesByIface import AllowedTypesByIfaceMixin'
                start_marker = False
            print >>out, 'from %s import %s' % (iface.getQualifiedModuleName(forcePluginRoot=True),iface.getCleanName())

        if self.backreferences_support:
            print >>out, 'from Products.ATBackRef.BackReferenceField import BackReferenceField, BackReferenceWidget'
            
        
        # #############################################################################    
        # ACV 20090926 to add generation of aliases (view method names to other view method names) 
        
        if element.getTaggedValue('aliases', '').strip():
            print >>out, 'from Products.ATContentTypes.content.document import ATDocument'
            print >>out, 'from Products.ATContentTypes.content.base import updateAliases'
        # ACV
        # #############################################################################    

        return out.getvalue()

    def addMsgid(self, msgid, msgstr, element, fieldname):
        """Adds a msgid to the catalog if it not exists.

        If it exists and not listed in occurrences, then add its occurence.
        """
        log.debug("Add msgid %s" % msgid)
        msgid = utils.normalize(msgid)
        if has_i18ndude and self.build_msgcatalog and len(self.msgcatstack):
            msgcat = self.msgcatstack[len(self.msgcatstack)-1]
            package = element.getPackage()
            module_id = os.path.join(element.getPackage().getFilePath(includeRoot=0),
                                     element.getName()+'.py')
            msgcat.add(msgid, msgstr=msgstr, references=[module_id])

    def generateMethodActions(self, element):
        log.debug("Generating method actions...")
        outfile=StringIO()
        print >> outfile
        log.debug("First finding our methods.")
# ACV OJO to add inheritable actions: 
# class methods with stereotype action and tagged value inheritable == "True"
# WAS
#        for m in element.getMethodDefs():
 
        someMethods = self.getMethodDefsAndInheritableActions( element)
        for m in someMethods:
            method_name = m.getName()
            code = utils.indent(m.getTaggedValue('code', ''), 1)
            if m.hasStereoType(['action', 'view', 'form'],
                               umlprofile=self.uml_profile):
                log.debug("Method has stereotype action/view/form.")
                action_name = m.getTaggedValue('action','').strip()
                if not action_name:
                    log.debug("No tagged value 'action', trying '%s' with a "
                              "default to the methodname.",
                              m.getStereoType())
                    action_name=m.getTaggedValue(m.getStereoType(), method_name).strip()
                log.debug("Ok, generating %s for %s.",
                          m.getStereoType(), action_name)
                dict={}

                if not action_name.startswith('string:') and not action_name.startswith('python:'):
                    action_target='string:${object_url}/'+action_name
                else:
                    action_target=action_name

                dict['action'] = utils.getExpression(action_target)
                dict['action_category'] = utils.getExpression(m.getTaggedValue('category','object'))
                dict['action_id'] = m.getTaggedValue('id',method_name)
                dict['action_label'] = m.getTaggedValue('action_label') or \
                    m.getTaggedValue('label',method_name)
                # action_label is deprecated and for backward compability only!
                dict['permission'] = utils.getExpression(m.getTaggedValue('permission','View'))

                condition=m.getTaggedValue('condition') or '1'
                dict['condition']='python:'+condition

                if not (m.hasTaggedValue('create_action') and utils.isTGVFalse(m.getTaggedValue('create_action'))):
                    print >>outfile, ACT_TEMPL % dict

            if m.hasStereoType('view', umlprofile=self.uml_profile):
                f=self.makeFile(os.path.join(self.getSkinPath(element),action_name+'.pt'),0)
                if f:
                    templdir=os.path.join(sys.path[0],'templates')
                    viewTemplate=open(os.path.join(templdir,'action_view.pt')).read()
                    f.write(viewTemplate % code)

            elif m.hasStereoType('form', umlprofile=self.uml_profile):
                f=self.makeFile(os.path.join(self.getSkinPath(element),action_name+'.cpt'),0)
                if f:
                    templdir=os.path.join(sys.path[0],'templates')
                    viewTemplate=open(os.path.join(templdir,'action_view.pt')).read()
                    f.write(viewTemplate % code)

            elif m.hasStereoType(['portlet_view','portlet'], umlprofile=self.uml_profile):
                view_name=m.getTaggedValue('view').strip() or method_name
                autoinstall=m.getTaggedValue('autoinstall')
                portlet='here/%s/macros/portlet' % view_name
                if autoinstall=='left':
                    self.left_slots.append(portlet)
                if autoinstall=='right':
                    self.right_slots.append(portlet)

                f=self.makeFile(os.path.join(self.getSkinPath(element),view_name+'.pt'),0)
                if f:
                    templdir=os.path.join(sys.path[0],'templates')
                    viewTemplate=open(os.path.join(templdir,'portlet_template.pt')).read()
                    label = m.getTaggedValue('label', method_name)
                    f.write(viewTemplate % {'method_name': method_name,
                                            'label': label})

        res=outfile.getvalue()
        return res


    def generateAdditionalImports(self, element):
        outfile = StringIO()

        if element.hasAssocClass:
            print >> outfile,'from Products.Archetypes.ReferenceEngine import ContentReferenceCreator'

        useRelations = 0

        #check wether we have to import Relation's Relation Field
        for rel in element.getFromAssociations():
            if self.getOption('relation_implementation',rel,'basic') == 'relations':
                useRelations = 1

        for rel in element.getToAssociations():
            if self.getOption('relation_implementation',rel,'basic') == 'relations' and \
               (rel.getTaggedValue('inverse_relation_name') or rel.fromEnd.isNavigable) :
                useRelations = 1

        if useRelations:
            print >> outfile,'from Products.Relations.field import RelationField'

        if element.hasStereoType(self.variable_schema, umlprofile=self.uml_profile):
            print >> outfile,'from Products.Archetypes.VariableSchemaSupport import VariableSchemaSupport'

        # ATVocabularyManager imports
        if element.hasStereoType(self.vocabulary_item_stereotype, umlprofile=self.uml_profile):
            print >> outfile, 'from Products.ATVocabularyManager.tools import registerVocabularyTerm'
        if element.hasStereoType(self.vocabulary_container_stereotype, umlprofile=self.uml_profile):
            print >> outfile, 'from Products.ATVocabularyManager.tools import registerVocabulary'
        if self.getOption('vocabulary:type', element, None) == 'ATVocabularyManager' or \
           element.hasAttributeWithTaggedValue('vocabulary:type','ATVocabularyManager'):
            print >> outfile, 'from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary'

        return outfile.getvalue()


    def getImportsByTaggedValues(self, element):
        # imports by tagged values
        additionalImports=self.getOption('imports', element, default=None,
                                         aggregate=True)
        return additionalImports


    def generateModifyFti(self,element):
        hide_actions = element.getTaggedValue('hide_actions', '').strip()
        if not hide_actions:
            return ''

        # Also permit comma separation, since Poseidon doesn't like multi-line
        # tagged values and specifying multiple tagged values is a pain
        hide_actions = hide_actions.replace(',', '\n')

        hide_actions=', '.join(["'"+a.strip()+"'" for a in hide_actions.split('\n')])
        return MODIFY_FTI % {'hideactions':hide_actions, }


    

    # #############################################################################    
    # ACV 20090926 to add generation of aliases (map view method names to other view method names) 
    def generateAliases(self, theElement):
        """Generate the aliases (view method names to other view method names)
        """

        unAliases = theElement.getTaggedValue('aliases', '').strip()
        unAliases_1 = theElement.getTaggedValue('aliases_1', '').strip()
        if not ( unAliases or unAliases_1):
            return ''
        
        unAllAliases = ''
        if unAliases and unAliases_1:
            unAliasesValue = {}
            try:
                unAliasesValue = eval( unAliases) 
            except:
                None
            unAliasesValue_1 = {}
            try:
                unAliasesValue_1 = eval( unAliases_1) 
            except:
                None
            unAliasesValue.update( unAliasesValue_1)   
            unAllAliases = repr( unAliasesValue)
        
        else:
            if unAliases:
                unAllAliases = unAliases
            else:
                unAllAliases = unAliases_1
                
            
        unAliasesCode = ALIASES_FULL % unAllAliases
        return unAliasesCode
    

        
        
    def generateActionsAndViews(self, element, subtypes):
        """Generate the views and actions (used to be in generateFti())
        """

        hasActions=False
        actTempl=ACTIONS_START
        base_actions=element.getTaggedValue('base_actions', '').strip()
        if base_actions:
            hasActions=True
            base_actions += ' + '
            actTempl = actTempl % base_actions
        else:
            actTempl = actTempl % ''

        if self.generateDefaultActions or element.getTaggedValue('default_actions'):
            hasActions=True
            actTempl += DEFAULT_ACTIONS
            if subtypes:
                actTempl=actTempl+DEFAULT_ACTIONS_FOLDERISH

        method_actions = self.generateMethodActions(element)
        if method_actions.strip():
            hasActions=True
            actTempl +=method_actions
        actTempl+=ACTIONS_END
        if hasActions:
            return actTempl
        else:
            return

        
    def getTypeMsgidsForClassNamed(self, theElement, theClassName): 
        if not theClassName:
            return None
        
        aClass = self.getClassNamed( theElement, theClassName)
        if not aClass:
            return None
        
        return self.getTypeMsgids( aClass)
         
        
        
    def getTypeMsgids(self, theClass):    
        if not theClass:
            return None
        
        aProductName = theClass.getPackage().getProductName()

        anArchetypeNameMsgid  = '%s_%s_label'  % ( aProductName, theClass.name, )
        aTypeDescriptionMsgid = '%s_%s_help'  % ( aProductName, theClass.name, )
        
        return [ anArchetypeNameMsgid, aTypeDescriptionMsgid, ]  
        
        
        
    def generateFti(self, element, subtypes):
        ''' generates Factory Type Information related attributes on the class'''

        ftiTempl=FTI_TEMPL
        immediate_view = self.getOption('immediate_view', element, default='base_view')        
        default_view = self.getOption('default_view', element, default=immediate_view)
        suppl_views = self.getOption('suppl_views', element, default='()')

        # In principle, allow globally
        global_allow = True
        # Unless it is only contained by another element
        if element.isDependent():
            # WARNING! isDependent() doesn't seem to work,
            # aggregates and compositions aren't detected.
            # 2005-05-11 reinout
            global_allow = False
        # Or if it is a hidden element
        if element.hasStereoType('hidden', umlprofile=self.uml_profile):
            global_allow = False
        # Or if it is a tool-like thingy
        if (element.hasStereoType(self.portal_tools, umlprofile=self.uml_profile) or
            element.hasStereoType(self.vocabulary_item_stereotype, umlprofile=self.uml_profile) or
            element.hasStereoType(self.cmfmember_stereotype, umlprofile=self.uml_profile) or
            element.hasStereoType(self.remember_stereotype, umlprofile=self.uml_profile) or
            element.isAbstract()):
            global_allow = False
        # But the tagged value overwrites all
        tgvglobalallow = self.getOption('global_allow', element, default=None)




        if utils.isTGVFalse(tgvglobalallow):
            global_allow = False
        if utils.isTGVTrue(tgvglobalallow):
            global_allow = True

        has_content_icon=''
        content_icon=element.getTaggedValue('content_icon')
        if not content_icon:
            # If an icon file with the default name exists in the skin, do not
            # comment out the icon definition
            content_icon = element.getCleanName()+'.gif'
            icon_filename = os.path.join(self.getSkinPath(element), content_icon)
            icon_full_filename = os.path.join(self.targetRoot, icon_filename)
            if not os.path.isfile(icon_full_filename):
                has_content_icon='#'

        # If we are generating a tool, include the template which sets
        # a tool icon
        if element.hasStereoType(self.portal_tools, umlprofile=self.uml_profile):
            ftiTempl += TOOL_FTI_TEMPL

        has_toolicon=''
        toolicon = element.getTaggedValue('toolicon')
        if not toolicon:
            has_toolicon='#'
            toolicon = element.getCleanName()+'.gif'


        # Filter content types?
        # Filter by default if it's a folder-like thingy
        filter_default = self.elementIsFolderish(element)
        # But a tagged value overrides
        filter_content_types = utils.isTGVTrue(element.getTaggedValue('filter_content_types',
                                                                      filter_default))
        # Set a type description.

             
        typeName = element.getTaggedValue('archetype_name') or \
                 element.getTaggedValue('label') or \
                 element.getName ()


        typeDescription = utils.getExpression(element.getTaggedValue('typeDescription', typeName))

        
        aTGVsDict = {
            'subtypes'             : repr(tuple(subtypes)),
            'has_content_icon'     : has_content_icon,
            'content_icon'         : content_icon,
            'has_toolicon'         : has_toolicon,
            'toolicon'             : toolicon,
            'global_allow'         : global_allow,
            'immediate_view'       : immediate_view,
            'default_view'         : default_view,
            'suppl_views'          : suppl_views,
            'filter_content_types' : filter_content_types,
            'typeDescription'      : typeDescription,
            'type_name_lc'         : element.getName().lower()}

# ACV OJO ADDITION 20080908
# Pass to generator tagged values with the label and description

        aProductName = element.getPackage().getProductName()

        anArchetypeNameMsgid  = '%s_%s_label'  % ( aProductName, element.name, )
        aTypeDescriptionMsgid = '%s_%s_help'  % ( aProductName, element.name, )
        
        unasTypesMsgids = self.getTypeMsgids( element)
        if unasTypesMsgids and len( unasTypesMsgids) > 1 and unasTypesMsgids[0] and unasTypesMsgids[ 1]:
            anArchetypeNameMsgid  = unasTypesMsgids[ 0]  
            aTypeDescriptionMsgid  = unasTypesMsgids[ 1]  

                
        aTGVsDict[ 'archetype_name2'] = element.getTaggedValue('archetype_name2', '')
        aTGVsDict[ 'typeDescription2'] = element.getTaggedValue('typeDescription2', '')
        aTGVsDict[ 'archetype_name_msgid'] = anArchetypeNameMsgid
        aTGVsDict[ 'typeDescription_msgid'] = aTypeDescriptionMsgid
        aTGVsDict[ 'exclude_from_typeconfigs'] = element.getTaggedValue('exclude_from_typeconfigs', '')

        aTGVsDict[ 'factory_methods']  = element.getTaggedValue( 'factory_methods', None)
        aTGVsDict[ 'factory_enablers'] = element.getTaggedValue( 'factory_enablers', None)
        aTGVsDict[ 'propagate_delete_impact_to'] = 'None'
        unPropagateDeleteImpactTo = element.getTaggedValue( 'propagate_delete_impact_to', None)
        if unPropagateDeleteImpactTo:
            aTGVsDict[ 'propagate_delete_impact_to'] = unPropagateDeleteImpactTo
            

        res = ftiTempl % aTGVsDict
        
        
        # Only set allow_discussion if it is explicitly set with a
        # tagged value. Leave empty if not, otherwise it cannot be
        # (un)set in Plone afterwards
        allow_discussion = element.getTaggedValue('allow_discussion', 'NOTSET')
        template = "    allow_discussion = %s\n"
        if allow_discussion != 'NOTSET':
            res += template % allow_discussion
        return res

    # TypeMap for Fields, format is
    #   type: {field: 'Y',
    #          lines: [key1=value1,key2=value2, ...]
    #   ...
    #   }
    typeMap= {
            'string': {'field': u'StringField',
                       'map': {},
                       },
            'text':  {'field': u'TextField',
                       'map': {},
            },
            'richtext': {'field': u'TextField',
                         'map': {u'default_output_type': u"'text/html'", u'allowable_content_types': u"('text/plain', 'text/structured', 'text/html', 'application/msword',)",},
            },
            'selection': {'field': u'StringField',
                        'map': {},
            },
            'multiselection': {'field': u'LinesField',
                               'map': {u'multiValued': u'1', },
            },
            'integer': {'field': u'IntegerField',
                        'map': {},
            },
            'float': {'field': u'FloatField',
                        'map': {},
            },
            'fixedpoint': {'field': u'FixedPointField',
                        'map': {},
            },
            'lines': {'field': u'LinesField',
                        'map': {},
            },
            'date': {'field': u'DateTimeField',
                        'map': {},
            },
            'image': {'field': u'ImageField',
                        'map': {u'storage': u'AttributeStorage()', },
            },
            'file': {'field': u'FileField',
                    'map': {u'storage': u'AttributeStorage()', },
            },
            'reference': {'field': u'ReferenceField',
                        'map': {},
            },
            'relation': {'field': u'RelationField',
                        'map': {},
            },
            'backreference': {'field': u'BackReferenceField',
                                'map': {},
            },
            'boolean': {'field': u'BooleanField',
                        'map': {},
            },
            'computed': {'field': u'ComputedField',
                        'map': {},
            },
            'photo': {'field': u'PhotoField',
                        'map': {},
            },
            'generic': {'field': u'%(type)sField',
                'map': {},
            },
        }

    widgetMap={
        'string': u'StringWidget' ,
        'fixedpoint': u'DecimalWidget' ,
        'float': u'DecimalWidget',
        'text': u'TextAreaWidget',
        'richtext': u'RichWidget',
        'file': u'FileWidget',
        'image': u'ImageWidget',
        'date': u'CalendarWidget',
        'selection': u'SelectionWidget',
        'multiselection': u'MultiSelectionWidget',
        'BackReference': u'BackReferenceWidget'
    }

    coerceMap={
        'xs:string': u'string',
        'xs:int': u'integer',
        'xs:integer': u'integer',
        'xs:byte': u'integer',
        'xs:double': u'float',
        'xs:float': u'float',
        'xs:boolean': u'boolean',
        'ofs.image': u'image',
        'ofs.file': u'file',
        'xs:date': u'date',
        'datetime': u'date',
        'list': u'lines',
        'liste': u'lines',
        'image': u'image',
        'int': u'integer',
        'bool': u'boolean',
        'dict': u'string',
        'String': u'string',
        '': u'string',     #
        None: u'string',
    }

    hide_classes=['EARootClass','int','float','boolean','long','bool',
                  'void','string', 'dict','tuple','list','object','integer',
                  'java::lang::int','java::lang::string','java::lang::long',
                  'java::lang::float','java::lang::void']+\
                list(typeMap.keys())+list(coerceMap.keys()) # Enterprise Architect and other automagically created crap Dummy Class

    def coerceType(self, intypename):
        #print 'coerceType: ',intypename,' -> ',
        typename=intypename.lower()
        if typename in self.typeMap.keys():
            return typename

        if typename=='copy':
            return typename

        if self.unknownTypesAsString:
            ctype=self.coerceMap.get(typename.lower(),'string')
        else:
            ctype=self.coerceMap.get(typename.lower(),None)
            if ctype is None:
                return 'generic' #raise ValueError,'Warning: unknown datatype : >%s< (use the option --unknown-types-as-string to force unknown types to be converted to string' % typename

        #print ctype,'\n'
        return ctype

    def getFieldAttributes(self,element):
        """ converts the tagged values of a field into extended attributes for the archetypes field """
        noparams=['documentation','element.uuid','transient','volatile',
                  'widget','copy_from','source_name']
        convtostring=['expression']
        map={}
        tgv=element.getTaggedValues()

        for kt in [('storage',),('callStorageOnSet',),('call_storage_on_set','callStorageOnSet')]:
            if len(kt)>1:
                skey=kt[0]
                key=kt[1]
            else:
                skey=kt[0]
                key=kt[0]

            if skey not in tgv.keys():
                v=self.getOption(skey,element,None)
                if v:
                    tgv.update({key:v})


        # set permissions, if theres one arround in the model
        perm=self.getOption('read_permission',element,default=None)
        if perm:
            tgv.update({'read_permission':perm})
        perm=self.getOption('write_permission',element,default=None)
        if perm:
            tgv.update({'write_permission':perm})

        # check for global settings
        searchable = self.getOption('searchable', element, default = _marker)
        if searchable is not _marker:
            tgv.update({'searchable': searchable})
        index = self.getOption('index', element, default=_marker)
        if index is not _marker:
            tgv.update({'index': index})

        # set attributes from tgv
        for k in tgv.keys():
            if k not in noparams and not k.startswith('widget:'):
                v = tgv[k]
                if v is None:
                    log.warn(u"Empty tagged value for tag '%s' in field '%s'.",
                             k, element.getName())
                    continue
                v = v.decode('utf8')

                if k not in self.nonstring_tgvs:
                    v=utils.getExpression(v)
                # [optilude] Permit python: if people forget they
                # don't have to (I often do!)
                else:
                    if v.startswith('python:'):
                        v = v[7:]

                map.update({k: v})
        return map

    def getWidget(self, widgettype, element, fieldname, elementclass, fieldclassname=None, theIsAggregation=False, theToEndName=""):
        """ returns either default widget, widget according to
        attributes or no widget.

        atributes/tgv's can be:
            * widget and a whole widget code block or
            * widget:PARAMETER which will be rendered as a PARAMETER=value

        """
        tgv = element.getTaggedValues()

# ACV OJO ADDITION 20080908

        tgv['owner_class_name'] = elementclass.name
        
# #############################################
# ACV OJO ADDITION 20080604
#  To default widget:label to the field label, and widget:description to the field:description
        
        if tgv.has_key( 'label') and not tgv.has_key('widget:label'):
            tgv['widget:label']= tgv['label']
        if tgv.has_key( 'label2') and not tgv.has_key('widget:label2'):
            tgv['widget:label2']= tgv['label2']
               
        if tgv.has_key( 'description') and not tgv.has_key('widget:description'):
            tgv['widget:description']= tgv['description']
        if tgv.has_key( 'description2') and not tgv.has_key('widget:description2'):
            tgv['widget:description2']= tgv['description2']
                 
  
            
        widgetcode = widgettype.capitalize()+'Widget'
        widgetmap = odict()
        custom = False # is there a custom setting for widget?
        widgetoptions = [t for t in tgv.items() if t[0].startswith('widget:')]

        # check if a global default overrides a widget. setting defaults is
        # provided through getOption.
        # to set an default just put:
        # default:widget:widgettype = widgetname
        # as a tagged value on the package or model
        if hasattr(element,'widgettype') and element.type != 'NoneType':
            atype = element.type
        else:
            atype = widgettype
        default_widget = self.getOption('default:widget:%s' % atype, element, None)

        if default_widget:
            widgetcode = default_widget + u'(\n'

        modulename = elementclass.getPackage().getProductName()
        check_map = odict()
        check_map['label']              = u"'%s'" % fieldname.capitalize().decode('utf8')
        check_map['label_msgid']        = u"'%s_label_%s'" % (modulename, utils.normalize(fieldname, 1))
        check_map['description_msgid']  = u"'%s_help_%s'" % (modulename, utils.normalize(fieldname, 1))
        check_map['i18n_domain']        = u"'%s'" % modulename

        
        if theIsAggregation:
            aScopedLabelMsgid        = u"'%s_%s_contents_%s_label'" % ( modulename, elementclass.name, theToEndName)
            aScopedDescriptionMsgid  = u"'%s_%s_contents_%s_help'"  % ( modulename, elementclass.name, theToEndName)
        else:
            if atype in [ "Reference"]:
                aScopedLabelMsgid        = u"'%s_%s_rel_%s_label'" % ( modulename, elementclass.name, fieldname)
                aScopedDescriptionMsgid  = u"'%s_%s_rel_%s_help'"  % ( modulename, elementclass.name, fieldname)
            else:
                aScopedLabelMsgid        = u"'%s_%s_attr_%s_label'" % ( modulename, elementclass.name, fieldname)
                aScopedDescriptionMsgid  = u"'%s_%s_attr_%s_help'"  % ( modulename, elementclass.name, fieldname)
       
        
# ACV OJO
# Abandon scoped, use again the standard msgid attributes
#        check_map['scoped_label_msgid']       = aScopedLabelMsgid              
#        check_map['scoped_description_msgid'] = aScopedDescriptionMsgid
        check_map['label_msgid']       = aScopedLabelMsgid              
        check_map['description_msgid'] = aScopedDescriptionMsgid
 
        
        wt = {} # helper

        if tgv.has_key('widget'):
            # Custom widget defined in attributes
            custom = True
            formatted = u''
            for line in tgv['widget'].split(u'\n'):
                if formatted:
                    line = utils.indent(line.strip(), 1)
                formatted += u"%s\n" % line
            widgetcode =  formatted

        elif [wt.update({t[0]:t[1]}) for t in widgetoptions if t[0] == u'widget:type']:
            custom = True
            widgetcode = wt['widget:type']

        elif self.widgetMap.has_key(widgettype) and not default_widget:
            # default widget for this widgettype found in widgetMap
            custom = True
            widgetcode = self.widgetMap[widgettype]

        elif fieldclassname:
            widgetcode="%s._properties['widget'](\n" % fieldclassname

        if ')' not in widgetcode: # XXX bad check *sigh*

            for tup in widgetoptions:
                key=tup[0][7:]
                val=tup[1]
                if key == 'type':
                    continue
                if key not in self.nonstring_tgvs:
                    val=utils.getExpression(val)
                # [optilude] Permit python: if people forget they don't have to (I often do!)
                else:
                    if val.startswith ('python:'):
                        val = val[7:]

                widgetmap.update({key:val})

            if '(' not in widgetcode:
                widgetcode += '(\n'

            ## before update the widget mapping, try to make a
            ## better description based on the given label

            for k in check_map:
                if not (k in widgetmap.keys()): # XXX check if disabled
                    widgetmap.update( {k: check_map[k]} )

            # remove description_msgid if there is no description
            if 'description' not in widgetmap.keys() and 'description_msgid' in widgetmap.keys() \
               and not self.default_description_generation:
                del widgetmap['description_msgid']

            if 'label_msgid' in widgetmap.keys() and has_enhanced_strip_support:
                self.addMsgid(widgetmap['label_msgid'].strip("'").strip('"'),
                              widgetmap.has_key('label') and widgetmap['label'].strip("'").strip('"') or fieldname,
                              elementclass,
                              fieldname
                          )
            if 'description_msgid' in widgetmap.keys() and has_enhanced_strip_support:
                self.addMsgid(widgetmap['description_msgid'].strip("'").strip('"'),
                              widgetmap.has_key('description') and widgetmap['description'].strip("'").strip('"') or fieldname,
                              elementclass,
                              fieldname
                          )

# ACV OJO
# Abandon scoped, use again the standard msgid attributes
# Originally: ACV ADDITION 20080908
            #if 'scoped_label_msgid' in widgetmap.keys() and has_enhanced_strip_support:
                #self.addMsgid(widgetmap['scoped_label_msgid'].strip("'").strip('"'),
                              #widgetmap.has_key('label') and widgetmap['label'].strip("'").strip('"') or fieldname,
                              #elementclass,
                              #fieldname
                          #)

            #if 'scoped_description_msgid' in widgetmap.keys() and has_enhanced_strip_support:
                #self.addMsgid(widgetmap['scoped_description_msgid'].strip("'").strip('"'),
                              #widgetmap.has_key('description') and widgetmap['description'].strip("'").strip('"') or fieldname,
                              #elementclass,
                              #fieldname
                          #)

            keqvs = list()
            for key in widgetmap:
                value = widgetmap[key]
                if type(value) != types.UnicodeType:
                    value = value.decode('utf-8')
                keqv = u'%s=%s' % (key, value)
                keqvs.append(keqv)

            widgetcode += utils.indent( \
                u',\n'.join(keqvs),
                1,
                skipFirstRow=0) \
                       + u',\n'
            widgetcode += u')'

        return widgetcode

    def getFieldFormatted(self, name, fieldtype, map={}, doc=None,
                          indent_level=0, rawType='String', array_field=False):
        """Return the a formatted field definition for the schema.
        """

        log.debug("Trying to get formatted field. name='%s', fieldtype='%s', "
                  "doc='%s', rawType='%s'.", name, fieldtype, doc, rawType)
        name = utils.normalize(name, 1)
        res = u''
        if array_field:
            array_options={}
            for key in map.keys():
                if key.startswith(u'array:'):
                    nkey=key[len(u'array:'):]
                    array_options[nkey]=map[key]
                    del map[key]

        # Capitalize only first letter of fields class name, keep camelcase
        a = rawType[0].upper()
        rawType = a + rawType[1:]

        # Add comment
        if doc:
            res += utils.indent(doc, indent_level, u'#') + u'\n' + res

        # If this is a generic field and the user entered MySpecialField,
        # then don't suffix it with 'field''
        if rawType.endswith(u'Field'):
            rawType = rawType[:-5]

        res += utils.indent(u"%s(\n    name='%s',\n" % (
            fieldtype % {'type': rawType}, name), indent_level)
        if map:
            prepend = utils.indent(u'', indent_level)
            for key in map:
                if key.find(u':') >= 0:
                    continue
                lines = map[key]
                if isinstance(lines, basestring):
                    linebreak = lines.find(u'\n')

                    if linebreak < 0:
                        linebreak = len(lines)
                    firstline = lines[:linebreak]
                else:
                    firstline = lines

                res += u'%s%s=%s' % (prepend, key, firstline)
                if isinstance(lines, basestring) and linebreak < len(lines):
                    for line in lines[linebreak+1:].split(u'\n'):
                        line = utils.indent(line, indent_level + 1)
                        res += u"\n%s" % line

                prepend = u',\n%s' % utils.indent('', indent_level +1)

        res += u'\n%s' % utils.indent(u'),', indent_level) + u'\n\n'

        if array_field:
            res = res.strip()
            if array_options.get('widget', None):
                if array_options['widget'].find('(') == -1:
                    array_options['widget'] += u'()'

            array_defs = u',\n'.join([u"%s=%s" % item for item in array_options.items()])
            res =  ARRAYFIELD % ( utils.indent(res, 2), utils.indent(array_defs, 2) ) 

        return res

    def getFieldsFormatted(self, field_specs):
        """Return the formatted field definitions for the schema from field_specs.
        """
        res = u''
        for field_spec in field_specs:
            log.debug("field_spec is %r.",
                      field_spec)
            try:
                # The following is needed to work around a bug in Sunew's
                # array_field fix. Apparently associations don't have the
                # rawType key. Should be fixed elsewhere, though.
                if type(field_spec) in StringTypes:
                    # need this for copied fields
                    res += field_spec
                elif (field_spec.has_key('rawType') and
                      field_spec.has_key('array_field')):
                    res += self.getFieldFormatted(field_spec['name'], 
                                                  field_spec['fieldtype'],
                                                  field_spec['map'],
                                                  field_spec['doc'],
                                                  field_spec['indent_level'],
                                                  field_spec['rawType'],
                                                  field_spec['array_field'],
                                              )
                else:
                    res += self.getFieldFormatted(field_spec['name'], 
                                                  field_spec['fieldtype'],
                                                  field_spec['map'],
                                                  field_spec['doc'],
                                                  field_spec['indent_level']
                                              )
            except Exception, e:
                log.critical("Couldn't render fields from field_specs: '%s'.",
                             field_specs)
                raise
        return res

    def getFieldSpec(self, element, classelement, indent_level=0):
        """Gets the schema field code."""
        typename = element.type
        ctype = self.coerceType(typename)
        map = typeMap[ctype]['map'].copy()
        res= {'name': element.getCleanName(),
              'fieldtype': self.typeMap[ctype]['field'].copy(),
              'map': map,
              'indent_level': indent_level}
        return res

    def addVocabulary(self, element, attr, map):
        # ATVocabularyManager: Add NamedVocabulary to field.
        vocaboptions = {}
        for t in attr.getTaggedValues().items():
            if t[0].startswith('vocabulary:'):
                vocaboptions[t[0][11:]] = t[1]
        if vocaboptions:
            if not 'name' in vocaboptions.keys():
                vocaboptions['name'] = '%s_%s' % (element.getCleanName(), \
                                                  attr.getName())
            if not 'term_type' in vocaboptions.keys():
                vocaboptions['term_type'] = self.getOption('vocabulary:term_type', attr, 'SimpleVocabularyTerm')

            if not 'vocabulary_type' in vocaboptions.keys():
                vocaboptions['vocabulary_type'] = self.getOption('vocabulary:vocabulary_type', attr, 'SimpleVocabulary')

            if not 'type' in vocaboptions.keys():
                vtype = self.getOption('vocabulary:type', attr, None)
                if vtype:
                    vocaboptions['type'] = vtype

            map.update({
                'vocabulary':'NamedVocabulary("""%s""")' % vocaboptions['name']
            })

            # remember this vocab-name and if set its portal_type
            package = element.getPackage()
            currentproduct = package.getProductName()
            if not currentproduct in self.vocabularymap.keys():
                self.vocabularymap[currentproduct] = {}

            if not vocaboptions['name'] in self.vocabularymap[currentproduct].keys():
                self.vocabularymap[currentproduct][vocaboptions['name']] = (
                    vocaboptions['vocabulary_type'],
                    vocaboptions['term_type'])
            else:
                log.warn("Vocabulary with name '%s' defined more than once.",
                         vocaboptions['name'])

        # end ATVM

        
        
        
        
        
    def getFieldSpecFromAttribute(self, attr, classelement, indent_level=0):
        """Gets the schema field code."""

        if not hasattr(attr, 'type') or attr.type == 'NoneType':
            ctype = 'string'
        else:
            ctype = self.coerceType(attr.type)

        if ctype=='copy':
            name = getattr(attr, 'rename_to', attr.getName())
            field = utils.indent("copied_fields['%s'],\n" % name, indent_level)
            return field

        map = self.typeMap[ctype]['map'].copy()
        if attr.hasDefault():
            map.update({'default': utils.getExpression(attr.getDefault())})
        map.update(self.getFieldAttributes(attr))

        atype = self.typeMap[ctype]['field']

        if ctype != 'generic' and self.i18n_content_support in self.i18n_at \
           and attr.isI18N():
            atype = 'I18N' + atype

        if ctype=='generic':
            fieldclassname=attr.type            
        else:
            fieldclassname=atype

        widget = self.getWidget(ctype, attr, attr.getName(), classelement, fieldclassname=fieldclassname)

        if not widget.startswith('GenericWidget'):
            map.update({'widget': widget})

        self.addVocabulary(classelement, attr, map)

        doc=attr.getDocumentation(striphtml=self.strip_html)

        if attr.hasTaggedValue('validators'):
            #make validators to a list in order to append the ExpressionValidator
            val = attr.getTaggedValue('validators')
            try:
                map['validators'] = tuple(eval(val))
            except:
                map['validators'] = tuple(val.split(','))

        if map.has_key('validation_expression'):
            #append the validation_expression to the validators
            expressions = attr.getTaggedValue('validation_expression').split('\n')
            errormsgs = attr.getTaggedValue('validation_expression_errormsg').split('\n')
            if errormsgs and errormsgs != [''] \
               and len(errormsgs) != len(expressions):
                log.critical('validation_expression and validation_expression_'
                             'errormsg tagged value must have the same size '
                             '(%s, %s)' %(expressions,errormsgs))
            def corresponding_error(errormsgs, ind):
                if errormsgs and errormsgs != ['']:
                    return ", '"+errormsgs[ind]+"'"
                return ""
            expval = ["""ExpressionValidator('''python:%s'''%s)""" %
                      (expression,corresponding_error(errormsgs,exp_index))
                      for exp_index,expression in enumerate(expressions)]

            if map.has_key('validators'):
                map['validators'] = repr(map.get('validators',())) + \
                   '+('+','.join(expval)+',)'
            else:
                map['validators'] = '(' + ','.join(expval) + ',)'

            del map['validation_expression']
            if map.has_key('validation_expression_errormsg'):
                del map['validation_expression_errormsg']

        res={'name':attr.getName(),
             'fieldtype':atype,
             'map':map,
             'doc':doc,
             'indent_level':indent_level,
             'rawType':attr.getType(),
             'array_field':attr.getUpperBound() != 1}

# ACV OJO ADDITION 20080908
# Pass to generator additional tagged values 
        
        if attr.hasTaggedValue('label'):
            res[ 'label'] = attr.getTaggedValue('label')
        if attr.hasTaggedValue('label2'):
            res[ 'label2'] = attr.getTaggedValue('label2')
        if attr.hasTaggedValue('description'):
            res[ 'description'] = attr.getTaggedValue('description')
        if attr.hasTaggedValue('description2'):
            res[ 'description2'] = attr.getTaggedValue('description2')
        if attr.hasTaggedValue('owner_class_name'):
            res[ 'owner_class_name'] = attr.getTaggedValue('owner_class_name')
            map[ 'owner_class_name'] = '"%s"' % attr.getTaggedValue('owner_class_name')
            
        if attr.hasTaggedValue('exclude_from_views'):
            res[ 'exclude_from_views'] = attr.getTaggedValue('exclude_from_views')
            map[ 'exclude_from_views'] = '"%s"' % attr.getTaggedValue('exclude_from_views')

        if attr.hasTaggedValue('custom_presentation_view'):
            res[ 'custom_presentation_view'] = attr.getTaggedValue('custom_presentation_view')
            map[ 'custom_presentation_view'] = '"%s"' % attr.getTaggedValue('custom_presentation_view')
            
            
        if attr.hasTaggedValue('is_creation_date'):
            map[ 'is_creation_date'] = attr.getTaggedValue('is_creation_date').lower() == 'true'

        if attr.hasTaggedValue('is_creation_date'):
            map[ 'is_creator_user'] = attr.getTaggedValue('is_creator_user').lower() == 'true'

        if attr.hasTaggedValue('is_creation_date'):
            map[ 'is_modification_date'] = attr.getTaggedValue('is_modification_date').lower() == 'true'

        if attr.hasTaggedValue('is_creation_date'):
            map[ 'is_modificator_user'] = attr.getTaggedValue('is_modificator_user').lower() == 'true'

        if attr.hasTaggedValue('is_change_log'):
            map[ 'is_change_log'] = attr.getTaggedValue('is_change_log').lower() == 'true'

        if attr.hasTaggedValue('additional_columns'):
            someAdditionalColumnsString   = attr.getTaggedValue( 'additional_columns') or None
            someAdditionalColumns = []
            if someAdditionalColumnsString:
                try:
                    someAdditionalColumns = eval( someAdditionalColumnsString)
                except:
                    None
                if someAdditionalColumns:
                    map[ 'additional_columns'] = someAdditionalColumns
                    
        if attr.hasTaggedValue('allowed_types'):
            someAllowedTypesString   = attr.getTaggedValue( 'allowed_types') or None
            someAllowedTypes = []
            if someAllowedTypesString:
                try:
                    someAllowedTypes = eval( someAllowedTypesString)
                except:
                    None
                if someAllowedTypes:
                    map[ 'allowed_types'] = someAllowedTypes
                    
            
        if attr.type == 'selection':
            unVocabulary = attr.getTaggedValue( 'vocabulary')
            if unVocabulary and unVocabulary.startswith( 'python:'):
                unVocabulary = unVocabulary[ len( 'python:'):]
            if unVocabulary:
                someVocabularyOptions = []
                try:
                    someVocabularyOptions = eval( unVocabulary)   
                except:
                    None
                if someVocabularyOptions and someVocabularyOptions.__class__.__name__ in [  'list', 'set', 'tuple']:
                    #unVocabulary2 = attr.getTaggedValue( 'vocabulary2')    
                    #if unVocabulary2 and unVocabulary2.startswith( 'python:'):
                        #unVocabulary2 = unVocabulary2[ len( 'python:'):]
                    #if unVocabulary2:
                        #someVocabularyOptions2 = []
                        #try:
                            #someVocabularyOptions2 = eval( unVocabulary2)   
                        #except:
                            #None     
                    someVocabularySymbols = []
                    for unOptionIndex in range( len( someVocabularyOptions)):
                        unVocabularyOption = someVocabularyOptions[ unOptionIndex]
                        unOptionSymbol      = '%s_%s_attr_%s_option_%s'  % ( attr.getParent().getPackage().getProductName(), attr.getParent().name, attr.name, unVocabularyOption)
                        someVocabularySymbols.append( unOptionSymbol)
                    if someVocabularySymbols:
                        attr.setTaggedValue( 'vocabulary_msgids', someVocabularySymbols)    
                        map[ 'vocabulary_msgids'] = someVocabularySymbols
            
        return res

    
    def getFieldSpecFromAssociation(self, rel, classelement, indent_level=0):
        """Return the schema field code."""

        log.debug("Getting the field string from an association.")
        multiValued = 0
        obj = rel.toEnd.obj
        name = rel.toEnd.getName()
        relname = rel.getName()
        log.debug("Endpoint name: '%s'.", name)
        log.debug("Relationship name: '%s'.", relname)

        if obj.isAbstract():
            allowed_types= tuple(obj.getGenChildrenNames())
        else:
            allowed_types=(obj.getName(),) + tuple(obj.getGenChildrenNames())

        if int(rel.toEnd.mult[1]) == -1:
            multiValued = 1
        if name == None:
            name = obj.getName()+'_ref'

        if self.getOption('relation_implementation', rel, 'basic') == 'relations':
            log.debug("Using the 'relations' relation implementation.")
            # The relation can override the field
            field = self.getOption('reference_field',rel,None) or \
                  rel.getTaggedValue('reference_field') or \
                  rel.toEnd.getTaggedValue('reference_field') or \
                  rel.getTaggedValue('field') or \
                  rel.toEnd.getTaggedValue('field') or \
                  self.typeMap['relation']['field']
            # TBD: poseidon reference-as-field handling or so...
            if not field:
                message = "Somehow we couldn't get at the fieldname. " \
                        "Use normal drawn associations instead of " \
                        "a named reference."
                log.critical(message)
                raise message

            map = self.typeMap['relation']['map'].copy()
            map.update({'multiValued': multiValued,
                        'relationship': "'%s'" % relname})

# ###########################################
# OJO ACV ADDITION
# add inverse relation name
            map.update({'inverse_relationship': "'%s'" % rel.getInverseName(),
                        'inverse_relation_field_name' : "'%s'" % rel.fromEnd.getName(),})
            
# ###########################################
# OJO ACV ADDITION
# mark if dependency supplier
            if rel.getTaggedValue( 'dependencySupplier', '') == rel.toEnd.getName():
                map.update({'dependency_supplier': "True" } )
                

# ###########################################
# OJO ACV ADDITION
# We want to pass the TGVs for the labels and descriptions 
# of the direct relation
#
            someTGVs = rel.getTaggedValues()
            if someTGVs.has_key('label'):
                rel.toEnd.taggedValues['label'] = someTGVs['label']
            if someTGVs.has_key('description'):
                rel.toEnd.taggedValues['description'] = someTGVs['description']
            if someTGVs.has_key('inverse_relation_label'):
                rel.toEnd.taggedValues['inverse_relation_label'] = someTGVs['inverse_relation_label']
            if someTGVs.has_key('inverse_relation_description'):
                rel.toEnd.taggedValues['inverse_relation_description'] = someTGVs['inverse_relation_description']
            if someTGVs.has_key('label2'):
                rel.toEnd.taggedValues['label2'] = someTGVs['label2']
            if someTGVs.has_key('description2'):
                rel.toEnd.taggedValues['description2'] = someTGVs['description2']
            if someTGVs.has_key('inverse_relation_label2'):
                rel.toEnd.taggedValues['inverse_relation_label2'] = someTGVs['inverse_relation_label2']
            if someTGVs.has_key('inverse_relation_description2'):
                rel.toEnd.taggedValues['inverse_relation_description2'] = someTGVs['inverse_relation_description2']
  

            map[ 'owner_class_name'] = '"%s"' % classelement.name

            map.update(self.getFieldAttributes(rel.toEnd))
            
            map.update({'widget': self.getWidget('Reference', rel.toEnd,
                                                 name, classelement)})
            
          
            
            
        else:
            log.debug("Using the standard relation implementation.")
            # The relation can override the field
            field = rel.getTaggedValue('reference_field') or \
                  rel.toEnd.getTaggedValue('reference_field') or \
                  self.typeMap['reference']['field']
            # TBD: poseidon reference-as-field handling or so...
            if not field:
                message = "Somehow we couldn't get at the fieldname. " \
                        "Use normal drawn associations instead of " \
                        "a named reference."
                log.critical(message)
                raise message
            map = self.typeMap['reference']['map'].copy()
            map.update({'allowed_types': repr(allowed_types),
                        'multiValued': multiValued,
                        'relationship': "'%s'" % relname})
            map.update(self.getFieldAttributes(rel.toEnd))
            map.update({'widget':self.getWidget('Reference', rel.toEnd,
                                                name, classelement)})

            if getattr(rel,'isAssociationClass',0):
                # Association classes with stereotype "stub" and tagged
                # value "import_from" will not use ContentReferenceCreator
                if rel.hasStereoType(self.stub_stereotypes,
                                     umlprofile=self.uml_profile) :
                    map.update({'referenceClass':"%s" % rel.getName()})
                    # do not forget the import!!!
                else:
                    map.update({'referenceClass':"ContentReferenceCreator('%s')"
                                % rel.getName()})

        if rel.hasTaggedValue( 'additional_columns'):
            someAdditionalColumnsString   = rel.getTaggedValue( 'additional_columns') or None
            someAdditionalColumns = []
            if someAdditionalColumnsString:
                try:
                    someAdditionalColumns = eval( someAdditionalColumnsString)
                except:
                    None
                if someAdditionalColumns:
                    map[ 'additional_columns'] = someAdditionalColumns
                    
        doc=rel.getDocumentation(striphtml=self.strip_html)
        res={'name':name,
             'fieldtype':field,
             'map':map,
             'doc':doc,
             'indent_level':indent_level}
        return res

    
    
    
    
    def getFieldSpecFromBackAssociation(self, rel, classelement, indent_level=0):
        """Gets the schema field code"""
        multiValued = 0
        obj = rel.fromEnd.obj
        name = rel.fromEnd.getName()
        relname = rel.getName()

        if obj.isAbstract():
            allowed_types= tuple(obj.getGenChildrenNames())
        else:
            allowed_types=(obj.getName(),) + tuple(obj.getGenChildrenNames())

        if int(rel.fromEnd.mult[1]) == -1:
            multiValued = 1
        if name == None:
            name = obj.getName() + '_ref'

        if self.getOption('relation_implementation', rel, 'basic') == \
           'relations'  and (rel.fromEnd.isNavigable or \
                             rel.getTaggedValue('inverse_reference_name')):
            # The relation can override the field
            field = rel.getTaggedValue('relation_field') or \
                  rel.getTaggedValue('field') or \
                  rel.fromEnd.getTaggedValue('field') or \
                  self.typeMap['relation']['field']
            map = self.typeMap['relation']['map'].copy()
            backrelname = rel.getInverseName()
            map.update({'multiValued': multiValued,
                        'relationship': "'%s'" % backrelname})

# ###########################################
# OJO ACV ADDITION
# add inverse relation name
            map.update({'inverse_relationship': "'%s'" % rel.getName(),
                        'inverse_relation_field_name' : "'%s'" % rel.toEnd.getName(),})
            
# ###########################################
# OJO ACV ADDITION
# mark if dependency supplier
            if rel.getTaggedValue( 'dependencySupplier', '') == rel.fromEnd.getName():
                map.update({'dependency_supplier': "True" } )

# ###########################################
# OJO ACV ADDITION
# We want to pass the TGVs for the labels and descriptions 
# of the inverse relation         
#
            someTGVs = rel.getTaggedValues()
            if someTGVs.has_key('inverse_relation_label'):
                rel.fromEnd.taggedValues['label'] = someTGVs['inverse_relation_label']
            if someTGVs.has_key('inverse_relation_label2'):
                rel.fromEnd.taggedValues['label2'] = someTGVs['inverse_relation_label2']
            if someTGVs.has_key('inverse_relation_description'):
                rel.fromEnd.taggedValues['description'] = someTGVs['inverse_relation_description']
            if someTGVs.has_key('inverse_relation_description2'):
                rel.fromEnd.taggedValues['description2'] = someTGVs['inverse_relation_description2']
            if someTGVs.has_key('label'):
                rel.fromEnd.taggedValues['inverse_relation_label'] = someTGVs['label']
            if someTGVs.has_key('label2'):
                rel.fromEnd.taggedValues['inverse_relation_label2'] = someTGVs['label2']
            if someTGVs.has_key('description'):
                rel.fromEnd.taggedValues['inverse_relation_description'] = someTGVs['description']
            if someTGVs.has_key('description2'):
                rel.fromEnd.taggedValues['inverse_relation_description2'] = someTGVs['description2']
            
            map.update(self.getFieldAttributes(rel.fromEnd))

            map.update({'widget':self.getWidget('Reference', rel.fromEnd,
                                                name, classelement)} )
                        
        else:
            # The relation can override the field
            field = rel.getTaggedValue('reference_field') or \
                  rel.toEnd.getTaggedValue('back_reference_field') or \
                  self.typeMap['backreference']['field']
            map = self.typeMap['backreference']['map'].copy()
            if rel.fromEnd.isNavigable and (self.backreferences_support or \
                                            self.getOption('backreferences_support', rel, '0') == '1'):
                map.update({'allowed_types': repr(allowed_types),
                            'multiValued': multiValued,
                            'relationship': "'%s'" % relname})
                map.update(self.getFieldAttributes(rel.fromEnd))
                map.update({'widget':self.getWidget('BackReference', rel.fromEnd,
                                                    name, classelement)})

                if getattr(rel,'isAssociationClass',0):
                    map.update({'referenceClass': "ContentReferenceCreator('%s')"
                                % rel.getName()})
            else:
                return None

        if rel.hasTaggedValue( 'additional_columns'):
            someAdditionalColumns = rel.getTaggedValue( 'additional_columns')
            if someAdditionalColumns:
                map[ 'additional_columns'] = someAdditionalColumns
            
            
        doc = rel.getDocumentation(striphtml=self.strip_html)
        res={'name':name,
             'fieldtype':field,
             'map':map,
             'doc':doc,
             'indent_level':indent_level}
        return res
    
   
    def fClassFieldsOrder(self, theClass):
        if not theClass:
            return []
        
        
        unAllFieldsOrder = []
        unHasTGV = False
        
        for unFieldsOrderIndex in range(0, 10):
            unTaggedValueName = 'fields_order_%d' % unFieldsOrderIndex
            unFieldsOrderString = theClass.getTaggedValue( unTaggedValueName, '')
            if unFieldsOrderString:
                unHasTGV = True
                unFieldsOrder = []
                try:
                    unFieldsOrder = eval( unFieldsOrderString)
                except:
                    None
                if unFieldsOrder:
                    for unFieldName in unFieldsOrder:
                        if unFieldName == 'super':
                            for unaClass in theClass.genParents:
                                unosFields = self.fClassFieldsOrder( unaClass)
                                for unFieldName in unosFields:
                                    if not unFieldName in unAllFieldsOrder:
                                        unAllFieldsOrder.append( unFieldName)
                        elif not unFieldName in unAllFieldsOrder:
                            unAllFieldsOrder.append( unFieldName)
        
        if not unHasTGV:
            for unaClass in theClass.genParents:
                unosFields = self.fClassFieldsOrder( unaClass)
                for unFieldName in unosFields:
                    if not unFieldName in unAllFieldsOrder:
                        unAllFieldsOrder.append( unFieldName)
            
        return unAllFieldsOrder


    def ORIG_fClassFieldsOrder(self, theClass):
        if not theClass:
            return []
        
        someSuperClasses = self.getAllSuperClasses( theClass)
        someSuperClasses.reverse()
        
        unAllFieldsOrder = []
        
        for unaClass in someSuperClasses:
            for unFieldsOrderIndex in range(1, 6):
                unTaggedValueName = 'fields_order_%d' % unFieldsOrderIndex
                unFieldsOrderString = unaClass.getTaggedValue( unTaggedValueName, '')
                if unFieldsOrderString:
                    unFieldsOrder = []
                    try:
                        unFieldsOrder = eval( unFieldsOrderString)
                    except:
                        None
                    if unFieldsOrder:
                        for unFieldName in unFieldsOrder:
                            if not unFieldName in unAllFieldsOrder:
                                unAllFieldsOrder.append( unFieldName)
        
        return unAllFieldsOrder
    
    
    def fSortTraversalConfigs(self, theClass, theTraversalConfigs):
        if not theClass:
            return theTraversalConfigs[:]
        
        if len( theTraversalConfigs) < 2:
            return theTraversalConfigs        
                
        unAllFieldsOrder = self.fClassFieldsOrder( theClass)
        
        if not unAllFieldsOrder:
            return theTraversalConfigs[:]
            
        unosOrderedToGenerate = [ None] * len( unAllFieldsOrder)
        unosUnorderedToGenerate  = [ ]
        for unaTraversalConfig in theTraversalConfigs: 
            unFieldName = ''
            if unaTraversalConfig.has_key( 'aggregation_name'):
                unFieldName = unaTraversalConfig.get( 'aggregation_name', '')
            elif unaTraversalConfig.has_key( 'relation_name'):
                unFieldName = unaTraversalConfig.get( 'relation_name', '')
            if unFieldName:
                if unFieldName in unAllFieldsOrder:
                    unNameIndex = unAllFieldsOrder.index( unFieldName)
                    if unNameIndex >= 0:
                        unosOrderedToGenerate[ unNameIndex] = unaTraversalConfig
                    else:
                        unosUnorderedToGenerate.append( [ unFieldName, unaTraversalConfig, ])   
                else:
                    unosUnorderedToGenerate.append( [ unFieldName, unaTraversalConfig, ])   
                
        unosSortedUnorderedToGenerate = sorted( unosUnorderedToGenerate, lambda unA, otroA : cmp( unA[ 0], otroA[ 0]))
        
        unosSortedToGenerate = []
        unosSortedToGenerate += [ unToGenerate for unToGenerate in unosOrderedToGenerate if unToGenerate]
        unosSortedToGenerate += [ unToGenerate[ 1] for unToGenerate in unosSortedUnorderedToGenerate]
        
        return unosSortedToGenerate
        

        
    
    def fSortFieldsToGenerate(self, theClass, theFieldsToGenerate):
        if not theClass:
            return theFieldsToGenerate[:]
        
        if len( theFieldsToGenerate) < 2:
            return theFieldsToGenerate
                        
        unAllFieldsOrder = self.fClassFieldsOrder( theClass)
        
        if not unAllFieldsOrder:
            return theFieldsToGenerate[:]
            
        unosOrderedToGenerate = [ None] * len( unAllFieldsOrder)
        unosUnorderedToGenerate  = [ ]
        for unFieldToGenerate in theFieldsToGenerate: 
            unNameToGenerate = unFieldToGenerate[ 2]
            if unNameToGenerate in unAllFieldsOrder:
                unNameIndex = unAllFieldsOrder.index( unNameToGenerate)
                if unNameIndex >= 0:
                    unosOrderedToGenerate[ unNameIndex] = unFieldToGenerate
                else:
                    unosUnorderedToGenerate.append( unFieldToGenerate)       
            else:
                unosUnorderedToGenerate.append( unFieldToGenerate)       
            
        
        unosSortedUnorderedToGenerate = sorted( unosUnorderedToGenerate, lambda unA, otroA : cmp( unA[ 2], otroA[ 2]))
        
        unosSortedToGenerate = []
        unosSortedToGenerate += [ unToGenerate for unToGenerate in unosOrderedToGenerate if unToGenerate]
        unosSortedToGenerate += unosSortedUnorderedToGenerate
        
        return unosSortedToGenerate
        
    
# ACVOJO REFACTOR: generate in the order specified in tagged values, if any                     
    def getLocalFieldSpecs(self, element, indent_level=0):
        field_specs = []
        aggregatedClasses = []
        
        unosToGenerate = []
        
        for unAttributeDef in element.getAttributeDefs():
            unosToGenerate.append( [ 'attribute', unAttributeDef,  unAttributeDef.getName(), ])

        for unChild in element.getChildren():
            if not( name in self.reservedAtts):
                unosToGenerate.append( [ 'child', unChild,  unChild.getCleanName(), ])
            
        if utils.toBoolean(self.getOption( 'generate_reference_fields', element, True) ):
            for unaRelation in element.getFromAssociations():
                unosToGenerate.append( [ 'relationfrom', unaRelation,  unaRelation.fromEnd.getName(), ])
            for unaRelation in element.getToAssociations():
                unosToGenerate.append( [ 'relationto', unaRelation,  unaRelation.toEnd.getName(), ])
           
        if utils.toBoolean(self.getOption('generate_subitem_fields', element, True) ):
            for unaAggregationClassAndEnds in self.getAggregationsClassesAndEnds( element):            
                unosToGenerate.append( [ 'subitemfield', unaAggregationClassAndEnds,  unaAggregationClassAndEnds[ 3].getName(), ])
                
                
        unosSortedToGenerate = self.fSortFieldsToGenerate(  element, unosToGenerate)               
            
        for unToGenerate in unosSortedToGenerate: 
            unKindToGenerate = unToGenerate[ 0]
            if unKindToGenerate == 'attribute':
                unAttributeDef = unToGenerate[ 1]
                unName = unAttributeDef.getName()
                unMappedName = utils.mapName( unName)
                field_specs.append(self.getFieldSpecFromAttribute( unAttributeDef, element, indent_level=indent_level+1))

            elif unKindToGenerate == 'child':
                unChild = unToGenerate[ 1]
                unName = unChild.getCleanName()
                unMappedName = unChild.getUnmappedCleanName()
                if unChild.getRef():
                    aggregatedClasses.append( str( unChild.getRef()))
                if child.isIntrinsicType():
                    field_specs.append(self.getFieldSpec( unChild, element, indent_level=indent_level+1))

            elif unKindToGenerate == 'relationfrom':
                unaRelation = unToGenerate[ 1]
                unName = unaRelation.fromEnd.getName()
                field_specs.append(self.getFieldSpecFromAssociation( unaRelation, element, indent_level=indent_level+1))

            elif unKindToGenerate == 'relationto':
                unaRelation = unToGenerate[ 1]
                unName = unaRelation.fromEnd.getName()
                field_specs.append(self.getFieldSpecFromBackAssociation( unaRelation, element, indent_level=indent_level+1))

            elif unKindToGenerate == 'subitemfield':
                unaAggregationClassAndEnds = unToGenerate[ 1]
                field_specs.append( self.getFieldSpecFromAggregation( element, unaAggregationClassAndEnds, indent_level=indent_level+1))   
            
        return field_specs
    
    
    
    
    

    def ORIG_getLocalFieldSpecs(self, element, indent_level=0):
        field_specs = []
        aggregatedClasses = []

        for attrDef in element.getAttributeDefs():
            name = attrDef.getName()
            #if name in self.reservedAtts:
            #    continue
            mappedName = utils.mapName(name)

            field_specs.append(self.getFieldSpecFromAttribute(attrDef, element,
                                                              indent_level=indent_level+1))

        for child in element.getChildren():
            name = child.getCleanName()
            if name in self.reservedAtts:
                continue
            unmappedName = child.getUnmappedCleanName()
            if child.getRef():
                aggregatedClasses.append(str(child.getRef()))

            if child.isIntrinsicType():
                field_specs.append(self.getFieldSpec(child, element,
                                                     indent_level=indent_level+1))

        # only add reference fields if tgv generate_reference_fields
        if utils.toBoolean(
            self.getOption('generate_reference_fields', element, True) ):
            #print 'rels:',element.getName(),element.getFromAssociations()
            # and now the associations
            for rel in element.getFromAssociations():
                name = rel.fromEnd.getName()
                end=rel.fromEnd

                #print 'generating from assoc'
                if name in self.reservedAtts:
                    continue
                field_specs.append(self.getFieldSpecFromAssociation(rel,
                                                                    element,
                                                                    indent_level=indent_level+1))

            #Back References
            for rel in element.getToAssociations():
                name = rel.fromEnd.getName()

                #print "backreference"
                if name in self.reservedAtts:
                    continue
                fc=self.getFieldSpecFromBackAssociation(rel,
                                                        element,
                                                        indent_level=indent_level+1)
                if fc:
                    field_specs.append(fc)

# ACVOJO ADDITION GENERATE FIELDS FOR AGGREGATIONS                     
        # only add computed reference fields for subitems if tgv generate_subitem_fields
        if utils.toBoolean(self.getOption('generate_subitem_fields', element, True) ):
            for unaAggregationClassAndEnds in self.getAggregationsClassesAndEnds( element):            
                field_specs.append( self.getFieldSpecFromAggregation( element, unaAggregationClassAndEnds, indent_level=indent_level+1))   
            
        return field_specs
    
    
    
    

    def getFieldSpecFromAggregation(self, theClass, theAggregationClassAndEnds, indent_level=0):
        """Return the schema field code."""

        anAssociation           = theAggregationClassAndEnds[0]
        aRelatedClass           = theAggregationClassAndEnds[1]
        aFromEnd                = theAggregationClassAndEnds[2]
        aToEnd                  = theAggregationClassAndEnds[3]
        aRelationName           = theAggregationClassAndEnds[4]
        anUpperBound            = aToEnd.getUpperBound()
        aToEndName              = aToEnd.getName()
        #aCapitalizedToEndName   = aToEndName.capitalize()+aToEnd.getName()[1:]
        unExcludeFromViews      = anAssociation.getTaggedValue( 'exclude_from_views', '')
        unNonFrameworkElements  = anAssociation.getTaggedValue( 'non_framework_elements', '') == 'True'
        aMultiplicityHigher     =  int( aToEnd.mult[ 1])
        
        log.debug("Getting the field string from an association.")
        log.debug("Endpoint name: '%s'.", aToEndName)
        log.debug("Relationship name: '%s'.", aRelationName)

        aFieldMap = self.typeMap['computed']['map'].copy()
 
        somePortalTypes = [ ]
        if not  aRelatedClass.isAbstract():
            somePortalTypes.append(  self.fClassMetaTypeOrCleanName( aRelatedClass))        
        someAdditionalClasses = aRelatedClass.getGenChildren(recursive=1)        
        for anAdditionalClass in someAdditionalClasses:
            if not anAdditionalClass.isAbstract():
                somePortalTypes.append( self.fClassMetaTypeOrCleanName( anAdditionalClass))            
        somePortalTypes.sort()
        
        aProductName = theClass.getPackage().getProductName()

        aFieldMap.update({ 
            'computed_types': repr( somePortalTypes), 
            'multiValued': 1, 
        })
        
        if aMultiplicityHigher > 0:
            aFieldMap.update({ 
                'multiplicity_higher': aMultiplicityHigher, 
            })
                 
        if anAssociation.hasTaggedValue( 'factory_views'):
            aFactoryViews = anAssociation.getTaggedValue( 'factory_views')
            if aFactoryViews:
                aFieldMap[ 'factory_views'] = aFactoryViews

        if anAssociation.hasTaggedValue( 'additional_columns'):
            someAdditionalColumnsString   = anAssociation.getTaggedValue( 'additional_columns') or None
            someAdditionalColumns = None
            if someAdditionalColumnsString:
                try:
                    someAdditionalColumns = eval( someAdditionalColumnsString)
                except:
                    someAdditionalColumns = None
            if someAdditionalColumns:
                aFieldMap[ 'additional_columns'] = someAdditionalColumns
                
        aWidget = self.getWidget( 'Computed', anAssociation, anAssociation.getName(), theClass, fieldclassname=None, theIsAggregation=True, theToEndName=aToEndName)
        aFieldMap[ 'widget'] = aWidget
        
        if self.getIsCollection( aRelatedClass):
            aFieldMap[ 'contains_collections'] = 'True'  
        else:
            aFieldMap[ 'contains_collections'] = 'False'        

            
        aFieldMap[ 'non_framework_elements'] = unNonFrameworkElements

        aField = self.typeMap['computed']['field']


        someTGVs = anAssociation.getTaggedValues()
        if someTGVs.has_key('label'):
            aFieldMap['label'] = repr( someTGVs['label'])
        if someTGVs.has_key('description'):
            aFieldMap['description'] = repr( someTGVs['description'])
        if someTGVs.has_key('label2'):
            aFieldMap['label2'] = repr( someTGVs['label2'])
        if someTGVs.has_key('description2'):
            aFieldMap['description2'] = repr( someTGVs['description2'])
            
            

        aFieldMap[ 'owner_class_name'] = '"%s"' % theClass.name
        aFieldMap[ 'expression'] = repr( "context.objectValues(%s)" % repr( somePortalTypes))
        aFieldMap[ 'represents_aggregation'] = True

        aDocumentation = anAssociation.getDocumentation(striphtml=self.strip_html)
        res={'name':        aToEndName,
             'fieldtype':   aField,
             'map':         aFieldMap,
             'doc':         aDocumentation,
             'indent_level':indent_level}
        return res    
    
    
    
    
    
    
    
    

    # Generate get/set/add member functions.
    def generateArcheSchema(self, element, field_specs, base_schema=None, 
                            outfile=None):
        """ generates the Schema """
        asString = False
        if outfile is None:
            outfile = StringIO()
            asString = True
        # first copy fields from other schemas if neccessary.
        startmarker = True
        for attr in element.getAttributeDefs():
            if attr.type.lower() == 'copy':
                if startmarker:
                    startmarker=False
                    print >> outfile, 'copied_fields = {}'
                if (element.hasStereoType(self.cmfmember_stereotype,
                                          umlprofile=self.uml_profile) or
                                          element.hasStereoType(self.remember_stereotype,
                                                                umlprofile=self.uml_profile) ):
                    copy = "BaseMember.content_schema"
                else:
                    copybase_schema = base_schema
                copyfrom = attr.getTaggedValue('copy_from', copybase_schema)
                name = attr.getTaggedValue('source_name',attr.getName())
                print >> outfile, "copied_fields['%s'] = %s['%s'].copy(%s)" % \
                      (attr.getName(), copyfrom, name, name!=attr.getName() \
                       and ("name='%s'" % attr.getName()) or '')
                map = self.getFieldAttributes(attr)
                for key in map:
                    if key.startswith('move:'):
                        continue
                    print >>outfile, "copied_fields['%s'].%s = %s" % \
                          (attr.getName(), key, map[key])
                tgv = attr.getTaggedValues()
                for key in tgv.keys():
                    if not key.startswith('widget:'):
                        continue
                    if key not in self.nonstring_tgvs:
                        tgv[key]=utils.getExpression(tgv[key])
                    print >>outfile, "copied_fields['%s'].widget.%s = %s" % \
                          (attr.getName(), key[7:], tgv[key])
                    # add pot msgid if necessary
                    widgetkey = key[7:]
                    widgetvalue = tgv[key]
                    fieldname = attr.getName()
                    if widgetkey=='label_msgid':
                        self.addMsgid(widgetvalue.strip("'").strip('"'),
                                      tgv.has_key('widget:label') and
                                      tgv['widget:label'].strip("'").strip('"')
                                      or fieldname, element, fieldname)
                    if widgetkey=='description_msgid':
                        self.addMsgid(widgetvalue.strip("'").strip('"'),
                                      tgv.has_key('widget:description') and
                                      tgv['widget:description'].strip("'").strip('"')
                                      or fieldname, element, fieldname)

        fieldsformatted = self.getFieldsFormatted(field_specs) + u'),'        
        print >> outfile, SCHEMA_START
        print >> outfile, fieldsformatted.encode('utf8')

        marshaller=element.getTaggedValue('marshaller') or element.getTaggedValue('marshall')
        if marshaller:
            print >> outfile, 'marshall='+marshaller

        print >> outfile, ')\n'
        if asString:
            return outfile.getvalue()

    def generateFieldMoves(self, outfile, schemaName, field_specs):
        """Generate moveField statements for the schema from field_specs.
        """

        for field_spec in field_specs:
            if type(field_spec) in StringTypes or \
               not field_spec.has_key('map'): 
                continue
            for key in field_spec['map'].keys():
                if key.startswith('move:'):
                    move_key = key[5:]
                    move_from = field_spec['name']
                    move_to = field_spec['map'][key]
                    if move_key == 'before':
                        print >> outfile, "%s.moveField('%s', before=%s)" % (schemaName, move_from, move_to)
                    elif move_key == 'after':
                        print >> outfile, "%s.moveField('%s', after=%s)" % (schemaName, move_from, move_to)
                    elif move_key == 'top' and move_to: # must be true
                        print >> outfile, "%s.moveField('%s', pos='top')" % (schemaName, move_from)
                    elif move_key == 'bottom' and move_to: # must be true
                        print >> outfile, "%s.moveField('%s', pos='bottom')" % (schemaName, move_from)
                    elif move_key == 'pos':
                        print >> outfile, "%s.moveField('%s', pos=%s)" % (schemaName, move_from, move_to)

        print >> outfile

    def generateMethods(self, outfile, element, mode='class'):
        print >> outfile,'    # Methods'

        generatedMethods = []
        allmethnames = [m.getName() for m in element.getMethodDefs(recursive=1)]

        for m in element.getMethodDefs():
            self.generateMethod(outfile, m, element, mode=mode)
            allmethnames.append(m.getName())
            generatedMethods.append(m)

        for interface in element.getRealizationParents():
            meths = [m for m in interface.getMethodDefs(recursive=1)
                     if m.getName() not in allmethnames]
            # Filter out doubles.
            # That can happen if two interfaces both have the same method.
            uniqueMethods = {}
            for method in meths:
                name = method.getName()
                uniqueMethods[name] = method
            meths = uniqueMethods.values()
            # We don't want to extra generate methods
            # that are already defined in the class
            if meths:
                print >> outfile, '\n    # Methods from Interface %s' % \
                      interface.getName()
                for m in meths:
                    self.generateMethod(outfile, m, element, mode=mode)
                    allmethnames.append(m.getName())
                    generatedMethods.append(m)

        # Contains _all_ generated method names
        method_names = [m.getName() for m in generatedMethods]

        #if __init__ has to be generated for tools i want _not_ __init__ to be preserved
        #if it is added to method_names it wont be recognized as a manual method (hacky but works)
        if element.hasStereoType(self.portal_tools, umlprofile=self.uml_profile) and '__init__' not in method_names:
            method_names.append('__init__')

        # As above .. 
        if element.hasStereoType(
            self.remember_stereotype,
            umlprofile=self.uml_profile) and '__call__' not in method_names:
            method_names.append('__call__') 

        #as __init__ above if at_post_edit_script has to be generated for tools
        #I want _not_ at_post_edit_script to be preserved (hacky but works)
        #if it is added to method_names it wont be recognized as a manual method
        if element.hasStereoType(self.portal_tools, umlprofile=self.uml_profile) \
           and 'at_post_edit_script' not in method_names:
            method_names.append('at_post_edit_script')

        if self.method_preservation:
            log.debug("We are to preserve methods, so we're looking for manual methods.")
            cl = self.parsed_class_sources.get(element.getPackage().getFilePath()+'/'+element.name, None)
            if cl:
                log.debug("The class has the following methods: %r.", cl.methods.keys())
                manual_methods = [mt for mt in cl.methods.values() if mt.name not in method_names]
                manual_methods.sort(lambda a,b: cmp(a.start, b.start))  # sort methods according to original order
                log.debug("Found the following manual methods: %r.", manual_methods)
                if manual_methods:
                    print >> outfile, '\n    # Manually created methods\n'

                for mt in manual_methods:
                    declaration = cl.getProtectionDeclaration(mt.getName())
                    if declaration:
                        print >> outfile, declaration
                    print >> outfile, mt.src
                print >> outfile


    def generateMethod(self, outfile, m, klass, mode='class'):
        #ignore actions and views here because they are generated separately
        if m.hasStereoType(['action', 'view', 'form', 'portlet_view',
                            'portlet'], umlprofile=self.uml_profile):
            return

        wrt = outfile.write
        paramstr = ''
        params = m.getParamExpressions()
        if params:
            paramstr = ',' + ','.join(params)

        print >> outfile

        if mode == 'class':
            declaration = self.generateMethodSecurityDeclaration(m)
            if declaration:
                print >> outfile, declaration

        cls = self.parsed_class_sources.get(klass.getPackage().getFilePath() +
                                            '/' + klass.getName(), None)
        if cls:
            method_code = cls.methods.get(m.getName())
        else:
            method_code = None

        if self.method_preservation and method_code:            
            wrt(method_code.src.encode('utf8'))
            # Holly hack: methods ending with a 'pass' command doesn't have
            # an extra blank line after reparsing the code, so we add it
            if method_code.src.split('\n')[-1].strip() == 'pass':
                print >> outfile
        else:
            if mode=='class':
                print >> outfile, '    def %s(self%s):' % (m.getName(), paramstr)
            elif mode=='interface':
                print >> outfile, '    def %s(%s):' % (m.getName(), paramstr[1:])

            code = m.taggedValues.get('code', '')
            doc = m.getDocumentation(striphtml=self.strip_html)
            if doc is not None:
                print >> outfile, utils.indent('"""%s\n"""' % doc, 2,
                                               stripBlank=True)
            if code and mode == 'class':
                print >> outfile, utils.indent('\n'+code, 2)
            else:
                print >> outfile, utils.indent('pass', 2)

        if m.isStatic():
            print >> outfile, '    %s = staticmethod(%s)\n' % (m.getName(),m.getName())

    def generateBaseTestcaseClass(self,element,template):
        log.debug('write runalltests.py and framework.py')
        runalltests=utils.readTemplate('tests/runalltests.py')
        framework=utils.readTemplate('tests/framework.py')

        log.debug('generate base testcase class')
        of=self.makeFile(os.path.join(element.getPackage().getFilePath(),'runalltests.py'))
        of.write(runalltests)
        of.close()

        of=self.makeFile(os.path.join(element.getPackage().getFilePath(),'framework.py'))
        of.write(framework)
        of.close()

        return self.generateTestcaseClass(element,template)

    def generateDocTestcaseClass(self,element,template ):
        #write runalltests.py and framework.py
        testdoc_t=utils.readTemplate('tests/testdoc.txt')
        testdoc=HTML(testdoc_t,{'klass':element })()


        testname=element.getTaggedValue('doctest_name') or element.getCleanName()
        self.makeDir(os.path.join(element.getPackage().getProduct().getFilePath(),'doc'))
        docfile=os.path.join(element.getPackage().getProduct().getFilePath(),'doc','%s.txt' % testname)
        if not self.readFile(docfile):
            of=self.makeFile(docfile)
            of.write(testdoc)
            of.close()

        init='#'
        of=self.makeFile(os.path.join(element.getPackage().getProduct().getFilePath(),'doc','__init__.py' ))

        of.write(init)
        of.close()


        return self.generateTestcaseClass(element,template,testname=testname)

    def generateTestcaseClass(self,element,template,**kw):
        log.info("%sGenerating testcase '%s'.",
                 '    '*self.infoind, element.getName())

        assert element.hasStereoType('plone_testcase', umlprofile=self.uml_profile) or element.getCleanName().startswith('test'), \
               "names of test classes _must_ start with 'test', but this class is named '%s'" % element.getCleanName()

        assert element.getPackage().getCleanName() == 'tests', \
               "testcase classes only make sense inside a package called 'tests' \
               but this class is named '%s' and located in package '%s'" % (element.getCleanName(),element.getPackage().getCleanName())

        if element.getGenParents():
            parent = element.getGenParents()[0]
        else:
            parent = None

        return BaseGenerator.generatePythonClass(self, element, template, parent=parent, nolog=True, **kw)

    def generateWidgetClass(self, element, template, zptname='widget.pt'):
        log.info("%sGenerating widget '%s'.",
                 "    "*self.infoind, element.getName())

        # Generate the template
        macroname = '%s.pt' % element.getTaggedValue('macro',
                                                     element.getCleanName())
        templpath = os.path.join(self.getSkinPath(element), macroname)
        fieldpt = self.readFile(templpath)
        if not fieldpt:
            templ = utils.readTemplate(zptname)
            d = {
                'klass': element,
                'generator': self,
                'parsed_class': element.parsed_class,
                'builtins': __builtins__,
                'utils': utils,
            }
            d.update(__builtins__)
            zptcode = HTML(templ,d)()

            fp = self.makeFile(templpath)
            print >> fp, zptcode
            fp.close()

        # And now the python code
        if element.getGenParents():
            parent = element.getGenParents()[0]
            parentname = parent.getCleanName()
        else:
            parent = None
            parentname = 'TypesWidget'

        return BaseGenerator.generatePythonClass(self, element, template,
                                                 parent=parent,
                                                 parentname=parentname)

    def generateFieldClass(self, element, template):
        log.info("%sGenerating field: '%s'.",
                 '    '*self.infoind, element.getName())

        # Generate the python code
        if element.getGenParents():
            parent = element.getGenParents()[0]
            parentname = parent.getCleanName()
        else:
            if element.getAttributeDefs():
                parent = None
                parentname = 'CompoundField'
            else:
                parent = None
                parentname = 'ObjectField'

        widgets = element.getClientDependencyClasses(targetStereotypes=['widget'])
        if widgets:
            widget = widgets[0]
            widgetname = widget.getCleanName()
        else:
            widget = None
            widgetname = None
        klass = BaseGenerator.generatePythonClass(self, element, template,
                                                  parent=parent,
                                                  parentname=parentname,
                                                  widget=widget,
                                                  widgetname=widgetname)
        return klass

    def elementIsFolderish(self, element):
        log.debug("Determining whether the element '%s' is folderish...",
                  element.name)
        # This entire method hould probably be moved off to the element classes.
        # Copy-pasted from generateArchetypesClass()...
        aggregatedClasses = element.getRefs() + element.getSubtypeNames(recursive=0,filter=['class'])
        log.debug("Found %s aggregated classes.",
                  len(aggregatedClasses))
        #also check if the parent classes can have subobjects
        baseaggregatedClasses=[]
        for b in element.getGenParents():
            baseaggregatedClasses.extend(b.getRefs())
            baseaggregatedClasses.extend(b.getSubtypeNames(recursive=1))
        log.debug("Found %s parents with aggregated classes.",
                  len(baseaggregatedClasses))
        aggregatedInterfaces=self.getAggregatedInterfaces(element, includeBases=1)
        log.debug("Found %s aggregated interfaces.",
                  len(aggregatedInterfaces))
        log.debug("Based on this info and the tagged value 'folderish' or the "
                  "stereotypes 'folder' and 'ordered', we look if it's a folder.")
        isFolderish = aggregatedInterfaces or aggregatedClasses or baseaggregatedClasses or \
                    utils.isTGVTrue(element.getTaggedValue('folderish')) or \
                    element.hasStereoType(self.folder_stereotype, umlprofile=self.uml_profile)
        log.debug("End verdict on folderish character: %s.",
                  bool(isFolderish))
        return bool(isFolderish)

    def getAggregatedInterfaces(self,element,includeBases=1):
        res = element.getAggregatedClasses(recursive=0,filter=['interface'])
        if includeBases:
            for b in element.getGenParents(recursive=1):
                res.extend(self.getAggregatedInterfaces(b,includeBases=0))

        return res

    def getArchetypesBase(self, element, parentnames, parent_is_archetype):
        """ find bases (baseclass and baseschema) and return a
            3-tuple (baseclass, baseschema, parentnames)

            Normally a one of the Archetypes base classes are set.
            if you dont want it set the TGV to zero '0'
        """
        if self.elementIsFolderish(element):
            # folderish

            if element.hasStereoType('ordered', umlprofile=self.uml_profile):
                baseclass ='OrderedBaseFolder'
                baseschema ='OrderedBaseFolderSchema'
            elif element.hasStereoType(['large','btree'], umlprofile=self.uml_profile):
                baseclass ='BaseBTreeFolder'
                baseschema ='BaseBTreeFolderSchema'
            else:
                baseclass ='BaseFolder'
                baseschema ='BaseFolderSchema'

            # XXX: How should <<ordered>> affect this?
            if self.i18n_content_support in self.i18n_at and element.isI18N():
                baseclass = 'I18NBaseFolder'
                baseschema = 'I18NBaseFolderSchema'

            if element.getTaggedValue('folder_base_class'):
                raise ValueError, "DEPRECATED: Usage of Tagged Value "\
                      "folder_base_class' in class %s" % element.getCleanName
        else:
            # contentish
            baseclass = 'BaseContent'
            baseschema = 'BaseSchema'
            if self.i18n_content_support in self.i18n_at and element.isI18N():
                baseclass ='I18NBaseContent'
                baseschema ='I18NBaseSchema'

        # if a parent is already an archetype we dont need a baseschema!
        if parent_is_archetype:
            baseclass = None

        # CMFMember support
        if element.hasStereoType(self.cmfmember_stereotype, umlprofile=self.uml_profile):
            baseclass = 'BaseMember.Member'
            baseschema = 'BaseMember.id_schema'

        #njj # remember support
        #njj if element.hasStereoType(self.remember_stereotype, umlprofile=self.uml_profile):
        #njj     baseclass = 'BaseMember'
        #njj     baseschema = 'BaseMember.schema'

        ## however: tagged values have priority
        # tagged values for base-class overrule
        if element.getTaggedValue('base_class'):
            baseclass = element.getTaggedValue('base_class')

        # tagged values for base-schema overrule
        if element.getTaggedValue('base_schema'):
            baseschema = element.getTaggedValue('base_schema')

        # [optilude] Ignore the standard class if this is an mixin
        # [jensens] An abstract class might have a base_class!
        if baseclass and not utils.isTGVFalse(element.getTaggedValue('base_class',1)) \
           and not element.hasStereoType('mixin', umlprofile=self.uml_profile):
            baseclasses = baseclass.split(',')
            if utils.isTGVTrue(element.getTaggedValue('parentclass_first')) or utils.isTGVTrue(element.getTaggedValue('parentclasses_first')):
                parentnames = parentnames + baseclasses #this way base_class is used after generalization parents
            else:
                parentnames = baseclasses + parentnames #this way base_class is used before anything else
        parentnames = [klass.strip() for klass in parentnames]

        #remove double entries in parentnames
        #this could be needed if base_class is one of the parents in parentnames...
        parentnames_ordered_set = []
        for klass in parentnames:
            if not klass in parentnames_ordered_set:
                parentnames_ordered_set.append(klass)
        parentnames = parentnames_ordered_set
        return baseclass, baseschema, parentnames

    def generateArchetypesClass(self, element, **kw):
        """this is the all singing all dancing core generator logic for a
           full featured Archetypes class
        """
        log.info("%sGenerating class '%s'.",
                 '    '*self.infoind, element.getName())

        name = element.getCleanName()

        # Prepare file
        outfile = StringIO()
        wrt = outfile.write

        # dealing with creation-permissions and -roles for this type
        klass = element.getCleanName()
        if self.detailed_created_permissions:
            creation_permission = "'Add %s Content'" % klass
            # TODO: looks a bit shitty, ^^^^^. 'Add Event Content'...
            # 'Add MyProduct Content' is ok, but the prefixed way
            # 'Myproduct: Add Event' is preferrable to the above
            # version.
            # As luck would have it, there was a typo
            # --detailed-created-permissions, so I fixed the non-typo
            # --detailed-creation-permissions up with the new
            # generated syntax.
        elif self.getOption('detailed_creation_permissions', element, None):
            product = element.getPackage().getProduct().getCleanName()
            creation_permission = "'%s: Add %s'" % (product, klass)
        else:
            creation_permission = None
        creation_roles = "('Manager', 'Owner')"
        cpfromoption = self.getOption('creation_permission', element, None)
        if cpfromoption:
            creation_permission = self.processExpression(cpfromoption)
        crfromoption = self.getOption('creation_roles', element, None)
        if crfromoption:
            creation_roles = self.processExpression(crfromoption)

        # generate header
        wrt(self.generateHeader(element))

        # generate basic imports

        dependentImports = self.generateDependentImports(element)
        if dependentImports.strip():
            log.debug("Generating dependent imports...")
            wrt(dependentImports)

        additionalImports = self.generateAdditionalImports(element)
        if additionalImports:
            log.debug("Generating additional imports...")
            wrt(additionalImports)

        # imports needed for remember subclassing
        if element.hasStereoType(self.remember_stereotype,
                                 umlprofile=self.uml_profile):
            wrt(REMEMBER_IMPORTS)
            # and set the add content permission to what remember needs
            creation_permission = u'ADD_MEMBER_PERMISSION'
            creation_roles = None

        # imports needed for CMFMember subclassing
        if element.hasStereoType(self.cmfmember_stereotype,
                                 umlprofile=self.uml_profile):
            wrt(CMFMEMBER_IMPORTS)
            # and set the add content permission to what CMFMember needs
            creation_permission = u'ADD_MEMBER_PERMISSION'
            creation_roles = None

        # imports needed for optional support of SQLStorage
        if utils.isTGVTrue(self.getOption('sql_storage_support',element,0)):
            wrt('from Products.Archetypes.SQLStorage import *\n')

        # import Product config.py
        wrt(TEMPLATE_CONFIG_IMPORT % {
            'module': element.getRootPackage().getProductModuleName()})

        # imports by tagged values
        additionalImports = self.getImportsByTaggedValues(element)
        if additionalImports:
            wrt(u"# additional imports from tagged value 'import'\n")
            wrt(additionalImports)
            wrt(u'\n')

        # CMFMember needs a special factory method
        if element.hasStereoType(self.cmfmember_stereotype,
                                 umlprofile=self.uml_profile):
            wrt(CMFMEMBER_ADD % {
                'module': element.getRootPackage().getProductModuleName(),
                'prefix': self.prefix,
                'name': name})
        # I don't think this is needed for remember, since instances of
        # member will be added by the membership tool 

        # Normally, archgenxml also looks at the parents of the
        # current class for allowed subitems. Likewise, subclasses of
        # classes allowed as subitems are also allowed on this
        # class. Classic polymorphing. In case this isn't desired, set
        # the tagged value 'disable_polymorphing' to 1.
        disable_polymorphing = element.getTaggedValue('disable_polymorphing', 0)
        if disable_polymorphing:
            recursive = 0
        else:
            recursive = 1

        aggregatedClasses = element.getRefs() + \
                          element.getSubtypeNames(recursive=recursive,
                                                  filter=['class'])
        # We *do* want the resursive=0 below, though!
        aggregatedInterfaces = element.getRefs() + \
                             element.getSubtypeNames(recursive=0,
                                                     filter=['interface'])
        if element.getTaggedValue('allowed_content_types'):
            aggregatedClasses = [e for e in aggregatedClasses]
            for e in element.getTaggedValue('allowed_content_types').split(','):
                e = e.strip()
                if e not in aggregatedClasses:
                    aggregatedClasses.append(e)

# ############################
# ACV OJO ADDITION 
# We want to be able to exclude some type names
# from the list of allowed_content_types aggregated in the model
#                     
        if element.getTaggedValue('forbidden_content_types'):
            aggregatedClasses = [e for e in aggregatedClasses]
            for e in element.getTaggedValue('forbidden_content_types').split(','):
                e = e.strip()
                if e in aggregatedClasses:
                    aggregatedClasses.remove(e)                    

                    
                    
                    
                 
            
                    
                    
                    
        # if it's a derived class check if parent has stereotype 'archetype'
        parent_is_archetype = False
        for p in element.getGenParents():
            parent_is_archetype = parent_is_archetype or \
                                p.hasStereoType(self.archetype_stereotype,
                                                umlprofile=self.uml_profile)

        # also check if the parent classes can have subobjects
        baseaggregatedClasses = []
        for b in element.getGenParents():
            baseaggregatedClasses.extend(b.getRefs())
            baseaggregatedClasses.extend(b.getSubtypeNames(recursive=1))

        #also check if the interfaces used can have subobjects
        baseaggregatedInterfaces = []
        for b in element.getGenParents(recursive=1):
            baseaggregatedInterfaces.extend(b.getSubtypeNames(recursive=1,filter=['interface']))

        parentnames = [p.getCleanName() for p in element.getGenParents()]
        additionalParents = element.getTaggedValue('additional_parents')
        if additionalParents:
            parentnames = additionalParents.split(',') + list(parentnames)

        # find base
        baseclass, baseschema, parentnames = self.getArchetypesBase(element, parentnames, parent_is_archetype)

        # Remark: CMFMember support includes VariableSchema support
        # Remark Reinout: since cmfmember 1.1, there's no more
        # variableschema support.
        # njj: Punt on this for now as far as remember is concerned.
        if element.hasStereoType(self.variable_schema,
                                 umlprofile=self.uml_profile):
            if element.hasStereoType(self.cmfmember_stereotype,
                                     umlprofile=self.uml_profile):
                log.warn("Adding VariableSchema to cmfmember, be careful "
                         "as cmfmember 1.0 already includes it.")
            # Including it by default anyway, since 1.4.0/dev.
            parentnames.insert(0, 'VariableSchemaSupport')

        if element.hasStereoType(self.remember_stereotype, umlprofile=self.uml_profile):
            parentnames.insert(0, 'BaseMember')

        # Interface aggregation
        if self.getAggregatedInterfaces(element):
            parentnames.insert(0, 'AllowedTypesByIfaceMixin')

        # a tool needs to be a unique object
        if element.hasStereoType(self.portal_tools, umlprofile=self.uml_profile):
            print >> outfile, TEMPL_TOOL_HEADER
            parentnames.insert(0, 'UniqueObject')

        parents = ', '.join(parentnames)

        # protected section
        self.generateProtectedSection(outfile, element, 'module-header')

        # generate local Schema from local field specifications
        field_specs = self.getLocalFieldSpecs(element)
        self.generateArcheSchema(element, field_specs, baseschema, outfile)

        # protected section
        self.generateProtectedSection(outfile, element, 'after-local-schema')

        # generate complete Schema
        # prepare schema as class attribute
        parent_schema = ["getattr(%s, 'schema', Schema(()))" % p.getCleanName()
                         for p in element.getGenParents()
                         if not p.hasStereoType(self.python_stereotype,
                                                umlprofile=self.uml_profile)]

        if (parent_is_archetype 
            and not element.hasStereoType(
                self.cmfmember_stereotype, umlprofile=self.uml_profile)
                and not element.hasStereoType(
                    self.remember_stereotype, umlprofile=self.uml_profile)):
            schema = parent_schema
        else:
            # [optilude] Ignore baseschema in abstract mixin classes
            if element.isAbstract():
                schema = parent_schema
            else:
                schema = [baseschema] + parent_schema

        if element.hasStereoType(self.cmfmember_stereotype, umlprofile=self.uml_profile):
            for addschema in ['contact_schema', 'plone_schema', 'plone_2_1_schema',
                              'security_schema', 'login_info_schema',]:
                if utils.isTGVTrue(element.getTaggedValue(addschema, '1')):
                    schema.append('BaseMember.%s' % addschema)
            if utils.isTGVTrue(element.getTaggedValue(addschema, '1')):
                schema.append('ExtensibleMetadata.schema')

        if element.hasStereoType(self.remember_stereotype, umlprofile=self.uml_profile):
            schema.append('BaseMember.schema')
            schema.append('ExtensibleMetadata.schema')

        # own schema overrules base and parents
        schema += ['schema']

        schemaName = '%s_schema' % name
        print >> outfile, utils.indent(schemaName + ' = ' + ' + \\\n    '.join(['%s.copy()' % s for s in schema]), 0)

        # move fields based on move: tagged values
        self.generateFieldMoves(outfile, schemaName, field_specs)

        # protected section
        self.generateProtectedSection(outfile, element, 'after-schema')

        if not element.isComplex():
            print "I: stop complex: ", element.getName()
            return outfile.getvalue()
        if element.getType() in AlreadyGenerated:
            print "I: stop already generated:", element.getName()
            return outfile.getvalue()
        AlreadyGenerated.append(element.getType())

        if self.ape_support:
            print >> outfile, TEMPL_APE_HEADER % {'class_name': name}

        # [optilude] It's possible parents may become empty now...
        if parents:
            parents = "(%s)" % (parents,)
        else:
            parents = ''
        # [optilude] ... so we can't have () around the last %s
        classDeclaration = 'class %s%s%s:\n' % (self.prefix, name, parents)

        wrt(classDeclaration)

        doc = element.getDocumentation(striphtml=self.strip_html)
        parsedDoc = ''
        if element.parsed_class:
            parsedDoc = element.parsed_class.getDocumentation()
        if doc:
            print >> outfile, utils.indent('"""%s\n"""' % doc, 1,
                                           stripBlank=True)
        elif parsedDoc:
            # Bit tricky, parsedDoc is already indented...
            print >> outfile, '    """%s"""' % parsedDoc
        else:
            print >> outfile, '    """\n    """'

        print >> outfile, utils.indent('security = ClassSecurityInfo()',1)

        print >> outfile, self.generateImplements(element, parentnames)

        header = element.getTaggedValue('class_header')
        if header:
            print >> outfile,utils.indent(header, 1)

        archetype_name = element.getTaggedValue('archetype_name') or \
                       element.getTaggedValue('label')
        if not archetype_name:
            archetype_name = name
        if type(archetype_name) != types.UnicodeType:
            archetype_name = archetype_name.decode('utf8')
        portaltype_name = element.getTaggedValue('portal_type') or name

        # [optilude] Only output portal type and AT name if it's not an abstract
        # mixin
        if not element.isAbstract():
            print >> outfile, (CLASS_ARCHETYPE_NAME % archetype_name).encode('utf8')
            print >> outfile, CLASS_META_TYPE % name
            print >> outfile, CLASS_PORTAL_TYPE % portaltype_name

            
            
        # ACV To add meta attributes identifying fields that hold creation and change auditing info
        someAllAttributes = self.getAllAttributeDefs( element)
        
        unCreationDateAttribute = None
        unCreationUserAttribute = None
        unModificationDateAttribute = None
        unModificationUserAttribute = None
        unDeletionDateAttribute = None
        unDeletionUserAttribute = None
        unIsInactiveAttribute = None
        unChangeCounterAttribute = None
        unSourcesCountersAttribute = None
        unChangeLogAttribute = None

        
        # ACV 20091001 To add meta attributes identifying fields that hold versioning and translation
        unInterVersionUIDAttribute = None
        unVersionAttribute  = None
        unVersionStorageAttribute  = None
        unVersionCommentAttribute  = None
        unVersionCommentStorageAttribute  = None
        unLanguageAttribute = None
        unIsTranslationAttribute = None
        unInterTranslationUIDAttribute = None
        unFieldsPendingTranslationAttribute = None
        unFieldsPendingRevisionAttribute = None
        
        
        for anAttribute in someAllAttributes:
            # ACV To add meta attributes identifying fields that hold creation and change auditing info
            if unCreationDateAttribute and unCreationUserAttribute and unModificationDateAttribute and unModificationUserAttribute and unDeletionDateAttribute and unDeletionUserAttribute and unIsInactiveAttribute and unChangeCounterAttribute and unSourcesCountersAttribute and unChangeLogAttribute and \
                unInterVersionUIDAttribute and unVersionAttribute and unVersionCommentAttribute and unLanguageAttribute and \
                unIsTranslationAttribute and unInterTranslationUIDAttribute and unFieldsPendingTranslationAttribute and unFieldsPendingRevisionAttribute:
                break
            
            if anAttribute.getTaggedValue( 'is_creation_date', '').lower() == 'true':
                if not unCreationDateAttribute:
                    unCreationDateAttribute = anAttribute
                continue
                
            if anAttribute.getTaggedValue( 'is_creation_user', '').lower() == 'true':
                if not unCreationUserAttribute:
                    unCreationUserAttribute = anAttribute
                continue
                
            if anAttribute.getTaggedValue( 'is_modification_date', '').lower() == 'true':
                if not unModificationDateAttribute:
                    unModificationDateAttribute = anAttribute
                continue
                
            if anAttribute.getTaggedValue( 'is_modification_user', '').lower() == 'true':
                if not unModificationUserAttribute:
                    unModificationUserAttribute = anAttribute
                continue
                
            if anAttribute.getTaggedValue( 'is_deletion_date', '').lower() == 'true':
                if not unDeletionDateAttribute:
                    unDeletionDateAttribute = anAttribute
                continue
                
            if anAttribute.getTaggedValue( 'is_deletion_user', '').lower() == 'true':
                if not unDeletionUserAttribute:
                    unDeletionUserAttribute = anAttribute
                continue
                
            if anAttribute.getTaggedValue( 'is_inactive_state', '').lower() == 'true':
                if not unIsInactiveAttribute:
                    unIsInactiveAttribute = anAttribute
                continue
            
            if anAttribute.getTaggedValue( 'is_change_counter', '').lower() == 'true':
                if not unChangeCounterAttribute:
                    unChangeCounterAttribute = anAttribute
                continue
            
            if anAttribute.getTaggedValue( 'is_sources_counters', '').lower() == 'true':
                if not unSourcesCountersAttribute:
                    unSourcesCountersAttribute = anAttribute
                continue
            
            if anAttribute.getTaggedValue( 'is_change_log', '').lower() == 'true':
                if not unChangeLogAttribute:
                    unChangeLogAttribute = anAttribute
                continue
            
            
            
            # ACV 20091001 To add meta attributes identifying fields that hold versioning and translation
            if anAttribute.getTaggedValue( 'is_inter_version', '').lower() == 'true':
                if not unInterVersionUIDAttribute:
                    unInterVersionUIDAttribute = anAttribute
                continue
            
            if anAttribute.getTaggedValue( 'is_version', '').lower() == 'true':
                if not unVersionAttribute:
                    unVersionAttribute = anAttribute
                continue
            
            if anAttribute.getTaggedValue( 'is_version_storage', '').lower() == 'true':
                if not unVersionStorageAttribute:
                    unVersionStorageAttribute = anAttribute
                continue
            
            if anAttribute.getTaggedValue( 'is_version_comment', '').lower() == 'true':
                if not unVersionCommentAttribute:
                    unVersionCommentAttribute = anAttribute
                continue
            
            if anAttribute.getTaggedValue( 'is_version_comment_storage', '').lower() == 'true':
                if not unVersionCommentStorageAttribute:
                    unVersionCommentStorageAttribute = anAttribute
                continue
            
            if anAttribute.getTaggedValue( 'is_language', '').lower() == 'true':
                if not unLanguageAttribute:
                    unLanguageAttribute = anAttribute
                continue
            
            if anAttribute.getTaggedValue( 'is_translation', '').lower() == 'true':
                if not unIsTranslationAttribute:
                    unIsTranslationAttribute = anAttribute
                continue
            
            if anAttribute.getTaggedValue( 'is_inter_translation', '').lower() == 'true':
                if not unInterTranslationUIDAttribute:
                    unInterTranslationUIDAttribute = anAttribute
                continue
            
            if anAttribute.getTaggedValue( 'is_fields_pending_translation', '').lower() == 'true':
                if not unFieldsPendingTranslationAttribute:
                    unFieldsPendingTranslationAttribute = anAttribute
                continue
            
            if anAttribute.getTaggedValue( 'is_fields_pending_revision', '').lower() == 'true':
                if not unFieldsPendingRevisionAttribute:
                    unFieldsPendingRevisionAttribute = anAttribute
                continue
            
            
        # ACV To add meta attributes identifying fields that hold creation and change auditing info
        if unCreationDateAttribute or unCreationUserAttribute or unModificationDateAttribute or unModificationUserAttribute or unDeletionDateAttribute or unDeletionUserAttribute or unIsInactiveAttribute or unChangeCounterAttribute or unChangeLogAttribute:
            print >> outfile, "\n\n    # Change Audit fields\n"
            
            if unCreationDateAttribute:
                print >> outfile, ("    creation_date_field = '%s'" % unCreationDateAttribute.name)
                
            if unCreationDateAttribute:
                print >> outfile, ("    creation_user_field = '%s'" % unCreationUserAttribute.name)
                
            if unModificationDateAttribute:
                print >> outfile, ("    modification_date_field = '%s'" % unModificationDateAttribute.name)
                
            if unModificationUserAttribute:
                print >> outfile, ("    modification_user_field = '%s'" % unModificationUserAttribute.name)
                
            if unDeletionDateAttribute:
                print >> outfile, ("    deletion_date_field = '%s'" % unDeletionDateAttribute.name)
                
            if unDeletionDateAttribute:
                print >> outfile, ("    deletion_user_field = '%s'" % unDeletionUserAttribute.name)
                            
            if unIsInactiveAttribute:
                print >> outfile, ("    is_inactive_field = '%s'" % unIsInactiveAttribute.name)
                
            if unChangeCounterAttribute:
                print >> outfile, ("    change_counter_field = '%s'" % unChangeCounterAttribute.name)
                
            if unSourcesCountersAttribute:
                print >> outfile, ("    sources_counters_field = '%s'" % unSourcesCountersAttribute.name)
    
            if unChangeLogAttribute:
                print >> outfile, ("    change_log_field = '%s'" % unChangeLogAttribute.name)
            
            print >> outfile, "\n\n"
           
            
        # 20091001 To add meta attributes identifying fields that hold versioning and translation
        if unInterVersionUIDAttribute or unVersionAttribute or unVersionStorageAttribute or unVersionCommentAttribute or unVersionCommentStorageAttribute or unLanguageAttribute or unIsTranslationAttribute or unFieldsPendingTranslationAttribute or unFieldsPendingRevisionAttribute:
            print >> outfile, "\n    # Versioning and Translation fields\n"
            
            if unInterVersionUIDAttribute:
                print >> outfile, ("    inter_version_field = '%s'" % unInterVersionUIDAttribute.name)
            
            if unVersionAttribute:
                print >> outfile, ("    version_field = '%s'" % unVersionAttribute.name)
            
            if unVersionStorageAttribute:
                print >> outfile, ("    version_storage_field = '%s'" % unVersionStorageAttribute.name)
            
            if unVersionCommentAttribute:
                print >> outfile, ("    version_comment_field = '%s'" % unVersionCommentAttribute.name)
                
            if unVersionCommentStorageAttribute:
                print >> outfile, ("    version_comment_storage_field = '%s'" % unVersionCommentStorageAttribute.name)

            if unInterTranslationUIDAttribute:
                print >> outfile, ("    inter_translation_field = '%s'" % unInterTranslationUIDAttribute.name)
            
            if unLanguageAttribute:
                print >> outfile, ("    language_field = '%s'" % unLanguageAttribute.name)
                
            if unIsTranslationAttribute:
                print >> outfile, ("    is_translation_field = '%s'" % unIsTranslationAttribute.name)
                
            if unFieldsPendingTranslationAttribute:
                print >> outfile, ("    fields_pending_translation_field = '%s'" % unFieldsPendingTranslationAttribute.name)
                
            if unFieldsPendingRevisionAttribute:
                print >> outfile, ("    fields_pending_revision_field = '%s'" % unFieldsPendingRevisionAttribute.name)
                
            print >> outfile, "\n\n"
        # END ACV To add meta attributes identifying fields that hold creation and change auditing info
        # END ACV 20091001 To add meta attributes identifying fields that hold versioning and translation
            
            
        # ACV 20091001 To add meta attributes identifying fields that hold traceability links
        unVersioningLinkFields   = element.getTaggedValue( 'versioning_link_fields', '')
        unTranslationLinkFields  = element.getTaggedValue( 'translation_link_fields', '')
        unUsageLinkFields        = element.getTaggedValue( 'usage_link_fields', '')
        unDerivationLinkFields   = element.getTaggedValue( 'derivation_link_fields', '')

        if unVersioningLinkFields or unTranslationLinkFields or unUsageLinkFields or unDerivationLinkFields:
            print >> outfile, "\n    # Traceability links fields\n"
        
            if unVersioningLinkFields:
                print >> outfile, ("    versioning_link_fields = %s" % unVersioningLinkFields)
                
            if unTranslationLinkFields:
                print >> outfile, ("    translation_link_fields = %s" % unTranslationLinkFields)
                
            if unUsageLinkFields:
                print >> outfile, ("    usage_link_fields = %s" % unUsageLinkFields)
                
            if unDerivationLinkFields:
                print >> outfile, ("    derivation_link_fields = %s" % unDerivationLinkFields)
                
            print >> outfile, "\n\n"
            

      
            
        # Let's see if we have to set use_folder_tabs to 0.
        if utils.isTGVTrue(element.getTaggedValue('hide_folder_tabs', False)):
            print >> outfile, CLASS_FOLDER_TABS % 0

        #allowed_content_classes
        parentAggregates = ''
             
        if utils.isTGVTrue(element.getTaggedValue('inherit_allowed_types', \
                                                  True)) and element.getGenParents():
            act = []
            for gp in element.getGenParents():
                if gp.hasStereoType(self.python_stereotype,
                                    umlprofile=self.uml_profile):
                    continue
                pt = gp.getTaggedValue('portal_type', None)
                if pt is not None:
                    act.append(pt)
                else:
                    act.append(gp.getCleanName())
            act = ["list(getattr(%s, 'allowed_content_types', []))" % i
                   for i in act]
            if act:
                parentAggregates = ' + ' + ' + '.join(act)
        print >> outfile, CLASS_ALLOWED_CONTENT_TYPES % \
              (repr(aggregatedClasses),parentAggregates)

        # allowed_interfaces
        parentAggregatedInterfaces = ''
        if utils.isTGVTrue(element.getTaggedValue('inherit_allowed_types', \
                                                  True)) and element.getGenParents():
            pattern = "getattr(%s, 'allowed_interfaces', [])"
            extras = ' + '.join([pattern % p.getCleanName()
                                 for p in element.getGenParents()])
            parentAggregatedInterfaces = '+ ' + extras

        if aggregatedInterfaces or baseaggregatedInterfaces:
            print >> outfile, CLASS_ALLOWED_CONTENT_INTERFACES % \
                  (','.join(aggregatedInterfaces), parentAggregatedInterfaces)

        # FTI as attributes on class
        # [optilude] Don't generate FTI for abstract mixins
        if not element.isAbstract():
            fti=self.generateFti(element,aggregatedClasses)
            print >> outfile,fti
        # But *do* add the actions, views, etc.
        actions_views = self.generateActionsAndViews(element,
                                                     aggregatedClasses)
        if actions_views:
            print >> outfile, actions_views

            
            
        # #############################################################################    
        # ACV 20090926 to add generation of aliases (view method names to other view method names) 
        someAliases = self.generateAliases(element,)
        if someAliases:
            print >> outfile, someAliases

        # ACV
        # #############################################################################    

        
            
            
             
            
        # _at_rename_after_creation
        rename_after_creation = self.getOption('rename_after_creation',
                                               element, default=True)
        if rename_after_creation:
            print >> outfile, CLASS_RENAME_AFTER_CREATION % \
                  (utils.isTGVTrue(rename_after_creation) and 'True' or 'False')

        # schema attribute
        wrt(utils.indent('schema = %s' % schemaName, 1) + '\n\n')

        # Set base_archetype for remember
        if element.hasStereoType(self.remember_stereotype, umlprofile=self.uml_profile):
            wrt(utils.indent("base_archetype = %s" % baseclass, 1) + '\n\n')

        self.generateProtectedSection(outfile, element, 'class-header', 1)

        # tool __init__ and at_post_edit_script
        if element.hasStereoType(self.portal_tools, umlprofile=self.uml_profile):
            tool_instance_name = element.getTaggedValue('tool_instance_name') \
                               or 'portal_%s' % element.getName().lower()
            print >> outfile, TEMPL_CONSTR_TOOL % (baseclass,tool_instance_name,archetype_name)
            self.generateProtectedSection(outfile, element,
                                          'constructor-footer', 2)
            print >> outfile, TEMPL_POST_EDIT_METHOD_TOOL
            self.generateProtectedSection(outfile, element,
                                          'post-edit-method-footer', 2)
            print >> outfile

        # Remember __call__
        if element.hasStereoType(self.remember_stereotype, umlprofile=self.uml_profile):
            print >> outfile, REMEMBER_CALL
            print >> outfile

        self.generateMethods(outfile, element)

        # [optilude] Don't do modify FTI for abstract mixins
        if not element.isAbstract():
            print >> outfile, self.generateModifyFti(element)

        # [optilude] Don't register type for abstract classes or tools
        if not (element.isAbstract() or element.hasStereoType('mixin',
                                                              umlprofile=self.uml_profile)):
            wrt(REGISTER_ARCHTYPE % name)

        # ATVocabularyManager: registration of class
        if element.hasStereoType(self.vocabulary_item_stereotype,
                                 umlprofile=self.uml_profile) and not element.isAbstract():
            # XXX TODO: fetch container_class - needs to be refined:
            # check if parent has vocabulary_container_stereotype and use its
            # name as container
            # else check for TGV vocabulary_container
            # fallback: use SimpleVocabulary
            container = element.getTaggedValue('vocabulary:portal_type',
                                               'SimpleVocabulary')
            wrt(REGISTER_VOCABULARY_ITEM % (name, container))
        if element.hasStereoType(self.vocabulary_container_stereotype,
                                 umlprofile=self.uml_profile):
            wrt(REGISTER_VOCABULARY_CONTAINER % name)

        wrt('# end of class %s\n\n' % name)

        self.generateProtectedSection(outfile, element, 'module-footer')

        ## handle add content permissions
        if not element.hasStereoType(self.portal_tools,
                                     umlprofile=self.uml_profile):
            # tgv overrules
            cpfromtgv = element.getTaggedValue('creation_permission', None)
            if cpfromtgv:
                creation_permission= self.processExpression(cpfromtgv)
            crfromtgv = element.getTaggedValue('creation_roles', None)
            if crfromtgv:
                creation_roles= self.processExpression(crfromtgv)
            ## abstract classes does not need an Add permission
            if creation_permission and not element.isAbstract():
                self.creation_permissions.append([element.getCleanName(),
                                                  creation_permission,
                                                  creation_roles])
                

                
        return outfile.getvalue()
    
    
    
    
    
    
    
    

    def generateZope2Interface(self, element, **kw):
        outfile = StringIO()
        log.info("%sGenerating zope2 interface '%s'.",
                 '    '*self.infoind, element.getName())

        wrt = outfile.write

        dependentImports = self.generateDependentImports(element).strip()
        if dependentImports:
            print >> outfile, dependentImports

        additionalImports = self.generateAdditionalImports(element)
        if additionalImports:
            print >> outfile, additionalImports

        print >> outfile, IMPORT_INTERFACE

        additionalImports = element.getTaggedValue('imports')
        if additionalImports:
            wrt(additionalImports)
        print >> outfile

        aggregatedClasses = element.getRefs() + element.getSubtypeNames(recursive=1)

        AlreadyGenerated.append(element.getType())
        name = element.getCleanName()

        wrt('\n')

        parentnames = [p.getCleanName() for p in element.getGenParents()]
        additionalParents = element.getTaggedValue('additional_parents')
        if additionalParents:
            parentnames = additionalParents.split(',') + list(parentnames)

        if not [c for c in element.getGenParents() if c.isInterface()]:
            parentnames.insert(0, 'Base')
        parents = ', '.join(parentnames)

        s1 = 'class %s%s(%s):\n' % (self.prefix, name, parents)

        wrt(s1)
        doc = element.getDocumentation(striphtml=self.strip_html)
        print >> outfile, utils.indent('"""%s\n"""' % doc, 1,
                                       stripBlank=True)

        header = element.getTaggedValue('class_header')
        if header:
            print >> outfile, utils.indent(header, 1)

        wrt('\n')
        self.generateMethods(outfile, element, mode='interface')
        wrt('\n# end of class %s' % name)

        return outfile.getvalue()


    def generateHeader(self, element):
        outfile=StringIO()
        i18ncontent = self.getOption('i18ncontent',element,
                                     self.i18n_content_support)

        if i18ncontent in self.i18n_at and element.isI18N():
            s1 = TEMPLATE_HEADER_I18N_I18N_AT
        elif i18ncontent == 'linguaplone':
            s1 = TEMPLATE_HEADER_I18N_LINGUAPLONE
        else:
            s1 = TEMPLATE_HEADER

        outfile.write(s1)

        genparentsstereotype = element.getRealizationParents()
        hasz3parent = False
        for gpst in genparentsstereotype:
            if gpst.hasStereoType('z3'):
                hasz3parent = True
                break
        if hasz3parent or element.hasStereoType('z3'):
            outfile.write('import zope\n')

        return outfile.getvalue()

    def getTools(self,package,autoinstallOnly=0):
        """ returns a list of  generated tools """
        res=[c for c in package.getClasses(recursive=1) if
             c.hasStereoType(self.portal_tools, umlprofile=self.uml_profile)]

        if autoinstallOnly:
            res=[c for c in res if utils.isTGVTrue(c.getTaggedValue('autoinstall')) ]

        return res

    def getGeneratedTools(self,package):
        """ returns a list of  generated tools """
        return [c for c in self.getGeneratedClasses(package) if
                c.hasStereoType(self.portal_tools, umlprofile=self.uml_profile)]

    def generateStdFiles(self, package):
        if package.isRoot():
            self.generateStdFilesForProduct(package)
        else:
            self.generateStdFilesForPackage(package)

    def generateStdFilesForPackage(self, package):
        """Generate the standard files for a non-root package"""

        # Generate an __init__.py
        self.generatePackageInitPy(package)

    def updateVersionForProduct(self, package):
        """Increment the build number in verion.txt"""

        build=1
        versionbase='0.1'
        fp=os.path.join(package.getFilePath(),'version.txt')
        vertext=self.readFile(fp)
        if vertext:
            versionbase=vertext=vertext.strip()
            parsed=vertext.split(' ')
            if parsed.count('build'):
                ind=parsed.index('build')
                try:
                    build=int(parsed[ind+1]) + 1
                except:
                    build=1

                versionbase=' '.join(parsed[:ind])

        version='%s build %d\n' % (versionbase,build)
        of=self.makeFile(fp)
        print >>of,version,
        of.close()

    def generateInstallPy(self, package):
        """Generate Extensions/Install.py from the DTML template"""

        # create Extension directory
        installTemplate=open(os.path.join(sys.path[0],'templates','Install.py')).read()
        extDir=os.path.join(package.getFilePath(),'Extensions')
        self.makeDir(extDir)

        # make __init__.py
        ipy=self.makeFile(os.path.join(extDir,'__init__.py'))
        ipy.write('# make me a python module\n')
        ipy.close()

        # prepare (d)TML varibles
        d={'package'    : package,
           'generator'  : self,
           'builtins'   : __builtins__,
           'utils'       :utils,
       }
        d.update(__builtins__)

        templ=utils.readTemplate('Install.py')
        dtml=HTML(templ,d)
        res=dtml()

        of=self.makeFile(os.path.join(extDir,'Install.py'))
        of.write(res)
        of.close()

        return

    def generateConfigPy(self, package):
        """ generates: config.py """

        configpath=os.path.join(package.getFilePath(),'config.py')
        parsed_config=self.parsePythonModule(package.getFilePath(), 'config.py')
        creation_permission = self.getOption('creation_permission', package, None)

        if creation_permission:
            default_creation_permission = creation_permission
        else:
            default_creation_permission = self.default_creation_permission

        roles = []
        creation_roles = []
        for perm in self.creation_permissions:
            if not perm[1] in roles and perm[2] is not None:
                roles.append(perm[1])
                creation_roles.append( (perm[1], perm[2]) )

        # prepare (d)TML varibles
        d={'package'                    : package,
           'generator'                  : self,
           'builtins'                   : __builtins__,
           'utils'                      : utils,
           'default_creation_permission': default_creation_permission,
           'creation_permissions'       : self.creation_permissions,
           'creation_roles'             : creation_roles,
           'parsed_config'              : parsed_config,
       }
        d.update(__builtins__)

        templ=utils.readTemplate('config.py')
        dtml=HTML(templ,d)
        res=dtml()

        of=self.makeFile(configpath)
        of.write(res)
        of.close()

        return

    def generateProductInitPy(self, package):
        """ Generate __init__.py at product root from the DTML template"""

        # Get the names of packages and classes to import
        packageImports = [m.getModuleName() for m in package.getAnnotation('generatedPackages') or []
                          if not (m.hasStereoType('tests', umlprofile=self.uml_profile) or
                                  m.hasStereoType('stub', umlprofile=self.uml_profile))]
        classImports   = [m.getModuleName() for m in package.generatedModules if not m.hasStereoType('tests', umlprofile=self.uml_profile)]

        # Find additional (custom) permissions
        additional_permissions=[]
        addperms= self.getOption('additional_permission',package,default=[]),
        for line in addperms:
            if len(line)>0:
                line=line.split('|')
                line[0]=line[0].strip()
                if len(line)>1:
                    line[1]=["'%s'" % r.strip() for r in line[1].split(',')]
                additional_permissions.append(line)

        # Find out if we need to initialise any tools
        generatedTools = self.getGeneratedTools(package)
        hasTools = 0
        toolNames = []
        if generatedTools:
            toolNames = [c.getQualifiedName(package, includeRoot=0) for c in generatedTools]
            hasTools = 1

        # Get the preserved code section
        parsed = self.parsePythonModule(package.getFilePath (), '__init__.py')

        protectedInitCodeH = self.getProtectedSection(parsed, 'custom-init-head', 0)
        protectedInitCodeT = self.getProtectedSection(parsed, 'custom-init-top', 1)
        protectedInitCodeB = self.getProtectedSection(parsed, 'custom-init-bottom', 1)

        # prepare DTML varibles
        d={'generator'                     : self,
           'utils'                         : utils,
           'package'                       : package,
           'product_name'                  : package.getProductName(),
           'package_imports'               : packageImports,
           'class_imports'                 : classImports,
           'additional_permissions'        : additional_permissions,
           'has_tools'                     : hasTools,
           'tool_names'                    : toolNames,
           'creation_permissions'          : self.creation_permissions,
           'protected_init_section_head'   : protectedInitCodeH,
           'protected_init_section_top'    : protectedInitCodeT,
           'protected_init_section_bottom' : protectedInitCodeB,
       }

        templ=utils.readTemplate('__init__.py')
        dtml=HTML(templ,d)
        res=dtml()

        of=self.makeFile(os.path.join(package.getFilePath(),'__init__.py'))
        of.write(res)
        of.close()

        return

    def generatePackageInitPy(self, package):
        """ Generate __init__.py for packages from the DTML template"""

        # Get the names of packages and classes to import
        packageImports = [m.getModuleName () for m in package.getAnnotation('generatedPackages') or []]
        classImports   = [m.getModuleName () for m in package.generatedModules]

        # Get the preserved code sections
        parsed = self.parsePythonModule(package.getFilePath (), '__init__.py')
        headerCode = self.getProtectedSection(parsed, 'init-module-header')
        footerCode = self.getProtectedSection(parsed, 'init-module-footer')

        # Prepare DTML varibles
        d={'generator'                     : self,
           'package'                       : package,
           'utils'                         : utils,
           'package_imports'               : packageImports,
           'class_imports'                 : classImports,
           'protected_module_header'       : headerCode,
           'protected_module_footer'       : footerCode,
       }

        templ=utils.readTemplate('__init_package__.py')
        dtml=HTML(templ,d)
        res=dtml()

        of=self.makeFile(os.path.join(package.getFilePath(),'__init__.py'))
        of.write(res)
        of.close()

        return


    def generateStdFilesForProduct(self, package):
        """Generate __init__.py,  various support files and and the skins
        directory. The result is a QuickInstaller installable product
        """

        target = package.getFilePath ()

        # remove trailing slash
        if target[-1] in ('/','\\'):
            target=target[:-1]

        templdir=os.path.join(sys.path[0],'templates')

        # Create a tool.gif if necessary
        if self.getGeneratedTools(package):
            toolgif = open(os.path.join(templdir,'tool.gif'),'rb').read()
            of=self.makeFile(os.path.join(package.getFilePath(),'tool.gif'), self.force, 1)
            if of:
                of.write(toolgif)
                of.close()

        # Generate a refresh.txt for the product
        of=self.makeFile(os.path.join(package.getFilePath(),'refresh.txt'))
        of.close()

        # Increment version.txt build number
        self.updateVersionForProduct(package)

        # Generate product root __init__.py
        self.generateProductInitPy(package)

        # Create a customisation policy if required
        if self.customization_policy:
            of=self.makeFile(os.path.join(package.getFilePath(),'CustomizationPolicy.py'),0)
            if of:
                cpTemplate=utils.readTemplate('CustomizationPolicy.py')
                d={'package':package,'generator':self}
                cp=HTML(cpTemplate,d)()
                of.write(cp)
                of.close()

        # Generate config.py from template
        self.generateConfigPy(package)

        # Generate Extensions/Install.py
        self.generateInstallPy(package)



    def generateApeConf(self, target,package):
        #generates apeconf.xml

        #remove trailing slash
        if target[-1] in ('/','\\'):
            target=target[:-1]

        templdir=os.path.join(sys.path[0],'templates')
        apeconfig_object=open(os.path.join(templdir,'apeconf_object.xml')).read()
        apeconfig_folder=open(os.path.join(templdir,'apeconf_folder.xml')).read()

        of=self.makeFile(os.path.join(target,'apeconf.xml'))
        print >> of, TEMPL_APECONFIG_BEGIN
        for el in self.root.getClasses():
            if el.isInternal() or el.hasStereoType(self.stub_stereotypes, umlprofile=self.uml_profile):
                continue

            print >>of
            if el.getRefs() + el.getSubtypeNames(recursive=1):
                print >>of,apeconfig_folder % {'project_name':package.getProductName(),'class_name':el.getCleanName()}
            else:
                print >>of,apeconfig_object % {'project_name':package.getProductName(),'class_name':el.getCleanName()}

        print >>of, TEMPL_APECONFIG_END
        of.close()

    def getGeneratedClasses(self,package):
        classes=package.getAnnotation('generatedClasses') or []
        for p in package.getPackages():
            if not p.isProduct():
                classes.extend(self.getGeneratedClasses(p))
        res=[]
        for c in classes:
            if c not in res:
                res.append(c)
        return res

    def generatePackage(self, package, recursive=1):
        log.debug("Generating package %s.",
                  package)
        if package.hasStereoType(self.stub_stereotypes, umlprofile=self.uml_profile):
            log.debug("It's a stub stereotyped package, skipping.")
            return
        package.generatedModules = []
        if package.getName().lower().startswith('java') or not package.getName():
            #to suppress these unneccesary implicit created java packages (ArgoUML and Poseidon)
            log.debug("Ignoring unneeded package '%s'.",
                      package.getName())
            return

        self.makeDir(package.getFilePath())

        for element in package.getClasses()+package.getInterfaces():
            #skip stub and internal classes
            if element.isInternal() or element.getName() in self.hide_classes \
               or element.getName().lower().startswith('java::'): # Enterprise Architect fix!
                log.debug("Ignoring unnecessary class '%s'.",
                          element.getName())
                continue
            if element.hasStereoType(self.stub_stereotypes, umlprofile=self.uml_profile):
                log.debug("Ignoring stub class '%s'.",
                          element.getName())
                continue

            module=element.getModuleName()
            package.generatedModules.append(element)
            outfilepath=os.path.join(package.getFilePath(), module+'.py')

            if self.method_preservation:
                filename = os.path.join(self.targetRoot, outfilepath)
                log.debug("Filename (joined with targetroot) is "
                          "'%s'.", filename)
                try:
                    mod=PyParser.PyModule(filename)
                    log.debug("Existing sources found for element %s: %s.",
                              element.getName(), outfilepath)
                    self.parsed_sources.append(mod)
                    for c in mod.classes.values():
                        self.parsed_class_sources[package.getFilePath()+'/'+c.name]=c
                except IOError:
                    log.debug("No source found at %s.",
                              filename)
                    pass
                except:
                    log.critical("Error while reparsing file '%s'.",
                                 outfilepath)
                    raise

            try:
                outfile = StringIO()
                element.parsed_class = self.parsed_class_sources.get(element.getPackage().getFilePath()+'/'+element.name,None)
                if not element.isInterface():
                    outfile.write(self.generateModuleInfoHeader(element))
                    print >>outfile, self.dispatchXMIClass(element)
                    generated_classes = package.getAnnotation('generatedClasses') or []
                    generated_classes.append(element)
                    package.annotate('generatedClasses', generated_classes)
                else:
                    outfile = StringIO()
                    outfile.write(self.generateModuleInfoHeader(element))
                    print >>outfile, self.dispatchXMIInterface(element)
                    generated_interfaces = package.getAnnotation('generatedInterfaces') or []
                    generated_interfaces.append(element)
                    package.annotate('generatedInterfaces', generated_interfaces)

                buf = outfile.getvalue()

                log.debug("The outfile is ready to be written to disk now. "
                          "Loading it with the pyparser just to be sure we're "
                          "not writing broken files to disk.")
                try:
                    PyParser.PyModule(buf, mode='string')
                    log.debug("Nothing wrong with the outfile '%s'.",
                              outfilepath)
                except:
                    log.info(buf)
                    log.critical("There's something wrong with the python code we're about "
                                 "to write to disk. Perhaps a faulty tagged value or a "
                                 "genuine bug in parsing the previous version of the file. "
                                 "The filename is '%s'. For easy debugging, the file is "
                                 "printed above.",
                                 outfilepath)
                    raise
                classfile = self.makeFile(outfilepath)
                # TBD perhaps check if the file is parseable
                if type(buf) == types.UnicodeType:
                    buf = buf.encode('utf-8')
                print >> classfile, buf
                classfile.close()
            except:
                #roll back the changes
                # and dont swallow the exception
                raise

        #generate subpackages
        generatedPkg = package.getAnnotation('generatedPackages') or []
        for p in package.getPackages():
            if p.isProduct():
                self.infoind += 1
                self.generateProduct(p)
                self.infoind -= 1
            else:
                log.info("%sGenerating package '%s'.",
                         '    '*self.infoind,
                         p.getName())
                self.infoind += 1
                self.generatePackage(p,recursive=1)
                self.infoind -= 1
                generatedPkg.append(p)
                package.annotate('generatedPackages',generatedPkg)

        self.generateStdFiles(package)

    def generateRelation(self, doc, collection, relname, relid,
                         sourcetype=None, targettype=None,
                         sourceinterface=None,targetinterface=None,
                         sourcecardinality=(None,None),
                         targetcardinality=(None,None),
                         assocclassname=None,
                         inverse_relation_id=None,
                         primary=0,
# OJO ACV EXTENSION Polymorphic relations Begin            
                         additionalSourceTypeNames=[],
                         additionalTargetTypeNames=[],
# OJO ACV EXTENSION End
):

        ruleset=doc.createElement('Ruleset')
        ruleset.setAttribute('id',relname)
        ruleset.setAttribute('uid',relid)
        collection.appendChild(ruleset)

        #type and interface constraints
        if sourcetype or targettype:
            typeconst=doc.createElement('TypeConstraint')
            typeconst.setAttribute('id','type_constraint')
            ruleset.appendChild(typeconst)

        if sourceinterface or targetinterface:
            ifconst=doc.createElement('InterfaceConstraint')
            ifconst.setAttribute('id','interface_constraint')
            ruleset.appendChild(ifconst)


        if sourcetype:
            el=doc.createElement('allowedSourceType')
            typeconst.appendChild(el)
            el.appendChild(doc.createTextNode(sourcetype))
# OJO ACV EXTENSION Polymorphic relations Begin            
            if additionalSourceTypeNames:
                for unAdditionalSourceTypeName in additionalSourceTypeNames:
                    if unAdditionalSourceTypeName:
                        aNewAllowedSourceTypeElement=doc.createElement('allowedSourceType')
                        typeconst.appendChild(aNewAllowedSourceTypeElement)                    
                        aNewAllowedSourceTypeElement.appendChild(doc.createTextNode(unAdditionalSourceTypeName))
# OJO ACV EXTENSION End            

        if sourceinterface:
            el=doc.createElement('allowedSourceInterface')
            ifconst.appendChild(el)
            el.appendChild(doc.createTextNode(sourceinterface))



        if targettype:
            el=doc.createElement('allowedTargetType')
            typeconst.appendChild(el)
            el.appendChild(doc.createTextNode(targettype))
# OJO ACV EXTENSION Polymorphic relations Begin            
            if additionalTargetTypeNames:
                for unAdditionalTargetTypeName in additionalTargetTypeNames:
                    if unAdditionalTargetTypeName:
                        aNewAllowedTargetTypeElement=doc.createElement('allowedTargetType')
                        typeconst.appendChild(aNewAllowedTargetTypeElement)                    
                        aNewAllowedTargetTypeElement.appendChild(doc.createTextNode(unAdditionalTargetTypeName))
# OJO ACV EXTENSION End            

        if targetinterface:
            ifconst.setAttribute('id','interface_constraint')
            el=doc.createElement('allowedTargetInterface')
            ifconst.appendChild(el)
            el.appendChild(doc.createTextNode(targetinterface))


        #association constraint
        if assocclassname:
            contref = doc.createElement('ContentReference')
            ruleset.appendChild(contref)
            contref.setAttribute('id', 'content_reference')
            pt = doc.createElement('portalType')
            contref.appendChild(pt)
            pt.appendChild(doc.createTextNode(assocclassname))

            pt = doc.createElement('shareWithInverse')
            contref.appendChild(pt)
            pt.appendChild(doc.createTextNode('1'))

            el = doc.createElement('primary')
            el.appendChild(doc.createTextNode(str(primary)))
            contref.appendChild(el)

        #cardinality
        targetcardinality=list(targetcardinality)
        if targetcardinality[0] == -1:
            targetcardinality[0] = None
        if targetcardinality[1] == -1:
            targetcardinality[1] = None

        if targetcardinality != [None, None]:
            const = doc.createElement('CardinalityConstraint')
            ruleset.appendChild(const)
            const.setAttribute('id', 'cardinality')
            if targetcardinality[0]:
                el = doc.createElement('minTargetCardinality')
                const.appendChild(el)
                el.appendChild(doc.createTextNode(str(targetcardinality[0])))
            if targetcardinality[1]:
                el = doc.createElement('maxTargetCardinality')
                const.appendChild(el)
                el.appendChild(doc.createTextNode(str(targetcardinality[1])))

        #create the inverse relation
        if inverse_relation_id:
            const=doc.createElement('InverseImplicator')
            ruleset.appendChild(const)
            const.setAttribute('id','inverse_relation')
            el=doc.createElement('inverseRuleset')
            const.appendChild(el)
            el.setAttribute('uidref',inverse_relation_id)

        return ruleset



    def getAggregatedClasses(self, recursive=0,
                             filter=['class', 'interface'], **kw):
        """Returns the non-intrinsic subtypes classes."""
        res = [o for o in self.subTypes if not o.isAbstract() ]
        if recursive:
            for sc in self.subTypes:
                res.extend([o for o in sc.getGenChildren(recursive=1)])
        res = [o for o in res if o.__class__.__name__ in
               ['XMI'+f.capitalize() for f in filter]]
        return res



# ACV OJO EXTENSION 2008/11/08
    def getMethodDefsAndInheritableActions( self, theElement):
        someMethods     = [ ]
        someMethodNames = [ ]

        someLocalMethods = theElement.methodDefs        
        for anMethod in someLocalMethods:
            if not (anMethod in someMethods) and not ( anMethod.name in someMethodNames):
                someMethods.append( anMethod)         
                someMethodNames.append( anMethod.name )
                    
        someAlreadyVisited = [ theElement]
        for aParent in theElement.genParents:
            someParentMethods = self.getInheritableActions_recursive( aParent, someAlreadyVisited, someMethodNames)
            for anMethod in someParentMethods:
                if not (anMethod in someMethods):
                    someMethods.append( anMethod)

        return someMethods      
    
    
# ACV OJO EXTENSION 2008/11/08 
    def getInheritableActions_recursive( self, theElement, theAlreadyVisited=[], theAlreadyGotMethodNames=[]):       
        someMethods = [ ]
        if theElement in theAlreadyVisited:
            return someMethods

        theAlreadyVisited.append( theElement)
 
        someLocalMethods = [ unMethod for unMethod in theElement.methodDefs if unMethod.hasStereoType( 'action') and unMethod.getTaggedValue( 'inheritable', '') == 'True' ]      
        for anMethod in someLocalMethods:
            if not (anMethod in someMethods) and not ( anMethod.name in theAlreadyGotMethodNames):
                someMethods.append( anMethod)
                theAlreadyGotMethodNames.append( anMethod.name)
        
        for aParent in theElement.genParents:
            someParentMethods = self.getInheritableActions_recursive( aParent, theAlreadyVisited, theAlreadyGotMethodNames)
            for anMethod in someParentMethods:
                if not (anMethod in someMethods):
                    someMethods.append( anMethod)
                    
        return someMethods    
    


  

# ACV OJO EXTENSION 2008/05/16
    def getAllAttributeDefs( self, theElement):
        someAlreadyVisited = [ ]
        return self.getAllAttributeDefs_recursive( theElement, someAlreadyVisited)     
    
    
    
# ACV OJO EXTENSION 2008/05/16
    def getAllAttributeDefs_recursive( self, theElement, theAlreadyVisited=[]):       
        someAttributes = [ ]
        if theElement in theAlreadyVisited:
            return someAttributes

        theAlreadyVisited.append( theElement)
        
        for aParent in theElement.genParents:
            someParentAttributes = self.getAllAttributeDefs_recursive( aParent, theAlreadyVisited)
            for anAttribute in someParentAttributes:
                if not (anAttribute in someAttributes):
                    someAttributes.append( anAttribute)
                    
        someLocalAttributes = theElement.attributeDefs        
        for anAttribute in someLocalAttributes:
            if not (anAttribute in someAttributes):
                someAttributes.append( anAttribute)

        return someAttributes    
    

   
    

# ACV OJO EXTENSION 2008/05/16
    def getAllSuperClasses( self, theElement):
        someSuperClasses = [ ]
        self.getAllSuperClasses_recursive( theElement, someSuperClasses)     
        return someSuperClasses
    
    
# ACV OJO EXTENSION 2008/05/16
    def getAllSuperClasses_recursive( self, theElement, theSuperClasses=[]):       
        if theElement in theSuperClasses:
            return self

        theSuperClasses.append( theElement)
        
        for aParent in theElement.genParents:
            self.getAllSuperClasses_recursive( aParent, theSuperClasses)
 
        return self    
    
    

    

# ACV OJO EXTENSION 2008/05/16
    def getIsCollection( self, theElement):
        someSuperClasses = [ ]
        return self.getIsCollection_recursive( theElement, someSuperClasses)     
    
        
    
    
    
# ACV OJO EXTENSION 2008/05/16
    def getIsCollection_recursive( self, theElement, theSuperClasses=[]):       
        if theElement in theSuperClasses:
            return False

        theSuperClasses.append( theElement)
        
        someOperations = theElement.getMethodDefs( recursive=False)
        for anOperation in someOperations:
            anOperationName = anOperation.getName()
            if anOperationName == 'getEsColeccion':
                unCodeTaggedValue = anOperation.getTaggedValue('code', '')
                if unCodeTaggedValue.endswith('True'):
                    return True
        
        for aParent in theElement.genParents:
            if self.getIsCollection_recursive( aParent, theSuperClasses):
                return True
 
        return False 
    

    
    
    
# ACV OJO EXTENSION 2008/09/03
    def getClaseRaiz( self, thePackage):
        for unaClass in thePackage.getClasses():
            if unaClass.getTaggedValue( 'is_model_root_type', ''):
                return unaClass
        return None
    
    
        
    
    
# ACV OJO EXTENSION 2008/05/16
    def getAllContainedClasses( self, theElement):      
        someSuperClasses = self.getAllSuperClasses( theElement)
        someClassesRefs = theElement.getRefs()
        someAggregatedClasses = []
        
        for aSuperClass in someSuperClasses:
            otherAggregatedClasses = aSuperClass.getAggregatedClasses(recursive=0,filter=['class'])
            for aClass in otherAggregatedClasses:
                if not( aClass in someAggregatedClasses):
                    someAggregatedClasses.append( aClass)
        return someAggregatedClasses
    
    
    
    
# ACV OJO EXTENSION 2008/09/03
    def getAllContainedClassesIncludingAbstractOnes( self, theElement):      
        someSuperClasses = self.getAllSuperClasses( theElement)
        someClassesRefs = theElement.getRefs()
        someAggregatedClasses = []
        
        for aSuperClass in someSuperClasses:
            otherAggregatedClasses = self.getAggregatedClassesIncludingAbstractOnes(aSuperClass, recursive=0,filter=['class'])
            for aClass in otherAggregatedClasses:
                if not( aClass in someAggregatedClasses):
                    someAggregatedClasses.append( aClass)
        return someAggregatedClasses
    
    
    
    

# ACV OJO EXTENSION 2008/09/03
    def getAggregatedClassesIncludingAbstractOnes(self, theClass, recursive=0, filter=['class', 'interface'], **kw):
        """Returns the non-intrinsic subtypes classes."""
        res = [o for o in theClass.subTypes]
        if recursive:
            for sc in theClass.subTypes:
                res.extend([o for o in sc.getGenChildren(recursive=1)])
        res = [o for o in res if o.__class__.__name__ in
               ['XMI'+f.capitalize() for f in filter]]
        return res

    
    
    
# ACV OJO EXTENSION 2008/05/16
    def getAllPackagesInModel( self, theElement):      
        aPackage = theElement.package
        if aPackage:
            return self.getAllPackagesInModel( aPackage)
        
        somePackages = [ ]
        self.getAllPackagesInModel_recursive( theElement, somePackages)
        return somePackages
    
    
    
    
# ACV OJO EXTENSION 2008/05/16
    def getAllPackagesInModel_recursive( self, theElement, thePackages=[]):              
        if theElement in thePackages:
            return self
        
        thePackages.append( theElement)
        
        someChildrenPackages = theElement.packages
        for aPackage in someChildrenPackages:
            self.getAllPackagesInModel_recursive( aPackage, thePackages)
        return self
    
    
    
 
    
# ACV OJO EXTENSION 2008/05/16
    def getAllAssociations( self, theElement):      
        someAssociations = []
        somePackages = self.getAllPackagesInModel( theElement)
        for aPackage in somePackages:
            somePackageAssociations = aPackage.getAssociations( recursive=0) # recursive=1
            for anAssociation in somePackageAssociations:
                if not( anAssociation in someAssociations):
                    someAssociations.append( anAssociation)
        return someAssociations
         
    
    
    def getAssociationNamed( self, theElement, theAssociationName):      
        someAssociations = []
        somePackages = self.getAllPackagesInModel( theElement)
        for aPackage in somePackages:
            somePackageAssociations = aPackage.getAssociations( recursive=0) 
            for anAssociation in somePackageAssociations:
                if anAssociation.name == theAssociationName:
                    return anAssociation
        return None
    
    def getAssociationOrAggregationNamed( self, theElement, theAssociationName):      
        for aPackage in self.getAllPackagesInModel( theElement):
            for aClass in aPackage.getClassesAndInterfaces( recursive=0):
                for anAssociation in aClass.assocsFrom + aClass.assocsTo :
                    if anAssociation.name == theAssociationName:
                        return anAssociation
        return None
    
    def getClassNamed( self, theElement, theClassName):      
        for aPackage in self.getAllPackagesInModel( theElement):
            for aClass in aPackage.getClassesAndInterfaces( recursive=0):
                if aClass.name == theClassName:
                    return aClass
        return None
    
    
    
# ACV OJO EXTENSION 2008/05/16
    def getAllAggregations( self, theElement):      
        someAssociations = Set()
        somePackages = self.getAllPackagesInModel( theElement)
        for aPackage in somePackages:
            somePackageClasses = aPackage.getClassesAndInterfaces( recursive=0)
            for aClass in somePackageClasses:
                someClassAggregations = aClass.getFromAssociations(aggtypes=['composite'])
                someAssociations.union_update( someClassAggregations)
        return someAssociations
    
    
# ACV OJO EXTENSION 2008/05/16
    def getAllNonAggregationsClassesAndEnds( self, theElement):    
        
        someAssociations = self.getAllAssociations( theElement)
        someSuperClasses = self.getAllSuperClasses( theElement)
        
        someResults = []
        someEnds = []
        for anAssociation in someAssociations:
            aFromEnd = anAssociation.fromEnd
            aFromEndClass = aFromEnd.obj

            aToEnd = anAssociation.toEnd
            aToEndClass = aToEnd.obj
            
            if not( aFromEnd.aggregation in ['aggregate', 'composite', ] or aToEnd.aggregation in ['aggregate', 'composite', ] ):
                if aFromEndClass in someSuperClasses:
                    if not ( aFromEnd in someEnds):
                        someResults.append( [ anAssociation, aToEndClass, aFromEnd, aToEnd, anAssociation.getName()])
                        someEnds.append( aFromEnd)
                if aToEndClass in someSuperClasses:
                    if not ( aToEnd in someEnds):
                        someResults.append( [ anAssociation, aFromEndClass, aToEnd, aFromEnd, anAssociation.getTaggedValue('inverse_relation_name', 'NOINVERSERELATIONFOUND')])
                        someEnds.append( aToEnd)
        return someResults
    
    
    
# ACV OJO EXTENSION 2008/05/16
    def getAllAggregationsAssociationsCompositionsWithComposite( self, theElement):      
        someAssociations = Set()
        somePackages = self.getAllPackagesInModel( theElement)
        for aPackage in somePackages:
            somePackageClasses = aPackage.getClassesAndInterfaces( recursive=0)
            for aClass in somePackageClasses:
                someClassAssocs = aClass.assocsFrom + aClass.assocsTo               
                someClassAggregations = [ anAssoc for anAssoc in someClassAssocs if anAssoc.fromEnd.aggregation in [ 'composite'] or anAssoc.toEnd.aggregation in [ 'composite'] ]
                someAssociations.union_update( someClassAggregations)

        return someAssociations
    
    
# ACV OJO EXTENSION 2008/05/16
    def getAllAggregationsClassesAndEnds( self, theElement):    
        
        someAssociations = self.getAllAggregationsAssociationsCompositionsWithComposite( theElement)
        someSuperClasses = self.getAllSuperClasses( theElement)
        
        someResults = []
        for anAssociation in someAssociations:
            aFromEnd = anAssociation.fromEnd
            aFromEndClass = aFromEnd.obj

            aToEnd = anAssociation.toEnd
            aToEndClass = aToEnd.obj
            
            if aFromEndClass in someSuperClasses :
                if aFromEnd.aggregation in ['aggregate', 'composite', ]:
                    someResults.append( [ anAssociation, aToEndClass, aFromEnd, aToEnd, anAssociation.getName()])

            if aToEndClass in someSuperClasses :
                if aToEnd.aggregation in ['aggregate', 'composite', ]:
                    someResults.append( [ anAssociation, aFromEndClass, aToEnd, aFromEnd, anAssociation.getName()])

        return someResults
    
    
# ACV OJO EXTENSION 2008/09/98
    def getNonAggregationsClassesAndEnds( self, theElement):    
        
        someAssociations = self.getAllAssociations( theElement)
        
        someResults = []
        for anAssociation in someAssociations:
            aFromEnd = anAssociation.fromEnd
            aFromEndClass = aFromEnd.obj

            aToEnd = anAssociation.toEnd
            aToEndClass = aToEnd.obj
            
            if (aFromEndClass == theElement) or (aToEndClass == theElement):
                if not( aFromEnd.aggregation in ['aggregate', 'composite', ] or aToEnd.aggregation in ['aggregate', 'composite', ] ):
                    if aFromEndClass == theElement:
                        someResults.append( [ anAssociation, aToEndClass, aFromEnd, aToEnd, anAssociation.getName()])
                    elif aToEndClass == theElement:
                        someResults.append( [ anAssociation, aFromEndClass, aToEnd, aFromEnd, anAssociation.getTaggedValue('inverse_relation_name', 'NOINVERSERELATIONFOUND')])
        return someResults
       
    
# ACV OJO EXTENSION 2008/09/08
    def getAggregationsClassesAndEnds( self, theElement):    
        
        someAssociations = self.getAllAggregationsAssociationsCompositionsWithComposite( theElement)
        someSuperClasses = self.getAllSuperClasses( theElement)
        
        someResults = []
        for anAssociation in someAssociations:
            aFromEnd = anAssociation.fromEnd
            aFromEndClass = aFromEnd.obj

            aToEnd = anAssociation.toEnd
            aToEndClass = aToEnd.obj
            
            if aFromEndClass == theElement :
                if aFromEnd.aggregation in ['aggregate', 'composite', ]:
                    someResults.append( [ anAssociation, aToEndClass, aFromEnd, aToEnd, anAssociation.getName()])

            if aToEndClass == theElement:
                if aToEnd.aggregation in ['aggregate', 'composite', ]:
                    someResults.append( [ anAssociation, aFromEndClass, aToEnd, aFromEnd, anAssociation.getName()])

        return someResults
    
  


#  ACV OJO EXTENSION 2008/09/03
    def generateI118Ncatalogs(self, thePackage):
        if not thePackage:
            return self
 
        unProjectName = thePackage.getProductName()
        unBaseLanguage = thePackage.getTaggedValue( 'baseLanguage') or ''
        unBaseLanguageTitle = thePackage.getTaggedValue( 'baseLanguageTitle') or unBaseLanguage
        unBaseLanguageFallbacks = thePackage.getTaggedValue( 'baseLanguageFallbacks') or ''
        unOtherLanguage = thePackage.getTaggedValue( 'otherLanguage') or ''
        unOtherLanguageTitle = thePackage.getTaggedValue( 'otherLanguageTitle') or unOtherLanguage
        unOtherLanguageFallbacks = thePackage.getTaggedValue( 'otherLanguageFallbacks') or ''
        
        if unBaseLanguage:
            self.generateI118NcatalogForLanguage( thePackage, unBaseLanguage, True, unBaseLanguageTitle, unBaseLanguageFallbacks)
            self.generatePloneI118NcatalogForLanguage( thePackage, unBaseLanguage, True, unBaseLanguageTitle, unBaseLanguageFallbacks)
    
        if unOtherLanguage:
            self.generateI118NcatalogForLanguage( thePackage, unOtherLanguage, False, unOtherLanguageTitle, unOtherLanguageFallbacks)
            self.generatePloneI118NcatalogForLanguage( thePackage, unOtherLanguage, False, unOtherLanguageTitle, unOtherLanguageFallbacks)
        
        return self
    
    
    
    
    
# ACV OJO EXTENSION 2008/09/08
    
    def parseExistingMessagesCatalog(self, theFilePath):
        someMessages= {}
        return someMessages
    
        
        
        
# ACV OJO EXTENSION 2008/09/08
    
    def generateI118NcatalogForLanguage(self, thePackage, theLanguage, theEsBaseLanguage, theLanguageTitle, theFallbacks):
        if not thePackage or not theLanguage:
            return self
   
        self.makeDir( os.path.join(thePackage.getFilePath(), 'i18n'))
        
        unProductName = thePackage.getProductName()
        aFileName = '%s-%s.po' % ( unProductName, theLanguage)
        aFilePath = os.path.join( thePackage.getFilePath(), 'i18n', aFileName)
        
        unosMensajes = {}
        if os.path.exists( aFilePath):
            unosMensajesExistentes = self.parseExistingMessagesCatalog( aFilePath)
            unosMensajes.update( unosMensajesExistentes)
            
            
        try:
            aFile = self.makeFile( aFilePath,force=1)
            if not aFile:
                log.info("generateI118NcatalogForLanguage %s failed opening" % ( theLanguage, str( aFileName)))
                return self
            
            aTemplatesDir =  os.path.join( sys.path[0], 'templates')
            aPotTemplate = open(os.path.join(sys.path[0], 'templates', 'msg_catalog.po')).read()
            someAuthors, someEmails, anAuthorline = self.getAuthors(thePackage)
            aFile.write( aPotTemplate % {
                'author':', '.join( someAuthors) or 'unknown author',
                'email':', '.join([ anEmail[1:-1] for anEmail in someEmails]) or 'unknown@email.address',
                'year': str( time.localtime()[0]),
                'datetime': time.ctime(),
                'charset': 'UTF-8',
                'package': unProductName,
                'domain': unProductName,
                'language_code': theLanguage,
                'language_name': theLanguageTitle,
                'fallbacks': theFallbacks,
            })

            for unaClass in self.getSortedClasses(  thePackage):
                #skip stub and internal classes
                if unaClass.isInternal() \
                    or unaClass.getName() in self.hide_classes \
                    or unaClass.getName().lower().startswith('java::') \
                    or unaClass.hasStereoType(self.stub_stereotypes, umlprofile=self.uml_profile):
                    continue
            
                self.generateI118NcatalogForLanguage_Class( aFile, unProductName, theLanguage, theEsBaseLanguage, unaClass)
        finally:
            if aFile:
                aFile.close()    
        return self
    
    
    
    

    

    def fHasCollectionDerivationParams(self, theElement):
        if not theElement:
            return False
                
        aPackage = theElement.getPackage()
        unLabelDerivation = aPackage.getTaggedValue( 'collection_label_derivation', '')    
        unDescriptionDerivation = aPackage.getTaggedValue( 'collection_description_derivation', '')    
        unLabelDerivation2 = aPackage.getTaggedValue( 'collection_label_derivation2', '')    
        unDescriptionDerivation2 = aPackage.getTaggedValue( 'collection_description_derivation2', '')    

        if unLabelDerivation and unDescriptionDerivation and unLabelDerivation2 and unDescriptionDerivation2:
            return True
        return False
    
    
    
        
# ACV OJO EXTENSION 2008/09/08
    def generateI118NcatalogForLanguage_Class(self, theFile, theProductName, theLanguage, theEsBaseLanguage, theClass):
        if not theFile or not theLanguage or not theClass:
            return self
        
        anArchetypeNameSymbol  = '%s_%s_label'  % ( theProductName, theClass.name, )
        aTypeDescriptionSymbol = '%s_%s_help'  % ( theProductName, theClass.name, )
        
        unReverseTranslations = theClass.getTaggedValue( 'reverse_translations') or False

        if theEsBaseLanguage:
            if not unReverseTranslations:
                unArchetypeNameValue    = theClass.getTaggedValue( 'archetype_name') or theClass.name
                unArchetypeNameDefault  = theClass.getTaggedValue( 'archetype_name') or theClass.name
                aTypeDescriptionValue   = theClass.getTaggedValue( 'typeDescription') or theClass.name
                aTypeDescriptionDefault = theClass.getTaggedValue( 'typeDescription') or theClass.name
            else:
                unArchetypeNameValue    = theClass.getTaggedValue( 'archetype_name2') or theClass.name
                unArchetypeNameDefault  = theClass.getTaggedValue( 'archetype_name2') or theClass.name
                aTypeDescriptionValue   = theClass.getTaggedValue( 'typeDescription2') or theClass.name
                aTypeDescriptionDefault = theClass.getTaggedValue( 'typeDescription2') or theClass.name
        else:
            if not unReverseTranslations:
                unArchetypeNameValue    = theClass.getTaggedValue( 'archetype_name2') or theClass.name
                unArchetypeNameDefault  = theClass.getTaggedValue( 'archetype_name') or theClass.name
                aTypeDescriptionValue   = theClass.getTaggedValue( 'typeDescription2') or theClass.name
                aTypeDescriptionDefault = theClass.getTaggedValue( 'typeDescription') or theClass.name
            else:
                unArchetypeNameValue    = theClass.getTaggedValue( 'archetype_name') or theClass.name
                unArchetypeNameDefault  = theClass.getTaggedValue( 'archetype_name2') or theClass.name
                aTypeDescriptionValue   = theClass.getTaggedValue( 'typeDescription') or theClass.name
                aTypeDescriptionDefault = theClass.getTaggedValue( 'typeDescription2') or theClass.name
                

        self.generateI18NMessage( theFile, theLanguage, theEsBaseLanguage, theClass, None, anArchetypeNameSymbol,  unArchetypeNameDefault,  unArchetypeNameValue)
        self.generateI18NMessage( theFile, theLanguage, theEsBaseLanguage, theClass, None, aTypeDescriptionSymbol, aTypeDescriptionDefault, aTypeDescriptionValue)
                    
        someAttributes = theClass.attributeDefs
        for anAttribute in sorted( someAttributes, lambda x,y: cmp( x.name, y.name)):
            self.generateI118NcatalogForLanguage_Attribute( theFile, theProductName, theLanguage, theEsBaseLanguage, theClass, anAttribute)

        someAggregations = self.getAggregationsClassesAndEnds( theClass)
        for anAggregationClassAndEnds in sorted( someAggregations, lambda x,y: cmp( x[ 3].name, y[ 3].name)):
            self.generateI118NcatalogForLanguage_Aggregation( theFile, theProductName, theLanguage, theEsBaseLanguage, theClass, anAggregationClassAndEnds)

        someRelations = self.getNonAggregationsClassesAndEnds( theClass)
        for aRelationClassAndEnds in sorted( someRelations, lambda x,y: cmp( x[ 3].name, y[ 3].name)):
            self.generateI118NcatalogForLanguage_Relation( theFile, theProductName, theLanguage, theEsBaseLanguage, theClass, aRelationClassAndEnds)
            
        return self
         
    
   
    
# ACV OJO EXTENSION 2008/09/08
    def generateI118NcatalogForLanguage_Attribute(self, theFile, theProductName, theLanguage, theEsBaseLanguage, theClass, theAttribute):
        if not theFile or not theLanguage or not theAttribute:
            return self

        aLabelSymbol       = '%s_%s_attr_%s_label'  % ( theProductName, theClass.name, theAttribute.name)
        aDescriptionSymbol = '%s_%s_attr_%s_help'  % ( theProductName, theClass.name, theAttribute.name)

        unReverseTranslations = theClass.getTaggedValue( 'reverse_translations') or False

        if theEsBaseLanguage:
            if not unReverseTranslations:
                unLabelValue        = theAttribute.getTaggedValue( 'label') or  theAttribute.name
                unLabelDefault      = theAttribute.getTaggedValue( 'label') or  theAttribute.name
                aDescriptionValue   = theAttribute.getTaggedValue( 'description') or  theAttribute.name
                aDescriptionDefault = theAttribute.getTaggedValue( 'description') or  theAttribute.name
            else:
                unLabelValue        = theAttribute.getTaggedValue( 'label2') or  theAttribute.name
                unLabelDefault      = theAttribute.getTaggedValue( 'label2') or  theAttribute.name
                aDescriptionValue   = theAttribute.getTaggedValue( 'description2') or  theAttribute.name
                aDescriptionDefault = theAttribute.getTaggedValue( 'description2') or  theAttribute.name                
        else:
            if not unReverseTranslations:            
                unLabelValue        = theAttribute.getTaggedValue( 'label2') or  theAttribute.name
                unLabelDefault      = theAttribute.getTaggedValue( 'label') or  theAttribute.name
                aDescriptionValue   = theAttribute.getTaggedValue( 'description2') or  theAttribute.name
                aDescriptionDefault = theAttribute.getTaggedValue( 'description') or theAttribute.name
            else:
                unLabelValue        = theAttribute.getTaggedValue( 'label') or  theAttribute.name
                unLabelDefault      = theAttribute.getTaggedValue( 'label2') or  theAttribute.name
                aDescriptionValue   = theAttribute.getTaggedValue( 'description') or  theAttribute.name
                aDescriptionDefault = theAttribute.getTaggedValue( 'description2') or theAttribute.name
                

        self.generateI18NMessage( theFile, theLanguage, theEsBaseLanguage, theClass, theAttribute, aLabelSymbol,       unLabelDefault,      unLabelValue)
        self.generateI18NMessage( theFile, theLanguage, theEsBaseLanguage, theClass, theAttribute, aDescriptionSymbol, aDescriptionDefault, aDescriptionValue)

        if theAttribute.type == 'selection':
            unVocabulary = theAttribute.getTaggedValue( 'vocabulary')
            if unVocabulary and unVocabulary.startswith( 'python:'):
                unVocabulary = unVocabulary[ len( 'python:'):]
            if unVocabulary:
                someVocabularyOptions = []
                someVocabularyOptions2 = []
                try:
                    someVocabularyOptions = eval( unVocabulary)   
                except:
                    None
                if someVocabularyOptions and someVocabularyOptions.__class__.__name__ in [  'list', 'set', 'tuple']:
                    
                    unVocabulary2 = theAttribute.getTaggedValue( 'vocabulary2')    
                    if unVocabulary2 and unVocabulary2.startswith( 'python:'):
                        unVocabulary2 = unVocabulary2[ len( 'python:'):]
                    if unVocabulary2:
                        someVocabularyOptions2 = []
                        try:
                            someVocabularyOptions2 = eval( unVocabulary2)   
                        except:
                            None
                            
                    for unOptionIndex in range( len( someVocabularyOptions)):
                        unVocabularyOption = someVocabularyOptions[ unOptionIndex]
                        unOptionSymbol      = '%s_%s_attr_%s_option_%s'  % ( theProductName, theClass.name, theAttribute.name, unVocabularyOption)
                        
                        if theEsBaseLanguage:
                            unOptionDefault     =  unVocabularyOption
                            unOptionValue       =  unVocabularyOption
                        else:
                            unOptionDefault     =  unVocabularyOption
                            if unOptionIndex < len( someVocabularyOptions2):
                                unOptionValue       =  someVocabularyOptions2[ unOptionIndex]    
                            else:
                                unOptionValue       =  unVocabularyOption
                            
                        self.generateI18NMessage( theFile, theLanguage, theEsBaseLanguage, theClass, theAttribute, unOptionSymbol, unOptionDefault, unOptionValue)
                     
        return self
            
            


    
    
# ACV OJO EXTENSION 2008/09/08
    def generateI118NcatalogForLanguage_Aggregation(self, theFile, theProductName, theLanguage, theEsBaseLanguage, theClass, theAggregationClassAndEnds):
        if not theFile or not theLanguage or not theAggregationClassAndEnds:
            return self

        
        anAssociation           = theAggregationClassAndEnds[0]

        aRelatedClass           = theAggregationClassAndEnds[1]
        aFromEnd                = theAggregationClassAndEnds[2]
        aToEnd                  = theAggregationClassAndEnds[3]
        aRelationName           = theAggregationClassAndEnds[4]
        anUpperBound            = aToEnd.getUpperBound()
        aToEndName              = aToEnd.getName()
        #aCapitalizedToEndName   = aToEndName.capitalize()+aToEnd.getName()[1:]

 
        if anAssociation.toEnd.aggregation in [ 'composite' ]:
            unLabelsSourceEndName   = anAssociation.fromEnd.name
            unLabelsSourceClassName =  anAssociation.toEnd.obj.name     
        else:
            unLabelsSourceEndName   = anAssociation.toEnd.name
            unLabelsSourceClassName =  anAssociation.fromEnd.obj.name                               
        
        aProductName = theClass.getPackage().getProductName()
        aLabelSymbol  =   '%s_%s_contents_%s_label' % ( aProductName, unLabelsSourceClassName, unLabelsSourceEndName)    
        aDescriptionSymbol =   '%s_%s_contents_%s_help' % ( aProductName, unLabelsSourceClassName, unLabelsSourceEndName)
        

        unReverseTranslations = anAssociation.getTaggedValue( 'reverse_translations') or False

        if theEsBaseLanguage:
            if not unReverseTranslations:
                unLabelValue        = anAssociation.getTaggedValue( 'label') or  anAssociation.name
                unLabelDefault      = anAssociation.getTaggedValue( 'label') or  anAssociation.name
                aDescriptionValue   = anAssociation.getTaggedValue( 'description') or anAssociation.name
                aDescriptionDefault = anAssociation.getTaggedValue( 'description') or anAssociation.name
            else:
                unLabelValue        = anAssociation.getTaggedValue( 'label2') or  anAssociation.name
                unLabelDefault      = anAssociation.getTaggedValue( 'label2') or  anAssociation.name
                aDescriptionValue   = anAssociation.getTaggedValue( 'description2') or anAssociation.name
                aDescriptionDefault = anAssociation.getTaggedValue( 'description2') or anAssociation.name                
        else:
            if not unReverseTranslations:
                unLabelValue        = anAssociation.getTaggedValue( 'label2') or anAssociation.name
                unLabelDefault      = anAssociation.getTaggedValue( 'label') or  anAssociation.name
                aDescriptionValue   = anAssociation.getTaggedValue( 'description2') or anAssociation.name
                aDescriptionDefault = anAssociation.getTaggedValue( 'description') or anAssociation.name
            else:
                unLabelValue        = anAssociation.getTaggedValue( 'label') or anAssociation.name
                unLabelDefault      = anAssociation.getTaggedValue( 'label2') or  anAssociation.name
                aDescriptionValue   = anAssociation.getTaggedValue( 'description') or anAssociation.name
                aDescriptionDefault = anAssociation.getTaggedValue( 'description2') or anAssociation.name
                

        self.generateI18NMessage( theFile, theLanguage, theEsBaseLanguage, theClass, aToEnd, aLabelSymbol,       unLabelDefault,      unLabelValue)
        self.generateI18NMessage( theFile, theLanguage, theEsBaseLanguage, theClass, aToEnd, aDescriptionSymbol, aDescriptionDefault, aDescriptionValue)

        return self    
            
            
    
    
# ACV OJO EXTENSION 2008/09/08
    def generateI118NcatalogForLanguage_Relation(self, theFile, theProductName, theLanguage, theEsBaseLanguage, theClass, theRelationClassAndEnds):
        if not theFile or not theLanguage or not theRelationClassAndEnds:
            return self

        anAssociation           = theRelationClassAndEnds[0]
        aRelatedClass           = theRelationClassAndEnds[1]
        aFromEnd                = theRelationClassAndEnds[2]
        aToEnd                  = theRelationClassAndEnds[3]
        aRelationName           = theRelationClassAndEnds[4]
        anUpperBound            = aToEnd.getUpperBound()
        aToEndName              = aToEnd.getName()
        #aCapitalizedToEndName   = aToEndName.capitalize()+aToEnd.getName()[1:]

        unReverseTranslations = anAssociation.getTaggedValue( 'reverse_translations') or False

        if theClass == anAssociation.fromEnd.obj:        
            aLabelSymbol       = '%s_%s_rel_%s_label'  % ( theProductName, theClass.name, anAssociation.toEnd.name)
            aDescriptionSymbol = '%s_%s_rel_%s_help'  % ( theProductName, theClass.name, anAssociation.toEnd.name)
            
            if theEsBaseLanguage:
                if not unReverseTranslations:
                    unLabelValue        = anAssociation.getTaggedValue( 'label') or  anAssociation.name
                    unLabelDefault      = anAssociation.getTaggedValue( 'label') or  anAssociation.name
                    aDescriptionValue   = anAssociation.getTaggedValue( 'description') or anAssociation.name
                    aDescriptionDefault = anAssociation.getTaggedValue( 'description') or anAssociation.name
                else:
                    unLabelValue        = anAssociation.getTaggedValue( 'label2') or  anAssociation.name
                    unLabelDefault      = anAssociation.getTaggedValue( 'label2') or  anAssociation.name
                    aDescriptionValue   = anAssociation.getTaggedValue( 'description2') or anAssociation.name
                    aDescriptionDefault = anAssociation.getTaggedValue( 'description2') or anAssociation.name                
            else:
                if not unReverseTranslations:
                    unLabelValue        = anAssociation.getTaggedValue( 'label2') or anAssociation.name
                    unLabelDefault      = anAssociation.getTaggedValue( 'label') or  anAssociation.name
                    aDescriptionValue   = anAssociation.getTaggedValue( 'description2') or anAssociation.name
                    aDescriptionDefault = anAssociation.getTaggedValue( 'description') or anAssociation.name
                else:
                    unLabelValue        = anAssociation.getTaggedValue( 'label') or anAssociation.name
                    unLabelDefault      = anAssociation.getTaggedValue( 'label2') or  anAssociation.name
                    aDescriptionValue   = anAssociation.getTaggedValue( 'description') or anAssociation.name
                    aDescriptionDefault = anAssociation.getTaggedValue( 'description2') or anAssociation.name
                    

            self.generateI18NMessage( theFile, theLanguage, theEsBaseLanguage, theClass, aToEnd, aLabelSymbol,       unLabelDefault,      unLabelValue)
            self.generateI18NMessage( theFile, theLanguage, theEsBaseLanguage, theClass, aToEnd, aDescriptionSymbol, aDescriptionDefault, aDescriptionValue)
 

        if theClass == anAssociation.toEnd.obj:        
            aLabelSymbol       = '%s_%s_rel_%s_label'  % ( theProductName, theClass.name, anAssociation.fromEnd.name)
            aDescriptionSymbol = '%s_%s_rel_%s_help'  % ( theProductName, theClass.name, anAssociation.fromEnd.name)
            
            if theEsBaseLanguage:
                if not unReverseTranslations:
                    unLabelValue        = anAssociation.getTaggedValue( 'inverse_relation_label') or anAssociation.name
                    unLabelDefault      = anAssociation.getTaggedValue( 'inverse_relation_label') or anAssociation.name
                    aDescriptionValue   = anAssociation.getTaggedValue( 'inverse_relation_description') or anAssociation.name
                    aDescriptionDefault = anAssociation.getTaggedValue( 'inverse_relation_description') or anAssociation.name
                else:
                    unLabelValue        = anAssociation.getTaggedValue( 'inverse_relation_label2') or anAssociation.name
                    unLabelDefault      = anAssociation.getTaggedValue( 'inverse_relation_label2') or anAssociation.name
                    aDescriptionValue   = anAssociation.getTaggedValue( 'inverse_relation_description2') or anAssociation.name
                    aDescriptionDefault = anAssociation.getTaggedValue( 'inverse_relation_description2') or anAssociation.name
                    
            else:
                if not unReverseTranslations:
                    unLabelValue        = anAssociation.getTaggedValue( 'inverse_relation_label2') or anAssociation.name
                    unLabelDefault      = anAssociation.getTaggedValue( 'inverse_relation_label') or  anAssociation.name
                    aDescriptionValue   = anAssociation.getTaggedValue( 'inverse_relation_description2') or  anAssociation.name
                    aDescriptionDefault = anAssociation.getTaggedValue( 'inverse_relation_description') or anAssociation.name
                else:
                    unLabelValue        = anAssociation.getTaggedValue( 'inverse_relation_label') or anAssociation.name
                    unLabelDefault      = anAssociation.getTaggedValue( 'inverse_relation_label2') or  anAssociation.name
                    aDescriptionValue   = anAssociation.getTaggedValue( 'inverse_relation_description') or  anAssociation.name
                    aDescriptionDefault = anAssociation.getTaggedValue( 'inverse_relation_description2') or anAssociation.name
                    
        
            self.generateI18NMessage( theFile, theLanguage, theEsBaseLanguage, theClass, aToEnd, aLabelSymbol,       unLabelDefault,      unLabelValue)
            self.generateI18NMessage( theFile, theLanguage, theEsBaseLanguage, theClass, aToEnd, aDescriptionSymbol, aDescriptionDefault, aDescriptionValue)
            
        return self    
            
            
          
    
    
    
#ACV OJO Extension 20090917
    def generatePloneI118NcatalogForLanguage(self, thePackage, theLanguage, theEsBaseLanguage, theLanguageTitle, theFallbacks):
        if not thePackage or not theLanguage:
            return self
   
        self.makeDir( os.path.join(thePackage.getFilePath(), 'i18n'))
        
        unProductName = thePackage.getProductName()
        aFileName = 'plone-%s-%s.po' % ( unProductName, theLanguage)
        aFilePath = os.path.join( thePackage.getFilePath(), 'i18n', aFileName)
        
        unosMensajes = {}
        if os.path.exists( aFilePath):
            unosMensajesExistentes = self.parseExistingMessagesCatalog( aFilePath)
            unosMensajes.update( unosMensajesExistentes)
            
            
        try:
            aFile = self.makeFile( aFilePath,force=1)
            if not aFile:
                log.info("generateI118NcatalogForLanguage %s failed opening" % ( theLanguage, str( aFileName)))
                return self
            
            aTemplatesDir =  os.path.join( sys.path[0], 'templates')
            aPotTemplate = open(os.path.join(sys.path[0], 'templates', 'msg_catalog.po')).read()
            someAuthors, someEmails, anAuthorline = self.getAuthors(thePackage)
            aFile.write( aPotTemplate % {
                'author':', '.join( someAuthors) or 'unknown author',
                'email':', '.join([ anEmail[1:-1] for anEmail in someEmails]) or 'unknown@email.address',
                'year': str( time.localtime()[0]),
                'datetime': time.ctime(),
                'charset': 'UTF-8',
                'package': unProductName,
                'domain': 'plone',
                'language_code': theLanguage,
                'language_name': theLanguageTitle,
                'fallbacks': theFallbacks,
            })

            for unaClass in self.getSortedClasses(  thePackage):
                #skip stub and internal classes
                if unaClass.isInternal() \
                    or unaClass.getName() in self.hide_classes \
                    or unaClass.isAbstract() \
                    or unaClass.getName().lower().startswith('java::') \
                    or unaClass.hasStereoType(self.stub_stereotypes, umlprofile=self.uml_profile):
                    continue
            
                self.generatePloneI118NcatalogForLanguage_Class( aFile, unProductName, theLanguage, theEsBaseLanguage, unaClass)
        finally:
            if aFile:
                aFile.close()    
        return self
        
    
    
    

        
# ACV OJO EXTENSION 2008/09/08
    def generatePloneI118NcatalogForLanguage_Class(self, theFile, theProductName, theLanguage, theEsBaseLanguage, theClass):
        if not theFile or not theLanguage or not theClass:
            return self
                
        unReverseTranslations = theClass.getTaggedValue( 'reverse_translations') or False
        
        if theEsBaseLanguage:
            if not unReverseTranslations:
                anArchetypeNameSymbol   = theClass.getTaggedValue( 'archetype_name') or theClass.name
                unArchetypeNameValue    = theClass.getTaggedValue( 'archetype_name') or theClass.name
                unArchetypeNameDefault  = theClass.getTaggedValue( 'archetype_name') or theClass.name
            else:
                anArchetypeNameSymbol   = theClass.getTaggedValue( 'archetype_name') or theClass.name
                unArchetypeNameValue    = theClass.getTaggedValue( 'archetype_name2') or theClass.name
                unArchetypeNameDefault  = theClass.getTaggedValue( 'archetype_name2') or theClass.name
        else:
            if not unReverseTranslations:
                anArchetypeNameSymbol   = theClass.getTaggedValue( 'archetype_name') or theClass.name
                unArchetypeNameValue    = theClass.getTaggedValue( 'archetype_name2') or theClass.name
                unArchetypeNameDefault  = theClass.getTaggedValue( 'archetype_name') or theClass.name
            else:
                anArchetypeNameSymbol   = theClass.getTaggedValue( 'archetype_name') or theClass.name
                unArchetypeNameValue    = theClass.getTaggedValue( 'archetype_name') or theClass.name
                unArchetypeNameDefault  = theClass.getTaggedValue( 'archetype_name2') or theClass.name
                
        self.generateI18NMessage( theFile, theLanguage, theEsBaseLanguage, theClass, None, anArchetypeNameSymbol,  unArchetypeNameDefault,  unArchetypeNameValue)
                    
        return self
         
        
        
    
# ACV OJO EXTENSION 2008/09/08
    def generateI18NMessage(self, theFile, theLanguage, theEsBaseLanguage, theClassOrAssociation, theFeature, theSymbol, theDefault, theValue):
        if not theFile or not theSymbol:
            return self
        
        theFile.write('\n')
        if theDefault:
            theFile.write('#. Default: "%s"\n' % (''.join( theDefault.strip("'").strip('"').strip('\n').strip('\t').splitlines())))
        else:
            theFile.write('#. Default: ""\n' )

        if theFeature:
            theFile.write('#: %s %s\n' % (theClassOrAssociation.name, theFeature.name))
        else:
            theFile.write('#: %s\n' % theClassOrAssociation.name)
            
        theFile.write('msgid "%s"\n' % theSymbol.strip("'").strip('"').strip('\n').strip('\t'))
        if theValue:
            theFile.write('msgstr "%s"\n' % (''.join( theValue.strip("'").strip('"').strip('\n').strip('\t').splitlines())))
        else:
            theFile.write('msgstr ""\n' )
            
        return self
    
    
    

    
    
# ACV OJO EXTENSION 2008/09/03
    def generateTraversalConfig(self, thePackage):

        unaClaseRaiz = self.getClaseRaiz( thePackage)
        if not unaClaseRaiz:
            return self
        unNombreClaseRaiz = unaClaseRaiz.name
        
        aFileName = '%s_TraversalConfig.py' % unNombreClaseRaiz
        aFilePath = os.path.join( thePackage.getFilePath(), aFileName)
        try:
            aFile =self.makeFile( aFilePath,force=1)
            if not aFile:
                log.info("generateTraversalConfig failed opening" % str( aFileName))
                return self
            
            aHeaderInfo = self.getHeaderInfo( thePackage)
            aHeaderInfo[ 'file_name'] = aFileName
            aFile.write( """# -*- coding: utf-8 -*-
#
# File: %(file_name)s
## %(copyright)s
#
# %(license)s
#
# Authors: 
# %(authors)s
#
#
""" % aHeaderInfo)    
            
            aFile.write( '''
__author__ = """%(authorline)s"""
''' % aHeaderInfo)        

            aFile.write( """
__docformat__ = 'plaintext'

from AccessControl                  import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.%(unProjectName)s.config import *


""" % { 'unProjectName': thePackage.getProductName(), 'unNombreClaseRaiz': unNombreClaseRaiz, } )
            
            
            aFile.write( """
class %s_TraversalConfig:            
""" % unNombreClaseRaiz)            
            
            
            aFile.write( '''
    """
    """
    security = ClassSecurityInfo()

    security.declarePublic('traversalConfig')
    def traversalConfig( self):
        return ''' % { 'unNC': unNombreClaseRaiz, } )
            
            aTraversalConfigList    = self.generateTraversalConfigList( thePackage)
            aTraversalConfigString  = self.prettyPrintTraversalConfig( aTraversalConfigList)
            aFile.write( aTraversalConfigString)
            
        finally:
            if aFile:
                aFile.close()
        return self
    
    
    
    
    
    
# ACV OJO EXTENSION 2008/09/03
    def generateTraversalConfigList(self, thePackage):
        unasConfigs = []
        
        for unaClass in self.getSortedClasses(  thePackage):
            #skip stub and internal classes
            if unaClass.isInternal() \
                or unaClass.getName() in self.hide_classes \
                or unaClass.isAbstract() \
                or unaClass.getName().lower().startswith('java::') \
                or unaClass.hasStereoType(self.stub_stereotypes, umlprofile=self.uml_profile):
                continue
            
            unasConfigs.append( self.generateTypeConfig_Mention( unaClass))
            unasConfigs.append( self.generateTypeConfig_Full( unaClass))
  
        return unasConfigs
        
    
    
    
    
# ACV OJO EXTENSION 2008/09/03
    def generateTypeConfig_Mention(self, theClass):
        unTypeConfigDict= {}
        
        unClassName =  self.fClassMetaTypeOrCleanName( theClass)
        unTypeConfigDict[ 'portal_types'] = [ unClassName,]
        unTypeConfigDict[ 'config_name'] = 'Mention'
        unTypeConfigDict[ 'mode'] = 'Reference'
        unTypeConfigDict[ 'extension'] = 'OneParagraph'
        unTypeConfigDict[ 'attrs'] = [
            { 'name': 'title',             'type': 'String',     'kind': 'Data',  }, 
            { 'name': 'archetype_name',    'type': 'String',     'kind': 'Meta',  }, 
            { 'name': 'description',       'type': 'Text',       'kind': 'Data', 'optional':  True, }, 
        ]
    
        return unTypeConfigDict
    
    
# ACV OJO EXTENSION 2008/09/03
    def generateTypeConfig_Full(self, theClass):
        unTypeConfigDict= {}
         
        unClassName =  self.fClassMetaTypeOrCleanName( theClass)
        unTypeConfigDict[ 'portal_types'] = [ unClassName,]
        unTypeConfigDict[ 'extension']      = 'NonTextAttrsOneParagraph'
        unTypeConfigDict[ 'divider']        = [ 'Before', ]
        unTypeConfigDict[ 'attrs']          = self.generateTypeConfig_Attributes( theClass)
        someTraversalConfigs                = self.generateTypeConfig_Subitems( theClass) + self.generateTypeConfig_Relations( theClass)  + self.generateTypeConfig_References( theClass)
        if someTraversalConfigs:
            someSortedTraversalConfigs = self.fSortTraversalConfigs( theClass, someTraversalConfigs)
            unTypeConfigDict[ 'traversals'] = someSortedTraversalConfigs

        return unTypeConfigDict  


    
# ACV OJO EXTENSION 2008/09/03
    def generateTypeConfig_Attributes(self, theClass):
        someAttrConfigs = [
            { 'name': 'title',             'type': 'String',     'kind': 'Data',   }, 
            { 'name': 'archetype_name',    'type': 'String',     'kind': 'Meta',   }, 
            { 'name': 'description',       'type': 'Text',       'kind': 'Data',  'optional':  True, }, 
            { 'name': 'text',              'type': 'Text',       'kind': 'Data',  'optional':  True,    'hide_label': True, }, 
        ]
        someAttributes = self.getAllAttributeDefs( theClass)
        someNonTextAttributes = [ ]
        someTextAttributes    = [ ]
        for anAttribute in someAttributes:
 
            unExcludeFromTraversalConfig = anAttribute.getTaggedValue( 'exclude_from_traversalconfig', '') == 'True'
            if unExcludeFromTraversalConfig:
                continue

            anAttribType = anAttribute.type.lower()
            if anAttribType == 'computed':
                anAttribType = anAttribute.getTaggedValue( 'computed_types', '')                
            if not (anAttribType in ['text', 'reference', ]) and not (anAttribType.find( '[') >= 0):
                someNonTextAttributes.append( anAttribute)
            elif (anAttribType == 'text' and not ( anAttribute.name in ['description', 'text',])):
                someTextAttributes.append( anAttribute)
                
        unosAttributesToSort = [ [ 'attribute', unAttribute, unAttribute.name, ] for unAttribute in  someNonTextAttributes + someTextAttributes]
           
        unosSortedToGenerate = self.fSortFieldsToGenerate(  theClass, unosAttributesToSort)               

        for aSortedAttribute in unosSortedToGenerate:
            anAttribute =  aSortedAttribute[ 1]
            unaAttributeConfig = None
            if anAttribute in someNonTextAttributes:
                unaAttributeConfig = self.generateAttributeConfig_NonText( anAttribute, theClass)
            elif anAttribute in someTextAttributes:
                unaAttributeConfig = self.generateAttributeConfig_Text(    anAttribute, theClass)
                
            if unaAttributeConfig:
                    someAttrConfigs.append( unaAttributeConfig)
                                    
        return someAttrConfigs

    
    

    
    
    def fNewVoidAttributeConfig(self,):
        unAttributeConfig = {
            'name':             '',  
            'type':             '', 
            'kind':             '',
            'optional':         True,
        }
        
        return unAttributeConfig
    
    
    
# ACV OJO EXTENSION 2008/09/03
    def generateAttributeConfig_NonText(self, theAttribute, theClass):
        
        
        unAttributeConfig = self.fNewVoidAttributeConfig()
        unAttributeConfig.update( {
            'name':             theAttribute.name,  
            'type':             'String', 
            'kind':             'Data',
            'optional':         True,
        } )
        
        anAttribType = theAttribute.type.lower()
        if anAttribType == 'computed':
            anAttribType = theAttribute.getTaggedValue( 'computed_types', '')          
                
        if anAttribType == 'date':
            unAttributeConfig[ 'type']= 'Date'
        elif anAttribType == 'boolean':
            unAttributeConfig[ 'type']= 'Boolean'
        elif anAttribType == 'int':
            unAttributeConfig[ 'type']= 'Number'
        else:
            unAttributeConfig[ 'type']= anAttribType
            
        someForceReadOnlyOnString = theClass.getTaggedValue( 'force_read_only_on') or ''
        someForceReadOnlyOn= []
        if someForceReadOnlyOnString:
            try:
                someForceReadOnlyOn  = eval( someForceReadOnlyOnString) 
            except:
                None

        someForceNoUIChangesOnString = theClass.getTaggedValue( 'force_no_ui_changes_on') or ''
        someForceNoUIChangesOn= []
        if someForceNoUIChangesOnString:
            try:
                someForceNoUIChangesOn  = eval( someForceNoUIChangesOnString) 
            except:
                None
                
        unExcludeFromViewsString  = theAttribute.getTaggedValue( 'exclude_from_views', '')
        unExcludeFromViews= []
        if unExcludeFromViewsString:
            try:
                unExcludeFromViews  = eval( unExcludeFromViewsString) 
            except:
                None
        if unExcludeFromViews:
            unAttributeConfig[ 'exclude_from_views'] = unExcludeFromViews

        unCustomPresentationView  = theAttribute.getTaggedValue( 'custom_presentation_view', '')
        if unCustomPresentationView:
            unAttributeConfig[ 'custom_presentation_view'] = unCustomPresentationView

        if theAttribute.getTaggedValue( 'exclude_from_values_form', False):
            unAttributeConfig[ 'exclude_from_values_form'] = True    
            
        if theAttribute.getTaggedValue( 'exclude_from_values_paragraph', False):
            unAttributeConfig[ 'exclude_from_values_paragraph'] = True    

        unReadOnly  = ((theAttribute.getTaggedValue( 'read_only', '') or '') == str( True)) or ( theAttribute.name in someForceReadOnlyOn)
        if unReadOnly:
            unAttributeConfig[ 'read_only'] = True
            
        if theAttribute.name in someForceNoUIChangesOn:
            unAttributeConfig[ 'no_ui_changes'] = True   
            
        unExcludeFromValuesParagraphWhenString = theAttribute.getTaggedValue( 'exclude_from_values_paragraph_when', '')
        unValueSentinel = object()
        unExcludeFromValuesParagraphWhen = unValueSentinel
        if unExcludeFromValuesParagraphWhenString:
            try:
                unExcludeFromValuesParagraphWhen  = eval( unExcludeFromValuesParagraphWhenString) 
            except:
                None
            if not ( unExcludeFromValuesParagraphWhen == unValueSentinel):
                unAttributeConfig[ 'exclude_from_values_paragraph_when'] = unExcludeFromValuesParagraphWhen    

        return unAttributeConfig
    
        
    
# ACV OJO EXTENSION 2008/09/03
    def generateAttributeConfig_Text(self, theAttribute, theClass):
        unAttributeConfig = self.fNewVoidAttributeConfig()
        unAttributeConfig.update( {
            'name':             theAttribute.name,  
            'type':             'Text', 
            'kind':             'Data',
            'optional':         True,
        } )
        
            
        someForceReadOnlyOnString = theClass.getTaggedValue( 'force_read_only_on') or ''
        someForceReadOnlyOn= []
        if someForceReadOnlyOnString:
            try:
                someForceReadOnlyOn  = eval( someForceReadOnlyOnString) 
            except:
                None
                
        someForceNoUIChangesOnString = theClass.getTaggedValue( 'force_no_ui_changes_on') or ''
        someForceNoUIChangesOn= []
        if someForceNoUIChangesOnString:
            try:
                someForceNoUIChangesOn  = eval( someForceNoUIChangesOnString) 
            except:
                None
                
        
        unExcludeFromViewsString  = theAttribute.getTaggedValue( 'exclude_from_views', '')
        unExcludeFromViews= []
        if unExcludeFromViewsString:
            try:
                unExcludeFromViews  = eval( unExcludeFromViewsString) 
            except:
                None
        if unExcludeFromViews:
            unAttributeConfig[ 'exclude_from_views'] = unExcludeFromViews

        unCustomPresentationView  = theAttribute.getTaggedValue( 'custom_presentation_view', '')
        if unCustomPresentationView:
            unAttributeConfig[ 'custom_presentation_view'] = unCustomPresentationView
            
        unReadOnly  = ((theAttribute.getTaggedValue( 'read_only', '') or '') == str( True)) or  ( theAttribute.name in someForceReadOnlyOn)
        if unReadOnly:
            unAttributeConfig[ 'read_only'] = True
            
        if theAttribute.name in someForceNoUIChangesOn:
            unAttributeConfig[ 'no_ui_changes'] = True   
            
        unExcludeFromValuesParagraphWhenString = theAttribute.getTaggedValue( 'exclude_from_values_paragraph_when', '')
        unValueSentinel = object()
        unExcludeFromValuesParagraphWhen = unValueSentinel
        if unExcludeFromValuesParagraphWhenString:
            try:
                unExcludeFromValuesParagraphWhen  = eval( unExcludeFromValuesParagraphWhenString) 
            except:
                None
            if not ( unExcludeFromValuesParagraphWhen == unValueSentinel):
                unAttributeConfig[ 'exclude_from_values_paragraph_when'] = unExcludeFromValuesParagraphWhen    

        return unAttributeConfig

    
    
    
    
    
    def fClassMetaTypeOrCleanName(self, theClass):
        if not theClass:
            return ''
        unMetaTypeName = theClass.getTaggedValue( 'meta_type_name', '')
        if unMetaTypeName:
            return unMetaTypeName
        unClassName =  theClass.getCleanName()
        return unClassName
    
        

   
        
# ACV OJO EXTENSION 2008/09/03
    def generateTypeConfig_Subitems(self, theClass):
        someSubitemConfigs = [ ]

        someExcludedFromTypeConfigsString = theClass.getTaggedValue( 'exclude_from_typeconfigs') or ''
        someExcludedFromTypeConfigs= []
        if someExcludedFromTypeConfigsString:
            try:
                someExcludedFromTypeConfigs  = eval( someExcludedFromTypeConfigsString) 
            except:
                None

        someForceReadOnlyOnString = theClass.getTaggedValue( 'force_read_only_on') or ''
        someForceReadOnlyOn= []
        if someForceReadOnlyOnString:
            try:
                someForceReadOnlyOn  = eval( someForceReadOnlyOnString) 
            except:
                None

        someForceNoUIChangesOnString = theClass.getTaggedValue( 'force_no_ui_changes_on') or ''
        someForceNoUIChangesOn= []
        if someForceNoUIChangesOnString:
            try:
                someForceNoUIChangesOn  = eval( someForceNoUIChangesOnString) 
            except:
                None
                
        someAggregationsClassesAndEnds = self.getAllAggregationsClassesAndEnds( theClass)
        someAggregationsClassesAndEnds.sort( cmp=lambda a, b: cmp( a[ 3].name, b[ 3].name))    
        for anAssocClassAndEnds in someAggregationsClassesAndEnds:
            anAssociation           = anAssocClassAndEnds[0]
            
            unExcludeFromTraversalConfig = anAssociation.getTaggedValue( 'exclude_from_traversalconfig', '') == 'True'
            if unExcludeFromTraversalConfig:
                continue

            aContainedClass         = anAssocClassAndEnds[1]
            aFromEnd                = anAssocClassAndEnds[2]
            aToEnd                  = anAssocClassAndEnds[3]
            aRelationName           = anAssocClassAndEnds[4]
            anUpperBound            = aToEnd.getUpperBound()
            aToEndName              = aToEnd.getName()
            aFactoryViews            = anAssociation.getTaggedValue( 'factory_views', None)
            unReadOnly              = ((anAssociation.getTaggedValue( 'read_only', '') or '') == str( True)) or ( aToEndName in someForceReadOnlyOn)
            unNoUIChanges           = aToEndName in someForceNoUIChangesOn
            
            if not aToEndName in someExcludedFromTypeConfigs:
                
                aSubItemConfig = { }                
                aSubItemTypeConfig  = {}
                aSubItemConfig['subitems' ] = [ aSubItemTypeConfig ]
                if aFactoryViews:
                    aFactoryViewsDict = None
                    try:
                        aFactoryViewsDict = eval( aFactoryViews)
                    except:
                        None
                    if aFactoryViewsDict:
                        aSubItemConfig[ 'factory_views'] = aFactoryViewsDict
                
                #aCapitalizedToEndName   = aToEndName.capitalize()+aToEnd.getName()[1:]
                unExcludeFromViews      = anAssociation.getTaggedValue( 'exclude_from_views', '')
                unNonFrameworkElements  = anAssociation.getTaggedValue( 'non_framework_elements', '') == 'True'
                someColumnsString   = anAssociation.getTaggedValue( 'columns') or None
                someColumns = []
                if someColumnsString:
                    try:
                        someColumns = eval( someColumnsString)
                    except:
                        None
                if not someColumns:
                    someColumns = []
                    
                someAdditionalColumnsString   = anAssociation.getTaggedValue( 'additional_columns') or None
                someAdditionalColumns = []
                if someAdditionalColumnsString:
                    try:
                        someAdditionalColumns = eval( someAdditionalColumnsString)
                    except:
                        None
                someExcludeColumnsString   = anAssociation.getTaggedValue( 'exclude_columns') or None
                someExcludeColumns = []
                if someExcludeColumnsString:
                    try:
                        someExcludeColumns = eval( someExcludeColumnsString)
                    except:
                        None
                        
                somePortalTypes = [ ]
                if not  aContainedClass.isAbstract():
                    somePortalTypes.append(  self.fClassMetaTypeOrCleanName( aContainedClass))
    
                someAdditionalClasses = aContainedClass.getGenChildren(recursive=1)
                
                for anAdditionalClass in someAdditionalClasses:
                    if not anAdditionalClass.isAbstract():
                        somePortalTypes.append( self.fClassMetaTypeOrCleanName( anAdditionalClass))
                        
                somePortalTypes.sort()
      
                aSubItemTypeConfig[ 'portal_types'] = somePortalTypes
                aSubItemTypeConfig[ 'reuse_config'] = 'Default'

                aSubItemConfig[ 'aggregation_name'] = aToEndName

                if anAssociation.getTaggedValue( 'tabular_tree', '') == 'False':
                    aSubItemConfig[ 'tabular_tree']  = False 
                else:
                    aSubItemConfig[ 'tabular_tree']  = True 
                    
                    
                if not self.getIsCollection( aContainedClass):
                    aSubItemConfig[ 'contains_collections'] = False        
                    aSubItemConfig[ 'tabular_tree']  = False        
                    if anAssociation.getTaggedValue( 'tabular_tree', '') == 'True':
                        aSubItemConfig[ 'tabular_tree']  = True   
                else:
                    aSubItemConfig[ 'contains_collections'] = True        
                    

                someAdditionalElementsInTreeString = anAssociation.getTaggedValue( 'additional_elements_in_tree', '') or''
                if someAdditionalElementsInTreeString:
                    someAdditionalElementsInTree = []
                    try:
                        someAdditionalElementsInTree = eval( someAdditionalElementsInTreeString )
                    except:
                        None
                    if someAdditionalElementsInTree:
                        aSubItemConfig[ 'additional_elements_in_tree']  =  someAdditionalElementsInTree
                        
                if unExcludeFromViews:
                    unExcludeFromViewsList = [ ]
                    try:
                        unExcludeFromViewsList = eval( unExcludeFromViews)  
                    except:
                        None
                    if unExcludeFromViewsList:
                        aSubItemConfig[ 'exclude_from_views']    = unExcludeFromViewsList         
                        
                    unCustomPresentationView  = anAssociation.getTaggedValue( 'custom_presentation_view', '')
                    if unCustomPresentationView:
                        aSubItemConfig[ 'custom_presentation_view'] = unCustomPresentationView
                            
                if unNonFrameworkElements:
                    aSubItemConfig[ 'non_framework_elements'] = unNonFrameworkElements
    
                if not 'description' in someColumns:
                    someColumns = [ 'description', ] + someColumns
                if not 'title' in someColumns:
                    someColumns = [ 'title', ] + someColumns
                if someAdditionalColumns:
                    someColumns += someAdditionalColumns                    
                for aColumn in someExcludeColumns:
                    if aColumn in someColumns:
                        someColumns.remove( aColumn)                        
                aSubItemConfig[ 'columns'] = someColumns
                    
                if unReadOnly:
                    aSubItemConfig[ 'read_only'] = True
                    
                if unNoUIChanges:
                    aSubItemConfig[ 'no_ui_changes'] = True   
                    
                
                someSubitemConfigs.append( aSubItemConfig)

        return someSubitemConfigs
    
        
    
    
    
# ACV OJO EXTENSION 2008/09/03
    def generateTypeConfig_Relations(self, theClass):
        someRelationConfigs = [ ]
        
        someExcludedFromTypeConfigsString = theClass.getTaggedValue( 'exclude_from_typeconfigs') or ''
        someExcludedFromTypeConfigs= []
        if someExcludedFromTypeConfigsString:
            try:
                someExcludedFromTypeConfigs  = eval( someExcludedFromTypeConfigsString) 
            except:
                None
                
        someForceReadOnlyOnString = theClass.getTaggedValue( 'force_read_only_on') or ''
        someForceReadOnlyOn= []
        if someForceReadOnlyOnString:
            try:
                someForceReadOnlyOn  = eval( someForceReadOnlyOnString) 
            except:
                None
                
        someForceNoUIChangesOnString = theClass.getTaggedValue( 'force_no_ui_changes_on') or ''
        someForceNoUIChangesOn= []
        if someForceNoUIChangesOnString:
            try:
                someForceNoUIChangesOn  = eval( someForceNoUIChangesOnString) 
            except:
                None
                
        someNonAggregationsClassesAndEnds = self.getAllNonAggregationsClassesAndEnds( theClass)
        someNonAggregationsClassesAndEnds.sort( cmp=lambda a, b: cmp( a[ 3].getName(), b[ 3].getName()))    
        
        someClassWithSuperClases = self.getAllSuperClasses( theClass)
        
        for anAssocClassAndEnds in someNonAggregationsClassesAndEnds:
 
            anAssociation           = anAssocClassAndEnds[0]
            
            unExcludeFromTraversalConfig = anAssociation.getTaggedValue( 'exclude_from_traversalconfig', '') == 'True'
            if unExcludeFromTraversalConfig:
                continue
            
            aRelatedClass           = anAssocClassAndEnds[1]
            aFromEnd                = anAssocClassAndEnds[2]
            aToEnd                  = anAssocClassAndEnds[3]
            aRelationName           = anAssocClassAndEnds[4]
            anUpperBound            = aToEnd.getUpperBound()
            aToEndName              = aToEnd.getName()
            #aCapitalizedToEndName   = aToEndName.capitalize()+aToEnd.getName()[1:]
            unExcludeFromViews      = anAssociation.getTaggedValue( 'exclude_from_views', '')
            unCandidatesScope       = anAssociation.getTaggedValue( 'candidates_scope', '') 
            unNonFrameworkElements  = anAssociation.getTaggedValue( 'non_framework_elements', '') == 'True'
            unDependencySupplier    = anAssociation.getTaggedValue( 'dependencySupplier', '')
            
            someColumnsString   = anAssociation.getTaggedValue( 'columns') or None
            someColumns = []
            if someColumnsString:
                try:
                    someColumns = eval( someColumnsString)
                except:
                    None
            if not someColumns:
                someColumns = []
            someAdditionalColumnsString   = anAssociation.getTaggedValue( 'additional_columns') or None
            someAdditionalColumns = []
            if someAdditionalColumnsString:
                try:
                    someAdditionalColumns = eval( someAdditionalColumnsString)
                except:
                    None
            someExcludeColumnsString   = anAssociation.getTaggedValue( 'exclude_columns') or None
            someExcludeColumns = []
            if someExcludeColumnsString:
                try:
                    someExcludeColumns = eval( someExcludeColumnsString)
                except:
                    None
                        
            someInverseColumnsString   = anAssociation.getTaggedValue( 'inverse_columns') or None
            someInverseColumns = []
            if someInverseColumnsString:
                try:
                    someInverseColumns = eval( someInverseColumnsString)
                except:
                    None
            if not someInverseColumns:
                someInverseColumns = []
            someInverseAdditionalColumnsString   = anAssociation.getTaggedValue( 'inverse_additional_columns') or None
            someInverseAdditionalColumns = []
            if someInverseAdditionalColumnsString:
                try:
                    someInverseAdditionalColumns = eval( someInverseAdditionalColumnsString)
                except:
                    None
            someInverseExcludeColumnsString   = anAssociation.getTaggedValue( 'inverse_exclude_columns') or None
            someInverseExcludeColumns = []
            if someInverseExcludeColumnsString:
                try:
                    someInverseExcludeColumns = eval( someInverseExcludeColumnsString)
                except:
                    None
                    
            somePortalTypes = [ ]
            if not  aRelatedClass.isAbstract():
                somePortalTypes.append(  self.fClassMetaTypeOrCleanName( aRelatedClass))

            someAdditionalClasses = aRelatedClass.getGenChildren(recursive=1)
            
            for anAdditionalClass in someAdditionalClasses:
                if not anAdditionalClass.isAbstract():
                    somePortalTypes.append(  self.fClassMetaTypeOrCleanName( anAdditionalClass))
                    
            somePortalTypes.sort()
            
            
            if anAssociation.fromEnd.obj in someClassWithSuperClases:
                if not anAssociation.toEnd.name in someExcludedFromTypeConfigs:
                    aRelatedTypeConfig  = {}
                    aRelatedTypeConfig[ 'portal_types'] = somePortalTypes
                    aRelatedTypeConfig[ 'reuse_config'] = 'Default'
                    aRelationConfig = { 'relation_name': anAssociation.toEnd.name, 'related_types': [ aRelatedTypeConfig, ], }
                    unReadOnly              = ((anAssociation.getTaggedValue( 'read_only', '') or '') == str( True)) or ( anAssociation.toEnd.name in someForceReadOnlyOn)
                    unNoUIChanges           = anAssociation.toEnd.name in someForceNoUIChangesOn
                    
                    if unExcludeFromViews:
                        unExcludeFromViewsList = [ ]
                        try:
                            unExcludeFromViewsList = eval( unExcludeFromViews)  
                        except:
                            None
                        if unExcludeFromViewsList:
                            aRelationConfig[ 'exclude_from_views']    = unExcludeFromViewsList     
                            
                    unCustomPresentationView  = anAssociation.getTaggedValue( 'custom_presentation_view', '')
                    if unCustomPresentationView:
                        aRelationConfig[ 'custom_presentation_view'] = unCustomPresentationView
                                                
                    if unCandidatesScope:
                        aRelationConfig[ 'candidates_scope'] = unCandidatesScope
                        
                    if unNonFrameworkElements:
                        aRelationConfig[ 'non_framework_elements'] = unNonFrameworkElements
                        
                    if unDependencySupplier and unDependencySupplier == anAssociation.toEnd.name:
                        aRelationConfig[ 'dependency'] = 'Supplier'
    
                    if not 'description' in someColumns:
                        someColumns = [ 'description', ] + someColumns
                    if not 'title' in someColumns:
                        someColumns = [ 'title', ] + someColumns
                    if someAdditionalColumns:
                        someColumns += someAdditionalColumns                    
                    for aColumn in someExcludeColumns:
                        if aColumn in someColumns:
                            someColumns.remove( aColumn)                        
                    aRelationConfig[ 'columns'] = someColumns

                    if unReadOnly:
                        aRelationConfig[ 'read_only'] = True
                        
                    if unNoUIChanges:
                        aRelationConfig[ 'no_ui_changes'] = True   
                         
                    aFoundExistingRelConfig = False
                    for anExistingRelConfigIndex in range( len( someRelationConfigs)):
                        anExistingRelConfig = someRelationConfigs[ anExistingRelConfigIndex]
                        if anExistingRelConfig[ 'relation_name'] == aRelationConfig[ 'relation_name']:
                            if len( anExistingRelConfig[ 'related_types'][ 0][ 'portal_types']) < len( aRelationConfig[ 'related_types'][ 0][ 'portal_types']):
                                someRelationConfigs[ anExistingRelConfigIndex] = aRelationConfig
                            aFoundExistingRelConfig = True
                            break
                        
                    if not aFoundExistingRelConfig:
                        someRelationConfigs.append( aRelationConfig)

            if  anAssociation.toEnd.obj in someClassWithSuperClases:
                if not anAssociation.fromEnd.name in someExcludedFromTypeConfigs:
                    aRelatedTypeConfig  = {}
                    aRelatedTypeConfig[ 'portal_types'] = somePortalTypes
                    aRelatedTypeConfig[ 'reuse_config'] = 'Default'
                    aRelationConfig = { 'relation_name': anAssociation.fromEnd.name, 'related_types': [ aRelatedTypeConfig, ], }
                    unReadOnly              = ((anAssociation.getTaggedValue( 'read_only', '') or '') == str( True)) or ( anAssociation.fromEnd.name in someForceReadOnlyOn)
                    unNoUIChanges           = anAssociation.fromEnd.name in someForceNoUIChangesOn
                    
                    if unExcludeFromViews:
                        unExcludeFromViewsList = [ ]
                        try:
                            unExcludeFromViewsList = eval( unExcludeFromViews)  
                        except:
                            None
                        if unExcludeFromViewsList:
                            aRelationConfig[ 'exclude_from_views']    = unExcludeFromViewsList  

                    unCustomPresentationView  = anAssociation.getTaggedValue( 'custom_presentation_view', '')
                    if unCustomPresentationView:
                        aRelationConfig[ 'custom_presentation_view'] = unCustomPresentationView
                                                
                    if unCandidatesScope:
                        aRelationConfig[ 'candidates_scope'] = unCandidatesScope
                                     
                    if unNonFrameworkElements:
                        aRelationConfig[ 'non_framework_elements'] = unNonFrameworkElements
                        
                    if unDependencySupplier and unDependencySupplier == anAssociation.fromEnd.name:
                        aRelationConfig[ 'dependency'] = 'Supplier'
                    
                    if not 'description' in someInverseColumns:
                        someInverseColumns = [ 'description', ] + someInverseColumns
                    if not 'title' in someInverseColumns:
                        someInverseColumns = [ 'title', ] + someInverseColumns
                    if someInverseAdditionalColumns:
                        someInverseColumns += someInverseAdditionalColumns                    
                    for aColumn in someInverseExcludeColumns:
                        if aColumn in someInverseColumns:
                            someInverseColumns.remove( aColumn)                        
                    aRelationConfig[ 'columns'] = someInverseColumns
                        
                    if unReadOnly:
                        aRelationConfig[ 'read_only'] = True
                        
                    if unNoUIChanges:
                        aRelationConfig[ 'no_ui_changes'] = True   
                         
                    aFoundExistingRelConfig = False
                    for anExistingRelConfigIndex in range( len( someRelationConfigs)):
                        anExistingRelConfig = someRelationConfigs[ anExistingRelConfigIndex]
                        if anExistingRelConfig[ 'relation_name'] == aRelationConfig[ 'relation_name']:
                            if len( anExistingRelConfig[ 'related_types'][ 0][ 'portal_types']) < len( aRelationConfig[ 'related_types'][ 0][ 'portal_types']):
                                someRelationConfigs[ anExistingRelConfigIndex] = aRelationConfig
                            aFoundExistingRelConfig = True
                            break
                        
                    if not aFoundExistingRelConfig:
                        someRelationConfigs.append( aRelationConfig)
                    
                
        return someRelationConfigs
    

    
  
        
    
# ACV OJO EXTENSION 2008/09/03
    def generateTypeConfig_References(self, theClass):
        someRelationConfigs = [ ]
        someAttributes = self.getAllAttributeDefs( theClass)

        someExcludedFromTypeConfigsString = theClass.getTaggedValue( 'exclude_from_typeconfigs') or ''
        someExcludedFromTypeConfigs= []
        if someExcludedFromTypeConfigsString:
            try:
                someExcludedFromTypeConfigs  = eval( someExcludedFromTypeConfigsString) 
            except:
                None
                
        someForceReadOnlyOnString = theClass.getTaggedValue( 'force_read_only_on') or ''
        someForceReadOnlyOn= []
        if someForceReadOnlyOnString:
            try:
                someForceReadOnlyOn  = eval( someForceReadOnlyOnString) 
            except:
                None

        someForceNoUIChangesOnString = theClass.getTaggedValue( 'force_no_ui_changes_on') or ''
        someForceNoUIChangesOn= []
        if someForceNoUIChangesOnString:
            try:
                someForceNoUIChangesOn  = eval( someForceNoUIChangesOnString) 
            except:
                None
                
                
        for anAttribute in someAttributes:
            
            unExcludeFromTraversalConfig = anAttribute.getTaggedValue( 'exclude_from_traversalconfig', '') == 'True'
            if unExcludeFromTraversalConfig:
                continue
            
            anAttribType = anAttribute.type.lower()
            if (not (anAttribute.name in someExcludedFromTypeConfigs)) and (anAttribType == 'reference' or (anAttribType == 'computed' and ( anAttribute.getTaggedValue( 'computed_types', '').find( '[') >= 0))):

                unReadOnly              = ((anAttribute.getTaggedValue( 'read_only', '') or '') == str( True)) or ( anAttribute.name in someForceReadOnlyOn)
                unNoUIChanges           = anAttribute.name in someForceNoUIChangesOn
                unExcludeFromViews      = anAttribute.getTaggedValue( 'exclude_from_views', '')
                unNonFrameworkElements  = anAttribute.getTaggedValue( 'non_framework_elements', '')

                someColumnsString   = anAttribute.getTaggedValue( 'columns') or None
                someColumns = []
                if someColumnsString:
                    try:
                        someColumns = eval( someColumnsString)
                    except:
                        None
                if not someColumns:
                    someColumns = []

                someAdditionalColumnsString   = anAttribute.getTaggedValue( 'additional_columns') or None
                someAdditionalColumns = []
                if someAdditionalColumnsString:
                    try:
                        someAdditionalColumns = eval( someAdditionalColumnsString)
                    except:
                        None
                someExcludeColumnsString   = anAttribute.getTaggedValue( 'exclude_columns') or None
                someExcludeColumns = []
                if someExcludeColumnsString:
                    try:
                        someExcludeColumns = eval( someExcludeColumnsString)
                    except:
                        None
                
                if anAttribType == 'computed':
                    someReferencedClasses = anAttribute.getTaggedValue( 'computed_types', '') 
                else:
                    someReferencedClasses = anAttribute.getTaggedValue( 'allowed_types', '') 
                        
                unReferencedClassesList = [ ]
                try:
                    unReferencedClassesList = eval( someReferencedClasses)  
                except:
                    None
                if unReferencedClassesList:
                    unReferencedClassesList = [  unNomClase for unNomClase in unReferencedClassesList]
                    unReferencedClassesList.sort()
                    
                    aRelatedTypeConfig  = {}
                    aRelatedTypeConfig[ 'portal_types'] = unReferencedClassesList
                    aRelatedTypeConfig[ 'reuse_config'] = 'Default'
                    aRelationConfig = { 'relation_name': anAttribute.name, 'related_types': [ aRelatedTypeConfig, ], }
        
                    if unExcludeFromViews:
                        unExcludeFromViewsList = [ ]
                        try:
                            unExcludeFromViewsList = eval( unExcludeFromViews)  
                        except:
                            None
                        if unExcludeFromViewsList:
                            aRelationConfig[ 'exclude_from_views']    = unExcludeFromViewsList    
                            
                    unCustomPresentationView  = anAttribute.getTaggedValue( 'custom_presentation_view', '')
                    if unCustomPresentationView:
                        aRelationConfig[ 'custom_presentation_view'] = unCustomPresentationView
                            
                            
                    if unNonFrameworkElements:
                        aRelationConfig[ 'non_framework_elements'] = unNonFrameworkElements
                    
                    if not 'description' in someColumns:
                        someColumns = [ 'description', ] + someColumns
                    if not 'title' in someColumns:
                        someColumns = [ 'title', ] + someColumns
                    if someAdditionalColumns:
                        someColumns += someAdditionalColumns                    
                    for aColumn in someExcludeColumns:
                        if aColumn in someColumns:
                            someColumns.remove( aColumn)                        
                    aRelationConfig[ 'columns'] = someColumns
                
                    if unReadOnly:
                        aRelationConfig[ 'read_only'] = True

                    if unNoUIChanges:
                        aRelationConfig[ 'no_ui_changes'] = True   
                        
                                           
                    someRelationConfigs.append( aRelationConfig)
            
        return someRelationConfigs

    
    
    

    
    
    
    

    
    
# ACV OJO EXTENSION 2009/05/29
    def generateExportConfig(self, thePackage):

        unaClaseRaiz = self.getClaseRaiz( thePackage)
        if not unaClaseRaiz:
            return self
        unNombreClaseRaiz = unaClaseRaiz.name
        
        aFileName = '%s_ExportConfig.py' % unNombreClaseRaiz
        aFilePath = os.path.join( thePackage.getFilePath(), aFileName)
        try:
            aFile =self.makeFile( aFilePath,force=1)
            if not aFile:
                log.info("generateExportConfig failed opening" % str( aFileName))
                return self
            
            aHeaderInfo = self.getHeaderInfo( thePackage)
            aHeaderInfo[ 'file_name'] = aFileName
            aFile.write( """# -*- coding: utf-8 -*-
#
# File: %(file_name)s
#
# %(copyright)s
#
# %(license)s
#
# Authors: 
# %(authors)s
#
#
""" % aHeaderInfo)    
            
            aFile.write( '''
__author__ = """%(authorline)s"""
''' % aHeaderInfo)        

            aFile.write( """
__docformat__ = 'plaintext'

from AccessControl                  import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.%(unProjectName)s.config import *


""" % { 'unProjectName': thePackage.getProductName(), 'unNombreClaseRaiz': unNombreClaseRaiz, } )
            
            
            aFile.write( """
class %s_ExportConfig:            
""" % unNombreClaseRaiz)            
            
            
            aFile.write( '''
    """
    """
    security = ClassSecurityInfo()
    
    
    security.declarePublic('exportConfig')
    def exportConfig( self):
        return ''' % { 'unNC': unNombreClaseRaiz, } )
            
            aExportConfigList    = self.generateExportConfigList( thePackage)
            aExportConfigString  = self.prettyPrintTraversalConfig( aExportConfigList)
            aFile.write( aExportConfigString)
            
        finally:
            if aFile:
                aFile.close()
        return self
    
    
    
    
    
    
# ACV OJO EXTENSION 2009/05/29
    def generateExportConfigList(self, thePackage):
        unasConfigs = []
        
        for unaClass in self.getSortedClasses(  thePackage):
            #skip stub and internal classes
            if unaClass.isInternal() \
                or unaClass.getName() in self.hide_classes \
                or unaClass.isAbstract() \
                or unaClass.getName().lower().startswith('java::') \
                or unaClass.hasStereoType(self.stub_stereotypes, umlprofile=self.uml_profile):
                continue
            
            unasConfigs.append( self.generateTypeExportConfig_Full( unaClass))
  
        return unasConfigs
        
    
    
   
    
# ACV OJO EXTENSION 2009/05/29
    def generateTypeExportConfig_Full(self, theClass):
        unTypeExportConfigDict= {}
         
        unClassName =  self.fClassMetaTypeOrCleanName( theClass)
        unTypeExportConfigDict[ 'portal_types']   = [ unClassName,]
        unTypeExportConfigDict[ 'attrs']          = self.generateTypeExportConfig_Attributes( theClass)
        someExportConfigs                = self.generateTypeExportConfig_Subitems( theClass) + self.generateTypeExportConfig_Relations( theClass)  + self.generateTypeExportConfig_References( theClass)
        if someExportConfigs:
            someSortedExportConfigs = self.fSortTraversalConfigs( theClass, someExportConfigs)
            unTypeExportConfigDict[ 'traversals'] = someSortedExportConfigs

        return unTypeExportConfigDict  


    
# ACV OJO EXTENSION 2009/05/29
    def generateTypeExportConfig_Attributes(self, theClass):
        someNoExportItemsString = theClass.getTaggedValue( 'no_export_items') or ''
        someNoExportItems= []
        if someNoExportItemsString:
            try:
                someNoExportItems  = eval( someNoExportItemsString) 
            except:
                None

        
        someAttrConfigs = [ ]
        
        if not ( 'title' in someNoExportItems):
            someAttrConfigs.append( { 'name': 'title',             'type': 'String',  })
            
        if not ( 'description' in someNoExportItems):
            someAttrConfigs.append( { 'name': 'description',       'type': 'Text',    })

        if not ( 'text' in someNoExportItems):
            someAttrConfigs.append( { 'name': 'text',              'type': 'Text',    })

        someAttributes = self.getAllAttributeDefs( theClass)
        someNonTextAttributes = [ ]
        someTextAttributes    = [ ]
        for anAttribute in someAttributes:
 
            if not ( anAttribute.name) in someNoExportItems:
                
                unExcludeFromExportConfig = anAttribute.getTaggedValue( 'exclude_from_exportconfig', '') == 'True'
                if unExcludeFromExportConfig:
                    continue

                anAttribType = anAttribute.type.lower()
                if anAttribType == 'computed':
                    continue
                
                if not (anAttribType in ['text', 'reference', ]) and not (anAttribType.find( '[') >= 0):
                    someNonTextAttributes.append( anAttribute)
                elif (anAttribType == 'text' and not ( anAttribute.name in ['description', 'text',])):
                    someTextAttributes.append( anAttribute)
                
        unosAttributesToSort = [ [ 'attribute', unAttribute, unAttribute.name, ] for unAttribute in  someNonTextAttributes + someTextAttributes]
           
        unosSortedToGenerate = self.fSortFieldsToGenerate(  theClass, unosAttributesToSort)               

        for aSortedAttribute in unosSortedToGenerate:
            anAttribute =  aSortedAttribute[ 1]
            unaAttributeExportConfig = None
            if anAttribute in someNonTextAttributes:
                unaAttributeExportConfig = self.generateAttributeExportConfig_NonText( anAttribute, theClass)
            elif anAttribute in someTextAttributes:
                unaAttributeExportConfig = self.generateAttributeExportConfig_Text(    anAttribute, theClass)
                
            if ( anAttribute.getTaggedValue( 'is_creation_user', '') == 'True') or ( anAttribute.getTaggedValue( 'is_modification_user', '') == 'True') or ( anAttribute.getTaggedValue( 'is_deletion_user', '') == 'True'):
                unaAttributeExportConfig[ 'is_activity_user'] = True
                
            if ( anAttribute.getTaggedValue( 'is_creation_date', '') == 'True') or ( anAttribute.getTaggedValue( 'is_modification_date', '') == 'True') or ( anAttribute.getTaggedValue( 'is_deletion_date', '') == 'True'):
                unaAttributeExportConfig[ 'is_activity_date'] = True
                
            if ( anAttribute.getTaggedValue( 'is_change_log', '') == 'True') or ( anAttribute.getTaggedValue( 'is_change_counter', '') == 'True') or ( anAttribute.getTaggedValue( 'is_sources_counters', '') == 'True'):
                unaAttributeExportConfig[ 'is_activity_counter'] = True
                
            if anAttribute.getTaggedValue( 'is_inter_version', '').lower() == 'true':
                unaAttributeExportConfig[ 'is_inter_version'] = True
                
                
            if unaAttributeExportConfig:
                someAttrConfigs.append( unaAttributeExportConfig)
                                    
        return someAttrConfigs

    
    

    
    
    def fNewVoidAttributeExportConfig(self,):
        unAttributeExportConfig = {
            'name':             '',  
            'type':             '', 
         }
        
        return unAttributeExportConfig
    
    
    
# ACV OJO EXTENSION 2009/05/29
    def generateAttributeExportConfig_NonText(self, theAttribute, theClass):
        
        unNoExport  = ((theAttribute.getTaggedValue( 'no_export', '') or '') == str( True)) 
        if unNoExport:
            return None
        
        unAttributeExportConfig = self.fNewVoidAttributeExportConfig()
        unAttributeExportConfig.update( {
            'name':             theAttribute.name,  
            'type':             'String', 
        } )
        
        anAttribType = theAttribute.type.lower()
        if anAttribType == 'computed':
            return None
                
        if anAttribType == 'date':
            unAttributeExportConfig[ 'type']= 'Date'
        elif anAttribType == 'boolean':
            unAttributeExportConfig[ 'type']= 'Boolean'
        elif anAttribType == 'int':
            unAttributeExportConfig[ 'type']= 'Number'
        else:
            unAttributeExportConfig[ 'type']= anAttribType
            
        return unAttributeExportConfig
    
        
    
# ACV OJO EXTENSION 2009/05/29
    def generateAttributeExportConfig_Text(self, theAttribute, theClass):
        unNoExport  = ((theAttribute.getTaggedValue( 'no_export', '') or '') == str( True))
        if unNoExport:
            return None

        unAttributeExportConfig = self.fNewVoidAttributeExportConfig()
        unAttributeExportConfig.update( {
            'name':             theAttribute.name,  
            'type':             'Text', 
        } )
            
            
        return unAttributeExportConfig
        
    

   
        
# ACV OJO EXTENSION 2009/05/29
    def generateTypeExportConfig_Subitems(self, theClass):
        someSubitemConfigs = [ ]

 
        someNoExportItemsString = theClass.getTaggedValue( 'no_export_items') or ''
        someNoExportItems= []
        if someNoExportItemsString:
            try:
                someNoExportItems  = eval( someNoExportItemsString) 
            except:
                None

               
        someAggregationsClassesAndEnds = self.getAllAggregationsClassesAndEnds( theClass)
        someAggregationsClassesAndEnds.sort( cmp=lambda a, b: cmp( a[ 3].name, b[ 3].name))    
        for anAssocClassAndEnds in someAggregationsClassesAndEnds:
            anAssociation           = anAssocClassAndEnds[0]
            
            unExcludeFromExportConfig = anAssociation.getTaggedValue( 'exclude_from_exportconfig', '') == 'True'
            if unExcludeFromExportConfig:
                continue
 
            aContainedClass         = anAssocClassAndEnds[1]
            aFromEnd                = anAssocClassAndEnds[2]
            aToEnd                  = anAssocClassAndEnds[3]
            aRelationName           = anAssocClassAndEnds[4]
            anUpperBound            = aToEnd.getUpperBound()
            aToEndName              = aToEnd.getName()
            aFactoryViews            = anAssociation.getTaggedValue( 'factory_views', None)
            
            if not (aToEndName in someNoExportItems):
                
                aSubItemConfig = { }                
                aSubItemTypeExportConfig  = {}
                aSubItemConfig['subitems' ] = [ aSubItemTypeExportConfig ]
                if aFactoryViews:
                    aFactoryViewsDict = None
                    try:
                        aFactoryViewsDict = eval( aFactoryViews)
                    except:
                        None
                    if aFactoryViewsDict:
                        aSubItemConfig[ 'factory_views'] = aFactoryViewsDict
                
                #aCapitalizedToEndName   = aToEndName.capitalize()+aToEnd.getName()[1:]
                unNonFrameworkElements  = anAssociation.getTaggedValue( 'non_framework_elements', '') == 'True'
                        
                somePortalTypes = [ ]
                if not  aContainedClass.isAbstract():
                    somePortalTypes.append(  self.fClassMetaTypeOrCleanName( aContainedClass))
    
                someAdditionalClasses = aContainedClass.getGenChildren(recursive=1)
                
                for anAdditionalClass in someAdditionalClasses:
                    if not anAdditionalClass.isAbstract():
                        somePortalTypes.append( self.fClassMetaTypeOrCleanName( anAdditionalClass))
                        
                somePortalTypes.sort()
      
                aSubItemTypeExportConfig[ 'portal_types'] = somePortalTypes
                aSubItemTypeExportConfig[ 'reuse_config'] = 'Default'

                aSubItemConfig[ 'aggregation_name'] = aToEndName
                              
                if not self.getIsCollection( aContainedClass):
                    aSubItemConfig[ 'contains_collections'] = False        
                    aSubItemConfig[ 'tabular_tree']  = False        
                    if anAssociation.getTaggedValue( 'tabular_tree', '') == 'True':
                        aSubItemConfig[ 'tabular_tree']  = True   
                else:
                    aSubItemConfig[ 'contains_collections'] = True        
                
                if anAssociation.getTaggedValue( 'tabular_tree', '') == 'False':
                    aSubItemConfig[ 'tabular_tree']  = False 
                else:
                    aSubItemConfig[ 'tabular_tree']  = True 
                                  
                if unNonFrameworkElements:
                    aSubItemConfig[ 'non_framework_elements'] = unNonFrameworkElements
                    
                someSubitemConfigs.append( aSubItemConfig)

        return someSubitemConfigs
    
        
    
    
    
# ACV OJO EXTENSION 2009/05/29
    def generateTypeExportConfig_Relations(self, theClass):
        someRelationConfigs = [ ]
        
        someNoExportItemsString = theClass.getTaggedValue( 'no_export_items') or ''
        someNoExportItems= []
        if someNoExportItemsString:
            try:
                someNoExportItems  = eval( someNoExportItemsString) 
            except:
                None

                
        someNonAggregationsClassesAndEnds = self.getAllNonAggregationsClassesAndEnds( theClass)
        someNonAggregationsClassesAndEnds.sort( cmp=lambda a, b: cmp( a[ 3].getName(), b[ 3].getName()))    
        
        someClassWithSuperClases = self.getAllSuperClasses( theClass)
        
        for anAssocClassAndEnds in someNonAggregationsClassesAndEnds:
 
            anAssociation           = anAssocClassAndEnds[0]
             
            unExcludeFromExportConfig = anAssociation.getTaggedValue( 'exclude_from_exportconfig', '') == 'True'
            if unExcludeFromExportConfig:
                continue
             
            aRelatedClass           = anAssocClassAndEnds[1]
            aFromEnd                = anAssocClassAndEnds[2]
            aToEnd                  = anAssocClassAndEnds[3]
            aRelationName           = anAssocClassAndEnds[4]
            anUpperBound            = aToEnd.getUpperBound()
            aToEndName              = aToEnd.getName()
            #aCapitalizedToEndName   = aToEndName.capitalize()+aToEnd.getName()[1:]
            unExcludeFromViews      = anAssociation.getTaggedValue( 'exclude_from_views', '')
            unCandidatesScope       = anAssociation.getTaggedValue( 'candidates_scope', '') 
            unNonFrameworkElements  = anAssociation.getTaggedValue( 'non_framework_elements', '') == 'True'
            unDependencySupplier    = anAssociation.getTaggedValue( 'dependencySupplier', '')
                                
            somePortalTypes = [ ]
            if not  aRelatedClass.isAbstract():
                somePortalTypes.append(  self.fClassMetaTypeOrCleanName( aRelatedClass))

            someAdditionalClasses = aRelatedClass.getGenChildren(recursive=1)
            
            for anAdditionalClass in someAdditionalClasses:
                if not anAdditionalClass.isAbstract():
                    somePortalTypes.append( self.fClassMetaTypeOrCleanName( anAdditionalClass))
                    
            somePortalTypes.sort()
            
            
            if anAssociation.fromEnd.obj in someClassWithSuperClases:
                if not ( anAssociation.toEnd.name in someNoExportItems):
                    aRelatedTypeExportConfig  = {}
                    aRelatedTypeExportConfig[ 'portal_types'] = somePortalTypes
                    aRelatedTypeExportConfig[ 'reuse_config'] = 'Default'
                    aRelationConfig = { 'relation_name': anAssociation.toEnd.name, 'related_types': [ aRelatedTypeExportConfig, ], }
                
                    if unCandidatesScope:
                        aRelationConfig[ 'candidates_scope'] = unCandidatesScope
                       
                    if unNonFrameworkElements:
                        aRelationConfig[ 'non_framework_elements'] = unNonFrameworkElements
                            
                    aFoundExistingRelConfig = False
                    for anExistingRelConfigIndex in range( len( someRelationConfigs)):
                        anExistingRelConfig = someRelationConfigs[ anExistingRelConfigIndex]
                        if anExistingRelConfig[ 'relation_name'] == aRelationConfig[ 'relation_name']:
                            if len( anExistingRelConfig[ 'related_types'][ 0][ 'portal_types']) < len( aRelationConfig[ 'related_types'][ 0][ 'portal_types']):
                                someRelationConfigs[ anExistingRelConfigIndex] = aRelationConfig
                            aFoundExistingRelConfig = True
                            break
                        
                    if not aFoundExistingRelConfig:
                        someRelationConfigs.append( aRelationConfig)

            if  anAssociation.toEnd.obj in someClassWithSuperClases:
                if not ( anAssociation.fromEnd.name in someNoExportItems):
                    aRelatedTypeExportConfig  = {}
                    aRelatedTypeExportConfig[ 'portal_types'] = somePortalTypes
                    aRelatedTypeExportConfig[ 'reuse_config'] = 'Default'
                    aRelationConfig = { 'relation_name': anAssociation.fromEnd.name, 'related_types': [ aRelatedTypeExportConfig, ], }

                    if unCandidatesScope:
                        aRelationConfig[ 'candidates_scope'] = unCandidatesScope
                    
                    if unNonFrameworkElements:
                        aRelationConfig[ 'non_framework_elements'] = unNonFrameworkElements
                        
                    aFoundExistingRelConfig = False
                    for anExistingRelConfigIndex in range( len( someRelationConfigs)):
                        anExistingRelConfig = someRelationConfigs[ anExistingRelConfigIndex]
                        if anExistingRelConfig[ 'relation_name'] == aRelationConfig[ 'relation_name']:
                            if len( anExistingRelConfig[ 'related_types'][ 0][ 'portal_types']) < len( aRelationConfig[ 'related_types'][ 0][ 'portal_types']):
                                someRelationConfigs[ anExistingRelConfigIndex] = aRelationConfig
                            aFoundExistingRelConfig = True
                            break
                        
                    if not aFoundExistingRelConfig:
                        someRelationConfigs.append( aRelationConfig)
                    
                
        return someRelationConfigs
    

    
  
        
    
# ACV OJO EXTENSION 2009/05/29
    def generateTypeExportConfig_References(self, theClass):
        someRelationConfigs = [ ]
        someAttributes = self.getAllAttributeDefs( theClass)

        someNoExportItemsString = theClass.getTaggedValue( 'no_export_items') or ''
        someNoExportItems= []
        if someNoExportItemsString:
            try:
                someNoExportItems  = eval( someNoExportItemsString) 
            except:
                None
  
                
                
        for anAttribute in someAttributes:
            
            unExcludeFromExportConfig = anAttribute.getTaggedValue( 'exclude_from_exportconfig', '') == 'True'
            if unExcludeFromExportConfig:
                continue
 
            anAttribType = anAttribute.type.lower()
            if (not (anAttribute.name in someNoExportItems)) and (anAttribType == 'reference' or (anAttribType == 'computed' and ( anAttribute.getTaggedValue( 'computed_types', '').find( '[') >= 0))):

                unNonFrameworkElements  = anAttribute.getTaggedValue( 'non_framework_elements', '')

                
                if anAttribType == 'computed':
                    continue
                
                someReferencedClasses = anAttribute.getTaggedValue( 'allowed_types', '') 
                        
                unReferencedClassesList = [ ]
                try:
                    unReferencedClassesList = eval( someReferencedClasses)  
                except:
                    None
                if unReferencedClassesList:
                    unReferencedClassesList = [  unNomClase for unNomClase in unReferencedClassesList]
                    unReferencedClassesList.sort()
                    
                    aRelatedTypeExportConfig  = {}
                    aRelatedTypeExportConfig[ 'portal_types'] = unReferencedClassesList
                    aRelationConfig = { 'relation_name': anAttribute.name, 'related_types': [ aRelatedTypeExportConfig, ], }
                            
                    if unNonFrameworkElements:
                        aRelationConfig[ 'non_framework_elements'] = unNonFrameworkElements
                                           
                    someRelationConfigs.append( aRelationConfig)
            
        return someRelationConfigs

        
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    
    
# ACV OJO EXTENSION 2009/05/29
    def generateCopyConfig(self, thePackage):

        unaClaseRaiz = self.getClaseRaiz( thePackage)
        if not unaClaseRaiz:
            return self
        unNombreClaseRaiz = unaClaseRaiz.name
        
        aFileName = '%s_CopyConfig.py' % unNombreClaseRaiz
        aFilePath = os.path.join( thePackage.getFilePath(), aFileName)
        try:
            aFile =self.makeFile( aFilePath,force=1)
            if not aFile:
                log.info("generateCopyConfig failed opening" % str( aFileName))
                return self
            
            aHeaderInfo = self.getHeaderInfo( thePackage)
            aHeaderInfo[ 'file_name'] = aFileName
            aFile.write( """# -*- coding: utf-8 -*-
#
# File: %(file_name)s
#
# %(copyright)s
#
# %(license)s
#
# Authors: 
# %(authors)s
#
#
""" % aHeaderInfo)    
            
            aFile.write( '''
__author__ = """%(authorline)s"""
''' % aHeaderInfo)        

            aFile.write( """
__docformat__ = 'plaintext'

from AccessControl                  import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.%(unProjectName)s.config import *


""" % { 'unProjectName': thePackage.getProductName(), 'unNombreClaseRaiz': unNombreClaseRaiz, } )
            
            
            aFile.write( """
class %s_CopyConfig:            
""" % unNombreClaseRaiz)            
            
            
            aFile.write( '''
    """
    """
    security = ClassSecurityInfo()
    
    
    security.declarePublic('copyConfig')
    def copyConfig( self):
        return ''' % { 'unNC': unNombreClaseRaiz, } )
            
            aCopyConfigList    = self.generateCopyConfigList( thePackage)
            aCopyConfigString  = self.prettyPrintTraversalConfig( aCopyConfigList)
            aFile.write( aCopyConfigString)
            
        finally:
            if aFile:
                aFile.close()
        return self
    
    
    
    
    
    
# ACV OJO EXTENSION 2009/05/29
    def generateCopyConfigList(self, thePackage):
        unasConfigs = []
        
        for unaClass in self.getSortedClasses(  thePackage):
            #skip stub and internal classes
            if unaClass.isInternal() \
                or unaClass.getName() in self.hide_classes \
                or unaClass.isAbstract() \
                or unaClass.getName().lower().startswith('java::') \
                or unaClass.hasStereoType(self.stub_stereotypes, umlprofile=self.uml_profile):
                continue
            
            unasConfigs.append( self.generateTypeCopyConfig_Full( unaClass))
  
        return unasConfigs
        
    
    
   
    
# ACV OJO EXTENSION 2009/05/29
    def generateTypeCopyConfig_Full(self, theClass):
        unTypeCopyConfigDict= {}
         
        unClassName =  self.fClassMetaTypeOrCleanName( theClass)
        unTypeCopyConfigDict[ 'portal_types']   = [ unClassName,]
        unTypeCopyConfigDict[ 'attrs']          = self.generateTypeCopyConfig_Attributes( theClass)
        someCopyConfigs                = self.generateTypeCopyConfig_Subitems( theClass) + self.generateTypeCopyConfig_Relations( theClass)  + self.generateTypeCopyConfig_References( theClass)
        if someCopyConfigs:
            someSortedCopyConfigs = self.fSortTraversalConfigs( theClass, someCopyConfigs)
            unTypeCopyConfigDict[ 'traversals'] = someSortedCopyConfigs

        return unTypeCopyConfigDict  


    
# ACV OJO EXTENSION 2009/05/29
    def generateTypeCopyConfig_Attributes(self, theClass):
        
        someNoCopyItemsString = theClass.getTaggedValue( 'no_copy_items') or ''
        someNoCopyItems= []
        if someNoCopyItemsString:
            try:
                someNoCopyItems  = eval( someNoCopyItemsString) 
            except:
                None

        
        someAttrConfigs = [ ]
        
        if not ( 'title' in someNoCopyItems):
            someAttrConfigs.append( { 'name': 'title',             'type': 'String',  })
            
        if not ( 'description' in someNoCopyItems):
            someAttrConfigs.append( { 'name': 'description',       'type': 'Text',    })

        if not ( 'text' in someNoCopyItems):
            someAttrConfigs.append( { 'name': 'text',              'type': 'Text',    })
      
        someAttributes = self.getAllAttributeDefs( theClass)
        someNonTextAttributes = [ ]
        someTextAttributes    = [ ]
        for anAttribute in someAttributes:

            if not ( anAttribute.name in someNoCopyItems):
                
                unExcludeFromCopyConfig = anAttribute.getTaggedValue( 'exclude_from_copyconfig', '') == 'True'
                if unExcludeFromCopyConfig:
                    continue
                
                anAttribType = anAttribute.type.lower()
                if anAttribType == 'computed':
                    continue
                
                if not (anAttribType in ['text', 'reference', ]) and not (anAttribType.find( '[') >= 0):
                    someNonTextAttributes.append( anAttribute)
                elif (anAttribType == 'text' and not ( anAttribute.name in ['description', 'text',])):
                    someTextAttributes.append( anAttribute)
                
        unosAttributesToSort = [ [ 'attribute', unAttribute, unAttribute.name, ] for unAttribute in  someNonTextAttributes + someTextAttributes]
           
        unosSortedToGenerate = self.fSortFieldsToGenerate(  theClass, unosAttributesToSort)               

        for aSortedAttribute in unosSortedToGenerate:
            anAttribute =  aSortedAttribute[ 1]
            unaAttributeCopyConfig = None
            if anAttribute in someNonTextAttributes:
                unaAttributeCopyConfig = self.generateAttributeCopyConfig_NonText( anAttribute, theClass)
            elif anAttribute in someTextAttributes:
                unaAttributeCopyConfig = self.generateAttributeCopyConfig_Text(    anAttribute, theClass)
                
            if unaAttributeCopyConfig:
                    someAttrConfigs.append( unaAttributeCopyConfig)
                                    
        return someAttrConfigs

    
    

    
    
    def fNewVoidAttributeCopyConfig(self,):
        unAttributeCopyConfig = {
            'name':             '',  
            'type':             '', 
         }
        
        return unAttributeCopyConfig
    
    
    
# ACV OJO EXTENSION 2009/05/29
    def generateAttributeCopyConfig_NonText(self, theAttribute, theClass):
        
        unNoCopy  = ((theAttribute.getTaggedValue( 'no_copy', '') or '') == str( True)) 
        if unNoCopy:
            return None
        
        
        unAttributeCopyConfig = self.fNewVoidAttributeCopyConfig()
        unAttributeCopyConfig.update( {
            'name':             theAttribute.name,  
            'type':             'String', 
        } )
        
        if theAttribute.getTaggedValue( 'do_not_copy') == 'True':
            unAttributeCopyConfig[ 'do_not_copy'] = True

        anAttribType = theAttribute.type.lower()
        if anAttribType == 'computed':
            return None
                
        if anAttribType == 'date':
            unAttributeCopyConfig[ 'type']= 'Date'
        elif anAttribType == 'boolean':
            unAttributeCopyConfig[ 'type']= 'Boolean'
        elif anAttribType == 'int':
            unAttributeCopyConfig[ 'type']= 'Number'
        else:
            unAttributeCopyConfig[ 'type']= anAttribType
            
        return unAttributeCopyConfig
    
        
    
# ACV OJO EXTENSION 2009/05/29
    def generateAttributeCopyConfig_Text(self, theAttribute, theClass):
        unNoCopy  = ((theAttribute.getTaggedValue( 'no_copy', '') or '') == str( True))
        if unNoCopy:
            return None

        unAttributeCopyConfig = self.fNewVoidAttributeCopyConfig()
        unAttributeCopyConfig.update( {
            'name':             theAttribute.name,  
            'type':             'Text', 
        } )
            
        if theAttribute.getTaggedValue( 'do_not_copy') == 'True':
            unAttributeCopyConfig[ 'do_not_copy'] = True
            
        return unAttributeCopyConfig
        
    

   
        
# ACV OJO EXTENSION 2009/05/29
    def generateTypeCopyConfig_Subitems(self, theClass):
        someSubitemConfigs = [ ]

 
        someNoCopyItemsString = theClass.getTaggedValue( 'no_copy_items') or ''
        someNoCopyItems= []
        if someNoCopyItemsString:
            try:
                someNoCopyItems  = eval( someNoCopyItemsString) 
            except:
                None

               
        someAggregationsClassesAndEnds = self.getAllAggregationsClassesAndEnds( theClass)
        someAggregationsClassesAndEnds.sort( cmp=lambda a, b: cmp( a[ 3].name, b[ 3].name))    
        for anAssocClassAndEnds in someAggregationsClassesAndEnds:
            anAssociation           = anAssocClassAndEnds[0]
 
            unExcludeFromCopyConfig = anAssociation.getTaggedValue( 'exclude_from_copyconfig', '') == 'True'
            if unExcludeFromCopyConfig:
                continue
            
            aContainedClass         = anAssocClassAndEnds[1]
            aFromEnd                = anAssocClassAndEnds[2]
            aToEnd                  = anAssocClassAndEnds[3]
            aRelationName           = anAssocClassAndEnds[4]
            anUpperBound            = aToEnd.getUpperBound()
            aToEndName              = aToEnd.getName()
            aFactoryViews            = anAssociation.getTaggedValue( 'factory_views', None)
            
            if not (aToEndName in someNoCopyItems):
                
                aSubItemConfig = { }                
                aSubItemTypeCopyConfig  = {}
                aSubItemConfig['subitems' ] = [ aSubItemTypeCopyConfig ]
                if aFactoryViews:
                    aFactoryViewsDict = None
                    try:
                        aFactoryViewsDict = eval( aFactoryViews)
                    except:
                        None
                    if aFactoryViewsDict:
                        aSubItemConfig[ 'factory_views'] = aFactoryViewsDict
                
                #aCapitalizedToEndName   = aToEndName.capitalize()+aToEnd.getName()[1:]
                unNonFrameworkElements  = anAssociation.getTaggedValue( 'non_framework_elements', '') == 'True'
                        
                somePortalTypes = [ ]
                if not  aContainedClass.isAbstract():
                    somePortalTypes.append(  self.fClassMetaTypeOrCleanName( aContainedClass))
    
                someAdditionalClasses = aContainedClass.getGenChildren(recursive=1)
                
                for anAdditionalClass in someAdditionalClasses:
                    if not anAdditionalClass.isAbstract():
                        somePortalTypes.append( self.fClassMetaTypeOrCleanName( anAdditionalClass))
                        
                somePortalTypes.sort()
      
                aSubItemTypeCopyConfig[ 'portal_types'] = somePortalTypes
                aSubItemTypeCopyConfig[ 'reuse_config'] = 'Default'

                aSubItemConfig[ 'aggregation_name'] = aToEndName
                              
                
                if anAssociation.getTaggedValue( 'tabular_tree', '') == 'False':
                    aSubItemConfig[ 'tabular_tree']  = False 
                else:
                    aSubItemConfig[ 'tabular_tree']  = True 
                    
                if not self.getIsCollection( aContainedClass):
                    aSubItemConfig[ 'contains_collections'] = False        
                    aSubItemConfig[ 'tabular_tree']  = False        
                    if anAssociation.getTaggedValue( 'tabular_tree', '') == 'True':
                        aSubItemConfig[ 'tabular_tree']  = True   
                else:
                    aSubItemConfig[ 'contains_collections'] = True        
                
                if unNonFrameworkElements:
                    aSubItemConfig[ 'non_framework_elements'] = unNonFrameworkElements
                    
                someSubitemConfigs.append( aSubItemConfig)

        return someSubitemConfigs
    
        
    
    
    
# ACV OJO EXTENSION 2009/05/29
    def generateTypeCopyConfig_Relations(self, theClass):
        someRelationConfigs = [ ]
        
        someNoCopyItemsString = theClass.getTaggedValue( 'no_copy_items') or ''
        someNoCopyItems= []
        if someNoCopyItemsString:
            try:
                someNoCopyItems  = eval( someNoCopyItemsString) 
            except:
                None

                
        someNonAggregationsClassesAndEnds = self.getAllNonAggregationsClassesAndEnds( theClass)
        someNonAggregationsClassesAndEnds.sort( cmp=lambda a, b: cmp( a[ 3].getName(), b[ 3].getName()))    
        
        someClassWithSuperClases = self.getAllSuperClasses( theClass)
        
        for anAssocClassAndEnds in someNonAggregationsClassesAndEnds:
 
            anAssociation           = anAssocClassAndEnds[0]
             
            unExcludeFromCopyConfig = anAssociation.getTaggedValue( 'exclude_from_copyconfig', '') == 'True'
            if unExcludeFromCopyConfig:
                continue
            
            someDoNotCopyAssocEndString = anAssociation.getTaggedValue( 'do_not_copy', '')
            someDoNotCopyAssocEndNames = []
            if someDoNotCopyAssocEndString:
                try:
                    someDoNotCopyAssocEndNames = eval( someDoNotCopyAssocEndString)
                except:
                    None
                
            unIsAcrossRoots = anAssociation.getTaggedValue( 'is_across_roots', False)
                    
            unIsIsomorphic = anAssociation.getTaggedValue( 'is_isomorphic', False)
            
            aRelatedClass           = anAssocClassAndEnds[1]
            aFromEnd                = anAssocClassAndEnds[2]
            aToEnd                  = anAssocClassAndEnds[3]
            aRelationName           = anAssocClassAndEnds[4]
            anUpperBound            = aToEnd.getUpperBound()
            aFromEndName            = aFromEnd.getName()
            aToEndName              = aToEnd.getName()
            #aCapitalizedToEndName   = aToEndName.capitalize()+aToEnd.getName()[1:]
            unExcludeFromViews      = anAssociation.getTaggedValue( 'exclude_from_views', '')
            unCandidatesScope       = anAssociation.getTaggedValue( 'candidates_scope', '') 
            unNonFrameworkElements  = anAssociation.getTaggedValue( 'non_framework_elements', '') == 'True'
            unDependencySupplier    = anAssociation.getTaggedValue( 'dependencySupplier', '')
                                
            somePortalTypes = [ ]
            if unIsIsomorphic:
                somePortalTypes =  [ self.fClassMetaTypeOrCleanName( theClass) , ]
            else:
                if not  aRelatedClass.isAbstract():
                    somePortalTypes.append(  self.fClassMetaTypeOrCleanName( aRelatedClass))
    
                someAdditionalClasses = aRelatedClass.getGenChildren(recursive=1)
                
                for anAdditionalClass in someAdditionalClasses:
                    if not anAdditionalClass.isAbstract():
                        somePortalTypes.append( self.fClassMetaTypeOrCleanName( anAdditionalClass))
                        
                        
                somePortalTypes.sort()
            
            
            if anAssociation.fromEnd.obj in someClassWithSuperClases:
                if not ( anAssociation.toEnd.name in someNoCopyItems):
                    aRelatedTypeCopyConfig  = {}
                    aRelatedTypeCopyConfig[ 'portal_types'] = somePortalTypes
                    aRelatedTypeCopyConfig[ 'reuse_config'] = 'Default'
                    aRelationConfig = { 'relation_name': anAssociation.toEnd.name, 'related_types': [ aRelatedTypeCopyConfig, ], }
                
                    if unCandidatesScope:
                        aRelationConfig[ 'candidates_scope'] = unCandidatesScope
                       
                    if unNonFrameworkElements:
                        aRelationConfig[ 'non_framework_elements'] = unNonFrameworkElements
                            
                    if  anAssociation.toEnd.name in someDoNotCopyAssocEndNames:
                        aRelationConfig[ 'do_not_copy'] = True
                        
                    if unIsAcrossRoots:
                        aRelationConfig[ 'is_across_roots'] = True
                        
                    
                    aFoundExistingRelConfig = False
                    for anExistingRelConfigIndex in range( len( someRelationConfigs)):
                        anExistingRelConfig = someRelationConfigs[ anExistingRelConfigIndex]
                        if anExistingRelConfig[ 'relation_name'] == aRelationConfig[ 'relation_name']:
                            if len( anExistingRelConfig[ 'related_types'][ 0][ 'portal_types']) < len( aRelationConfig[ 'related_types'][ 0][ 'portal_types']):
                                someRelationConfigs[ anExistingRelConfigIndex] = aRelationConfig
                            aFoundExistingRelConfig = True
                            break
                        
                    if not aFoundExistingRelConfig:
                        someRelationConfigs.append( aRelationConfig)

            if  anAssociation.toEnd.obj in someClassWithSuperClases:
                if not ( anAssociation.fromEnd.name in someNoCopyItems):
                    aRelatedTypeCopyConfig  = {}
                    aRelatedTypeCopyConfig[ 'portal_types'] = somePortalTypes
                    aRelatedTypeCopyConfig[ 'reuse_config'] = 'Default'
                    aRelationConfig = { 'relation_name': anAssociation.fromEnd.name, 'related_types': [ aRelatedTypeCopyConfig, ], }

                    if unCandidatesScope:
                        aRelationConfig[ 'candidates_scope'] = unCandidatesScope
                    
                    if unNonFrameworkElements:
                        aRelationConfig[ 'non_framework_elements'] = unNonFrameworkElements
                        
                    if anAssociation.fromEnd.name in someDoNotCopyAssocEndNames:
                        aRelationConfig[ 'do_not_copy'] = True

                    if unIsAcrossRoots:
                        aRelationConfig[ 'is_across_roots'] = True

                    aFoundExistingRelConfig = False
                    for anExistingRelConfigIndex in range( len( someRelationConfigs)):
                        anExistingRelConfig = someRelationConfigs[ anExistingRelConfigIndex]
                        if anExistingRelConfig[ 'relation_name'] == aRelationConfig[ 'relation_name']:
                            if len( anExistingRelConfig[ 'related_types'][ 0][ 'portal_types']) < len( aRelationConfig[ 'related_types'][ 0][ 'portal_types']):
                                someRelationConfigs[ anExistingRelConfigIndex] = aRelationConfig
                            aFoundExistingRelConfig = True
                            break
                        
                    if not aFoundExistingRelConfig:
                        someRelationConfigs.append( aRelationConfig)
                    
                
        return someRelationConfigs
    

    
  
        
    
# ACV OJO EXTENSION 2009/05/29
    def generateTypeCopyConfig_References(self, theClass):
        someRelationConfigs = [ ]
        someAttributes = self.getAllAttributeDefs( theClass)

        someNoCopyItemsString = theClass.getTaggedValue( 'no_copy_items') or ''
        someNoCopyItems= []
        if someNoCopyItemsString:
            try:
                someNoCopyItems  = eval( someNoCopyItemsString) 
            except:
                None
  
                
                
        for anAttribute in someAttributes:
            
            unExcludeFromCopyConfig = anAttribute.getTaggedValue( 'exclude_from_copyconfig', '') == 'True'
            if unExcludeFromCopyConfig:
                continue

            anAttribType = anAttribute.type.lower()
            if (not (anAttribute.name in someNoCopyItems)) and (anAttribType == 'reference' or (anAttribType == 'computed' and ( anAttribute.getTaggedValue( 'computed_types', '').find( '[') >= 0))):

                unNonFrameworkElements  = anAttribute.getTaggedValue( 'non_framework_elements', '')

                
                if anAttribType == 'computed':
                    continue
                
                someReferencedClasses = anAttribute.getTaggedValue( 'allowed_types', '') 
                        
                unReferencedClassesList = [ ]
                try:
                    unReferencedClassesList = eval( someReferencedClasses)  
                except:
                    None
                if unReferencedClassesList:
                    unReferencedClassesList = [  unNomClase for unNomClase in unReferencedClassesList]
                    unReferencedClassesList.sort()
                    
                    aRelatedTypeCopyConfig  = {}
                    aRelatedTypeCopyConfig[ 'portal_types'] = unReferencedClassesList
                    aRelationConfig = { 'relation_name': anAttribute.name, 'related_types': [ aRelatedTypeCopyConfig, ], }
                            
                    if unNonFrameworkElements:
                        aRelationConfig[ 'non_framework_elements'] = unNonFrameworkElements
                                           
                    someRelationConfigs.append( aRelationConfig)
            
        return someRelationConfigs

        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# ACV OJO EXTENSION 2008/09/03
    def prettyPrintTraversalConfig(self, theTraversalConfigList):
    
        anOutput = StringIO()
        
        self.prettyPrintList( anOutput, theTraversalConfigList, 0, theIndentAtStart = True, theFinalComa=False)
        aResult = anOutput.getvalue()
        return aResult
    
    
    
    def fElementTypeName( self, theElement):
        unTypePrefix = "<type '"
        unStr = str( theElement.__class__)        
        
        if not unStr.startswith( unTypePrefix):
            return ""
        
        unTypeNameEndIndex = unStr.find( "'", len( unTypePrefix))
        if not unTypeNameEndIndex:
            unTypeNameEndIndex = len( unStr)
        
        unTypeName = unStr[ len( unTypePrefix): unTypeNameEndIndex]
        return unTypeName
        

    
    
    def fAreAllElementsStrings(self, theList):
        for unElement in theList:
            if not ( self.fElementTypeName( unElement) == 'str'):
                return False
        return True
    
    
    def fAreAllElementsAllElementsStrings(self, theList):
        for unElement in theList:
            if not self.fElementTypeName( unElement) == 'list':
                return False
            
            if not self.fAreAllElementsStrings( unElement):
                return False
        return True
   
    
    def prettyPrintList(self, theOutput, theList, theIndentLevel, theIndentAtStart = True, theFinalComa = True):
        if theIndentAtStart:
            theOutput.write(  cIndent *  theIndentLevel)
            
        theOutput.write( '[')
        
        unTodosStrings = self.fAreAllElementsStrings( theList)
        
        if unTodosStrings:
            theOutput.write( ' ')
            for unElement in theList:
                theOutput.write( "'%s', " % unElement)
            theOutput.write( "],\n")     
        else:
            if self.fAreAllElementsAllElementsStrings( theList):
                unosMaxWidths = []
                for unaSubList in theList:
                    for unSubElementIndex in range( 0, len( unaSubList)):
                        if len( unosMaxWidths) <= unSubElementIndex:
                            unosMaxWidths.append( 0)
                        unSubElement = unaSubList[ unSubElementIndex]
                        if len( unSubElement) > unosMaxWidths[ unSubElementIndex]:
                            unosMaxWidths[ unSubElementIndex] = len( unSubElement)    
                        
                theOutput.write( '\n')
                for unaSubList in theList:
                    theOutput.write(  cIndent *  (theIndentLevel + 1))
                    theOutput.write( '[ ')
#                    theOutput.write(  cIndent[0: len( cIndent) -1])
                    for unSubElementIndex in range( 0, len( unaSubList)):
                        unSubElement = unaSubList[ unSubElementIndex]
                        theOutput.write( "'%s', " % unSubElement)
                        if len( unSubElement) < unosMaxWidths[ unSubElementIndex]:
                            theOutput.write(  ' ' * (unosMaxWidths[ unSubElementIndex] - len( unSubElement)) )
                    theOutput.write( ' ],\n')
                    
                theOutput.write(  cIndent *  theIndentLevel)
                theOutput.write( "],\n")     

            else:
                theOutput.write( "\n") 
                for unElement in theList:
                    unElementTypeName = self.fElementTypeName( unElement)
                    if unElementTypeName == 'str':
                        theOutput.write(  cIndent *  (theIndentLevel + 1))
                        theOutput.write( "'%s',\n" % unElement)
                    elif unElementTypeName == 'list':
                        self.prettyPrintList( theOutput, unElement, theIndentLevel + 1,  theIndentAtStart = True)
                    elif unElementTypeName == 'dict':
                        self.prettyPrintDict( theOutput, unElement, theIndentLevel + 1)
                    elif unElementTypeName == 'bool':
                        theOutput.write( "%s,\n" % str( unElement))
                    else:
                        theOutput.write( "'%s',\n" % str( unElement))
                
                theOutput.write(  cIndent *  theIndentLevel)
                if theFinalComa:
                    theOutput.write( "],\n")     
                else:
                    theOutput.write( "]\n")     
                    
        return self      

    
    def fSortedConfigDictKeys( self, theKeys):
        someOrderedKeys = []
        someOtherKeys = []

        for unaKey in cConfigDictKeysPreferedOrder:
            if unaKey in theKeys:
                someOrderedKeys.append( unaKey)

        for unaKey in theKeys:
            if not( unaKey in someOrderedKeys):
                someOtherKeys.append( unaKey)
                                
        someOrderedKeys.extend( sorted( someOtherKeys))
        return someOrderedKeys
        
  
    def prettyPrintDict(self, theOutput, theDict, theIndentLevel):
        theOutput.write(  cIndent *  theIndentLevel)
        theOutput.write( '{')
    
        unasKeys = self.fSortedConfigDictKeys( theDict.keys())
        
        unaMaxKeyLen = 0
        for unaKey in unasKeys:
            if len( unaKey) > unaMaxKeyLen:
                unaMaxKeyLen = len( unaKey)       
    
        for unaKey in unasKeys:
                
            unElement = theDict[ unaKey]
            
            if unaKey == unasKeys[ 0]:
                theOutput.write(  cIndent[0: len( cIndent) -1] )
            else:
                theOutput.write(  cIndent *  (theIndentLevel + 1))
                
            theOutput.write(  "'%s': " % unaKey)
            
            if len( unaKey) < unaMaxKeyLen:
                theOutput.write(  ' ' * (unaMaxKeyLen - len( unaKey)) )
                 
            unElementTypeName = self.fElementTypeName( unElement)
            if unElementTypeName == 'str':
                theOutput.write( "'%s',\n" % unElement)
            elif unElementTypeName == 'list':
                self.prettyPrintList( theOutput, unElement, theIndentLevel + 1, theIndentAtStart = False)
            elif unElementTypeName == 'dict':
                self.prettyPrintDict( theOutput, unElement, theIndentLevel + 1)
            elif unElementTypeName == 'bool':
                theOutput.write( "%s,\n" % str( unElement))
            else:
                theOutput.write( "'%s',\n" % str( unElement))

    
    
        theOutput.write(  cIndent *  theIndentLevel)
        theOutput.write( "},\n")     
        return self
    
        
    
    
# ACV OJO EXTENSION 2008/10/17
    def generateMeta(self, thePackage):

        unaClaseRaiz = self.getClaseRaiz( thePackage)
        if not unaClaseRaiz:
            return self
        unNombreClaseRaiz = unaClaseRaiz.name
        
        aFileName = '%s_Meta.py' % unNombreClaseRaiz
        aFilePath = os.path.join( thePackage.getFilePath(), aFileName)
        try:
            aFile =self.makeFile( aFilePath,force=1)
            if not aFile:
                log.info("generateMeta failed opening" % str( aFileName))
                return self
            
            aHeaderInfo = self.getHeaderInfo( thePackage)
            aFile.write( """
# %(copyright)s
#
# %(license)s
#
# Authors: 
# %(authors)s
#
#
""" % aHeaderInfo)    
            
            aFile.write( '''
__author__ = """%(authorline)s"""
''' % aHeaderInfo)        

            aFile.write( """
__docformat__ = 'plaintext'

from AccessControl                  import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.%(unProjectName)s.config import *


# Classes added here during runtime will be acceptable roots,
# after invocation of the fParentArchetypeClassNames_ResetCache method
#
gAdditionalParentArchetypeClassNames = [ ]



# Private Cache of class names
# 
gParentArchetypeClassNamesCache      = [ ]



""" % { 'unNombreClaseRaiz': unNombreClaseRaiz, 'unProjectName': thePackage.getProductName(), })
            
            
            aFile.write( """
class %s_Meta:            
""" % unNombreClaseRaiz)            
            
            
            aFile.write( '''
    """
    """
    security = ClassSecurityInfo()


    



  
  
  
    security.declarePrivate('fParentArchetypeClassNames')
    def fParentArchetypeClassNames( self):
    
        if gParentArchetypeClassNamesCache:
            return gParentArchetypeClassNamesCache
        
        return self.fParentArchetypeClassNames_ResetCache()
        
        
        
        
        
        
        
    security.declarePrivate('fParentArchetypeClassNames_ResetCache')
    def fParentArchetypeClassNames_ResetCache( self):
    
        aWorkingCopy = self.fArchetypeClassNames()[:]
        
        # Thread safety to be assured here for cases when simultaneusly:
        #
        # Others may be adding to the gAdditionalParentArchetypeClassNames
        # Others may also invoke this method
        #
        if gAdditionalParentArchetypeClassNames:
            aWorkingCopy += gAdditionalParentArchetypeClassNames
        
        gParentArchetypeClassNamesCache = aWorkingCopy
        
        return gParentArchetypeClassNamesCache
        
            
    
    
    
    security.declarePrivate('fArchetypeSchemaByName')
    def fArchetypeSchemaByName( self, theMetaTypeName):
        if not theMetaTypeName:
            return None    
    
        aMetaType = self.fArchetypeClassByName( theMetaTypeName)
        if not aMetaType:
            return None
        return getattr( aMetaType, 'schema', None)
  

    security.declarePrivate('fArchetypeClassNames')
    def fArchetypeClassNames( self):
        return [ 
%(archetypes_names)s 
        ]
        
        
                    
    security.declarePrivate('fArchetypeClassByName')
    def fArchetypeClassByName( self, theMetaTypeName):
        if not theMetaTypeName:
            return None    

        try:            
            %(archetypes_lines)s
        except:
            None
       
        return None
            
''' % { 
        'unNC': unNombreClaseRaiz,  
        'archetypes_names' : self.generateMeta_ArchetypeNames( thePackage ), 
        'archetypes_lines' : self.generateMeta_ArchetypesLines( thePackage ), 
    })

        finally:
            if aFile:
                aFile.close()
                
        return self
    

    
    
    
    def getSortedClasses(self, thePackage):
        someClasses = thePackage.getClasses()
        someSortedClasses = sorted( someClasses, lambda a,b: cmp(a.name, b.name))
        return someSortedClasses
    
    
    
# ACV OJO EXTENSION 2008/10/17
    def generateMeta_ArchetypeNames(self, thePackage):
        unosArchetypesNames = ''
        for unaClass in self.getSortedClasses( thePackage):
            #skip stub and internal classes
            if unaClass.isInternal() \
                or unaClass.getName() in self.hide_classes \
                or unaClass.isAbstract() \
                or unaClass.getName().lower().startswith('java::') \
                or unaClass.hasStereoType(self.stub_stereotypes, umlprofile=self.uml_profile):
                continue
            
            unosArchetypesNames += "            '%s',\n" % unaClass.name
  
        return unosArchetypesNames
    
        
       
     
    
    
# ACV OJO EXTENSION 2008/10/17
    def generateMeta_ArchetypesLines(self, thePackage):
        unasArchetypesLines = ''
        for unaClass in self.getSortedClasses( thePackage):
            #skip stub and internal classes
            if unaClass.isInternal() \
                or unaClass.getName() in self.hide_classes \
                or unaClass.isAbstract() \
                or unaClass.getName().lower().startswith('java::') \
                or unaClass.hasStereoType(self.stub_stereotypes, umlprofile=self.uml_profile):
                continue
            
            unasArchetypesLines += """
            if theMetaTypeName == '%(unNC)s':
                from Products.%(unProjectName)s.%(unNC)s         import %(unNC)s
                return %(unNC)s            
""" % { 'unNC': unaClass.name, 'unProjectName': thePackage.getProductName(), }           
  
        return unasArchetypesLines
    
        
    
    
    
    
# ACV OJO EXTENSION 2008/09/03
    def generateTypeConfig_Mention(self, theClass):
        unTypeConfigDict= {}
         
        unTypeConfigDict[ 'portal_types'] = [ theClass.getCleanName(),]
        unTypeConfigDict[ 'config_name'] = 'Mention'
        unTypeConfigDict[ 'mode'] = 'Reference'
        unTypeConfigDict[ 'extension'] = 'OneParagraph'
        unTypeConfigDict[ 'attrs'] = [
            { 'name': 'title',             'type': 'String',     'kind': 'Data',  }, 
            { 'name': 'archetype_name',    'type': 'String',     'kind': 'Meta',  }, 
            { 'name': 'description',       'type': 'Text',       'kind': 'Data', 'optional':  True, }, 
        ]
    
        return unTypeConfigDict
 



# ###################################################################################
# ACV OJO FIX 2008/04/30
#
#   Problem:
#       ArchetypesGenerator.ArchetypesGenerator.generateRelations() and generateRelation() 
#       fails to generate in relations.xml 
#       multiple allowedSourceType elements or multiple allowedTargetType elements
#       for specialization classes of related classes
#
#   Prerequisites:
#
#   When:
#       In an Argo UML model with classes related through associations
#       and the classes have specializations classes
#
#
#   Sample error output:
#		<Ruleset id="Guias_detallan_Reglamento" uid="-64--88-1-33-76a6eb09:1199c527f27:-8000:0000000000000DD0">
#			<TypeConstraint id="type_constraint">
#				<allowedSourceType>
#					Guia
#				</allowedSourceType>
#				<allowedTargetType>
#					Reglamento
#				</allowedTargetType>
#			</TypeConstraint>
#			<InverseImplicator id="inverse_relation">
#				<inverseRuleset uidref="reglamentos_guias"/>
#			</InverseImplicator>
#		</Ruleset>
#
#   Sample corrected output:
#		<Ruleset id="Guias_detallan_Reglamento" uid="-64--88-1-33-76a6eb09:1199c527f27:-8000:0000000000000DD0">
#			<TypeConstraint id="type_constraint">
#				<allowedSourceType>
#					Guia
#				</allowedSourceType>
#				<allowedTargetType>
#					Reglamento
#				</allowedTargetType>
#				<allowedTargetType>
#					Procedimento
#				</allowedTargetType>
#				<allowedTargetType>
#					ProcedimentoSimple
#				</allowedTargetType>
#				<allowedTargetType>
#					Norma
#				</allowedTargetType>
#			</TypeConstraint>
#			<InverseImplicator id="inverse_relation">
#				<inverseRuleset uidref="reglamentos_guias"/>
#			</InverseImplicator>
#		</Ruleset>
#
#   Diagnosis:
#       The code ignores the specialization classes, when generating the relations.xml
#
#   Fix:
#      To add additional elements to the XML file, for each specialization class of source or target classes
#      Both to the "direct" and "inverse" relationship rule sets
#
#   New code marked in the file as 
# OJO ACV EXTENSION Polymorphic relations Begin
#





    def generateRelations(self, package):
        doc=minidom.Document()
        lib=doc.createElement('RelationsLibrary')
        doc.appendChild(lib)
        coll=doc.createElement('RulesetCollection')
        coll.setAttribute('id',package.getCleanName())
        lib.appendChild(coll)
        package.num_generated_relations=0
        assocs = package.getAssociations(recursive=1)
        processed = [] # xxx hack and workaround, not solution, avoids double
                        # generation of relations
        #import pdb; pdb.set_trace()
        for assoc in assocs:
            if assoc in processed:
                continue
            processed.append(assoc)
            if self.getOption('relation_implementation',assoc,'basic') != 'relations':
                continue

            source=assoc.fromEnd.obj
            target=assoc.toEnd.obj

            targetcard=list(assoc.toEnd.mult)
            sourcecard=list(assoc.fromEnd.mult)
            sourcecard[0]=None #temporary pragmatic fix
            targetcard[0]=None #temporary pragmatic fix
            #print 'relation:',assoc.getName(),'target cardinality:',targetcard,'sourcecard:',sourcecard
            sourcetype=None
            targettype=None
            sourceinterface=None
            targetinterface=None

# OJO ACV EXTENSION Polymorphic relations Begin
            unosAdditionalSourceTypeNames=[]
            unosAdditionalTargetTypeNames=[]
# OJO ACV EXTENSION End


            if source.isInterface():
                sourceinterface=source.getCleanName()
            else:
                sourcetype=source.getCleanName()
# OJO ACV EXTENSION Polymorphic relations Begin
                unosAdditionalSourceTypeNames=source.getGenChildrenNames(recursive=1)
                #print
                #print "sourcetype=%s                        source=%s" % ( str( sourcetype), str( source),)
                #print "additional=%s" % str(unosAdditionalSourceTypeNames)                 
# OJO ACV EXTENSION End


            if target.isInterface():
                targetinterface=target.getCleanName()
            else:
                targettype=target.getCleanName()
# OJO ACV EXTENSION Polymorphic relations Begin
                unosAdditionalTargetTypeNames=target.getGenChildrenNames(recursive=1)
                #print "targettype=%s                        target=%s" % ( str( targettype), str( target),)
                #print "additional=%s" % str(unosAdditionalTargetTypeNames) 
# OJO ACV EXTENSION End

            inverse_relation_name = assoc.getTaggedValue('inverse_relation_name', None)
            if not inverse_relation_name and assoc.fromEnd.isNavigable:
                if self.getOption('old_inverse_relation_name', assoc, None):
                    # BBB
                    inverse_relation_name = '%s_inverse' % assoc.getCleanName()
                else:
                    fromEndName = assoc.fromEnd.getName(ignore_cardinality=1)
                    toEndName = assoc.toEnd.getName(ignore_cardinality=1)
                    if fromEndName == toEndName:
                        inverse_relation_name =  '%s_inv' % assoc.getCleanName()
                    else:
                        inverse_relation_name =  '%s_%s' % (toEndName.lower(), fromEndName.lower())

            assocclassname=getattr(assoc,'isAssociationClass',0) and assoc.getCleanName() or assoc.getTaggedValue('association_class') or self.getOption('association_class',assoc,None)
            self.generateRelation(doc, coll,
                                  assoc.getCleanName(),
                                  assoc.getId(),
                                  sourcetype=sourcetype,
                                  targettype=targettype,
                                  sourceinterface=sourceinterface,
                                  targetinterface=targetinterface,
                                  sourcecardinality=sourcecard,
                                  targetcardinality=targetcard,

                                  assocclassname=assocclassname,
                                  inverse_relation_id=inverse_relation_name,
                                  primary=1,
# OJO ACV EXTENSION Polymorphic relations Begin               
additionalSourceTypeNames=unosAdditionalSourceTypeNames,
additionalTargetTypeNames=unosAdditionalTargetTypeNames,
# OJO ACV EXTENSION End
)

            #create the counterrelation
            if inverse_relation_name:
                self.generateRelation(doc, coll,
                                      inverse_relation_name,
                                      inverse_relation_name,
                                      sourcetype=targettype,
                                      targettype=sourcetype,
                                      sourceinterface=targetinterface,
                                      targetinterface=sourceinterface,
                                      sourcecardinality=targetcard,
                                      targetcardinality=sourcecard,

                                      assocclassname=assocclassname,
                                      inverse_relation_id=assoc.getId(),
# OJO ACV EXTENSION Polymorphic relations Begin               
additionalSourceTypeNames=unosAdditionalTargetTypeNames,
additionalTargetTypeNames=unosAdditionalSourceTypeNames,
# OJO ACV EXTENSION End
)

            # ATVM integration - by jensens
            # very special case: create a vocabulary with the association name
            # this is needed for some use-cases, where a association class has
            # use an vocabulary with the name ofthe relation

            if utils.isTGVTrue(self.getOption('association_vocabulary', assoc, '0')):
                # remember this vocab-name and if set its portal_type
                currentproduct = package.getProductName()
                if not currentproduct in self.vocabularymap.keys():
                    self.vocabularymap[currentproduct] = {}
                type = self.getOption('association_vocabularytype', assoc, 'SimpleVocabulary')
                if not assoc.getCleanName() in self.vocabularymap[currentproduct].keys():
                    self.vocabularymap[currentproduct][assoc.getCleanName()] = (
                        type,
                        'SimpleVocabularyTerm'
                    )
                else:
                    print "warning: vocabulary with name %s defined more than once." % assoc.getCleanName()
                if inverse_relation_name and not inverse_relation_name in self.vocabularymap[currentproduct].keys():
                    self.vocabularymap[currentproduct][inverse_relation_name] = (
                        type,
                        'SimpleVocabularyTerm'
                    )                    

            #/ATVM

            package.num_generated_relations += 1

        if package.num_generated_relations:
            of=self.makeFile(os.path.join(package.getFilePath(),'relations.xml'))
            print >>of,doc.toprettyxml()
            of.close()

    def generateProduct(self, root):
        dirMode=0
        outfile=None

        if self.generate_packages and root.getCleanName() not in self.generate_packages:
            log.info("%sSkipping package '%s'.",
                     '    '*self.infoind,
                     root.getCleanName())
            return

        dirMode=1
        if root.hasStereoType(self.stub_stereotypes, umlprofile=self.uml_profile):
            log.debug("Skipping stub Product '%s'.",
                      root.getName())
            return

        log.info("Starting new Product: '%s'.",
                 root.getName())

        # increment indent of output
        self.infoind += 1

        # before generate a Product we need to push the current permissions on a
        # stack in orderto reinitialize the permissions
        self.creation_permission_stack.append(self.creation_permissions)
        self.creation_permissions = []

        #create the directories
        self.makeDir(root.getFilePath())
        self.makeDir(os.path.join(root.getFilePath(),'skins'))
        self.makeDir(os.path.join(root.getFilePath(),'skins',
                                  root.getProductModuleName()))
        # [reinout:] I removed the creation of /skins/..._public/
        of = self.makeFile(os.path.join(root.getFilePath(), 'skins',
                                        root.getProductModuleName(), 'readme.txt'))
        print >> of, READMELOWEST % root.getProductName()
        of.close()

        # prepare messagecatalog
        if has_i18ndude and self.build_msgcatalog:
            self.makeDir(os.path.join(root.getFilePath(), 'i18n'))
            filepath = os.path.join(root.getFilePath(), 'i18n', 'generated.pot')
            if not os.path.exists(filepath):
                templdir = os.path.join(sys.path[0], 'templates')
                PotTemplate = open(os.path.join(sys.path[0], 'templates', 'generated.pot')).read()
                authors, emails, authorline = self.getAuthors(root)
                PotTemplate = PotTemplate % {
                    'author':', '.join(authors) or 'unknown author',
                    'email':', '.join([email[1:-1] for email in emails]) or 'unknown@email.address',
                    'year': str(time.localtime()[0]),
                    'datetime': time.ctime(),
                    'charset': 'UTF-8',
                    'package': root.getProductName(),
                }
                of = self.makeFile(filepath)
                of.write(PotTemplate)
                of.close()
            self.msgcatstack.append(msgcatalog.MessageCatalog(
                filename=os.path.join(self.targetRoot, filepath)))

        package = root
        if self.noclass:
            # skip the other generation steps
            return
        self.generateRelations(root)
        self.generatePackage(root)
        
# ACV OJO ADDITION 20080906
        self.generateTraversalConfig( root)
        
        
# ACV OJO ADDITION 200090529
        self.generateExportConfig( root)
        
        
# ACV OJO ADDITION 200090529
        self.generateCopyConfig( root)
        
# ACV OJO ADDITION 20081017
        self.generateMeta( root)

# ACV OJO ADDITION 20080903
        self.generateI118Ncatalogs( root)


        if self.ape_support:
            self.generateApeConf(root.getFilePath(),root)

        #start Workflow creation
        wfg = WorkflowGenerator(package, self)
        wfg.generateWorkflows()

        # write messagecatalog
        if has_i18ndude and self.build_msgcatalog:
            filepath = os.path.join(root.getFilePath(), 'i18n', 'generated.pot')
            of = self.makeFile(filepath) or open(filepath, 'w')
            pow = msgcatalog.POWriter(of, self.msgcatstack.pop())
            pow.write(sort=True, msgstrToComment=True)
            of.close()

        # post-creation
        self.infoind -= 1
        self.creation_permissions = self.creation_permission_stack.pop()

    def parseAndGenerate(self):

        # and now start off with the class files
        self.generatedModules=[]

        suff = os.path.splitext(self.xschemaFileName)[1].lower()
        log.info("Parsing...")
        if not self.noclass:
            if suff.lower() in ('.xmi','.xml', '.uml'):
                log.debug("Opening xmi...")
                self.root = root= XMIParser.parse(self.xschemaFileName,
                                                  packages=self.parse_packages,
                                                  generator=self,
                                                  generate_datatypes=self.generate_datatypes)
                log.debug("Created a root XMI parser.")
            elif suff.lower() in ('.zargo','.zuml','.zip'):
                log.debug("Opening %s ..." % suff.lower())
                zf=ZipFile(self.xschemaFileName)
                xmis=[n for n in zf.namelist() if os.path.splitext(n)[1].lower()in ['.xmi','.xml']]
                assert(len(xmis)==1)
                buf=zf.read(xmis[0])
                self.root=root=XMIParser.parse(xschema=buf,
                                               packages=self.parse_packages, generator=self,
                                               generate_datatypes=self.generate_datatypes)
            else:
                raise TypeError,'input file not of type .xmi, .xml, .zargo, .zuml'

            if self.outfilename:
                log.debug("We've got an self.outfilename: %s.",
                          self.outfilename)
                lastPart = os.path.split(self.outfilename)[1]
                log.debug("We've split off the last directory name: %s.",
                          lastPart)
                # [Reinout 2006-11-05]: We're not setting the root's
                # name from the outfilename anymore. That prevents
                # (amongst others) Optilude from generating some
                # product into a directory named "trunk", for
                # instance.
                #root.setName(lastPart)
                #log.debug("Set the name of the root generator to that"
                #          " directory name.")
                existingName = root.getName()
                if not existingName == lastPart:
                    log.warn("Not setting the product's name to '%s', "
                             "this was the old behaviour. Just name your "
                             "class diagram according to your product "
                             "name. ",
                             lastPart)
                root.setOutputDirectoryName(self.outfilename)
            else:
                log.debug("No outfilename present, not changing the "
                          "name of the root generator.")
            log.info("Directory in which we're generating the files: '%s'.",
                     self.outfilename)
        else:
            self.root=root=DummyModel(self.outfilename)
        log.info('Generating...')
        if self.method_preservation:
            log.debug('Method bodies will be preserved')
        else:
            log.debug('Method bodies will be overwritten')
        if not has_enhanced_strip_support:
            log.warn("Can't build i18n message catalog. Needs 'python 2.3' or later.")
        if self.build_msgcatalog and not has_i18ndude:
            log.warn("Can't build i18n message catalog. Module 'i18ndude' not found.")
        if not XMIParser.has_stripogram:
            log.warn("Can't strip html from doc-strings. Module 'stripogram' not found.")
        self.generateProduct(root)
        
        