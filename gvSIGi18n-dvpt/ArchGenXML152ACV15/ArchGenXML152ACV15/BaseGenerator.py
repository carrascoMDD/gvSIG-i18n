#-----------------------------------------------------------------------------
# Name:        BaseGenerator.py
# Purpose:     provide some common methods for the generator
#
# Author:      Jens Klein
#
# Created:     2005-01-10
# RCS-ID:      $Id: BaseGenerator.py 3411 2005-01-05 01:55:45Z yenzenz $
# Copyright:   (c) 2005-2006 BlueDynamics Alliance, Austria
# Licence:     GPL
#-----------------------------------------------------------------------------

class DummyMarker:
    pass
_marker = DummyMarker()

import os
import time
import logging
from StringIO import StringIO

from documenttemplate.documenttemplate import HTML

import utils
from codesnippets import *

import XMIParser, PyParser
from UMLProfile import UMLProfile

log = logging.getLogger("basegenerator")


class BaseGenerator:
    """Abstract base class for the different concrete generators."""

    uml_profile = UMLProfile()
    uml_profile.addStereoType('z3', ['XMIInterface'],
        dispatching=1,
        generator='generateZope3Interface',
        template='zope3_interface.py',
        description='Generate this interface class as zope 3 interface. This '
                    'will inherit from zope.interface.Interface.')

    uml_profile.addStereoType('python_class', ['XMIClass'],
        dispatching=1,
        generator='generatePythonClass',
        template='python_class.py',
        description='Generate this class as a plain python class '
                    'instead of as an Archetypes class.')

    uml_profile.addStereoType('zope_class', ['XMIClass'],
        dispatching=1,
        generator='generateZopeClass',
        template='zope_class.py',
        description='Generate this class as a plain Zope class '
                    'instead of as an Archetypes class.')

    default_class_type = 'python_class'
    default_interface_type = 'z3'
    
    # indent helper for log output:
    infoind = 0

    def isTGVTrue(self,v):
        return utils.isTGVTrue(v)

    def isTGVFalse(self,v):
        return utils.isTGVFalse(v)

    def getUMLProfile(self):
        return self.uml_profile

    def getDefaultClassType(self):
        return self.getUMLProfile().getStereoType(self.default_class_type)

    def getDefaultInterfaceType(self):
        return self.getUMLProfile().getStereoType(self.default_interface_type)

    def processExpression(self, value, asString=True):
        """Process the string returned by tagged values.

        * python: prefixes a python expression
        * string: prefixes a string
        * fallback to default, which is string, if asString isnt set to False
        """
        if value.startswith('python:'):
            return value[7:]
        elif value.startswith('string:'):
            return "'%s'" % value[7:]
        if asString:
            return "'%s'" % value
        else:
            return value

    def getOption(self, option, element, default=_marker, aggregate=False):
        """Query element for value of an option.

        Query a certain option for an element including 'acquisition':
        search the element, then the packages upwards, then global
        options.
        """
        log.debug("Trying to get value of option '%s' for element '%s' "
                  "(default value is '%s', aggregate is '%s').",
                  option, element.name, default, aggregate)
        if element:
            o = element
            log.debug("Found the element.")
            # Climb up the hierarchy
            aggregator = ''

            while o:
                if o.hasTaggedValue(option):
                    log.debug("The element has a matching tagged value.")
                    value = o.getTaggedValue(option)
                    log.debug("The value is '%s'.",
                              value)
                    if aggregate:
                        log.debug("Adding the value to the aggregate.")
                        # Create a multiline string
                        aggregator += o.getTaggedValue(option)+'\n'
                    else:
                        log.debug("Returning value.")
                        return o.getTaggedValue(option)
                o = o.getParent()
                if o:
                    log.debug("Trying our parent: %s.", o.name)
            if aggregator:
                log.debug("Didn't find anything, return the current aggregated value.")
                return aggregator
            else:
                log.debug("Found nothing in the assorted taggedvalues.")

        # Look in the options
        log.debug("Now looking in the options.")
        if hasattr(self, option):
            log.debug("Found a matching option (passed on the commandline or in the configfile).")
            value = getattr(self, option)
            log.debug("The value is '%s'.",
                      value)
            return value

        if default != _marker:
            log.debug("Returning default value '%s'.",
                      default)
            return default
        else:
            message = "option '%s' is mandatory for element '%s'" % (option, element and element.getName())
            log.error(message)
            raise ValueError, message

    def cleanName(self, name):
        return name.replace(' ','_').replace('.','_').replace('/','_')

    def parsePythonModule(self, packagePath, fileName):
        """Parse a python module and return the module object.

        This can then be passed to getProtectedSection() to
        generate protected sections.
        """

        targetPath = os.path.join(self.targetRoot, packagePath, fileName)
        parsed = None

        if self.method_preservation:
            try:
                parsed = PyParser.PyModule(targetPath)
            except IOError:
                pass
            except :
                print
                print '***'
                print '***Error while reparsing the file', targetPath
                print '***'
                print
                raise

        return parsed

    def getProtectedSection(self, parsed, section, ind=0):
        """Given a parsed python module and a section name, return a string
        with the protected code-section to be included in the generated module.
        """

        outstring = utils.indent(PyParser.PROTECTED_BEGIN, ind) + ' ' + \
                            section +u' #fill in your manual code here\n'
        if parsed:
            sectioncode = parsed.getProtectedSection(section)
            if sectioncode:
                outstring += sectioncode + '\n'

        outstring += utils.indent(PyParser.PROTECTED_END, ind) + u' ' + section + u'\n'
        return outstring

    def generateProtectedSection(self, outfile, element, section, indent=0):
        if self.getOption('manual_code_sections', element, None):
            parsed = self.parsed_class_sources.get(element.getPackage().getFilePath() + \
                u'/'+element.getName(), None)
            print >> outfile, self.getProtectedSection(parsed, section, indent).encode('utf-8')

    def generateDependentImports(self, element):
        outfile = StringIO()
        package = element.getPackage()

        # Imports for stub-association classes
        importLines = []

        parents = element.getGenParents()
        parents += element.getRealizationParents()
        parents += element.getClientDependencyClasses(includeParents=True)

        for p in parents:

            if p.hasStereoType(self.stub_stereotypes):
                # In principle, don't do a thing, but...
                if p.getTaggedValue('import_from', None):
                    print >> outfile,'from %s import %s' % \
                          (p.getTaggedValue('import_from'), p.getName())
                # Just a comment to keep someone from accidentally moving
                # below 'else' to the wrong column :-)
            else:
                print >> outfile,'from %s import %s' % (
                    p.getQualifiedModuleName(
                        None,
                        forcePluginRoot=self.force_plugin_root,
                        includeRoot=0,
                    ),
                    p.getName())

        assocs = element.getFromAssociations()
        element.hasAssocClass = 0
        for p in assocs:
            if getattr(p,'isAssociationClass',0):
                # get import_from and add it to importLines
                module = p.getTaggedValue('import_from', None)
                if module:
                    importLine = 'from %s import %s' % (module, p.getName())
                    importLines.append(importLine)
                element.hasAssocClass = 1
                break

        if self.backreferences_support:
            bassocs = element.getToAssociations()
            for p in bassocs:
                if getattr(p, 'isAssociationClass', 0):
                    element.hasAssocClass = 1
                    break

        if element.hasAssocClass:
            for line in importLines:
                print >> outfile, line

        return outfile.getvalue().strip()

    def generateImplements(self, element, parentnames):
        outfile = StringIO()
        # Zope 2 Interfaces
        # "__implements__" line -> handle realization parents
        reparents = element.getRealizationParents()
        z2reparentnames = [p.getName() for p in reparents if not p.hasStereoType('z3')]
        if z2reparentnames:
            z2iface_implements = \
                ' + '.join(["(%s,)" % i for i in z2reparentnames])
        else:
            z2iface_implements = None

        if parentnames:
            z2parentclasses_implements = \
                    ' + '.join(["(getattr(%s,'__implements__',()),)" % i for i in parentnames])
        else:
            z2parentclasses_implements = None

        z2implements_line = None
        if z2iface_implements is not None or z2parentclasses_implements is not None:
            z2implements_line = '__implements__ = '
        if z2parentclasses_implements is not None:
            z2implements_line += z2parentclasses_implements
        if z2iface_implements and z2parentclasses_implements:
            z2implements_line += ' + '
        if z2iface_implements is not None:
            z2implements_line += z2iface_implements
        if z2implements_line is not None:
            print >> outfile, utils.indent(z2implements_line, 1)

        # Zope 3 interfaces
        z3reparentnames = [p.getName() for p in reparents if p.hasStereoType('z3')]
        if z3reparentnames:
            print >> outfile, utils.indent('# zope3 interfaces', 1)
            concatstring = ', '.join(z3reparentnames)
            print >> outfile, utils.indent("zope.interface.implements(%s)" % concatstring, 1)

        return outfile.getvalue()

    def getMethodsToGenerate(self, element):
        manual_methods = []
        generatedMethods = []
        allmethnames = [m.getName() for m in element.getMethodDefs(recursive=1)]

        for m in element.getMethodDefs():
            generatedMethods.append(m)
            allmethnames.append(m.getName())

        for interface in element.getRealizationParents():
            meths = [m for m in interface.getMethodDefs(recursive=1) if m.getName() not in allmethnames]
            # I dont want to extra generate methods that are already defined in the class
            for m in meths:
                generatedMethods.append(m)
                allmethnames.append(m.getName())

        # contains _all_ generated method names
        method_names = [m.getName() for m in generatedMethods]

        # If __init__ has to be generated for tools i want _not_ __init__ to be preserved
        # If it is added to method_names it wont be recognized as a manual method (hacky but works)
        if element.hasStereoType(self.portal_tools) and '__init__' not in method_names:
            method_names.append('__init__')

        if self.method_preservation:
            cl = self.parsed_class_sources.get(element.getPackage().getFilePath()+'/'+element.name, None)
            if cl:
                manual_methods=[mt for mt in cl.methods.values() if mt.name not in method_names]

        return generatedMethods, manual_methods

    def dispatchXMIClass(self, element):
        log.debug("Finding suitable dispatching stereotype for element...")
        dispatching_stereotypes = self.getUMLProfile().findStereoTypes(entities=['XMIClass'],
                                                                       dispatching=1)
        log.debug("Dispatching stereotypes found in our UML profile: %r.",
                  dispatching_stereotypes)
        dispatching_stereotype = None
        for stereotype in dispatching_stereotypes:
            if element.hasStereoType(stereotype.getName()):
                dispatching_stereotype = stereotype

        if not dispatching_stereotype:
            dispatching_stereotype = self.getDefaultClassType()

        generator = dispatching_stereotype.generator
        return getattr(self, generator)(element,
                                       template=getattr(dispatching_stereotype,
                                                        'template', None))

    def dispatchXMIInterface(self, element):
        log.debug("Finding suitable dispatching stereotype for element...")
        dispatching_stereotypes = self.getUMLProfile().findStereoTypes(entities=['XMIInterface'],
                                                                       dispatching=1)
        log.debug("Dispatching stereotypes found in our UML profile: %r.",
                  dispatching_stereotypes)
        dispatching_stereotype = None
        for stereotype in dispatching_stereotypes:
            if element.hasStereoType(stereotype.getName()):
                dispatching_stereotype = stereotype

        if not dispatching_stereotype:
            dispatching_stereotype = self.getDefaultInterfaceType()

        generator = dispatching_stereotype.generator
        return getattr(self,generator)(element,
                                       template=getattr(dispatching_stereotype,
                                                        'template', None))

    def generatePythonClass(self, element, template, nolog=False, **kw):
        if not nolog:
            log.info("%sGenerating python class '%s'.",
                     ' '*4*self.infoind,
                     element.getName())

        templ = utils.readTemplate(template)
        d = {
            'klass': element,
            'generator': self,
            'parsed_class': element.parsed_class,
            'builtins': __builtins__,
            'utils': utils,
        }
        d.update(__builtins__)
        d.update(kw)
        res = HTML(templ, d)()
        return res

    def generateZopeClass(self, element, template, nolog=False, **kw):
        if not nolog:
            log.info("%sGenerating Zope class '%s'.",
                     ' '*4*self.infoind,
                     element.getName())

        templ = utils.readTemplate(template)
        d = {
            'klass': element,
            'generator': self,
            'parsed_class': element.parsed_class,
            'builtins': __builtins__,
            'utils': utils,
        }
        d.update(__builtins__)
        d.update(kw)
        res = HTML(templ, d)()
        return res

    def generateMethodSecurityDeclaration(self, m):
            # [optilude] Added check for permission:mode - public (default),
            # private or protected
            # [jensens] You can also use the visibility value from UML
            # (implemented for 1.2 only!) TGV overrides UML-mode!
            permissionMode = m.getVisibility() or 'public'

            # A public method means it's part of the class' public interface,
            # not to be confused with the fact that Zope has a method called
            # declareProtected() to protect a method which is *part of the
            # class' public interface* with a permission. If a method is public
            # and has no permission set, declarePublic(). If it has a permission
            # declareProtected() by that permission.
            if permissionMode == 'public':
                rawPerm = m.getTaggedValue('permission',None)
                permission = utils.getExpression(rawPerm)
                if rawPerm:
                    return utils.indent("security.declareProtected"
                                                   "(%s, '%s')" % (permission,
                                                   m.getName()), 1)
                else:
                    return utils.indent("security.declarePublic"
                                                   "('%s')" % m.getName(), 1)
            # A private method is always declarePrivate()'d
            elif permissionMode == 'private':
                return utils.indent("security.declarePrivate('%s')"
                                               % m.getName(), 1)

            # A protected method is also declarePrivate()'d. The semantic
            # meaning of 'protected' is that is hidden from the outside world,
            # but accessible to subclasses. The model may wish to be explicit
            # about this intention (even though python has no concept of
            # such protection). In this case, it's still a privately declared
            # method as far as TTW code is concerned.
            elif permissionMode == 'protected':
                return utils.indent("security.declarePrivate('%s')"
                                               % m.getName(), 1)

            # A package-level method should be without security declarartion -
            # it is accessible to other methods in the same module, and will
            # use the class/module defaults as far as TTW code is concerned.
            elif permissionMode == 'package':
                # No declaration
                return utils.indent("# Use class/module security "
                                              "defaults", 1)
            else:
                log.warn("Method visibility should be 'public', 'private', "
                         "'protected' or 'package', got '%s'.", permissionMode)
                return ''


    def generateZope3Interface(self, element, template, **kw):
        log.info("%sGenerating zope3 interface '%s'.",
                 '        ',
                 element.getName())

        templ = utils.readTemplate(template)
        d = {
            'klass': element,
            'generator': self,
            'parsed_class': element.parsed_class,
            'builtins': __builtins__,
            'utils': utils,
        }
        d.update(__builtins__)
        d.update(kw)
        res = HTML(templ, d)()
        return res

    def getLicenseInfo(self, element):
        license_name = self.getOption('license', element, self.license)
        license = LICENSES.get(license_name)
        if license is None:
            license = {
                'name': license_name,
                'text': self.getOption('license_text', element, ''),
            }
        if license['name'] or license['text']:
            license_text = '%(name)s\n#\n%(text)s' % license
        else:
            license_text = ""
        log.debug("License: %r.", license_text)
        return license_text


    def getHeaderInfo(self, element, name=None):
        log.debug("Getting info for the header...")

        # ACV FIX 20110301 - remove the auto injection of year in the copyright notice, y the notice already incluides the year
        aYearStr = str(time.localtime()[0])
        aCopyrightOrAuthor = self.getOption('copyright', element, self.copyright) or self.author
        if aYearStr in aCopyrightOrAuthor:
            copyright = COPYRIGHT_wo_year % aCopyrightOrAuthor
        else:
            copyright = COPYRIGHT % (aYearStr, aCopyrightOrAuthor)
            
        log.debug("Copyright = %r.", copyright)

        license = self.getLicenseInfo(element)
        authors, emails, authorline = self.getAuthors(element)

        if self.getOption('rcs_id', element, False):
            log.debug("Using id keyword.")
            filename_or_id = '$'+'Id'+'$'
        else:
            log.debug("Using filename.")
            filename_or_id = 'File: %s.py' % (name or element.getModuleName())

        if self.getOption('generated_date', element, False):
            date = '# Generated: %s\n' % time.ctime()
        else:
            date = ''

        if utils.isTGVTrue(self.getOption('version_info', element, True)):
            log.debug("We want version info in every file.")
            versiontext = utils.version()
        elif element.__class__ == XMIParser.XMIModel:
            log.debug("We don't want version info in all files, "
                      "but we do want them in the config and Install.")
            versiontext = utils.version()
        else:
            log.debug("We don't want version info in this file.")
            versiontext = ''
            
        encoding = self.getOption('encoding', element, 'utf-8')
        log.debug("Encoding for python files is set to %s" % encoding)
        
        moduleinfo = {
            'authors': ', '.join(authors),
            'emails': ', '.join(emails),
            'authorline': authorline,
            'version': versiontext,
            'date': date,
            'copyright': '\n# '.join(utils.wrap(copyright, 77).split('\n')),
            'license': license,
            'filename_or_id': filename_or_id,
            'encoding': encoding,
        }
        return moduleinfo

    def generateModuleInfoHeader(self, element, name=None):
        """Generate the module header.
        
        Watch out: generate at least the encoding header, the rest is
        optional.
        """

        result = ''
        fileheaderinfo = self.getHeaderInfo(element, name=name)
        result = ENCODING_HEADER % fileheaderinfo
        if self.module_info_header:
            result += MODULE_INFO_HEADER % fileheaderinfo
        return result

    def getAuthors(self, element):
        log.debug("Getting the authors...")
        authors = self.getOption('author', element, self.author) or 'unknown'
        if not type(authors) == type([]):
            log.debug("Trying to split authors on ','.")
            authors = authors.split(',')
        else:
            log.debug("self.author is already a list, no need to split it.")
        authors = [i.strip() for i in authors]
        log.debug("Found the following authors: %r.", authors)
        log.debug("Getting the email addresses.")
        emails = self.getOption('email', element, self.email) or 'unknown'
        if not type(emails) == type([]):
            # self.email is already a list
            emails = emails.split(',')
        emails = ['<%s>' % i.strip() for i in emails]
        log.debug("Found the following email addresses: %r.", emails)

        authoremail = []
        for author in authors:
            if authors.index(author) < len(emails):
                authoremail.append("%s %s" % (author, emails[authors.index(author)]))
            else:
                authoremail.append("%s <unknown>" % author)

        authorline = utils.wrap(", ".join(authoremail), 77)

        return authors, emails, authorline
