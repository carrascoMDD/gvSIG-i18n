Overview


  gvSIGtraducciones allows the collaborative translations
  of user interface strings from the gvSIG application
   - an open source GIS made in Java - 
   and the collaborative tools used in the gvSIG project
   - made in open source Plone.
   
   gvSIGtraducciones also allows indeed to translate
   user interface strings from any other program,
   as it imports and exports translations in both
   Java .properties format for intenationalization localized files,
   and .PO files according to GNU gettext.
   




REQUIRED INSTALLATION STEP (manual)

  Remember to copy to the Plone instance Extensions folder,
  the files in the product folder
  gvSIGi18n\manualadditions\AsExternalMethodInSiteRoot
  including TRAChangeAndBrowseTranslations.py, TRAExport_ctrl.py,
  TRARenderProfiling.py, TRARenderSecurity.py.




KNOWN ISSUES:

  When creating the root instance of TRACatalogo (Catalogo de Traducciones, Translations Catalog)
  in the new element edit form:
  ENTER a Title, but DOT ENTER an id for the new TRACatalogo.
  
  You may enter as Title the exact id you want for the new TRACatalogo. 
  Upon creation the id will be taken from the supplied Title.
  After creation you may edit the Title as you want it displayed.


  Further details on the issue of incomplete initialization when entering and id to create a translations catalog:

    If an id is entered, the initialization of TRACatalogo will fail.
    If it is the first root translations catalog created in the plone site, 
    and no root instance has been created for another product from Model Driven Development sl
    the incomplete initialization will fail to create in the Plone site 
    an instance  of ModelDDvlPloneTool,
    and cause an error that will be reported
    to the connected user as:

    Tipo de Error
        AttributeError
    Valor del Error
        ModelDDvlPlone_tool


    If an instance of ModelDDvlPloneTool already exists,
    because other instances have been previously created
    of TRACatalogo (or other root instance from other product by Model Driven Development sl)
    then the incomplete initialization can be noticed visiting the 
    'Advanced View' of the new TRACatalogo,
    (visit the URL of the new TRACatalogo, appending /Tabular to the URL),
    because there will be no collections to hold items under the new TRACatalogo
    Languages Collection (Coleccion de Idiomas)
    Modules Collection (Coleccino de Modulos)
    Import processes collection (Coleccion de Importaciones)
    Status Reports collection (Coleccion de Informes de Estado)
    String Requests Collection (Coleccion de Solicitudes de Cadenas)
  


    Initialization of the new TRACatalog can be forced by navigating
    to the URL new TRACatalogo, appending /TRACatalogoLazyInit_action to the URL





 
PREREQUISITE PRODUCTS

  Make available to the Plone instance (by copying or linking)
  the Plone products:

  - ModelDDvlPlone

  - ModelDDvlPloneTool

  - Relations (a version patched by MDDsl, i.e.: v 0.6bMDDsl0.1)

  - Archetypes
  
  - PloneLanguageTool

  And optionally, for support of searches of translations into Chinese or Japanese,
  make available to the plone instance the products

  - CJKSplitter
  
  - ZopeChinaPak

   
  Installation will fail if these products are not 
  correctly deployed and available in the Plone instance.
  
  The installer will automatically install the prerequisite
  products, if correctly deployed and available in the Plone instance.
     

     
Copyright


  Copyright (c) 2008, 2009 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
  


Project Forge
 

  - "Project at OSOR (Open Source Observatory and Repository of the European Comission)":http://www.osor.eu/projects/gvsig-i18n
     
  - "Forge at OSOR (Open Source Observatory and Repository of the European Comission)":http://forge.osor.eu/projects/gvsig-i18n
  

  
Project Home


  - "gvSIG.org":http://gvSIG.org 
  
  - "GVA CIT":http://www.gvsig.gva.es
  
  - "ModelDD.org":http://www.ModelDD.org 

  
Authors

  - Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana, "GVA CIT":http://www.gvsig.gva.es
  
  - Antonio Carrasco Valero and "Model Driven Development sl  Valencia (Spain)":http://www.ModelDD.org 


License

  GNU General Public License (GPL)
 
  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.
 
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
  02110-1301, USA.
  

