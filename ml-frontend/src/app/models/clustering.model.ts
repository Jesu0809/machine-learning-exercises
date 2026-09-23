export interface ClusterInfo {
  records: number;
  features: string[];
  featureUnits: Record<string, string>;
  k: number;
  clusterNames: Record<string, string>;
  clusterSizes: Record<string, number>;
  centroids: Record<string, Record<string, number>>;
  silhouetteScore: number;
  inertia: number;
  source: string;
}

export interface ClusterInput {
  annual_income: number;
  debt_to_income_ratio: number;
  credit_history_length: number;
  open_credit_lines: number;
}

export interface ClusterResult {
  input: Record<string, number>;
  cluster: number;
  clusterName: string;
  distanceToCentroid: number;
}

export interface ClusterRecord extends ClusterInput {
  approved: number;
  cluster: number;
}

export interface ClusterMetrics {
  inertia: number;
  silhouetteScore: number;
  clusterSizes: Record<string, number>;
  clusterPercentages: Record<string, number>;
  approvalRateByCluster: Record<string, number>;
  clusterNames: Record<string, string>;
}

export interface ManualClusteringContext {
  records: number;
  featureX: string;
  featureXUnit: string;
  featureY: string;
  featureYUnit: string;
  k: number;
  iterations: number;
  clusterNames: Record<string, string>;
  source: string;
}

export interface ManualCentroid {
  cluster: number;
  name?: string;
  debt_to_income_ratio: number;
  annual_income_k: number;
}

export interface ManualRecord {
  index: number;
  debt_to_income_ratio: number;
  annual_income_k: number;
  distanceToCluster0: number;
  distanceToCluster1: number;
  distanceToCluster2: number;
  assignedCluster: number;
}

export interface ManualIteration {
  iteration: number;
  records: ManualRecord[];
  centroidsBefore: ManualCentroid[];
  centroidsAfter: ManualCentroid[];
  variance: Record<string, number>;
  clusterSizes: Record<string, number>;
}

export interface ManualVarianceComparison {
  iterations: number[];
  varianceByCluster: Record<string, number[]>;
  totalVariance: number[];
}
