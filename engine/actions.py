
"""
Reusable character animation actions.
Each action is a timeline of poses and movements.
"""

ACTIONS = {
    "idle": [
        (0.0, "idle", 0, 0),
        (1.0, "idle", 0, -2),
        (2.0, "idle", 0, 0),
    ],

    "walk": [
        (0.0, "walk", 0, 0),
        (0.25, "walk", 3, -2),
        (0.5, "walk", 0, 0),
        (0.75, "walk", -3, -2),
        (1.0, "walk", 0, 0),
    ],

    "point": [
        (0.0, "idle", 0, 0),
        (0.3, "point", 0, 0),
        (1.5, "point", 0, 0),
        (2.0, "idle", 0, 0),
    ],

    "react": [
        (0.0, "idle", 0, 0),
        (0.15, "idle", 0, -5),
        (0.35, "idle", 0, 2),
        (0.7, "idle", 0, 0),
    ],
}


def get_action_frame(action, time_seconds):
    """Return the character's pose and position at a given time."""

    timeline = ACTIONS.get(action, ACTIONS["idle"])

    duration = timeline[-1][0]

    if duration > 0:
        time_seconds = time_seconds % duration

    previous = timeline[0]
    following = timeline[-1]

    for i in range(len(timeline) - 1):
        if timeline[i][0] <= time_seconds <= timeline[i + 1][0]:
            previous = timeline[i]
            following = timeline[i + 1]
            break

    start_time, start_pose, start_x, start_y = previous
    end_time, end_pose, end_x, end_y = following

    if end_time == start_time:
        progress = 0
    else:
        progress = (
            (time_seconds - start_time) /
            (end_time - start_time)
        )

    # Smooth movement
    progress = progress * progress * (3 - 2 * progress)

    return {
        "pose": start_pose if progress < 0.5 else end_pose,
        "x": start_x + (end_x - start_x) * progress,
        "y": start_y + (end_y - start_y) * progress,
    }
  
