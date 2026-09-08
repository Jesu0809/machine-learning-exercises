import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import {
  ClassMetrics,
  DatasetPage,
  TreeInfo,
  TreeInput,
  TreeRecord,
  TreeResult,
} from '../models/classification.model';

@Injectable({ providedIn: 'root' })
export class DecisionTreeService {
  private readonly http = inject(HttpClient);

  classify(values: TreeInput): Observable<TreeResult> {
    return this.http.post<TreeResult>('/api/tree/classify', values);
  }

  getModelInfo(): Observable<TreeInfo> {
    return this.http.get<TreeInfo>('/api/tree/model-info');
  }

  getMetrics(): Observable<ClassMetrics> {
    return this.http.get<ClassMetrics>('/api/tree/metrics');
  }

  getDataset(page: number, limit: number): Observable<DatasetPage<TreeRecord>> {
    return this.http.get<DatasetPage<TreeRecord>>(
      `/api/tree/dataset?page=${page}&limit=${limit}`,
    );
  }

  scatterPlotUrl(values?: TreeInput | null): string {
    if (!values) {
      return '/api/tree/scatter-plot';
    }
    const query = new URLSearchParams(
      Object.entries(values).map(([key, value]) => [key, String(value)]),
    ).toString();
    return `/api/tree/scatter-plot?${query}`;
  }

  confusionPlotUrl(): string {
    return '/api/tree/confusion-plot';
  }

  importancePlotUrl(): string {
    return '/api/tree/importance-plot';
  }

  treePlotUrl(): string {
    return '/api/tree/tree-plot';
  }
}
