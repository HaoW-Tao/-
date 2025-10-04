import random
import multiprocessing as mp
from functools import partial

def P(n):
    if n <= 65:
        return 0.008
    elif n <= 70:
        return 0.008 + 0.04 * (n - 65)
    elif n <= 75:
        return 0.208 + 0.08 * (n - 70)
    elif n <= 80:
        return 0.608 + 0.10 * (n - 75)
    else:
        return 1.0

def P_weapon(n):
    """武器池五星概率函数"""
    if n <= 65:
        return 0.007
    elif n <= 70:
        return 0.007 + 0.07 * (n - 65)
    elif n <= 75:
        return 0.357 + 0.08 * (n - 70)
    elif n <= 80:
        return 0.757 + 0.10 * (n - 75)
    else:
        return 1.0

def simulate_task1(num_simulations):
    """情况1: 抽取一个角色本体与五个回音频段+1把武器，不使用珊瑚"""
    total_paid_pulls = 0
    total_coral = 0
    
    for _ in range(num_simulations):
        paid_pulls = 0
        coral = 0
        character_pity_5 = 0
        character_pity_4 = 0
        weapon_pity_5 = 0
        weapon_pity_4 = 0
        character_guaranteed_4_up = False
        character_guaranteed_5_up = False
        weapon_guaranteed_4_up = False
        weapon_guaranteed_5_up = False
        weapon_fate_points = 0
        owned_4star_chars = {}
        owned_5star_chars = {}
        owned_4star_weapons = {}
        owned_5star_weapons = {}
        copies_of_up_char = 0
        copies_of_up_weapon = 0
        
        # 角色列表
        std_4star_chars = [f"std_4char_{i}" for i in range(1, 20)]
        up_4star_chars_char = [f"up_4char_{i}" for i in range(1, 4)]
        up_5star_char = "up_5char"
        std_5star_chars = [f"std_5char_{i}" for i in range(1, 6)]
        
        # 武器列表
        std_4star_weapons = [f"std_4weapon_{i}" for i in range(1, 21)]
        up_4star_weapons = [f"up_4weapon_{i}" for i in range(1, 6)]
        up_5star_weapon = "up_5weapon"
        std_5star_weapons = [f"std_5weapon_{i}" for i in range(1, 6)]
        
        # 抽取直到获得1个角色本体和5个回音频段+1把武器
        while not (copies_of_up_char >= 1 and min(copies_of_up_char - 1, 6) >= 5 and copies_of_up_weapon >= 1):
            paid_pulls += 1
            
            # 决定抽角色池还是武器池
            # 如果角色未完成，优先抽角色池
            if copies_of_up_char < 6:
                # 模拟角色池抽取
                n5 = character_pity_5 + 1
                prob_5 = P(n5)
                if random.random() < prob_5:
                    # 获得五星角色
                    character_pity_5 = 0
                    character_pity_4 = 0
                    
                    # 判断是否为UP角色
                    if character_guaranteed_5_up:
                        is_up = True
                        character_guaranteed_5_up = False
                    else:
                        if random.random() < 0.5:
                            is_up = True
                        else:
                            is_up = False
                            character_guaranteed_5_up = True
                    
                    if is_up:
                        # 获得UP角色
                        char_id = up_5star_char
                        copies_of_up_char += 1
                        
                        # 计算珊瑚
                        if char_id in owned_5star_chars:
                            count = owned_5star_chars[char_id]
                            if count < 7:
                                coral += 15
                            else:
                                coral += 40
                            owned_5star_chars[char_id] += 1
                        else:
                            owned_5star_chars[char_id] = 1
                            coral += 15
                    else:
                        # 获得非UP角色
                        char_id = random.choice(std_5star_chars)
                        if char_id in owned_5star_chars:
                            count = owned_5star_chars[char_id]
                            if count < 7:
                                coral += 15
                            else:
                                coral += 40
                            owned_5star_chars[char_id] += 1
                        else:
                            owned_5star_chars[char_id] = 1
                            coral += 15
                else:
                    character_pity_5 = n5
                    
                    # 检查四星
                    if character_pity_4 >= 9:
                        obtained_4star = True
                        character_pity_4 = 0
                    else:
                        if random.random() < 0.06:
                            obtained_4star = True
                            character_pity_4 = 0
                        else:
                            obtained_4star = False
                            character_pity_4 += 1
                    
                    if obtained_4star:
                        if character_guaranteed_4_up:
                            is_up = True
                            character_guaranteed_4_up = False
                        else:
                            if random.random() < 0.5:
                                is_up = True
                            else:
                                is_up = False
                                character_guaranteed_4_up = True
                        
                        if is_up:
                            # 获得UP四星角色
                            char_id = random.choice(up_4star_chars_char)
                            if char_id in owned_4star_chars:
                                count = owned_4star_chars[char_id]
                                if count < 7:
                                    coral += 3
                                else:
                                    coral += 8
                                owned_4star_chars[char_id] += 1
                            else:
                                owned_4star_chars[char_id] = 1
                                coral += 3
                        else:
                            # 获得非UP四星内容
                            r = random.randint(1, 28)
                            if r <= 8:
                                # 获得非UP四星角色
                                char_id = random.choice(std_4star_chars[:8])
                                if char_id in owned_4star_chars:
                                    count = owned_4star_chars[char_id]
                                    if count < 7:
                                        coral += 3
                                    else:
                                        coral += 8
                                    owned_4star_chars[char_id] += 1
                                else:
                                    owned_4star_chars[char_id] = 1
                                    coral += 3
                            else:
                                # 获得四星武器
                                coral += 3
            else:
                # 模拟武器池抽取
                n5 = weapon_pity_5 + 1
                prob_5 = P_weapon(n5)
                if random.random() < prob_5:
                    # 获得五星武器
                    weapon_pity_5 = 0
                    weapon_pity_4 = 0
                    
                    # 判断是否为UP武器
                    if weapon_guaranteed_5_up:
                        is_up = True
                        weapon_guaranteed_5_up = False
                    else:
                        if random.random() < 0.75:
                            is_up = True
                        else:
                            is_up = False
                            weapon_guaranteed_5_up = True
                    
                    if is_up:
                        # 获得UP武器
                        if weapon_fate_points == 2 or random.random() < 0.5:
                            # 获得目标UP武器
                            weapon_id = up_5star_weapon
                            copies_of_up_weapon += 1
                            weapon_fate_points = 0
                        else:
                            # 获得非目标UP武器
                            weapon_id = f"up_5weapon_other"
                            weapon_fate_points = min(weapon_fate_points + 1, 2)
                    else:
                        # 获得非UP武器
                        weapon_id = random.choice(std_5star_weapons)
                    
                    # 计算珊瑚
                    if weapon_id in owned_5star_weapons:
                        count = owned_5star_weapons[weapon_id]
                        if count < 7:
                            coral += 15
                        else:
                            coral += 40
                        owned_5star_weapons[weapon_id] += 1
                    else:
                        owned_5star_weapons[weapon_id] = 1
                        coral += 15
                else:
                    weapon_pity_5 = n5
                    
                    # 检查四星
                    if weapon_pity_4 >= 9:
                        obtained_4star = True
                        weapon_pity_4 = 0
                    else:
                        if random.random() < 0.06:
                            obtained_4star = True
                            weapon_pity_4 = 0
                        else:
                            obtained_4star = False
                            weapon_pity_4 += 1
                    
                    if obtained_4star:
                        if weapon_guaranteed_4_up:
                            is_up = True
                            weapon_guaranteed_4_up = False
                        else:
                            if random.random() < 0.75:
                                is_up = True
                            else:
                                is_up = False
                                weapon_guaranteed_4_up = True
                        
                        if is_up:
                            # 获得UP四星武器
                            weapon_id = random.choice(up_4star_weapons)
                            if weapon_id in owned_4star_weapons:
                                count = owned_4star_weapons[weapon_id]
                                if count < 7:
                                    coral += 3
                                else:
                                    coral += 8
                                owned_4star_weapons[weapon_id] += 1
                            else:
                                owned_4star_weapons[weapon_id] = 1
                                coral += 3
                        else:
                            # 获得非UP四星武器
                            weapon_id = random.choice(std_4star_weapons)
                            if weapon_id in owned_4star_weapons:
                                count = owned_4star_weapons[weapon_id]
                                if count < 7:
                                    coral += 3
                                else:
                                    coral += 8
                                owned_4star_weapons[weapon_id] += 1
                            else:
                                owned_4star_weapons[weapon_id] = 1
                                coral += 3
        
        total_paid_pulls += paid_pulls
        total_coral += coral
    
    return total_paid_pulls, total_coral

