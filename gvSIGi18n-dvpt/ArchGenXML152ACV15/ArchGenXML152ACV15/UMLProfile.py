import logging
import textwrap
log = logging.getLogger('umlprofile')

class ChainedDict(dict):
    ''' chained dict class allows to conatenate dictionaries '''

    parent_chain = []

    def __init__(self, parent_chain=[], **kw):
        log.debug("Initializing ChainedDict class.")
        dict.__init__(self,**kw)
        self.parent_chain=parent_chain
        self._keys = []

    def __getitem__(self,key):
        if dict.has_key(self,key):
            return dict.__getitem__(self,key)

        for p in self.getParentChain():
            if p.has_key(key):
                return p.__getitem__(key)

        raise KeyError,key

    def getParentChain(self):
        return self.parent_chain

    def addToParentChain(self,d):
        self.parent_chain.append(d)

    def __iter__(self):
        return iter(self.keys())

    def clear(self):
        dict.clear(self)
        self._keys = []

    def items(self):
        res=dict.items(self)
        for p in self.getParentChain():
            res.extend(p.items())

        return res

    def keys(self):
        res=dict.keys(self)
        for p in self.getParentChain():
            res.extend(p.keys())
        return res

    def values(self):
        return map(self.get, self.keys())

    def get(self,key,default=None):
        if dict.has_key(self,key):
            return dict.get(self,key)

        for p in self.getParentChain():
            if p.has_key(key):
                return p.get(key)

class ProfileEntry:
    ''' base class '''

    def __init__(self, name, entities, description='TODO', **kw):
        log.debug("Initializing ProfileEntry %s.",
                  name)
        self.name = name
        self.entities = entities
        self.description = description
        self.__dict__.update(kw)

    def __repr__(self):
        return '<%s name=%s entities=%s>' % (
            self.__class__.__name__,
            self.name,
            repr(self.entities))

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def getName(self):
        return self.name

class TaggedValue(ProfileEntry):
    """Represents a tagged value with its attributes.
    """


class StereoType(ProfileEntry):
    """Represents a stereotype with its attributes.
    """


class UMLProfile:
    ''' '''

    def __init__(self, parents=[]):
        log.debug("Initializing UMLProfile.")
        if type(parents) not in (type(()),type([])):
            parents = [parents]
        stereoTypes = [p.stereoTypes for p in parents]
        log.debug(repr(stereoTypes))
        self.stereoTypes = ChainedDict(stereoTypes)

    def addStereoType(self, name, entities, **kw):
        log.debug("Adding stereotype '%s' to registry for entities %r.",
                  name, entities)
        log.debug("We're passing the extra parameters %r.",
                  kw)
        stereotype = StereoType(name, entities, **kw)
        self.stereoTypes[name] = stereotype

    def filterObjects(self,list,entities,**kw):
        res = []
        #import pdb;pdb.set_trace()
        for item in list:

            #if one of the entities aplies, its ok
            if entities:
                ok = 0
                for e in entities:
                    if e in item.entities:
                        ok = 1
                        continue

                if not ok:
                    continue
            ok = 1
            for k in kw:
                if getattr(item, k, None) != kw[k]:
                    ok=0

            if not ok:
                continue

            res.append(item)

        return res

    def getAllStereoTypes(self):
        return self.stereoTypes.values()

    def findStereoTypes(self, entities=[], **kw):
        log.debug("Finding stereotypes for entities %r.",
                  entities)
        entities = [entity.replace('XMIParser.', '') for entity in entities]
        log.debug("Stripped off 'XMIParser.': %r.",
                  entities)
        list = self.getAllStereoTypes()
        return self.filterObjects(list, entities, **kw)

    def getStereoType(self,name):
        return self.stereoTypes.get(name, None)

    def documentation(self, indentation=0):
        """Return the documentation for all stereotypes.

        The documentation is returned as a string. 'indentation' can
        be used to get it back indented 'indentation' spaces. Handy
        for (classic) structured text.

        """

        categoryFromClassMap = {
            #'XMIElement': [],
            'XMIPackage': 'package',
            'XMIModel': 'model',
            'XMIClass': 'class',
            'XMIInterface': 'interface',
            #'XMIMethodParameter': ,
            'XMIMethod': 'method',
            'XMIAttribute': 'attribute',
            #'XMIAssocEnd': ,
            'XMIAssociation': 'association',
            #'XMIAbstraction': ,
            'XMIDependency': 'dependency',
            #'XMIStateContainer': ,
            #'XMIStateMachine': ,
            'XMIStateTransition': 'state transition',
            #'XMIAction': ,
            #'XMIGuard': ,
            'XMIState': 'state',
            #'XMICompositeState': ,
            #'XMIDiagram': ,
            }
        import StringIO
        out = StringIO.StringIO()
        all = self.getAllStereoTypes()
        stereotypes = []
        for item in all:
            stereotype = {}
            stereotype['name'] = item.name
            stereotype['categories'] = []
            for entity in item.entities:
                mapped_entity = categoryFromClassMap[entity]
                stereotype['categories'].append(mapped_entity)
            stereotype['description'] = item.get('description', 'TODO')
            stereotypes.append(stereotype)
        names = [item['name'] for item in stereotypes]
        names.sort()
        categories = {}
        for item in stereotypes:
            for category in item['categories']:
                categories[category] = "dictionary just for making keys unique"
        categories = categories.keys()
        categories.sort()
        wrapper = textwrap.TextWrapper(replace_whitespace=True,
                                       initial_indent = ' ',
                                       subsequent_indent = '    ',
                                       width=72)
        for category in categories:
            print >> out
            print >> out, category
            print >> out
            for name in names:
                for stereotype in stereotypes:
                    if stereotype['name'] != name:
                        continue
                    if category not in stereotype['categories']:
                        continue
                    description_lines = stereotype['description'].split('\n')
                    description_lines = [line.strip() for line in description_lines]
                    description = '\n'.join(description_lines)
                    outstring = "%s -- %s" % (name,
                                              description)
                    outstring = wrapper.fill(outstring)
                    print >> out, outstring
                    print >> out
        spaces = ' ' * indentation
        lines = out.getvalue().split('\n')
        indentedLines = [(spaces + line) for line in lines]
        return '\n'.join(indentedLines)


if __name__=='__main__':
    # The tests that were originally here have been moved to
    # tests/testUMLProfile.py.
    from ArchetypesGenerator import ArchetypesGenerator
    uml_profile = ArchetypesGenerator.uml_profile
    print uml_profile.documentation()

