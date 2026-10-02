export interface RewardTable {
  valid_move: number;
  off_grid: number;
  wall_hit: number;
  danger_zone: number;
  goal: number;
}

export interface TrainingConfig {
  episodes: number;
  gamma: number;
  epsilon_start: number;
  epsilon_min: number;
  epsilon_decay: number;
  learning_rate: number;
  max_steps_per_episode: number;
  update_every: number;
}

export interface GridInfo {
  grid: number[][];
  start: [number, number];
  goal: [number, number];
  actions: string[];
  rows: number;
  columns: number;
  rewards: RewardTable;
  training_config: TrainingConfig;
}

export interface ReinforcementStep {
  number: number;
  state: [number, number];
  action: string;
  next_state: [number, number];
  reward: number;
  cell_type: string;
}

export interface QTableRow {
  state: [number, number];
  action_values: number[];
}

export interface TrainResult {
  episodes: number;
  successes: number;
  final_average: number;
  final_epsilon: number;
  reached_goal: boolean;
  evaluation_moves: number;
  evaluation_reward: number;
  path: [number, number][];
  steps: ReinforcementStep[];
  q_table: QTableRow[];
}
