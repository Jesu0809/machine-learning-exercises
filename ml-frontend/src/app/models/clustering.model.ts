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
