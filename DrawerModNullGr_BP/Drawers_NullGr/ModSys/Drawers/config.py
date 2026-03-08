# -*- coding: utf-8 -*-
"""
抽屉模块 - 数据驱动配置表
"""

# ─── 木材类型映射 ─────────────────────────────────────────────────────────────
# 索引对应抽屉名称中的数字 drawers_{woodType}_{slots}
WOOD_TYPES = {
    0: 'oak',       # 橡木
    1: 'spruce',    # 云杉
    2: 'birch',     # 白桦
    3: 'jungle',    # 丛林
    4: 'acacia',    # 金合欢
    5: 'dark_oak',  # 深色橡木
}

# ─── 基础容量配置 ─────────────────────────────────────────────────────────────
BASE_VOLUME_1_SLOT = 2048      # 1格抽屉基础容量
BASE_VOLUME_2_SLOT = 1024      # 2格抽屉基础容量（每格）
BASE_VOLUME_4_SLOT = 512       # 4格抽屉基础容量（每格）
COMPACT_MULTIPLIER = 2         # 压缩抽屉容量倍率

# ─── 升级槽配置 ─────────────────────────────────────────────────────────────────
UPGRADE_SLOT_COUNT = 7         # 升级槽数量 (0-6)

# ─── 渲染实体配置 ─────────────────────────────────────────────────────────────────
RENDER_ENTITY_ICON = 'drawers_nullgr:drawers_icon'           # 物品图标实体
RENDER_ENTITY_ICON_BLOCK = 'drawers_nullgr:drawers_icon_block'  # 方块图标实体
RENDER_ENTITY_ICON_TOOLS = 'drawers_nullgr:drawers_icon_tools'  # 工具图标实体

# ─── 自动生成方块配置表 ─────────────────────────────────────────────────────────
def _generate_drawers_data():
    """自动生成所有抽屉方块的配置数据"""
    data = {}
    
    for wood_idx in range(6):
        # 普通抽屉
        for slots, base_vol in [(1, BASE_VOLUME_1_SLOT), (2, BASE_VOLUME_2_SLOT), (4, BASE_VOLUME_4_SLOT)]:
            name = 'drawers_nullgr:drawers_{}_{}'.format(wood_idx, slots)
            data[name] = {
                'slots': slots,
                'baseVolume': base_vol,
                'compact': False,
                'woodType': wood_idx,
            }
        
        # 压缩抽屉
        for slots, base_vol in [(1, BASE_VOLUME_1_SLOT), (2, BASE_VOLUME_2_SLOT), (4, BASE_VOLUME_4_SLOT)]:
            name = 'drawers_nullgr:drawers_compact_{}_{}'.format(wood_idx, slots)
            data[name] = {
                'slots': slots,
                'baseVolume': base_vol * COMPACT_MULTIPLIER,
                'compact': True,
                'woodType': wood_idx,
            }
    
    return data

drawersData = _generate_drawers_data()

# ─── 便捷分类列表 ─────────────────────────────────────────────────────────────────
# 1格抽屉
drawers_1 = [k for k, v in drawersData.items() if v['slots'] == 1 and not v['compact']]
compact_drawers_1 = [k for k, v in drawersData.items() if v['slots'] == 1 and v['compact']]
all_drawers_1 = drawers_1 + compact_drawers_1

# 2格抽屉
drawers_2 = [k for k, v in drawersData.items() if v['slots'] == 2 and not v['compact']]
compact_drawers_2 = [k for k, v in drawersData.items() if v['slots'] == 2 and v['compact']]
all_drawers_2 = drawers_2 + compact_drawers_2

# 4格抽屉
drawers_4 = [k for k, v in drawersData.items() if v['slots'] == 4 and not v['compact']]
compact_drawers_4 = [k for k, v in drawersData.items() if v['slots'] == 4 and v['compact']]
all_drawers_4 = drawers_4 + compact_drawers_4

# 所有抽屉方块列表
all_drawers = list(drawersData.keys())

# ─── 打包抽屉配置（Phase4 使用）─────────────────────────────────────────────────
# 打包版本后缀 _packing，暂不生成，Phase4 时添加
drawers_packing = []

# ─── 防双击时间间隔 ─────────────────────────────────────────────────────────────
PC_TIME_CLICK = 0.15  # 秒
