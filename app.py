print("--- 欢迎使用国补价格计算器 (含店补版) ---")

while True:
    choice = input("\n输入 'c' 开始计算，输入 'quit' 退出程序: ").strip().lower()

    if choice == 'quit':
        print("感谢使用，再见！")
        break 
    
    elif choice == 'c':
        try:
            # 1. 获取原价
            original_price = float(input("请输入商品原价（元）: "))
            
            # 2. 处理店补逻辑
            has_shop_discount = input("是否有店补？(y/n): ").strip().lower()
            shop_discount = 0.0
            
            if has_shop_discount == 'y':
                shop_discount = float(input("请输入店补减免金额（元）: "))
            
            # 计算扣除店补后的中间价
            intermediate_price = original_price - shop_discount
            if intermediate_price < 0:
                intermediate_price = 0
            
            # 3. 执行国补逻辑 (基于扣除店补后的价格计算)
            # 逻辑：85折（即优惠15%），但国补最高优惠通常有上限（这里沿用你之前的1500逻辑）
            if intermediate_price <= 10000:
                national_subsidy = intermediate_price * 0.15
                final_price = intermediate_price * 0.85
            else:
                national_subsidy = 1500
                final_price = intermediate_price - 1500
            
            # 4. 输出结果
            total_discount = shop_discount + national_subsidy
            print("-" * 30)
            print(f"原始价格: {original_price:.2f} 元")
            if shop_discount > 0:
                print(f"店补减免: -{shop_discount:.2f} 元")
            print(f"国补金额: -{national_subsidy:.2f} 元")
            print(f">>> 最终到手价: {final_price:.2f} 元")
            print(f">>> 总共节省了: {total_discount:.2f} 元")
            print("-" * 30)
            
        except ValueError:
            print("错误：请输入有效的数字！")
            
    else:
        print("指令无效，请输入 'c' 或 'quit'。")