"""
Symbol data for sign language notation system.
"""

HANDSHAPE_SYMBOLS = [
    {"id": "A", "label": "A", "unicode_char": "A", "description_ru": "Кулак", "description_en": "Fist", "group": "A — Кулак", "accent": "none", "visual_hint": "✊"},
    {"id": "A_dot", "label": "Ȧ", "unicode_char": "Ȧ", "description_ru": "Кулак, большой палец выставлен", "description_en": "Fist, thumb out", "group": "A — Кулак", "accent": "dot", "visual_hint": "👍"},
    {"id": "A_circ", "label": "Â", "unicode_char": "Â", "description_ru": "Кулак, вариант 2", "description_en": "Fist variant 2", "group": "A — Кулак", "accent": "circumflex", "visual_hint": "✊"},

    {"id": "G", "label": "G", "unicode_char": "G", "description_ru": "Указательный палец", "description_en": "Index finger", "group": "G — Указательный", "accent": "none", "visual_hint": "☝"},
    {"id": "G_dot", "label": "Ġ", "unicode_char": "Ġ", "description_ru": "Указательный, вариант с точкой", "description_en": "Index, dot variant", "group": "G — Указательный", "accent": "dot", "visual_hint": "☝"},
    {"id": "G_circ", "label": "Ĝ", "unicode_char": "Ĝ", "description_ru": "Указательный согнут", "description_en": "Index bent", "group": "G — Указательный", "accent": "circumflex", "visual_hint": "☝"},
    {"id": "G_bar", "label": "Ḡ", "unicode_char": "Ḡ", "description_ru": "Указательный, с чертой", "description_en": "Index, bar", "group": "G — Указательный", "accent": "bar", "visual_hint": "☝"},
    {"id": "G_2dots", "label": "G̈", "unicode_char": "G\u0308", "description_ru": "Указательный, две точки", "description_en": "Index, two dots", "group": "G — Указательный", "accent": "two_dots", "visual_hint": "☝"},
    {"id": "G_3dots", "label": "G⃛", "unicode_char": "G\u20DB", "description_ru": "Указательный, три точки", "description_en": "Index, three dots", "group": "G — Указательный", "accent": "three_dots", "visual_hint": "☝"},
    {"id": "Gd", "label": "Gd", "unicode_char": "Gd", "description_ru": "Указательный вниз", "description_en": "Index down", "group": "G — Указательный", "accent": "none", "visual_hint": "👇"},

    {"id": "R", "label": "R", "unicode_char": "R", "description_ru": "Скрещенные пальцы", "description_en": "Crossed fingers", "group": "R — Скрещенные", "accent": "none", "visual_hint": "🤞"},

    {"id": "H", "label": "H", "unicode_char": "H", "description_ru": "Указ. и средний вместе", "description_en": "Index+middle together", "group": "H — Два пальца", "accent": "none", "visual_hint": "🤚"},
    {"id": "H_bar", "label": "H̄", "unicode_char": "H\u0304", "description_ru": "H с чертой", "description_en": "H bar", "group": "H — Два пальца", "accent": "bar", "visual_hint": "🤚"},
    {"id": "H_dot", "label": "Ḣ", "unicode_char": "Ḣ", "description_ru": "H с точкой", "description_en": "H dot", "group": "H — Два пальца", "accent": "dot", "visual_hint": "🤚"},
    {"id": "H_circ", "label": "Ĥ", "unicode_char": "Ĥ", "description_ru": "H с крышечкой", "description_en": "H circumflex", "group": "H — Два пальца", "accent": "circumflex", "visual_hint": "🤚"},

    {"id": "V", "label": "V", "unicode_char": "V", "description_ru": "V-форма (два пальца врозь)", "description_en": "V-shape", "group": "V — Виктория", "accent": "none", "visual_hint": "✌"},
    {"id": "V_dot", "label": "V̇", "unicode_char": "V\u0307", "description_ru": "V с точкой", "description_en": "V dot", "group": "V — Виктория", "accent": "dot", "visual_hint": "✌"},
    {"id": "V_circ", "label": "V̂", "unicode_char": "V\u0302", "description_ru": "V с крышечкой", "description_en": "V circumflex", "group": "V — Виктория", "accent": "circumflex", "visual_hint": "✌"},
    {"id": "V_bar", "label": "V̄", "unicode_char": "V\u0304", "description_ru": "V с чертой", "description_en": "V bar", "group": "V — Виктория", "accent": "bar", "visual_hint": "✌"},

    {"id": "K", "label": "K", "unicode_char": "K", "description_ru": "K-форма", "description_en": "K-shape", "group": "K", "accent": "none", "visual_hint": "🤙"},

    {"id": "W", "label": "W", "unicode_char": "W", "description_ru": "Три пальца врозь", "description_en": "Three fingers spread", "group": "W — Три пальца", "accent": "none", "visual_hint": "🖖"},
    {"id": "Wm", "label": "Wm", "unicode_char": "Wm", "description_ru": "Wm-вариант", "description_en": "Wm variant", "group": "W — Три пальца", "accent": "none", "visual_hint": "🖖"},

    {"id": "NUM4", "label": "④", "unicode_char": "④", "description_ru": "Четыре пальца вместе", "description_en": "Four fingers", "group": "④ — Четыре", "accent": "none", "visual_hint": "🖐"},
    {"id": "F", "label": "F", "unicode_char": "F", "description_ru": "Кольцо (большой+указательный)", "description_en": "Ring (thumb+index)", "group": "F — Кольцо", "accent": "none", "visual_hint": "👌"},
    {"id": "F_bar", "label": "F̄", "unicode_char": "F\u0304", "description_ru": "F с чертой", "description_en": "F bar", "group": "F — Кольцо", "accent": "bar", "visual_hint": "👌"},
    {"id": "NUM7", "label": "⑦", "unicode_char": "⑦", "description_ru": "Семёрка", "description_en": "Seven", "group": "⑦ — Семь", "accent": "none", "visual_hint": "🤟"},

    {"id": "I", "label": "I", "unicode_char": "I", "description_ru": "Мизинец вытянут", "description_en": "Pinky extended", "group": "I — Мизинец", "accent": "none", "visual_hint": "🤙"},
    {"id": "I_bar", "label": "Ī", "unicode_char": "Ī", "description_ru": "I с чертой", "description_en": "I bar", "group": "I — Мизинец", "accent": "bar", "visual_hint": "🤙"},
    {"id": "Y", "label": "Y", "unicode_char": "Y", "description_ru": "Большой палец + мизинец", "description_en": "Thumb + pinky", "group": "Y", "accent": "none", "visual_hint": "🤙"},

    {"id": "CH", "label": "Ч", "unicode_char": "Ч", "description_ru": "Рога (Ч-форма)", "description_en": "Horns", "group": "Ч — Рога", "accent": "none", "visual_hint": "🤘"},
    {"id": "CH_dot", "label": "Ч̇", "unicode_char": "Ч\u0307", "description_ru": "Рога с точкой", "description_en": "Horns dot", "group": "Ч — Рога", "accent": "dot", "visual_hint": "🤘"},

    {"id": "NUM8", "label": "⑧", "unicode_char": "⑧", "description_ru": "Восьмёрка", "description_en": "Eight", "group": "⑧ — Восемь", "accent": "none", "visual_hint": "🤟"},
    {"id": "NUM8_dot", "label": "⑧̇", "unicode_char": "⑧\u0307", "description_ru": "Восьмёрка с точкой", "description_en": "Eight dot", "group": "⑧ — Восемь", "accent": "dot", "visual_hint": "🤟"},
    {"id": "NUM8_circ", "label": "⑧̂", "unicode_char": "⑧\u0302", "description_ru": "Восьмёрка с крышечкой", "description_en": "Eight circumflex", "group": "⑧ — Восемь", "accent": "circumflex", "visual_hint": "🤟"},

    {"id": "NUM5", "label": "⑤", "unicode_char": "⑤", "description_ru": "Пять пальцев растопырены", "description_en": "Five spread", "group": "⑤ — Пять", "accent": "none", "visual_hint": "🖐"},
    {"id": "NUM5_bar", "label": "⑤̄", "unicode_char": "⑤\u0304", "description_ru": "Пять с чертой", "description_en": "Five bar", "group": "⑤ — Пять", "accent": "bar", "visual_hint": "🖐"},
    {"id": "NUM5_dot", "label": "⑤̇", "unicode_char": "⑤\u0307", "description_ru": "Пять с точкой", "description_en": "Five dot", "group": "⑤ — Пять", "accent": "dot", "visual_hint": "🖐"},
    {"id": "NUM5_circ", "label": "⑤̂", "unicode_char": "⑤\u0302", "description_ru": "Пять с крышечкой", "description_en": "Five circumflex", "group": "⑤ — Пять", "accent": "circumflex", "visual_hint": "🖐"},

    {"id": "B", "label": "B", "unicode_char": "B", "description_ru": "Плоская ладонь", "description_en": "Flat hand", "group": "B — Ладонь", "accent": "none", "visual_hint": "✋"},
    {"id": "B_dot", "label": "Ḃ", "unicode_char": "Ḃ", "description_ru": "Ладонь с точкой", "description_en": "Flat dot", "group": "B — Ладонь", "accent": "dot", "visual_hint": "✋"},
    {"id": "B_circ", "label": "B̂", "unicode_char": "B\u0302", "description_ru": "Ладонь с крышечкой", "description_en": "Flat circumflex", "group": "B — Ладонь", "accent": "circumflex", "visual_hint": "✋"},
    {"id": "B_bar", "label": "B̄", "unicode_char": "B\u0304", "description_ru": "Ладонь с чертой", "description_en": "Flat bar", "group": "B — Ладонь", "accent": "bar", "visual_hint": "✋"},
    {"id": "B_2dots", "label": "B̈", "unicode_char": "B\u0308", "description_ru": "Ладонь с двумя точками", "description_en": "Flat two dots", "group": "B — Ладонь", "accent": "two_dots", "visual_hint": "✋"},
    {"id": "B_arc", "label": "B̑", "unicode_char": "B\u0311", "description_ru": "Ладонь с дугой", "description_en": "Flat arc", "group": "B — Ладонь", "accent": "arc", "visual_hint": "✋"},

    {"id": "C", "label": "C", "unicode_char": "C", "description_ru": "C-форма", "description_en": "C-shape", "group": "C", "accent": "none", "visual_hint": "🤏"},
    {"id": "C_dot", "label": "Ċ", "unicode_char": "Ċ", "description_ru": "C с точкой", "description_en": "C dot", "group": "C", "accent": "dot", "visual_hint": "🤏"},
    {"id": "O", "label": "O", "unicode_char": "O", "description_ru": "O-форма (кольцо)", "description_en": "O-shape", "group": "O", "accent": "none", "visual_hint": "👌"},
    {"id": "E", "label": "E", "unicode_char": "E", "description_ru": "E-форма (полусогнутые)", "description_en": "E-shape", "group": "E", "accent": "none", "visual_hint": "✊"},
    {"id": "E_dot", "label": "Ė", "unicode_char": "Ė", "description_ru": "E с точкой", "description_en": "E dot", "group": "E", "accent": "dot", "visual_hint": "✊"},
]

