import time

def changbin_tour():
    print("--- 🌊 歡迎來到台東長濱鄉：山海間的慢活天堂 ---")
    
    locations = {
        "1": {"name": "金剛大道", "desc": "絕美的 S 型公路，背靠金剛山，面朝太平洋。"},
        "2": {"name": "八仙洞", "desc": "台灣最古老的神祕遺址，感受萬年舊石器文化。"},
        "3": {"name": "烏石鼻", "desc": "全台最大的柱狀火山岩，是釣客與風景攝影師的寶地。"},
        "4": {"name": "玉長公路", "desc": "連接花蓮玉里與台東長濱，穿越海岸山脈的最美捷徑。"}
    }

    while True:
        print("\n📍 您想探索哪個景點？")
        for key, info in locations.items():
            print(f"[{key}] {info['name']}")
        print("[Q] 結束行程")

        choice = input("\n請輸入編號 (或 Q 離開): ").upper()

        if choice == 'Q':
            print("\n🚗 感謝您的造訪！在長濱，時間是用來浪費在美景上的。再見！")
            break
        elif choice in locations:
            spot = locations[choice]
            print(f"\n【{spot['name']}】")
            print("導覽中...")
            time.sleep(1)  # 模擬導覽載入感
            print(f"💡 景點簡介：{spot['desc']}")
        else:
            print("❌ 哎呀，這個編號不在地圖上，請再選一次！")

if __name__ == "__main__":
    changbin_tour()
