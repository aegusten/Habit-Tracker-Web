PRESET_HABITS = {
    'stop_smoking': {
        'extra_fields': [
            {'key': 'cigarettes_per_day', 'label': 'Cigarettes per Day', 'type': 'number'},
            {'key': 'craving_level', 'label': 'Craving Level (1-10)', 'type': 'number'},
            {'key': 'planned_quit_date', 'label': 'Planned Quit Date', 'type': 'date'},
            {'key': 'nicotine_replacement', 'label': 'Replacements', 'type': 'text'},
            {'key': 'trigger_coping', 'label': 'Triggers & Coping Strategies', 'type': 'text'}
        ]
    },
    'wake_up_early': {
        'extra_fields': [
            {'key': 'current_wake_time', 'label': 'Current Wake Time', 'type': 'time'},
            {'key': 'desired_wake_time', 'label': 'Desired Wake Time', 'type': 'time'},
            {'key': 'bedtime', 'label': 'Bedtime', 'type': 'time'},
            {'key': 'sleep_quality', 'label': 'Sleep Quality (1-10)', 'type': 'number'},
            {'key': 'snooze_count', 'label': 'Number of Snoozes', 'type': 'number'}
        ]
    },
    'eat_healthy': {
        'extra_fields': [
            {'key': 'daily_calorie_target', 'label': 'Daily Calorie Target', 'type': 'number'},
            {'key': 'fruit_veg_target', 'label': 'Fruit & Veg Servings', 'type': 'number'},
            {'key': 'water_intake_goal', 'label': 'Water Intake (glasses/day)', 'type': 'number'},
            {'key': 'junk_food_consumption', 'label': 'Junk Food Consumption', 'type': 'number'}
        ]
    }
}

PRESET_TEMPLATES = [
    {'key': 'stop_smoking', 'icon': 'bi-emoji-smile', 'label': 'Stop Smoking'},
    {'key': 'wake_up_early', 'icon': 'bi-sunrise', 'label': 'Wake Up Early'},
    {'key': 'eat_healthy', 'icon': 'bi-apple', 'label': 'Eat Healthy'},
    {'key': 'custom', 'icon': 'bi-pencil-square', 'label': 'Custom'}
]

AWARD_MESSAGES = {
    'stop_smoking': [
        "Great job staying smoke-free today! 💨",
        "You’re building real strength. Keep breathing clean! 💪",
        "Amazing progress! Your lungs are already thanking you 👃",
        "You're unstoppable! No puff can stop you now 🚭",
        "Champion of Control – Freedom from smoking is yours 🏆"
    ],
    'eat_healthy': [
        "Healthy bites, healthy life! 🥗",
        "Your body is smiling inside! Keep fueling it right 💚",
        "You're crunching those goals – just like carrots! 🥕",
        "Nourish to flourish! 🌿 You're doing excellent.",
        "Green Badge Unlocked! You're a nutrition ninja! 🥦🏆"
    ],
    'wake_up_early': [
        "Early bird vibes activated! ☀️",
        "Morning master! Keep rising strong 💡",
        "You're building discipline with each sunrise 🌅",
        "Consistent mornings, powerful days 🚀",
        "Wakey Legend: You own the a.m. hours 🏆"
    ],
    'custom': [
        "One step at a time. You’re doing great! 👣",
        "You're showing up – and that’s winning! 🏁",
        "Your commitment is solid. Keep going 💥",
        "You're in the habit zone. Focused and steady 🧠",
        "Custom Champion: You're crushing your own path! 🏆"
    ]
}

NOTIFICATION_MESSAGES = {
    'stop_smoking': [
        "You're building consistency – don’t stop now 🌟",
        "Cravings are temporary – freedom is forever 💨",
        "Each day smoke-free is a win! 🎯",
        "Breathe deep. You’re stronger than you think 💪",
        "Champion of Control – smoke-free and proud 🏆"
    ],
    'eat_healthy': [
        "Healthy bites, healthy life 🥗",
        "Fruit + Veg = Fuel 💚",
        "You're crushing your greens goal! 🥦",
        "One snack at a time 🍏",
        "Eat clean, feel great ✨"
    ],
    'wake_up_early': [
        "Sun’s up – and so are you 🌞",
        "You’re owning your morning 🚀",
        "Wakey wakey, legend! 🏅",
        "Routine power activated 🔁",
        "Start strong, finish stronger 💼"
    ],
    'custom': [
        "One step at a time. You’ve got this 👣",
        "You're showing up – and that’s a win 🏁",
        "Staying steady in your lane 🛣️",
        "You’re in the habit zone 🔥",
        "Custom goal, custom greatness 🛠️"
    ]
}


def get_notification_message(habit_type, stage=0):
    messages = NOTIFICATION_MESSAGES.get(habit_type, NOTIFICATION_MESSAGES["custom"])
    return messages[stage] if stage < len(messages) else messages[-1]


def get_random_reminder(habit_type):
    from random import choice
    return choice(NOTIFICATION_MESSAGES.get(habit_type, NOTIFICATION_MESSAGES['custom']))

def get_award_message(habit_type, stage=0):
    messages = AWARD_MESSAGES.get(habit_type, AWARD_MESSAGES["custom"])
    return messages[stage] if stage < len(messages) else messages[-1]


def get_random_award(habit_type):
    from random import choice
    return choice(AWARD_MESSAGES.get(habit_type, AWARD_MESSAGES['custom']))
