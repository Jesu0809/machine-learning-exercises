import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { SalaryPredictionResponse } from '../models/salary-prediction.model';

@Injectable({providedIn: 'root'})
export class LinearRegressionService {
  private readonly http = inject(HttpClient);

  public calculateSalaryPrediction(years: number): Observable<SalaryPredictionResponse> {
    return this.http.post<SalaryPredictionResponse>('/api/predict-salary', { years });
  }
}
