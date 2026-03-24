def generate_seq(bans):
    s = []
    
    if bans == 5:
        # --- Tournament Ban 5 ---
        
        # 1st Ban Phase : Blue, Red, Blue, Red, Blue, Red
        s.extend([('Ban', 'Blue'), ('Ban', 'Red'), ('Ban', 'Blue'), ('Ban', 'Red'), ('Ban', 'Blue'), ('Ban', 'Red')])
        
        # 1st Pick Phase : Blue, Red, Red, Blue, Blue, Red
        s.extend([('Pick', 'Blue'), ('Pick', 'Red'), ('Pick', 'Red'), ('Pick', 'Blue'), ('Pick', 'Blue'), ('Pick', 'Red')])
        
        # 2nd Ban Phase : Red, Blue, Red, Blue
        s.extend([('Ban', 'Red'), ('Ban', 'Blue'), ('Ban', 'Red'), ('Ban', 'Blue')])
        
        # 2nd Pick Phase : Red, Blue, Blue, Red
        s.extend([('Pick', 'Red'), ('Pick', 'Blue'), ('Pick', 'Blue'), ('Pick', 'Red')])
        
    elif bans == 3:
        # --- Tournament Ban 3 ---
        
        # 1st Ban Phase : Blue, Red, Blue, Red
        s.extend([('Ban', 'Blue'), ('Ban', 'Red'), ('Ban', 'Blue'), ('Ban', 'Red')])
        
        # 1st Pick Phase : Blue, Red, Red, Blue, Blue, Red
        s.extend([('Pick', 'Blue'), ('Pick', 'Red'), ('Pick', 'Red'), ('Pick', 'Blue'), ('Pick', 'Blue'), ('Pick', 'Red')])
        
        # 2nd Ban Phase : Red, Blue
        s.extend([('Ban', 'Red'), ('Ban', 'Blue')])
        
        # 2nd Pick Phase : Red, Blue, Blue, Red
        s.extend([('Pick', 'Red'), ('Pick', 'Blue'), ('Pick', 'Blue'), ('Pick', 'Red')])

    return s