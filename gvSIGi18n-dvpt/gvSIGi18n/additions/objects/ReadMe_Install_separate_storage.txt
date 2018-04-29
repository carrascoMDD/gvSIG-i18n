Optional installation of separate storage files.
The application works without limitations if this optional installation is not performed.

It is reccommended to install separate storage files
on production sites that host a significant amount of content
other than translations, 
or when the application will manage a high number of translations
(as calculated by number of strings multiplied by the number of languages),
i.e. 10,000 or more translations.

The benefits of separate storage are:
- better performance
- better recoverability after unexpected server failures


-----------------------------


SUB-PROCESS 1: CREATE ADDITIONAL STORAGE FILE
Create a new blank storage file, 
to be mounted later in the main plone site
by using an auxiliary plone instance for a few moments,


1) Optionally, Create new zope/Plone instance
2) Optionally, Start zope/plone instance, verify that was correctly created, you can login, see the default Plnoe site (just to make sure it works)
3) Shutdown zope/plone
4) Edit zope.conf
   add at the bottom an entry:

# Just to create storage files
# Remove and comment the following two zodb_db entries once created
<zodb_db i18nstoredb>
    <filestorage>
      path $INSTANCE/var/i18nstore.fs
    </filestorage>
    mount-point /i18nstore
</zodb_db>

<zodb_db bpdstoredb>
    <filestorage>
      path $INSTANCE/var/bpdstore.fs
    </filestorage>
    mount-point /bpdstore
</zodb_db>


5) start zope/plone new instance
   if it does not start, or there are startup warnings,
   verify your changes to zope.conf, edit them, and restart zope/plone

6) login into zmi

7) At the root of the ZMI (i.e. NOT within  any Plone site)
   Add a ZODB Mount point, choosing from the menu of factory types
   The /i18nstore mount poitn shall be visible, select it if not alrady, 
   select check box "Create new folders if the mounted objects don't yet exist" 
   and click button "Create selected mount points"
   - a file i18nstore.fs (and .lock, .index, .tmp,) appear in the  $INSTANCE/var folder in the filesystem

8) From ZMI, inside the i18nstore folder in the ZMI,
   create a Plone Site by choosing from the factories menu:
id
i18nstoresite
title
i18nstoresite

id
bpdstoresite
title
bpdstoresite


9) Navigate the new Plone site i18nstoresite from a Plone view
   i.e., navigate into the Plone site instance from ZMI, and
   open new browser  on the View ZMI tab of the Plone Site.

10) (optional) From Plone site root contents, You may delete the Welcome page at the root of the i18nstoresite

11) Create in the root of the plone site a folder
id
i18ndb
title
I18N Database


id
bpddb
title
Business Process Definition Database


12) Shut down  zope/plone instance

-----------------------

At this point, we have a file  i18nstore.fs
with a plone site i18nstoresite and wihtin it a folder i18nstorefolder
complete path: 
/i18nstore/i18nstoresite/i18ndb
/bpdstore/bpdstoresite/bpddb
that now we will use as secondary storage for our main plone instance and site).

!!!! COPY A BACKUP OF i18nstore.fs and bpdstore.fs !!!!!
-----------------------------------------





SUBPROCESS 2: MOUNT ADDITIONAL STORAGE FILE ON MAIN PLONE SITE

suposing that the plone site where the store must be mounted into 
has id
gvsigweb

and that the store must be mounted is in a folder named 'i18nmount'
at the root of site gvsigweb

1) Copy the file i18nstore.fs (bpdstore.fs) created in Subprocess 1
   to the main zope/plone instance var folder (wherever the Data.fs file is, usually within a var directory)


2) Edit main zope/plone instance zope.conf

3) Add at the bottom an entry


<zodb_db i18nstoredb>
    mount-point /modeldd/i18ndb:/i18nstore/i18nstoresite/i18ndb
    <filestorage>
      path $INSTANCE/var/i18nstore.fs
    </filestorage>
</zodb_db>

<zodb_db bpdstoredb>
    mount-point /modeldd/bpddb:/bpdstore/bpdstoresite/bpddb
    <filestorage>
      path $INSTANCE/var/bpdstore.fs
    </filestorage>
</zodb_db>



Important the name 'i18nstorefolder' of the mount point 
must be the same of that of the mapped folder 'i18nstorefolder' (bpdstorefolder) created in the i18nstoresite (bpdstoresite)plone site storage file i18nstore.fs (bpdstore.fs) in Process 1 above.


(note that in unix it may be necesary to change $INSTANCE by $INSTANCE_HOME

4) Start (or restart) main zope/plone instance
   if it does not start, or there are startup warnings,
   edit zope.conf: possibly the path is wrong
     maybe should use $INSTANCE_HOME in unix rather than $INSTANCE as in windos


5) At the root of the ZMI (i.e. NOT within  any Plone site)
   Add a ZODB Mount point, choosing from the menu of factory types
   The /gvsigweb/i18nstorefolder (/gvsigweb/bpdstorefolder)  mount poitn shall be visible, select it if not alrady, 
   Select check box "Create new folders if the mounted objects don't yet exist" 
   and click button "Create selected mount points"
 

6) Rebuild the plone site 'portal_catalog' (Clear and rebuild option, removing all entries and walk entire portal adding content objects)
   From Plone Site portal_catalog objext Advanced tab.


-----

At this point, content created under the folder
/gvsigweb/i18nstorefolder
will be written in the storage file i18nstore.fs
 
Create a file and upload some megabytes, to see the i18nstore.fs grow.



