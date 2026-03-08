# -*- coding:utf-8 -*-

import mod.client.extraClientApi as cApi

snode = cApi.GetScreenNodeCls()

class ui(snode):
    def __init__(self,namespace,uikey,p):
        snode.__init__(self,namespace,uikey,p)
        print "ui sys"

    def Creat(self):
        print "ui Creat"

        pass