LOCATION_SYMBOLS = [
    {"id": "loc_neutral", "label": "Ø", "unicode_char": "Ø", "description_ru": "Нейтральное место", "description_en": "Neutral space", "group": "Нейтральное"},
    {"id": "loc_top_head", "label": "ʞ", "unicode_char": "ʞ", "description_ru": "Верх головы", "description_en": "Top of head", "group": "Голова"},
    {"id": "loc_upper_face", "label": "∩", "unicode_char": "∩", "description_ru": "Верхняя часть лица", "description_en": "Upper face", "group": "Голова"},
    {"id": "loc_whole_face", "label": "◯", "unicode_char": "◯", "description_ru": "Всё лицо", "description_en": "Whole face", "group": "Голова"},
    {"id": "loc_eye", "label": "Ш", "unicode_char": "Ш", "description_ru": "Глаз", "description_en": "Eye", "group": "Голова"},
    {"id": "loc_nose", "label": "Д", "unicode_char": "Д", "description_ru": "Нос", "description_en": "Nose", "group": "Голова"},
    {"id": "loc_cheek", "label": "Э", "unicode_char": "Э", "description_ru": "Щека", "description_en": "Cheek", "group": "Голова"},
    {"id": "loc_ear", "label": "⊃", "unicode_char": "⊃", "description_ru": "Ухо", "description_en": "Ear", "group": "Голова"},
    {"id": "loc_mouth", "label": "⊂⊃", "unicode_char": "⊂⊃", "description_ru": "Рот и губы", "description_en": "Mouth/lips", "group": "Голова"},
    {"id": "loc_chin", "label": "U", "unicode_char": "U", "description_ru": "Подбородок", "description_en": "Chin", "group": "Голова"},
    {"id": "loc_under_chin", "label": "Ü", "unicode_char": "Ü", "description_ru": "Под подбородком", "description_en": "Under chin", "group": "Голова"},
    {"id": "loc_throat", "label": "Π", "unicode_char": "Π", "description_ru": "Горло / шея", "description_en": "Throat/neck", "group": "Шея"},
    {"id": "loc_chest", "label": "[]", "unicode_char": "[]", "description_ru": "Грудь", "description_en": "Chest", "group": "Туловище"},
    {"id": "loc_chest_left", "label": "[ˡ", "unicode_char": "[ˡ", "description_ru": "Левая сторона груди", "description_en": "Left chest", "group": "Туловище"},
    {"id": "loc_chest_right", "label": "ʳ]", "unicode_char": "ʳ]", "description_ru": "Правая сторона груди", "description_en": "Right chest", "group": "Туловище"},
    {"id": "loc_shoulders", "label": "⌐¬", "unicode_char": "⌐¬", "description_ru": "Перед плечами", "description_en": "Shoulders front", "group": "Туловище"},
    {"id": "loc_left_shoulder", "label": "⌐ˡ", "unicode_char": "⌐ˡ", "description_ru": "Левое плечо", "description_en": "Left shoulder", "group": "Туловище"},
    {"id": "loc_right_shoulder", "label": "ˡ⌐", "unicode_char": "ˡ⌐", "description_ru": "Правое плечо", "description_en": "Right shoulder", "group": "Туловище"},
    {"id": "loc_trunk_upper", "label": "⌈⌉", "unicode_char": "⌈⌉", "description_ru": "Верхняя часть туловища", "description_en": "Upper trunk", "group": "Туловище"},
    {"id": "loc_trunk_lower", "label": "⌊⌋", "unicode_char": "⌊⌋", "description_ru": "Нижняя часть туловища", "description_en": "Lower trunk", "group": "Туловище"},
    {"id": "loc_upper_arm", "label": "ǂ", "unicode_char": "ǂ", "description_ru": "Плечо (верх руки)", "description_en": "Upper arm", "group": "Рука"},
    {"id": "loc_elbow", "label": "ʲ", "unicode_char": "ʲ", "description_ru": "Локоть", "description_en": "Elbow", "group": "Рука"},
    {"id": "loc_forearm", "label": "ǁ", "unicode_char": "ǁ", "description_ru": "Предплечье", "description_en": "Forearm", "group": "Рука"},
    {"id": "loc_wrist_in", "label": "α", "unicode_char": "α", "description_ru": "Внутри запястья", "description_en": "Wrist inside", "group": "Рука"},
    {"id": "loc_wrist_out", "label": "ο", "unicode_char": "ο", "description_ru": "Тыл запястья", "description_en": "Wrist back", "group": "Рука"},
    {"id": "loc_hip", "label": "Н", "unicode_char": "Н", "description_ru": "Бедро", "description_en": "Hip", "group": "Нога"},
    {"id": "loc_upper_leg", "label": "‼", "unicode_char": "‼", "description_ru": "Верхняя часть ноги", "description_en": "Upper leg", "group": "Нога"},
    {"id": "loc_left_body", "label": "⟨", "unicode_char": "⟨", "description_ru": "Левая сторона тела", "description_en": "Left body", "group": "Стороны"},
    {"id": "loc_right_body", "label": "⟩", "unicode_char": "⟩", "description_ru": "Правая сторона тела", "description_en": "Right body", "group": "Стороны"},
]

