# create shallow copy of "PokeAttributes"
att = attributes["PokeAttributes"]
# 18 (0-17) attributes for type1
type1_attribute = att["type1"][random.randint(0, 17)]
# 19 (0-18) for type2
type2_attribute = att["type2"][random.randint(0, 18)]
# 2  (0-1)for legendary
legendary_attribute = att["legendary"][random.randint(0, 1)]