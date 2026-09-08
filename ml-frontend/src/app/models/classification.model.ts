export interface ConfusionMatrix {
  trueNegatives: number;
  falsePositives: number;
  falseNegatives: number;
  truePositives: number;
}

export interface ClassMetrics {
  confusionMatrix: ConfusionMatrix;
  matrix: number[][];
  accuracy: number;
  precision: number;
  recall: number;
  f1Score: number;
  testRecords: number;
  trainAccuracy?: number;
}

export interface DatasetPage<T> {
  records: T[];
  page: number;
  limit: number;
  totalRecords: number;
  totalPages: number;
}

export interface LogRegInfo {
  records: number;
  trainRecords: number;
  testRecords: number;
  featureName: string;
  featureUnit: string;
  targetName: string;
  classLabels: Record<string, string>;
  positiveClass: number;
  coefficient: number;
  intercept: number;
  threshold: number;
  xMin: number;
  xMax: number;
  xMean: number;
  classCounts: Record<string, number>;
  source: string;
}

export interface LogRegResult {
  input: number;
  predictedClass: number;
  label: string;
  probabilityHighRisk: number;
  withinRange: boolean;
}

export interface LogRegRecord {
  ratio: number;
  defaulted: number;
}

export interface TreeInfo {
  records: number;
  trainRecords: number;
  testRecords: number;
  features: string[];
  featureUnits: Record<string, string>;
  targetName: string;
  classLabels: Record<string, string>;
  positiveClass: number;
  maxDepth: number;
  treeDepth: number;
  leaves: number;
  featureImportances: Record<string, number>;
  ranges: Record<string, { min: number; max: number }>;
  classCounts: Record<string, number>;
  source: string;
}

export interface TreeInput {
  annual_income: number;
  debt_to_income_ratio: number;
  credit_history_length: number;
  open_credit_lines: number;
}

export interface TreeResult {
  input: Record<string, number>;
  predictedClass: number;
  label: string;
  probabilityApproved: number;
}

export interface TreeRecord extends TreeInput {
  approved: number;
}