MOVEMENT_SYMBOLS = [
    {"id": "mov_none", "label": "●", "unicode_char": "●", "description_ru": "Нет движения", "description_en": "No movement", "group": "Направление"},
    {"id": "mov_up", "label": "∧", "unicode_char": "∧", "description_ru": "Вверх", "description_en": "Up", "group": "Направление"},
    {"id": "mov_down", "label": "∨", "unicode_char": "∨", "description_ru": "Вниз", "description_en": "Down", "group": "Направление"},
    {"id": "mov_up_down", "label": "↕", "unicode_char": "↕", "description_ru": "Вверх и вниз", "description_en": "Up and down", "group": "Направление"},
    {"id": "mov_towards", "label": "τ", "unicode_char": "τ", "description_ru": "К говорящему", "description_en": "Towards signer", "group": "Направление"},
    {"id": "mov_away", "label": "⊥", "unicode_char": "⊥", "description_ru": "От говорящего", "description_en": "Away from signer", "group": "Направление"},
    {"id": "mov_towards_away", "label": "⇅", "unicode_char": "⇅", "description_ru": "К и от говорящего", "description_en": "Towards and away", "group": "Направление"},
    {"id": "mov_left", "label": "<", "unicode_char": "<", "description_ru": "Влево", "description_en": "Left", "group": "Направление"},
    {"id": "mov_right", "label": ">", "unicode_char": ">", "description_ru": "Вправо", "description_en": "Right", "group": "Направление"},
    {"id": "mov_side", "label": "⟷", "unicode_char": "⟷", "description_ru": "Из стороны в сторону", "description_en": "Side to side", "group": "Направление"},

    {"id": "mov_apart", "label": "↔", "unicode_char": "↔", "description_ru": "Друг от друга", "description_en": "Apart", "group": "Взаимодействие"},
    {"id": "mov_together", "label": "⇉", "unicode_char": "⇉", "description_ru": "Друг к другу", "description_en": "Together", "group": "Взаимодействие"},
    {"id": "mov_join", "label": "⊕", "unicode_char": "⊕", "description_ru": "Соединиться", "description_en": "Join", "group": "Взаимодействие"},
    {"id": "mov_enter", "label": "⊙", "unicode_char": "⊙", "description_ru": "Войти", "description_en": "Enter", "group": "Взаимодействие"},
    {"id": "mov_cross", "label": "✦", "unicode_char": "✦", "description_ru": "Пересечь", "description_en": "Cross", "group": "Взаимодействие"},
    {"id": "mov_swap", "label": "⇄", "unicode_char": "⇄", "description_ru": "Поменяться местами", "description_en": "Change places", "group": "Взаимодействие"},
    {"id": "mov_circle", "label": "◯", "unicode_char": "◯", "description_ru": "По кругу", "description_en": "Circle", "group": "Взаимодействие"},
    {"id": "mov_touch", "label": "×", "unicode_char": "×", "description_ru": "Касание", "description_en": "Touch", "group": "Контакт"},

    {"id": "mov_twist", "label": "ω", "unicode_char": "ω", "description_ru": "Поворот запястья", "description_en": "Twist wrist", "group": "Запястье"},
    {"id": "mov_palm_up", "label": "⊓", "unicode_char": "⊓", "description_ru": "Ладонь вверх", "description_en": "Palm up", "group": "Запястье"},
    {"id": "mov_palm_down", "label": "⊔", "unicode_char": "⊔", "description_ru": "Ладонь вниз", "description_en": "Palm down", "group": "Запястье"},
    {"id": "mov_bend", "label": "η", "unicode_char": "η", "description_ru": "Сгиб в запястье", "description_en": "Bend wrist", "group": "Запястье"},
    {"id": "mov_knuckle_bend", "label": "Μ", "unicode_char": "Μ", "description_ru": "Сгиб в суставах", "description_en": "Knuckle bend", "group": "Запястье"},
    {"id": "mov_flex", "label": "μ", "unicode_char": "μ", "description_ru": "Сгиб в фалангах", "description_en": "Flex", "group": "Запястье"},
    {"id": "mov_wiggle", "label": "≋", "unicode_char": "≋", "description_ru": "Шевеление пальцами", "description_en": "Wiggle", "group": "Запястье"},
    {"id": "mov_rub", "label": "⊞", "unicode_char": "⊞", "description_ru": "Большой палец трётся", "description_en": "Thumb rubs", "group": "Запястье"},

    {"id": "mov_open", "label": "□", "unicode_char": "□", "description_ru": "Раскрыть", "description_en": "Open", "group": "Модификаторы"},
    {"id": "mov_close", "label": "■", "unicode_char": "■", "description_ru": "Закрыть", "description_en": "Close", "group": "Модификаторы"},
    {"id": "mov_short", "label": "˙", "unicode_char": "˙", "description_ru": "Короткое движение", "description_en": "Short", "group": "Модификаторы"},
    {"id": "mov_sharp", "label": "ˈ", "unicode_char": "ˈ", "description_ru": "Резкое движение", "description_en": "Sharp", "group": "Модификаторы"},
    {"id": "mov_alt", "label": "∼", "unicode_char": "∼", "description_ru": "Попеременные", "description_en": "Alternating", "group": "Модификаторы"},
    {"id": "mov_repeat", "label": "˜", "unicode_char": "˜", "description_ru": "Повторение", "description_en": "Repeated", "group": "Модификаторы"},
]

