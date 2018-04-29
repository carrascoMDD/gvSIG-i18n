# Pak to make only user who have right to access Members folder
# Attention: it seems that user.has_permission is wrong. it always 
# check permission for the current login user.
from AccessControl.User import nobody
from Products.CMFCore.utils import getToolByName
def wrapUser(self, u, wrap_anon=0):
        '''
        Sets up the correct acquisition wrappers for a user
        object and provides an opportunity for a portal_memberdata
        tool to retrieve and store member data independently of
        the user object.
        '''
        b = getattr(u, 'aq_base', None)
        if b is None:
            # u isn't wrapped at all.  Wrap it in self.acl_users.
            b = u
            u = u.__of__(self.acl_users)
        if (b is nobody and not wrap_anon) or hasattr(b, 'getMemberId'):
            # This user is either not recognized by acl_users or it is
            # already registered with something that implements the
            # member data tool at least partially.
            return u

        parent = self.aq_inner.aq_parent
        base = getattr(parent, 'aq_base', None)
        if hasattr(base, 'portal_memberdata'):
            # Apply any role mapping if we have it
            if hasattr(self, 'role_map'):
                for portal_role in self.role_map.keys():
                    if (self.role_map.get(portal_role) in u.roles and
                            portal_role not in u.roles):
                        u.roles.append(portal_role)

            # Get portal_memberdata to do the wrapping.
            md = getToolByName(parent, 'portal_memberdata')
            try:
                portal_user = md.wrapUser(u)

                # Check for the member area creation flag and
                # take appropriate (non-) action
                if getattr(self, 'memberareaCreationFlag', 0) != 0:
                    if self.getHomeUrl(portal_user.getId()) is None:
                      parent = self.aq_inner.aq_parent
                      members =  getattr(parent, 'Members', None)
                      for role in portal_user.getRolesInContext(members):
                        if role in ['Member', 'Manager', 'Reviewer', 'AdvancedMember', 'Contributor', 'Owner']:
                          self.createMemberarea(portal_user.getId())
                          break
                return portal_user

            except:
                from zLOG import LOG, ERROR
                import sys
                type,value,tb = sys.exc_info()
                try:
                    LOG('CMFCore.MembershipTool',
                        ERROR,
                        'Error during wrapUser:',
                        "\nType:%s\nValue:%s\n" % (type,value))
                finally:
                    tb = None       # Avoid leaking frame
                pass
        # Failed.
        return u

from Products.CMFCore.MembershipTool import MembershipTool
MembershipTool.wrapUser = wrapUser

def setSecurityProfile(self, password=None, roles=None, domains=None):
        """Set the user's basic security profile"""
        u = self.getUser()
        # This is really hackish.  The Zope User API needs methods
        # for performing these functions.
        if not roles:
            roles = u.getRoles()
        # don't spam the user's roles with Authenticaed
        roles = filter(lambda x: x != 'Authenticated', roles)
        # set the profile on the user folder
        # keep password of None if given - could get encrypted password
        u.aq_parent._doChangeUser(u.getUserName(), password,
                                  roles, domains or u.getDomains())

from Products.CMFCore.MemberDataTool import MemberData
MemberData.setSecurityProfile = setSecurityProfile

def setPassword(self, password, domains=None):
        '''Allows the authenticated member to set his/her own password.
        '''
        registration = getToolByName(self, 'portal_registration', None)
        if not self.isAnonymousUser():
            member = self.getAuthenticatedMember()
            if registration:
                failMessage = registration.testPasswordValidity(password)
                if failMessage is not None:
                    raise 'Bad Request', failMessage
            member.changePassword(password=password)
        else:
            raise 'Bad Request', 'Not logged in.'

from Products.CMFCore.MembershipTool import MembershipTool
MembershipTool.setPassword = setPassword
