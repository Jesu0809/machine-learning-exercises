import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {
  ClassMetrics,
  DatasetPage,
  LogRegInfo,
  LogRegRecord,
  LogRegResult,
} from '../models/classification.model';

@Injectable({ providedIn: 'root' })
export class LogisticRegressionService {
  private readonly http = inject(HttpClient);

  classify(ratio: number): Observable<LogRegResult> {
    return this.http.post<LogRegResult>('/api/logreg/classify', { ratio });
  }

  getModelInfo(): Observable<LogRegInfo> {
    return this.http.get<LogRegInfo>('/api/logreg/model-info');
  }

  getMetrics(): Observable<ClassMetrics> {
    return this.http.get<ClassMetrics>('/api/logreg/metrics');
  }

  getDataset(page: number, limit: number): Observable<DatasetPage<LogRegRecord>> {
    return this.http.get<DatasetPage<LogRegRecord>>(
      `/api/logreg/dataset?page=${page}&limit=${limit}`,
    );
  }

  scatterPlotUrl(ratio?: number | null): string {
    return ratio == null
      ? '/api/logreg/scatter-plot'
      : `/api/logreg/scatter-plot?predict=${ratio}`;
  }

  confusionPlotUrl(): string {
    return '/api/logreg/confusion-plot';
  }

  sigmoidPlotUrl(): string {
    return '/api/logreg/sigmoid-plot';
  }
}