ORIENTATION_SYMBOLS = [
    {"id": "ori_up", "label": "∧", "unicode_char": "∧", "description_ru": "Вверх", "description_en": "Up"},
    {"id": "ori_down", "label": "∨", "unicode_char": "∨", "description_ru": "Вниз", "description_en": "Down"},
    {"id": "ori_towards", "label": "τ", "unicode_char": "τ", "description_ru": "К говорящему", "description_en": "Towards"},
    {"id": "ori_away", "label": "⊥", "unicode_char": "⊥", "description_ru": "От говорящего", "description_en": "Away"},
    {"id": "ori_left", "label": "<", "unicode_char": "<", "description_ru": "Влево", "description_en": "Left"},
    {"id": "ori_right", "label": ">", "unicode_char": ">", "description_ru": "Вправо", "description_en": "Right"},
]

HAND_ARRANGEMENT_SYMBOLS = [
    {"id": "ha_right_up", "label": "A̅", "unicode_char": "A\u0305", "description_ru": "Правая выше левой", "description_en": "Right higher"},
    {"id": "ha_left_up", "label": "A̲", "unicode_char": "A\u0332", "description_ru": "Левая выше правой", "description_en": "Left higher"},
    {"id": "ha_side", "label": "‖", "unicode_char": "‖", "description_ru": "Рядом", "description_en": "Side by side"},
    {"id": "ha_contact", "label": "×", "unicode_char": "×", "description_ru": "Контакт", "description_en": "Contact"},
    {"id": "ha_nearer", "label": "⊣", "unicode_char": "⊣", "description_ru": "Ближе к телу", "description_en": "Nearer body"},
    {"id": "ha_interlink", "label": "⊗", "unicode_char": "⊗", "description_ru": "Сцепление", "description_en": "Interlinking"},
    {"id": "ha_inside", "label": "⊙", "unicode_char": "⊙", "description_ru": "Одна внутри другой", "description_en": "One inside other"},
    {"id": "ha_crossed", "label": "⊘", "unicode_char": "⊘", "description_ru": "Перекрещены", "description_en": "Crossed"},
]