def simulate_task2(num_simulations):
    """情况2: 每满8个珊瑚就兑换一次抽数，抽取一个角色本体与六个回音频段+1把武器"""
    total_paid_pulls = 0
    total_remaining_coral = 0
    
    for _ in range(num_simulations):
        paid_pulls = 0
        coral = 0
        exchange_pulls = 0
        character_pity_5 = 0
        character_pity_4 = 0
        weapon_pity_5 = 0
        weapon_pity_4 = 0
        character_guaranteed_4_up = False
        character_guaranteed_5_up = False
        weapon_guaranteed_4_up = False
        weapon_guaranteed_5_up = False
        weapon_fate_points = 0
        owned_4star_chars = {}
        owned_5star_chars = {}
        owned_4star_weapons = {}
        owned_5star_weapons = {}
        copies_of_up_char = 0
        copies_of_up_weapon = 0
        
        # 角色列表
        std_4star_chars = [f"std_4char_{i}" for i in range(1, 20)]
        up_4star_chars_char = [f"up_4char_{i}" for i in range(1, 4)]
        up_5star_char = "up_5char"
        std_5star_chars = [f"std_5char_{i}" for i in range(1, 6)]
        
        # 武器列表
        std_4star_weapons = [f"std_4weapon_{i}" for i in range(1, 21)]
        up_4star_weapons = [f"up_4weapon_{i}" for i in range(1, 6)]
        up_5star_weapon = "up_5weapon"
        std_5star_weapons = [f"std_5weapon_{i}" for i in range(1, 6)]
        
        # 抽取直到获得1个角色本体和6个回音频段+1把武器
        while not (copies_of_up_char >= 1 and min(copies_of_up_char - 1, 6) >= 6 and copies_of_up_weapon >= 1):
            # 检查是否有兑换的抽数可用
            if exchange_pulls > 0:
                exchange_pulls -= 1
            else:
                paid_pulls += 1
            
            # 决定抽角色池还是武器池
            # 如果角色未完成，优先抽角色池
            if copies_of_up_char < 7:
                # 模拟角色池抽取
                n5 = character_pity_5 + 1
                prob_5 = P(n5)
                if random.random() < prob_5:
                    # 获得五星角色
                    character_pity_5 = 0
                    character_pity_4 = 0
                    
                    # 判断是否为UP角色
                    if character_guaranteed_5_up:
                        is_up = True
                        character_guaranteed_5_up = False
                    else:
                        if random.random() < 0.5:
                            is_up = True
                        else:
                            is_up = False
                            character_guaranteed_5_up = True
                    
                    if is_up:
                        # 获得UP角色
                        char_id = up_5star_char
                        copies_of_up_char += 1
                        
                        # 计算珊瑚
                        if char_id in owned_5star_chars:
                            count = owned_5star_chars[char_id]
                            if count < 7:
                                coral += 15
                            else:
                                coral += 40
                            owned_5star_chars[char_id] += 1
                        else:
                            owned_5star_chars[char_id] = 1
                            coral += 15
                    else:
                        # 获得非UP角色
                        char_id = random.choice(std_5star_chars)
                        if char_id in owned_5star_chars:
                            count = owned_5star_chars[char_id]
                            if count < 7:
                                coral += 15
                            else:
                                coral += 40
                            owned_5star_chars[char_id] += 1
                        else:
                            owned_5star_chars[char_id] = 1
                            coral += 15
                else:
                    character_pity_5 = n5
                    
                    # 检查四星
                    if character_pity_4 >= 9:
                        obtained_4star = True
                        character_pity_4 = 0
                    else:
                        if random.random() < 0.06:
                            obtained_4star = True
                            character_pity_4 = 0
                        else:
                            obtained_4star = False
                            character_pity_4 += 1
                    
                    if obtained_4star:
                        if character_guaranteed_4_up:
                            is_up = True
                            character_guaranteed_4_up = False
                        else:
                            if random.random() < 0.5:
                                is_up = True
                            else:
                                is_up = False
                                character_guaranteed_4_up = True
                        
                        if is_up:
                            # 获得UP四星角色
                            char_id = random.choice(up_4star_chars_char)
                            if char_id in owned_4star_chars:
                                count = owned_4star_chars[char_id]
                                if count < 7:
                                    coral += 3
                                else:
                                    coral += 8
                                owned_4star_chars[char_id] += 1
                            else:
                                owned_4star_chars[char_id] = 1
                                coral += 3
                        else:
                            # 获得非UP四星内容
                            r = random.randint(1, 28)
                            if r <= 8:
                                # 获得非UP四星角色
                                char_id = random.choice(std_4star_chars[:8])
                                if char_id in owned_4star_chars:
                                    count = owned_4star_chars[char_id]
                                    if count < 7:
                                        coral += 3
                                    else:
                                        coral += 8
                                    owned_4star_chars[char_id] += 1
                                else:
                                    owned_4star_chars[char_id] = 1
                                    coral += 3
                            else:
                                # 获得四星武器
                                coral += 3
            else:
                # 模拟武器池抽取
                n5 = weapon_pity_5 + 1
                prob_5 = P_weapon(n5)
                if random.random() < prob_5:
                    # 获得五星武器
                    weapon_pity_5 = 0
                    weapon_pity_4 = 0
                    
                    # 判断是否为UP武器
                    if weapon_guaranteed_5_up:
                        is_up = True
                        weapon_guaranteed_5_up = False
                    else:
                        if random.random() < 0.75:
                            is_up = True
                        else:
                            is_up = False
                            weapon_guaranteed_5_up = True
                    
                    if is_up:
                        # 获得UP武器
                        if weapon_fate_points == 2 or random.random() < 0.5:
                            # 获得目标UP武器
                            weapon_id = up_5star_weapon
                            copies_of_up_weapon += 1
                            weapon_fate_points = 0
                        else:
                            # 获得非目标UP武器
                            weapon_id = f"up_5weapon_other"
                            weapon_fate_points = min(weapon_fate_points + 1, 2)
                    else:
                        # 获得非UP武器
                        weapon_id = random.choice(std_5star_weapons)
                    
                    # 计算珊瑚
                    if weapon_id in owned_5star_weapons:
                        count = owned_5star_weapons[weapon_id]
                        if count < 7:
                            coral += 15
                        else:
                            coral += 40
                        owned_5star_weapons[weapon_id] += 1
                    else:
                        owned_5star_weapons[weapon_id] = 1
                        coral += 15
                else:
                    weapon_pity_5 = n5
                    
                    # 检查四星
                    if weapon_pity_4 >= 9:
                        obtained_4star = True
                        weapon_pity_4 = 0
                    else:
                        if random.random() < 0.06:
                            obtained_4star = True
                            weapon_pity_4 = 0
                        else:
                            obtained_4star = False
                            weapon_pity_4 += 1
                    
                    if obtained_4star:
                        if weapon_guaranteed_4_up:
                            is_up = True
                            weapon_guaranteed_4_up = False
                        else:
                            if random.random() < 0.75:
                                is_up = True
                            else:
                                is_up = False
                                weapon_guaranteed_4_up = True
                        
                        if is_up:
                            # 获得UP四星武器
                            weapon_id = random.choice(up_4star_weapons)
                            if weapon_id in owned_4star_weapons:
                                count = owned_4star_weapons[weapon_id]
                                if count < 7:
                                    coral += 3
                                else:
                                    coral += 8
                                owned_4star_weapons[weapon_id] += 1
                            else:
                                owned_4star_weapons[weapon_id] = 1
                                coral += 3
                        else:
                            # 获得非UP四星武器
                            weapon_id = random.choice(std_4star_weapons)
                            if weapon_id in owned_4star_weapons:
                                count = owned_4star_weapons[weapon_id]
                                if count < 7:
                                    coral += 3
                                else:
                                    coral += 8
                                owned_4star_weapons[weapon_id] += 1
                            else:
                                owned_4star_weapons[weapon_id] = 1
                                coral += 3
            
            # 每满8个珊瑚就兑换一次抽数
            while coral >= 8:
                coral -= 8
                exchange_pulls += 1
        
        total_paid_pulls += paid_pulls
        total_remaining_coral += coral
    
    return total_paid_pulls, total_remaining_coral

