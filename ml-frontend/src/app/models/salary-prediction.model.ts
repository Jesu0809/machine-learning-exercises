export interface SalaryPredictionRequest {
  years: number;
}

export interface SalaryPredictionResponse {
  result: number;
  years: number;
  slope: number;
  intercept: number;
  equation: string;
  withinRange: boolean;
  xMin: number;
  xMax: number;
}

export interface ModelInfo {
  slope: number;
  intercept: number;
  r2: number;
  records: number;
  xMin: number;
  xMax: number;
  xMean: number;
  yMin: number;
  yMax: number;
  yMean: number;
  equation: string;
  xName: string;
  yName: string;
  xUnit: string;
  yUnit: string;
}
