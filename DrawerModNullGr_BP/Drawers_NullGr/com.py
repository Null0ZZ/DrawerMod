
# -*- coding: utf-8 -*-

modName = "Drawers"
csname = "Drawers_nullgr_ClientSys"
ssname = "Drawers_nullgr_ServerSys"
uiPath = "Drawers_NullGr.ui.ui"
csPath = "Drawers_NullGr.Drawers_main_cs.Drawers_nullgr_main_ClientSys"
ssPath = "Drawers_NullGr.Drawers_main_ss.Drawers_nullgr_main_ServerSys"

# ─── 模块系统注册 ─────────────────────────────────────────────────────────────
# 抽屉核心模块
drawers_ssname = "Drawers_ServerSys"
drawers_ssPath = "Drawers_NullGr.ModSys.Drawers.Drawers_ss.Drawers_ServerSys"

# ─── 防双击间隔 ─────────────────────────────────────────────────────────────────
pc_time_click = 0.15

serverSysKey = {
    ssname: ssPath,
    drawers_ssname: drawers_ssPath,
}

clientSysKey = {
    csname: csPath,
}