from Products.CMFPlone import MigrationTool #:wort registerSetupWidget
from ChineseSupport import ChineseSupportSetup

widgets = [ChineseSupportSetup, ]

for widget in widgets:
    MigrationTool.registerSetupWidget(widget)
