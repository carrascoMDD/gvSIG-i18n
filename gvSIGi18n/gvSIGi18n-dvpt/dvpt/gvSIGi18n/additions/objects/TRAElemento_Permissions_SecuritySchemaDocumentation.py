# -*- coding: utf-8 -*-
#
# File: TRAElemento_Permissions_SecuritySchemaDocumentation.py
#
# Copyright (c) 2008, 2009,2010 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# Authors: 
# Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana (Spain) <gvSIGi18n@gvSIG.org>  
# Model Driven Development sl  Valencia (Spain) <http://www.ModelDD.org> 
# Antonio Carrasco Valero                       <carrasco@ModelDD.org>
#
#
__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana <gvSIGi18n@gvSIG.org>, 
Model Driven Development sl <gvSIGi18n@ModelDD.org>, 
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'


cREMOVEDContents_JumpsBackTodefaultpage_SecuritySchemaDocumentation = u"""

.. contents::

|
|

"""


cSecuritySchemaDocumentation = u"""


**NEED FULL REWRITE - THIS IS NOT UP TO DATE**


Roles
=====

**TRAManager**, **TRACoordinator**, **TRAReviewer**, **TRATranslator**, **TRAVisitor**

|
|

*"Global"* user groups
======================

* *"Global"* User Groups with roles assigned in the *Catalogo* (TRACatalogo).

|
|

*  Role acquisition from parent is allowed for the the language independent elements,
  consisting in the contents of *Catalogo*,
  except the languages collection (TRAColeccionIdiomas)
  (and the modules collection TRAColeccion Modulos).

|
|
  
* The elements that acquire role assignment from the *"Catalogo"* are:
  * collection of strings (TRAColeccionCadenas), 
  * collection of reports (TRAColeccionInformes),
  * collection of imports (TRAColeccionImportacionts),
  * and their contents (TRACadena, TRAInforme, TRAImportacion, TRAContenidoIntercambio),

|
|
  
*  Users added to the *"Global"* user groups 
  will therefore hold the corresponding roles
  in all the elements that are language (and module) independent.

|
|

*  All users need to be members of at least one of the *"Global"* user groups,
  such that they have access to the non language (or module) specific elements.

|
|

* Because all users must also be members of at least one of 
  the *"AllLanguages"* user groups or at least one of 
  the *"LanguageSpecific"* user groups,
  and to avoid the work of assigning the users to two groups,
  the "AllLanguages" groups and all the "LanguageSpecific" groups 
  shall be members of the corresponding *"Global"* group.
  
  Whenever a new language is created, 
  its language specific user groups will be created
  and added as member of the corresponding *"Global"* user group.

|
|

* Acquisition of role assignments is "cut" (not allowed)
  in the languages  collection (TRAColeccionIdiomas) 
  (and the modules collection TRAColeccion Modulos).

|
|
  
* Acquisition of role assignments is also "cut" (not allowed)
  in the languages (TRAIdioma) to be managed with its language specific users group
  (or the modules to be managed with module specific users group).

|
|


*"AllLanguages"* user groups
============================

* *"AllLanguages"* User Groups with roles assigned 
  in the languages collection (TRAColeccionIdiomas).

|
|

* All languages that are not managed with specific user groups
  shall have enabled the acquisition of role assignments
  from its parent languages collection.

|
|

* Users added to the *"AllLanguages"* user groups
  will have access to the languages 
  that are not managed with a language specific user groups.
|
|

* The *"AllLanguages*" user groups will be added as members
  to the corresponding *"Global"* user groups,
  to allow users to have access to the language independen elements,
  and to save the effort of adding users 
  to both the *"Global"* and the *"AllLanguages"* user groups.
  

*"LanguageSpecific"* user groups
================================

* *"LanguageSpecific"* User Groups with roles assigned 
  in one and only one language (TRAIdioma).
  

|
|


User groups summary
===================



The *"Global"* User Groups have names of the form:

* **TRA_<path>_Managers**
* **TRA_<path>_Coordinators**
* **TRA_<path>_Reviewers**
* **TRA_<path>_Translators**
* **TRA_<path>_Visitors**

|
|

The *"AccessAll"* User Groups have names of the form:

* **TRA_<path>_la_ALL_Managers**
* **TRA_<path>_la_ALL_Coordinators**
* **TRA_<path>_la_ALL_Reviewers**
* **TRA_<path>_la_ALL_Translators**
* **TRA_<path>_la_ALL_Visitors**

|
|

The *"Language specific"* User Groups have names of the form:

* **TRA_<path>_la-<code>_Managers**
* **TRA_<path>_la-<code>_Coordinators**
* **TRA_<path>_la-<code>_Reviewers**
* **TRA_<path>_la-<code>_Translators**
* **TRA_<path>_la-<code>_Visitors**

|
|

Sample user groups summary
==========================

For example, with a base *"Catalogo"* object named **"gvSIGi18n"** located a the root of the *"Plone site*"


* The *"Global"* User Groups will be:
  * *TRA_gvSIGi18n_Managers*
  * *TRA_gvSIGi18n_Coordinators*
  * *TRA_gvSIGi18n_Reviewers*
  * *TRA_gvSIGi18n_Translators*
  * *TRA_gvSIGi18n_Visitors*
  
|
|
  

* The *"AccessAll"* User Groups will be:  

  * *TRA_gvSIGi18n_la_ALL_Managers*
  * *TRA_gvSIGi18n_la_ALL_Coordinators*
  * *TRA_gvSIGi18n_la_ALL_Reviewers*
  * *TRA_gvSIGi18n_la_ALL_Translators*
  * *TRA_gvSIGi18n_la_ALL_Visitors*    

|
|

* The *"Language specific"* User Groups for the language *"es"* will be:  

  * *TRA_gvSIGi18n_la-es_Managers*
  * *TRA_gvSIGi18n_la-es_Coordinators*
  * *TRA_gvSIGi18n_la-es_Reviewers*
  * *TRA_gvSIGi18n_la-es_Translators*
  * *TRA_gvSIGi18n_la-es_Visitors*

|
|

* Or, for the country specific "es-ar", the *"Language specific"* User Groups for the language *"es"* will be:  

  * *TRA_gvSIGi18n_la-es-ar_Managers*
  * *TRA_gvSIGi18n_la-es-ar_Coordinators*
  * *TRA_gvSIGi18n_la-es-ar_Reviewers*
  * *TRA_gvSIGi18n_la-es-ar_Translators*
  * *TRA_gvSIGi18n_la-es-ar_Visitors*

|
|

  
Goals
=====

* **Use Case driven**

  To drive the specification of the security requirements
  along with the specification of the use case requirements.

* **Tight control**

  To enable a tight security control of the connected users
  attempting accesses to read and write application objects.

* **Use Plone/Zope**

  To rely upon the security mechanisms supplied by the Zope 2.9 and Plone 2.5 platforms
  for enforcement of the use case driven security requirements.
  
* **Platform automation**

  To automate the transformation of use case driven security requirement specifications,
  into security mechanisms supplied by the Zope 2.9 and Plone 2.5 platforms.

* **Scaleability**

  To allow the growth to a large number of languages, translators, and strings.
  
* **Manageability**

  To allow security management with mechanisms familiar to those already knowledgeable on the platform.  

|
|

Objectives
==========

* Specify security requirements for each Use Case, including: *(Goals: Use Case driven, Tight control,Use Plone/Zope)*

  * the Role or Roles that shall authorize role playing Users to exercise the Use Case
  * the Types of objects participating in the Use Case
  * the Zope/Plone permissions that must be granted to object Types involved in the Use Case

* Security shall be configurable for Users able to the operate: *(Goal: Scaleability)*

  * on all the Languages,
  * only on a specific subset of Languages

* Security platform will be configured
  on each individual application object instance,
  upon creation, and later managed explicitely when appropriate. *(Goal: Tight control)*
  
* Use standard security management Zope/Plone user interfaces to authorize Users to play specific Roles. *(Goals: Manageability, Use Plone/Zope)* 

* Avoid impact of security enforcement mechanisms 
  on the performance and resources of the non-scaleable server.*(Goals: Scaleability, Use Plone/Zope)*
  
* Grant access to Users by joining them to User Groups *(Goals: Scaleability, Manageability)*
  
  * Global user groups to grant repository-wide access
  * Language specific to grant access separately to each Language
    
|
|
 
Use Case driven security specification
======================================

The application's security is driven by the Use Cases that the application supports.

For each Use Case, the specification states a number of Use Case security Rules.

The Rules will be assessed on the connected User
as a pre-condition whenever the User executes the Use Case on specific objects,
or to inform the User whether the Use Case can be initiated on specific objects.

The Rules are used during initialization of the application's object repository,
and the instantiation of application objects during its lifecycle,
to set up on each object upon creation, 
the permissions and role assignment to certain user groups.

|
|

Use Case security Rules
=======================

A Use Case driven security Rule specifies:

* An optional display **Title**, and default value "default".

* An optional rule enforcement **Mode**, with default value *"All"*, and possible values:

  * **All**
  * **Filter**
  * **NoneOrSome**
  * **NoneOrAll**

* When the Mode is "Filter",  
  a required **Name** for the resulting set of object instances that pass the rule.
    
* An optional **Path** to traverse and reach the objects against which to assess the rule
  
* A list of **Roles**, any of which, if held by the connected User, 
  shall authorize him to exercise the use case.

* A list of Zope/Plone **Permissions**
  that the connected User shall have on the assessed object instance,
  for the Rule to pass.
  
|
|

*Interesting* permissions
=========================

Only a few of the permissions available in Zope/Plone
are actively used (set and observed) by the translations application. 

* **View**              
* **ListFolderContents**
* **AddPortalContent**  
* **AddPortalFolders**  
* **DeleteObjects**     
* **ModifyPortalContent**
* **ManageProperties**

|
|

Application Roles
=================

The application considers the Plone standard roles "manager" and "owner",
when setting up and querying role availability on objects.

In addition, the application defines additional roles:

* **TRAManager**
* **TRACoordinator**
* **TRAReviewer**
* **TRATranslator**
* **TRAVisitor**

|
|

No object shall acquire  from its container the "interesting" permissions
=========================================================================

For no object of any TRA type,
will a connected user
obtain a permission
because the user obtained it for the container element.

The flag "Adquire permission settings ?" will display de-selected
on the "Security" tab of the element's *"Zope Management Interface"*

|
|

(almost) Every object shall acquire from its container the role assignments to users and user groups
====================================================================================================

*With the exceptions listed below,*

Every object of all TRA types,
will acquire from its container
the assignment of roles to users and user groups.

Therefore (with the exceptions below) it suffices
to assign roles to users and user groups at the root object (a TRACatalogo).

This means that a user o a user group that has been granted a role in the root object, 
will have granted the role in every object contained by the root.

|
|

Root object
===========

The application stores and manages all information
as an object instance of type TRACatalogo.

We often refer to this base object instance as **"Catalogo"**, 
in the paragraphs below.

|
|

Separate security control on specific Languages
===============================================

If security enforcement on a Language is to be managed for specific users,
then the application object instance of Type TRALanguage,
will cease to acquire the role assignments to users and user groups from its container.

The flag "Inherit roles from higher levels " will display de-selected
on the "Advanced settings" section,
of the "sharing" Plone page (you need permission ManageProperties to see this).

|
|

User Groups for Roles
=====================

The application shall utilize for each Role a specific User Group,
to facilitate assignment of the Role to selected Users.

This is not only a logical convenience 
but has the advantage over assigning roles to individual users,
i.e. in the base *"Catalogo*" object,
of eliminating the processing overhead and storage access and consumption 
of changing and propagating permissions or role assignments
over a large number of objects.

Adding or removing users from user groups
do not change objects permission or role asignments
on the objects where the user group has been assigned roles,
or others of significance for performance (AsFarAsIKnownNow).

Therefore, the application shall create, manage and and observe,
a User Group for each of the application roles:
  
  * **TRAManager**, **TRACoordinator**, **TRAReviewer**, **TRATranslator**, **TRAVisitor**

The groups shall be managed prefereably 
from the "groups" tab of the "User and Groups Administration" Plone tool,
under a manager's Plone "preferences" page 
(accessible through link in top-right corner of Plone pages).

These User Groups will also show in the "sharing" Plone page 
(you need permission ManageProperties to see this)
of application objects because these groups shall have granted roles on them,
whether directly or acquired.

These groups can also be seen in the *"acl_users"* / *"source_groups"* element of the 
*root "Plone Site*" *"Zope Management Interface"*.

|
|

*"Global"* Language Independent User Groups
============================================

To assign Roles to Users in the whole of the application objects repository,
and allow the User to operate in the objects that are independent of any Languages,
( - including the *"Catalogo"* objects repository, 
the unstranslated strings, reports, imports, import contents, 
and the collections of these - ), 
the User must be added to the *"Global"* Language Independent User Groups.

To enable the managed access to the complete *"Catalogo"* objects repository,
and thanks to having all objects (with the noted exception of Languages managed separately)
acquiring  Role assignments to Users and User Groups from its container:

* The application will assign to the corresponding groups all the application Roles 
  *TRAManager*, *TRACoordinator*, *TRAReviewer*, *TRATranslator*, *TRAVisitor*, 
  on the base *"Catalogo"* object, 
  such that the assignment of Roles to the *Global" User Groups 
  is acquired by all the objects in the *"Catalogo"* objects repository.

To enable the separate management of translation activity in specific languages,
yet to maintain managerial and coordination access to these languages, 
when and if the Language becomes managed separately,
and the Language object will not acquire the Role assignments to Users and User Groups from its container:

* The application will also assign to the corresponding *"Global"* user groups
  the application Roles *TRAManager* and "TRACoordinator*,
   - but NOT the roles  *TRAReviewer* nor *TRATranslator* nor *TRAVisitor* ! - ,
  on all the Language objects (type *TRAIdioma*).

|
|

The *"Global"* User Groups have names of the form:

* **TRA_<path>_Managers**
* **TRA_<path>_Coordinators**
* **TRA_<path>_Reviewers**
* **TRA_<path>_Translators**
* **TRA_<path>_Visitors**

|
|

Substituting:

* *<path>* by the path of the the application repository (an object of type TRACatalogo),
  from the root of the *"Plone Site*" (i.e., without the id of the Plone Site).
  with slashes ("/") substituted by underscores ("_").

For example, with a base *"Catalogo"* object named **"gvSIGi18n"** located a the root of the *"Plone site*"
  * *TRA_gvSIGi18n_Managers*
  * *TRA_gvSIGi18n_Coordinators*
  * *TRA_gvSIGi18n_Reviewers*
  * *TRA_gvSIGi18n_Translators*
  * *TRA_gvSIGi18n_Visitors*

|
|

Plone security generalities
===========================

Group membership
----------------

Role assignment may be granted not only to users,
but also to user groups.

Whenever a role is granted to a user group,
the role is granted to all members of the group.

If the RecursiveGroupsPlugin is active in Plone,
then a group may have other groups as members.


"""


