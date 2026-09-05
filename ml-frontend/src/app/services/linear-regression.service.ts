import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ModelInfo, SalaryPredictionResponse } from '../models/salary-prediction.model';
import { SalaryDataResponse } from '../models/salary-data.model';

@Injectable({ providedIn: 'root' })
export class LinearRegressionService {
  private readonly http = inject(HttpClient);

  calculateSalaryPrediction(years: number): Observable<SalaryPredictionResponse> {
    return this.http.post<SalaryPredictionResponse>('/api/predict-salary', { years });
  }

  getModelInfo(): Observable<ModelInfo> {
    return this.http.get<ModelInfo>('/api/model-info');
  }

  getSalaryData(page: number, limit: number): Observable<SalaryDataResponse> {
    return this.http.get<SalaryDataResponse>(`/api/salary-data?page=${page}&limit=${limit}`);
  }

  regressionPlotUrl(predictYears?: number | null): string {
    return predictYears == null
      ? '/api/regression-plot'
      : `/api/regression-plot?predict=${predictYears}`;
  }
}
