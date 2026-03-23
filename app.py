import random
from typing import List, Dict, Optional
from datetime import datetime, timedelta

# ==========================================
# ⚖️ 領域模型與資料庫 (Data Layer)
# ==========================================

# 景點資料庫：包含標籤、建議停留時間(小時)、以及適合的交通工具
ATTRACTIONS_DB = [
    {"id": 1, "name": "金剛大道", "region": "長濱", "tags": ["風景", "拍照"], "hours": 1.5, "transport": ["機車", "汽車"]},
    {"id": 2, "name": "八仙洞", "region": "長濱", "tags": ["歷史", "地質"], "hours": 2.0, "transport": ["機車", "汽車", "巴士"]},
    {"id": 3, "name": "三仙台", "region": "成功", "tags": ["生態", "地標"], "hours": 2.5, "transport": ["機車", "汽車", "巴士"]},
    {"id": 4, "name": "都歷海灘 (天空之鏡)", "region": "成功", "tags": ["網美", "海景"], "hours": 1.5, "transport": ["機車", "汽車"]},
    {"id": 5, "name": "加路蘭遊憩區", "region": "卑南", "tags": ["裝置藝術", "看海"], "hours": 1.0, "transport": ["機車", "汽車", "巴士"]},
]

# 住宿資料庫
HOTELS_DB = [
    {"id": 101, "name": "長濱邊境牧海", "region": "長濱", "price_level": 3, "tags": ["海景", "設計"]},
    {"id": 102, "name": "台東跑者之家", "region": "長濱", "price_level": 1, "tags": ["平價", "溫馨"]},
    {"id": 103, "name": "都蘭草堂", "region": "東河", "price_level": 3, "tags": ["隱密", "自然"]},
]

# ==========================================
# 🧠 行程生成核心引擎 (Logic Layer - Code-CRF)
# ==========================================

class TravelPlannerEngine:
    """
    旅遊規劃引擎：負責過濾、權重計算與行程生成。
    遵循遍歷性原則 (Ergodicity)，確保任何輸入組合都不會導致系統崩潰。
    """
    def __init__(self, attractions: List[Dict], hotels: List[Dict]):
        self.attractions = attractions
        self.hotels = hotels

    def generate_itinerary(
        self, 
        days: int, 
        preferences: List[str], 
        transport: str
    ) -> Dict[str, any]:
        
        # 🛡️ 遍歷性防禦：限制極端天數
        actual_days = max(1, min(days, 7))

        # 1. 篩選符合交通工具與偏好的景點 (Slicing)
        filtered_spots = [
            spot for spot in self.attractions
            if transport in spot["transport"]
        ]

        # 如果沒有符合條件的景點，退回保底景點 (Fallback)
        if not filtered_spots:
            filtered_spots = self.attractions

        # 2. 按天分配景點
        daily_plan = {}
        used_spots = set()

        for day in range(1, actual_days + 1):
            # 每天隨機挑選 2~3 個景點，且不重複
            available_spots = [s for s in filtered_spots if s["id"] not in used_spots]
            
            # 若景點不夠用，重置歷史（紅皇后動態監測）
            if len(available_spots) < 2:
                used_spots.clear()
                available_spots = filtered_spots

            today_selection = random.sample(
                available_spots, 
                k=min(3, len(available_spots))
            )
            
            # 記錄已使用的景點
            for s in today_selection:
                used_spots.add(s["id"])

            daily_plan[f"第 {day} 天"] = today_selection

        # 3. 推薦住宿 (取決於最後一天的區域)
        last_day_spots = daily_plan[f"第 {actual_days} 天"]
        preferred_region = last_day_spots[0]["region"] if last_day_spots else "長濱"
        
        recommended_hotels = [
            h for h in self.hotels if h["region"] == preferred_region
        ]
        
        # 保底機制：若該區域無住宿，推薦全局住宿
        if not recommended_hotels:
            recommended_hotels = self.hotels

        return {
            "metadata": {
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "total_days": actual_days,
                "transport": transport
            },
            "itinerary": daily_plan,
            "accommodations": random.sample(recommended_hotels, k=min(2, len(recommended_hotels)))
        }

# ==========================================
# 🖥️ 終端輸出介面 (Presentation Layer)
# ==========================================

def print_itinerary(result: Dict):
    """
    將結構化數據美化輸出至終端機。
    """
    meta = result["metadata"]
    print("=" * 45)
    print(f"✨ 智選旅遊行程表 (生成時間: {meta['generated_at']})")
    print(f"🚌 交通方式: {meta['transport']} | 🗓️ 總天數: {meta['total_days']} 天")
    print("=" * 45)

    for day, spots in result["itinerary"].items():
        print(f"\n📌 【{day}】")
        for i, spot in enumerate(spots, 1):
            tags_str = "/".join(spot['tags'])
            print(f"  {i}. {spot['name']} ({spot['region']}) - ⏱️ 停留 {spot['hours']}h [{tags_str}]")

    print("\n" + "-" * 45)
    print("🏨 建議入住飯店 (依據您的地理軌跡推薦)")
    for hotel in result["accommodations"]:
        print(f"  🏠 {hotel['name']} ({hotel['region']}) - 🏷️ {hotel['tags'][0]}")
    print("=" * 45)


# ==========================================
# 🚀 執行主程式
# ==========================================
if __name__ == "__main__":
    # 初始化引擎
    planner = TravelPlannerEngine(ATTRACTIONS_DB, HOTELS_DB)

    # 模擬使用者輸入：3天、騎機車、喜歡拍照
    user_days = 3
    user_transport = "機車"
    user_prefs = ["拍照", "海景"]

    # 生成並打印
    plan_result = planner.generate_itinerary(user_days, user_prefs, user_transport)
    print_itinerary(plan_result)