HAND_PARTS_SYMBOLS = [
    {"id": "hp_thumb", "label": "a", "unicode_char": "ₐ", "description_ru": "Большой палец", "description_en": "Thumb"},
    {"id": "hp_index", "label": "e", "unicode_char": "ₑ", "description_ru": "Указательный", "description_en": "Index"},
    {"id": "hp_middle", "label": "i", "unicode_char": "ᵢ", "description_ru": "Средний", "description_en": "Middle"},
    {"id": "hp_ring", "label": "o", "unicode_char": "ₒ", "description_ru": "Безымянный", "description_en": "Ring"},
    {"id": "hp_pinky", "label": "u", "unicode_char": "ᵤ", "description_ru": "Мизинец", "description_en": "Pinky"},
    {"id": "hp_12", "label": "1", "unicode_char": "₁", "description_ru": "Между большим и указательным", "description_en": "Between thumb/index"},
    {"id": "hp_23", "label": "2", "unicode_char": "₂", "description_ru": "Между указательным и средним", "description_en": "Between index/middle"},
    {"id": "hp_34", "label": "3", "unicode_char": "₃", "description_ru": "Между средним и безымянным", "description_en": "Between middle/ring"},
    {"id": "hp_45", "label": "4", "unicode_char": "₄", "description_ru": "Между безымянным и мизинцем", "description_en": "Between ring/pinky"},
]