def run_simulations():
    """使用多核优化运行模拟"""
    num_simulations = 1000000
    num_cores = mp.cpu_count()
    
    print(f"使用 {num_cores} 个核心进行 {num_simulations} 次模拟...")
    print()
    
    # 模拟情况1: 抽取一个角色本体与五个回音频段+1把武器，不使用珊瑚
    print("正在模拟情况1: 抽取一个角色本体与五个回音频段+1把武器，不使用珊瑚...")
    
    # 分割任务到多个核心
    chunk_size = num_simulations // num_cores
    with mp.Pool(processes=num_cores) as pool:
        results = pool.map(simulate_task1, [chunk_size] * num_cores)
    
    # 汇总结果
    total_paid_pulls_1 = sum(result[0] for result in results)
    total_coral_1 = sum(result[1] for result in results)
    
    average_paid_pulls_1 = total_paid_pulls_1 / num_simulations
    average_coral_1 = total_coral_1 / num_simulations
    average_star_voice_1 = average_paid_pulls_1 * 160
    
    print(f"情况1 - 平均所需抽数: {average_paid_pulls_1:.2f}")
    print(f"情况1 - 平均总星声消耗: {average_star_voice_1:.2f}")
    print(f"情况1 - 平均所得珊瑚数: {average_coral_1:.2f}")
    print()
    
    # 模拟情况2: 每满8个珊瑚就兑换一次抽数，抽取一个角色本体与六个回音频段+1把武器
    print("正在模拟情况2: 每满8个珊瑚就兑换一次抽数，抽取一个角色本体与六个回音频段+1把武器...")
    
    # 分割任务到多个核心
    with mp.Pool(processes=num_cores) as pool:
        results = pool.map(simulate_task2, [chunk_size] * num_cores)
    
    # 汇总结果
    total_paid_pulls_2 = sum(result[0] for result in results)
    total_remaining_coral_2 = sum(result[1] for result in results)
    
    average_paid_pulls_2 = total_paid_pulls_2 / num_simulations
    average_remaining_coral_2 = total_remaining_coral_2 / num_simulations
    average_star_voice_2 = average_paid_pulls_2 * 160
    
    print(f"情况2 - 平均所需抽数: {average_paid_pulls_2:.2f}")
    print(f"情况2 - 平均总星声消耗: {average_star_voice_2:.2f}")
    print(f"情况2 - 平均剩余珊瑚数: {average_remaining_coral_2:.2f}")
    print()
    
    # 计算比较结果
    star_voice_saved = average_star_voice_2 - average_star_voice_1
    extra_coral = average_coral_1 - 360 - average_remaining_coral_2
    
    print(f"珊瑚兑换回音频段在6+1这个档位平均比珊瑚兑换抽数节约{star_voice_saved:.2f}星声，且额外获得{extra_coral:.2f}个余波珊瑚")

if __name__ == "__main__":
    run_simulations()
