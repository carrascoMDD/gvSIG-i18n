
from Products.CMFCore.utils import getToolByName

def installActions(self, portal, actions):
    """ install action to site, typical actions definition:
        actions=(
             {"type":"ContentPanels",
              "id":"plone_news_sin",
              "name":"Plone News",
              "action":"here/sin_tool/macros/plone_news",
              "condition":"",
              "permission":"View",
              "category":"panel_viewlets",
              "visible":1},

             {"type":"ContentPanels",
              "id":"plope_blog_sin",
              "name":"plope",
              "action":"here/sin_tool/macros/plope_blog",
              "condition":"",
              "permission":"View",
              "category":"panel_viewlets",
              "visible":1},

             )
    """

    portal_types = getToolByName(portal, 'portal_types')
    for action in actions:
       portalType = portal_types.getTypeInfo(action['type'])
       if not portalType:
           continue
       portalTypeActions = portalType.listActions()
       for i in range(0, len(portalTypeActions)):
           try: # is CMF 1.4+ ?
               isExisted = action['id'] == portalTypeActions[i].id
           except:
               isExisted = action['id'] == portalTypeActions[i]['id']
           if isExisted:
               portalType.deleteActions((i,))
               break

       try: # isCMF1_4+ ?
           portalType.addAction(
               id=action['id'],
               name=action['name'],
               action='string:'+action['action'],
               condition=action['condition'],
               permission=action['permission'],
               category=action['category'],
               visible=action['visible'])
       except:
           portalType.addAction(
              id=action['id'],
              name=action['name'],
              action=action['action'],
              permission=action['permission'],
              category=action['category'],
              visible=action['visible'])