# Порядок клавиш QWERTY для маппинга
QWERTY_ROWS = [
    list("`1234567890-="),
    list("qwertyuiop[]\\"),
    list("asdfghjkl;'"),
    list("zxcvbnm,./"),
]

def _build_key_map(symbols):
    """Присваивает символам клавиши QWERTY по порядку."""
    all_keys = []
    for row in QWERTY_ROWS:
        all_keys.extend(row)
    mapping = {}
    for i, sym in enumerate(symbols):
        if i < len(all_keys):
            mapping[all_keys[i]] = sym["id"]
    return mapping

HANDSHAPE_KEY_MAP = _build_key_map(HANDSHAPE_SYMBOLS)
LOCATION_KEY_MAP = _build_key_map(LOCATION_SYMBOLS)
MOVEMENT_KEY_MAP = _build_key_map(MOVEMENT_SYMBOLS)

def get_symbol_by_id(symbol_id, symbols_list=None):
    """Найти символ по ID."""
    lists = [symbols_list] if symbols_list else [
        HANDSHAPE_SYMBOLS, LOCATION_SYMBOLS, MOVEMENT_SYMBOLS,
        ORIENTATION_SYMBOLS, HAND_ARRANGEMENT_SYMBOLS, HAND_PARTS_SYMBOLS
    ]
    for lst in lists:
        if lst is None:
            continue
        for s in lst:
            if s["id"] == symbol_id:
                return s
    return None

def get_key_map(layer):
    return {"handshape": HANDSHAPE_KEY_MAP, "location": LOCATION_KEY_MAP, "movement": MOVEMENT_KEY_MAP}.get(layer, {})

def get_symbols(layer):
    return {"handshape": HANDSHAPE_SYMBOLS, "location": LOCATION_SYMBOLS, "movement": MOVEMENT_SYMBOLS}.get(layer, [])