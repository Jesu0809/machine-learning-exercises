import random
import numpy as np
from sklearn.linear_model import SGDRegressor


# 0 = open path, 1 = wall, 2 = danger zone (enterable, but penalized).
CELL_OPEN = 0
CELL_WALL = 1
CELL_DANGER = 2

GRID = [
    [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 2, 1, 0, 2, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 2, 0, 0, 1, 0],
    [2, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 2, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 2, 0, 0, 1, 0, 0, 2, 0],
    [0, 2, 0, 2, 0, 1, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
]

START = (0, 0)
GOAL = (9, 9)


# Row and column changes for each action.
ACTIONS = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1)
]

ACTION_NAMES = [
    "Up",
    "Down",
    "Left",
    "Right"
]

ROWS = len(GRID)
COLUMNS = len(GRID[0])
NUMBER_OF_ACTIONS = len(ACTIONS)
NUMBER_OF_FEATURES = ROWS * COLUMNS * NUMBER_OF_ACTIONS

# Five reward categories, one value each.
REWARD_VALID_MOVE = -1
REWARD_OFF_GRID = -3
REWARD_WALL_HIT = -5
REWARD_DANGER_ZONE = -10
REWARD_GOAL = 50

REWARD_TABLE = {
    "valid_move": REWARD_VALID_MOVE,
    "off_grid": REWARD_OFF_GRID,
    "wall_hit": REWARD_WALL_HIT,
    "danger_zone": REWARD_DANGER_ZONE,
    "goal": REWARD_GOAL,
}

# Training configuration, kept as named constants so it can be shown as-is.
GAMMA = 0.95
EPSILON_START = 1.0
EPSILON_MIN = 0.05
EPSILON_DECAY = 0.995
LEARNING_RATE = 0.1
MAX_STEPS_PER_EPISODE = 300

TRAINING_CONFIG = {
    "gamma": GAMMA,
    "epsilon_start": EPSILON_START,
    "epsilon_min": EPSILON_MIN,
    "epsilon_decay": EPSILON_DECAY,
    "learning_rate": LEARNING_RATE,
    "max_steps_per_episode": MAX_STEPS_PER_EPISODE,
}


def cell_type(position):

    if position == GOAL:
        return "Goal"

    if position == START:
        return "Start"

    value = GRID[position[0]][position[1]]

    if value == CELL_WALL:
        return "Wall"

    if value == CELL_DANGER:
        return "Danger"

    return "Open"


def step(state, action):

    row = state[0] + ACTIONS[action][0]
    column = state[1] + ACTIONS[action][1]

    # Reject moves outside the grid.
    if not (0 <= row < ROWS and 0 <= column < COLUMNS):
        return state, REWARD_OFF_GRID, False

    # Reject moves into a wall.
    if GRID[row][column] == CELL_WALL:
        return state, REWARD_WALL_HIT, False

    next_state = (row, column)

    # Reaching the goal ends the episode.
    if next_state == GOAL:
        return next_state, REWARD_GOAL, True

    # Danger zones can be entered, but cost more than a normal move.
    if GRID[row][column] == CELL_DANGER:
        return next_state, REWARD_DANGER_ZONE, False

    return next_state, REWARD_VALID_MOVE, False


def encode(state, action):

    features = np.zeros(NUMBER_OF_FEATURES, dtype=float)

    state_index = state[0] * COLUMNS + state[1]
    feature_index = state_index * NUMBER_OF_ACTIONS + action

    features[feature_index] = 1.0

    return features


def predict_q_values(model, state):

    features = np.array([
        encode(state, action)
        for action in range(NUMBER_OF_ACTIONS)
    ])

    return model.predict(features)


def train(episodes=1000):

    if episodes < 1:
        raise ValueError("episodes must be at least 1")

    rng = random.Random(42)

    gamma = GAMMA
    epsilon = EPSILON_START

    # Incremental linear model for Q-values.
    model = SGDRegressor(
        loss="squared_error",
        penalty=None,
        fit_intercept=False,
        learning_rate="constant",
        eta0=LEARNING_RATE,
        random_state=42,
    )

    # Initialize before calling predict().
    model.partial_fit(
        np.zeros((1, NUMBER_OF_FEATURES)),
        np.array([0.0]),
    )

    successes = 0
    rewards = []

    # Training
    for _ in range(episodes):

        state = START
        total = 0

        for _ in range(MAX_STEPS_PER_EPISODE):

            # Exploration and exploitation
            if rng.random() < epsilon:
                action = rng.randrange(NUMBER_OF_ACTIONS)
            else:
                q_values = predict_q_values(model, state)

                best_actions = np.flatnonzero(
                    q_values == q_values.max()
                ).tolist()

                action = rng.choice(best_actions)

            # Take action
            next_state, reward, terminated = step(state, action)

            # Calculate target
            if terminated:
                target = float(reward)
            else:
                next_q_values = predict_q_values(model, next_state)
                target = reward + gamma * float(next_q_values.max())

            # Learn from the transition
            features = encode(state, action).reshape(1, -1)

            model.partial_fit(
                features,
                np.array([target])
            )

            state = next_state
            total += reward

            if terminated:
                successes += 1
                break

        # Record reward from the episode
        rewards.append(total)

        # Reduce exploration
        epsilon = max(EPSILON_MIN, epsilon * EPSILON_DECAY)

    # Evaluate without updating the model.
    state = START
    path = [state]
    steps = []

    for number in range(1, MAX_STEPS_PER_EPISODE + 1):

        q_values = predict_q_values(model, state)
        action = int(np.argmax(q_values))

        next_state, reward, terminated = step(state, action)

        steps.append({
            "number": number, "state": state,
            "action": ACTION_NAMES[action],
            "next_state": next_state, "reward": reward,
            "cell_type": cell_type(next_state),
        })

        path.append(next_state)
        state = next_state

        if terminated:
            break

    reached_goal = state == GOAL

    # Build a display table from model predictions.
    q_table = []
    for row in range(ROWS):
        for column in range(COLUMNS):
            position = (row, column)
            if GRID[row][column] != CELL_WALL and position != GOAL:
                q_table.append({
                    "state": position,
                    "action_values": predict_q_values(
                        model, position
                    ).tolist(),
                })

    return {
        "episodes": episodes,
        "successes": successes,
        "final_average": round(
            sum(rewards[-100:]) / len(rewards[-100:]), 2
        ),
        "final_epsilon": round(epsilon, 4),
        "reached_goal": reached_goal,
        "path": path,
        "steps": steps,
        "q_table": q_table,
    }
